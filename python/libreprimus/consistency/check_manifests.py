"""Manifest consistency checks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from libreprimus.bounded_experiments.policy_checker import check_queue
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.approval_readiness.readiness_analyzer import analyze_approval_readiness
from libreprimus.approval_execution.approval_gate import evaluate_approval_execution_gate
from libreprimus.approval_execution.request_loader import load_approval_execution_request
from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest
from libreprimus.experiment_proposals.approval_records import load_approval_record
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal
from libreprimus.experiments.candidate_estimator import estimate_candidate_count
from libreprimus.experiments.manifest_loader import load_exploratory_manifest
from libreprimus.method_backlog.counts import validate_candidate_count
from libreprimus.method_backlog.loader import load_method_backlog
from libreprimus.method_backlog.support import classify_executor_support
from libreprimus.method_backlog.validation import validate_stage3e_queue_item
from libreprimus.paths import repo_root
from libreprimus.result_store.validation import validate_result_store_manifest_file
from libreprimus.solved_baselines.validation import validate_manifest_file
from libreprimus.transforms.registry import DEFAULT_REGISTRY_PATH, compute_sha256

GROUP = "manifests"
SOLVED_MANIFEST_DIR = repo_root() / "experiments/manifests/solved-baselines"
RESULT_STORE_MANIFEST_DIR = repo_root() / "experiments/manifests/result-store"
EXPLORATORY_MANIFEST_DIR = repo_root() / "experiments/manifests/exploratory"
CPU_EXECUTION_MANIFEST_DIR = repo_root() / "experiments/manifests/cpu-execution"
PROPOSAL_DIR = repo_root() / "experiments/proposals/stage2g"
APPROVAL_RECORD_DIR = repo_root() / "experiments/proposals/stage2g/approval-records"
STAGE2H_PROPOSAL_DIR = repo_root() / "experiments/proposals/stage2h"
STAGE2H_APPROVAL_RECORD_DIR = repo_root() / "experiments/proposals/stage2h/approval-records"
STAGE2I_PROPOSAL_DIR = repo_root() / "experiments/proposals/stage2i"
STAGE2I_APPROVAL_RECORD_DIR = repo_root() / "experiments/proposals/stage2i/approval-records"
OPERATOR_POLICY_PATH = repo_root() / "experiments/policies/operator-policy-v0.yaml"
BOUNDED_QUEUE_PATH = repo_root() / "experiments/queues/stage2j-bounded-cpu-queue.yaml"
STAGE3B_BOUNDED_QUEUE_PATH = repo_root() / "experiments/queues/stage3b-bounded-cpu-queue.yaml"
STAGE3C_BOUNDED_QUEUE_PATH = repo_root() / "experiments/queues/stage3c-bounded-cpu-queue.yaml"
STAGE3E_METHOD_BACKLOG_PATH = repo_root() / "experiments/queues/stage3e-method-backlog.yaml"
STAGE3E_BOUNDED_QUEUE_PATH = repo_root() / "experiments/queues/stage3e-bounded-cpu-queue.yaml"
REGISTRY_PATH = repo_root() / DEFAULT_REGISTRY_PATH


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Manifest payload must be a mapping: {path}")
    return payload


def _no_raw_dump(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    return "data/raw" not in text and len(text) < 20000


def check_manifest_consistency(
    *,
    solved_manifest_dir: Path = SOLVED_MANIFEST_DIR,
    result_store_manifest_dir: Path = RESULT_STORE_MANIFEST_DIR,
    exploratory_manifest_dir: Path = EXPLORATORY_MANIFEST_DIR,
    cpu_execution_manifest_dir: Path = CPU_EXECUTION_MANIFEST_DIR,
    proposal_dir: Path = PROPOSAL_DIR,
    approval_record_dir: Path = APPROVAL_RECORD_DIR,
    stage2h_proposal_dir: Path = STAGE2H_PROPOSAL_DIR,
    stage2h_approval_record_dir: Path = STAGE2H_APPROVAL_RECORD_DIR,
    stage2i_proposal_dir: Path = STAGE2I_PROPOSAL_DIR,
    stage2i_approval_record_dir: Path = STAGE2I_APPROVAL_RECORD_DIR,
    operator_policy_path: Path = OPERATOR_POLICY_PATH,
    bounded_queue_path: Path = BOUNDED_QUEUE_PATH,
    stage3b_bounded_queue_path: Path = STAGE3B_BOUNDED_QUEUE_PATH,
    stage3c_bounded_queue_path: Path = STAGE3C_BOUNDED_QUEUE_PATH,
    stage3e_method_backlog_path: Path = STAGE3E_METHOD_BACKLOG_PATH,
    stage3e_bounded_queue_path: Path = STAGE3E_BOUNDED_QUEUE_PATH,
    registry_path: Path = REGISTRY_PATH,
) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    registry_sha = compute_sha256(registry_path)

    for manifest in sorted(solved_manifest_dir.glob("*.yaml")):
        try:
            errors = validate_manifest_file(manifest)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            errors = [str(exc)]
        if errors:
            results.extend(fail_result(GROUP, "solved_manifest_valid", error, path=manifest) for error in errors)
        else:
            results.append(pass_result(GROUP, "solved_manifest_valid", "Solved manifest validates.", path=manifest))
        payload = _load_yaml(manifest)
        _check_manifest_flags(results, payload, manifest)
        if payload.get("registry_sha256") != registry_sha:
            results.append(fail_result(GROUP, "manifest_registry_sha", "Registry SHA mismatch.", path=manifest))
        for group in payload.get("fixture_groups", []):
            fixture_dir = repo_root() / str(group.get("fixture_dir", ""))
            if not fixture_dir.is_dir():
                results.append(
                    fail_result(GROUP, "manifest_fixture_dir_exists", "Fixture dir missing.", path=fixture_dir)
                )
        if not _no_raw_dump(manifest):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Manifest appears to include raw data.", path=manifest))

    all_known = solved_manifest_dir / "stage2a-all-known-solved-baselines.yaml"
    if all_known.is_file():
        payload = _load_yaml(all_known)
        counts = payload.get("expected_counts", {})
        if counts.get("fixture_count") == 10 and counts.get("pass_count") == 10:
            results.append(pass_result(GROUP, "all_known_counts", "All-known manifest expects 10 passes."))
        else:
            results.append(fail_result(GROUP, "all_known_counts", "All-known manifest count drift."))

    for manifest in sorted(result_store_manifest_dir.glob("*.yaml")):
        try:
            errors = validate_result_store_manifest_file(manifest)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            errors = [str(exc)]
        if errors:
            results.extend(fail_result(GROUP, "result_store_manifest_valid", error, path=manifest) for error in errors)
        else:
            results.append(
                pass_result(GROUP, "result_store_manifest_valid", "Result-store manifest validates.", path=manifest)
            )
        payload = _load_yaml(manifest)
        _check_manifest_flags(results, payload, manifest)
        input_manifest = repo_root() / str(payload.get("input_manifest_path", ""))
        if not input_manifest.is_file():
            results.append(
                fail_result(GROUP, "result_store_input_manifest_exists", "Input manifest missing.", path=input_manifest)
            )

    exploratory_manifests = sorted(exploratory_manifest_dir.glob("*-dry-run.yaml"))
    for manifest in exploratory_manifests:
        try:
            loaded = load_exploratory_manifest(manifest)
            estimate = estimate_candidate_count(loaded.payload)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "exploratory_manifest_valid", str(exc), path=manifest))
            continue
        results.append(pass_result(GROUP, "exploratory_manifest_valid", "Exploratory manifest validates.", path=manifest))
        _check_exploratory_flags(results, loaded.payload, manifest)
        upper_bound = int(loaded.payload["expected_candidate_count_upper_bound"])
        if estimate.candidate_count > upper_bound:
            results.append(
                fail_result(
                    GROUP,
                    "exploratory_candidate_bound",
                    "Exploratory estimate exceeds upper bound.",
                    path=manifest,
                )
            )
        if not _no_raw_dump(manifest):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Manifest appears to include raw data.", path=manifest))

    if not any(result.check_name == "manifest_fixture_dir_exists" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_fixture_dir_exists", "Manifest fixture dirs exist."))
    if not any(result.check_name == "manifest_registry_sha" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_registry_sha", "Manifest registry SHA values match."))
    if not any(result.check_name == "manifest_flags_false" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_flags_false", "Manifest search/CUDA/scoring flags are false."))
    if not any(result.check_name == "manifest_no_raw_dump" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "manifest_no_raw_dump", "Manifests do not contain raw corpus dumps."))
    if exploratory_manifests and not any(
        result.check_name == "exploratory_manifest_valid" and result.is_failure for result in results
    ):
        results.append(pass_result(GROUP, "exploratory_manifests_valid", "Exploratory manifests validate."))
    if exploratory_manifests and not any(
        result.check_name == "exploratory_flags_false" and result.is_failure for result in results
    ):
        results.append(pass_result(GROUP, "exploratory_flags_false", "Exploratory manifests disable execution."))
    if exploratory_manifests and not any(
        result.check_name == "exploratory_candidate_bound" and result.is_failure for result in results
    ):
        results.append(pass_result(GROUP, "exploratory_candidate_bound", "Exploratory estimates fit bounds."))

    execution_manifests = sorted(cpu_execution_manifest_dir.glob("*.yaml"))
    blocked_expected = 0
    for manifest in execution_manifests:
        expected_failure = "expected_validation_status: fail" in manifest.read_text(encoding="utf-8")
        try:
            loaded = load_cpu_execution_manifest(manifest)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            if expected_failure:
                blocked_expected += 1
                results.append(
                    pass_result(
                        GROUP,
                        "cpu_execution_blocked_manifest_fails",
                        "Blocked CPU execution manifest fails as expected.",
                        path=manifest,
                    )
                )
                continue
            results.append(fail_result(GROUP, "cpu_execution_manifest_valid", str(exc), path=manifest))
            continue
        if expected_failure:
            results.append(
                fail_result(
                    GROUP,
                    "cpu_execution_blocked_manifest_fails",
                    "Blocked CPU execution manifest unexpectedly validates.",
                    path=manifest,
                )
            )
            continue
        results.append(pass_result(GROUP, "cpu_execution_manifest_valid", "CPU execution manifest validates.", path=manifest))
        _check_cpu_execution_flags(results, loaded.payload, manifest)
        if not _no_raw_dump(manifest):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Manifest appears to include raw data.", path=manifest))

    if execution_manifests and not any(
        result.check_name == "cpu_execution_manifest_valid" and result.is_failure for result in results
    ):
        results.append(pass_result(GROUP, "cpu_execution_manifests_valid", "Safe CPU execution manifests validate."))
    if blocked_expected:
        results.append(
            pass_result(
                GROUP,
                "cpu_execution_blocked_manifest_present",
                "Blocked unsolved CPU execution negative manifest is present.",
            )
        )
    if execution_manifests and not any(
        result.check_name == "cpu_execution_flags_false" and result.is_failure for result in results
    ):
        results.append(pass_result(GROUP, "cpu_execution_flags_false", "CPU execution manifests disable unsafe flags."))

    proposals = sorted(proposal_dir.glob("*.yaml"))
    for proposal in proposals:
        try:
            loaded = load_experiment_proposal(proposal)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "experiment_proposal_valid", str(exc), path=proposal))
            continue
        results.append(pass_result(GROUP, "experiment_proposal_valid", "Experiment proposal validates.", path=proposal))
        _check_proposal_flags(results, loaded.payload, proposal)
        corpus_slice = loaded.payload.get("corpus_slice", {})
        if (
            isinstance(corpus_slice, dict)
            and corpus_slice.get("slice_kind") == "future_unsolved_page_candidate"
            and loaded.payload.get("human_approval_required") is not True
        ):
            results.append(
                fail_result(
                    GROUP,
                    "proposal_human_approval_required",
                    "Future unsolved proposals require human approval.",
                    path=proposal,
                )
            )
        if not _no_raw_dump(proposal):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Proposal appears to include raw data.", path=proposal))

    approval_records = sorted(approval_record_dir.glob("*.yaml"))
    approved_records = 0
    for approval_record in approval_records:
        try:
            loaded = load_approval_record(approval_record)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "approval_record_valid", str(exc), path=approval_record))
            continue
        results.append(pass_result(GROUP, "approval_record_valid", "Approval record validates.", path=approval_record))
        if loaded.payload.get("approval_status") == "approved" or loaded.payload.get("approved_for_execution") is True:
            approved_records += 1
            results.append(
                fail_result(
                    GROUP,
                    "no_stage2g_approved_records",
                    "Stage 2G must not commit approved approval records.",
                    path=approval_record,
                )
            )

    if proposals and not any(result.check_name == "experiment_proposal_valid" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "experiment_proposals_valid", "Stage 2G proposals validate."))
    if proposals and not any(result.check_name == "proposal_flags_false" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "proposal_flags_false", "Stage 2G proposals remain unapproved and non-executable."))
    if proposals and not any(
        result.check_name == "proposal_human_approval_required" and result.is_failure for result in results
    ):
        results.append(pass_result(GROUP, "proposal_human_approval_required", "Future unsolved proposals require human approval."))
    if approval_records and approved_records == 0:
        results.append(pass_result(GROUP, "no_stage2g_approved_records", "No approved Stage 2G approval records are committed."))

    stage2h_proposals = sorted(
        path
        for path in stage2h_proposal_dir.glob("*.yaml")
        if not path.name.endswith("-request.yaml")
    )
    stage2h_requests = sorted(stage2h_proposal_dir.glob("*-request.yaml"))
    stage2h_approved_records = 0
    stage2h_approved_unsolved_records = 0
    stage2h_proposal_by_id: dict[str, Any] = {}
    for proposal in stage2h_proposals:
        try:
            loaded = load_experiment_proposal(proposal)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "stage2h_proposal_valid", str(exc), path=proposal))
            continue
        stage2h_proposal_by_id[loaded.proposal_id] = loaded.payload
        results.append(pass_result(GROUP, "stage2h_proposal_valid", "Stage 2H proposal validates.", path=proposal))
        _check_proposal_flags(results, loaded.payload, proposal)
        if not _no_raw_dump(proposal):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Proposal appears to include raw data.", path=proposal))

    for approval_record in sorted(stage2h_approval_record_dir.glob("*.yaml")):
        try:
            loaded = load_approval_record(approval_record)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "stage2h_approval_record_valid", str(exc), path=approval_record))
            continue
        results.append(pass_result(GROUP, "stage2h_approval_record_valid", "Stage 2H approval record validates.", path=approval_record))
        if loaded.payload.get("approval_status") == "approved" or loaded.payload.get("approved_for_execution") is True:
            stage2h_approved_records += 1
            proposal_payload = stage2h_proposal_by_id.get(str(loaded.payload.get("proposal_id")), {})
            corpus_slice = proposal_payload.get("corpus_slice", {}) if isinstance(proposal_payload, dict) else {}
            approval_scope = loaded.payload.get("approval_scope", {})
            safe_scope = isinstance(approval_scope, dict) and approval_scope.get("execution_scope") in {
                "synthetic_only",
                "solved_fixture_only",
                "synthetic_and_solved_fixture_only",
            }
            if (
                not safe_scope
                or not isinstance(corpus_slice, dict)
                or corpus_slice.get("slice_kind") == "future_unsolved_page_candidate"
            ):
                stage2h_approved_unsolved_records += 1
                results.append(
                    fail_result(
                        GROUP,
                        "stage2h_no_approved_unsolved_records",
                        "Stage 2H approved records must be synthetic or solved-control only.",
                        path=approval_record,
                    )
                )

    for request in stage2h_requests:
        try:
            loaded_request = load_approval_execution_request(request)
            gate = evaluate_approval_execution_gate(loaded_request)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "stage2h_request_valid", str(exc), path=request))
            continue
        results.append(pass_result(GROUP, "stage2h_request_valid", "Stage 2H request validates.", path=request))
        if loaded_request.payload.get("search_execution_enabled") is not False:
            results.append(fail_result(GROUP, "stage2h_request_flags_false", "search_execution_enabled must be false.", path=request))
        if loaded_request.payload.get("scoring_enabled") is not False:
            results.append(fail_result(GROUP, "stage2h_request_flags_false", "scoring_enabled must be false.", path=request))
        if loaded_request.payload.get("cuda_enabled") is not False:
            results.append(fail_result(GROUP, "stage2h_request_flags_false", "cuda_enabled must be false.", path=request))
        if loaded_request.payload.get("unsolved_execution_allowed") is not False:
            results.append(fail_result(GROUP, "stage2h_request_flags_false", "unsolved_execution_allowed must be false.", path=request))
        if loaded_request.execution_scope == "no_op_review_only" and gate.approval_gate_status != "blocked":
            results.append(fail_result(GROUP, "stage2h_noop_real_blocked", "No-op real request must remain blocked.", path=request))

    if stage2h_proposals and not any(result.check_name == "stage2h_proposal_valid" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2h_proposals_valid", "Stage 2H proposals validate."))
    if stage2h_requests and not any(result.check_name == "stage2h_request_valid" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2h_requests_valid", "Stage 2H requests validate."))
    if stage2h_requests and not any(result.check_name == "stage2h_request_flags_false" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2h_request_flags_false", "Stage 2H requests keep unsafe flags false."))
    if stage2h_approved_records and stage2h_approved_unsolved_records == 0:
        results.append(
            pass_result(
                GROUP,
                "stage2h_no_approved_unsolved_records",
                "Stage 2H approved records are limited to synthetic or solved controls.",
            )
        )
    if stage2h_requests and not any(result.check_name == "stage2h_noop_real_blocked" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2h_noop_real_blocked", "Stage 2H no-op real request remains blocked."))

    stage2i_proposals = sorted(stage2i_proposal_dir.glob("*.yaml"))
    stage2i_approval_records = sorted(stage2i_approval_record_dir.glob("*.yaml"))
    stage2i_proposal_by_id: dict[str, Any] = {}
    for proposal in stage2i_proposals:
        try:
            loaded = load_experiment_proposal(proposal)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "stage2i_proposal_valid", str(exc), path=proposal))
            continue
        stage2i_proposal_by_id[loaded.proposal_id] = loaded.payload
        results.append(pass_result(GROUP, "stage2i_proposal_valid", "Stage 2I proposal validates.", path=proposal))
        _check_proposal_flags(results, loaded.payload, proposal)
        corpus_slice = loaded.payload.get("corpus_slice", {})
        if not isinstance(corpus_slice, dict) or corpus_slice.get("slice_kind") != "future_unsolved_page_candidate":
            results.append(
                fail_result(
                    GROUP,
                    "stage2i_future_unsolved_metadata",
                    "Stage 2I proposal must touch reviewable unsolved metadata.",
                    path=proposal,
                )
            )
        if isinstance(corpus_slice, dict) and corpus_slice.get("review_required") is not True:
            results.append(
                fail_result(
                    GROUP,
                    "stage2i_future_unsolved_metadata",
                    "Stage 2I proposal requires review_required=true.",
                    path=proposal,
                )
            )
        if loaded.payload.get("candidate_count_estimate") != 841 or loaded.payload.get("candidate_count_upper_bound") != 841:
            results.append(fail_result(GROUP, "stage2i_candidate_bound", "Stage 2I candidate bound must be 841.", path=proposal))
        if not _no_raw_dump(proposal):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Stage 2I proposal appears to include raw data.", path=proposal))

    approved_stage2i_records = 0
    for approval_record in stage2i_approval_records:
        try:
            loaded = load_approval_record(approval_record)
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "stage2i_approval_record_valid", str(exc), path=approval_record))
            continue
        results.append(pass_result(GROUP, "stage2i_approval_record_valid", "Stage 2I approval record validates.", path=approval_record))
        if loaded.payload.get("approval_status") == "approved" or loaded.payload.get("approved_for_execution") is True:
            approved_stage2i_records += 1
            results.append(
                fail_result(
                    GROUP,
                    "stage2i_no_approved_records",
                    "Stage 2I must not commit approved approval records.",
                    path=approval_record,
                )
            )
        proposal_payload = stage2i_proposal_by_id.get(str(loaded.payload.get("proposal_id")))
        if proposal_payload is not None and loaded.payload.get("proposal_sha256"):
            proposal_path = stage2i_proposal_dir / f"{loaded.payload['proposal_id']}.yaml"
            if proposal_path.is_file() and loaded.payload.get("proposal_sha256") != compute_sha256(proposal_path):
                results.append(fail_result(GROUP, "stage2i_approval_sha", "Stage 2I approval SHA mismatch.", path=approval_record))

    if stage2i_proposals and stage2i_approval_records:
        try:
            analyze_approval_readiness(stage2i_proposals[0], approval_path=stage2i_approval_records[0])
            results.append(pass_result(GROUP, "stage2i_readiness_analyzes", "Stage 2I readiness analyzer accepts proposal."))
        except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
            results.append(fail_result(GROUP, "stage2i_readiness_analyzes", str(exc), path=stage2i_proposals[0]))

    if stage2i_proposals and not any(result.check_name == "stage2i_proposal_valid" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2i_proposals_valid", "Stage 2I proposals validate."))
    if stage2i_approval_records and approved_stage2i_records == 0:
        results.append(pass_result(GROUP, "stage2i_no_approved_records", "No Stage 2I approved approval records are committed."))
    if stage2i_proposals and not any(result.check_name == "stage2i_future_unsolved_metadata" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2i_future_unsolved_metadata", "Stage 2I proposal references reviewable unsolved metadata."))
    if stage2i_proposals and not any(result.check_name == "stage2i_candidate_bound" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "stage2i_candidate_bound", "Stage 2I candidate bound is 841."))

    try:
        policy = load_operator_policy(operator_policy_path)
        results.append(pass_result(GROUP, "operator_policy_valid", "Stage 2J operator policy validates.", path=operator_policy_path))
    except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
        policy = None
        results.append(fail_result(GROUP, "operator_policy_valid", str(exc), path=operator_policy_path))

    try:
        queue = load_bounded_queue(bounded_queue_path)
        results.append(pass_result(GROUP, "bounded_queue_valid", "Stage 2J bounded queue validates.", path=bounded_queue_path))
    except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
        queue = None
        results.append(fail_result(GROUP, "bounded_queue_valid", str(exc), path=bounded_queue_path))

    if policy is not None and queue is not None:
        checks = check_queue(policy, queue)
        pass_or_warning = {check.item_id for check in checks if not check.blocking_reasons}
        blocked = {check.item_id for check in checks if check.blocking_reasons}
        if "stage2j-caesar-affine-first-reviewable-slice" in pass_or_warning:
            results.append(pass_result(GROUP, "stage2j_first_item_policy_pass", "Stage 2J first item passes policy."))
        else:
            results.append(fail_result(GROUP, "stage2j_first_item_policy_pass", "Stage 2J first item does not pass policy."))
        if "stage2j-solved-baseline-regression-control" in pass_or_warning:
            results.append(pass_result(GROUP, "stage2j_control_policy_pass", "Stage 2J solved control passes policy."))
        else:
            results.append(fail_result(GROUP, "stage2j_control_policy_pass", "Stage 2J solved control does not pass policy."))
        if "stage2j-blocked-overbudget-example" in blocked:
            results.append(pass_result(GROUP, "stage2j_overbudget_blocked", "Stage 2J over-budget item is blocked."))
        else:
            results.append(fail_result(GROUP, "stage2j_overbudget_blocked", "Stage 2J over-budget item was not blocked."))
        for item in queue.items:
            if not _no_raw_dump(Path(queue.path)):
                results.append(fail_result(GROUP, "manifest_no_raw_dump", "Stage 2J queue appears to include raw data.", path=bounded_queue_path))
            if item.get("cuda_enabled") is not False:
                results.append(fail_result(GROUP, "stage2j_flags_false", "Queue item enables CUDA.", path=bounded_queue_path))
            if item.get("no_solve_claim") is not True:
                results.append(fail_result(GROUP, "stage2j_flags_false", "Queue item lacks no_solve_claim=true.", path=bounded_queue_path))
        if not any(result.check_name == "stage2j_flags_false" and result.is_failure for result in results):
            results.append(pass_result(GROUP, "stage2j_flags_false", "Stage 2J queue keeps unsafe flags false."))
    try:
        stage3b_queue = load_bounded_queue(stage3b_bounded_queue_path)
        results.append(
            pass_result(GROUP, "stage3b_queue_valid", "Stage 3B bounded queue validates.", path=stage3b_bounded_queue_path)
        )
    except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
        stage3b_queue = None
        results.append(fail_result(GROUP, "stage3b_queue_valid", str(exc), path=stage3b_bounded_queue_path))

    if policy is not None and stage3b_queue is not None:
        checks = check_queue(policy, stage3b_queue)
        pass_or_warning = {check.item_id for check in checks if not check.blocking_reasons}
        blocked = {check.item_id for check in checks if check.blocking_reasons}
        if "stage3b-caesar-affine-reverse-direction" in pass_or_warning:
            results.append(pass_result(GROUP, "stage3b_reverse_item_policy_pass", "Stage 3B reverse item passes policy."))
        else:
            results.append(fail_result(GROUP, "stage3b_reverse_item_policy_pass", "Stage 3B reverse item does not pass policy."))
        if "stage3b-stage3a-rerank-control" in pass_or_warning:
            results.append(pass_result(GROUP, "stage3b_rerank_policy_pass", "Stage 3B rerank control passes policy."))
        else:
            results.append(fail_result(GROUP, "stage3b_rerank_policy_pass", "Stage 3B rerank control does not pass policy."))
        if "stage3b-blocked-overbudget-control" in blocked:
            results.append(pass_result(GROUP, "stage3b_overbudget_blocked", "Stage 3B over-budget item is blocked."))
        else:
            results.append(fail_result(GROUP, "stage3b_overbudget_blocked", "Stage 3B over-budget item was not blocked."))
        for item in stage3b_queue.items:
            if not _no_raw_dump(Path(stage3b_queue.path)):
                results.append(
                    fail_result(
                        GROUP,
                        "manifest_no_raw_dump",
                        "Stage 3B queue appears to include raw data.",
                        path=stage3b_bounded_queue_path,
                    )
                )
            if item.get("cuda_enabled") is not False:
                results.append(fail_result(GROUP, "stage3b_flags_false", "Queue item enables CUDA.", path=stage3b_bounded_queue_path))
            if item.get("no_solve_claim") is not True:
                results.append(
                    fail_result(GROUP, "stage3b_flags_false", "Queue item lacks no_solve_claim=true.", path=stage3b_bounded_queue_path)
                )
        if not any(result.check_name == "stage3b_flags_false" and result.is_failure for result in results):
            results.append(pass_result(GROUP, "stage3b_flags_false", "Stage 3B queue keeps unsafe flags false."))
    try:
        stage3c_queue = load_bounded_queue(stage3c_bounded_queue_path)
        results.append(
            pass_result(GROUP, "stage3c_queue_valid", "Stage 3C bounded queue validates.", path=stage3c_bounded_queue_path)
        )
    except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
        stage3c_queue = None
        results.append(fail_result(GROUP, "stage3c_queue_valid", str(exc), path=stage3c_bounded_queue_path))

    if policy is not None and stage3c_queue is not None:
        checks = check_queue(policy, stage3c_queue)
        pass_or_warning = {check.item_id for check in checks if not check.blocking_reasons}
        blocked = {check.item_id for check in checks if check.blocking_reasons}
        if "stage3c-small-vigenere-known-motif-key-list" in pass_or_warning:
            results.append(pass_result(GROUP, "stage3c_next_item_policy_pass", "Stage 3C next item passes policy."))
        else:
            results.append(fail_result(GROUP, "stage3c_next_item_policy_pass", "Stage 3C next item does not pass policy."))
        if "stage3c-blocked-overbudget-control" in blocked:
            results.append(pass_result(GROUP, "stage3c_overbudget_blocked", "Stage 3C over-budget item is blocked."))
        else:
            results.append(fail_result(GROUP, "stage3c_overbudget_blocked", "Stage 3C over-budget item was not blocked."))
        for item in stage3c_queue.items:
            if not _no_raw_dump(Path(stage3c_queue.path)):
                results.append(
                    fail_result(
                        GROUP,
                        "manifest_no_raw_dump",
                        "Stage 3C queue appears to include raw data.",
                        path=stage3c_bounded_queue_path,
                    )
                )
            if item.get("cuda_enabled") is not False:
                results.append(fail_result(GROUP, "stage3c_flags_false", "Queue item enables CUDA.", path=stage3c_bounded_queue_path))
            if item.get("no_solve_claim") is not True:
                results.append(
                    fail_result(GROUP, "stage3c_flags_false", "Queue item lacks no_solve_claim=true.", path=stage3c_bounded_queue_path)
                )
        if not any(result.check_name == "stage3c_flags_false" and result.is_failure for result in results):
            results.append(pass_result(GROUP, "stage3c_flags_false", "Stage 3C queue keeps unsafe flags false."))

    try:
        stage3e_backlog = load_method_backlog(stage3e_method_backlog_path)
        results.append(
            pass_result(
                GROUP,
                "stage3e_method_backlog_valid",
                "Stage 3E method backlog validates.",
                path=stage3e_method_backlog_path,
            )
        )
    except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
        stage3e_backlog = None
        results.append(fail_result(GROUP, "stage3e_method_backlog_valid", str(exc), path=stage3e_method_backlog_path))

    try:
        stage3e_queue = load_bounded_queue(stage3e_bounded_queue_path)
        results.append(
            pass_result(GROUP, "stage3e_queue_valid", "Stage 3E bounded queue validates.", path=stage3e_bounded_queue_path)
        )
    except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
        stage3e_queue = None
        results.append(fail_result(GROUP, "stage3e_queue_valid", str(exc), path=stage3e_bounded_queue_path))

    if stage3e_backlog is not None:
        if len(stage3e_backlog.items) >= 7:
            results.append(pass_result(GROUP, "stage3e_backlog_item_count", "Stage 3E backlog has at least seven items."))
        else:
            results.append(fail_result(GROUP, "stage3e_backlog_item_count", "Stage 3E backlog is missing items."))
        for item in stage3e_backlog.items:
            if item.get("cuda_enabled") is not False:
                results.append(fail_result(GROUP, "stage3e_backlog_flags_false", "Backlog item enables CUDA.", path=stage3e_method_backlog_path))
            if item.get("no_solve_claim") is not True:
                results.append(
                    fail_result(GROUP, "stage3e_backlog_flags_false", "Backlog item lacks no_solve_claim=true.", path=stage3e_method_backlog_path)
                )
        if not any(result.check_name == "stage3e_backlog_flags_false" and result.is_failure for result in results):
            results.append(pass_result(GROUP, "stage3e_backlog_flags_false", "Stage 3E backlog keeps unsafe flags false."))

    if policy is not None and stage3e_queue is not None:
        checks = check_queue(policy, stage3e_queue)
        blocked = [check for check in checks if check.blocking_reasons]
        if not blocked:
            results.append(pass_result(GROUP, "stage3e_policy_pass", "All Stage 3E queue items fit operator-policy limits."))
        else:
            for check in blocked:
                results.append(
                    fail_result(
                        GROUP,
                        "stage3e_policy_pass",
                        f"{check.item_id} has blocking reasons: {', '.join(check.blocking_reasons)}",
                        path=stage3e_bounded_queue_path,
                    )
                )
        expected_counts = {
            "stage3e_vig_lp_evidence_pack_v1": 48,
            "stage3e_prime_minus_one_offsets_v1": 256,
            "stage3e_vig_history_key_pack_v1": 56,
            "stage3e_negative_control_extension_v1": 100,
            "stage3e_reset_advance_ablation_v1": 64,
            "stage3e_prime_mod_gap_pack_v1": 256,
            "stage3i_mersenne_prime_stream_tiny_v1": 192,
        }
        support_statuses: dict[str, str] = {}
        for item in stage3e_queue.items:
            try:
                validate_stage3e_queue_item(item)
                calculated = validate_candidate_count(item)
            except Exception as exc:  # noqa: BLE001 - consistency reports collect validation failures.
                results.append(fail_result(GROUP, "stage3e_candidate_counts", str(exc), path=stage3e_bounded_queue_path))
                continue
            item_id = str(item.get("item_id"))
            expected = expected_counts.get(item_id)
            if calculated == expected:
                results.append(
                    pass_result(GROUP, "stage3e_candidate_counts", f"{item_id} count is {calculated}.", path=stage3e_bounded_queue_path)
                )
            else:
                results.append(
                    fail_result(
                        GROUP,
                        "stage3e_candidate_counts",
                        f"{item_id} count {calculated} does not match expected {expected}.",
                        path=stage3e_bounded_queue_path,
                    )
                )
            support_status, _support_reason = classify_executor_support(item)
            support_statuses[item_id] = support_status
            if item.get("cuda_enabled") is not False:
                results.append(fail_result(GROUP, "stage3e_flags_false", "Queue item enables CUDA.", path=stage3e_bounded_queue_path))
            if item.get("no_solve_claim") is not True:
                results.append(
                    fail_result(GROUP, "stage3e_flags_false", "Queue item lacks no_solve_claim=true.", path=stage3e_bounded_queue_path)
                )
            if item.get("canonical_corpus_active") is not False or item.get("page_boundaries_final") is not False:
                results.append(
                    fail_result(
                        GROUP,
                        "stage3e_flags_false",
                        "Queue item activates canonical corpus or final page boundaries.",
                        path=stage3e_bounded_queue_path,
                    )
                )
        if not _no_raw_dump(stage3e_bounded_queue_path):
            results.append(fail_result(GROUP, "manifest_no_raw_dump", "Stage 3E queue appears to include raw data.", path=stage3e_bounded_queue_path))
        if not any(result.check_name == "stage3e_candidate_counts" and result.is_failure for result in results):
            results.append(pass_result(GROUP, "stage3e_candidate_counts_verified", "Stage 3E deterministic candidate counts match."))
        if not any(result.check_name == "stage3e_flags_false" and result.is_failure for result in results):
            results.append(pass_result(GROUP, "stage3e_flags_false", "Stage 3E queue keeps unsafe flags false."))
        if (
            sum(1 for status in support_statuses.values() if status == "runnable_now") == 2
            and sum(1 for status in support_statuses.values() if status == "needs_executor") == 3
            and sum(
            1 for status in support_statuses.values() if status == "dry_run_only"
            )
            == 2
        ):
            results.append(pass_result(GROUP, "stage3e_executor_support", "Stage 3E executor support classification is deterministic."))
        else:
            results.append(fail_result(GROUP, "stage3e_executor_support", "Stage 3E executor support classification drifted."))
    return results


def _check_manifest_flags(results: list[ConsistencyCheckResult], payload: dict[str, Any], path: Path) -> None:
    for field in ["search_enabled", "cuda_enabled", "scoring_enabled", "canonical_corpus_active"]:
        if payload.get(field) is not False:
            results.append(fail_result(GROUP, "manifest_flags_false", f"{field} must be false.", path=path))


def _check_exploratory_flags(results: list[ConsistencyCheckResult], payload: dict[str, Any], path: Path) -> None:
    if payload.get("dry_run_only") is not True:
        results.append(fail_result(GROUP, "exploratory_flags_false", "dry_run_only must be true.", path=path))
    for field in [
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        if payload.get(field) is not False:
            results.append(fail_result(GROUP, "exploratory_flags_false", f"{field} must be false.", path=path))


def _check_cpu_execution_flags(results: list[ConsistencyCheckResult], payload: dict[str, Any], path: Path) -> None:
    if payload.get("execution_enabled") is not True:
        results.append(fail_result(GROUP, "cpu_execution_flags_false", "execution_enabled must be true.", path=path))
    if payload.get("execution_scope") not in {
        "synthetic_only",
        "solved_fixture_only",
        "synthetic_and_solved_fixture_only",
    }:
        results.append(fail_result(GROUP, "cpu_execution_flags_false", "execution_scope is unsafe.", path=path))
    for field in [
        "unsolved_execution_allowed",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        if payload.get(field) is not False:
            results.append(fail_result(GROUP, "cpu_execution_flags_false", f"{field} must be false.", path=path))


def _check_proposal_flags(results: list[ConsistencyCheckResult], payload: dict[str, Any], path: Path) -> None:
    if payload.get("human_approval_required") is not True:
        results.append(fail_result(GROUP, "proposal_flags_false", "human_approval_required must be true.", path=path))
    for field in [
        "approved_for_execution",
        "execution_enabled",
        "search_execution_enabled",
        "candidate_generation_enabled",
        "scoring_enabled",
        "cuda_enabled",
        "canonical_corpus_active",
        "page_boundaries_final",
        "trusted_as_canonical",
    ]:
        if payload.get(field) is not False:
            results.append(fail_result(GROUP, "proposal_flags_false", f"{field} must be false.", path=path))
