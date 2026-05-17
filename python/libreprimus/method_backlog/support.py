"""Executor-support classification for Stage 3E queue items."""

from __future__ import annotations

from typing import Any


def classify_executor_support(item: dict[str, Any]) -> tuple[str, str]:
    kind = str(item.get("experiment_kind", ""))
    declared = str(item.get("implementation_status", "needs_executor"))
    if declared == "blocked":
        return "blocked", str(item.get("required_executor", "blocked_by_manifest"))
    if kind == "vigenere_key_pack":
        return "needs_executor", "reset_advance_key_pack_executor"
    if kind == "prime_minus_one_offset_sweep":
        return "needs_executor", "prime_offset_sweep_executor"
    if kind == "family_specific_negative_controls":
        return "needs_executor", "family_specific_negative_control_executor"
    if kind == "reset_advance_ablation":
        return "dry_run_only", "reset_advance_state_machine"
    if kind == "prime_neighbour_streams":
        return "dry_run_only", "prime_neighbour_stream_executor"
    return "needs_executor", f"unsupported_experiment_kind:{kind}"


def unsupported_executor_reasons(items: list[dict[str, Any]]) -> dict[str, str]:
    return {str(item.get("item_id")): classify_executor_support(item)[1] for item in items}
