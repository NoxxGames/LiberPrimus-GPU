# Context Packs

Stage 5EF adds deterministic context-pack templates only. They contain no wall-clock timestamps, local paths,
temporary output paths, or worktree-dirt snapshots.

Templates:
- `number_fact_enrichment` -> `docs/context-packs/context-pack-number-fact-enrichment.md`
- `source_lock_addendum` -> `docs/context-packs/context-pack-source-lock-addendum.md`
- `validation_repair` -> `docs/context-packs/context-pack-validation-repair.md`
- `target_priority` -> `docs/context-packs/context-pack-target-priority.md`
- `experiment_design` -> `docs/context-packs/context-pack-experiment-design.md`
- `doc_drift` -> `docs/context-packs/context-pack-doc-drift.md`

Generated or volatile context-pack outputs belong under ignored output roots, not committed docs.
