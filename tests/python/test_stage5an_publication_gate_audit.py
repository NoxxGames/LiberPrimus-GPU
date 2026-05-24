from __future__ import annotations

from libreprimus.deep_research_export.publication_gates import build_publication_gate_audit


def test_publication_gate_audit_preserves_private_statuses() -> None:
    audit = build_publication_gate_audit(
        gate_records=[{"gate_id": "gate"}],
        included_files=[
            {"publication_status": "private_deep_research_only"},
            {"publication_status": "blocked_private_or_sensitive"},
        ],
        excluded_records=[{"path": "raw.zip", "reason": "forbidden_raw_or_binary_extension"}],
    )
    assert audit["publication_gate_audit_passed"] is True
    assert audit["public_website_publication_performed"] is False
    assert audit["private_deep_research_only_count"] == 1
    assert audit["excluded_forbidden_file_count"] == 1
