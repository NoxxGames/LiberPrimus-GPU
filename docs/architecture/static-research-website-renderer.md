# Static Research Website Renderer

Stage 5AM adds `libreprimus website-render`, a metadata-only static renderer for the Stage 5AL website-ingest package. It reads committed JSON/YAML under `data/website-ingest/stage5al/` and writes an ignored uploadable export under `website-export/stage5am/research-index/`.

The renderer is intentionally conservative:

- It renders source cards, bundle cards, content metadata, community-claim metadata, missing-source metadata, publication gates, and Deep Research handoff metadata.
- It does not publish raw source bodies, private Discord/forum bodies, extracted workbook cells, raw images, PDFs, archives, audio, video, or generated private bundle bodies.
- It includes `robots.txt` with `Disallow: /` and every HTML page has `noindex,nofollow,noarchive`.
- Publication gates are displayed as review state, not overridden.

The generated site is a private/review-gated navigation surface. It is not public website publication, not Deep Research output, not experiment execution, and not solve evidence.
