# Source Harvester Curated Bundles CLI

Stage 5AI extends `libreprimus source-harvester` with curated-bundle commands.

Typical local run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester classify-local-sources
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-source-cards
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-curated-bundles
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-content-index
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-website-ingest-index
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-deep-research-pack-index
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-missing-source-plan
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ai-guardrail
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ai-readiness
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ai-next-stage-decision
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ai-summary
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-stage5ai
```

Generated bundle bodies are written under `research-inputs/stage5ai/` and generated reports under
`experiments/results/research-bundles/stage5ai/`. Both are ignored except for README/.gitkeep
directory scaffolds.

The CLI is local-only by default. Stage 5AI does not fetch, clone, use Google Drive as project
storage, run Deep Research, run OCR/AI/ML, run image/stego/audio tools, run CUDA, benchmark, execute
scored experiments, or make solve claims.
