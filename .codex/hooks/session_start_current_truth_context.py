"""Project-local SessionStart current-truth context hook."""

from __future__ import annotations

from pathlib import Path
import re


def main() -> int:
    root = _repo_root()
    state = root / "data/project-state/current-stage-state.yaml"
    text = state.read_text(encoding="utf-8") if state.exists() else ""
    latest = _field(text, "latest_completed_stage_title")
    next_stage = _field(text, "recommended_next_stage_title")
    print("LiberPrimus current truth: data/project-state/current-stage-state.yaml is authoritative.")
    if latest:
        print(f"Latest completed: {latest}")
    if next_stage:
        print(f"Next routed: {next_stage}")
    return 0


def _repo_root() -> Path:
    path = Path.cwd().resolve()
    for candidate in (path, *path.parents):
        if (candidate / ".git").exists():
            return candidate
    return path


def _field(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


if __name__ == "__main__":
    raise SystemExit(main())
