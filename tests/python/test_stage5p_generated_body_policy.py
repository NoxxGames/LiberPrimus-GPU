from __future__ import annotations

from pathlib import Path

from libreprimus.gematria_cuda_result_store.generated_body_policy import build_generated_body_policy


def test_stage5p_generated_body_policy_blocks_publication(tmp_path: Path) -> None:
    records = build_generated_body_policy(
        generated_body_policy_out=tmp_path / "generated-body-policy.yaml",
        out_dir=tmp_path,
    )

    assert len(records) == 4
    assert all(record["compact_metadata_allowed"] is True for record in records)
    assert all(record["body_publication_allowed"] is False for record in records)
    assert all(record["generated_body_publication_allowed"] is False for record in records)
    assert all(record["generated_outputs_committed"] is False for record in records)


def test_stage5p_generated_body_policy_covers_codex_output_and_sqlite(tmp_path: Path) -> None:
    records = build_generated_body_policy(
        generated_body_policy_out=tmp_path / "generated-body-policy.yaml",
        out_dir=tmp_path,
    )
    classes = {record["artifact_class"] for record in records}

    assert "codex_completion_handoff" in classes
    assert "raw_sqlite_and_local_reports" in classes
