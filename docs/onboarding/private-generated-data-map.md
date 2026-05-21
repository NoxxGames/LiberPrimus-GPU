# Private And Generated Data Map

## Local Private Or Ignored Inputs

- `third_party/LiberPrimusDiscordChats/`: local/private Discord HTML exports. Do not commit raw logs, message bodies, usernames, IDs, or private URLs.
- `third_party/LiberPrimusPages/`: local raw Liber Primus page images. Do not commit raw images.
- `third_party/CicadaArchive/`: local historical Cicada artefacts. Commit only README/.gitkeep and curated metadata.
- `third_party/CicadaOutGuess/`: local OutGuess regression artefacts. Commit only README/.gitkeep and curated metadata.
- `third_party/CicadaSolversIddqd/`: local cache for the `cicada-solvers/iddqd` source-delta audit. Commit only README/.gitkeep; do not commit downloaded images, audio, fonts, archives, blobs, or cloned repository contents.
- `third_party/SourceSnapshots/`: local cache for Stage 4K allowlisted public source-lock fetches. Commit only README/.gitkeep; fetched public HTML/text bytes remain ignored unless a later explicit policy approves a small text snapshot path.
- `third_party/StegoPositiveControls/`: local ignored cache for Stage 4N stego/audio positive-control fixture artefacts. Commit only README/.gitkeep; do not commit cached image, audio, binary, font, archive, or extracted payload files.
- `data/raw/`: immutable raw input area. Do not overwrite or commit real raw artefacts unless a future stage explicitly scopes a curated placeholder or lock.

## Generated Outputs

