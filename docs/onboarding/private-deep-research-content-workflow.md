# Private Deep Research Content Workflow

Use this workflow when preparing the private Stage 5AN content package for Deep Research or when handing Stage 5AT review-pack metadata, Stage 5AR coordinate-lock metadata, and Stage 5AP token-block metadata to manual review.

1. Validate Stage 5AL and Stage 5AM records.
2. Build the Stage 5AN content pack, hosted private-content export, and combined webroot with `libreprimus deep-research-export`.
3. Validate Stage 5AN records and generated private outputs with `validate-stage5an`.
4. Confirm generated outputs remain ignored:

```powershell
git check-ignore -v deep-research-content-packs/stage5an/deep-research-content-pack-stage5an.zip
git check-ignore -v website-export/stage5an/private-content/index.html
git check-ignore -v website-export/stage5an/webserver-root/index.html
git check-ignore -v website-export/stage5an/webserver-root/private-content/index.html
```

5. For hosted handoff, copy the contents of `website-export/stage5an/webserver-root/` to the private webserver root.

Deep Research should use the metadata site and private content URL together. Stage 5AU should use `data/token-block/stage5at-*`, `data/project-state/stage5at-summary.yaml`, `data/token-block/stage5ar-*`, `data/project-state/stage5ar-summary.yaml`, `data/token-block/stage5ap-*`, `data/stego/stage5ap-outguess-*`, and `data/project-state/stage5ap-summary.yaml` for page 49-51 token-case review. Do not hand off raw `third_party/` paths or raw page images as source truth, and do not treat hosted private extracts, token-block preflight records, coordinate-lock records, or generated review-pack crops as public publication or solve evidence.
