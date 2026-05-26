# Token Case Review Pack V2 Workflow

Use Stage 5AU records when preparing the next manual review:

1. Open the ignored local pack at `human-review-packs/stage5au/token-case-review-v2/index.html`.
2. Review the cell, glyph-candidate, context, row, strip, and overlay crops together.
3. Fill a copy of the blank v2 decision template manually.
4. Keep ambiguous cases marked as unresolved rather than forcing a token choice.
5. Do not use OCR, AI/ML, LLM vision, image interpretation, stego, hash/preimage search, CUDA, or scored experiments to fill decisions.

The generated crops are aids for review only. Canonical transcription remains unchanged until a later explicit integration stage validates human decisions.

Stage 5AV is that integration stage. It validates the filled local template, records 126 keep-current confirmations and 77 unresolved branches, preserves reviewer-declared possible tokens, and still keeps canonical transcription unchanged because no explicit `change_token` decisions were present.
