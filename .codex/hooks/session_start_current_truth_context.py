"""Project-local SessionStart current-truth context hook."""

from __future__ import annotations

from pathlib import Path
import re
import sys

from hook_common import drain_stdin, repo_root_from, strict_mode


def main() -> int:
    drain_stdin()
    try:
        root = repo_root_from(Path(__file__))
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
    except Exception as exc:
        print(f"LiberPrimus SessionStart hook warning: {exc}", file=sys.stderr)
        return 1 if strict_mode() else 0


def _field(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


if __name__ == "__main__":
    raise SystemExit(main())
