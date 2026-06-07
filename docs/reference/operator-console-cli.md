# Operator Console CLI

Stage 5DQ adds `libreprimus operator-console` and `libreprimus source-browser` command groups for review-only source browsing.

## Commands

Build the ignored local index cache:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console build-source-index
```

Validate committed metadata loading plus Source Browser config:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console validate-source-index
```

Validate manual entries, overrides, and tombstones:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console validate-manual-entries
```

Print a compact source-browser summary:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console summary
```

Report the local context-file status:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console open-context
```

Run the optional GUI:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli operator-console run
```

The GUI command requires the optional `gui` extras. Without PySide6, it exits with an installation hint and CI remains valid.

Aliases:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser run
.\.venv\Scripts\python.exe -m libreprimus.cli source-browser validate-index
```

## Boundary

The CLI never runs puzzle execution. It does not run route extraction, OCR, image forensics, AI/ML interpretation, scoring, DWH/hash search, byte-stream generation, CUDA, or source files. Generated index caches live under `.cache/operator-console/**` and must remain ignored.
