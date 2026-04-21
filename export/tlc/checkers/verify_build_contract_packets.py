#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


RE_DOC_BASENAME_LOWER_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def read_frontmatter_block(md_text: str) -> str | None:
    if not md_text.startswith("---"):
        return None
    lines = md_text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]) + "\n"
    return None


def parse_minimal_yaml_kv(frontmatter: str) -> dict:
    out: dict = {}
    stack: list[tuple[int, dict]] = [(0, out)]
    for raw in frontmatter.splitlines():
        if not raw.strip():
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        while stack and indent < stack[-1][0]:
            stack.pop()
        target = stack[-1][1]
        if value == "":
            new_obj: dict = {}
            target[key] = new_obj
            stack.append((indent + 2, new_obj))
        else:
            if value.lower() in {"true", "false"}:
                target[key] = value.lower() == "true"
            elif value == "null":
                target[key] = None
            else:
                target[key] = value.strip('"')
    return out


def load_rules(rules_path: Path) -> dict:
    return json.loads(rules_path.read_text(encoding="utf-8"))


def validate_doc_basename(path: Path) -> list[Finding]:
    findings: list[Finding] = []
    basename = path.name
    if basename in {"README.md", "INDEX.md", "HELP.md"}:
        return findings
    if basename.isupper() or (basename.endswith(".md") and basename[:-3].replace("_", "").isupper()):
        return findings
    if not RE_DOC_BASENAME_LOWER_KEBAB.match(basename):
        findings.append(
            Finding(
                code="DOC_BASENAME_INVALID",
                path=str(path),
                message="Doc basename must be lower-kebab-case.md unless canonical ALL-CAPS.",
            )
        )
    return findings


def required_exists(packet_dir: Path, required: str) -> bool:
    if required.endswith("/"):
        return (packet_dir / required[:-1]).is_dir()
    return (packet_dir / required).exists()


def validate_packet(packet_dir: Path, rules: dict) -> list[Finding]:
    findings: list[Finding] = []
    bc = packet_dir / "BUILD_CONTRACT.md"
    if not bc.exists():
        return [Finding(code="MISSING_BUILD_CONTRACT", path=str(packet_dir), message="Missing BUILD_CONTRACT.md")]

    fm = read_frontmatter_block(bc.read_text(encoding="utf-8"))
    if fm is None:
        return [Finding(code="MISSING_FRONTMATTER", path=str(bc), message="Missing YAML frontmatter")]

    meta = parse_minimal_yaml_kv(fm)
    state = meta.get("state")
    states = set(rules["state_machine"]["states"])
    if state not in states:
        findings.append(Finding(code="INVALID_STATE", path=str(bc), message=f"Invalid state: {state!r}"))

    baseline = rules["required_artifacts"]["baseline"]
    for req in baseline:
        if not required_exists(packet_dir, req if req != "evidence/" else "evidence/"):
            findings.append(Finding(code="MISSING_REQUIRED_ARTIFACT", path=str(packet_dir), message=f"Missing: {req}"))

    per_state = rules["required_artifacts"].get("per_state", {})
    for req in per_state.get(state, []):
        if not required_exists(packet_dir, req if req != "evidence/" else "evidence/"):
            findings.append(Finding(code="MISSING_STATE_ARTIFACT", path=str(packet_dir), message=f"Missing for {state}: {req}"))

    safety_critical = False
    scope = meta.get("scope")
    if isinstance(scope, dict) and isinstance(scope.get("safety_critical"), bool):
        safety_critical = scope["safety_critical"]

    if safety_critical and state in {"reconciliation", "sign_and_bind", "enforced"}:
        decision = packet_dir / "decision.md"
        if decision.exists() and "safety_vote" not in decision.read_text(encoding="utf-8"):
            findings.append(
                Finding(
                    code="SAFETY_VOTE_REQUIRED",
                    path=str(decision),
                    message="Safety-critical packets must record safety_vote before reconciliation/sign/enforce.",
                )
            )

    return findings


def main() -> int:
    root = Path(os.environ.get("TLC_EXPORT_ROOT", Path(__file__).resolve().parents[1]))
    rules_path = root / "constitution" / "rules.json"
    if not rules_path.exists():
        print(f"FAIL: missing rules.json at {rules_path}", file=sys.stderr)
        return 2
    rules = load_rules(rules_path)

    findings: list[Finding] = []

    # docs casing checks (export-side)
    docs_root = root / "docs"
    if docs_root.exists():
        for p in docs_root.rglob("*.md"):
            findings.extend(validate_doc_basename(p))

    # packet checks (export-side example packets)
    packets_root = root / "example_packets"
    if packets_root.exists():
        for packet in packets_root.iterdir():
            if packet.is_dir():
                findings.extend(validate_packet(packet, rules))

    if findings:
        for f in findings:
            print(f"{f.code}\t{f.path}\t{f.message}")
        return 1

    print("PASS: export/tlc checker passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

