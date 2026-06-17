"""Bounded SessionStart preflight for doc-staleness warnings."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import time
from typing import Any

from hook_common import (
    drain_stdin,
    env_for_repo,
    python_for_repo,
    repo_root_from,
    strict_mode,
    write_report,
)

REPORT_RELATIVE = Path("experiments/results/doc-drift/codex-preprompt-doc-staleness-preflight.json")
SCANNER_TIMEOUT_SECONDS = 120
MAX_WARNING_EXAMPLES = 5
AUTHORITATIVE_REPORT_KINDS = {"daily_doc_staleness_automation", "local_stale_current_reproduction"}
NONAUTHORITATIVE_REPORT_KINDS = {
    "codex_preprompt_doc_staleness_preflight",
    "codex_stop_doc_staleness_guard",
}


def main() -> int:
    drain_stdin()
    root = repo_root_from(Path(__file__))
    report_path = root / REPORT_RELATIVE
    strict = strict_mode()
    try:
        status = _latest_report_status(root)
        if status is None:
            status = _run_local_reproduction(root, report_path)
        _annotate_preflight_report(status)
        _emit_status(status)
        exit_code = _strict_exit_code(status) if strict else 0
        status["strict_mode"] = strict
        status["exit_code"] = exit_code
        write_report(report_path, status)
        return exit_code
    except Exception as exc:
        payload = {
            "preflight_status": "report_unavailable",
            "required_action": "triage_doc_staleness_before_main_task",
            "warning_count": None,
            "error_count": None,
            "report_path": REPORT_RELATIVE.as_posix(),
            "timeout_recorded": False,
            "exception": repr(exc),
            "strict_mode": strict,
            "exit_code": 1 if strict else 0,
        }
        _annotate_preflight_report(payload)
        _emit_status(payload)
        write_report(report_path, payload)
        return 1 if strict else 0


def _latest_report_status(root: Path) -> dict[str, Any] | None:
    candidates = sorted(
        (root / "experiments/results/doc-drift").glob("*.json"),
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    now = time.time()
    for candidate in candidates:
        if not candidate.exists() or now - candidate.stat().st_mtime > 24 * 60 * 60:
            continue
        try:
            payload = json.loads(candidate.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not _may_use_as_latest_report(candidate, payload):
            continue
        warning_count = _int_value(payload, "warning_count", "stale_current_warning_count")
        error_count = _int_value(payload, "error_count", "stale_current_error_count")
        if warning_count is None and isinstance(payload.get("findings"), list):
            warning_count = sum(1 for item in payload["findings"] if str(item.get("severity", "")).startswith("warning"))
        if error_count is None and isinstance(payload.get("findings"), list):
            error_count = sum(1 for item in payload["findings"] if item.get("severity") == "error")
        if warning_count is None and error_count is None:
            continue
        return {
            "preflight_status": _status_for_counts(warning_count, error_count),
            "required_action": _action_for_counts(warning_count, error_count),
            "warning_count": warning_count,
            "error_count": error_count,
            "report_path": REPORT_RELATIVE.as_posix(),
            "source_report_path": candidate.relative_to(root).as_posix(),
            "source_report_kind": payload.get("report_kind", "legacy_filename_classified"),
            "source": "latest_doc_staleness_report_within_24h",
            "timeout_recorded": False,
            "warning_examples": _warning_examples(payload),
        }
    return None


def _run_local_reproduction(root: Path, report_path: Path) -> dict[str, Any]:
    command = [
        str(python_for_repo(root)),
        "-m",
        "libreprimus.cli",
        "consistency",
        "audit-stale-current-claims",
        "--strict",
        "--report-only",
        "--out",
        str(report_path),
    ]
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=env_for_repo(root),
            text=True,
            capture_output=True,
            timeout=SCANNER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return {
            "preflight_status": "report_unavailable",
            "required_action": "triage_doc_staleness_before_main_task",
            "warning_count": None,
            "error_count": None,
            "report_path": REPORT_RELATIVE.as_posix(),
            "source": "local_reproduction_timeout",
            "timeout_recorded": True,
        }

    payload: dict[str, Any] = {}
    if report_path.exists():
        try:
            payload = json.loads(report_path.read_text(encoding="utf-8"))
        except Exception:
            payload = {}
    warning_count = _int_value(payload, "warning_count", "stale_current_warning_count")
    error_count = _int_value(payload, "error_count", "stale_current_error_count")
    if warning_count is None:
        warning_count = _count_cli_line(result.stdout, "stale_current_warning_count")
    if error_count is None:
        error_count = _count_cli_line(result.stdout, "stale_current_error_count")
    return {
        "preflight_status": _status_for_counts(warning_count, error_count, result.returncode),
        "required_action": _action_for_counts(warning_count, error_count, result.returncode),
        "warning_count": warning_count,
        "error_count": error_count,
        "report_path": REPORT_RELATIVE.as_posix(),
        "source": "local_report_only_reproduction",
        "scanner_return_code": result.returncode,
        "timeout_recorded": False,
        "warning_examples": _warning_examples(payload),
    }


def _emit_status(status: dict[str, Any]) -> None:
    print(f"LIBERPRIMUS_PREFLIGHT_DOC_STALENESS_STATUS={status.get('preflight_status', 'report_unavailable')}")
    print(f"LIBERPRIMUS_PREFLIGHT_REQUIRED_ACTION={status.get('required_action', 'triage_doc_staleness_before_main_task')}")
    print(f"LIBERPRIMUS_PREFLIGHT_REPORT={REPORT_RELATIVE.as_posix()}")
    print(f"LIBERPRIMUS_PREFLIGHT_WARNING_COUNT={_display(status.get('warning_count'))}")
    print(f"LIBERPRIMUS_PREFLIGHT_ERROR_COUNT={_display(status.get('error_count'))}")
    if status.get("preflight_status") in {"warnings", "errors", "report_unavailable"}:
        print(
            "Before implementing the user prompt, Codex must triage doc-staleness warnings, "
            "fix legitimate current-doc drift, avoid scanner weakening, run the strict "
            "stale-current scanner, and only then continue with the requested stage work."
        )
        for example in (status.get("warning_examples") or [])[:MAX_WARNING_EXAMPLES]:
            print(f"LIBERPRIMUS_PREFLIGHT_WARNING_EXAMPLE={example}")


def _annotate_preflight_report(payload: dict[str, Any]) -> None:
    payload.update(
        {
            "report_kind": "codex_preprompt_doc_staleness_preflight",
            "report_producer": ".codex/hooks/doc_staleness_preflight.py",
            "authoritative_automation_report": False,
            "may_be_used_as_latest_automation_report": False,
        }
    )


def _may_use_as_latest_report(path: Path, payload: dict[str, Any]) -> bool:
    report_kind = payload.get("report_kind")
    if report_kind in AUTHORITATIVE_REPORT_KINDS:
        return True
    if report_kind in NONAUTHORITATIVE_REPORT_KINDS:
        return False
    if payload.get("may_be_used_as_latest_automation_report") is False:
        return False
    name = path.name.lower()
    if name in {
        "codex-preprompt-doc-staleness-preflight.json",
        "codex-stop-hook-stale-current-audit.json",
    }:
        return False
    if "preprompt" in name or "stop-hook" in name or "stop" in name:
        return False
    return "local-stale-current-triage" in name or "daily" in name or "automation" in name or "stale-current" in name


def _status_for_counts(warnings: int | None, errors: int | None, return_code: int = 0) -> str:
    if errors and errors > 0:
        return "errors"
    if warnings and warnings > 0:
        return "warnings"
    if warnings == 0 and errors == 0 and return_code == 0:
        return "clean"
    return "report_unavailable"


def _action_for_counts(warnings: int | None, errors: int | None, return_code: int = 0) -> str:
    status = _status_for_counts(warnings, errors, return_code)
    if status == "errors":
        return "fix_doc_staleness_before_main_task"
    if status in {"warnings", "report_unavailable"}:
        return "triage_doc_staleness_before_main_task"
    return "proceed"


def _strict_exit_code(status: dict[str, Any]) -> int:
    return 0 if status.get("preflight_status") == "clean" else 1


def _int_value(payload: dict[str, Any], *keys: str) -> int | None:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                pass
    return None


def _count_cli_line(text: str, key: str) -> int | None:
    prefix = f"{key}="
    for line in text.splitlines():
        if line.startswith(prefix):
            try:
                return int(line.removeprefix(prefix).strip())
            except ValueError:
                return None
    return None


def _warning_examples(payload: dict[str, Any]) -> list[str]:
    findings = payload.get("findings")
    if not isinstance(findings, list):
        return []
    examples = []
    for item in findings:
        if not str(item.get("severity", "")).startswith("warning"):
            continue
        examples.append(f"{item.get('claim_type')}:{item.get('path')}:{item.get('line')}")
        if len(examples) >= MAX_WARNING_EXAMPLES:
            break
    return examples


def _display(value: object) -> str:
    return "null" if value is None else str(value)


if __name__ == "__main__":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    raise SystemExit(main())
