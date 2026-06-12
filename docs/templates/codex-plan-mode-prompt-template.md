# Codex Plan-Mode Prompt Template

Use this template for multi-file, governance, source-lock, validation, or stage-routing work.

Required Fields:
- stage_id
- scope
- authoritative_current_truth: `data/project-state/current-stage-state.yaml`
- guardrails
- files expected to change
- files explicitly not to change
- validation plan
- commit/push/CI plan

Stage 5EF Evidence Fields:
- plan_mode_used_for_stage5ef: true
- plan_review_performed_before_editing: true
- plan_amendment_applied_before_editing: true
- plan_deviation_count: 0 unless real deviations occur
