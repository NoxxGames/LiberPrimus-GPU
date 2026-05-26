# Stage 5AW Token Variant Repair

Stage 5AW repaired a Stage 5AV parser-quality issue before bounded token-block preflight design.

The parser now treats `possible_tokens=` as a semicolon-delimited field value rather than an open-ended prose capture. For example, `04|O4 row overlay supports ?4` becomes `04`, `O4`, and the review-only placeholder `?4`; prose is retained only in malformed-fragment audit records.

Research impact:

- Stage 5AW supersedes Stage 5AV branch metadata for future planning.
- Human decisions remain unchanged.
- Canonical transcription remains unchanged.
- Visual placeholders are not primary-60 byte-stream options.
- Malformed prose fragments are auditable but excluded from variant options.
- Stage 5AX can design bounded preflight manifests from the repaired branch surface.

The repaired records are not solve evidence and do not authorize execution.
