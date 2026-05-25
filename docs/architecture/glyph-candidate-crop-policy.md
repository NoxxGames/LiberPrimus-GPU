# Glyph Candidate Crop Policy

Stage 5AU uses only the Stage 5AR selected original local page images for crop derivation:

- `third_party/LiberPrimusPages/49.jpg`
- `third_party/LiberPrimusPages/50.jpg`
- `third_party/LiberPrimusPages/51.jpg`

The crop algorithm starts from Stage 5AR cell boxes, expands the local region, thresholds dark pixels deterministically, filters tiny connected components, unions components overlapping the review cell, and pads the resulting box. If no component is suitable, the crop falls back to the Stage 5AR cell and records that fallback.

The generated crop types are `cell_crop`, `cell_crop_x4`, `glyph_candidate_crop`, `glyph_candidate_crop_x8`, `context_small`, `context_medium`, `context_large`, `row_context`, `row_context_overlay`, `page_strip_context`, `page_strip_overlay`, and `debug_overlay`.

All overlays are labelled as derived review overlays and not source truth. The crop policy never classifies glyphs, chooses candidate values, changes the canonical transcription, or creates experiment seeds.
