# data/normalized/legacy-workbook

## Purpose

Ignored local output directory for generated legacy workbook extraction records.

## What belongs here

Generated sheet inventories, solved-delta JSONL, Prime Sums JSONL, formula JSONL, summaries, and warning files from the parser.

## What does not belong here

Canonical corpus files, raw workbooks, committed generated outputs, databases, or result claims.

## Codex modification policy

Codex may write generated outputs here during smoke validation, but only this README and `.gitkeep` should be committed.

## Stage 0B restrictions

Generated workbook-derived records are artefacts, not source truth, and remain ignored unless explicitly promoted by a later policy.
