"""Stage 2F result-store integration preview helpers."""

from __future__ import annotations

from typing import Any


def build_result_store_preview(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "record_type": "cpu_execution_result_store_preview",
        "import_mode": "preview_only",
        "jsonl_sink_supported": True,
        "sqlite_sink_supported": True,
        "committed_outputs": False,
        "result_count": summary.get("result_count", 0),
        "deferred_reason": "Stage 2F writes ignored execution records; DB import remains generated output.",
    }

