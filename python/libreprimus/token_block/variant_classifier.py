"""Stage 5AT image-variant classifier repair helpers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .models import STAGE5AT_ID, TOKEN_BLOCK_ID, read_yaml, write_json, write_yaml


def path_tokens(path: str) -> set[str]:
    return {token for token in re.split(r"[^a-z0-9]+", path.lower()) if token}


def classify_variant_metadata(*, source_path: str, sha256: str, page_number: int, selected_hashes: dict[int, str]) -> tuple[str, str, bool]:
    """Classify metadata with hash equality before path heuristics."""

    lower_path = source_path.lower()
    if page_number in selected_hashes and sha256 == selected_hashes[page_number]:
        if "liberprimuspages" in lower_path and Path(source_path).name.lower() == f"{page_number}.jpg":
            return "original_candidate", "original_liber_primus_page_image", True
        return "byte_identical_original_copy", "byte_identical_original_copy", True
    tokens = path_tokens(source_path)
    if any(term in lower_path for term in ("screenshot", "screen-shot", "capture")):
        return "derived_screenshot", "forbidden_supporting_only", False
    if any(term in lower_path for term in ("crop", "cropped")):
        return "crop", "forbidden_supporting_only", False
    if any(term in lower_path for term in ("annotated", "highlight", "overlay", "circled")):
        return "annotated_or_highlighted", "forbidden_supporting_only", False
    if "modified" in tokens or "composite" in tokens:
        return "modified_or_composite", "forbidden_supporting_only", False
    if lower_path.startswith(("website-export/", "research-inputs/", "deep-research-content-packs/")):
        return "private_content_generated", "forbidden_supporting_only", False
    if "the-complete-cicada3301-archive" in lower_path:
        return "near_original_variant", "original_archive_page_image", False
    return "unknown", "unknown", False


def build_variant_classifier_repair_summary(
    *,
    stage5ar_source_lock: Path,
    stage5ar_variants: Path,
    results_dir: Path,
    out: Path,
) -> dict[str, Any]:
    source = read_yaml(stage5ar_source_lock)
    variants = read_yaml(stage5ar_variants)
    selected_hashes = {int(record["page_number"]): record["sha256"] for record in source.get("records", [])}
    page_49_hash = selected_hashes[49]
    unmodified_class = classify_variant_metadata(
        source_path="A drop box of all unmodified files/49.jpg",
        sha256=page_49_hash,
        page_number=49,
        selected_hashes=selected_hashes,
    )
    modified_class = classify_variant_metadata(
        source_path="A drop box of modified files/49.jpg",
        sha256="0" * 64,
        page_number=49,
        selected_hashes=selected_hashes,
    )
    payload = {
        "record_type": "variant_classifier_repair_summary",
        "schema": "schemas/token-block/variant-classifier-repair-summary-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_variant_record_count": variants.get("variant_record_count", 0),
        "variant_classifier_repaired": True,
        "repair_rule": "hash_equality_precedes_tokenized_path_heuristics",
        "unmodified_path_bug_test_passed": unmodified_class[0] == "byte_identical_original_copy",
        "hash_equality_overrides_path_heuristics": unmodified_class[2] is True,
        "modified_path_hash_diff_forbidden": modified_class[0] == "modified_or_composite" and modified_class[2] is False,
        "unmodified_test": {
            "source_path": "A drop box of all unmodified files/49.jpg",
            "variant_class": unmodified_class[0],
            "coordinate_source_class": unmodified_class[1],
            "coordinate_truth_allowed": unmodified_class[2],
        },
        "modified_test": {
            "source_path": "A drop box of modified files/49.jpg",
            "variant_class": modified_class[0],
            "coordinate_source_class": modified_class[1],
            "coordinate_truth_allowed": modified_class[2],
        },
        "source_selection_changed": False,
        "review_item_created": False,
        "raw_image_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }
    write_yaml(out, payload)
    write_json(results_dir / "variant_classifier_repair_report.json", payload)
    return payload
