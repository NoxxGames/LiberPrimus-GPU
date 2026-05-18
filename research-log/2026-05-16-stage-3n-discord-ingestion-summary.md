# Stage 3N Discord Ingestion Summary

Date: 2026-05-16

## Scope

Stage 3N ingested admin-provided local Discord HTML exports as a privacy-preserving
source-discovery layer. It did not scrape Discord, call live APIs, use self-bots, upload logs to
AI services, execute extracted methods, use CUDA, activate the canonical corpus, finalize page
boundaries, or claim a solve.

## Local Run

- HTML files scanned: 42
- Total bytes scanned: 465845099
- Extracted links: 386511
- Unique domains: 2224
- Attachment candidates: 38647
- Method-claim candidates: 48107
- Numeric-observation candidates: 67660
- Known-bogus/debunked or tried-and-failed claim candidates: 7324
- Hash-like candidate count: 900
- Warnings: 2

Warnings were limited to high-volume files reaching the configured interesting-fragment limit.

## Output Policy

Generated outputs remain ignored under:

```text
experiments/results/discord-ingestion/stage3n/
```

Committed aggregate records:

```text
data/locks/third-party/discord-chats/discord-archive-summary-v0.yaml
data/observations/discord/discord-ingestion-aggregate-summary-v0.yaml
```

Raw Discord HTML logs, message bodies, usernames, user IDs, avatars, private attachment URLs, and
the local review index are not committed.

## Result

The ingestion run succeeded as source discovery only. Discord claims remain reviewable leads, not
facts or experiment seeds. No solve claim is made.
