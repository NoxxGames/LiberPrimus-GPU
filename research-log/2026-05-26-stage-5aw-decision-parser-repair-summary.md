# Stage 5AW Decision Parser Repair Summary

Stage 5AW repaired a Stage 5AV possible-token parser quality issue. The Stage 5AV reviewer-extra set contained three prose fragments that were accidentally captured as token alternatives.

The repaired parser preserves valid two-character reviewer extras, extracts visual placeholders such as `?4` and `3?` into review-only unmappable metadata, and records malformed prose fragments in an audit file instead of storing them as reviewer-extra possible tokens.

Result: Stage 5AW found `3` malformed fragments, preserved `10` valid reviewer-extra tokens, preserved `2` visual placeholders, kept canonical transcription unchanged, and selected Stage 5AX bounded token-block preflight manifest design without execution.
