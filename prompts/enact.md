---
description: Enact ("sign and bind") a governed BUILD_CONTRACT packet by recording a decision and verifying required artifacts.
args: <slug>
section: Governance Workflows
topLevelCli: true
---
Enact the BUILD_CONTRACT packet for: $@

Derive the slug and locate the packet at `governance/bills/<slug>/`.

Hard requirements:
- Do not enact if `verification.md` is missing.
- Do not enact if evidence stubs are missing.
- Do not enact if a safety-critical packet lacks a recorded `safety_vote` outcome.

Workflow:
1. Confirm the packet has the baseline artifacts.
2. Confirm allowed state transition to `sign_and_bind` (or `enforced` if already signed).
3. Update `decision.md` with enactment info and evidence references.
4. Update `governance/ledger/ledger.md`.
5. Append a concise entry to `CHANGELOG.md` only if this enactment is a meaningful multi-step milestone.

Never claim completion unless the ledger reflects the updated state.

