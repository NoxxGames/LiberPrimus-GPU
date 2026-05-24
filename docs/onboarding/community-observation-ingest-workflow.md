# Community Observation Ingest Workflow

Use this workflow when a local community observation bundle is supplied outside normal scraping access.

1. Keep the raw folder under ignored `third_party/**`.
2. Hash and inventory files without committing raw text, images, audio, archives, or generated extracts.
3. Preserve message locators and attachment order in ignored private extracts.
4. Commit only compact source-card, content-index, claim, correction, arithmetic-preflight, readiness, guardrail, and summary metadata.
5. Mark public website publication blocked until a later review stage.
6. Keep private Deep Research handoff files under ignored `research-inputs/**`.

Community observations are claims to review, not facts to execute. Do not run OCR, AI/ML interpretation, image forensics, stego/audio tooling, CUDA, benchmarks, scored experiments, hypothesis generation/execution, source crawling, website expansion, corpus activation, page-boundary finalisation, method-status upgrades, or solve-claim workflows during ingest.

Stage 5AL exports community-claim metadata to `data/website-ingest/stage5al/community-claims.yaml` without raw message bodies, formulas, claimed-values maps, private message locators, or attachment bodies. Stage 5AM renders only that metadata into the ignored private static research index and preserves the publication gate labels. Stage 5AN includes only review-gated private handoff content and keeps raw community logs/attachments out of committed files. Publication remains blocked/private until a future review stage changes the gate.
