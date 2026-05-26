# Token Case Decision Integration Workflow

Use this workflow after a human reviewer fills the Stage 5AU v2 decision template.

1. Keep the filled file local and ignored at `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`.
2. Run the Stage 5AV ingest and validation commands.
3. Build decision records, unresolved variant records, branch-manifest metadata, updates, and summary records.
4. Run `validate-stage5av`.
5. Do not stage the decision template, generated HTML/crops, JSON reports, or variant bodies.

Unresolved cases should keep `selected_token: null` and place alternatives in `reviewer_notes` as `possible_tokens=...`. Stage 5AV preserves these branches for future bounded preflight design and does not change the canonical transcription.

Stage 5AW repairs the Stage 5AV possible-token parser before preflight design proceeds. Stage 5AX then adds validation infrastructure only. Stage 5AY planning uses `data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml`, not the original Stage 5AV branch manifest. Stage 5AZ repairs the duplicate bounded variant-family ID before review, and Stage 5BB makes the Stage 5AW branch manifest active through the no-execution runner registry. Neither stage changes Stage 5AV decisions or Stage 5AW branch semantics. Valid reviewer extras are preserved, visual placeholders are review-only and primary-60 unmappable, and prose fragments are stored only in malformed-fragment audit records.
