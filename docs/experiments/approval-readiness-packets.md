# Approval-Readiness Packets

## Purpose

Approval-readiness packets summarize whether a proposal is ready for human review. They are generated review artifacts, not approvals and not execution records.

## Packet Contents

A packet records proposal status, approval status, corpus-slice summary, transform-space summary, candidate-count bounds, safety gate summary, review checklist summary, approval requirements, blocking conditions, risk summary, generated output preview, and result-store preview.

## Blocking Conditions

Stage 2I packets always block execution for the first real proposal because approval is pending and a separate human decision is required.

Common blockers include missing approval, pending approval, non-matching proposal hash, missing checklist, invalid bounds, or any enabled execution/search/candidate-generation/scoring/CUDA flag.

## Risk Summary

Packets flag that the proposal touches reviewable unsolved metadata. They also record that canonical corpus activation and page-boundary finalization remain false.

## Generated-Output Policy

Generated packets are ignored under `experiments/results/approval-readiness/stage2i/`. They must not be committed, and they must not include raw unsolved text or candidate plaintext.

## Review Process

Run the approval-readiness CLI, inspect the JSON and Markdown packet locally, then make a separate human decision in a later stage. Stage 2I does not approve, execute, score, or rank anything.
