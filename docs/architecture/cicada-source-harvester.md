# Cicada Source Harvester

Stage 5AF adds `CicadaSourceHarvester`, exposed as `libreprimus source-harvester`. It is a local-first source-lock and provenance tool for Cicada/Liber Primus archive, visual, numeric, stego, DWH, GP, tool, wiki, forum, Pastebin, Google, Dropbox, YouTube, and community-source records.

The harvester is safe by default:

- `plan` and `validate-manifest` do not fetch network content.
- `fetch` requires `--allow-network`, and download-style capture requires `--allow-downloads`.
- `fetch` requires an output root and rejects ordinary committed repository paths as raw output roots.
- Google Sheet, Google Doc, Google Colab, and Dropbox sources are manual-export/local-ignored sources.
- Google Drive is not a project storage location.
- Raw downloads, scraped bodies, archives, images, audio, video, and extracted full bodies are not committed.

Stage 5AF generated only dry-run reports under `experiments/results/source-harvester/stage5af/`. It did not run a live broad crawl, process raw archives, run CUDA, run p56/full-p56/unsolved-page CUDA, benchmark, execute scored experiments, expand the website, or make a solve claim.

The committed manifest is `data/source-harvester/stage5af-cicada-source-manifest.yaml`. Future stages may run the harvester against user-provided local downloads, but the raw output roots must remain ignored.
