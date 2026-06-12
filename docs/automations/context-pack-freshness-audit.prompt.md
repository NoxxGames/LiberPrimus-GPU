# Stage 5EF Report-Only Automation Template: context_pack_freshness_audit

Purpose: Report context-pack freshness gaps only.

Rules:
- Report-only.
- Do not auto-commit.
- Do not execute puzzle work.
- Do not add source-lock evidence.
- Do not mutate raw, third-party, generated, or `codex-output` roots.
- Do not schedule this template automatically; a later explicit prompt is required.

Report Fields:
- stage_id: `stage-5ef`
- current_truth_authority: `data/project-state/current-stage-state.yaml`
- findings
- warnings
- recommended_next_stage_id: `stage-5eg`
