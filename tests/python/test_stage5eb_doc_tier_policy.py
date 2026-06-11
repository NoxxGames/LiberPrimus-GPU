from __future__ import annotations

from test_stage5eb_common import ensure_stage5eb_built, load_yaml


def test_stage5eb_doc_ledger_tier_policy_limits_latest_stage_requirements() -> None:
    ensure_stage5eb_built()

    record = load_yaml("data/project-state/stage5eb-doc-ledger-tier-policy.yaml")

    assert record["tier_1_docs_required_latest_stage"] is True
    assert "STATUS.md" in record["tier_1_paths"]
    assert "docs/roadmap/staged-plan.md" in record["tier_1_paths"]
    assert record["tier_2_docs_required_only_if_domain_changed"] is True
    assert record["tier_3_docs_must_not_require_latest_stage"] is True
    assert record["broad_docs_can_defer_to_current_stage_registry"] is True
