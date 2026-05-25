# Source Harvester Workflow

Use this workflow when running the Stage 5AF harvester locally. For Stage 5AG local source inventory over `third_party/`, use `docs/onboarding/local-source-inventory-workflow.md` after validating the manifest. Stage 5AH repaired the documentation gate; Stage 5AI completed curated extraction metadata; Stage 5AJ integrated UsefulFilesAndIdeas metadata and extraction/redaction/scraper policy; Stage 5AK integrated community-facts claim-record metadata; Stage 5AL added the website-ingest and private Deep Research export layer; Stage 5AM rendered that metadata into an ignored private static research index; Stage 5AN added the ignored private content pack and hosted private-content webroot; Stage 5AP added page 49-51 token-block source-lock metadata; Stage 5AR added original-image coordinate-lock metadata while keeping raw/extracted bodies ignored.

1. Validate the committed manifest:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester validate-manifest `
  --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml
```

2. Build a dry-run plan:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester plan `
  --manifest data/source-harvester/stage5af-cicada-source-manifest.yaml `
  --out experiments/results/source-harvester/stage5af/harvest_plan.json
```

3. Put user-provided exports/downloads only under ignored local roots:

- `source-harvester-output/`
- `harvest-output/`
- `research-inputs/`
- another ignored local path outside the repo

Do not use Google Drive as storage for this project. For Google Sheet, Google Doc, Google Colab, and Dropbox sources, manually export files to local ignored storage, then inventory those local files.

4. Hash or inventory local material:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli source-harvester hash-path `
  --path source-harvester-output `
  --out experiments/results/source-harvester/stage5af/local_hashes.jsonl
```

5. Commit only compact metadata when a future prompt explicitly scopes it. Do not commit raw downloads, archives, scraped bodies, images, audio, video, generated bundles, or `codex-output/**`.

Stage 5AG adds local inventory outputs under `experiments/results/source-harvester-local/stage5ag/` and compact metadata under `data/source-harvester/stage5ag-*`. Stage 5AH adds doc-staleness/stage-ledger coverage before extraction resumes. Stage 5AI adds curated bundle metadata under `data/source-harvester/stage5ai-*`, generated ignored bundle bodies under `research-inputs/stage5ai/`, and generated ignored reports under `experiments/results/research-bundles/stage5ai/`. Stage 5AJ adds UsefulFilesAndIdeas metadata under `data/source-harvester/stage5aj-*`, generated ignored bundle bodies under `research-inputs/stage5aj/`, and generated ignored reports under `experiments/results/source-harvester-usefulfiles/stage5aj/`. Stage 5AK adds community-facts metadata under `data/source-harvester/stage5ak-*`, generated ignored private addenda under `research-inputs/stage5ak/`, and generated ignored reports under `experiments/results/source-harvester-community-facts/stage5ak/`. Stage 5AL adds `data/website-ingest/stage5al/`, `data/source-harvester/stage5al-*`, ignored `research-inputs/stage5al/`, and ignored `experiments/results/website-ingest/stage5al/`. Stage 5AM adds `data/website-render/stage5am-*`, ignored static export files under `website-export/stage5am/`, and ignored renderer reports under `experiments/results/website-render/stage5am/`. Stage 5AN adds `data/deep-research-export/stage5an-*`, ignored private pack files under `deep-research-content-packs/stage5an/`, and ignored hosted/webroot files under `website-export/stage5an/`. Stage 5AP adds `data/token-block/stage5ap-*`, `data/stego/stage5ap-outguess-*`, and ignored token-block/stego-control reports under `experiments/results/token-block/stage5ap/` and `experiments/results/stego-controls/stage5ap/`. Stage 5AR adds `data/token-block/stage5ar-*`, `data/project-state/stage5ar-*`, and ignored coordinate reports under `experiments/results/token-block/stage5ar/`. Online fetching/cloning, Google Drive storage, public website publication, and Deep Research execution remain out of scope until explicitly scoped.
