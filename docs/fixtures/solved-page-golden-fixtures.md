# Solved-Page Golden Fixtures

## Purpose

Solved-page golden fixtures are regression tests for already documented solved material. They are not solve claims.

## Fixture Schema

Fixture manifests use `schemas/corpus/solved-page-fixture-v0.schema.json`.

## Provenance Requirements

Fixtures must record transcript source IDs, solved-reference source IDs, profile IDs, corpus candidate IDs, and fixture versions.

## Source SHA-256 Requirements

Fixtures must include SHA-256 values for the rtkd transcript and solved-reference source used to define expectations.

## Profile SHA-256 Requirements

Fixtures must include SHA-256 values for Gematria, separator grammar, and glyph variant profiles.

## Passing vs Pending Fixtures

Passing-intended fixtures require expected normalized plaintext and its SHA-256. Pending fixtures may omit expected text when reference text or span selection is ambiguous, but must explain why.

## Generated Reproduction Records

Reproduction records are generated under ignored `data/normalized/solved-baselines/` paths and must not be committed.

## Why Fixtures Are Not Solve Claims

A passing fixture only means current tooling reproduces an existing known solved reference under pinned inputs. It does not prove new plaintext or activate canonical corpus status.

## How To Add Future Fixtures

Add a fixture manifest, cite locked sources, include profile hashes, choose an explicit selector, document caveats, and add tests before using it in experiments.
