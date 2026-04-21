---
title: Governance Workflows
description: Governance-as-code workflows for the “I’m Just a Build” build-contract pipeline.
section: Reference
order: 3
---

These governance workflows implement a strict, legible pipeline modeled on Schoolhouse Rock’s “I’m Just a Bill” (remixed as “I’m Just a Build”).

They are designed to be **one-thing-well** and **fail-closed**: do not claim progress unless required artifacts exist on disk.

## Commands

| Command | Description |
| --- | --- |
| `/build-contract <slug>` | Create or update a governed build-contract packet under `governance/bills/<slug>/` |
| `/court <slug>` | Constitutional review of a governed packet (writes `outputs/<slug>-court.md`) |
| `/enact <slug>` | Enact a packet by recording decisions and updating the governance ledger |

## Required governed artifacts

For a given `<slug>`, the governed packet must include:

- `governance/bills/<slug>/bill.md`
- `governance/bills/<slug>/decision.md`
- `governance/bills/<slug>/verification.md`
- `governance/bills/<slug>/evidence/index.md`

## Export bundle (for downstream import)

The pull-ready bundle lives under `export/tlc/`:

- `export/tlc/build_contract_as_bill/` (templates)
- `export/tlc/constitution/` (rules)
- `export/tlc/checkers/` (deterministic verifiers)
- `export/tlc/example_packets/` (golden paths)

