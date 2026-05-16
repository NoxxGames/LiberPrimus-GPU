# Payload Preservation Policy

## Purpose

Payloads are non-plaintext material embedded in solved fixture spans. They must be preserved and checked separately from decoded text.

## Payload Versus Plaintext

Payload text is not merged into normalized plaintext and must not be treated as rune-derived letters.

## Hex Payload Blocks

Stage 1D supports a hex literal block policy: `preserve_exact_normalized_hex`. The p56 block is extracted as ordered non-empty logical lines and joined with single newlines.

## Payload Tokenization

Payload extraction preserves numeric and unknown-symbol token raw text from declared payload logical-line ranges.

## SHA-256 Checks

Fixture payload checks include expected payload text and SHA-256. Reproduction records include expected hash, actual hash, match status, length, and warnings.

## Advancement Rules

Payload tokens must not advance prime streams, Vigenere keys, or other cipher streams.

## Generated Records

Payload check results are stored in `payload_check_results` on generated reproduction records. These generated outputs remain ignored.

## Failure Modes

Missing selectors or missing extracted payload produce pending payload checks with warnings. Hash mismatches fail the payload check and surface warnings.

## Future Payload Types

Future stages may add payload kinds beyond hex blocks, but they must keep payload provenance, exact preservation policy, and non-canonical flags.
