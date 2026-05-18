# Stage 3X CLI Modularisation

## Scope

Stage 3X modularises the Python CLI without changing behavior. It keeps `python -m libreprimus.cli` as the public entrypoint and moves command groups under `python/libreprimus/cli_commands/`.

## Initial State

- Starting commit: `d8a5e97178bc4493f7360a482566f19b1bd41da9`
- Branch: `main`
- Local HEAD matched `origin/main`.
- Latest known CI after Stage 3W: run `26060038131`, passing.
- `python/libreprimus/cli.py` initial line count: `4875`.
- Existing state-drift and consistency checks passed before edits.
- Raw/generated outputs were not staged.

## Implementation Notes

- Added `python/libreprimus/cli_commands/`.
- Kept `python/libreprimus/cli.py` as a thin entrypoint exposing `app`.
- Moved command groups into domain modules while preserving Typer command names and options.
- Added command-surface tests for root groups, key subcommands, help output, and package layout.
- Added CLI modularisation architecture and reference docs.

## Validation

- `python -m libreprimus.cli --help`: passed.
- `python -m libreprimus.cli consistency --help`: passed.
- `python -m libreprimus.cli consistency check-state-drift`: passed.
- `python -m libreprimus.cli consistency check-all --allow-warnings`: passed.
- `python -m libreprimus.cli smoke`: passed.
- `ruff check python/libreprimus tests/python`: passed.
- `pytest -q tests/python`: `846` passed.
- Local CI consistency, public-doc status, lock-hash, workflow-static, and wiki-source validation passed.

## Policy

No experiments were executed. No raw/generated outputs, raw Discord logs, raw page images, raw historical artefacts, SQLite files, or local deep-research reports are part of this stage.
