# Website Ingest Source Card Format

Stage 5AI prepares website-ingestible metadata only. It does not expand or publish the website.

The committed format summary is `data/source-harvester/stage5ai-website-ingest-format.yaml`.
Generated ingest indexes under `research-inputs/stage5ai/` and
`experiments/results/research-bundles/stage5ai/` remain ignored.

Website ingest records carry:

- source id and bundle id;
- local source classification;
- content availability and extraction status;
- publication status;
- source-card and content-index references;
- explicit `solve_claim=false`;
- explicit `website_expansion_performed=false`.

No raw third-party bytes, generated extracted bodies, images, PDFs, archives, audio/video, raw
Discord logs, or private source paths are website-ready by default. Stage 5AI records `0` public
website-ready bundles and keeps publication review required for generated extracts.

Future website work must consume these metadata records, not ignored generated bodies directly, and
must run a separate publication/privacy review before exposing any source-derived content.
