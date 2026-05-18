# Stage 3X CLI Modularisation

Stage 3X is a maintainability stage. It split the large Python CLI entrypoint into focused command modules without adding experiment behavior, changing schemas, processing raw data, using CUDA, activating the canonical corpus, finalizing page boundaries, or making a solve claim.

The public command remains:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli --help
```

The command surface is guarded by tests that check root groups, key post-Discord and stego commands, help output, package layout, and the thin-entrypoint line count.

Generated outputs and raw artefacts remain outside the commit surface.
