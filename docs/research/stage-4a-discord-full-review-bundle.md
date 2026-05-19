# Stage 4A Discord Full Review Bundle

Stage 4A converts local ignored Discord HTML exports into a redacted, static, Deep-Research-friendly
review bundle.

## Scope

The stage creates:

- redacted chronological JSONL streams per channel;
- ordered channel shards;
- topic shards and index records;
- public link, image, attachment, method, numeric, visual, and debunk indexes;
- a Liber Primus page-image gallery from local ignored page images;
- an SFTP-ready static site under `experiments/results/discord-full-review/stage4a/site/`;
- aggregate committed summaries only.

It does not scrape Discord, call the Discord API, run OCR, run AI summarisation, execute extracted
methods, activate canonical corpus records, finalize page boundaries, use CUDA, or claim a solve.

## Privacy

Stage 4A defaults to `redacted_public`. Generated review material must not expose raw usernames,
user IDs, message IDs, private Discord CDN URLs, raw HTML, or private attachments. Generated site
files and copied/derived images are ignored outputs.

## Result

The generated bundle is a review and Deep Research handoff aid. It is not source truth by itself.
Any lead found through the bundle still needs source-locking, exact public references, and normal
project promotion rules before it can affect experiment manifests or method status.
