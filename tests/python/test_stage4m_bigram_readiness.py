from __future__ import annotations

from PIL import Image

from libreprimus.image_preflight.bigram_readiness import build_bigram_readiness_record
from libreprimus.image_preflight.models import BIGRAM_BLOCKERS


def test_stage4m_bigram_readiness_remains_blocked_with_synthetic_image(tmp_path) -> None:
    image = tmp_path / "Fib421.jpg"
    Image.new("RGB", (8, 8), (1, 2, 3)).save(image)
    manifest = [
        {
            "manifest_readiness_id": "stage4l-manifest-readiness-exp_stage4m_bigram_diagonal_fibonacci_421_audit",
            "future_manifest_id": "exp_stage4m_bigram_diagonal_fibonacci_421_audit",
            "ready_state": "blocked",
        }
    ]
    promotion = [{"observation_id": "stage4l-bigram-diagonal-fibonacci-421-claim", "readiness_record_id": "r1"}]

    record = build_bigram_readiness_record(
        manifest_readiness_records=manifest,
        promotion_readiness_records=promotion,
        bigram_image=image,
        repo_root=tmp_path,
        allow_missing_bigram_image=False,
    )

    assert record["ready_state"] == "blocked"
    assert record["matrix_regenerated"] is False
    assert record["frequency_pattern_experiment_executed"] is False
    assert set(BIGRAM_BLOCKERS).issubset(record["blockers"])
    assert record["bigram_image_present"] is True
