# Cipher Catalog

## Purpose

This catalog records planned transform families and the standards required before implementation.

## Current Cipher Status

After Stage 5P, the repository has solved-baseline CPU reference transforms, bounded experiment executors, an OutGuess regression harness, a method-retirement ledger, source-lock/visual-observation intake records, visual annotation task infrastructure, bounded no-fudge numeric verifier audits, metadata-only source-delta records for selected public artefact categories, stego/audio fixture source-lock metadata, a source-backed cookie exact-refresh result, a CPU batch transform API with expanded adapter parity expectations, scorer/calibration records, an observation review lifecycle, allowlisted public source-lock snapshot records, a reviewed observation promotion ledger, metric-only image source-variant/compression preflight records, stego/audio positive-control readiness records, result-store/score-summary unification records, CPU benchmark/parity planning records, CUDA planning/parity scaffold records, CUDA parity harness skeleton records, CUDA build/device detection records, native C++ CPU backend/threading records, a first CUDA kernel contract for `shift_score_kernel`, a synthetic-only CUDA parity implementation of that contract, parity-reporting/device-code-subset metadata for the synthetic kernel, a separate Gematria mod-29 numeric shift-score contract with a synthetic native fixture, Gematria CUDA preparation records, a synthetic numeric Gematria CUDA kernel implementation, Gematria CUDA parity-reporting/preflight metadata, solved-fixture-safe Gematria token-mapping/native parity records, exact solved-fixture-safe Gematria CUDA/native parity records, controlled expansion gate records, exact repeat/result-store preflight records, and compact result-store/score-summary integration records. It does not implement broad cipher search, broad number-sequence search, broad CUDA acceleration, GPU benchmarking, OCR/AI image interpretation, broad stego fishing, stego/audio extraction, broad hash cracking, or solve claims.

Canonical corpus activation remains inactive and page boundaries remain reviewable.

Method-family status and reopening conditions are now tracked in `data/research/method-family-status-records-v0.yaml` and `data/research/method-retirement-records-v0.yaml`. Noisy or negative families such as Caesar/affine widening, broad Vigenere/dictionary expansion, and cookie SHA-256 broadening must not be expanded without the recorded source-evidence conditions.

Stage 4B visual observations for cuneiform/base-60, mirrored three-dot delimiters, dot/binary ambiguity, number squares, and cookie/hash artefacts are review-only. Stage 4C creates annotation tasks and blank coordinate templates for the visual subset. They are not cipher modules and are not experiment seeds until a later review/promotion stage accepts exact coordinates, alternate readings, controls, and explicit seed status.

Stage 4D bounded numeric verifier work is not a cipher transform. It audits exact numeric inputs only when source-backed and bounded, records skipped/deferred states when evidence is missing, and prohibits nearest-prime, +/-n, row/column arithmetic, fuzzy matching, and route expansion.

Stage 4E source-delta audit work is not a cipher transform and not image/stego analysis. It records selected repository path metadata and future source-lock backlog items only. JPEG-like compression artefact observations and source variants are future-preflight records, not evidence or seeds.

Stage 4F historical OutGuess/audio fixture source-locking is not a cipher transform and not a stego/audio analysis stage. It records fixture provenance, source health, and toolchain requirements only. OutGuess, OpenPuff, MP3Stego, hexdump/strings, and audio rendering remain deferred until a later explicit execution stage with assets, tools, controls, and output policy.

Stage 4G cookie exact-candidate refresh is not a cipher transform and not a hash-cracking campaign. It tests only source-backed Stage 4B strings against historical cookie artefacts with SHA-256 exact matching, finds zero exact matches, and keeps cookie SHA-256 packs negative/deprioritised unless new exact source strings are source-locked.

Stage 4H CPU batch transform API is not a new cipher family. It packages existing CPU transform semantics into deterministic batch records and a future CUDA parity contract. New adapters must preserve existing transform behavior and include synthetic batch tests with output hash expectations.

