from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.validation import validate_operator_policy_payload

REPO = Path(__file__).resolve().parents[2]
POLICY = REPO / "experiments/policies/operator-policy-v0.yaml"


def test_operator_policy_validates() -> None:
    policy = load_operator_policy(POLICY)

    assert policy.policy_id == "operator-policy-v0"
    assert policy.max_candidate_count == 100000
    assert policy.max_estimated_runtime_seconds == 600
    assert policy.max_generated_output_mb == 250


def test_operator_policy_blocks_over_limit_policy() -> None:
    payload = yaml.safe_load(POLICY.read_text(encoding="utf-8"))
    payload["limits"]["max_candidate_count"] = 100001

    with pytest.raises(ValueError, match="max_candidate_count"):
        validate_operator_policy_payload(payload)
