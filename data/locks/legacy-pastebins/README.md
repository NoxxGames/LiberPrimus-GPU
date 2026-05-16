# data/locks/legacy-pastebins

## Purpose

Stores committed checksum and provenance metadata for ignored legacy Pastebin raw text files.

## What belongs here

Small `.sha256` and metadata JSON files describing local legacy Pastebin artefacts.

## What does not belong here

Raw text files, generated normalized JSON/JSONL, reports, logs, or inferred corpus outputs.

## Codex modification policy

Codex may add or update lock metadata when the corresponding local source file is present and unchanged.

## Stage 0C restrictions

Lock metadata describes non-canonical legacy sources only.
