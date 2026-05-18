# CLI Command Modularisation

Stage 3X keeps `python -m libreprimus.cli` as the public command entrypoint while moving command registration and command bodies into `python/libreprimus/cli_commands/`.

## Public Entry Point

- `python/libreprimus/cli.py` remains importable and exposes `app`.
- Tests and users should continue to invoke `python -m libreprimus.cli ...`.
- Do not create `python/libreprimus/cli/` while `cli.py` exists; it conflicts with the module entrypoint.

## Internal Layout

- `cli_commands/root.py` owns the root Typer app and registers domain modules.
- `cli_commands/common.py` keeps shared imports, console formatting, default paths, and common path helpers.
- Domain modules own command groups such as `consistency`, `post-discord`, `stego`, Discord review commands, bounded-run commands, solved fixtures, and result-store commands.

Stage 3X is mechanical: command names, options, help text, and output semantics are intended to remain unchanged.

## Change Policy

Future CLI edits should add or update command-surface tests when they add, remove, rename, or move commands. Behavior changes should be staged separately from mechanical modularisation.
