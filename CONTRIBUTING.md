# Contributing

## Contribution policy

Contributions should improve reproducibility, documentation, tests, or clearly scoped implementation.

## Development setup

Use the Windows scripts in `scripts/` or equivalent CMake/Python commands from the README.

See `tutorials/` for user-facing setup and workflow guides.

Start with `docs/onboarding/start-here.md` and `docs/onboarding/contributor-module-map.md` before choosing a task lane.

## Coding standards

Follow existing module boundaries and keep behavior small, testable, and documented.

## Testing expectations

Run CTest and pytest when the relevant toolchains are available. CUDA changes require parity tests.

For Stage 2C and later, run the local CI reproduction scripts when touching Python, schema, manifest, or workflow files:

```powershell
.\scripts\ci\run-python-ci.ps1
.\scripts\ci\run-schema-manifest-checks.ps1
```

## Documentation expectations

Update policy documents when behavior, data handling, or experiment rules change.

Tutorial and wiki changes must not include raw corpus dumps, generated JSONL records, or unsupported solve claims. Repository docs and tutorials are the source of truth; wiki pages are mirrors.

When stage status or direction changes, keep `STATUS.md`, `ROADMAP.md`, `AGENTS.md`, `README.md`, and `docs/roadmap/staged-plan.md` synchronized. Update `data/research/project-direction-change-records-v0.yaml` for direction changes and update `docs/onboarding/private-generated-data-map.md` for new raw/private/generated paths. Run the anti-drift and research-synthesis checks before staging documentation-heavy changes:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli consistency check-state-drift
.\.venv\Scripts\python.exe -m libreprimus.cli research-synthesis validate --data-dir data/research --staged-plan docs/roadmap/staged-plan.md
```

## Data rules

Do not modify `data/raw/` in place. Do not commit raw corpus files, local workbooks, local Pastebin TXT, raw transcripts, or generated normalized outputs.

## Issue filing guidance

Useful issues include current status, scope, non-goals, deliverables, acceptance criteria, safety/provenance rules, dependencies, and links to local docs. Do not attach raw data.

## Pull request guidance

Pull requests should state validation commands, changed docs, raw/generated exclusions, and related issues. Keep work scoped and avoid combining project-management changes with corpus or solver changes.

## Experiment result rules

Generated results belong under ignored output locations and must not be committed.

Stage 4B source-lock and visual-intake contributions must promote only allowlisted public sources, preserve visual ambiguity, and keep disabled manifests disabled until a future explicit execution stage. Do not attach raw Discord logs, raw page images, generated Stage 4A site files, or generated Stage 4B triage outputs.

## Pull request checklist

- Scope is limited and documented.
- Tests pass or skipped toolchains are explained.
- GitHub Actions CI remains raw-data-free, CUDA-free, secret-free, and free of default artifact uploads.
- No generated outputs, caches, raw data, installers, logs, or databases are staged.
- Manifest and provenance requirements are preserved.
