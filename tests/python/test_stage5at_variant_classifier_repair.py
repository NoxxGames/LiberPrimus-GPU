from pathlib import Path

import yaml

from libreprimus.token_block.original_images import classify_variant
from libreprimus.token_block.models import sha256_file


def test_stage5at_variant_classifier_treats_unmodified_copy_as_original(tmp_path: Path) -> None:
    path = tmp_path / "A drop box of all unmodified files" / "49.jpg"
    path.parent.mkdir()
    path.write_bytes(b"synthetic image bytes for hash-equality classification")
    selected_hashes = {49: sha256_file(path)}

    variant_class, _, allowed = classify_variant(path, selected_hashes)

    assert variant_class == "byte_identical_original_copy"
    assert allowed is True


def test_stage5at_variant_repair_summary_passed() -> None:
    payload = yaml.safe_load(Path("data/token-block/stage5at-variant-classifier-repair-summary.yaml").read_text())
    assert payload["variant_classifier_repaired"] is True
    assert payload["unmodified_path_bug_test_passed"] is True
    assert payload["modified_path_hash_diff_forbidden"] is True
