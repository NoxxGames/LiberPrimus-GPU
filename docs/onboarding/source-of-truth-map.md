# Source Of Truth Map

## Current Operational Truth

- `STATUS.md`: latest completed stage, current boundaries, and no-solve/no-CUDA/no-corpus-activation posture.
- `ROADMAP.md`: short and medium-term plan.
- `docs/roadmap/staged-plan.md`: durable staged plan, deferred work, retired/deprioritised directions, and Deep Research influence.
- `AGENTS.md`: Codex operating rules and non-negotiable policies.
- `README.md`: public project overview and where-to-start summary.
- `data/project-state/stage5ah-doc-staleness-source-of-truth.yaml`: active current/next-stage expectations for the document staleness checker; after Stage 5AW it names Stage 5AW as latest complete and Stage 5AX as next.
- `data/project-state/stage5ab-doc-staleness-source-of-truth.yaml`: superseded staleness-check source for historical Stage 5AB/5AG validation context.
- `data/project-state/operational-file-map.yaml`: maintained lifecycle map for operational, tutorial, mirror, and historical files.
- `data/source-harvester/stage5af-cicada-source-manifest.yaml`: Stage 5AF source-harvester source manifest.
- `data/source-harvester/stage5ag-source-harvester-summary.yaml`: Stage 5AG local source inventory aggregate summary.
- `data/source-harvester/stage5ai-curated-research-bundle-summary.yaml`: Stage 5AI curated research-bundle extraction aggregate summary.
- `data/source-harvester/stage5aj-summary.yaml`: Stage 5AJ UsefulFilesAndIdeas integration aggregate summary.
- `data/source-harvester/stage5ak-summary.yaml`: Stage 5AK community-facts claim-record integration aggregate summary.
- `data/source-harvester/stage5al-summary.yaml`: Stage 5AL website-ingest staging and Deep Research export aggregate summary.
- `data/website-ingest/stage5al/`: committed metadata-only website-ingest package.
- `data/website-render/stage5am-summary.yaml`: Stage 5AM static research website renderer aggregate summary.
- `data/website-render/stage5am-*.yaml`: committed Stage 5AM render policy, input, manifest, validation, privacy, upload, guardrail, and next-stage decision records.
- `data/deep-research-export/stage5an-summary.yaml`: Stage 5AN private content-pack and hosted private-content aggregate summary.
- `data/deep-research-export/stage5an-*.yaml`: committed Stage 5AN content-pack, hosted export, combined webroot, file-selection, publication-gate, upload, consumption-guide, guardrail, and next-stage records.
- `data/token-block/stage5ap-*.yaml`: committed Stage 5AP page 49-51 source-lock, image-provenance, transcription, coordinate, alphabet, mapping, null-control, and DWH records.
- `data/token-block/stage5ar-*.yaml`: committed Stage 5AR original-image source-lock, image-variant, page-split, pixel-coordinate, case-policy, coordinate-validation, source-lock/null-control update, DWH coordinate context, and guardrail records.
- `data/token-block/stage5at-*.yaml`: committed Stage 5AT token case-review policy, challenge, crop-manifest, decision-template, review-pack manifest, variant-classifier repair, doc-drift repair, null-control update, DWH context, and guardrail records.
- `data/token-block/stage5au-*.yaml`: committed Stage 5AU usability-audit, crop-geometry, crop-quality, v2 challenge, v2 decision-template, review-pack v2 manifest, UI coverage, null-control, DWH context, and guardrail records.
- `data/token-block/stage5av-*.yaml`: committed Stage 5AV decision ingest, validation, human decision, confirmed-token, unresolved-variant, reviewer-extra-token, primary-60 impact, branch-manifest, canonical non-update, null-control, DWH context, and guardrail records.
- `data/token-block/stage5aw-*.yaml`: committed Stage 5AW decision-parser audit, parser policy, repaired decision/variant/reviewer-extra records, malformed-fragment audit, repaired primary-60 impact, repaired compact branch-manifest, canonical non-update, null-control, DWH context, and guardrail records.
- `data/stego/stage5ap-outguess-*.yaml`: committed Stage 5AP OutGuess policy, toolchain, positive-control matrix, historical fixture readiness, and guardrail records.
- `data/project-state/stage5ap-summary.yaml`: Stage 5AP aggregate summary and guardrail state.
- `data/project-state/stage5ar-summary.yaml`: Stage 5AR aggregate summary and guardrail state.
- `data/project-state/stage5at-summary.yaml`: Stage 5AT aggregate summary and guardrail state.
- `data/project-state/stage5au-summary.yaml`: Stage 5AU aggregate summary, guardrail state, and historical Stage 5AV next-stage decision.
- `data/project-state/stage5av-summary.yaml`: Stage 5AV aggregate summary, guardrail state, and Stage 5AW next-stage decision.
- `data/project-state/stage5aw-summary.yaml`: Stage 5AW parser-repair aggregate summary, guardrail state, and Stage 5AX next-stage decision.
- `data/project-state/stage5ah-doc-staleness-summary.yaml`: Stage 5AH operational doc-staleness coverage summary.
- `docs/onboarding/source-harvester-workflow.md`: local-only source-harvester workflow and manual-export policy.
- `docs/onboarding/deep-research-bundle-workflow.md`: Stage 5AI/5AJ/5AK private Deep-Research bundle handoff workflow.
- `docs/onboarding/deep-research-ingest-format.md`: Stage 5AJ Deep Research ingest metadata and fidelity policy.
- `docs/onboarding/community-observation-ingest-workflow.md`: Stage 5AK community observation ingest and claim-record policy.
- `docs/onboarding/static-research-index-workflow.md`: Stage 5AM static research index renderer and upload workflow.
- `docs/onboarding/private-deep-research-content-workflow.md`: Stage 5AN private content-pack and SFTP webroot workflow.
- `docs/onboarding/token-block-source-lock-workflow.md`: Stage 5AP page 49-51 token-block source-lock workflow.
- `docs/onboarding/page49-51-coordinate-source-lock-workflow.md`: Stage 5AR original-image coordinate-lock workflow.
- `docs/onboarding/token-case-human-review-workflow.md`: Stage 5AU/5AV token case human-review workflow.
- `docs/onboarding/token-case-review-pack-v2-workflow.md`: Stage 5AU v2 review-pack usage workflow.
- `docs/onboarding/token-case-decision-integration-workflow.md`: Stage 5AV decision integration workflow.
- `docs/onboarding/decision-parser-repair-workflow.md`: Stage 5AW decision parser repair workflow.
- `docs/onboarding/local-source-inventory-workflow.md`: local `third_party/` source inventory workflow and raw-data guardrails.

