---
id: "BUILD-YYYY-NNNN"
status: "Draft"
state: "draft_build"
scope:
  project: "project-slug"
  change_summary: "One sentence description of what will be governed."
  safety_critical: false
evidence:
  required:
    - "decision.md"
    - "verification.md"
    - "evidence/index.md"
  present: []
---

# BUILD_CONTRACT

## Intent

State the intention as a single operational sentence.

## BillText (the build-as-bill)

Write the build contract in plain language with explicit constraints. It should be possible to deterministically decide whether it is satisfied.

## Stage gating

This contract is governed by the “I’m Just a Build” bill-to-law state machine:

- `draft_build` → `committee_review` → (`product_vote` and/or `safety_vote`) → `reconciliation` → `sign_and_bind` → `enforced`

