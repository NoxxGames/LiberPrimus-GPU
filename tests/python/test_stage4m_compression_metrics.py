from __future__ import annotations

from PIL import Image

from libreprimus.image_preflight.compression_metrics import build_compression_records
from libreprimus.image_preflight.metadata import build_metadata_records


def test_stage4m_compression_metrics_deterministic_and_metric_only(tmp_path) -> None:
    image_dir = tmp_path / "images"
    image_dir.mkdir()
    image_path = image_dir / "sample.jpg"
    Image.new("RGB", (16, 16), (120, 130, 140)).save(image_path, quality=90)
    metadata = build_metadata_records(image_dir, repo_root=tmp_path)

    first = build_compression_records(metadata, repo_root=tmp_path)
    second = build_compression_records(metadata, repo_root=tmp_path)

    assert first == second
    assert first[0]["compression_metric_status"] == "computed"
    assert first[0]["metric_only"] is True
    assert first[0]["generated_image_committed"] is False
    assert "blockiness_proxy" in first[0]
