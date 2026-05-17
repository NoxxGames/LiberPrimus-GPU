# Stage 3L Cookie Hash Preimage Packs

Stage 3L adds a bounded SHA-256-only preimage test for the archived 2013 cookie/hash artefacts recorded in Stage 3K.

Initial state:

- Branch: `main`
- Local HEAD: `8fe9dfe079eb8c652b2843e987f44f500da92989`
- Origin remote: `https://github.com/NoxxGames/LiberPrimus-GPU.git`
- Local equals `origin/main`: true
- Latest known CI: success, run `26001758425`
- Cookie records: 2, both `hex64`
- Operator policy: present
- Generated outputs staged: 0
- Raw files staged: 0
- Raw images staged: 0
- Root research reports staged: 0

Scope:

- SHA-256 exact matching only.
- Explicit literal and numeric/base29 packs only.
- No external dictionaries, no fuzzy matching, no GPU/hashcat, no live Tor, and no solve claim.

Implementation plan:

- Add hash-preimage schemas and explicit candidate packs.
- Add `libreprimus.hash_preimage` loader, byte-variant, base29, runner, export, summary, and validation modules.
- Add `libreprimus hash-preimage` CLI commands.
- Run the local bounded packs and commit only summary research logs and source artefacts.

Implementation status:

- Output directory and ignore policy: complete.
- Schemas: 4 added.
- Candidate packs: literal pack and base29/numeric pack added.
- Literal pack count: generated `288`, deduplicated to `249`.
- Numeric pack count: generated `1680`, deduplicated to `1560`.
- Total generated before dedup: `1968`.
- Total candidates after dedup: `1809`.
- Total target comparisons: `3618`.
- Exact SHA-256 matches: `0`.
- Generated outputs: ignored under `experiments/results/hash-preimage/stage3l/`.
- Solve claim: false.
