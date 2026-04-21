---
document_type: "Architectural"
id: "DOC-ARCH-BCP-001"
status: "Draft"
canonical_path: "docs/architecture/build-contract-packet.md"
next_file: "docs/architecture/state-machine.md"
last_verified:
  commit: null
  timestamp: null
---

# build-contract-packet

This document describes the **one-thing-well BUILD_CONTRACT packet**: the minimal, self-contained artifact set that can be reviewed, verified, and promoted through the “I’m Just a Build” pipeline without external context.

## Packet layout (filesystem)

```text
projects/<project_slug>/
  BUILD_CONTRACT.md
  decision.md
  verification.md
  evidence/
    index.md
    ...
```

## Monotropic design constraints

- **Single-thread**: one packet = one change lane.
- **Local completeness**: reviewers should not need to cross-navigate unrelated directories.
- **No hidden state**: state + transitions are explicit in `BUILD_CONTRACT.md`.

