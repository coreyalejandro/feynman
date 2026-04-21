---
description: Create or update an "I’m Just a Build" BUILD_CONTRACT packet and validate it against governance rules.
args: <slug>
section: Governance Workflows
topLevelCli: true
---
Start an “I’m Just a Build” BUILD_CONTRACT for: $@

Derive a short slug (lowercase, hyphens, ≤5 words). Use this slug for all artifacts.

Required artifacts (governed location):
- `governance/bills/<slug>/bill.md`
- `governance/bills/<slug>/decision.md`
- `governance/bills/<slug>/verification.md`
- `governance/bills/<slug>/evidence/index.md`

Workflow:
1. Create the packet directory under `governance/bills/<slug>/`.
2. Write `bill.md` with frontmatter including `id`, `status`, `state`, and `scope`.
3. Write `decision.md` and `verification.md`.
4. Ensure `evidence/index.md` exists (can be a stub at draft stage).
5. Run the export checker (if available) and fail closed if it reports missing artifacts.
6. Update `governance/ledger/ledger.md` with a new row for the bill/build.

Never claim completion unless all required artifacts exist on disk.

