# Contributing

## Contribution policy

Contributions should improve reproducibility, documentation, tests, or clearly scoped implementation.

## Development setup

Use the Windows scripts in `scripts/` or equivalent CMake/Python commands from the README.

## Coding standards

Follow existing module boundaries and keep behavior small, testable, and documented.

## Testing expectations

Run CTest and pytest when the relevant toolchains are available. CUDA changes require parity tests.

## Documentation expectations

Update policy documents when behavior, data handling, or experiment rules change.

## Data rules

Do not modify `data/raw/` in place. Do not commit raw corpus files in Stage 0A.

## Experiment result rules

Generated results belong under ignored output locations and must not be committed.

## Pull request checklist

- Scope is limited and documented.
- Tests pass or skipped toolchains are explained.
- No generated outputs, caches, raw data, installers, logs, or databases are staged.
- Manifest and provenance requirements are preserved.
