from __future__ import annotations

from pathlib import Path

from libreprimus.operator_console.source_browser.normalizer import normalize_record
from test_stage5dv_common import ensure_stage5dv_built, load_yaml


def _paths(raw: dict[str, object]) -> list[str]:
    return normalize_record(Path("data/test-stage5dv.yaml"), raw).local_paths


def test_file_name_with_relative_path_produces_only_relative_path() -> None:
    paths = _paths(
        {
            "record_type": "stage5dv_test_record",
            "file_name": "0.png",
            "relative_path": "third_party/BigGapsFoundInLiberPrimus/0.png",
        }
    )
    assert "third_party/BigGapsFoundInLiberPrimus/0.png" in paths
    assert "0.png" not in paths


def test_label_only_bare_image_filename_is_not_root_path() -> None:
    paths = _paths(
        {
            "record_type": "stage5dv_test_record",
            "title": "a famous book.png",
            "description": "coincidence for me_01.png",
            "notes": "results.png",
        }
    )
    assert paths == []


def test_source_root_relative_source_images_are_resolved() -> None:
    paths = _paths(
        {
            "record_type": "stage5dv_test_record",
            "source_root": "third_party/NumberFactsCollection",
            "source_images": ["google_doc_1.png"],
        }
    )
    assert paths == ["third_party/NumberFactsCollection/google_doc_1.png"]


def test_source_images_without_source_root_do_not_become_root_paths() -> None:
    paths = _paths(
        {
            "record_type": "stage5dv_test_record",
            "source_images": ["google_doc_1.png", "messages.txt"],
        }
    )
    assert "google_doc_1.png" not in paths
    assert "messages.txt" not in paths


def test_stage5dv_path_policy_records_required_aliases() -> None:
    ensure_stage5dv_built()
    policy = load_yaml("data/operator-console/source-browser/path-canonicalization-policy.yaml")
    assert policy["bare_filename_default"] == "label_not_root_path"
    assert "third_party/CiadaSolversIddqd_v2/liber-primus__images--full" in policy[
        "required_alias_roots"
    ]
