from pathlib import Path

import yaml


def test_stage5bb_legacy_pointer_audit_replaces_stage5ay_variant_family_pointer() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5bb-legacy-pointer-audit.yaml").read_text())

    assert payload["legacy_pointer_count"] in {0, 1}
    assert payload["active_loader_target"] == "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml"
    if payload["legacy_pointer_count"]:
        pointer = payload["legacy_pointers_detected"][0]
        assert pointer["classification"] == "legacy_superseded_pointer"
        assert pointer["legacy_path"] == "data/token-block/stage5ay-bounded-variant-family-manifest.yaml"
        assert pointer["stale_active_load_allowed"] is False
