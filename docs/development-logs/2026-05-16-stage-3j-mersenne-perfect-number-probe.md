# Stage 3J Mersenne / Perfect-Number Probe Developer Log

Date: 2026-05-16

## Scope

Stage 3J implemented the bounded Mersenne/perfect-number tiny stream probe from the Stage 3G backlog.

In scope:

- finite cyclic exponent sequence from queue metadata only;
- three stream variants: `mersenne_mod29`, `mersenne_minus_one_mod29`, `perfect_number_mod29`;
- offsets `0..15`, directions `forward` and `reverse`, reset modes `none` and `line`;
- calibrated Stage 3C triage scoring;
- duplicate stream-signature reporting;
- ignored generated outputs.

Out of scope:

- arbitrary number-sequence search;
- external Mersenne exponent lists;
- visual/image observation registry;
- CUDA;
- canonical corpus activation;
- page-boundary finalization;
- solve claims.

## Implementation Notes

Added `python/libreprimus/bounded_execution/mersenne_stream_probe.py` and `libreprimus bounded-run run-mersenne-stream-probe`.

The executor uses the committed queue exponent sequence `2, 3, 5, 7, 13, 17, 19, 31` as a cyclic stream. Offsets may therefore produce duplicate stream signatures; the executor records `stream_signature_sha256` for every candidate and summary-level unique/duplicate counts.

The Stage 3E backlog item is now marked runnable through the Stage 3J executor. A dedicated `experiments/queues/stage3j-bounded-cpu-queue.yaml` provides the stage-specific run entry.

## Local Run

- Queue item: `stage3j_mersenne_prime_stream_tiny_v1`
- Input slice: `stage3a-page-candidate-018-reviewable-slice`
- Expected candidates: `192`
- Executed candidates: `192`
- Deferred candidates: `0`
- Unique stream signatures: `96`
- Duplicate stream signatures: `96`
- Top variant: `perfect_number_mod29`
- Top offset: `3`
- Top direction: `forward`
- Top reset mode: `none`
- Top score: `1.515716`
- Top calibrated confidence: `inconclusive`

Generated outputs are ignored under `experiments/results/bounded-auto-runs/stage3j/`.

## Safety

No generated candidate dumps are committed. The root Deep Research source file and local research report remain untracked/ignored. No solve claim, CUDA change, canonical corpus activation, or page-boundary finalization is made.
