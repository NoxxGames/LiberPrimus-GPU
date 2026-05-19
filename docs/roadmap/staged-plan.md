# LiberPrimus-GPU Staged Plan

## Purpose

This file is the durable staged plan for LiberPrimus-GPU. It records completed work, current direction, planned stages, deferred work, and method families that should not be widened without new evidence.

## Current Project State

- Latest completed stage before this record: Stage 3Z - source-of-truth / newcomer map.
- Current stage: Stage 4A - full Discord research-bundle extraction for Deep Research.
- Canonical corpus: inactive.
- Page boundaries: reviewable.
- CUDA: deferred.
- Solve claims: none.
- Raw and generated outputs: ignored and not committed.
- Discord raw logs: local, private, ignored research material.
- Local Liber Primus page images: local third-party material, ignored and not committed.
- OutGuess: deterministic harness exists; tool/assets still need local setup and source-locking.

## Completed Stage Timeline

- Stage 0A-0E: source, profile, separator, transcript, and corpus-candidate foundations.
- Stage 1A-1D: solved-page fixtures and ten solved baselines for direct, Atbash-family, Vigenere, and prime-stream known-solved cases.
- Stage 2A-2J: transform registry, result store, CI, dry-runs, bounded execution, approval gates, and operator policy.
- Stage 3A-3J: bounded text, numeric, hash, ablation, and reranking experiments; most families were noisy, inconclusive, or negative.
- Stage 3K-3Q: archive/source records, image locks, Discord ingestion/review, visual observations, and review bundles.
- Stage 3R: Discord lead promotion with public-source corroboration and the first post-Discord manifest queue.
- Stage 3S: executed EXP-3R-003 Onion 7 explicit seed pack; result was inconclusive.
- Stage 3T: executed EXP-3R-004 GP/rune claim verifier; most exact claims verified, unsupported claims stayed quarantined.
- Stage 3U: executed EXP-3R-001 cookie SHA-256 signed-variant pack; exact matches were zero.
- Stage 3V: added OutGuess regression harness; missing tool/assets were handled as valid skips.
- Stage 3W: consolidated project state and added anti-drift checks.
- Stage 3X: modularised CLI command registration without behaviour changes.
- Stage 3Y: created the durable staged plan, research-synthesis records, method-retirement ledger, Deep Research influence records, and direction-change records.
- Stage 3Z: created source-of-truth and newcomer maps for users, Codex, Deep Research, contributors, and reviewers.

## Current Stage

Stage 4A builds a privacy-preserving full Discord research-bundle for Deep Research from local ignored Discord HTML exports and local ignored Liber Primus page images.

Stage 4A creates redacted chronological streams, channel shards, topic shards, indexes, an LP page gallery, and an SFTP-ready static site under ignored output paths. It executes no cryptanalytic experiments and makes no solve claim.

## Planned Next Stages

- Stage 4A - full Discord research-bundle extraction for Deep Research.
- Stage 4B - website-derived source-lock triage and visual observation intake.
- Stage 4C - cuneiform/dot annotation workflow.
- Stage 4D - OutGuess/audio historical fixture source-locking.
- Stage 4E - CPU batch transform API extraction.
- Stage 4F - scorer consolidation and calibration report.
- Stage 5A - CUDA planning and parity scaffolding only.

The independent review originally suggested CPU batch API extraction as Stage 4A. User direction after Discord website review moved full Discord research-bundle extraction earlier so Deep Research can work with local Discord exports in a redacted, structured form. CPU batch API extraction remains planned as Stage 4E; it is deferred, not cancelled.

## Deferred Work

- CUDA implementation and broad GPU campaigns.
- Broad unsolved-page campaigns.
- Canonical corpus activation.
- Page-boundary finalization.
- Dictionary-scale Vigenere.
- Unbounded skip-mask search.
- Broad hash cracking, hashcat, or GPU hash attacks.
- Open-ended spectrogram or image pareidolia work.
- AI, OCR, or ML as source truth.
- Live Discord, Tor, or web crawling.

## Stage 4A Direction

Stage 4A converts local admin-provided Discord HTML exports into full Deep-Research-friendly bundles. The output must be redacted, scoped, image-aware where metadata exists, and generated under ignored paths. Raw Discord logs, private attachments, usernames, user IDs, message IDs, private URLs, generated static site files, copied LP page images, thumbnails, and archives must not be committed or handed off raw.

The next planned stage after Stage 4A is Stage 4B: website-derived source-lock triage and visual observation intake, using Stage 4A bundle outputs.

## Retired Or Deprioritised Directions

- Caesar/affine widening: noisy; do not widen without new source evidence.
- Reverse/reranked affine/Caesar: noisy.
- Small motif Vigenere and LP evidence Vigenere packs: noisy.
- Historical motif Vigenere pack: noisy.
- p56-local prime offset sweeps: inconclusive/noisy; revisit only with a stronger source anchor.
- Mersenne/perfect-number tiny probe: inconclusive and low priority unless image/source evidence emerges.
- Cookie SHA-256 packs: negative for tried exact packs; do not broaden without an explicit new candidate source.
- Broad dictionary/hash cracking: deferred and prohibited without explicit scoped evidence.
- CUDA acceleration: deferred until CPU batch APIs, stable scorer definitions, parity tests, and benchmarks exist.

## Deep Research Influence Log

- Original Liber Primus GPU research report: moved the project toward reproducible GPU-ready architecture, but Stage 0-3 work kept CPU references and provenance ahead of acceleration.
- CPU method/backlog report: encouraged bounded CPU experiments, null controls, and method-specific stop conditions before any CUDA work.
- Archive/image/onion research report: promoted source-locking, exact artefact metadata, Onion 7 numeric observations, and deterministic image-review infrastructure.
- Discord corroboration and triage reports: established Discord as lead discovery only; public-source corroboration decides promotion, and raw logs remain private/ignored.
- Independent project review: recommended Stage 3W consolidation, Stage 3X CLI modularisation, and this Stage 3Y result-synthesis ledger before new experiment stages.

## Direction-Change Policy

- Any future Deep Research report or major Codex stage that changes project direction must update this file.
- If `ROADMAP.md` changes, this file must be checked and updated when relevant.
- If `STATUS.md` changes, this file must be checked and updated when relevant.
- If `AGENTS.md` changes current-stage guidance, this file must be checked and updated when relevant.
- If a method family is retired, reopened, or reprioritised, this file and `data/research/method-retirement-records-v0.yaml` must be checked.
- Direction changes must record why the prior direction changed, what evidence supports the new direction, and which public docs were updated.

## Update Policy

Every Codex stage that changes stage status, roadmap, experiment priority, method-family status, data policy, CLI behaviour, or schema/result families must update the relevant `.md` and `.txt` project-context files. At minimum, check `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, `EXPERIMENTS.md`, `RESULTS_SCHEMA.md`, `TESTING.md`, `CIPHER_CATALOG.md`, this file, tutorials, and `docs/wiki-source`.

If no docs need updates, the final report for that stage must say why.
