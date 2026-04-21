---
description: Perform a constitutional review ("court") of a governed BUILD_CONTRACT packet.
args: <slug>
section: Governance Workflows
topLevelCli: true
---
Run constitutional review for: $@

Derive the slug and locate the packet at `governance/bills/<slug>/`.
Derive a run timestamp in local time: `YYYY-MM-DD_HHMM`. Define `run_id = <timestamp>_<slug>`. Use `run_id` for all artifact filenames so files sort by recency.

Required artifacts:
- `outputs/.plans/<run_id>-court-plan.md`
- `outputs/<run_id>-court_FINAL.md`

Workflow:
1. Write the plan file with: issue statement, evidence needed, checks to perform, and pass/fail criteria.
2. Inspect the packet artifacts (`bill.md`, `decision.md`, `verification.md`, `evidence/index.md`).
3. Run any available rule checker. Record its output in the court report.
4. Produce `outputs/<run_id>-court_FINAL.md` with:
   - Summary judgment (PASS / PASS WITH NOTES / BLOCKED / STRUCK)
   - Findings (FATAL / MAJOR / MINOR)
   - Required remedies (if any)
   - Evidence consulted (file paths)
5. If STRUCK, require the packet `state` be set to `struck` in a follow-up governed change.

Never claim completion unless `outputs/<run_id>-court_FINAL.md` exists.

