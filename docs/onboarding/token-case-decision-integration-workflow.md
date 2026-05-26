# Token Case Decision Integration Workflow

Use this workflow after a human reviewer fills the Stage 5AU v2 decision template.

1. Keep the filled file local and ignored at `human-review-packs/stage5au/token-case-review-v2/decision-template.yaml`.
2. Run the Stage 5AV ingest and validation commands.
3. Build decision records, unresolved variant records, branch-manifest metadata, updates, and summary records.
4. Run `validate-stage5av`.
5. Do not stage the decision template, generated HTML/crops, JSON reports, or variant bodies.

Unresolved cases should keep `selected_token: null` and place alternatives in `reviewer_notes` as `possible_tokens=...`. Stage 5AV preserves these branches for future bounded preflight design and does not change the canonical transcription.
