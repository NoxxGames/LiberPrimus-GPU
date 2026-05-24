# Research Website-Ingest Contract

Stage 5AL defines a metadata-only website-ingest package at `data/website-ingest/stage5al/`.
It is a data contract for a future website or static index, not a public website
publication.

The package contains research bundle cards, source-card metadata, content-index metadata,
community-claim metadata, publication gates, missing-source records, and a Deep Research
export pointer. It must not contain raw message bodies, private identifiers, raw images,
raw workbook bodies, full article dumps, generated extract bodies, local absolute paths,
tokens, cookies, or credentials.

Public website-ready remains `0` after Stage 5AL. Future website pages must use the
publication-gate records before displaying any source or claim metadata.

Deep Research should consume the Stage 5AL export manifest and ignored private export files
under `research-inputs/stage5al/`, not raw `third_party/` paths.
