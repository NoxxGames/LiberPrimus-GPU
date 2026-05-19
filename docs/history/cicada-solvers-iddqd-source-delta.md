# Cicada Solvers iddqd Source Delta

Stage 4E inspects the public `cicada-solvers/iddqd` repository as a source-lock delta target. It records tree metadata and path categories only; it does not mirror the repository, process artefacts, or commit raw files.

Stage 4K later locks selected `cicada-solvers/iddqd` references as commit-addressed public-source
metadata. The source-delta tree remains metadata-only; image, audio, font, archive, and payload files
are not committed.

## Scope

The audit target is:

- `https://github.com/cicada-solvers/iddqd.git`
- Remote HEAD recorded during Stage 4E: `0e3789ad2949c62ea7fb9e3e00ded93df3b3ce07`
- Tree paths observed: 310

The selected categories include LP full images, LP unsolved images, `lp_outguessed`, historical puzzle artefacts, audio fixture candidates, image fixture candidates, transcription, translation, key, byte-string, and font metadata-only paths.

## Records

Committed Stage 4E records:

- `data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml`
- `data/locks/third-party/stage4e-cicada-solvers-iddqd-source-health.yaml`
- `data/observations/visual/stage4e-image-compression-artifact-observations.yaml`
- `experiments/manifests/stage4e-disabled/`

Generated diagnostics are under ignored `experiments/results/source-delta/stage4e/`.

## Boundary

Stage 4E is metadata-only. It does not download or commit images, audio, fonts, archives, OutGuess payloads, or extracted artefacts. The audit preserves `trusted_as_canonical=false` and `solve_claim=false` for every committed record.

## Stage 4F Follow-Up

Stage 4F uses selected Stage 4E categories as fixture provenance inputs for historical OutGuess/audio source-locking. It records `lp_outguessed`, Interconnectedness MP3, `4gq25.jpg`, 2013/02 asset, promoted OutGuess/OpenPuff/Instar source-page, and toolchain requirement metadata without downloading or committing raw artefacts.

Stage 4F outputs:

- `data/observations/stego/stage4f-outguess-fixture-source-records.yaml`
- `data/observations/stego/stage4f-audio-fixture-source-records.yaml`
- `data/locks/third-party/stage4f-stego-fixture-source-health.yaml`
- `data/observations/stego/stage4f-toolchain-requirements.yaml`
- `experiments/manifests/stego/stage4f-disabled/`

Generated diagnostics remain ignored under `experiments/results/stego-fixtures/stage4f/`.

`lp_outguessed` is queued for future fixture source-locking. LP image categories are queued for later source-variant comparison. Font paths are metadata-only and must not be committed or redistributed.
