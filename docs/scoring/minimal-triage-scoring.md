# Minimal Triage Scoring

Stage 3A adds a small deterministic scoring function for sorting bounded CPU candidates. It is a triage aid only.

## Features

The score includes:

- Latin letter count
- Unknown symbol count
- Vowel ratio
- Hits from `data/scoring/english-common-words-tiny-v0.txt`
- Repeated-character penalty
- Printable ratio
- Entropy estimate

The word list is intentionally tiny and generic. It is not a language model, not a large dictionary, and not tuned to Liber Primus phrases.

## Non-Goals

Minimal triage scoring is not solve evidence. It does not establish plaintext correctness, page boundaries, canonical corpus status, or cryptanalytic success.

## Safety

Scoring is local, CPU-only, deterministic, and has no network or paid-service dependency. Generated score records remain part of ignored experiment output unless summarized at a high level in a research log.
