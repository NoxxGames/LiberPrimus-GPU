# Token Case Review Pack V2 Workflow

## Stage 5BB Note

The filled Stage 5AU v2 decision template remains local and ignored. Stage 5AW consumed it only to rebuild compact repaired metadata and does not change generated review-pack files, crops, overlays, or canonical transcription. Stage 5AX adds validation infrastructure only, Stage 5AY records bounded preflight design without execution, Stage 5AZ repairs duplicate manifest metadata without execution, and Stage 5BB records runner-scaffold metadata without execution.

Use Stage 5AU records when preparing the next manual review:

1. Open the ignored local pack at `human-review-packs/stage5au/token-case-review-v2/index.html`.
2. Review the cell, glyph-candidate, context, row, strip, and overlay crops together.
3. Fill a copy of the blank v2 decision template manually.
4. Keep ambiguous cases marked as unresolved rather than forcing a token choice.
5. Do not use OCR, AI/ML, LLM vision, image interpretation, stego, hash/preimage search, CUDA, or scored experiments to fill decisions.

The generated crops are aids for review only. Canonical transcription remains unchanged until a later explicit integration stage validates human decisions.

Stage 5AV is that integration stage. It validates the filled local template, records 126 keep-current confirmations and 77 unresolved branches, preserves reviewer-declared possible tokens, and still keeps canonical transcription unchanged because no explicit `change_token` decisions were present.
