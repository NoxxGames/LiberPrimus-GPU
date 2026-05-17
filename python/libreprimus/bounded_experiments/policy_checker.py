"""Evaluate bounded experiment queue items against the Stage 2J operator policy."""

from __future__ import annotations

from typing import Any

from libreprimus.bounded_experiments.models import BoundedExperimentQueue, OperatorPolicy, PolicyCheckResult

PASS = "pass"
FAIL = "fail"
WARNING = "warning"


def check_queue(policy: OperatorPolicy, queue: BoundedExperimentQueue) -> list[PolicyCheckResult]:
    if queue.policy_id != policy.policy_id:
        raise ValueError(f"Queue policy_id {queue.policy_id!r} does not match policy {policy.policy_id!r}.")
    return [check_item(policy, item) for item in queue.items]


def check_item(policy: OperatorPolicy, item: dict[str, Any]) -> PolicyCheckResult:
    checks: list[dict[str, str]] = []
    blocking: list[str] = []
    warnings: list[str] = []

    def add(check_id: str, ok: bool, message: str, reason: str | None = None) -> None:
        status = PASS if ok else FAIL
        checks.append({"check_id": check_id, "status": status, "message": message})
        if not ok:
            blocking.append(reason or check_id)

    item_id = str(item.get("item_id", "unknown-item"))
    add("enabled", bool(item.get("enabled")), "Item is enabled.", "item_disabled")
    add(
        "candidate_count_upper_bound",
        int(item.get("candidate_count_upper_bound", 0)) <= policy.max_candidate_count,
        f"Candidate upper bound <= {policy.max_candidate_count}.",
        "over_candidate_limit_requires_explicit_user_instruction",
    )
    add(
        "estimated_runtime_seconds",
        int(item.get("estimated_runtime_seconds", 0)) <= policy.max_estimated_runtime_seconds,
        f"Estimated runtime <= {policy.max_estimated_runtime_seconds} seconds.",
        "over_runtime_limit_requires_explicit_user_instruction",
    )
    add(
        "generated_output_budget_mb",
        float(item.get("generated_output_budget_mb", 0)) <= policy.max_generated_output_mb,
        f"Generated output budget <= {policy.max_generated_output_mb:g} MB.",
        "over_output_limit_requires_explicit_user_instruction",
    )
    add("cpu_only", item.get("cpu_only") is True, "CPU-only execution is required.", "non_cpu_execution_blocked")
    add("cuda_disabled", item.get("cuda_enabled") is False, "CUDA must remain disabled.", "cuda_requires_explicit_user_instruction")
    add(
        "cloud_disabled",
        item.get("cloud_execution", False) is False,
        "Cloud execution must remain disabled.",
        "cloud_requires_explicit_user_instruction",
    )
    add(
        "paid_services_disabled",
        item.get("external_paid_services", item.get("paid_services", False)) is False,
        "Paid services must remain disabled.",
        "paid_services_require_explicit_user_instruction",
    )
    add(
        "raw_data_not_committed",
        item.get("raw_data_committed", False) is False,
        "Raw data must not be committed.",
        "raw_data_commit_blocked",
    )
    add(
        "generated_outputs_not_committed",
        item.get("generated_outputs_committed", False) is False
        and dict(item.get("output_policy", {})).get("commit_outputs", False) is False,
        "Generated outputs must remain ignored.",
        "generated_output_commit_requires_explicit_user_instruction",
    )
    add(
        "canonical_corpus_inactive",
        item.get("canonical_corpus_active", False) is False,
        "Canonical corpus remains inactive.",
        "canonical_corpus_activation_requires_explicit_user_instruction",
    )
    add(
        "page_boundaries_not_final",
        item.get("page_boundaries_final", False) is False,
        "Page boundaries remain reviewable.",
        "page_boundary_finalization_requires_explicit_user_instruction",
    )
    add(
        "no_solve_claim",
        item.get("no_solve_claim") is True and item.get("solve_claim_made", False) is False,
        "No solve claim is made.",
        "solve_claim_requires_explicit_user_instruction",
    )

    scoring = item.get("scoring_enabled", False)
    if scoring not in {False, "trivial_summary_only", "minimal_triage"}:
        add("scoring_bounded", False, "Scoring must be false, trivial_summary_only, or minimal_triage.", "scoring_not_allowed")
    else:
        checks.append(
            {
                "check_id": "scoring_bounded",
                "status": PASS,
                "message": "Scoring is disabled or limited to bounded local triage.",
            }
        )

    key_count = _declared_key_count(item)
    if key_count is not None:
        add(
            "declared_key_count_within_bound",
            key_count <= int(item.get("candidate_count_upper_bound", 0)),
            "Declared explicit key count is within candidate_count_upper_bound.",
            "declared_key_count_exceeds_candidate_bound",
        )

    selector = dict(dict(item.get("corpus_slice", {})).get("selector", {}))
    if item.get("experiment_kind") == "caesar_affine_reviewable_slice" and (
        not selector.get("page_candidate_id") or "placeholder" in str(selector.get("page_candidate_id"))
    ):
        warnings.append("Reviewable-slice item is policy-eligible but requires a safe real executor before execution.")

    status = FAIL if blocking else WARNING if warnings else PASS
    return PolicyCheckResult(
        item_id=item_id,
        policy_id=policy.policy_id,
        status=status,
        checks=checks,
        blocking_reasons=blocking,
        warnings=warnings,
    )


def _declared_key_count(item: dict[str, Any]) -> int | None:
    if str(item.get("experiment_kind", "")) not in {"vigenere_tiny_key_list_preview", "vigenere_key_list_preview"}:
        return None
    families = dict(item.get("transform_plan", {})).get("families", [])
    for family in families:
        if not isinstance(family, dict):
            continue
        params = dict(family.get("parameters", {}))
        keys = params.get("keys")
        if isinstance(keys, list):
            return len(keys)
    return None
