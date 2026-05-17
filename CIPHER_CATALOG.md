# Cipher Catalog

## Purpose

This catalog records planned transform families and the standards required before implementation.

## Stage 0A status

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

Generic broad affine/shift/search infrastructure remains unimplemented. Stage 3A adds one bounded CPU Caesar plus affine mod-29 enumerator for the policy-approved `841` candidate queue item only. Stage 3B adds a bounded reverse/decryption-convention comparison and refined lead scoring for the same candidate-count envelope. Stage 3C adds scoring calibration and queues a tiny explicit-key Vigenere preview. Stage 3D executes that four-key explicit-list preview only. Stage 3E queues larger but still bounded evidence-ranked Vigenere packs and prime-stream previews as dry-run manifests; it does not execute them until missing reset/advance and prime-offset executors exist, and it does not implement broad key search.

## Stage 2A CPU Reference Transform Registry

Stage 2A registers the implemented known-solved baseline transforms as CPU reference transforms only:

- `direct_translation`
- `reverse_gematria`
- `rotated_reverse_gematria`
- `vigenere_explicit_key`
- `prime_minus_one_stream`
- `phi_prime_stream` as an alias of `prime_minus_one_stream`

Every registry entry has `supports_gpu=false`, `search_enabled=false`, and `scoring_enabled=false`. The registry is used by solved-baseline manifests and does not implement broad affine/shift search, Vigenere key search, prime-stream search, CUDA acceleration, or unsolved-page campaign execution. Stage 3A through Stage 3D minimal triage scoring, calibration, and explicit-list Vigenere preview execution exist outside the registry for bounded CPU queue items only. Stage 3E backlog and queue records are planning metadata with deterministic candidate counts and executor-support classification, not new cipher implementations.

## Stage 2B Result Store Relationship

Stage 2B does not add cipher behavior. It imports solved-baseline manifest-run outputs into JSONL and SQLite result stores with provenance and false search/CUDA/scoring flags.

The result store is infrastructure for future experiment accounting. It does not implement broad affine/shift search, Vigenere key search, prime-stream search, CUDA acceleration, or unsolved-page campaign execution.
