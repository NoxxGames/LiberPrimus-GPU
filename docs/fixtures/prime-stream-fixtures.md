# Prime-Stream Fixtures

## Purpose

Prime-stream fixtures are known-solved baseline tests for explicit prime-derived transforms. They are not new solve claims.

## Fixture List

- `p56-an-end-prime-minus-one`: p56 `An End`, method `prime_minus_one_stream`, alias `phi_prime_stream`.

## p56 An End

The fixture uses Stage 0E logical lines `1690..1710` and marks the span as `reviewable`.

## Formula

`decoded_index = (cipher_index - ((prime_i - 1) mod 29)) mod 29`

## Phi-Prime Alias

For prime inputs, `phi(p)=p-1`, so `phi_prime_stream` is equivalent to `prime_minus_one_stream`.

## Declared Parameters

- `prime_start_index=0`
- `direction=forward`
- `stream_value=prime_minus_one_mod29`
- `advance_on=enciphered_rune_tokens_only`

## Skip Rules

The fixture declares `cleartext_f_pass_through` for rune index `0` and explicit token index `22202`. The skip does not advance the stream.

## Payload Checks

Payload `p56-hex-block` is extracted from logical lines `1697..1705` and checked with SHA-256 `45622e92614e822640345088530b674d0ec2c1cb3a6887271ed9734c5ef00885`.

## Expected Text And Hashes

Expected normalized plaintext SHA-256: `9a6527f0aece860a7f1ced09ac5265168521da48690a48240b7fb52aa9330693`.

## Reproduction Command

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli solved-fixture reproduce-prime-stream --fixture-dir data/fixtures/solved-pages/prime-stream-v0 --candidate-dir data/normalized/corpus-candidates/rtkd-master-v0-candidate --out-dir data/normalized/solved-baselines/prime-stream-v0 --allow-pending --allow-warnings
```

## Current Status

Prime-stream fixtures: `1` pass, `0` fail, `0` pending, `0` skipped.

## Known Caveats

The corpus candidate and page boundaries remain reviewable. Generated reproduction outputs remain ignored.
