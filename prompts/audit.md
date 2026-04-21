---
description: Compare a paper's claims against its public codebase and identify mismatches, omissions, and reproducibility risks.
args: <item>
section: Research Workflows
topLevelCli: true
---
Audit the paper and codebase for: $@

Derive a short slug from the audit target (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.
Derive a run timestamp in local time: `YYYY-MM-DD_HHMM`. Define `run_id = <timestamp>_<slug>`. Use `run_id` for all artifact filenames so files sort by recency.

Requirements:
- Before starting, outline the audit plan: which paper, which repo, which claims to check. Write the plan to `outputs/.plans/<run_id>.md`. Briefly summarize the plan to the user and continue immediately. Do not ask for confirmation or wait for a proceed response unless the user explicitly requested plan review.
- Use the `researcher` subagent for evidence gathering and the `verifier` subagent to verify sources and add inline citations when the audit is non-trivial.
- Compare claimed methods, defaults, metrics, and data handling against the actual code.
- Call out missing code, mismatches, ambiguous defaults, and reproduction risks.
- Save exactly one audit artifact to `outputs/<run_id>-audit_FINAL.md`.
- End with a `Sources` section containing paper and repository URLs.
