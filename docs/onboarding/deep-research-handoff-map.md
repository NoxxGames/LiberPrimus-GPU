# Deep Research Handoff Map

## Repository Context

Repository: `https://github.com/NoxxGames/LiberPrimus-GPU`

Before a Deep Research handoff, verify the latest commit and CI status locally. The handoff should cite the commit hash, stage, and generated bundle paths.

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
- `experiments/results/discord-full-review/stage4a/`

Only pass redacted topic shards, aggregate summaries, public links, public source records, and curated observation/negative-control records. Prefer small focused bundles over huge dumps.

Stage 4A also creates an SFTP-ready static review site:

- `experiments/results/discord-full-review/stage4a/site/index.html`
- `experiments/results/discord-full-review/stage4a/deep_research_bundle_manifest.yaml`
- `experiments/results/discord-full-review/stage4a/SFTP_UPLOAD_INSTRUCTIONS.md`

Use the Stage 4A static site or redacted shards for Deep Research handoff. Do not substitute raw
Discord HTML exports for the generated redacted bundle.

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
