from __future__ import annotations

from pathlib import Path

from libreprimus.discord_review.review_index import write_review_index


def test_review_index_generated(tmp_path: Path) -> None:
    path = write_review_index(
        out_dir=tmp_path,
        shard_records=[
            {
                "topic": "source-links-and-datasets",
                "lead_count": 1,
                "output_relative_path": "experiments/results/discord-review-bundles/stage3q/topic_shards/source-links-and-datasets.md",
            }
        ],
        summary={"review_lead_count": 1, "topic_shard_count": 1},
    )

    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "Raw logs" in text
    assert "source-links-and-datasets" in text
