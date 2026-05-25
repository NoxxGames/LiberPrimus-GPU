# Token Case Human Review Workflow

Use this workflow for Stage 5AV manual review of the Stage 5AU token-case challenge pack v2.

1. Start from `data/project-state/stage5au-summary.yaml`.
2. Read the policy in `data/token-block/stage5at-case-review-policy.yaml`.
3. Open the generated local pack at `human-review-packs/stage5au/token-case-review-v2/index.html`.
4. Fill decisions using `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml` or the matching JSON/CSV template.
5. Keep undecidable cases explicit. Do not infer intent, plaintext, or hash meaning.
6. Do not edit the Stage 5AP canonical transcription during manual review.

The Stage 5AT pack is preserved as historical generated output but Stage 5AU records it as count-valid and not usable for reliable decisions. Use the v2 pack because it surfaces glyph-candidate crops, context crops, row context, overlays, all 203 case-review challenges, and all 212 canonical-transcription challenges.

The review pack is ignored local material. Do not commit crops, HTML, overlays, review sheets, ZIP files, or manually filled decision files unless a future prompt explicitly defines a safe integration path.
