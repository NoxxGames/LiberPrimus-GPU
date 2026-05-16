# Contributing

## Contribution policy

Contributions should improve reproducibility, documentation, tests, or clearly scoped implementation.

## Development setup

Use the Windows scripts in `scripts/` or equivalent CMake/Python commands from the README.

See `tutorials/` for user-facing setup and workflow guides.

## Coding standards

Follow existing module boundaries and keep behavior small, testable, and documented.

## Testing expectations

Run CTest and pytest when the relevant toolchains are available. CUDA changes require parity tests.

## Documentation expectations

Update policy documents when behavior, data handling, or experiment rules change.

Tutorial and wiki changes must not include raw corpus dumps, generated JSONL records, or unsupported solve claims. Repository docs and tutorials are the source of truth; wiki pages are mirrors.

## Data rules

Do not modify `data/raw/` in place. Do not commit raw corpus files, local workbooks, local Pastebin TXT, raw transcripts, or generated normalized outputs.

## Issue filing guidance

Useful issues include current status, scope, non-goals, deliverables, acceptance criteria, safety/provenance rules, dependencies, and links to local docs. Do not attach raw data.

## Pull request guidance

Pull requests should state validation commands, changed docs, raw/generated exclusions, and related issues. Keep work scoped and avoid combining project-management changes with corpus or solver changes.

## Experiment result rules

Generated results belong under ignored output locations and must not be committed.

## Pull request checklist

- Scope is limited and documented.
- Tests pass or skipped toolchains are explained.
- No generated outputs, caches, raw data, installers, logs, or databases are staged.
- Manifest and provenance requirements are preserved.
