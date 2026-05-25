# Token Case Human Review Workflow

Use this workflow for Stage 5AU manual review of the Stage 5AT token-case challenge pack.

1. Start from `data/project-state/stage5at-summary.yaml`.
2. Read the policy in `data/token-block/stage5at-case-review-policy.yaml`.
3. Open the generated local pack at `human-review-packs/stage5at/token-case-review/index.html`.
4. Fill decisions using `human-review-packs/stage5at/token-case-review/decision-template.yaml` or the matching JSON/CSV template.
5. Keep undecidable cases explicit. Do not infer intent, plaintext, or hash meaning.
6. Do not edit the Stage 5AP canonical transcription during manual review.

The review pack is ignored local material. Do not commit crops, HTML, review sheets, ZIP files, or manually filled decision files unless a future prompt explicitly defines a safe integration path.
