# Audio Fixture Source-Locking

Stage 4F records audio fixture metadata for later deterministic regression preparation.

Stage 4N consumes these source records and writes audio readiness, fixture-cache, expected-output,
and toolchain records. It does not download or commit audio artefacts by default and does not run
audio tools.

## Audio Candidates

- `2014/05/3301 - Interconnectedness.mp3`
- `2013/02/761.MP3`
- Public Instar emergence and What Happened 2014 source pages.
- MP3Stego reference tooling metadata.

## Toolchain Requirements

Toolchain records live in `data/observations/stego/stage4f-toolchain-requirements.yaml` and separate:

- `openpuff`
- `mp3stego`
- `hexdump/strings`
- `audio_rendering`
- `outguess`

Stage 4F does not run the tools. It records that future work needs explicit tool availability, source-locked assets, expected-output controls, and ignored generated outputs.
