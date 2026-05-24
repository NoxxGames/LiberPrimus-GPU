# Deep Research Handoff Map

## Repository Context

Repository: `https://github.com/NoxxGames/LiberPrimus-GPU`

Before a Deep Research handoff, verify the latest commit and CI status locally. The handoff should cite the commit hash, stage, and generated bundle paths.

Stage 5AN selects Stage 5AO Deep Research source inventory and reliability review with private content as the next prompt. Use `data/source-harvester/stage5al-deep-research-export.yaml`, `data/website-ingest/stage5al/`, `data/website-render/stage5am-summary.yaml`, `data/deep-research-export/stage5an-summary.yaml`, and ignored `research-inputs/stage5al/` helper files. The ignored static index under `website-export/stage5am/research-index/` is a metadata review aid, and the ignored private content library under `website-export/stage5an/private-content/` is a private generated handoff, not source truth or public publication. These records summarize the Stage 5AI curated bundles, Stage 5AJ UsefulFiles metadata, and Stage 5AK community claim records behind publication gates. Do not hand Deep Research raw `third_party/` paths as source truth. Public website expansion remains a future review-gated project.

## Files Deep Research Should Inspect First

- `README.md`
- `STATUS.md`
- `docs/roadmap/staged-plan.md`
- `docs/onboarding/start-here.md`
- `docs/onboarding/source-of-truth-map.md`
- `docs/experiments/method-retirement-ledger.md`
- Relevant `research-log/**` summaries.

## Generated/Redacted Bundles To Use

Use generated, redacted, local-only review bundles when a stage creates them under ignored paths, such as:

- `experiments/results/discord-review-bundles/stage3q/`
- `experiments/results/source-harvester/stage5af/research_bundles_preview/`
- `experiments/results/source-harvester-local/stage5ag/research_bundle_readiness.json`
- `research-inputs/stage5ai/`
- `research-inputs/stage5aj/`
- `data/source-harvester/stage5ai-curated-research-bundle-summary.yaml`
- `data/source-harvester/stage5aj-summary.yaml`
- `docs/onboarding/deep-research-ingest-format.md`
- `experiments/results/discord-full-review/stage4a/`

Only pass redacted topic shards, aggregate summaries, public links, public source records, and curated observation/negative-control records. Prefer small focused bundles over huge dumps.

Stage 4A also creates an SFTP-ready static review site:

- `experiments/results/discord-full-review/stage4a/site/index.html`
- `experiments/results/discord-full-review/stage4a/deep_research_bundle_manifest.yaml`
- `experiments/results/discord-full-review/stage4a/SFTP_UPLOAD_INSTRUCTIONS.md`

Use the Stage 4A static site or redacted shards for Deep Research handoff. Do not substitute raw
Discord HTML exports for the generated redacted bundle.

If the static site is hosted for review, use the Stage 4A follow-up privacy-hardened rebuild. It
includes noindex metadata, `robots.txt`, a site privacy notice, SFTP checklist, and site manifest.

## Do Not Give Deep Research

- Raw Discord HTML logs.
- Message bodies, usernames, user IDs, message IDs, or private Discord CDN URLs.
- Raw private attachments.
- Raw Liber Primus page images unless a future source-lock stage explicitly scopes them.
- Large generated dumps without redaction and scope.

## Stage 4A Bundle

Stage 4A prepares full Discord research-bundle extraction for Deep Research from local HTML exports.
It produces redacted, structured, image-aware bundles and a static site that Deep Research can use
without publishing raw logs.

## Stage 4B Intake From Deep Research

Stage 4B ingests the Stage 4A Discord Research-Bundle Review into durable project records:

- promoted public-source records under `data/observations/archive/stage4b-promoted-source-records.yaml`;
- source-health records under `data/locks/third-party/stage4b-source-health-records.yaml`;
- review-only visual observations under `data/observations/visual/stage4b-visual-observation-records.yaml`;
- negative controls under `data/observations/research/stage4b-negative-control-records.yaml`;
- disabled future manifests under `experiments/manifests/stage4b-disabled/`.

Future Deep Research handoffs should prefer these curated records plus the redacted Stage 4A site. Do not hand off raw Discord logs or raw local page images.
