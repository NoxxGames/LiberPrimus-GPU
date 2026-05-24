# Private Deep Research Content Workflow

Use this workflow when preparing the private Stage 5AN content package for Deep Research.

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

Deep Research should use the metadata site and private content URL together. Do not hand off raw `third_party/` paths as source truth, and do not treat hosted private extracts as public publication or solve evidence.
