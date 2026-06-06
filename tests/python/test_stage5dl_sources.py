from __future__ import annotations

import pytest

from libreprimus.token_block import stage5dl
from test_stage5dl_common import ensure_stage5dl_built, load_yaml


def test_stage5dl_requires_stage5dk_predecessor(monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
    monkeypatch.setitem(stage5dl.STAGE5DK_DATA_PATHS, "summary", tmp_path / "missing.yaml")

    with pytest.raises(FileNotFoundError):
        stage5dl.build_stage5dl(write_completion=False)


def test_stage5dl_records_number_triangle_aliases_and_v2_path() -> None:
    ensure_stage5dl_built()
    record = load_yaml("data/project-state/stage5dl-local-source-path-aliases.yaml")
    rows = {row["alias_id"]: row for row in record["path_aliases"]}

    assert rows["number_triangle_primary"]["path"] == "third_party/NumberTriangleStuff"
    assert rows["number_triangle_primary"]["exists_locally"] is True
    assert rows["number_triangle_primary"]["preferred_for_stage5dl"] is True
    assert rows["number_triangle_primary_content_root"]["path"].endswith("v2-number-triangles")
    assert rows["number_triangle_legacy_usefulfiles"]["superseded_by"] == "third_party/NumberTriangleStuff"


def test_stage5dl_records_reddit_url_image_pairs() -> None:
    ensure_stage5dl_built()
    record = load_yaml(
        "data/source-harvester/stage5dl-reddit-thread-image-source-lock-register.yaml"
    )
    rows = {row["reddit_folder"]: row for row in record["reddit_folders"]}

    assert set(rows) == {"FibonacciSequence", "PrimeGPSums", "Layered_primes"}
    for row in rows.values():
        assert row["url_txt_exists"] is True
        assert row["image_exists"] is True
        assert row["url"].startswith("http")
        assert row["network_fetch_performed"] is False
        assert row["raw_reddit_images_committed"] is False


def test_stage5dl_disk_cipher_metadata_does_not_execute_html() -> None:
    ensure_stage5dl_built()
    record = load_yaml("data/historical-route/stage5dl-disk-alberti-branch-source-lock.yaml")

    assert record["source_root"] == "third_party/DiskCipherStuff"
    assert record["html_tool_execution_performed_now"] is False
    assert record["html_execution_performed"] is False
    assert record["disk_cipher_experiment_executed"] is False
    assert record["manual_branching_false_positive_risk"] == "high"
    assert record["requires_programmatic_reproduction_before_experiment"] is True


def test_stage5dl_source_digest_records_metadata_only() -> None:
    ensure_stage5dl_built()
    record = load_yaml("data/project-state/stage5dl-source-digest-index.yaml")

    assert record["source_file_count"] > 0
    assert record["raw_files_committed"] is False
    assert record["generated_outputs_committed"] is False
    assert all(row["raw_file_committed"] is False for row in record["source_file_records"])
