# Source Harvester UsefulFiles CLI

Stage 5AJ extends `libreprimus source-harvester` with local-only UsefulFilesAndIdeas commands.

Key commands:

- `inventory-usefulfiles`
- `extract-xlsx-metadata`
- `parse-important-links`
- `build-usefulfiles-source-cards`
- `build-scraper-capture-policy`
- `build-redaction-policy`
- `build-extraction-fidelity-policy`
- `build-stage5aj-new-clue-categories`
- `update-deep-research-packs`
- `build-stage5aj-guardrail`
- `build-stage5aj-next-stage-decision`
- `build-stage5aj-summary`
- `validate-stage5aj`

The commands read ignored local files under `third_party/UsefulFilesAndIdeas/` and write compact committed summaries under `data/source-harvester/`. Generated indexes and bundle bodies remain ignored under `research-inputs/stage5aj/`, `experiments/results/research-bundles/stage5aj/`, and `experiments/results/source-harvester-usefulfiles/stage5aj/`.

The CLI does not fetch network sources, clone repositories, use Google Drive storage, execute Deep Research, run OCR/AI/ML, execute image/stego/audio tooling, run CUDA, run benchmarks, execute scored experiments, expand the website, or make solve claims.
