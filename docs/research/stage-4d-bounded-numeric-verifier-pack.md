# Stage 4D Research Note: Bounded Numeric Verifier Pack

Stage 4D is a conservative verification stage. It uses Stage 4B and Stage 4C records to determine which numeric claims are ready for bounded audit and which must stay skipped or deferred.

## Inputs

- Stage 4B disabled manifests under `experiments/manifests/stage4b-disabled/`.
- Stage 4B visual observation records.
- Stage 4C cuneiform, delimiter, dot-pattern, and visual negative-control task records.

## Findings

- GP/rune batch002 had no exact new website-derived spans, so the verifier emitted `skipped_no_exact_claims`.
- Delimiter records were audited as metadata only. Orientation and handedness are still `unknown_pending_annotation`.
- Dot ambiguity was audited as a negative-control measurement. Claimed readings are not unique.
- Onion7/raw number-square route verification skipped because raw values remain pending source-lock.
- Visual negative controls produced ambiguity metrics.
- Cuneiform seed execution remains deferred until accepted coordinates/readout exist.
- Cookie pack v2 remains deferred to Stage 4E.

## Boundaries

Stage 4D does not run broad number-theory search, cuneiform seed tests, cookie hash packs, OCR, AI/ML, Discord raw-log processing, CUDA, or image-derived cipher execution.

The no-fudge policy is the main result: missing exact evidence is recorded as a skip/defer state rather than filled in with nearby primes, arithmetic adjustments, or route expansion.
