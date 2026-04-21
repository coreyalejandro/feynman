---
id: "BUILD-TEST-0001"
status: "Draft"
state: "draft_build"
scope:
  project: "pilot"
  change_summary: "Establish the minimal I’m Just a Build packet format and verifier."
  safety_critical: false
evidence:
  required:
    - "verification.md"
    - "decision.md"
    - "evidence/index.md"
  present:
    - "verification.md"
    - "decision.md"
    - "evidence/index.md"
---

# BUILD_CONTRACT

## Intent

Define and verify a minimal BUILD_CONTRACT packet that can be advanced through the “I’m Just a Build” state machine.

## Proposed change

- Introduce `tlc-next/docs/constitution/IM_JUST_A_BUILD_PIPELINE.md`
- Provide schema + verifier

