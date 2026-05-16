# Stage 2C-followup-4 Public Docs Status

## Status

Public README/STATUS/ROADMAP status correction and regression checks.

## Goal

Make the public top-level documentation reflect that Stage 2A, Stage 2B, and Stage 2C are complete; that known solved baselines total 10 passing fixtures; and that Stage 2D is the next milestone before any bounded CPU exploratory experiment scaffolding.

## Result

README, STATUS, and ROADMAP now present Stage 2A, Stage 2B, and Stage 2C as completed infrastructure and identify Stage 2D as the next milestone. Public documentation status checks were added to pytest and local CI scripts so stale top-level status or minified public Markdown is caught before push.

Local validation passed:

- Full pytest: `252 passed in 42.38s`
- Ruff: passed.
- Python smoke: passed.
- Registry and manifest validation: passed.
- Lock and workflow static validation: passed.

## Non-goals

No unsolved-page search, scoring, CUDA implementation, canonical corpus activation, or page-boundary finalization was added.
