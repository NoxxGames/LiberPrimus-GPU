# User Token Case Review Decision Integration

Stage 5AV consumes the filled local Stage 5AU v2 `decision-template.yaml` and converts it into committed metadata. The decision file remains ignored at `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`; only its path, SHA-256, validation status, and derived compact records are committed.

## Integration Policy

- `keep_current` decisions confirm the current Stage 5AP token without rewriting the transcription.
- `unresolved` decisions preserve reviewer-declared `possible_tokens=...` alternatives.
- Reviewer extra possible tokens outside the generated candidates are preserved and classified separately.
- `change_token` would require explicit validation before any transcription update; Stage 5AV recorded zero changes.
- No token experiments, DWH/hash searches, decode attempts, OCR, AI/ML, LLM/vision reading, stego, CUDA, benchmarks, scored experiments, or solve claims are performed.

Stage 5AV records 203 human decisions: 126 `keep_current`, 77 `unresolved`, 0 `change_token`, and 0 `not_reviewable`.
