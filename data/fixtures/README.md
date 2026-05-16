# data/fixtures

## Purpose

Small committed fixtures for parser, profile, corpus, and solved-baseline tests.

## What belongs here

Synthetic non-corpus inputs and curated solved-page fixture manifests that are safe to commit.

## What does not belong here

Raw corpus, generated results, page images, raw transcript dumps, or generated solved-baseline output.

## Stage 1A solved fixtures

Stage 1A direct-translation fixture manifests live under `data/fixtures/solved-pages/direct-translation-v0/`. They are test expectations with source/profile provenance, not solve claims.

## Codex modification policy

Codex may add small synthetic fixtures and reviewed fixture manifests when tests require them. Generated reproduction outputs belong under ignored `data/normalized/` paths.
