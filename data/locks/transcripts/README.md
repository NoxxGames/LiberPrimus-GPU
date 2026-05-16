# Transcript Locks

Purpose: stores committed checksum and provenance metadata for raw transcript source files.

What belongs here: SHA-256 files and JSON metadata for transcript sources mirrored under `data/raw/transcripts/`.

What does not belong here: raw transcript files, generated alignment outputs, or mutable local notes.

Codex may update lock metadata only after verifying the raw file path, source URL, file size, SHA-256, and non-canonical Stage 0D status.
