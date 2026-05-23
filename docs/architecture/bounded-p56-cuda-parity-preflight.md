# Bounded p56 CUDA Parity Preflight

Stage 5AC preflights only the bounded p56 vector `stage5z-validation-p56-bounded-v0` for a future explicit Stage 5AD parity run.

The preflight is ready only because:

- Stage 5AA synthetic CUDA parity passed.
- The expected and computed synthetic hash match.
- Stage 5AB doc-staleness checks are clean.
- The bounded p56 mapping already has a source-backed expected hash.

The future scope is exactly:

- mapping: `stage5w-mapping-p56-stage4o-bounded-v0`
- fixture: `p56-an-end-prime-minus-one`
- candidate: `stage4o-prime-minus-one-an-v0`
- expected hash: `4a3059f12c0f8450bd4ef7e31bf879fbc104202e5fb0e53b7ba514241f07cd87`

Full p56 remains blocked because the full committed p56 cipher token buffer is missing. Stage 5AC does not run p56 CUDA, full p56 CUDA, unsolved-page CUDA, benchmarks, or scored experiments.
