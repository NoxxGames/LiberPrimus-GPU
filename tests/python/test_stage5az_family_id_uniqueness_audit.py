from pathlib import Path

import yaml


def test_stage5az_detects_and_repairs_duplicate_family_id() -> None:
    stage5ay = yaml.safe_load(
        Path("data/token-block/stage5ay-bounded-variant-family-manifest.yaml").read_text(encoding="utf-8")
    )
    audit = yaml.safe_load(
        Path("data/token-block/stage5az-family-id-uniqueness-audit.yaml").read_text(encoding="utf-8")
    )

    ids = [record["family_id"] for record in stage5ay["families"]]
    assert ids.count("unresolved_as_current_only") == 2
    assert audit["duplicate_family_id_count_before_repair"] == 1
    assert audit["duplicate_family_id_count_after_repair"] == 0
    assert audit["known_duplicate_family_id_found"] is True
