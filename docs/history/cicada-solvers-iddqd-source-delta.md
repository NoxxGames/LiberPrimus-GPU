# Cicada Solvers iddqd Source Delta

Stage 4E inspects the public `cicada-solvers/iddqd` repository as a source-lock delta target. It records tree metadata and path categories only; it does not mirror the repository, process artefacts, or commit raw files.

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

`lp_outguessed` is queued for future fixture source-locking. LP image categories are queued for later source-variant comparison. Font paths are metadata-only and must not be committed or redistributed.
