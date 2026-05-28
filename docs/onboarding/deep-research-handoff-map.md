# Deep Research Handoff Map

## Stage 5BK Note

Stage 5BK did not execute Deep Research or any experiment. It consumes Stage 5BJ original/archive crosswalk closure records, Stage 5BI Fandom/source-lock triage records, Stage 5BF local archive metadata, and Stage 5BD token-block dry-run gates. It source-locks iddqd-v2 as compact metadata, records String 4 as page49-51 matrix-hex context only, keeps transcription/translation/key files non-canonical, audits one suspicious Stage 5BJ crosswalk row, and selects Stage 5BL for Deep Research review.

Use `data/historical-route/stage5bk-*`, `data/token-block/stage5bk-*`, `data/source-harvester/stage5bk-*`, `data/project-state/stage5bk-summary.yaml`, and `data/project-state/stage5bk-next-stage-decision.yaml` first for the current review handoff. Do not hand Deep Research raw `third_party/` paths, iddqd-v2 raw bodies, Fandom HTML/images, spreadsheet bodies, full extracted 2014 surface bodies, decoded bytes, fonts, media, or raw page images as source truth. Public website expansion remains a future review-gated project.

## Stage 5BJ Note

Stage 5BJ did not execute Deep Research or any experiment. It consumes Stage 5BI Fandom/source-lock triage, inspects ignored local archive metadata as provenance material, closes or carries forward the high-priority original/archive crosswalk gaps, locks three exact 2014 512-hex surfaces as metadata, preserves page 49-51 token-block lineage unchanged, and selects Stage 5BK for historical-route planning constraint integration. Future handoffs should cite Stage 5BJ, Stage 5BI, Stage 5BF, and Stage 5BD/5BB/5AZ/5AY/5AW records as planning context, not decoded text or solve evidence.

## Repository Context

Repository: `https://github.com/NoxxGames/LiberPrimus-GPU`

Before a Deep Research handoff, verify the latest commit and CI status locally. The handoff should cite the commit hash, stage, and generated bundle paths.

Stage 5BK selects Stage 5BL Deep Research review as the next prompt. Use `data/historical-route/stage5bk-*`, `data/source-harvester/stage5bk-*`, `data/token-block/stage5bk-*`, `data/project-state/stage5bk-summary.yaml`, `data/project-state/stage5bk-next-stage-decision.yaml`, `data/historical-route/stage5bj-*`, `data/source-harvester/stage5bj-*`, `data/token-block/stage5bj-*`, `data/project-state/stage5bj-summary.yaml`, `data/project-state/stage5bj-next-stage-decision.yaml`, `data/historical-route/stage5bi-*`, `data/project-state/stage5bi-summary.yaml`, `data/historical-route/stage5bf-*`, `data/project-state/stage5bf-summary.yaml`, `data/token-block/stage5bd-*`, `data/project-state/stage5bd-summary.yaml`, `data/token-block/stage5bb-*`, `data/project-state/stage5bb-summary.yaml`, `data/token-block/stage5az-*`, `data/project-state/stage5az-summary.yaml`, `data/token-block/stage5ay-*`, `data/project-state/stage5ay-summary.yaml`, `data/token-block/stage5aw-*`, `data/project-state/stage5aw-summary.yaml`, and the page 49-51 lineage records from Stage 5AP through Stage 5AR. Ignored Stage 5BK reports under `experiments/results/historical-route/stage5bk/` and `experiments/results/token-block/stage5bk/`, ignored Stage 5BJ reports under `experiments/results/historical-route/stage5bj/`, ignored Stage 5BF reports under `experiments/results/historical-route/stage5bf/`, ignored content packs under `deep-research-content-packs/stage5bf/`, ignored ZIP outputs under `deep-research-repo-zips/stage5bf/`, ignored Stage 5BD reports under `experiments/results/token-block/stage5bd/`, and ignored review pack v2 under `human-review-packs/stage5au/token-case-review-v2/` are generated aids, not source truth or public publication. Do not hand Deep Research raw `third_party/` paths, iddqd-v2 raw bodies, Fandom HTML/images, spreadsheet bodies, full extracted 2014 surface bodies, decoded bytes, fonts, media, or raw page images as source truth. Public website expansion remains a future review-gated project.

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
- `data/token-block/stage5ap-token-block-canonical-transcription.yaml`
- `data/token-block/stage5ap-token-block-mapping-preflight.yaml`
- `data/token-block/stage5ap-token-block-null-control-plan.yaml`
- `data/token-block/stage5ap-token-block-dwh-context.yaml`

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
## Stage 5BD Archive Markers

Future ZIP-based Deep Research handoffs should use the Stage 5BD archive marker policy and scripts so the archive exposes commit, branch, stage, next-stage, and manifest-hash metadata without requiring `.git/`.

## Stage 5BI Fandom Triage

Stage 5BI records Fandom page triage, item source-lock candidates, original/archive crosswalk candidates, Fandom media non-original policy, 2014 surface context, negative controls, source gaps, and local spreadsheet metadata. The three 2014 256-byte surfaces are context only, not experiment inputs, and must not be combined with page 49-51 without a future explicit source-lock and execution gate.

## Stage 5BJ Crosswalk Closure

Stage 5BJ records 12 original/archive crosswalk closure rows, 3 exact 2014 512-hex surface source locks, 7 Fandom page-body crosswalk rows, a local boards-thread archive-equivalent DOCX record, 8 media-equivalence closure rows, 7 source-gap updates, token-block lineage preservation, guardrails, and Stage 5BK next-stage routing. Fandom pages remain secondary context unless a page-body snapshot is explicitly source-locked, Fandom media remain secondary copies, exact 2014 surface extraction is provenance metadata only, and page 49-51 active records remain unchanged. No token-block execution occurred and no raw/generated files were committed.

## Stage 5BK Planning Constraints

Stage 5BK records iddqd-v2 source-root/tree metadata, 4 byte-string source locks, 2 transcription locks, 4 translation/key-lineage records, 11 positive-control context records, 9 historical family planning statuses, 7 source-gap severity records, and 1 Stage 5BJ errata warning. String 4 is external page49-51 matrix-hex context only and must not replace Stage 5AP or authorize byte-stream generation. The next handoff is Stage 5BL review, not execution.
