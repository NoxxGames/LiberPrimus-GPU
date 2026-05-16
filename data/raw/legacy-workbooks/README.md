# data/raw/legacy-workbooks

## Purpose

Stores local legacy analysis workbook drops as immutable raw artefacts.

## What belongs here

Legacy workbook files such as `tranlsations.xlsx` when explicitly supplied by the user and hash-locked under `data/locks/legacy-workbooks/`.

## What does not belong here

Canonical corpus data, generated normalized records, extraction output, reports, logs, or rewritten workbook copies.

## Codex modification policy

Codex may add README and `.gitkeep` placeholders and may move an untracked user-supplied workbook here without changing its bytes. Codex must not commit raw workbook files.

## Stage 0B restrictions

Workbooks here are non-canonical legacy analysis sources. They are ignored by Git and must not be treated as solved-page proof or final Gematria mapping evidence.
