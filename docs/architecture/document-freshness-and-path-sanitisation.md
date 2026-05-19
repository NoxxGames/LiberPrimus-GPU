# Document Freshness And Path Sanitisation

Stage 4J hardens operational documentation against stale current-state claims
and local workstation path leaks.

Long-lived current-state docs should link to `STATUS.md` and
`docs/roadmap/staged-plan.md` instead of repeating volatile stage text. When
stage status changes, update README, STATUS, ROADMAP, AGENTS, the staged plan,
and affected reference/tutorial docs together.

Committed operational records and docs must use repository-relative paths for
generated outputs. Absolute workstation paths such as Windows drive paths, UNC
shares, Linux home directories, or macOS user-home paths are rejected unless a
troubleshooting example is explicitly marked with `example_path`.

Run:

```powershell
.\.venv\Scripts\python.exe -m libreprimus.cli observation-review check-paths --repo-root .
```
