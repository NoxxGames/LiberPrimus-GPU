# Static Research Index Workflow

Use the Stage 5AM static research index when you need a browser-readable view of Stage 5AL metadata. Use the Stage 5AN combined webroot when you need both the metadata index and private content library for Deep Research handoff. Use Stage 5AR coordinate records and Stage 5AP token-block records only as metadata references for Stage 5AS review.

1. Build the site with `libreprimus website-render build-stage5am-site`.
2. Validate it with `libreprimus website-render validate-stage5am`.
3. Open or upload `website-export/stage5am/research-index/`.
4. Do not upload raw or generated-private folders.
5. For Stage 5AN hosted handoff, copy the contents of `website-export/stage5an/webserver-root/` to the private webserver root after validation.

The Stage 5AM site is metadata-only. It includes no raw source bodies, no private identifiers, no generated extraction bodies, no solve claims, and no Deep Research report text. The Stage 5AN private content library is still generated private handoff material and requires access-control review if hosted. Stage 5AP token-block material and Stage 5AR coordinate material remain source-lock/preflight metadata and must not be displayed as decoded plaintext or image interpretation.
