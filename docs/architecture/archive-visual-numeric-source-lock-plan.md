# Archive Visual Numeric Source-Lock Plan

Stage 5AF prepares source-lock inventory before any hypothesis execution. The source-lock sequence is:

1. Validate the committed source manifest and priority records.
2. Plan capture work without fetching.
3. Place user-provided exports/downloads under ignored local roots such as `source-harvester-output/`, `harvest-output/`, or `research-inputs/`.
4. Hash and inventory local files.
5. Extract only deterministic summaries, links, text snippets, image metadata, or bundle scaffolds when explicitly scoped.
6. Promote only compact metadata to committed records in a later source-lock stage.

The plan covers archive zips, Fandom/wiki pages, forum targets, Pastebin data, Google manual exports, Dropbox manual exports, GitHub repositories, GPPrimeView/DWH tooling, OutGuess/PGP/Gematria tool provenance, visual/red-marker/cuneiform/page-image sources, and negative/retired ideas.

Source-locking precedes experiments because many candidate leads are screenshot-based, post-hoc, alphabet-order dependent, or sensitive to source revisions. The harvester records provenance and blockers; it does not infer hidden messages or select experiments.
