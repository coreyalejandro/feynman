---
document_type: "Constitutional"
id: "DOC-IJAB-PIPELINE-001"
repo_scope: "Cross-Repo"
authority_level: "L4"
truth_rank: 1
status: "Draft"
canonical_path: "docs/constitution/IM_JUST_A_BUILD_PIPELINE.md"
next_file: "docs/constitution/TERMINOLOGY.md"
last_verified:
  commit: null
  timestamp: null
metadata:
  est_time_minutes: 12
  cognitive_load: "Medium"
  requires_interruption_buffer: true
---

# IM_JUST_A_BUILD_PIPELINE

This document defines a **constitutionally-regulated, single-pass BUILD_CONTRACT pipeline** that mirrors the familiar Schoolhouse Rock lifecycle:

> “I’m just a bill…” → remix: **“I’m just a build…”**

The goal is **one-thing-well governance**: every governed change is represented as a BUILD_CONTRACT that moves through a strict, legible set of stages with **no hidden transitions** and **fail-closed** enforcement.

## Core mapping (metaphor → SDLC)

| Bill-to-law stage | “I’m Just a Build” stage | R&D lane | Output artifact class |
| --- | --- | --- | --- |
| Idea | DraftBuild | Research | Proposal + intent |
| Committee | CommitteeReview | Research | Evidence plan + hazard analysis |
| House vote | ProductVote | Results | Decision record (product) |
| Senate vote | SafetyVote | Results | Decision record (safety) |
| Reconciliation | Reconciliation | Results | Resolved diff + final contract text |
| Executive sign | SignAndBind | Product | Binding to live governance surface |
| Law | Enforced | Product | Enforced build guardrails |
| Court review (anytime) | ConstitutionalReview | Any | Strike / remedy / sunset |

## Normative invariants

- **INVARIANT_IJAB_01 (Single entrypoint)**: Any governed work begins as a `BUILD_CONTRACT` (no bypass path).
- **INVARIANT_IJAB_02 (Explicit state machine)**: Each BUILD_CONTRACT has a single `state` value and a monotonic transition history.
- **INVARIANT_IJAB_03 (Fail closed)**: Missing required artifacts or verification = deny / block advancement.
- **INVARIANT_IJAB_04 (Evidence-bound decisions)**: Any approval step must cite evidence pointers (files, hashes, or URLs) sufficient to reproduce the judgment.
- **INVARIANT_IJAB_05 (Monotropic continuity)**: All required context for a transition must live in the BUILD_CONTRACT packet; no “go read the chat” dependencies.

## State machine (v1)

Allowed states are:

- `draft_build`
- `committee_review`
- `product_vote`
- `safety_vote`
- `reconciliation`
- `sign_and_bind`
- `enforced`
- `struck`
- `sunset`

Allowed transitions:

- `draft_build` → `committee_review`
- `committee_review` → `product_vote`
- `committee_review` → `safety_vote` (if safety-critical)
- `product_vote` → `reconciliation`
- `safety_vote` → `reconciliation`
- `reconciliation` → `sign_and_bind`
- `sign_and_bind` → `enforced`
- `enforced` → `sunset`
- Any → `struck` (constitutional review outcome; must include remedy notes)

## Required packet artifacts (per BUILD_CONTRACT)

Minimum packet (must exist to advance beyond `draft_build`):

- `BUILD_CONTRACT.md` (the bill/build text)
- `verification.md` (verification log; may be `BLOCKED` at early stages but must exist)
- `decision.md` (decision record; can be `pending` before votes)
- `evidence/` directory (may be empty in draft, but must exist once `committee_review` begins)

## Enforcement interface

This repository provides:

- A JSON schema for `BUILD_CONTRACT.md` frontmatter and required fields
- A deterministic verifier script that validates:
  - state transitions
  - required artifacts per state
  - casing + canonical path rules for docs