- `experiments/results/`: generated run outputs, review bundles, candidate records, summaries, SQLite stores, image derivatives, OutGuess payloads, and wiki sync reports.
- `experiments/results/discord-full-review/stage4a/`: generated Stage 4A full Discord review bundle, redacted streams, channel shards, topic shards, indexes, LP page gallery copies/thumbnails, static site, and optional upload archive.
- `experiments/results/discord-full-review/stage4a/site/`: generated SFTP-ready static review site, including noindex metadata, `robots.txt`, privacy notice, upload checklist, manifests, copied LP page images, and thumbnails.
- `experiments/results/source-lock-triage/stage4b/`: generated Stage 4B source-lock triage diagnostics, rejected-link lists, duplicate-link lists, warnings, and summaries.
- `experiments/results/visual-annotation/stage4c/`: generated Stage 4C visual annotation workspace, local static site, page-image review copies, coordinate-grid overlays, blank templates, and annotation manifest.
- `experiments/results/bounded-numeric/stage4d/`: generated Stage 4D bounded numeric summaries, result JSONL, manifest-status JSONL, warnings, and negative-control audit records.
- `experiments/results/source-delta/stage4e/`: generated Stage 4E source-delta path indexes, source-delta reports, duplicate/unique candidate JSONL files, and warnings.
- `experiments/results/stego-fixtures/stage4f/`: generated Stage 4F stego/audio fixture candidate reports, source-gap JSONL files, and warnings.
- `experiments/results/cookie-refresh/stage4g/`: generated Stage 4G cookie refresh candidate records, exact-match records, duplicate records, summary JSON, and warnings.
- `experiments/results/cpu-batch/stage4h/`: generated Stage 4H CPU batch result JSONL, summary JSON, adapter coverage JSON, and warning records.
- `experiments/results/cpu-batch/stage4o/`: generated Stage 4O CPU batch result JSONL, adapter coverage JSON, parity expectation JSONL, scoring compatibility JSON, summary JSON, and warning records.
- `experiments/results/result-store-unification/stage4p/`: generated Stage 4P source inventory, unified result JSONL, unified score-summary JSONL, method-status joins, cross-stage reports, summaries, warnings, and any local SQLite probes.
- `experiments/results/benchmarks/stage4q/`: generated Stage 4Q environment, CPU smoke, CUDA parity readiness, summary, and warning diagnostics.
- `experiments/results/cuda-planning/stage5a/`: generated Stage 5A CUDA target-plan, parity scaffold, implementation-gate, non-target, summary, and warning reports.
- `experiments/results/cuda-parity/stage5b/`: generated Stage 5B CUDA parity harness, fixture, backend capability, future-kernel matrix, summary, and warning reports.
- `experiments/results/cuda-build/stage5c/`: generated Stage 5C CUDA toolchain detection, device detection, optional smoke-build, summary, and warning reports.
- `experiments/results/native-cpu/stage5d/`: generated Stage 5D native CPU backend capability, threading parity, native/Python parity, diagnostic, summary, and warning reports.
- `experiments/results/cuda-kernel-contract/stage5e/`: generated Stage 5E first-kernel contract, adapter-selection, native parity adapter, implementation-readiness, summary, and warning reports.
- `experiments/results/cuda-kernel/stage5f/`: generated Stage 5F synthetic CUDA kernel implementation, build, parity, summary, and warning reports.
- `experiments/results/cuda-parity-reporting/stage5g/`: generated Stage 5G shift_score parity report, CUDA device-code subset audit, solved-fixture-safe preflight, summary, and warning reports.
- `experiments/results/gematria-shift-contract/stage5h/`: generated Stage 5H Gematria shift contract, native fixture, solved-fixture mapping, score-summary parity plan, summary, and warning reports.
- `experiments/results/gematria-cuda-prep/stage5i/`: generated Stage 5I Gematria CUDA preparation, ABI plan, validation vector, implementation checklist, summary, and warning reports.
- `experiments/results/gematria-cuda-kernel/stage5j/`: generated Stage 5J Gematria CUDA kernel implementation, build, synthetic parity, summary, and warning reports.
- `experiments/results/gematria-cuda-parity-reporting/stage5k/`: generated Stage 5K Gematria CUDA parity report, device-code audit, solved-fixture-safe preflight, score-summary preflight, summary, and warning reports.
- `experiments/results/gematria-solved-fixture-mapping/stage5l/`: generated Stage 5L solved-fixture token mapping, native parity, output-hash contract, score-summary shape, summary, and warning reports.
- `experiments/results/gematria-solved-fixture-cuda/stage5m/`: generated Stage 5M solved-fixture CUDA run, parity, boundary, summary, and warning reports.
- `experiments/results/gematria-solved-fixture-cuda-reporting/stage5n/`: generated Stage 5N parity report, controlled expansion gate, boundary review, result-store preflight, no-unsolved guardrail, summary, and warning reports.
- `experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/`: generated Stage 5O repeat run, repeat parity, result-store preflight, score-summary preflight, expansion-decision, summary, and warning reports.
- `experiments/results/gematria-cuda-result-store/stage5p/`: generated Stage 5P result-store integration, score-summary integration, method-status impact, generated-body policy, controlled expansion candidate, summary, and warning reports.
- `codex-output/`: local Codex completion handoff files; do not stage or publish.
- `experiments/results/scoring-consolidation/stage4i/`: generated Stage 4I scorer inventories, rendered calibration reports, CPU batch compatibility JSON, and warnings.
- `experiments/results/observation-review/stage4j/`: generated Stage 4J observation review decision reports, quarantine reports, promotion-gate reports, path-sanitisation reports, and warnings.
- `experiments/results/source-lock-snapshots/stage4k/`: generated Stage 4K fetch reports, rejected-source records, duplicate-source records, warnings, and local diagnostics.
- `experiments/results/observation-promotion/stage4l/`: generated Stage 4L promotion ledger, manifest-readiness, blocker, and warning reports.
- `experiments/results/image-preflight/stage4m/`: generated Stage 4M image metadata JSONL, compression metric JSONL, source-variant JSONL, artifact candidate reports, summaries, and warnings.
- `experiments/results/stego-positive-controls/stage4n/`: generated Stage 4N stego/audio readiness, cache, toolchain, and warning reports.
- `third_party/CommunityObservations/`: ignored local community-observation screenshots and metadata sidecars such as the Fib421 review input. Commit only README and marker files.
- `data/normalized/`: generated normalized candidate outputs unless a stage explicitly commits a placeholder or curated source.
- SQLite outputs: `*.sqlite`, `*.sqlite3`, and `*.db` are generated and must not be committed.

## What May Be Committed

- Schemas.
- Locks and source metadata.
- Curated aggregate summaries.
- Redacted public-source review records.
- Negative-control records.
- Summary-only research logs.
- README/.gitkeep files that preserve ignored directory structure.

## What Must Not Be Committed

