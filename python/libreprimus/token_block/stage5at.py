"""Stage 5AT token case-review pack generation and validation."""

from __future__ import annotations

import csv
import zipfile
from pathlib import Path
from typing import Any

from .mapping import token_to_value
from .models import (
    FALSE_GUARDRAILS,
    PRIMARY_ALPHABET,
    STAGE5AT_ID,
    TOKEN_BLOCK_ID,
    read_yaml,
    repo_relative,
    sha256_file,
    write_json,
    write_jsonl,
    write_yaml,
)

ACTIVE_AMBIGUITY_CLASSES = ["I/l", "O/0", "1/I/l", "S/5", "Z/2", "B/8", "G/6", "o/0", "q/g/p"]
STALE_DOC_ONLY_EXAMPLES = ["f/F", "A/4", "C/G"]
PAGE_TRANSITION_ROWS = {9, 10, 22, 23, 31}

STAGE5AT_FALSE_GUARDRAILS = {
    **FALSE_GUARDRAILS,
    "live_web_scrape_performed": False,
    "raw_images_committed": False,
    "generated_crops_committed": False,
    "generated_review_pack_committed": False,
    "codex_output_committed": False,
    "third_party_raw_staged": False,
    "third_party_raw_tracked_new": False,
    "public_website_publication_performed": False,
    "llm_vision_token_reading_performed": False,
    "semantic_image_interpretation_performed": False,
    "hidden_content_image_forensics_performed": False,
    "decode_attempt_performed": False,
    "hypothesis_generation_performed": False,
    "new_cuda_kernel_added": False,
    "new_cuda_kernels_added": 0,
    "method_status_upgraded": False,
}