## Research And Workflow Truth

- `EXPERIMENTS.md`: experiment policy, queue expectations, and no-broadening rules.
- `RESULTS_SCHEMA.md`: committed and generated result/record families.
- `TESTING.md`: local and CI validation commands.
- `DATASET.md`: data and provenance policy.
- `RESEARCH.md`: research posture and evidence expectations.
- `CIPHER_CATALOG.md`: method-family status and transform policy.
- `docs/reference/source-harvester-cli.md`: source-harvester CLI usage and guardrails.
- `docs/reference/source-harvester-local-inventory-cli.md`: Stage 5AG local source inventory CLI usage.
- `docs/reference/source-harvester-curated-bundles-cli.md`: Stage 5AI curated bundle/source-card/content-index CLI usage.
- `docs/reference/source-harvester-usefulfiles-cli.md`: Stage 5AJ UsefulFilesAndIdeas CLI usage and guardrails.
- `docs/reference/source-harvester-community-facts-cli.md`: Stage 5AK community-facts CLI usage and guardrails.
- `docs/reference/website-render-cli.md`: Stage 5AM website-render CLI usage and guardrails.
- `docs/reference/deep-research-export-cli.md`: Stage 5AN deep-research-export CLI usage and guardrails.
- `docs/reference/token-block-cli.md`: Stage 5AP token-block CLI usage and guardrails.
- `docs/reference/token-block-coordinate-cli.md`: Stage 5AR coordinate-lock CLI usage and guardrails.
- `docs/reference/token-case-review-pack-cli.md`: Stage 5AT token case-review pack CLI usage and guardrails.
- `docs/reference/token-case-review-pack-v2-cli.md`: Stage 5AU token case-review pack v2 CLI usage and guardrails.
- `docs/reference/token-case-decision-integration-cli.md`: Stage 5AV token case decision integration CLI usage and guardrails.
- `docs/reference/decision-parser-repair-cli.md`: Stage 5AW decision parser repair CLI usage and guardrails.
- `docs/reference/stego-controls-cli.md`: Stage 5AP stego-control CLI usage and guardrails.

## Architecture And CI Truth

- `ARCHITECTURE.md`: project architecture overview.
- `CUDA_NOTES.md`: CUDA status and deferral requirements.
- `docs/architecture/**`: source-of-truth, freshness, and implementation policy.
- `docs/ci/**`: CI and anti-drift policy.

## Historical And Stage Truth

- `docs/development-logs/**`: dated implementation logs.
- `research-log/**`: summary-only research logs.
- `docs/research/**`: curated research stage docs.
- `data/research/**`: Stage 3Y synthesis records.

Historical docs may mention old stages. Current-state claims must be taken from the operational files above.
