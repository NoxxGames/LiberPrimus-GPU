# Promotion Blocker Taxonomy

Stage 4L blocker records make non-promotion explicit.

Common blockers:

- `needs_coordinates`: visual page/region evidence is incomplete.
- `needs_source_lock`: source metadata is not strong enough.
- `needs_human_review`: automated checks cannot accept meaning.
- `ambiguous_reading`: dot/cuneiform ordering, polarity, or reading is unforced.
- `missing_expected_output`: stego/audio regression lacks expected output hash.
- `toolchain_unavailable`: required toolchain is not available.
- `negative_result`: prior exact bounded result was negative.
- `quarantined_false_positive`: known false-positive class.
- `rejected`: reviewed and rejected.
- `deferred`: valid future branch, not ready.

Blockers are useful state. They prevent accidental execution and identify the
specific evidence required before a future stage can proceed.
