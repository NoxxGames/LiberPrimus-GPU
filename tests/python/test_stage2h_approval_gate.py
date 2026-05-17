from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import yaml

from libreprimus.approval_execution.approval_gate import evaluate_approval_execution_gate
from libreprimus.approval_execution.request_loader import load_approval_execution_request
from libreprimus.transforms.registry import compute_sha256

REPO = Path(__file__).resolve().parents[2]
STAGE2H = REPO / "experiments/proposals/stage2h"
SYNTHETIC_REQUEST = STAGE2H / "stage2h-approved-synthetic-direct-request.yaml"
SOLVED_REQUEST = STAGE2H / "stage2h-approved-solved-fixture-replay-request.yaml"
NOOP_REQUEST = STAGE2H / "stage2h-noop-real-request.yaml"
SYNTHETIC_APPROVAL = STAGE2H / "approval-records/stage2h-approved-synthetic-direct-approval.yaml"


def test_approved_synthetic_record_passes() -> None:
    gate = evaluate_approval_execution_gate(load_approval_execution_request(SYNTHETIC_REQUEST))

    assert gate.approval_gate_status == "pass"
    assert gate.approved_for_execution is True


def test_approved_solved_fixture_replay_record_passes() -> None:
    gate = evaluate_approval_execution_gate(load_approval_execution_request(SOLVED_REQUEST))

    assert gate.approval_gate_status == "pass"
    assert gate.approved_for_execution is True


def test_pending_approval_blocks() -> None:
    gate = evaluate_approval_execution_gate(load_approval_execution_request(NOOP_REQUEST))

    assert gate.approval_gate_status == "blocked"
    assert gate.approved_for_execution is False


def test_denied_approval_blocks(tmp_path: Path) -> None:
    request_path = _request_with_approval_status(tmp_path, "denied")
    gate = evaluate_approval_execution_gate(load_approval_execution_request(request_path))

    assert gate.approval_gate_status == "blocked"


def test_expired_approval_blocks(tmp_path: Path) -> None:
    request_path = _request_with_approval_status(tmp_path, "approved", expiry_utc="2001-01-01T00:00:00Z")
    gate = evaluate_approval_execution_gate(load_approval_execution_request(request_path))

    assert gate.approval_gate_status == "blocked"
    assert any("expired" in reason for reason in gate.blocking_reasons)


def test_mismatched_proposal_sha_blocks(tmp_path: Path) -> None:
    request_path = _request_with_approval_status(tmp_path, "approved", proposal_sha256="0" * 64)
    gate = evaluate_approval_execution_gate(load_approval_execution_request(request_path))

    assert gate.approval_gate_status == "blocked"
    assert any("proposal_sha256" in reason for reason in gate.blocking_reasons)


def test_wrong_scope_blocks(tmp_path: Path) -> None:
    request_path = _request_with_approval_status(tmp_path, "approved", execution_scope="solved_fixture_only")
    gate = evaluate_approval_execution_gate(load_approval_execution_request(request_path))

    assert gate.approval_gate_status == "blocked"
    assert any("scope" in reason.lower() for reason in gate.blocking_reasons)


def test_future_unsolved_page_candidate_blocks_even_with_approved_record(tmp_path: Path) -> None:
    proposal = yaml.safe_load((STAGE2H / "stage2h-noop-real-proposal.yaml").read_text(encoding="utf-8"))
    proposal["proposal_id"] = "stage2h-unit-unsolved-synthetic-scope"
    proposal["execution_scope"] = "synthetic_only"
    proposal["execution_manifest_path"] = "experiments/manifests/cpu-execution/stage2f-synthetic-direct-execution.yaml"
    proposal["review_checklist"]["proposal_id"] = proposal["proposal_id"]
    proposal["review_checklist"]["checklist_id"] = "stage2h-unit-unsolved-checklist"
    proposal_path = tmp_path / "unsolved-proposal.yaml"
    proposal_path.write_text(yaml.safe_dump(proposal, sort_keys=False), encoding="utf-8")

    approval = yaml.safe_load(SYNTHETIC_APPROVAL.read_text(encoding="utf-8"))
    approval.update(
        {
            "approval_id": "stage2h-unit-unsolved-approval",
            "proposal_id": proposal["proposal_id"],
            "proposal_sha256": compute_sha256(proposal_path),
            "approval_scope": {"proposal_id": proposal["proposal_id"], "execution_scope": "synthetic_only"},
        }
    )
    approval_path = tmp_path / "approval.yaml"
    approval_path.write_text(yaml.safe_dump(approval, sort_keys=False), encoding="utf-8")
    request = yaml.safe_load(SYNTHETIC_REQUEST.read_text(encoding="utf-8"))
    request.update(
        {
            "request_id": "stage2h-unit-unsolved-request",
            "proposal_path": str(proposal_path),
            "approval_record_path": str(approval_path),
        }
    )
    request_path = tmp_path / "request.yaml"
    request_path.write_text(yaml.safe_dump(request, sort_keys=False), encoding="utf-8")

    gate = evaluate_approval_execution_gate(load_approval_execution_request(request_path))

    assert gate.approval_gate_status == "blocked"
    assert any("Future unsolved" in reason for reason in gate.blocking_reasons)


def _request_with_approval_status(
    tmp_path: Path,
    status: str,
    *,
    expiry_utc: str = "2099-01-01T00:00:00Z",
    proposal_sha256: str | None = None,
    execution_scope: str = "synthetic_only",
) -> Path:
    proposal_path = STAGE2H / "stage2h-approved-synthetic-direct-proposal.yaml"
    approval = deepcopy(yaml.safe_load(SYNTHETIC_APPROVAL.read_text(encoding="utf-8")))
    approval.update(
        {
            "approval_id": f"unit-{status}-approval",
            "approval_status": status,
            "approved_for_execution": status == "approved",
            "proposal_sha256": proposal_sha256 or compute_sha256(proposal_path),
            "approval_scope": {
                "proposal_id": approval["proposal_id"],
                "execution_scope": execution_scope,
            },
            "expiry_utc": expiry_utc if status == "approved" else "",
        }
    )
    if status != "approved":
        approval["approved_by"] = ""
        approval["approved_at_utc"] = ""
        approval["constraints"] = []
    approval_path = tmp_path / f"{status}-approval.yaml"
    approval_path.write_text(yaml.safe_dump(approval, sort_keys=False), encoding="utf-8")

    request = yaml.safe_load(SYNTHETIC_REQUEST.read_text(encoding="utf-8"))
    request["approval_record_path"] = str(approval_path)
    request_path = tmp_path / f"{status}-request.yaml"
    request_path.write_text(yaml.safe_dump(request, sort_keys=False), encoding="utf-8")
    return request_path
