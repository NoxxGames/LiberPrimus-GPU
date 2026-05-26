# Token-Block Preflight Runner Scaffold

Stage 5BB adds a no-execution scaffold for future page 49-51 token-block preflight work. The scaffold is a manifest loader, validator, dry-run preview, counter, fixture-schema, and gate-enforcement layer only.

The active loader path is the Stage 5BB active-manifest registry. Future runner code must not load Stage 5AV or the old Stage 5AY bounded variant-family manifest as active inputs. Those records are available only for explicit historical diagnostics.

Active inputs:

- Stage 5AW repaired branch metadata.
- Stage 5AY branch-eligibility policy and supporting controls.
- Stage 5AZ repaired preflight design, bounded variant-family manifest, branch budget, execution gates, and DWH context.

Blocked behavior:

- Real token-block byte-stream generation.
- Variant branch materialisation.
- Cartesian enumeration or sampling.
- DWH/hash/preimage search or hash comparison.
- Decode attempts, scoring, CUDA, benchmarks, OCR, AI/ML, LLM vision, stego, and solve claims.

The generated Stage 5BB reports under `experiments/results/token-block/stage5bb/` are local review material and remain ignored.