- Raw Discord logs or private attachments.
- Raw page images.
- Raw third-party historical artefacts.
- Generated candidate dumps.
- Generated extraction payloads.
- Generated Stage 4A static sites, redacted message streams, channel shards, topic shards, copied LP page images, thumbnails, contact sheets, and upload archives.
- Generated Stage 4B source-lock triage diagnostics under `experiments/results/source-lock-triage/stage4b/`.
- Generated Stage 4C annotation-site files, copied review images, grid overlays, and blank/fillable annotation templates under `experiments/results/visual-annotation/stage4c/`.
- Generated Stage 4D bounded numeric JSON/JSONL outputs under `experiments/results/bounded-numeric/stage4d/`.
- Generated Stage 4E source-delta JSON/JSONL outputs under `experiments/results/source-delta/stage4e/`.
- Generated Stage 4F stego/audio fixture JSON/JSONL outputs under `experiments/results/stego-fixtures/stage4f/`.
- Generated Stage 4G cookie refresh JSON/JSONL and summary JSON outputs under `experiments/results/cookie-refresh/stage4g/`.
- Generated Stage 4H CPU batch result, summary, adapter coverage, and warning outputs under `experiments/results/cpu-batch/stage4h/`.
- Generated Stage 4O CPU batch result, adapter coverage, parity expectation, scoring compatibility, summary, and warning outputs under `experiments/results/cpu-batch/stage4o/`.
- Generated Stage 4P source inventory, unified result records, unified score-summary records, method-status join records, cross-stage reports, summary JSON, warnings, and SQLite files under `experiments/results/result-store-unification/stage4p/`.
- Generated Stage 4Q benchmark planning records under `experiments/results/benchmarks/stage4q/`, generated Stage 5A CUDA planning reports under `experiments/results/cuda-planning/stage5a/`, generated Stage 5B CUDA parity reports under `experiments/results/cuda-parity/stage5b/`, generated Stage 5C CUDA build/device reports under `experiments/results/cuda-build/stage5c/`, generated Stage 5D native CPU reports under `experiments/results/native-cpu/stage5d/`, generated Stage 5E CUDA kernel contract reports under `experiments/results/cuda-kernel-contract/stage5e/`, generated Stage 5F CUDA kernel reports under `experiments/results/cuda-kernel/stage5f/`, generated Stage 5G CUDA parity-reporting reports under `experiments/results/cuda-parity-reporting/stage5g/`, generated Stage 5H Gematria shift contract reports under `experiments/results/gematria-shift-contract/stage5h/`, generated Stage 5I Gematria CUDA preparation reports under `experiments/results/gematria-cuda-prep/stage5i/`, generated Stage 5J Gematria CUDA kernel reports under `experiments/results/gematria-cuda-kernel/stage5j/`, generated Stage 5K Gematria CUDA parity-reporting reports under `experiments/results/gematria-cuda-parity-reporting/stage5k/`, generated Stage 5L solved-fixture mapping reports under `experiments/results/gematria-solved-fixture-mapping/stage5l/`, generated Stage 5M solved-fixture CUDA parity reports under `experiments/results/gematria-solved-fixture-cuda/stage5m/`, generated Stage 5N solved-fixture CUDA reporting reports under `experiments/results/gematria-solved-fixture-cuda-reporting/stage5n/`, generated Stage 5O solved-fixture CUDA repeat reports under `experiments/results/gematria-solved-fixture-cuda-repeat/stage5o/`, generated Stage 5P CUDA result-store integration reports under `experiments/results/gematria-cuda-result-store/stage5p/`, and local Codex handoffs under `codex-output/`.
- Generated Stage 4I scorer inventory, calibration report, CPU batch compatibility, and warning outputs under `experiments/results/scoring-consolidation/stage4i/`.
- Generated Stage 4J observation review reports under `experiments/results/observation-review/stage4j/`.
- Generated Stage 4K source-lock snapshot reports under `experiments/results/source-lock-snapshots/stage4k/`.
- Generated Stage 4L observation-promotion reports under `experiments/results/observation-promotion/stage4l/`.
- Generated Stage 4M image-preflight reports under `experiments/results/image-preflight/stage4m/`.
- Generated Stage 4N stego/audio positive-control reports under `experiments/results/stego-positive-controls/stage4n/`.
- Raw or sidecar community-observation artefacts under `third_party/CommunityObservations/`.
- Cached Stage 4K source snapshot bytes under `third_party/SourceSnapshots/`.
- Cached Stage 4N stego/audio fixture bytes under `third_party/StegoPositiveControls/`.
- Downloaded or cached `cicada-solvers/iddqd` images, audio, fonts, archives, blobs, or cloned repository contents under `third_party/CicadaSolversIddqd/`.
- SQLite databases.
- Root Deep Research report copies or `deep-research-reports/**`.
