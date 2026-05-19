# OutGuess Regression Harness

Stage 3V adds deterministic OutGuess regression scaffolding for historical Cicada steganography controls.

The harness detects an `outguess` executable, validates explicit manifest cases, runs only manifest-listed artefacts, records payload hashes, and treats missing tools or assets as explicit skipped outcomes when allowed.

It does not scan all Liber Primus images, run other stego tools, infer hidden meaning from payloads, or make solve claims.

Stage 4F adds fixture source-lock metadata for future OutGuess/audio work. These records identify candidate public paths and toolchain requirements only; they do not provide local assets, execute OutGuess, run OpenPuff/MP3Stego, or interpret payloads.

## Paths

- Artefact metadata: `data/observations/stego/outguess-artifacts-v0.yaml`
- Source-lock metadata: `data/locks/third-party/outguess-regression/`
- Manifest: `experiments/manifests/stego/outguess-regression-v1.yaml`
- Generated outputs: `experiments/results/stego/outguess/stage3v/`
- Optional local artefacts: `third_party/CicadaArchive/`, `third_party/CicadaOutGuess/`
- Stage 4F OutGuess fixture metadata: `data/observations/stego/stage4f-outguess-fixture-source-records.yaml`
- Stage 4F audio fixture metadata: `data/observations/stego/stage4f-audio-fixture-source-records.yaml`
- Stage 4F disabled manifests: `experiments/manifests/stego/stage4f-disabled/`

Raw artefacts and extracted payloads are ignored and must not be committed.