Stage 4I scorer consolidation is not a cipher transform. It records scorer inventories, confidence labels, compatibility mappings, calibration profiles, and CPU batch score-summary compatibility. Scoring is triage only and cannot imply solved plaintext.

Stage 4J observation review workflow is not a cipher transform. It adds review states, promotion gates, quarantine records, negative-control policy, and path-sanitisation checks so visual, numeric, source, cookie, stego/audio, and Discord-derived observations cannot silently become experiment seeds.

Stage 4K public source-lock snapshot work is not a cipher transform. It locks allowlisted source
metadata, GitHub commit-addressed references, fetch hashes, and copyright notes so future claims can
cite reproducible public-source records without mirroring raw artefacts or treating sources as
canonical truth.

Stage 4L reviewed observation promotion work is not a cipher transform. It records which reviewed
observations are source references, controls, blocked, deferred, quarantined, rejected, or future
manifest-ready while executing nothing.

Stage 4M image source-variant and compression preflight is not a cipher transform and not hidden-message extraction. It records image metadata, source-variant readiness, deterministic compression metrics, review-only artefact candidates, and blocked bigram/Fibonacci-421 readiness without promoting visual or numeric-pattern observations to seeds.

Stage 4N OutGuess/audio positive-control completion is not a cipher transform and not stego/audio extraction. It records readiness, fixture-cache, expected-output, toolchain, and synthetic-control metadata while keeping historical cases blocked until assets, expected outputs, and tools are ready.

Stage 4O CPU batch adapter expansion is not a new cipher family. It records solved-fixture-safe streams, adapter coverage, deterministic parity expectations, and score-summary compatibility for existing CPU transform families only. Missing adapters are deferred with reasons instead of changing semantics to fit the batch API.

Stage 4P result-store and score-summary unification is not a cipher transform. It records source inventory, unified result records, Stage 4I-compatible score views, method-status joins, and a cross-stage report for comparability only. It does not add scorer semantics, reinterpret noisy results, execute experiments, or publish generated result bodies.

Stage 5C CUDA build and device detection is not a cipher transform. It records no-GPU-safe build profiles, toolchain detection, optional device metadata, and smoke-build status only. It does not add CUDA kernels, execute CUDA transforms, run GPU benchmarks, claim speedups, require the local 16GB profile, expand the website, or create solve evidence.

Stage 5D native C++ CPU backend work is not a new cipher family. It implements a deterministic CPU execution baseline over a synthetic fixture, records threading parity and native/Python parity hashes, keeps Python as orchestration, and does not add CUDA kernels, change transform semantics, run broad experiments, or create solve evidence.

Stage 5E first CUDA kernel contract work is not a new cipher family. It selects the future
`shift_score_kernel` contract for the existing `caesar_mod29` transform family, maps the native
synthetic shift parity adapter, and keeps CUDA implementation, GPU benchmarking, broad execution,
and solve claims deferred.

Stage 5F first synthetic-only CUDA parity work is still not a new cipher family. It implements only
the selected `shift_score_kernel` target for the Stage 5D uppercase Latin synthetic shift fixture.
It is not production Gematria mod-29 CUDA, does not run real Liber Primus data, and cannot be cited
as speedup or solve evidence.

Stage 5G reports the Stage 5F hash match and hardens the CUDA-facing source boundary. It still does
not create a new cipher family, production Gematria mod-29 CUDA behavior, or solved-fixture CUDA
execution permission.

Stage 5H Gematria mod-29 shift-score contract work is not a new cipher family. It defines the
future token-domain contract for the existing shift/caesar family: numeric rune tokens `0..28`,
`(token + shift) % 29`, candidate-index ordering, and preserved separators. It prepares synthetic
native fixture metadata only and does not execute CUDA, solve fixtures, unsolved pages, or broad
searches.

