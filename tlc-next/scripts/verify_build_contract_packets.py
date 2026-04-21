#!/usr/bin/env python3

from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_STATES = [
    "draft_build",
    "committee_review",
    "product_vote",
    "safety_vote",
    "reconciliation",
    "sign_and_bind",
    "enforced",
    "struck",
    "sunset",
]

ALLOWED_TRANSITIONS = {
    ("draft_build", "committee_review"),
    ("committee_review", "product_vote"),
    ("committee_review", "safety_vote"),
    ("product_vote", "reconciliation"),
    ("safety_vote", "reconciliation"),
    ("reconciliation", "sign_and_bind"),
    ("sign_and_bind", "enforced"),
    ("enforced", "sunset"),
}

ANY_TO_STRUCK = "struck"

RE_DOC_BASENAME_LOWER_KEBAB = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


@dataclass(frozen=True)
class Finding:
    code: str
    message: str
    path: str


def read_frontmatter_block(md_text: str) -> str | None:
    if not md_text.startswith("---"):
        return None
    parts = md_text.split("\n")
    if len(parts) < 3:
        return None
    # Find second delimiter line '---'
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            return "\n".join(parts[1:i]) + "\n"
    return None


def parse_minimal_yaml_kv(frontmatter: str) -> dict[str, Any]:
    """
    Minimal parser: supports simple 'key: value' pairs and nested one-level blocks used here.
    This is intentionally strict and not a general YAML parser (keeps verifier deterministic).
    """
    out: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(0, out)]
    for raw in frontmatter.splitlines():
        if not raw.strip():
            continue
        if raw.strip().startswith("#"):
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
            new_obj: dict[str, Any] = {}
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


def validate_doc_casing(doc_path: Path) -> list[Finding]:
    findings: list[Finding] = []
    basename = doc_path.name
    if basename in {"README.md", "INDEX.md", "HELP.md"}:
        return findings
    # Canonical docs may be ALL CAPS in TLC; we allow ALL CAPS + underscores as a special case.
    if basename.isupper() or (basename.endswith(".md") and basename[:-3].replace("_", "").isupper()):
        return findings
    if not RE_DOC_BASENAME_LOWER_KEBAB.match(basename):
        findings.append(
            Finding(
                code="DOC_BASENAME_INVALID",
                message="Doc basename must be lower-kebab-case.md unless it is a canonical ALL-CAPS doc.",
                path=str(doc_path),
            )
        )
    return findings


def validate_build_contract_packet(packet_dir: Path, schema: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    bc_path = packet_dir / "BUILD_CONTRACT.md"
    if not bc_path.exists():
        return [Finding(code="MISSING_BUILD_CONTRACT", message="Missing BUILD_CONTRACT.md", path=str(packet_dir))]

    text = bc_path.read_text(encoding="utf-8")
    fm = read_frontmatter_block(text)
    if fm is None:
        return [Finding(code="MISSING_FRONTMATTER", message="BUILD_CONTRACT.md missing YAML frontmatter block", path=str(bc_path))]

    meta = parse_minimal_yaml_kv(fm)
    state = meta.get("state")
    if state not in ALLOWED_STATES:
        findings.append(Finding(code="INVALID_STATE", message=f"Invalid state '{state}'", path=str(bc_path)))

    # Artifact requirements per stage (minimal v1)
    required = ["decision.md", "verification.md", "evidence"]
    for item in required:
        p = packet_dir / item
        if item == "evidence":
            if not p.exists() or not p.is_dir():
                findings.append(Finding(code="MISSING_EVIDENCE_DIR", message="Missing evidence/ directory", path=str(packet_dir)))
        else:
            if not p.exists():
                findings.append(Finding(code="MISSING_REQUIRED_ARTIFACT", message=f"Missing required artifact: {item}", path=str(packet_dir)))

    # Transition checks (if transitions are present)
    transitions_raw = meta.get("transitions")
    # This minimal YAML parser does not support arrays; v1 accepts absence and relies on file-level invariants later.
    if transitions_raw is not None:
        findings.append(
            Finding(
                code="TRANSITIONS_UNSUPPORTED_IN_V1_PARSER",
                message="Frontmatter 'transitions' is reserved for v2 YAML parsing; keep transition history in decision.md for now.",
                path=str(bc_path),
            )
        )

    # Safety critical requires safety_vote (enforced only once state reaches reconciliation+)
    safety_critical = meta.get("scope", {}).get("safety_critical") if isinstance(meta.get("scope"), dict) else False
    if safety_critical and state in {"reconciliation", "sign_and_bind", "enforced"}:
        decision_text = (packet_dir / "decision.md").read_text(encoding="utf-8") if (packet_dir / "decision.md").exists() else ""
        if "safety_vote" not in decision_text:
            findings.append(
                Finding(
                    code="MISSING_SAFETY_VOTE_MARKER",
                    message="Safety-critical contract must record a safety_vote outcome in decision.md before reconciliation/sign/enforce.",
                    path=str(packet_dir / "decision.md"),
                )
            )

    return findings


def load_schema(schema_path: Path) -> dict[str, Any]:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def main() -> int:
    root = Path(os.environ.get("TLC_NEXT_ROOT", Path(__file__).resolve().parents[1]))
    schema_path = root / "schemas" / "build_contract.schema.json"
    if not schema_path.exists():
        print(f"FAIL: missing schema at {schema_path}", file=sys.stderr)
        return 2
    schema = load_schema(schema_path)

    findings: list[Finding] = []

    # Doc casing checks under docs/
    docs_root = root / "docs"
    if docs_root.exists():
        for p in docs_root.rglob("*.md"):
            findings.extend(validate_doc_casing(p))

    # Packet checks under projects/ (TLC-shaped)
    projects_root = root / "projects"
    if projects_root.exists():
        for project in projects_root.iterdir():
            if not project.is_dir():
                continue
            findings.extend(validate_build_contract_packet(project, schema))

    if findings:
        for f in findings:
            print(f"{f.code}\t{f.path}\t{f.message}")
        return 1

    print("PASS: tlc-next verifier checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

