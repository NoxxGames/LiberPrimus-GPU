# ChatGPT Context File

## Current Project State

Current completed stage: Stage 5DV - Operator Console Source Browser performance, path canonicalization, and ChatGPT context hardening, without puzzle execution.

Current work after Stage 5DV: Stage 5DW - Operator/assistant source-lock number-fact review batch 1, without execution.

Stage 5DV was inserted after Stage 5DU because the Source Browser became large enough that table responsiveness and path hygiene were blocking review. Stage 5DV does not perform the number-fact review batch, does not backfill number facts, does not rewrite historical source-lock records, and does not select a target.

The canonical Codex handoff root is `codex-output`. The deprecated `codex_output` root must remain absent. Completion summaries under `codex-output/**` are local ignored handoffs and must not be committed.

## Stage 5DV Source Browser Repair

- Source Browser records remain metadata views over committed records and ignored local third-party files.
- Source Browser table cells must stay cheap: compact strings/counts only, no eager widgets, pixmaps, YAML serialization, validators, or thumbnail generation.
- Detail panel content may be richer, but thumbnails, path resolution, and raw YAML previews must be lazy or cached.
- Repeated selection of the same entry should not rebuild the detail panel.
- Search/filter text should use precomputed `entry.search_text` and debounce user input.
- Path resolution uses a cache keyed by normalized path and repository root.
- Thumbnail cache entries are keyed by resolved path, file size/mtime, and requested size under `.cache/operator-console/thumbnails/`.

## Source Browser Path Rules

- Bare filenames are labels unless a path-bearing key or source-root policy resolves them.
- `file_name: 0.png` does not create a root-level `0.png` path when a sibling `relative_path` exists.
- Path-bearing keys include `path`, `paths`, `local_path`, `relative_path`, `source_path`, `source_file`, `image_path`, `document_path`, `pdf_path`, `audio_path`, `attachment_path`, `thread_folder`, `canonical_page_root`, `root_path`, `file_path`, `source_record_path`, and `schema_path`.
- Label-only keys such as `title`, `name`, `summary`, `description`, `notes`, `phrase`, and unrooted `file_name` are not paths by suffix alone.
- Source-root-relative keys such as `source_images`, `source_files`, `source_documents`, `image_files`, `document_files`, `expected_files`, `observed_files`, `files.file_name`, `records.file_name`, `image_locks.file_name`, `pdf_locks.file_name`, and `audio_locks.file_name` resolve only when an explicit source root is available.
- If both `relative_path` and `file_name` are present in one object, the explicit relative path wins.
- Missing bare basename duplicates are suppressed when a canonical rooted path for the same basename is present.
- Allowed root-level path exceptions remain narrow: `ChatGPT-ContextFile.md`, `README.md`, `STATUS.md`, and `ROADMAP.md`.

## Canonical Local Source Roots

The Source Browser path aliases include these local ignored roots:

- `third_party/BigGapsFoundInLiberPrimus`
- `third_party/CribbingPage15`
- `third_party/Mobius_totient_first_page_theory`
- `third_party/PotentialCrib_RedRunes_Pages_54_55`
- `third_party/RedRunes_Possible_Koan_Connection`
- `third_party/StarArtifactsInLPPageImages`
- `third_party/CicadaMusic`
- `third_party/CicadaMusic/community-theory`
- `third_party/NumberFactsCollection`
- `third_party/PotentialHint-3301-on-Page32`
- `third_party/DiskCipherStuff`
- `third_party/RedditStuff`
- `third_party/NumberTriangleStuff`
- `third_party/CiadaSolversIddqd_v2/liber-primus__images--full`
- `third_party/CiadaSolversIddqd_v2/liber-primus__images--unsolved`
- `third_party/CiadaSolversIddqd_v2/lp_outguessed`
- `third_party/The-Complete-Cicada3301-Archive-main`

The spelling `CiadaSolversIddqd_v2` is intentional because that is the current local path spelling. Do not silently change it to `Cicada...`.

## Legacy ChatGPT Context Validator Anchors

Stage 5DP source-locked new Reddit Mayfly/dot/cover/ISO material. MayFlyInvestigation is high value, includes 2033 active reduced cells, and remains candidate-only, not active solve routes.

Stage 5DS expanded music/Ouroboros/token-block static addendum. Stage 5DR GUI follow-up keeps the details panel as right-side/right-dock source review UI. Token-block static context preserves first 16 bytes `cbe7a7ba61ed7eb75cf99cdef704b7d4` as metadata only.

Stage 5DT source-review readiness planning remains the prior number-fact-card planning layer; Stage 5DV repairs Source Browser performance/path handling before the Stage 5DW review batch.

