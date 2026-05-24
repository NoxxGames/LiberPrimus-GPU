"""Stage 5AK community-facts attachment metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from PIL import Image

from .export import repo_relative, resolve, write_json, write_records
from .hashing import hash_file
from .models import (
    STAGE5AK_ATTACHMENT_INDEX_PATH,
    STAGE5AK_ID,
    STAGE5AK_OUTPUT_DIR,
    STAGE5AK_REPORTS,
    STAGE5AK_SOURCE_ROOT,
    STAGE5AK_SOURCE_STAGE_ID,
)


IMAGE_EXTENSIONS = {".webp", ".png", ".jpg", ".jpeg"}
IMAGE_CLAIM_FAMILIES = {
    1: "doublet_route_index_observations",
    2: "p15_red_text_progressive_sum_square",
    3: "p54_55_p56_p57_hash_length_equivalence",
    4: "red_3299_fehu_count_prime_index",
    5: "cicada_prime_index_number_network",
    6: "pixel_measurement_prime_dimension_claims",
    7: "no_fehu_section_count_graph",
    8: "no_fehu_section_count_graph",
    9: "no_fehu_section_count_graph",
    10: "no_fehu_section_count_graph",
}


def build_community_attachment_index(
    *,
    source_root: Path = STAGE5AK_SOURCE_ROOT,
    results_dir: Path = STAGE5AK_OUTPUT_DIR,
    out: Path = STAGE5AK_ATTACHMENT_INDEX_PATH,
) -> dict[str, Any]:
    """Hash and order community-facts image attachments without OCR."""

    root = resolve(source_root)
    images = []
    if root.exists():
        images = [
            path
            for path in sorted(root.iterdir(), key=lambda item: (_numeric_prefix(item.name), item.name.lower()))
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ]
    records = []
    for order, path in enumerate(images, start=1):
        prefix = _numeric_prefix(path.name)
        hashed = hash_file(path)
        records.append(
            {
                "record_type": "stage5ak_community_facts_attachment_record",
                "schema": "schemas/source-harvester/community-facts-attachment-index-v0.schema.json",
                "stage_id": STAGE5AK_ID,
                "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
                "source_id": "community_facts_observations_local",
                "attachment_id": f"community-facts-attachment-{order:02d}",
                "file_name": path.name,
                "relative_path": repo_relative(path),
                "image_order": order,
                "numeric_filename_order": prefix,
                "sha256": hashed["sha256"],
                "size_bytes": hashed["size_bytes"],
                "extension": path.suffix.lower(),
                "claim_family_hint": IMAGE_CLAIM_FAMILIES.get(prefix, "community_number_fact_thread"),
                "message_to_image_linkage": "inferred_from_thread_order",
                "raw_image_committed": False,
                "image_forensics_performed": False,
                "ocr_performed": False,
                "ai_ml_interpretation_performed": False,
                "website_publication_allowed": False,
                "deep_research_private_allowed": True,
                "solve_claim": False,
                **_image_metadata(path),
            }
        )
    summary = {
        "record_type": "stage5ak_community_facts_attachment_index",
        "schema": "schemas/source-harvester/community-facts-attachment-index-v0.schema.json",
        "stage_id": STAGE5AK_ID,
        "source_stage_id": STAGE5AK_SOURCE_STAGE_ID,
        "source_id": "community_facts_observations_local",
        "source_root": source_root.as_posix(),
        "local_folder_exists": root.exists(),
        "attachment_index_records": len(records),
        "attachment_images_detected": len(records),
        "attachment_order": [record["file_name"] for record in records],
        "raw_images_committed": False,
        "generated_outputs_committed": False,
        "ocr_performed": False,
        "image_forensics_performed": False,
        "ai_ml_interpretation_performed": False,
        "solve_claim": False,
    }
    write_records(out, records, **summary)
    write_json(results_dir / STAGE5AK_REPORTS["attachment_index"], {**summary, "records": records})
    return {**summary, "records": records}


def _numeric_prefix(name: str) -> int:
    match = re.match(r"^(\d+)", name)
    return int(match.group(1)) if match else 10_000


def _image_metadata(path: Path) -> dict[str, Any]:
    try:
        with Image.open(path) as image:
            return {
                "width": int(image.width),
                "height": int(image.height),
                "image_format": image.format,
                "colour_mode": image.mode,
            }
    except OSError:
        return {
            "width": None,
            "height": None,
            "image_format": "unreadable",
            "colour_mode": None,
        }
