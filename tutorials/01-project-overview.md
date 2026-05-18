# Project Overview

## Purpose

`liberprimus-gpu` is a conservative research workbench for Liber Primus cryptanalysis. It keeps
source provenance, solved baselines, bounded CPU experiments, generated-output policy, and CI gates
ahead of broader search or CUDA work.

The durable staged plan lives at `docs/roadmap/staged-plan.md`. Stage 3Y adds result-synthesis
records and a method-retirement ledger so noisy or negative methods are not widened without new
source evidence.

## What It Is Not

It is not a solve claim, raw corpus dump, Discord scraper, live Tor crawler, GPU hash-cracker, or
CUDA campaign. Current exploratory runs are bounded, CPU-only, and review-oriented.

## Prerequisites

- Git
- Python 3.12
- PowerShell on Windows or a POSIX shell on Linux
- Optional CMake/Ninja for C++ smoke builds

## Expected Outputs

Most experiment commands write generated JSON/JSONL under `experiments/results/`. Those outputs are
ignored and should be inspected locally, not committed.

## Do Not Commit

Raw data, generated outputs, SQLite databases, local Discord HTML, raw page images, and root
research reports unless copied into committed docs intentionally.

## Troubleshooting

Run `.\.venv\Scripts\python.exe -m libreprimus.cli smoke` first. Then run the consistency suite
and `libreprimus research-synthesis validate` before assuming a local environment issue is a code
bug.
