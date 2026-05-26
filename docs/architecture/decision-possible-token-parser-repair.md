# Decision Possible-Token Parser Repair

Stage 5AW repairs the Stage 5AV possible-token parser used for reviewer notes in the page 49-51 token-block decision workflow.

The repaired parser reads semicolon-delimited fields, limits `possible_tokens=` to its own field value, splits only that value on `|`, and accepts only two-character token-like options. If a segment begins with a plausible two-character token followed by prose, Stage 5AW extracts the token prefix, records a cleanup warning, and preserves any visual placeholder such as `?4` or `3?` separately.

Stage 5AW does not reinterpret human decisions. It removes prose fragments from the reviewer-extra token set, keeps valid extras such as `1i`, `0j`, `Oj`, and `1I`, and records malformed fragments in `data/token-block/stage5aw-malformed-possible-token-fragments.yaml`.

Visual placeholders remain review metadata only. They are marked `primary60_status: visual_placeholder_unmappable`, `primary60_mappable: false`, and `variant_byte_stream_eligible: false`.

No token experiment, variant byte stream, DWH/hash search, decode attempt, OCR, AI/ML interpretation, LLM/vision reading, semantic image interpretation, hidden-content image forensics, stego execution, CUDA, benchmark, scored experiment, canonical transcription change, or solve claim is part of this repair.
