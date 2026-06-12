# Stage 5EF Context Pack Template: doc_drift

Purpose: Audit current-truth mirror drift without changing historical evidence.

Authority:
- Authoritative current truth: `data/project-state/current-stage-state.yaml`
- Current stage: `stage-5ef`
- Next routed stage: `stage-5eg` - Stage 5EG - Source-lock number-fact review batch 006, without execution

Required Guardrails:
- Do not add source-lock evidence.
- Do not add number-fact enrichment overlays.
- Do not backfill source records.
- Do not select a target or pivot.
- Do not generate byte streams.
- Do not execute puzzle, CUDA, scoring, benchmark, image, OCR, audio, stego, Tor, or website work.
- Do not claim a solve.

Inputs To Review:
- Current-stage registry and Stage 5EF policy ledgers.
- Existing committed source records only.
- Focused validator output, if provided.

Output Shape:
- Summary of scoped records consulted.
- Exact blocker list.
- Recommended next action, if any.
- Confirmation that generated outputs remain ignored and uncommitted.

Determinism:
- This template contains no wall-clock timestamp, local path, temporary output path, or worktree-dirt snapshot.
