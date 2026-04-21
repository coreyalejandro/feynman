---
description: Set up a recurring or deferred research watch on a topic, company, paper area, or product surface.
args: <topic>
section: Research Workflows
topLevelCli: true
---
Create a research watch for: $@

Derive a short slug from the watch topic (lowercase, hyphens, no filler words, ≤5 words). Use this slug for all files in this run.
Derive a run timestamp in local time: `YYYY-MM-DD_HHMM`. Define `run_id = <timestamp>_<slug>`. Use `run_id` for all artifact filenames so files sort by recency.

Requirements:
- Before starting, outline the watch plan: what to monitor, what signals matter, what counts as a meaningful change, and the check frequency. Write the plan to `outputs/.plans/<run_id>.md`. Briefly summarize the plan to the user and continue immediately. Do not ask for confirmation or wait for a proceed response unless the user explicitly requested plan review.
- Start with a baseline sweep of the topic.
- Use `schedule_prompt` to create the recurring or delayed follow-up instead of merely promising to check later.
- Save exactly one baseline artifact to `outputs/<run_id>-baseline_FINAL.md`.
- End with a `Sources` section containing direct URLs for every source used.
