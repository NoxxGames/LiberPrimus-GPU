# Stage 5AL Website-Ingest CLI

Stage 5AL extends `libreprimus source-harvester` with:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-website-ingest-stage5al
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester build-deep-research-export-stage5al
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-website-ingest-stage5al
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-stage5al
```

The build commands use committed Stage 5AI, Stage 5AJ, and Stage 5AK metadata plus local
ignored research-input metadata when present. They do not require network access and do not
read raw third-party bodies.

Validation enforces publication gates, no public website publication, no local absolute
paths, no private claim body fields, no Deep Research execution, no CUDA, no benchmarks,
and no solve claim.
