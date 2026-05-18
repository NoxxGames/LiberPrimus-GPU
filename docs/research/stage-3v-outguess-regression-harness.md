# Stage 3V Research Note: OutGuess Regression Harness

OutGuess is historically relevant to Cicada 3301, but Stage 3V treats it as regression tooling only.

The committed manifest contains synthetic controls and historical known-positive placeholders. Historical placeholders remain `missing` until exact public artefacts are source-locked locally. A non-empty extraction is not interpreted unless an expected payload hash is known and matches.

The local run found no OutGuess binary, so enabled cases were skipped as `skipped_tool_missing`. This is an accepted Stage 3V result because the harness, schemas, manifests, documentation, and tests now preserve the workflow without requiring raw assets or system tools in CI.
