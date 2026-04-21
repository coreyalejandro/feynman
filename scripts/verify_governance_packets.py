#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    code: str
    path: str
    message: str


def load_rules(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def required_exists(base: Path, rel: str) -> bool:
    if rel.endswith("/"):
        return (base / rel[:-1]).is_dir()
    return (base / rel).exists()


def check_bill_packet(root: Path, slug: str, rules: dict) -> list[Finding]:
    findings: list[Finding] = []
    packet = root / "governance" / "bills" / slug
    if not packet.is_dir():
        return [Finding(code="MISSING_PACKET_DIR", path=str(packet), message="Missing packet directory")]

    # Baseline artifacts
    baseline = rules["required_artifacts"]["baseline"]
    for req in baseline:
        concrete = req.replace("governance/bills/<slug>/", f"governance/bills/{slug}/")
        if not required_exists(root, concrete):
            findings.append(Finding(code="MISSING_REQUIRED_ARTIFACT", path=str(packet), message=f"Missing: {concrete}"))

    return findings


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    rules_path = root / "governance" / "constitution" / "rules.json"
    if not rules_path.exists():
        print(f"FAIL: missing {rules_path}", file=sys.stderr)
        return 2
    rules = load_rules(rules_path)

    bills_root = root / "governance" / "bills"
    if not bills_root.exists():
        print("PASS: no governance/bills directory (nothing to verify)")
        return 0

    findings: list[Finding] = []
    for p in bills_root.iterdir():
        if p.is_dir():
            findings.extend(check_bill_packet(root, p.name, rules))

    if findings:
        for f in findings:
            print(f"{f.code}\t{f.path}\t{f.message}")
        return 1

    print("PASS: governance packets verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

