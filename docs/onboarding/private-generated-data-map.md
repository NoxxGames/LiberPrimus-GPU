# Private And Generated Data Map

## Local Private Or Ignored Inputs

- `third_party/LiberPrimusDiscordChats/`: local/private Discord HTML exports. Do not commit raw logs, message bodies, usernames, IDs, or private URLs.
- `third_party/LiberPrimusPages/`: local raw Liber Primus page images. Do not commit raw images.
- `third_party/CicadaArchive/`: local historical Cicada artefacts. Commit only README/.gitkeep and curated metadata.
- `third_party/CicadaOutGuess/`: local OutGuess regression artefacts. Commit only README/.gitkeep and curated metadata.
- `third_party/CicadaSolversIddqd/`: local cache for the `cicada-solvers/iddqd` source-delta audit. Commit only README/.gitkeep; do not commit downloaded images, audio, fonts, archives, blobs, or cloned repository contents.
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
- `experiments/results/cpu-batch/stage4h/`: generated Stage 4H CPU batch result JSONL, summary JSON, adapter coverage JSON, and warning records.
- `experiments/results/scoring-consolidation/stage4i/`: generated Stage 4I scorer inventories, rendered calibration reports, CPU batch compatibility JSON, and warnings.
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
- Generated Stage 4H CPU batch result, summary, adapter coverage, and warning outputs under `experiments/results/cpu-batch/stage4h/`.
- Generated Stage 4I scorer inventory, calibration report, CPU batch compatibility, and warning outputs under `experiments/results/scoring-consolidation/stage4i/`.
- Downloaded or cached `cicada-solvers/iddqd` images, audio, fonts, archives, blobs, or cloned repository contents under `third_party/CicadaSolversIddqd/`.
- SQLite databases.
- Root Deep Research report copies or `deep-research-reports/**`.
