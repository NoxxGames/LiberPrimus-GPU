# OutGuess Regression Harness

Stage 3V adds deterministic OutGuess regression scaffolding for historical Cicada steganography controls.

The harness detects an `outguess` executable, validates explicit manifest cases, runs only manifest-listed artefacts, records payload hashes, and treats missing tools or assets as explicit skipped outcomes when allowed.

It does not scan all Liber Primus images, run other stego tools, infer hidden meaning from payloads, or make solve claims.

## Paths

- Artefact metadata: `data/observations/stego/outguess-artifacts-v0.yaml`
- Source-lock metadata: `data/locks/third-party/outguess-regression/`
- Manifest: `experiments/manifests/stego/outguess-regression-v1.yaml`
- Generated outputs: `experiments/results/stego/outguess/stage3v/`
- Optional local artefacts: `third_party/CicadaArchive/`, `third_party/CicadaOutGuess/`

Raw artefacts and extracted payloads are ignored and must not be committed.
