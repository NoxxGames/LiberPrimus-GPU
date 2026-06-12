# Daily Doc-Staleness Triage Automation

Report-only daily audit for `LiberPrimus daily doc-staleness and current-truth drift audit`.

Rules:
- Do not edit files.
- Do not commit.
- Do not run puzzle, route, source-lock, number-fact, byte-stream, CUDA, scoring, benchmark, image, OCR, audio, stego, or website work.
- Read `data/project-state/current-stage-state.yaml`.
- Run or simulate `python -m libreprimus.cli consistency audit-stale-current-claims --report-only`.
- Run current/next consistency in report-only mode.
- Report exact path, line, matched text, severity, and suggested fix to the Automations/Triage inbox.
- If there are no findings, say no actionable drift found.
