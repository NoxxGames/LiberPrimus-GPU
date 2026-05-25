# Canonical Transcription Challenge Set

The Stage 5AT canonical-transcription challenge set records review prompts around token-case ambiguity while preserving the Stage 5AP canonical 32x8 transcription.

The challenge set is not a replacement transcript. It is a human-review queue that records where case ambiguity, page transitions, and control tokens should be inspected. Stage 5AT writes `212` canonical-transcription challenge records and keeps `canonical_transcription_changed=false`.

Future integration must preserve the distinction between:

- the committed Stage 5AP canonical transcription;
- Stage 5AR original-image coordinates;
- Stage 5AT human-review challenges and generated crops;
- Stage 5AU human decision files, once manually filled.

No OCR, AI/ML, LLM vision, semantic image interpretation, hidden-content forensics, or automatic case resolution may populate the decision fields.
