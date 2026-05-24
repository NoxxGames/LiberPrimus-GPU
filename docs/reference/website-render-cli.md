# Website Render CLI

The Stage 5AM renderer is available as:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli website-render build-stage5am-site
.\.venv\Scripts\python.exe -m libreprimus.cli website-render validate-stage5am-site
.\.venv\Scripts\python.exe -m libreprimus.cli website-render build-stage5am-guardrail
.\.venv\Scripts\python.exe -m libreprimus.cli website-render build-stage5am-next-stage-decision
.\.venv\Scripts\python.exe -m libreprimus.cli website-render build-stage5am-summary
.\.venv\Scripts\python.exe -m libreprimus.cli website-render validate-stage5am
.\.venv\Scripts\python.exe -m libreprimus.cli website-render summary
```

The build command reads committed Stage 5AL metadata and writes the generated site under `website-export/stage5am/research-index/`. The validate command works from committed metadata plus ignored generated site files and does not read raw sources.
