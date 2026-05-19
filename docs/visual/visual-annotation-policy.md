# Visual Annotation Policy

Visual annotation records location and review state. It must not infer meaning.

## Evidence Layers

1. Source and image lock metadata identify the artefact.
2. Coordinate annotations identify a region on the artefact.
3. Reading candidates record possible interpretations and alternatives.
4. Experiment seeds require a later explicit promotion step.

Stage 4C implements layers 1-3 only. Stage 4J adds the review workflow that can block,
defer, quarantine, or later allow explicit layer-4 promotion. It does not promote any visual
observation by implication.

## Required Guardrails

- Coordinates and readings are separate.
- `unknown_pending_annotation` must be used when coordinates are missing.
- `needs_human_coordinates` must be used for broad or unannotated tasks.
- Cuneiform, dot, delimiter, braille, and constellation claims must remain review-only until exact geometry and ambiguity are recorded.
- OCR, AI, ML, and generated overlays are not source truth.
- Generated annotation sites, copied images, grid overlays, and filled templates remain ignored unless a later stage explicitly promotes a curated record.
- Stage 4J promotion gates require page/image reference and coordinate or region evidence before visual observations can become seeds.
