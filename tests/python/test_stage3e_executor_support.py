from __future__ import annotations

from pathlib import Path

from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.method_backlog.support import classify_executor_support

REPO = Path(__file__).resolve().parents[2]
QUEUE = REPO / "experiments/queues/stage3e-bounded-cpu-queue.yaml"


def test_stage3e_executor_support_classification_is_deterministic() -> None:
    queue = load_bounded_queue(QUEUE)
    statuses = {str(item["item_id"]): classify_executor_support(item) for item in queue.items}

    assert statuses == {
        "stage3e_vig_lp_evidence_pack_v1": ("runnable_now", "stage3f_evidence_key_pack_executor"),
        "stage3e_prime_minus_one_offsets_v1": ("runnable_now", "stage3g_prime_offset_sweep_executor"),
        "stage3e_vig_history_key_pack_v1": ("runnable_now", "stage3i_historical_key_pack_executor"),
        "stage3e_negative_control_extension_v1": ("needs_executor", "family_specific_negative_control_executor"),
        "stage3e_reset_advance_ablation_v1": ("runnable_now", "stage3h_reset_advance_ablation_executor"),
        "stage3e_prime_mod_gap_pack_v1": ("dry_run_only", "prime_neighbour_stream_executor"),
        "stage3i_mersenne_prime_stream_tiny_v1": ("runnable_now", "stage3j_mersenne_stream_probe_executor"),
    }


def test_stage3e_manifest_statuses_match_support_policy() -> None:
    queue = load_bounded_queue(QUEUE)

    for item in queue.items:
        status, reason = classify_executor_support(item)
        assert item["implementation_status"] == status
        assert item["required_executor"] == reason