Stage 5I Gematria CUDA preparation work is not a new cipher family and not a kernel implementation.
It translates the Stage 5H contract into a CUDA-C ABI plan, raw numeric token buffers,
transformable masks, validation vectors, and a Stage 5J checklist for the future
`gematria_mod29_shift_score_kernel`. It adds no CUDA source and still does not execute CUDA, solve
fixtures, unsolved pages, or broad searches.

Stage 5J Gematria CUDA kernel work is still not a new cipher family. It implements only the
synthetic numeric `gematria_mod29_shift_score_kernel` for the Stage 5H fixture, matches the native
hash, and keeps production Gematria mod-29 CUDA, solved fixtures, unsolved pages, broad searches,
benchmarks, speedup claims, and solve claims blocked.

Stage 5K Gematria CUDA parity reporting work is still not a new cipher family and not a CUDA
execution stage. It records the Stage 5J hash match, audits device-code subset compliance, records
solved-fixture-safe blockers, and keeps token mapping, score-summary parity, solved fixtures,
unsolved pages, benchmarks, speedup claims, and solve claims blocked.

Stage 5L solved-fixture Gematria token mapping work is still not a new cipher family and not a CUDA
execution stage. It maps committed safe streams into numeric token buffers, prepares native
output-token hashes, records score-summary shape constraints, and keeps solved-fixture CUDA
execution blocked pending explicit future-stage approval.

Stage 5M solved-fixture Gematria CUDA parity work is still not a new cipher family and not a broad
CUDA stage. It runs only the existing `gematria_mod29_shift_score_kernel` over the exact Stage 5L
mapped token buffers, records CUDA/native hash parity, adds no new kernel, changes no device
arithmetic, runs no unsolved data, and makes no benchmark, speedup, page-boundary, corpus, or solve
claim.

Stage 5N solved-fixture Gematria CUDA reporting is not a new cipher family and not CUDA execution.
It reports Stage 5M parity, records controlled expansion gates, keeps unsolved-page CUDA blocked,
and makes no benchmark, speedup, page-boundary, corpus, or solve claim.

Stage 5O solved-fixture Gematria CUDA repeat verification is still not a new cipher family.
It repeats only the exact Stage 5M buffer set, compares repeat hashes to Stage 5L and Stage 5M,
records result-store preflight metadata, and keeps broad solved-fixture and unsolved-page CUDA
blocked.

Stage 5P controlled CUDA result-store integration is still not a new cipher family. It records
compact Stage 5O parity hashes in Stage 4P/Stage 4I-compatible surfaces, blocks generated-body
publication, and forbids method-status upgrades by parity alone.

## Historical Stage 0A status

No real cipher modules are implemented in Stage 0A. Placeholder modules return smoke statuses only.

Stage 0B legacy workbook ingestion does not implement real cipher modules. It only extracts non-canonical hint records.

Stage 0C local Pastebin ingestion does not implement cipher modules. It only validates legacy rune/prime-value serialization.

Stage 0D transcript alignment does not implement cipher modules. It prepares corpus views and alignment hints for future transforms only.

## Future transform registry

Later stages should register transforms with stable IDs, CPU reference behavior, parameters, inverse behavior when available, and test vectors.

## Direct translation

Direct rune-to-symbol translation must wait for a frozen Gematria profile and transcript policy.

The workbook can support future tests for direct translation, reverse Gematria, and rotated reverse Gematria. These modules remain unimplemented unless added in a later stage.

## Mod-29 Caesar

A mod-29 Caesar transform will need explicit alphabet order, wrap rules, and known controls.

## Atbash

Atbash variants must define alphabet order and whether digits, spaces, and punctuation are in scope.

## Affine mod 29

Affine transforms must validate invertibility and define parameter enumeration policy.

## Repeating-key Vigenere

Repeating-key transforms require key-source policy, length limits, and null controls.

The legacy workbook supports future tests for Vigenere `DIVINITY` and `FIRFUMFERENFE`, but these modules are not implemented by Stage 0B.

