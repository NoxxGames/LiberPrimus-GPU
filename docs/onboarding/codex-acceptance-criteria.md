# Codex Acceptance Criteria

Future Codex stage work must define acceptance criteria that inspect final repository files, not only self-attesting metadata records. Current mirrors, handoff files, hook reports, source-root policies, traceability rows, and no-execution guardrails must be validated after all build and doc-generation steps finish.

Bad instruction:
"Update AGENTS.md."

Good instruction:
"Update AGENTS.md as a whole final file, then verify its current section matches current-stage-state.yaml, contains no repeated generated phrases, contains no stale latest/next-stage claims, and contains no stale completion-summary path."

For current-stage updates, validators must read the final files directly, compare latest and next-stage claims to `data/project-state/current-stage-state.yaml`, reject stale handoff paths, and run the strict stale-current scanner before staging.
