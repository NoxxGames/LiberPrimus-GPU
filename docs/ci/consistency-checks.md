# Consistency Checks

## Purpose

Stage 2D adds a raw-data-free consistency suite that checks whether committed
schemas, manifests, registry metadata, documentation, ignored-output policy, and
result-store definitions still agree.

## Check Groups

- Registry consistency: transform IDs, aliases, fixture-set paths, SHA locks,
  and disabled search/CUDA/scoring flags.
- Manifest consistency: solved-baseline, result-store, and exploratory dry-run
  manifests, registry SHA references, fixture directories, expected counts,
  candidate-count bounds, and false capability flags.
- Schema consistency: JSON parsing, expected schema files, unique schema
  metadata, record type constants, and non-canonical trust flags.
- Documentation consistency: README, STATUS, ROADMAP, AGENTS, and cipher catalog
  status claims.
- Ignored-output consistency: raw paths, generated outputs, SQLite databases,
  and committed schemas/manifests/profiles.
- Result-store consistency: Stage 2B manifest and local generated outputs when
  present.
- State-drift consistency: long-lived operational docs agree on current stage,
  canonical corpus inactive status, page-boundary review status, CUDA deferral,
  raw/generated output policy, Discord privacy, and no-solve-claim policy.

## Local Commands

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-all --allow-warnings
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings
.\scripts\ci\run-consistency-checks.ps1
```

Linux/macOS:

```sh
python -m libreprimus.cli consistency check-all --allow-warnings
python -m libreprimus.cli consistency check-state-drift
python -m libreprimus.cli consistency check-result-store --allow-missing-generated --allow-warnings
scripts/ci/run-consistency-checks.sh
```

## CI Integration

GitHub Actions runs the consistency suite in the Python CI job after the
registry and manifest validation commands. The check is raw-data-free and does
not require generated local result-store outputs.

Stage 3W adds anti-drift checks to `check-all` and to the local CI helper
scripts.

Stage 2E also validates exploratory dry-run manifests and runs a Caesar preview
dry run into a temporary CI directory.

Stage 2F validates CPU execution manifests and runs a synthetic direct execution
smoke into an ignored generated output directory.

## Raw-Data-Free Policy

The suite checks ignored raw paths, but it does not read or require local raw
transcripts, Pastebin files, workbooks, or mirrored reference repositories.

## Generated-Output Policy

Generated summaries may be written under `experiments/results/consistency/`.
Those summaries are ignored by Git. CI exports any temporary summary to a temp
directory, not to a committed path.

## Failure Handling

Any failing check returns a non-zero CLI exit. Warnings are allowed only when
the caller passes `--allow-warnings`; this is used for optional local generated
outputs that are absent on a clean CI checkout.

## Future Extensions

Stage 2G extends the suite to proposal schemas, blocked proposal examples,
pending/denied approval examples, and ignored proposal review packet paths.

Future stages can add scorer metadata checks and result-store import checks for
new committed manifest types before any unsolved-page campaign is allowed to run.
