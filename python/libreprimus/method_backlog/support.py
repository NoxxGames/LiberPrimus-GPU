"""Executor-support classification for Stage 3E queue items."""

from __future__ import annotations

from typing import Any


def classify_executor_support(item: dict[str, Any]) -> tuple[str, str]:
    kind = str(item.get("experiment_kind", ""))
    declared = str(item.get("implementation_status", "needs_executor"))
    if declared == "blocked":
        return "blocked", str(item.get("required_executor", "blocked_by_manifest"))
    if kind == "vigenere_key_pack":
        if (
            item.get("item_id") == "stage3e_vig_lp_evidence_pack_v1"
            and declared == "runnable_now"
            and item.get("required_executor") == "stage3f_evidence_key_pack_executor"
        ):
            return "runnable_now", "stage3f_evidence_key_pack_executor"
        if (
            item.get("item_id") == "stage3e_vig_history_key_pack_v1"
            and declared == "runnable_now"
            and item.get("required_executor") == "stage3i_historical_key_pack_executor"
        ):
            return "runnable_now", "stage3i_historical_key_pack_executor"
        return "needs_executor", "reset_advance_key_pack_executor"
    if kind == "prime_minus_one_offset_sweep":
        if (
            item.get("item_id") == "stage3e_prime_minus_one_offsets_v1"
            and declared == "runnable_now"
            and item.get("required_executor") == "stage3g_prime_offset_sweep_executor"
        ):
            return "runnable_now", "stage3g_prime_offset_sweep_executor"
        return "needs_executor", "prime_offset_sweep_executor"
    if kind == "family_specific_negative_controls":
        if (
            item.get("item_id") == "stage3h_family_specific_negative_controls_v1"
            and declared == "runnable_now"
            and item.get("required_executor") == "stage3h_family_negative_control_executor"
        ):
            return "runnable_now", "stage3h_family_negative_control_executor"
        return "needs_executor", "family_specific_negative_control_executor"
    if kind == "reset_advance_ablation":
        if (
            item.get("item_id") in {"stage3e_reset_advance_ablation_v1", "stage3h_reset_advance_ablation_v1"}
            and declared == "runnable_now"
            and item.get("required_executor") == "stage3h_reset_advance_ablation_executor"
        ):
            return "runnable_now", "stage3h_reset_advance_ablation_executor"
        return "dry_run_only", "reset_advance_state_machine"
    if kind == "prime_neighbour_streams":
        return "dry_run_only", "prime_neighbour_stream_executor"
    if kind == "mersenne_prime_stream_tiny":
        return "needs_executor", "mersenne_prime_stream_executor"
    return "needs_executor", f"unsupported_experiment_kind:{kind}"


def unsupported_executor_reasons(items: list[dict[str, Any]]) -> dict[str, str]:
    return {str(item.get("item_id")): classify_executor_support(item)[1] for item in items}
