# Fast Local Validation

Use the Stage 5AX wrappers when a Codex turn needs faster local validation:

```powershell
.\scripts\ci\run-parallel-validation.ps1 -Workers 16 -PytestWorkers 16 -PytestMode auto
```

On systems with Bash:

```bash
bash scripts/ci/run-parallel-validation.sh --workers 16 --pytest-workers 16 --pytest-mode auto
```

The wrappers rebuild the Stage 5AX plan, run pytest plus read-only checks through the parallel harness, build summary records, and validate the records. They are opt-in; the existing serial CI scripts remain the default conservative path.

Environment overrides:

- `LIBERPRIMUS_VALIDATION_WORKERS`
- `LIBERPRIMUS_PYTEST_WORKERS`
- `LIBERPRIMUS_PYTEST_MODE`
- `LIBERPRIMUS_PARALLEL_VALIDATION_RESULTS_DIR`

Generated logs remain ignored. Run git safety checks serially before staging or pushing.