## Prime / phi-prime stream

Prime-derived streams must define sequence generation, indexing, offset, modulus, and reproducible fixtures.

Prime values from the local Pastebin source must be converted to decimal indices before any future modulo-29 cipher operation.

Transcript alignment records may contain decimal-index views for comparison, but cipher transforms must still wait for a frozen Gematria profile and canonical transcript policy.

Public docs must not describe planned or placeholder cipher modules as implemented solver functionality.

The workbook supports future tests for a prime-minus-one stream, including p56 hint checks. This is not a canonical corpus claim.

## Prime-gap stream

Prime-gap transforms must define gap source, indexing, modulus, and expected controls.

## Length-derived streams

Length-derived streams must document which text length and normalization rules feed the stream.

## Simple transpositions

Transpositions must define grid shape, padding, direction, and incomplete-row policy.

## Composition engine

Composed transforms need manifest serialization and full replay. A flexible engine without controls is a false-positive risk.

## Do-not-start-with list

Do not start with brute force, page-specific hacks, GPU-only transforms, or transforms whose CPU reference cannot be tested.

## Stage 0D-followup reminder

Transcript alignment prepares corpus views for future transform work, but it does not implement cipher modules. Prime values from legacy sources must still be converted to decimal indices before any modulo-29 transform. Public docs must not describe planned transform families as implemented.

## Stage 0E profile reminder

Future cipher modules must use Gematria profile v0 for rune/index/prime mapping. Stage 0E does not implement any cipher module.

## Stage 1A direct-translation baseline

Stage 1A implemented a direct-translation reproduction baseline for solved fixtures only. It maps rune tokens to Gematria profile preferred Latin labels. Later stages added Atbash-family, explicit-key Vigenere, and prime-minus-one solved-baseline transforms; generic search remains unimplemented.

## Stage 1B Atbash-family baselines

Stage 1B implements CPU-only known-solved fixture reproduction for `reverse_gematria` and `rotated_reverse_gematria`.

- `reverse_gematria`: implemented for fixtures as `decoded_index = 28 - cipher_index`.
- `rotated_reverse_gematria`: implemented for fixtures as `decoded_index = (28 - cipher_index + rotation) mod 29`.
- Rotations are explicit fixture parameters. No rotation search is implemented.
- Reverse Gematria is affine over `Z_29` with `a=-1, b=28`.
- Rotated reverse Gematria is affine over `Z_29` with `a=-1, b=28+rotation`.

Vigenere, prime-minus-one, generic affine search, scoring, and CUDA acceleration remain unimplemented.

## Stage 1C Explicit-Key Vigenere Baselines

Stage 1C implements CPU-only known-solved fixture reproduction for `vigenere_explicit_key`.

- Formula: `decoded_index = (cipher_index - key_index[key_position]) mod 29`.
- Keys are explicit fixture parameters, not inferred.
- Key position advances only on enciphered rune tokens.
- Cleartext-F pass-through rules are declared per fixture and recorded in reproduction output.
- No key search, scoring, CUDA, prime-stream, or generic Vigenere search is implemented.

## Stage 1D Prime-Minus-One / Phi-Prime Baseline

Stage 1D implements `prime_minus_one_stream` only as a known-solved p56 fixture transform.

- Formula: `decoded_index = (cipher_index - ((prime_i - 1) mod 29)) mod 29`.
- Alias: `phi_prime_stream`, because `phi(p)=p-1` for prime inputs.
- Stream position advances only on enciphered rune tokens.
- Payload tokens are preserved and checked separately.
- No generic prime-stream search, offset sweep, scoring, or CUDA acceleration is implemented. Stage 2A later registered this as a CPU reference solved-baseline transform.

