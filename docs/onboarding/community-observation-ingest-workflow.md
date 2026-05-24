# Community Observation Ingest Workflow

Use this workflow when a local community observation bundle is supplied outside normal scraping access.

1. Keep the raw folder under ignored `third_party/**`.
2. Hash and inventory files without committing raw text, images, audio, archives, or generated extracts.
3. Preserve message locators and attachment order in ignored private extracts.
4. Commit only compact source-card, content-index, claim, correction, arithmetic-preflight, readiness, guardrail, and summary metadata.
5. Mark public website publication blocked until a later review stage.
6. Keep private Deep Research handoff files under ignored `research-inputs/**`.

Community observations are claims to review, not facts to execute. Do not run OCR, AI/ML interpretation, image forensics, stego/audio tooling, CUDA, benchmarks, scored experiments, hypothesis generation/execution, source crawling, website expansion, corpus activation, page-boundary finalisation, method-status upgrades, or solve-claim workflows during ingest.
