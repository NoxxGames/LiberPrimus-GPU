# Stage 4K Allowlisted Source-Lock Snapshots

Stage 4K locks a small public-source subset selected from Stage 4B source records, Stage 4E
`cicada-solvers/iddqd` source-delta records, Stage 4F stego/audio fixture records, and Stage 4J
review decisions.

The stage records metadata only by default:

- source URL and canonical URL;
- retrieval timestamp and HTTP metadata where fetched;
- SHA-256 for fetched ignored-cache content;
- source class and copyright note;
- explicit snapshot policy and lock status;
- GitHub commit-addressed references when possible.

Local run summary:

- Sources considered: `43`.
- Unique allowlisted source-lock records: `15`.
- Sources fetched into ignored cache: `1`.
- GitHub commit-address locks: `8`.
- Metadata-only records: `8`.
- Ignored local snapshot policy records: `7`.
- Committed small text snapshots: `0`.
- Rejected unsafe/noisy or non-priority sources: `22`.
- Duplicate sources: `6`.
- Fetch failures recorded as metadata/failure records: `6`.

Stage 4K does not broad crawl, blind-mirror repositories, commit raw HTML by default, commit
binary/image/audio/font/archive artefacts, execute experiments, activate the canonical corpus, finalize
page boundaries, use CUDA, or make solve claims.
