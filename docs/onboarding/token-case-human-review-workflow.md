# Token Case Human Review Workflow

## Stage 5BD Note

Stage 5AW repairs parser handling after human decisions were integrated. Stage 5AX adds validation infrastructure only. Stage 5AY designs bounded preflight manifests and gates from Stage 5AW repaired branch metadata. Stage 5AZ repairs duplicate manifest metadata only. Stage 5BB scaffolds the no-execution runner and active-manifest registry only. Stage 5BD adds dry-run planning only. Human decisions remain unchanged, prose fragments are audited rather than stored as token alternatives, and visual placeholders remain review-only.

Use this workflow as the historical Stage 5AV manual-review input process for the Stage 5AU token-case challenge pack v2. Stage 5AV has now integrated the filled template into compact metadata.

1. Start from `data/project-state/stage5au-summary.yaml`.
2. Read the policy in `data/token-block/stage5at-case-review-policy.yaml`.
3. Open the generated local pack at `human-review-packs/stage5au/token-case-review-v2/index.html`.
4. Fill decisions using `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml` or the matching JSON/CSV template.
5. Keep undecidable cases explicit. Do not infer intent, plaintext, or hash meaning.
6. Do not edit the Stage 5AP canonical transcription during manual review.

The Stage 5AT pack is preserved as historical generated output but Stage 5AU records it as count-valid and not usable for reliable decisions. Use the v2 pack because it surfaces glyph-candidate crops, context crops, row context, overlays, all 203 case-review challenges, and all 212 canonical-transcription challenges.

The review pack is ignored local material. Do not commit crops, HTML, overlays, review sheets, ZIP files, or manually filled decision files. Stage 5AV commits only derived decision/branch metadata; Stage 5AW repairs that metadata; Stage 5AY consumes those committed records for design only; Stage 5AZ supersedes only the duplicate bounded variant-family manifest for review.
## Stage 5BD Status

Stage 5BD consumes repaired Stage 5AW branch metadata and does not reopen or reinterpret human review decisions.