## Stage 5DU - Community visual/red-heading/negative-space source-lock addendum

## Stage 5DU Six-Thread Summary

Stage 5DU source-locked six local community thread folders as compact metadata: BigGapsFoundInLiberPrimus, CribbingPage15, Mobius_totient_first_page_theory, PotentialCrib_RedRunes_Pages_54_55, RedRunes_Possible_Koan_Connection, and StarArtifactsInLPPageImages.

Stage 5DU represented 234 files: 148 images, 39 Python files, 2 spreadsheets, 39 text outputs, and 6 `messages.txt` files. It created 72 review-only candidate records, 12 number-fact cards or enrichments, 6 number-fact overlays, 1490 Source Browser entries, and 103 Stage 5DU Source Browser entries. Source Browser validation had 0 errors and 548 warnings.

Original LP page images for crosschecks live under `third_party/CiadaSolversIddqd_v2/liber-primus__images--full`. Old per-thread `original-pages/` folders are not source truth.

## Top Candidate Stack

### RedRunes / Gateless Gate

RedRunes/Gateless Gate strongest observation:

- Red rune grouping 2/11/3 matches THE / ENLIGHTENED / MAN.
- The claimed koan context is Gateless Gate koan #20 of 49.
- THE ENLIGHTENED MAN zero-index GP sum is 227, equal to prime(49).
- 227 is not unique among titles; the 2/11/3 grouping is the stronger constraint.
- ENLIGHTENED = MUMON'S COMMENT under index and prime sums.
- The 742 and 682 bridges are candidate-only and retain overfit warnings.

### BigGapsFoundInLiberPrimus

BigGaps strongest observations:

- Sixteen claimed big-gap pages have one-based page sum 569.
- Red big-gap subset one-based page sum is 229.
- Claimed line gaps include 73, 109, and 129; 109 is prime(29).
- Same-frame overlays and vertical phase-shift observations remain candidates with high layout-artifact risk.

### StarArtifactsInLPPageImages

StarArtifacts strongest observations:

- Exact max-channel/RGB 254 threshold reveals a near-white star/sunburst layer in the community observation.
- Pages 10-13 and 41-43 are key pages for that observation.
- Tree offsets 641 and 709 have prime-index gap 11.
- The stardust phrase GP 2540 = 254 * 10 is unverified community decode context.
- ICC/profile/JPEG profile observations are production metadata, not clue proof.

### CribbingPage15

- Internal phrase GP facts and the YOUR TRUTH crib pointer are preserved.
- Standard short-token GP makes YOUR/TRUTH 4/4, not clean 4/5; the warning remains.

### PotentialCrib RedRunes Pages 54/55

- GP 491 family contains A POSTLUDE, DEAD TREE, YGGDRASIL, DIVINITY WITHIN, and A CROSSROADS.
- A POSTLUDE is not unique by GP alone.
- Red-heading and marginalia GP-equivalence families require controls before any target decision.

### Mobius Totient First Page Theory

- Arithmetic Mobius/totient zero-class method is preserved as a candidate method.
- Page0 DIVINITY WITHIN / A CROSSROADS claim remains candidate context.
- The proposed 33-word page0 plaintext is quarantined and is not accepted.

## Number-Fact Review Principle

- Source-locked does not mean review-ready.
- A useful fact card must explain value, type, expression, components, relation, why stored, source anchor, verification status, risks, and crosslinks.
- Older zero-fact entries are usually not reviewed, not necessarily number-free.
- Stage 5DW should start the 20-entry review batch 1 after the Stage 5DV repair.

## Governance And Preservation

- Stage 5DG real operator approval remains preserved, but there is still no Deep Research acceptance and no satisfied combined gate.
- Stage 5BD run-plan IDs remain preserved at 10.
- Active lineage records remain preserved at 8.
- The Stage 5CM-and-later parallel validation cap remains 8 workers.
- String 4 remains inactive.
- Active planning input remains unauthorized and unselected.

## Guardrails

- No number-fact review batch in Stage 5DV.
- No historical number-fact backfill.
- No source-lock rewrite.
- No target selection.
- No operator readiness decision.
- No Deep Research acceptance.
- No active ingestion.
- No byte generation.
- No token-block variant materialization.
- No branch enumeration.
- No route extraction.
- No OCR, image forensics, semantic image interpretation, or AI/ML image analysis.
- No community code, native code, spreadsheet macro, HTML tool, or VM execution.
- No DWH, hash, preimage, Tor, or network target validation.
- No scoring, benchmarking, CUDA, or GPU execution.
- No website expansion.
- No canonical corpus activation.
- No page-boundary finalization.
- No solve claim.
