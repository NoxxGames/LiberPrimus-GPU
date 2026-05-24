# Deep Research Ingest Format

Deep Research handoffs use committed source-card, content-index, missing-source, readiness, extraction-fidelity, and redaction-policy metadata as the control plane. Generated bundle bodies may exist locally under ignored `research-inputs/` paths, but they are not committed and are not public documentation.

For Stage 5AK, private handoffs may additionally reference:

- `data/source-harvester/stage5ak-community-facts-source-card-summary.yaml`
- `data/source-harvester/stage5ak-community-facts-content-index-summary.yaml`
- `data/source-harvester/stage5ak-community-facts-attachment-index.yaml`
- `data/source-harvester/stage5ak-community-facts-claim-records.yaml`
- `data/source-harvester/stage5ak-community-facts-correction-log.yaml`
- `data/source-harvester/stage5ak-community-facts-arithmetic-preflight.yaml`
- `data/source-harvester/stage5ak-summary.yaml`
- ignored private addenda under `research-inputs/stage5ak/`

For Stage 5AL, Deep Research should start from:

- `data/source-harvester/stage5al-deep-research-export.yaml`
- `data/website-ingest/stage5al/`
- ignored helper files under `research-inputs/stage5al/`

Do not use raw `third_party/` files as the ingest root, and do not treat website-ingest metadata as public publication permission.

For Stage 5AJ, private handoffs may reference:

- `data/source-harvester/stage5aj-usefulfiles-source-card-summary.yaml`
- `data/source-harvester/stage5aj-usefulfiles-content-index-summary.yaml`
- `data/source-harvester/stage5aj-xlsx-extraction-summary.yaml`
- `data/source-harvester/stage5aj-important-links-source-index.yaml`
- `data/source-harvester/stage5aj-extraction-fidelity-policy.yaml`
- `data/source-harvester/stage5aj-redaction-policy.yaml`
- `data/source-harvester/stage5aj-deep-research-pack-update-summary.yaml`

Private extracts should retain technical details such as runes, numbers, hashes, tables, formulas, coordinates, highlights, and technical links. Public extracts remain review-gated and should not expose raw local content.
