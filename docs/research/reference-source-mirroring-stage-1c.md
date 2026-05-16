# Reference Source Mirroring Stage 1C

## Purpose

Stage 1C mirrors small reference files used as provenance for solved-fixture methods.

## Mirrored Files

From `scream314/cicada3301`: `README.md`, `pages_and_ciphers.md`, and `gematria_primus.md`.

From `lipeeeee/gematria`: `README.md`, `LICENSE`, `pyproject.toml`, `requirements.txt`, `lib/gematria.py`, and `hash.py`.

## Lock Metadata

Lock metadata is committed under `data/locks/reference-repos/`. Raw mirrored files remain ignored under `data/raw/reference-repos/`.

## Reference-Only Policy

Mirrored files are method/provenance references only. They are not canonical corpus inputs.

## Raw-File Ignore Policy

Raw mirrored files must not be staged or committed. Only README placeholders and lock metadata are stageable.

## Licence Caution

`lipeeeee/gematria` includes a mirrored `LICENSE` file. Its code is not imported, executed, or copied into production modules.

## No Code-Copy Policy

Stage 1C reimplements explicit-key Vigenere behavior from the local project requirements and tests. It does not copy external implementation code.

## Generated Summaries

Generated reference summaries are written under ignored `data/normalized/reference-summaries/stage-1c/`.

## Next Uses

Future fixture stages can cite the lock metadata, but any new behaviour must still be implemented locally with tests.
