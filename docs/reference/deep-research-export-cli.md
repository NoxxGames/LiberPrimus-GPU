# Deep Research Export CLI

Stage 5AN commands are exposed under:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli deep-research-export --help
```

Primary commands:

- `build-stage5an-content-pack`
- `build-stage5an-hosted-export`
- `build-stage5an-combined-webroot`
- `build-stage5an-guardrail`
- `build-stage5an-next-stage-decision`
- `build-stage5an-summary`
- `validate-stage5an`
- `summary`

The build commands may read ignored `research-inputs/` and safe local-source roots. They write generated outputs under `deep-research-content-packs/stage5an/` and `website-export/stage5an/`, plus compact committed metadata under `data/deep-research-export/`.

Use repeated flags for multiple roots:

```powershell
--research-input-roots research-inputs/stage5ai `
--research-input-roots research-inputs/stage5aj `
--research-input-roots research-inputs/stage5ak `
--research-input-roots research-inputs/stage5al
```

Do not use these commands to fetch from the network, clone repositories, run Deep Research, or publish generated content publicly.
