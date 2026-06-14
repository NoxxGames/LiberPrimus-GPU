# Daily Doc-Staleness Triage Setup

Automation name: `LiberPrimus daily doc-staleness and current-truth drift audit`

Suggested cadence: daily at 09:00 Europe/London.

Expected behavior:
- Report-only.
- Auto-edit disabled.
- Auto-commit disabled.
- Source-lock mutation disabled.
- Puzzle execution disabled.
- Execution environment: local repository checkout.
- Preferred command:
  `.\.venv\Scripts\python.exe -m libreprimus.cli consistency audit-stale-current-claims --strict --report-only`
- Environment failures must be reported explicitly and must not be counted as document drift.
- Output goes to the Codex Automations Triage inbox.

If runtime automation creation is unavailable, create this manually from
`docs/automations/daily-doc-staleness-triage.prompt.md`.
