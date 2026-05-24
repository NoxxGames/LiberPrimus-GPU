# Extraction Fidelity And Redaction Policy

Stage 5AJ makes extraction fidelity a first-class source-harvester contract for private Deep Research handoffs. Private extracts should preserve technical content aggressively: rune strings, number sequences, hashes, URLs, formulas, sheet names, cell coordinates, highlight state, table shape, and workbook metadata are evidence-bearing context and must not be stripped by default.

Redaction is minimal and logged. It may remove credentials, private identities, access tokens, private file-system paths, or clearly unsafe operational details, but each removal must be recorded with reason and scope. Public website ingest is a separate conservative view and remains review-gated; Stage 5AJ records `0` public website-ready bundles.

Raw `third_party/UsefulFilesAndIdeas/` files and generated workbook-cell indexes remain ignored local material. Committed records are compact metadata summaries only and are not source truth, hypotheses, experiment seeds, or solve evidence.