Generic broad affine/shift/search infrastructure remains unimplemented. Stage 3A adds one bounded CPU Caesar plus affine mod-29 enumerator for the policy-approved `841` candidate queue item only. Stage 3B adds a bounded reverse/decryption-convention comparison and refined lead scoring for the same candidate-count envelope. Stage 3C adds scoring calibration and queues a tiny explicit-key Vigenere preview. Stage 3D executes that four-key explicit-list preview only. Stage 3E queues larger but still bounded evidence-ranked Vigenere packs and prime-stream previews as dry-run manifests. Stage 3F executes only the LP evidence-key Vigenere pack with 12 manifest-bound keys, two reset modes, and two advance modes. Stage 3G executes only the p56-local prime-minus-one offset sweep with offsets `0..63`, two directions, and two reset modes. Stage 3H executes only a bounded reset/advance ablation with eight base transforms, four reset modes, and two advance modes. Stage 3I executes only the historical motif Vigenere pack with 14 manifest-bound keys, two reset modes, and two advance modes. Stage 3J executes only the finite-sequence Mersenne/perfect-number probe with three stream variants, offsets `0..15`, two directions, and two reset modes. Stage 3K through Stage 3R add archive, web, deterministic image-analysis, Discord source-discovery, image-transform, Discord review-bundle, promotion-audit, negative-control, and disabled-manifest records only. Stage 3S executes only `EXP-3R-003`, the bounded Onion 7 explicit seed pack. Stage 3T executes only `EXP-3R-004`, the bounded GP/rune claim verifier. Stage 3U executes only `EXP-3R-001`, the bounded cookie SHA-256 signed-variant pack. Stage 3V adds an OutGuess regression harness only. These stages do not implement broad key search, broad number-sequence search, image-derived cipher execution, broad stego fishing, broad claim fishing, dictionary hash cracking, or Discord raw-log processing.

## Stage 3J Mersenne / Perfect-Number Bounded Probe

Stage 3J adds a bounded queue executor for `mersenne_prime_stream_tiny` only.

- `mersenne_mod29`: `(2^p - 1) mod 29`
- `mersenne_minus_one_mod29`: `(2^p - 2) mod 29`
- `perfect_number_mod29`: `2^(p - 1) * (2^p - 1) mod 29`

The exponent sequence is the committed finite list `2, 3, 5, 7, 13, 17, 19, 31` and is treated cyclically. This is not a generic number-sequence framework, does not import external exponent lists, and does not enable CUDA.

## Stage 2A CPU Reference Transform Registry

Stage 2A registers the implemented known-solved baseline transforms as CPU reference transforms only:

- `direct_translation`
- `reverse_gematria`
- `rotated_reverse_gematria`
- `vigenere_explicit_key`
- `prime_minus_one_stream`
- `phi_prime_stream` as an alias of `prime_minus_one_stream`

Every registry entry has `supports_gpu=false`, `search_enabled=false`, and `scoring_enabled=false`. The registry is used by solved-baseline manifests and does not implement broad affine/shift search, Vigenere key search, prime-stream search, CUDA acceleration, or unsolved-page campaign execution. Stage 3A through Stage 3J minimal triage scoring, calibration, explicit-list Vigenere execution, bounded p56-local prime offset execution, reset/advance ablation, and the Mersenne/perfect-number tiny probe exist outside the registry for bounded CPU queue items only. Stage 3E backlog and queue records are planning metadata with deterministic candidate counts and executor-support classification, not new registry cipher implementations.

## Visual And Archive Observations

Stage 3K registry records are not cipher transforms. Cuneiform/base-60 candidates, binary-dot observations, prime-dimension examples, and cookie/hash artefacts are reviewable observations only.

Stage 3L hash-preimage packs are not cipher transforms. They are bounded SHA-256 exact-match tests for archived cookie/hash artefacts and do not imply plaintext recovery or solve evidence.

Stage 3M deterministic image-analysis records are not cipher transforms. Visual feature flags are review aids only and do not imply plaintext recovery, seed validity, or solve evidence.

Stage 3N Discord ingestion records are not cipher transforms. Extracted Discord links and claims are source-discovery leads only and do not imply source truth, seed validity, plaintext recovery, or solve evidence.

