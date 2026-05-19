# Historical OutGuess And Audio Fixtures

Stage 4F records historical stego/audio fixture metadata for future regression work. It does not download fixture assets, run OutGuess, run OpenPuff, run MP3Stego, render audio, scan strings, or interpret payloads.

## Fixture Record Sets

- `data/observations/stego/stage4f-outguess-fixture-source-records.yaml`
- `data/observations/stego/stage4f-audio-fixture-source-records.yaml`
- `data/locks/third-party/stage4f-stego-fixture-source-health.yaml`
- `data/observations/stego/stage4f-toolchain-requirements.yaml`

## Selected Fixture Categories

- `lp_outguessed/` from `cicada-solvers/iddqd`.
- `2016/01/4gq25.jpg` from `cicada-solvers/iddqd`.
- `2013/02/` historical assets from `cicada-solvers/iddqd`.
- `2014/05/3301 - Interconnectedness.mp3`.
- `2013/02/761.MP3`.
- Stage 4B public source pages for OutGuess, Instar emergence, What Happened 2014, OpenPuff context, and MP3Stego tooling.

All fixture records keep `trusted_as_canonical=false` and `solve_claim=false`.

## Boundary

Fixture candidates are provenance targets only. A later explicit execution stage must source-lock assets, document expected outputs or null controls, verify tool availability, and keep generated outputs ignored before any regression run.
