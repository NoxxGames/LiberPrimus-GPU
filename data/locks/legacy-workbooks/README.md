# data/locks/legacy-workbooks

## Purpose

Stores committed lock metadata for ignored legacy workbook artefacts.

## What belongs here

Small checksum and provenance files that identify local workbook drops without committing the raw `.xlsx`.

## What does not belong here

Raw workbooks, generated extraction JSON/JSONL, reports, logs, or databases.

## Codex modification policy

Codex may add or update lock metadata when the corresponding local workbook is present and unchanged.

## Stage 0B restrictions

Lock files describe non-canonical legacy analysis artefacts only.