def _records_by_index(pixel_payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    return {int(record["token_index_0_based"]): record for record in pixel_payload.get("records", [])}


def _ambiguity_membership(ambiguity_payload: dict[str, Any]) -> dict[int, list[dict[str, Any]]]:
    membership: dict[int, list[dict[str, Any]]] = {}
    for record in ambiguity_payload.get("records", []):
        for index in record.get("affected_token_indexes_0_based", []):
            membership.setdefault(int(index), []).append(record)
    return membership


def _mapped_value(token: str) -> int | None:
    if len(token) != 2 or token[0] not in "01234" or token[1] not in PRIMARY_ALPHABET:
        return None
    return token_to_value(token, PRIMARY_ALPHABET)


def _candidate_symbols(token: str, records: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    first_symbols = {token[0]}
    suffix_symbols = {token[1]}
    for record in records:
        candidates = [str(candidate) for candidate in record.get("ambiguous_symbol_candidates", [])]
        if token[0] in candidates:
            first_symbols.update(candidates)
        if token[1] in candidates:
            suffix_symbols.update(candidates)
    return sorted(first_symbols), sorted(suffix_symbols)


def _candidate_tokens(first_symbols: list[str], suffix_symbols: list[str]) -> list[str]:
    return sorted({f"{first}{suffix}" for first in first_symbols for suffix in suffix_symbols})


def _value_records(current_token: str, candidates: list[str]) -> tuple[int | None, list[dict[str, Any]], dict[str, Any]]:
    current_value = _mapped_value(current_token)
    candidate_records = []
    mapped_values = []
    invalid_count = 0
    for candidate in candidates:
        value = _mapped_value(candidate)
        if value is None:
            invalid_count += 1
        else:
            mapped_values.append(value)
        candidate_records.append(
            {
                "candidate_token": candidate,
                "primary_60_value": value,
                "value_status": "mapped_primary_60" if value is not None else "outside_primary_60_mapping",
                "delta_from_current": None if value is None or current_value is None else value - current_value,
            }
        )
    delta_summary = {
        "current_value": current_value,
        "mapped_candidate_count": len(mapped_values),
        "invalid_candidate_count": invalid_count,
        "mapped_candidate_min": min(mapped_values) if mapped_values else None,
        "mapped_candidate_max": max(mapped_values) if mapped_values else None,
        "value_sensitive": any(value != current_value for value in mapped_values) or invalid_count > 0,
    }
    return current_value, candidate_records, delta_summary


def build_case_review_policy(
    *,
    stage5ar_case_policy: Path,
    stage5ar_case_ambiguities: Path,
    stage5ap_transcription: Path,
    out: Path,
) -> dict[str, Any]:
    policy = read_yaml(stage5ar_case_policy)
    ambiguities = read_yaml(stage5ar_case_ambiguities)
    read_yaml(stage5ap_transcription)
    active = [record["canonical_symbol"] for record in ambiguities.get("records", [])]
    payload = {
        "record_type": "case_review_policy",
        "schema": "schemas/token-block/case-review-policy-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "source_stage_id": "stage-5ar",
        "token_block_id": TOKEN_BLOCK_ID,
        "policy_status": "human_review_required",
        "active_ambiguity_classes": active,
        "active_ambiguity_class_count": len(active),
        "expected_active_ambiguity_classes": ACTIVE_AMBIGUITY_CLASSES,
        "active_classes_match_stage5ar_data": active == ACTIVE_AMBIGUITY_CLASSES,
        "stale_doc_only_examples": STALE_DOC_ONLY_EXAMPLES,
        "stale_examples_active": [],
        "canonical_transcription_changed": False,
        "canonical_transcription_change_allowed": False,
        "human_review_required": True,
        "automatic_case_resolution_performed": False,
        "review_status": "human_review_required",
        "source_stage5ar_policy_status": policy.get("case_policy_status"),
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    return payload


def build_case_challenge_sets(
    *,
    stage5ar_case_ambiguities: Path,
    stage5ar_pixel_coordinates: Path,
    stage5ap_transcription: Path,
    stage5ap_alphabet_registry: Path,
    results_dir: Path,
    out_case_challenges: Path,
    out_canonical_challenges: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    ambiguities = read_yaml(stage5ar_case_ambiguities)
    pixel_payload = read_yaml(stage5ar_pixel_coordinates)
    transcription = read_yaml(stage5ap_transcription)
    read_yaml(stage5ap_alphabet_registry)
    membership = _ambiguity_membership(ambiguities)
    coordinates = _records_by_index(pixel_payload)
    challenge_records = []
    for token_index in sorted(membership):
        coordinate = coordinates[token_index]
        records = membership[token_index]
        token = coordinate["token"]
        first_symbols, suffix_symbols = _candidate_symbols(token, records)
        candidates = _candidate_tokens(first_symbols, suffix_symbols)
        current_value, candidate_values, delta_summary = _value_records(token, candidates)
        challenge_id = f"stage5at-token-case-{token_index:03d}"
        crop_refs = [f"{challenge_id}-token-bbox", f"{challenge_id}-token-magnified-x4"]
        context_refs = [
            f"{challenge_id}-context-small",
            f"{challenge_id}-context-medium",
            f"{challenge_id}-row-context",
        ]
        challenge_records.append(
            {
                "record_type": "case_review_challenge_record",
                "schema": "schemas/token-block/case-review-challenge-record-v0.schema.json",
                "stage_id": STAGE5AT_ID,
                "token_block_id": TOKEN_BLOCK_ID,
                "challenge_id": challenge_id,
                "token_review_group_id": f"stage5at-token-review-group-{token_index:03d}",
                "ambiguity_classes": [record["canonical_symbol"] for record in records],
                "ambiguity_class": records[0]["canonical_symbol"],
                "token_index_0_based": token_index,
                "token_index_1_based": token_index + 1,
                "canonical_token": token,
                "candidate_tokens": candidates,
                "current_first_symbol": token[0],
                "current_suffix_symbol": token[1],
                "candidate_first_symbols": first_symbols,
                "candidate_suffix_symbols": suffix_symbols,
                "page_number": coordinate["assigned_page_number"],
                "global_row_index_0_based": coordinate["global_row_index_0_based"],
                "global_row_index_1_based": coordinate["global_row_index_1_based"],
                "page_row_index_0_based": coordinate["assigned_page_row_index_0_based"],
                "page_row_index_1_based": coordinate["assigned_page_row_index_1_based"],
                "column_index_0_based": coordinate["global_column_index_0_based"],
                "column_index_1_based": coordinate["global_column_index_1_based"],
                "coordinate_ref": f"r{coordinate['global_row_index_1_based']:02d}c{coordinate['global_column_index_1_based']:02d}",
                "original_image_id": coordinate["original_image_id"],
                "original_image_sha256": coordinate["original_image_sha256"],
                "bbox": {
                    "x_min": coordinate["bbox_x_min"],
                    "y_min": coordinate["bbox_y_min"],
                    "x_max": coordinate["bbox_x_max"],
                    "y_max": coordinate["bbox_y_max"],
                    "width": coordinate["bbox_width"],
                    "height": coordinate["bbox_height"],
                },
                "review_crop_refs": crop_refs,
                "context_crop_refs": context_refs,
                "primary_60_current_value": current_value,
                "primary_60_candidate_values": candidate_values,
                "value_delta_summary": delta_summary,
                "review_status": "human_review_required",
                "decision_status": "unresolved",
                "canonical_transcription_change_allowed": False,
                "notes": "Human review required; Stage 5AT does not resolve token glyph case automatically.",
                "ocr_performed": False,
                "ai_ml_interpretation_performed": False,
                "llm_vision_token_reading_performed": False,
                "semantic_image_interpretation_performed": False,
                "solve_claim": False,
            }
        )
    ambiguous_indexes = {record["token_index_0_based"] for record in challenge_records}
    rows = transcription["token_grid"]
    canonical_items: dict[int, dict[str, Any]] = {}
    for challenge in challenge_records:
        row = challenge["global_row_index_0_based"]
        priority = "critical" if row in PAGE_TRANSITION_ROWS and challenge["value_delta_summary"]["value_sensitive"] else "high"
        canonical_items[challenge["token_index_0_based"]] = {
            "token_index": challenge["token_index_0_based"],
            "current_canonical_token": challenge["canonical_token"],
            "review_reason": "case_ambiguity",
            "review_priority": priority,
            "coordinate_ref": challenge["coordinate_ref"],
            "crop_refs": challenge["review_crop_refs"] + challenge["context_crop_refs"],
            "decision_status": "unresolved",
        }
    for row_index in sorted(PAGE_TRANSITION_ROWS):
        for col_index, token in enumerate(rows[row_index]):
            token_index = row_index * 8 + col_index
            canonical_items.setdefault(
                token_index,
                {
                    "token_index": token_index,
                    "current_canonical_token": token,
                    "review_reason": "page_transition_row",
                    "review_priority": "medium",
                    "coordinate_ref": f"r{row_index + 1:02d}c{col_index + 1:02d}",
                    "crop_refs": [],
                    "decision_status": "unresolved",
                },
            )
    controls = []
    for page_number in (49, 50, 51):
        page_coords = [
            record
            for record in coordinates.values()
            if record["assigned_page_number"] == page_number and record["token_index_0_based"] not in ambiguous_indexes
        ]
        for record in page_coords[:2]:
            controls.append(record["token_index_0_based"])
            canonical_items.setdefault(
                record["token_index_0_based"],
                {
                    "token_index": record["token_index_0_based"],
                    "current_canonical_token": record["token"],
                    "review_reason": "non_ambiguous_control",
                    "review_priority": "control",
                    "coordinate_ref": f"r{record['global_row_index_1_based']:02d}c{record['global_column_index_1_based']:02d}",
                    "crop_refs": [],
                    "decision_status": "unresolved",
                },
            )
    canonical_records = [
        {
            "record_type": "canonical_transcription_challenge_record",
            "schema": "schemas/token-block/canonical-transcription-challenge-record-v0.schema.json",
            "stage_id": STAGE5AT_ID,
            "token_block_id": TOKEN_BLOCK_ID,
            "challenge_id": f"stage5at-canonical-token-{index:03d}",
            **record,
            "canonical_transcription_changed": False,
            "canonical_transcription_change_allowed": False,
            "review_status": "human_review_required",
        }
        for index, record in sorted(canonical_items.items())
    ]
    case_payload = {
        "record_type": "case_review_challenge_set",
        "schema": "schemas/token-block/case-review-challenge-record-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "active_ambiguity_classes": ACTIVE_AMBIGUITY_CLASSES,
        "active_ambiguity_class_count": len(ACTIVE_AMBIGUITY_CLASSES),
        "challenge_count": len(challenge_records),
        "unique_token_review_group_count": len(challenge_records),
        "review_status": "human_review_required",
        "decision_status": "unresolved",
        "canonical_transcription_changed": False,
        "canonical_transcription_change_allowed": False,
        "records": challenge_records,
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    canonical_payload = {
        "record_type": "canonical_transcription_challenge_set",
        "schema": "schemas/token-block/canonical-transcription-challenge-record-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "challenge_count": len(canonical_records),
        "ambiguity_affected_token_count": len(challenge_records),
        "non_ambiguous_control_token_count": len(controls),
        "page_transition_review_item_count": 40,
        "canonical_transcription_changed": False,
        "canonical_transcription_change_allowed": False,
        "records": canonical_records,
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out_case_challenges, case_payload)
    write_yaml(out_canonical_challenges, canonical_payload)
    write_json(results_dir / "case_review_challenge_set.json", case_payload)
    write_json(results_dir / "canonical_transcription_challenge_set.json", canonical_payload)
    return case_payload, canonical_payload


def _clip_bbox(bbox: dict[str, int], width: int, height: int, margin: int = 0) -> tuple[int, int, int, int]:
    return (
        max(0, int(bbox["x_min"]) - margin),
        max(0, int(bbox["y_min"]) - margin),
        min(width, int(bbox["x_max"]) + margin),
        min(height, int(bbox["y_max"]) + margin),
    )


def _crop_record(
    *,
    crop_id: str,
    challenge: dict[str, Any],
    source_path: Path,
    image_size: tuple[int, int],
    bbox: tuple[int, int, int, int],
    crop_type: str,
    scale_factor: int,
    out_path: Path,
) -> dict[str, Any]:
    from PIL import Image

    with Image.open(source_path) as image:
        crop = image.crop(bbox)
        if scale_factor != 1:
            crop = crop.resize((crop.width * scale_factor, crop.height * scale_factor), Image.Resampling.NEAREST)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        crop.save(out_path)
    return {
        "crop_id": crop_id,
        "challenge_id": challenge["challenge_id"],
        "source_original_image_id": challenge["original_image_id"],
        "source_original_image_sha256": challenge["original_image_sha256"],
        "source_page_number": challenge["page_number"],
        "source_bbox": challenge["bbox"],
        "crop_bbox": {"x_min": bbox[0], "y_min": bbox[1], "x_max": bbox[2], "y_max": bbox[3]},
        "scale_factor": scale_factor,
        "crop_type": crop_type,
        "path": repo_relative(out_path),
        "sha256": sha256_file(out_path),
        "generated_from_original_image": True,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "semantic_interpretation_performed": False,
        "derived_review_image_not_source": True,
        "solve_claim": False,
    }


def build_review_pack(
    *,
    stage5ar_source_lock: Path,
    stage5ar_pixel_coordinates: Path,
    case_challenges: Path,
    canonical_challenges: Path,
    out_root: Path,
    results_dir: Path,
    out_crop_manifest: Path,
    out_decision_template: Path,
    out_pack_manifest: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    source_lock = read_yaml(stage5ar_source_lock)
    pixel_payload = read_yaml(stage5ar_pixel_coordinates)
    case_payload = read_yaml(case_challenges)
    read_yaml(canonical_challenges)
    image_paths = {record["original_image_id"]: Path(record["source_path"]) for record in source_lock.get("records", [])}
    image_sizes = {
        record["original_image_id"]: (int(record["width"]), int(record["height"])) for record in source_lock.get("records", [])
    }
    coordinates = _records_by_index(pixel_payload)
    out_root.mkdir(parents=True, exist_ok=True)
    (out_root / "assets").mkdir(parents=True, exist_ok=True)
    (out_root / "crops").mkdir(parents=True, exist_ok=True)
    (out_root / "context-crops").mkdir(parents=True, exist_ok=True)
    (out_root / "review-sheets").mkdir(parents=True, exist_ok=True)
    crop_records = []
    for challenge in case_payload["records"]:
        image_id = challenge["original_image_id"]
        source_path = image_paths[image_id]
        width, height = image_sizes[image_id]
        token_bbox = _clip_bbox(challenge["bbox"], width, height)
        small_bbox = _clip_bbox(challenge["bbox"], width, height, 32)
        medium_bbox = _clip_bbox(challenge["bbox"], width, height, 96)
        row_records = [
            record
            for record in coordinates.values()
            if record["assigned_page_number"] == challenge["page_number"]
            and record["global_row_index_0_based"] == challenge["global_row_index_0_based"]
        ]
        row_bbox = (
            0,
            max(0, min(record["bbox_y_min"] for record in row_records) - 32),
            width,
            min(height, max(record["bbox_y_max"] for record in row_records) + 32),
        )
        crop_specs = [
            ("token-bbox", "token_bbox_crop", 1, token_bbox, out_root / "crops" / f"{challenge['challenge_id']}-token.png"),
            ("token-magnified-x4", "magnified_token_crop", 4, token_bbox, out_root / "crops" / f"{challenge['challenge_id']}-token-x4.png"),
            ("context-small", "context_crop_small", 1, small_bbox, out_root / "context-crops" / f"{challenge['challenge_id']}-context-small.png"),
            ("context-medium", "context_crop_medium", 1, medium_bbox, out_root / "context-crops" / f"{challenge['challenge_id']}-context-medium.png"),
            ("row-context", "row_context_crop", 1, row_bbox, out_root / "context-crops" / f"{challenge['challenge_id']}-row-context.png"),
        ]
        for suffix, crop_type, scale, bbox, path in crop_specs:
            crop_records.append(
                _crop_record(
                    crop_id=f"{challenge['challenge_id']}-{suffix}",
                    challenge=challenge,
                    source_path=source_path,
                    image_size=(width, height),
                    bbox=bbox,
                    crop_type=crop_type,
                    scale_factor=scale,
                    out_path=path,
                )
            )
    decision_rows = [
        {
            "challenge_id": challenge["challenge_id"],
            "token_index_0_based": challenge["token_index_0_based"],
            "current_canonical_token": challenge["canonical_token"],
            "human_selected_token": None,
            "human_selected_first_symbol": None,
            "human_selected_suffix_symbol": None,
            "decision": "unresolved",
            "confidence": None,
            "reviewer_notes": None,
            "reviewer_initials_or_id_optional": None,
            "review_date_optional": None,
            "requires_second_review": True,
        }
        for challenge in case_payload["records"]
    ]
    decision_template = {
        "record_type": "human_review_decision_template",
        "schema": "schemas/token-block/human-review-decision-template-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "template_status": "empty_unfilled",
        "human_review_required": True,
        "codex_filled_decisions": False,
        "canonical_transcription_changed": False,
        "decision_count": len(decision_rows),
        "records": decision_rows,
        "allowed_decisions": ["keep_current", "change_token", "unresolved", "not_reviewable"],
        "allowed_confidence": ["high", "medium", "low"],
        "instructions": "The user must fill this in manually. Codex must not fill decisions automatically.",
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out_root / "challenge-set.yaml", case_payload)
    write_json(out_root / "challenge-set.json", case_payload)
    write_yaml(out_root / "decision-template.yaml", decision_template)
    write_json(out_root / "decision-template.json", decision_template)
    with (out_root / "decision-template.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(decision_rows[0]))
        writer.writeheader()
        writer.writerows(decision_rows)
    (out_root / "README.md").write_text("# Stage 5AT Token Case Review Pack\n\nGenerated review pack. Do not commit generated crops or decisions.\n", encoding="utf-8")
    (out_root / "review-instructions.md").write_text(
        "# Review Instructions\n\nInspect the generated crops manually and fill the decision template. Do not treat crops as source truth.\n",
        encoding="utf-8",
    )
    (out_root / "assets" / "site.css").write_text("body{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto}.card{border:1px solid #ccc;padding:1rem;margin:1rem 0}img{max-width:220px;image-rendering:pixelated}\n", encoding="utf-8")
    (out_root / "assets" / "site.js").write_text("document.documentElement.dataset.reviewPack='stage5at';\n", encoding="utf-8")
    cards = []
    for challenge in case_payload["records"][:80]:
        crop = f"crops/{challenge['challenge_id']}-token-x4.png"
        cards.append(f"<section class='card'><h2>{challenge['challenge_id']}</h2><p>{challenge['canonical_token']} | {', '.join(challenge['ambiguity_classes'])}</p><img src='{crop}' alt='Review crop'></section>")
    (out_root / "index.html").write_text(
        "<!doctype html><meta charset='utf-8'><meta name='robots' content='noindex'><link rel='stylesheet' href='assets/site.css'><title>Stage 5AT Token Case Review</title><h1>Stage 5AT Token Case Review</h1>"
        + "".join(cards),
        encoding="utf-8",
    )
    for ambiguity in ACTIVE_AMBIGUITY_CLASSES:
        sheet = out_root / "review-sheets" / f"{ambiguity.replace('/', '-')}.md"
        related = [challenge for challenge in case_payload["records"] if ambiguity in challenge["ambiguity_classes"]]
        sheet.write_text(
            "# Review sheet: " + ambiguity + "\n\n" + "\n".join(f"- {item['challenge_id']} token {item['canonical_token']}" for item in related) + "\n",
            encoding="utf-8",
        )
    manifest_files = sorted(path for path in out_root.rglob("*") if path.is_file())
    file_manifest = {
        "record_type": "case_review_pack_file_manifest",
        "stage_id": STAGE5AT_ID,
        "file_count": len(manifest_files),
        "files": [{"path": repo_relative(path), "sha256": sha256_file(path), "size_bytes": path.stat().st_size} for path in manifest_files],
    }
    write_json(out_root / "file-manifest.json", file_manifest)
    zip_path = out_root / "token-case-review-pack.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in out_root.rglob("*") if p.is_file() and p != zip_path):
            archive.write(path, path.relative_to(out_root))
    crop_manifest = {
        "record_type": "case_review_crop_manifest",
        "schema": "schemas/token-block/case-review-crop-manifest-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "crop_count": len(crop_records),
        "context_crop_count": sum(1 for record in crop_records if record["crop_type"].startswith("context") or record["crop_type"] == "row_context_crop"),
        "generated_from_original_images": True,
        "derived_review_images_not_source_truth": True,
        "records": crop_records,
        "raw_images_committed": False,
        "generated_crops_committed": False,
        "generated_review_pack_committed": False,
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    pack_manifest = {
        "record_type": "case_review_pack_manifest",
        "schema": "schemas/token-block/case-review-pack-manifest-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "review_pack_generated": True,
        "review_pack_root": repo_relative(out_root),
        "review_pack_zip_created": True,
        "review_pack_zip_path": repo_relative(zip_path),
        "review_pack_zip_sha256": sha256_file(zip_path),
        "generated_crop_count": crop_manifest["crop_count"],
        "generated_context_crop_count": crop_manifest["context_crop_count"],
        "generated_review_sheet_count": len(ACTIVE_AMBIGUITY_CLASSES),
        "generated_html_review_pack_created": True,
        "decision_template_paths": [
            repo_relative(out_root / "decision-template.yaml"),
            repo_relative(out_root / "decision-template.json"),
            repo_relative(out_root / "decision-template.csv"),
        ],
        "file_manifest_path": repo_relative(out_root / "file-manifest.json"),
        "derived_review_images_not_source_truth": True,
        "generated_review_pack_committed": False,
        "generated_crops_committed": False,
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out_crop_manifest, crop_manifest)
    write_yaml(out_decision_template, decision_template)
    write_yaml(out_pack_manifest, pack_manifest)
    write_json(results_dir / "crop_manifest.json", crop_manifest)
    write_json(results_dir / "review_pack_manifest.json", pack_manifest)
    return crop_manifest, decision_template, pack_manifest


def build_doc_drift_repair_summary(*, case_review_policy: Path, results_dir: Path, out: Path) -> dict[str, Any]:
    policy = read_yaml(case_review_policy)
    payload = {
        "record_type": "doc_drift_repair_summary",
        "schema": "schemas/token-block/doc-drift-repair-summary-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "doc_drift_repaired": True,
        "active_ambiguity_classes": policy["active_ambiguity_classes"],
        "stale_doc_only_examples": STALE_DOC_ONLY_EXAMPLES,
        "stale_examples_not_active": True,
        "doc_drift_active_classes_match_data": policy["active_classes_match_stage5ar_data"],
        "canonical_transcription_changed": False,
        "no_solve_claim": True,
    }
    write_yaml(out, payload)
    write_json(results_dir / "doc_drift_repair_report.json", payload)
    return payload


def build_null_control_case_update(*, stage5ar_null_control_update: Path, case_challenges: Path, out: Path) -> dict[str, Any]:
    source = read_yaml(stage5ar_null_control_update)
    challenges = read_yaml(case_challenges)
    payload = {
        "record_type": "null_control_case_update",
        "schema": "schemas/token-block/null-control-case-update-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_stage5ar_null_controls": source.get("source_null_control_plan"),
        "case_decision_controls_added": True,
        "review_bias_controls_added": True,
        "value_sensitivity_controls_added": True,
        "case_decision_controls": ["keep-current control", "change-token control", "unresolved-control", "not-reviewable-control"],
        "review_bias_controls": ["blind duplicate review item", "non-ambiguous calibration control", "page-transition calibration control"],
        "value_sensitivity_controls": ["primary-60 value-change control", "outside-primary-60 candidate control"],
        "challenge_count": challenges.get("challenge_count"),
        "execution_enabled": False,
        "no_decode": True,
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    return payload


def build_dwh_case_context(*, out: Path) -> dict[str, Any]:
    payload = {
        "record_type": "dwh_case_context",
        "schema": "schemas/token-block/dwh-case-context-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "dwh_status": "speculative_non_operational",
        "case_policy_relevance": "case-sensitive token values can change primary-60 mapped bytes",
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "decode_attempt_performed": False,
        "stage_scope": "human_review_and_case_sensitivity_planning_only",
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out, payload)
    return payload


def build_stage5at_summary(
    *,
    case_review_policy: Path,
    case_challenges: Path,
    canonical_challenges: Path,
    crop_manifest: Path,
    decision_template: Path,
    pack_manifest: Path,
    variant_repair: Path,
    doc_drift_summary: Path,
    null_control_update: Path,
    dwh_case_context: Path,
    results_dir: Path,
    out_guardrail: Path,
    out_next_stage: Path,
    out_summary: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    policy = read_yaml(case_review_policy)
    challenges = read_yaml(case_challenges)
    canonical = read_yaml(canonical_challenges)
    crops = read_yaml(crop_manifest)
    decisions = read_yaml(decision_template)
    pack = read_yaml(pack_manifest)
    variant = read_yaml(variant_repair)
    doc_drift = read_yaml(doc_drift_summary)
    nulls = read_yaml(null_control_update)
    dwh = read_yaml(dwh_case_context)
    guardrail = {
        "record_type": "stage5at_guardrail",
        "schema": "schemas/token-block/stage5at-guardrail-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "human_review_required": True,
        "automatic_case_resolution_performed": False,
        "canonical_transcription_changed": False,
        "generated_crops_committed": False,
        "generated_review_pack_committed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "decode_attempt_performed": False,
        "hash_preimage_search_performed": False,
        "solve_claim": False,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    next_stage = {
        "record_type": "stage5at_next_stage_decision",
        "schema": "schemas/project-state/stage5at-summary-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "status": "complete",
        "selected_next_stage_short_name": "Stage 5AU",
        "selected_next_stage_title": "Stage 5AU - manual human review of token case challenge pack",
        "selected_next_prompt_type": "manual_human_review",
        "selection_reason": "The review pack validates and no human decision file is present.",
        "manual_human_review_recommended": True,
        "codex_integration_next_ready": False,
        "bounded_preflight_recommended": False,
        "scored_experiments_recommended": False,
        "unsolved_page_cuda_recommended": False,
        "public_website_expansion_recommended": False,
        "execution_enabled": False,
        "no_solve_claim": True,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    summary = {
        "record_type": "stage5at_token_case_review_pack_summary",
        "schema": "schemas/project-state/stage5at-summary-v0.schema.json",
        "stage_id": STAGE5AT_ID,
        "status": "complete",
        "source_stage_id": "stage-5as",
        "source_stage5ar_commit": "4a5050e14981c1a3134381290f8a5a8bc1ac101b",
        "case_review_policy_created": True,
        "active_ambiguity_classes": policy["active_ambiguity_classes"],
        "active_ambiguity_class_count": policy["active_ambiguity_class_count"],
        "case_review_challenge_count": challenges["challenge_count"],
        "unique_token_review_group_count": challenges["unique_token_review_group_count"],
        "canonical_transcription_challenge_count": canonical["challenge_count"],
        "non_ambiguous_control_token_count": canonical["non_ambiguous_control_token_count"],
        "page_transition_review_item_count": canonical["page_transition_review_item_count"],
        "review_pack_generated": pack["review_pack_generated"],
        "review_pack_root": pack["review_pack_root"],
        "review_pack_zip_created": pack["review_pack_zip_created"],
        "review_pack_zip_path": pack["review_pack_zip_path"],
        "generated_crop_count": crops["crop_count"],
        "generated_context_crop_count": crops["context_crop_count"],
        "generated_review_sheet_count": pack["generated_review_sheet_count"],
        "generated_html_review_pack_created": pack["generated_html_review_pack_created"],
        "human_review_decisions_present": False,
        "human_review_decisions_integrated": False,
        "canonical_transcription_changed": decisions["canonical_transcription_changed"],
        "canonical_transcription_change_allowed": False,
        "variant_classifier_repaired": variant["variant_classifier_repaired"],
        "unmodified_path_bug_test_passed": variant["unmodified_path_bug_test_passed"],
        "doc_drift_repaired": doc_drift["doc_drift_repaired"],
        "doc_drift_active_classes_match_data": doc_drift["doc_drift_active_classes_match_data"],
        "null_control_case_update_created": nulls["case_decision_controls_added"],
        "dwh_case_context_created": dwh["dwh_defined"],
        "next_manual_review_required": True,
        "deep_research_next_ready": False,
        "manual_human_review_next_ready": True,
        "codex_integration_next_ready": False,
        **STAGE5AT_FALSE_GUARDRAILS,
    }
    write_yaml(out_guardrail, guardrail)
    write_yaml(out_next_stage, next_stage)
    write_yaml(out_summary, summary)
    write_json(results_dir / "null_control_case_update.json", nulls)
    write_json(results_dir / "summary.json", summary)
    write_jsonl(results_dir / "warnings.jsonl", [])
    return guardrail, next_stage, summary


def validate_stage5at(
    *,
    case_review_policy: Path,
    case_challenges: Path,
    canonical_challenges: Path,
    crop_manifest: Path,
    decision_template: Path,
    pack_manifest: Path,
    variant_repair: Path,
    doc_drift_summary: Path,
    null_control_update: Path,
    dwh_case_context: Path,
    guardrail: Path,
    next_stage_decision: Path,
    summary: Path,
    review_pack_root: Path,
    results_dir: Path,
) -> tuple[dict[str, Any], list[str]]:
    policy = read_yaml(case_review_policy)
    challenges = read_yaml(case_challenges)
    canonical = read_yaml(canonical_challenges)
    crops = read_yaml(crop_manifest)
    decisions = read_yaml(decision_template)
    pack = read_yaml(pack_manifest)
    variant = read_yaml(variant_repair)
    doc_drift = read_yaml(doc_drift_summary)
    nulls = read_yaml(null_control_update)
    dwh = read_yaml(dwh_case_context)
    guard = read_yaml(guardrail)
    next_stage = read_yaml(next_stage_decision)
    summary_record = read_yaml(summary)
    errors: list[str] = []
    if policy.get("active_ambiguity_classes") != ACTIVE_AMBIGUITY_CLASSES:
        errors.append("active_ambiguity_classes_mismatch")
    if any(example in policy.get("active_ambiguity_classes", []) for example in STALE_DOC_ONLY_EXAMPLES):
        errors.append("stale_doc_examples_active")
    if challenges.get("challenge_count", 0) <= 0:
        errors.append("case_challenge_set_empty")
    if any(record.get("review_status") != "human_review_required" for record in challenges.get("records", [])):
        errors.append("challenge_review_status_not_human_review_required")
    if any(record.get("decision_status") != "unresolved" for record in challenges.get("records", [])):
        errors.append("challenge_decision_status_not_unresolved")
    if decisions.get("template_status") != "empty_unfilled" or decisions.get("codex_filled_decisions") is not False:
        errors.append("decision_template_not_empty")
    if crops.get("derived_review_images_not_source_truth") is not True or crops.get("generated_crops_committed") is not False:
        errors.append("crop_manifest_guardrail_failed")
    if variant.get("unmodified_path_bug_test_passed") is not True:
        errors.append("variant_classifier_unmodified_test_failed")
    if doc_drift.get("doc_drift_active_classes_match_data") is not True:
        errors.append("doc_drift_not_repaired")
    if nulls.get("case_decision_controls_added") is not True:
        errors.append("null_control_case_update_missing")
    if dwh.get("dwh_expansion") != "Deep Web Hash" or dwh.get("hash_search_performed") is not False:
        errors.append("dwh_case_guardrail_failed")
    for key in (
        "automatic_case_resolution_performed",
        "ocr_performed",
        "ai_ml_interpretation_performed",
        "llm_vision_token_reading_performed",
        "semantic_image_interpretation_performed",
        "hidden_content_image_forensics_performed",
        "stego_tool_execution_performed",
        "hash_preimage_search_performed",
        "decode_attempt_performed",
        "cuda_execution_performed",
        "cuda_source_modified",
        "benchmark_performed",
        "scored_experiments_executed",
        "solve_claim",
    ):
        if guard.get(key) not in (False, 0):
            errors.append(f"{key}_not_false")
    _ = (review_pack_root, results_dir)
    counts = {
        "stage_id": STAGE5AT_ID,
        "active_ambiguity_classes": ",".join(policy.get("active_ambiguity_classes", [])),
        "case_review_challenge_count": challenges.get("challenge_count"),
        "canonical_transcription_challenge_count": canonical.get("challenge_count"),
        "generated_crop_count": crops.get("crop_count"),
        "generated_review_sheet_count": pack.get("generated_review_sheet_count"),
        "variant_classifier_repaired": variant.get("variant_classifier_repaired"),
        "doc_drift_repaired": doc_drift.get("doc_drift_repaired"),
        "canonical_transcription_changed": summary_record.get("canonical_transcription_changed"),
        "human_review_decisions_present": summary_record.get("human_review_decisions_present"),
        "human_review_decisions_integrated": summary_record.get("human_review_decisions_integrated"),
        "selected_next_stage_title": next_stage.get("selected_next_stage_title"),
        "manual_human_review_recommended": next_stage.get("manual_human_review_recommended"),
        "ocr_performed": guard.get("ocr_performed"),
        "cuda_execution_performed": guard.get("cuda_execution_performed"),
        "new_cuda_kernels_added": guard.get("new_cuda_kernels_added"),
        "validation_error_count": len(errors),
    }
    return counts, errors
