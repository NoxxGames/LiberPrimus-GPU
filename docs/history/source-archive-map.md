# Source Archive Map

Stage 3K records source/archive references in `data/observations/archive/source-archive-records-v0.yaml`.

The map separates stronger technical references from secondary archives and mutable community pages. These records are source-discovery metadata only. They do not activate the canonical corpus and they do not prove plaintext.

Current classes include:

- `strong_community_technical`: rtkd/iddqd and scream314/cicada3301 style technical references.
- `secondary_archive`: archive mirrors such as The Complete Cicada3301 Archive.
- `archived_claim`: mutable or community-maintained claims that need review before use.

Every record keeps `trusted_as_canonical=false`.

Stage 3N adds separate Discord aggregate records under `data/observations/discord/` and
`data/locks/third-party/discord-chats/`. These are not canonical archive records; they identify
review queues for public links and method claims found in local admin-provided HTML exports.
