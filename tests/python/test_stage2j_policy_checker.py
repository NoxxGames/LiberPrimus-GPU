from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from libreprimus.bounded_experiments.policy_checker import check_item, check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"
QUEUE = REPO / "experiments/queues/stage2j-bounded-cpu-queue.yaml"


def _loaded():
    return load_operator_policy(POLICY), load_bounded_queue(QUEUE)


def test_policy_checker_accepts_841_candidate_item() -> None:
    policy, queue = _loaded()
    checks = {check.item_id: check for check in check_queue(policy, queue)}

    check = checks["stage2j-caesar-affine-first-reviewable-slice"]
    assert check.status == "warning"
    assert check.blocking_reasons == []


def test_policy_checker_accepts_solved_baseline_control() -> None:
    policy, queue = _loaded()
    checks = {check.item_id: check for check in check_queue(policy, queue)}

    check = checks["stage2j-solved-baseline-regression-control"]
    assert check.status == "pass"
    assert check.blocking_reasons == []


def test_policy_checker_blocks_overbudget_item() -> None:
    policy, queue = _loaded()
    checks = {check.item_id: check for check in check_queue(policy, queue)}

    check = checks["stage2j-blocked-overbudget-example"]
    assert check.status == "fail"
    assert "over_candidate_limit_requires_explicit_user_instruction" in check.blocking_reasons


def test_policy_checker_blocks_cuda_cloud_solve_claim_and_output_commit() -> None:
    policy, queue = _loaded()
    base = next(item for item in queue.items if item["item_id"] == "stage2j-solved-baseline-regression-control")

    for field, value, expected in [
        ("cuda_enabled", True, "cuda_requires_explicit_user_instruction"),
        ("cloud_execution", True, "cloud_requires_explicit_user_instruction"),
        ("solve_claim_made", True, "solve_claim_requires_explicit_user_instruction"),
        ("generated_outputs_committed", True, "generated_output_commit_requires_explicit_user_instruction"),
    ]:
        item = deepcopy(base)
        item["item_id"] = f"bad-{field}"
        item[field] = value
        check = check_item(policy, item)
        assert check.status == "fail"
        assert expected in check.blocking_reasons


def test_policy_checker_blocks_generated_output_commit_request() -> None:
    policy, queue = _loaded()
    item = deepcopy(next(item for item in queue.items if item["item_id"] == "stage2j-solved-baseline-regression-control"))
    item["item_id"] = "bad-output-policy"
    item["output_policy"]["commit_outputs"] = True

    check = check_item(policy, item)

    assert check.status == "fail"
    assert "generated_output_commit_requires_explicit_user_instruction" in check.blocking_reasons
