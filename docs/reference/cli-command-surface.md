# CLI Command Surface

Entrypoint:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli
```

Stage 3X intentionally preserves the existing command names and options. This reference is a concise command-surface map, not a generated full help dump.

## Root Commands

- `smoke`
- `paths`
- `toolchain`

## Command Groups

- `legacy-workbook`
- `legacy-pastebin`
- `transcript-source`
- `corpus-alignment`
- `profile`
- `corpus-candidate`
- `reference-source`
- `transform-registry`
- `solved-baseline`
- `result-store`
- `consistency`
- `experiment`
- `execution`
- `proposal`
- `approval-execution`
- `approval-readiness`
- `bounded-experiment`
- `bounded-run`
- `candidate-inspect`
- `scoring`
- `archive`
- `observation`
- `hash-preimage`
- `image-analysis`
- `image-transform`
- `discord-ingest`
- `discord-promote`
- `discord-review`
- `discord-leads`
- `post-discord`
- `research-synthesis`
- `stego`
- `solved-fixture`
- `token-block`
- `stego-controls`

## Guarded Commands

Stage 3X tests explicitly cover:

- `consistency check-state-drift`
- `consistency check-all`
- `stego outguess-run`
- `post-discord run-onion7-seed-pack`
- `post-discord run-gp-rune-verifier`
- `post-discord run-cookie-signed-variants`
- `research-synthesis validate`
- `token-block validate-stage5ap`
- `stego-controls validate-stage5ap-outguess`

Future command changes should update this file and the Stage 3X command-surface tests together.
