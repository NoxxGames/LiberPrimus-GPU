# Token Case Review Pack V2

Stage 5AU rebuilds the Stage 5AT token-case review pack because the original pack was count-valid but not usable for reliable human decisions. The v2 pack is a local, ignored review surface under `human-review-packs/stage5au/token-case-review-v2/`.

The committed records are metadata only. The generated HTML, crops, overlays, review sheets, ZIP archive, and JSON reports remain ignored generated outputs.

Stage 5AV later consumed the filled local `decision-template.yaml` from that pack. The filled file remains ignored; committed Stage 5AV records store only the ingest hash, validation status, keep-current confirmations, unresolved variant branches, reviewer-extra possible tokens, compact branch manifest, and guardrail metadata.

## Coverage

- Case-review challenges rendered: `203`.
- Canonical-transcription challenges rendered: `212`.
- Review sheets: one per active ambiguity class.
- Per-page pages: pages `49`, `50`, and `51`.
- Page-transition and canonical-review pages are present.

## Boundaries

Derived crops and overlays are review aids, not source truth. Stage 5AU does not resolve token identity, fill decisions, change canonical transcription, run OCR, run AI/ML or LLM/vision reading, run semantic image interpretation, run hidden-content image forensics, run stego, search hashes, decode, run CUDA, benchmark, execute scored experiments, or make solve claims.

Stage 5AV does not reinterpret the crops either. It preserves human unresolved decisions as variant-branch metadata and leaves the Stage 5AP canonical transcription unchanged because the integrated decision file contains zero `change_token` records.
