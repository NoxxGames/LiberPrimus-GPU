# Doc Staleness Stage Ledger Checks

Stage 5AH adds stage-ledger coverage on top of the Stage 5AB document-staleness scanner.

The check looks for mutable operational sections that claim to summarize implemented, completed, current, or latest work. If such a ledger contains enough stage entries to be operational and its maximum stage is older than the expected latest stage, the check fails. Historical snapshots and clearly archival sections are exempt.

The Stage 5AH expected state is:

- Latest completed stage: `Stage 5AH`
- Next stage: `Stage 5AI`
- Source of truth: `data/project-state/stage5ah-doc-staleness-source-of-truth.yaml`
- Operational map: `data/project-state/operational-file-map.yaml`

Generated reports stay under `experiments/results/doc-staleness/stage5ah/` and are not committed. The committed records are compact summaries under `data/project-state/`.

The checks are process-quality infrastructure only. They do not process raw sources, run Deep Research, execute CUDA, benchmark, run scored experiments, expand the website, or make solve claims.
