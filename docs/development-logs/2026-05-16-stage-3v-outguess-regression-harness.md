# Stage 3V OutGuess Regression Harness Development Log

## Scope

Stage 3V adds a deterministic OutGuess regression harness. It is a regression and fixture hygiene stage, not a Liber Primus solve attempt and not a broad steganography scan.

## Initial State

- Branch: `main`
- Starting commit: `64200bc9d48394f0878e4b7c364b135bfa137b22`
- Origin remote: `https://github.com/NoxxGames/LiberPrimus-GPU.git`
- Latest CI before work: `26053820610`, passed
- OutGuess tool detected locally: false
- `third_party/LiberPrimusDiscordChats/` present and not processed
- `third_party/LiberPrimusPages/` present and not processed
- Existing untracked root reports and generated output directories were left unmodified and uncommitted

## Policy

- Raw historical artefacts stay under ignored `third_party/` paths.
- Extracted payloads and generated OutGuess records stay under ignored `experiments/results/stego/`.
- Missing OutGuess or missing assets are explicit skipped outcomes when allowed by the manifest.
- Non-empty payloads are not interpreted unless an expected payload hash matches.
- No CUDA, no broad stego scan, no canonical corpus activation, and no solve claim.

## Implementation Notes

- Added stego schemas for artefact, manifest, tool, extraction, and summary records.
- Added metadata-only artefact placeholders for historical OutGuess-relevant public sources.
- Added `outguess-regression-v1` with synthetic controls and historical placeholders.
- Added `libreprimus.stego` with tool detection, manifest validation, synthetic JPEG controls, command wrapping, result export, and summary loading.
- Added `libreprimus stego` CLI commands for detection, validation, run, and summary.
- Added raw-data-free consistency checks and CI script hooks.

## Local Run

- Tool available: false
- Cases: 7
- Attempted: 0
- Passed: 0
- Failed: 0
- Skipped for missing tool: 6
- Skipped for missing assets: 0
- Skipped disabled: 1
- Extraction errors: 0
- Reference extractions recorded: 0
- Generated outputs staged: 0
- Raw artefacts staged: 0

## Validation

- Focused Stage 3V tests: `14 passed`
- Full Python tests: `815 passed`
- Ruff: passed
- Smoke: passed
- Consistency suite: `435/435` passed
- CI consistency script: passed
- Public docs status: `11 passed`
- Lock hashes: passed
- Workflow static validation: `13 passed`
- Wiki source validation and dry-run sync: passed
