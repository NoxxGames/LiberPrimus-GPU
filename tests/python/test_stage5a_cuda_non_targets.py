from __future__ import annotations

from libreprimus.cuda_planning.non_targets import build_non_target_records


def test_stage5a_non_targets_cover_required_boundaries() -> None:
    records = build_non_target_records()
    text = " ".join(
        f"{record['non_target_id']} {record['name']} {record['reason']}".lower()
        for record in records
    )
    for term in ("discord", "image", "stego", "audio", "cookie", "hash", "bigram", "website"):
        assert term in text
    assert all(record["target_status"] == "non_cuda_target" for record in records)
