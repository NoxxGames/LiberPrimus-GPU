# ChatGPT Context File

## Current Project State

Current completed stage: Stage 5DY - Validation performance, parallel-test discipline, stage-isolation, and non-mutating validator repair, without execution.

Current work after Stage 5DY: Stage 5DZ - Operator/assistant source-lock number-fact review batch 3, without execution.

Stage 5DV was inserted after Stage 5DU because the Source Browser became large enough that table responsiveness and path hygiene were blocking review. Stage 5DW completed the first high-signal number-fact review batch as overlay metadata only. Stage 5DX completed the second visual/red-heading/transform bridge review batch as overlay metadata only. Stage 5DY repaired validation performance and stage isolation before the next batch. Stage 5DY does not perform number-fact batch 3, backfill number facts directly, rewrite historical source-lock records, select a target, generate bytes, execute anything, or make solve claims.

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

Stage 5DT source-review readiness planning remains the prior number-fact-card planning layer; Stage 5DV repaired Source Browser performance/path handling before Stage 5DW completed review batch 001.

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
- Stage 5DW completed the high-signal 20-entry review batch 001 after the Stage 5DV repair; Stage 5DX completed the visual/red-heading/transform 20-entry review batch 002. Stage 5DY inserted validation repair before the next review batch, so Stage 5DZ should continue with number-fact review batch 003.

## Governance And Preservation

- Stage 5DG real operator approval remains preserved, but there is still no Deep Research acceptance and no satisfied combined gate.
- Stage 5BD run-plan IDs remain preserved at 10.
- Active lineage records remain preserved at 8.
- The Stage 5CM-and-later parallel validation cap remains 8 workers.
- String 4 remains inactive.
- Active planning input remains unauthorized and unselected.

## Guardrails

- No direct historical source-record number-fact backfill in Stage 5DW.
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

## Stage 5DW Number-Fact Review Batch 001

- Stage 5DW completed high-signal number-fact review batch 001 after Stage 5DV path/performance repair.
- The batch reviewed 20 selected evidence/candidate records, not the Stage 5DT stable batch-001 list.
- Historical source-lock records were not rewritten; facts were added through NumberFactCard overlays.
- Overlay-only fact cards are now supported, so older zero-extracted-fact records can display review facts without source-record mutation.
- Key added fact families: Page32 red-header 2472; Page32 463->3299/3301; NO-F section-flow 1433/2883/1894/1814/695/91; LP doublets 89/4337; LP1 word count 464->3301; artwork/title 449/311; solved-koan 1229/337/199/1033; page54-57 308/154; Page32 Fibonacci mod29 primes; Final.jpg road/way 3301/991/1229; prime-index 761/167/464/1033/3301; RGB185=3301 plus 1033/1103 correction; Instar parable product; Instar 761/167; Interconnectedness 772/277/1049; Ouroboros see-also GP scan; RedRunes/Gateless Gate 2/11/3/227/742/682/155/551; BigGaps 569/229/109; StarArtifacts 254/2540/641/709; red-heading GP491 family.
- All remain review-only; no target selection, route extraction, byte generation, execution, OCR/image forensics/audio/stego/Tor/network/CUDA/scoring, or solve claim.

## Stage 5DX - Number-fact review batch 002

- Stage 5DX enriched 20 selected visual/red-heading/transform source-lock entries using NumberFactCard overlays only.
- Stage 5DX did not rewrite historical source locks, select a target, run routes, generate bytes, execute code, run OCR/image forensics, or make solve claims.
- RedRunes secondary facts preserved: ENLIGHTENED/MUMON'S COMMENT 155/551, red prime-sum 742, key/speech-tongue 682, first-two-rune sum 31.
- BigGaps/StarArtifacts facts preserved: red-subset sum 229, gap metrics 73/109/129 with 109=prime(29), tree offsets 641/709 with prime-index gap 11, stardust phrase 2540=254*10, Mayfly 72/600 twin-prime gaps, ICC boundary pages 00-16 vs 17-74 with 2576-byte profile claim.
- Red-heading/Mobius facts preserved: Page15 instruction phrase primes, DIVINITY WITHIN 491/563/1229 crosslink, YGGDRASIL spelling 491/564 warning, A POSTLUDE 1/8 structure, Mobius/totient zero-class 14-token partition, page0 DIVINITY WITHIN/A CROSSROADS 491.
- PDD/Disk/Ouroboros facts preserved: 56311 net +25 over modulus 153, gcd(25,153)=1, 4-phase period 612; OUROBOROS 167 minus 153 gives offset 14; Disk 56311 from center 41/WYNN reaches word52/WAY.
- Stage 5DY inserted validation repair before number-fact review batch 003. Stage 5DZ should continue the review batch unless a blocking Source Browser issue appears.

## Stage 5DY Validation Policy

- Stage 5DX completed at eb93bc8d with 23 overlays and CI passed, but its Codex output exposed validation-tooling pain.
- Full serial pytest took 1h38m41s and should not be required by default in every future prompt.
- Full monolithic consistency exceeded 45 minutes locally; use focused/stage-fast and full-parallel profiles unless a full serial fallback is explicitly justified.
- Future prompts should tell Codex: use focused tests during iteration, run broad parallel validation once near final, avoid broad repeated serial test loops.
- Historical validators must not depend on mutable current global Source Browser counts.
- Stage-specific schemas must not overwrite shared schemas.
- Validate/summary commands must be read-only for committed records.
- PowerShell wildcard expansion differs from Bash; use explicit file lists in examples.
- Stage 5DZ remains the next fact-review batch.
