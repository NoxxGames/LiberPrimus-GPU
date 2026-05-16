# Public Docs Wording Policy

## Purpose

Public README, STATUS, and ROADMAP wording must separate permanent safety rules from temporary implementation boundaries. Deferred future work should not be described as a permanent non-goal unless the project explicitly intends never to implement it.

The root README must not use a top-level `## Non-goals` or `## Non-goals for Stage 0A` heading for temporary boundaries. Use `## Current boundaries and deferred work` instead.

## Required Distinctions

- Permanent safety rules: raw data immutability, no generated outputs as solve evidence, no unreviewed solve claims, and no committed generated result stores.
- Current boundaries: capabilities that are intentionally absent right now, such as inactive canonical corpus, reviewable page boundaries, and no active search, scoring, or CUDA campaigns.
- Deferred future work: staged work that may be implemented later after provenance, manifests, tests, and review gates exist.
- Completed work: infrastructure already delivered in earlier stages.

## Validation

The Stage 2D follow-up README boundary tests reject stale Stage 0A non-goals wording and check that the current public README keeps these categories distinct.

When public rendering appears stale, verify the fetched Git blob first:

```powershell
.\scripts\ci\verify-remote-readme-status.ps1 -Remote origin -Branch main -CheckRawUrl -CheckGitHubApi
```
