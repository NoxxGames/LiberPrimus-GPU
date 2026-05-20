# Architecture

## Design Principles

The workbench favors reproducibility, provenance, and skeptical review over speed. Generated output is review material, not evidence of a solve. GPU acceleration is useful only after CPU behavior is correct, testable, and stable.

## Current Repository State

Stage 5D is complete after the Stage 3W through Stage 5C infrastructure chain. The canonical corpus is inactive, page boundaries are reviewable, broad unsolved-page campaigns are not started, and CUDA implementation is deferred beyond build/device-detection and native CPU threading scaffolding. No solve claim is made.

Historical Stage 0A was a bootstrap scaffold. The current repository now includes profile/corpus candidate foundations, solved fixtures, CPU transform registry, result-store foundations, bounded execution policy, archive/image/Discord/post-Discord/stego modules, and raw-data-free CI.

## Component Graph

```mermaid
flowchart LR
    Manifest["Experiment manifest"] --> Corpus["Corpus locks, profiles, and slices"]
    Manifest --> Transforms["CPU reference transforms"]
    Transforms --> Scorers["Scorers and null controls"]
    Scorers --> Results["Ignored JSONL / SQLite result stores"]
    Corpus --> Registries["Source and observation registries"]
    Registries --> Manifests["Bounded manifest queues"]
    Transforms -. future optional batches .-> CUDA["CUDA transform-score kernels"]
    CUDA -. parity tests .-> Scorers
```

## CPU/GPU Responsibility Split

The CPU owns corpus management, profile loading, hypothesis generation, bounded experiment orchestration, provenance, scoring, validation, and review. The GPU may later accelerate large regular transform-and-score batches only after CPU references, batch APIs, parity tests, and benchmarks exist.

Existing CUDA code is scaffold and smoke-test infrastructure unless a future stage explicitly adds a CPU-parity-tested kernel. Stage 5D adds a native C++ CPU execution plane for deterministic synthetic batch parity; Python remains orchestration and policy validation.

## Corpus And Profile Layer

Gematria, separator, and glyph-variant profiles are committed and locked. Corpus candidates and page-boundary records remain non-canonical until a future corpus activation stage. Raw source material remains immutable and ignored unless explicitly promoted through source-lock metadata.

## Transform And Experiment Layer

Solved-baseline transforms are CPU reference implementations registered for manifest-addressable replay. Bounded exploratory and post-Discord stages add manifest-scoped executors only; they do not start broad search campaigns.

## Scoring Layer

Stage 3C introduced calibrated scoring for bounded review candidates. The scorer is used to sort and label bounded outputs, not to claim solves. Null controls, positive controls, and conservative confidence labels remain required for any future scored campaign.

## Result Sink

JSONL and SQLite result stores exist as generated outputs. They are ignored by Git and must not be committed. Committed records are limited to schemas, manifests, source locks, curated observation metadata, aggregate summaries, tests, docs, and summary research logs.

## Source And Observation Modules

Stage 3K through Stage 3V added source/visual/web observations, image metadata and transforms, Discord ingestion/review/promotion, post-Discord bounded executors, and OutGuess regression harness metadata. These modules preserve provenance and review status. They do not activate a canonical corpus, finalize page boundaries, publish raw logs/images, or claim solves.

## Testing Layer

CI is raw-data-free, no-GPU-safe, secret-free, and does not upload generated artefacts by default. Tests cover schema validation, manifest safety, bounded executor behavior, fake-tool stego behavior, ignored-output policy, documentation status, Stage 3W anti-drift checks, Stage 4Q benchmark-planning validation, Stage 5A CUDA planning validation, Stage 5B CUDA parity harness validation, Stage 5C CUDA build/device detection validation, and Stage 5D native CPU backend/threading validation.

## Failure Modes

Primary risks are false positives, stale context, transcript drift, silent rune-table changes, generated outputs treated as evidence, raw/private data leakage, and GPU code diverging from CPU references. Stage 3W adds anti-drift checks to catch stale operational docs before contributors or Codex sessions act on obsolete assumptions.
