# Curated Research Bundle Format

Stage 5AI creates local-only curated research bundles under `research-inputs/stage5ai/`.
The generated bundle bodies are ignored and are not publication artefacts.

Committed Stage 5AI records live under `data/source-harvester/stage5ai-*` and describe:

- source cards for local inventory inputs;
- curated bundle skeleton counts;
- content-index summary counts;
- publication-review status;
- missing-source plans;
- guardrails proving no network fetch, Google Drive storage, raw source commit, OCR, AI/ML interpretation, CUDA, scored experiment, benchmark, website expansion, or solve claim.

The generated root contains `master_manifest.yaml`, `source_cards.jsonl`, `content_index.jsonl`,
`website_ingest_index.json`, `deep_research_pack_index.json`, `missing_sources.jsonl`,
global question/assumption notes, and one directory per curated bundle.

Each bundle directory contains metadata and review scaffolds only. Extracted local text snippets are
private generated review inputs and remain ignored unless a later explicit publication stage reviews
and promotes a compact, source-safe record.

## Boundary

Stage 5AI is source-provenance infrastructure. It does not run Deep Research, create hypotheses,
execute experiments, expand the website, process raw Discord logs, run OCR, run image/stego/audio
tools, use CUDA, benchmark, activate the canonical corpus, finalise page boundaries, or make a solve
claim.
