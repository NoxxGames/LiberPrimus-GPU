# Score Record Policy

Score records are review aids. They cannot override source provenance, solved-baseline fixtures, corpus status, page-boundary review status, or experiment manifests.

Required safety fields:

- `solve_claim=false`
- `trusted_as_canonical=false`
- `cuda_used=false`

Scoring records must preserve:

- scorer id and version
- calibration profile id or explicit `calibration_not_available`
- candidate and input stream identifiers
- transform family
- score status
- finite confidence label where scoring is available

New scorers require scorer records, compatibility mapping, tests, and calibration notes before they can appear in CPU batch summaries.
