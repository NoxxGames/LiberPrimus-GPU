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

For Stage 5AM, Deep Research may also use:

- `data/website-render/stage5am-summary.yaml`
- `data/website-render/stage5am-render-output-manifest.yaml`
- the ignored metadata-only static index under `website-export/stage5am/research-index/`

For Stage 5AN, Deep Research may use the private hosted content URL and content-pack manifest after the user uploads the combined webroot:

- `data/deep-research-export/stage5an-summary.yaml`

For Stage 5AU manual review, use the Stage 5AT case-review package with the Stage 5AR coordinate-lock package and Stage 5AP token-block source-lock package:

- `data/token-block/stage5ar-original-page-image-source-lock.yaml`
- `data/token-block/stage5ar-page-split-records.yaml`
- `data/token-block/stage5ar-token-pixel-coordinate-records.yaml`
- `data/token-block/stage5ar-token-case-policy.yaml`
- `data/token-block/stage5at-case-review-policy.yaml`
- `data/token-block/stage5at-case-review-challenge-set.yaml`
- `data/token-block/stage5at-human-review-decision-template.yaml`
- `data/token-block/stage5ar-token-coordinate-validation.yaml`
- `data/project-state/stage5ar-summary.yaml`
- `data/token-block/stage5ap-page49-51-source-lock.yaml`
- `data/token-block/stage5ap-token-block-canonical-transcription.yaml`
- `data/token-block/stage5ap-token-block-mapping-preflight.yaml`
- `data/token-block/stage5ap-token-block-null-control-plan.yaml`
- `data/token-block/stage5ap-token-block-dwh-context.yaml`
- `data/project-state/stage5ap-summary.yaml`

Stage 5AT, Stage 5AR, and Stage 5AP records are source-lock/preflight/review metadata only. Do not infer plaintext, intentionality, hash targets, OCR output, image semantics, automatic transcription changes, or execution permission from them.
- `data/deep-research-export/stage5an-content-pack-manifest-summary.yaml`
- Metadata site: `http://liberprimus-gpu-data.info/index.html`
- Private content: `http://liberprimus-gpu-data.info/private-content/`
- Private content manifest: `http://liberprimus-gpu-data.info/private-content/data/content-pack-manifest.json`

These URLs are private/review-gated handoff aids. They are not public publication approval and do not replace committed source-card, content-index, claim-record, and publication-gate metadata.

Do not use raw `third_party/` files as the ingest root, and do not treat website-ingest or website-render metadata as public publication permission.

For Stage 5AJ, private handoffs may reference:

- `data/source-harvester/stage5aj-usefulfiles-source-card-summary.yaml`
- `data/source-harvester/stage5aj-usefulfiles-content-index-summary.yaml`
- `data/source-harvester/stage5aj-xlsx-extraction-summary.yaml`
- `data/source-harvester/stage5aj-important-links-source-index.yaml`
- `data/source-harvester/stage5aj-extraction-fidelity-policy.yaml`
- `data/source-harvester/stage5aj-redaction-policy.yaml`
- `data/source-harvester/stage5aj-deep-research-pack-update-summary.yaml`

Private extracts should retain technical details such as runes, numbers, hashes, tables, formulas, coordinates, highlights, and technical links. Public extracts remain review-gated and should not expose raw local content.
