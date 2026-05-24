# Source Harvester Community Facts CLI

Stage 5AK extends `libreprimus source-harvester` with community-facts commands:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester inventory-community-facts
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-community-attachment-index
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-community-facts-source-cards
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-community-claim-records
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-community-arithmetic-preflight
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester update-community-deep-research-packs
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ak-guardrail
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ak-next-stage-decision
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-stage5ak-summary
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-stage5ak
```

The commands read the ignored local folder, write compact committed metadata under `data/source-harvester/`, and write private/generated body files under ignored `research-inputs/stage5ak/` and `experiments/results/source-harvester-community-facts/stage5ak/`.

The CLI does not fetch from the network, clone online sources, use Google Drive storage, run Deep Research, perform OCR, interpret images, execute stego/audio tooling, generate or execute hypotheses, run CUDA, benchmark, execute scored experiments, expand the website, or claim a solve.
