"""SessionStart dispatcher preserving current truth before doc-staleness preflight."""

from __future__ import annotations

from pathlib import Path
import importlib.util
import sys

from hook_common import drain_stdin, strict_mode


def main() -> int:
    drain_stdin()
    failures = []
    for script_name in ("session_start_current_truth_context.py", "doc_staleness_preflight.py"):
        try:
            module = _load_hook_module(script_name)
            result = int(module.main())
        except Exception as exc:
            print(f"LiberPrimus SessionStart dispatcher warning: {script_name}: {exc}", file=sys.stderr)
            result = 1
        if result != 0:
            failures.append((script_name, result))
    if strict_mode() and failures:
        return failures[0][1] or 1
    return 0


def _load_hook_module(script_name: str):
    path = Path(__file__).resolve().parent / script_name
    spec = importlib.util.spec_from_file_location(f"liberprimus_codex_hook_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    raise SystemExit(main())