Stage 3O promoted Discord records are still not cipher transforms. They are redacted, public-source review leads and must not be treated as experiment seeds, facts, or solve evidence without later independent source-lock review.

Stage 3P deterministic image transform records are not cipher transforms. Derived images, contact sheets, split/mirror differences, bitplanes, component overlays, and visual transform candidate flags are review aids only and do not imply plaintext recovery, seed validity, or solve evidence.

Stage 3Q Discord review bundles are not cipher transforms. Redacted topic shards and review leads are local review aids only and do not imply source truth, seed validity, plaintext recovery, or solve evidence.

Stage 3R Discord lead promotion records and post-Discord manifests are not cipher transforms. Promoted records are corroboration and review scaffolding, negative controls are false-positive controls, and the three post-Discord manifests remain disabled until a later bounded execution stage explicitly runs one.

Stage 3S Onion 7 seed-pack execution is not a general number-theory transform. It runs one manifest-bound stream-subtract pack over reviewed raw and derived Onion 7 table value spaces, with fixed routes, directions, and reset modes. Raw table values and derived values remain separated, the top result is inconclusive, and no solve claim is made.

Stage 3T GP/rune claim verification is not a cipher transform. It recomputes exact count, GP-sum, residue, prime-status, and derived-value claims only when exact spans or explicit values are available. It does not search neighbouring spans, infer boundaries, activate canonical corpus, or claim a solve.

Stage 3U cookie signed-variant execution is not a cipher transform or hash-cracking campaign. It tests a manifest-declared set of signed/public UTF-8 byte strings with SHA-256 exact matching only. Zero exact matches were found, and no solve claim is made.

Stage 3V OutGuess regression is not a cipher transform. It detects/wraps OutGuess for explicit known-positive, known-negative, and synthetic regression cases only. Missing tools/assets are recorded as skipped, and non-empty payloads are not interpreted without expected-hash validation.

Do not convert visual or web observations into transform seeds without a later manifest, count validation, controls, and explicit bounded execution policy.

## Scoring Is Not A Cipher Transform

Stage 4I scorer consolidation is not a cipher transform and not a solve mechanism. The minimal triage scorer, Stage 3C calibration classifier, crib checks, confidence-label records, and CPU batch score summaries are review-prioritisation infrastructure only.

No score label can mean solved or plaintext verified. New scorers require committed scorer records, compatibility mapping, tests, calibration notes, and CPU batch compatibility checks before use.

## Stage 2B Result Store Relationship

Stage 2B does not add cipher behavior. It imports solved-baseline manifest-run outputs into JSONL and SQLite result stores with provenance and false search/CUDA/scoring flags.

The result store is infrastructure for future experiment accounting. It does not implement broad affine/shift search, Vigenere key search, prime-stream search, CUDA acceleration, or unsolved-page campaign execution.
# Stage 4Q Benchmark Planning Note

Stage 4Q does not add cipher families or transform semantics. It records CPU benchmark planning and future CUDA parity readiness for existing CPU transform-adapter families only.

# Stage 5A CUDA Planning Note

Stage 5A does not add cipher families, transform semantics, CUDA kernels, or GPU benchmark behavior. It records future CUDA target boundaries for existing CPU transform-adapter families only.

Readiness records are not solve evidence. Cookie/hash, stego/audio, image/compression, and bigram records are non-CUDA transform targets unless a later explicit stage changes that boundary.

# Stage 5B CUDA Parity Harness Note

Stage 5B does not add cipher families, transform semantics, CUDA kernels, CUDA source changes, or GPU benchmark behavior. It records future CUDA harness, fixture, backend capability, and kernel-matrix boundaries for existing CPU transform-adapter families only.

Harness records are not solve evidence, implementation approval, or performance evidence. Future CUDA kernels must still be introduced by explicit implementation stages with CPU/GPU parity tests.
