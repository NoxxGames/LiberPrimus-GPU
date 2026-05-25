"""Metadata-only source-lock and image provenance helpers for Stage 5AP."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .models import FALSE_GUARDRAILS, STAGE_ID, TOKEN_BLOCK_ID, repo_relative, sha256_file, write_json, write_yaml

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp"}
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json"}
PAGE_STEMS = {"49", "50", "51"}


def inspect_page_images(search_roots: list[Path]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for root in search_roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                continue
            if path.stem not in PAGE_STEMS and not any(f"page{stem}" in path.stem.lower() for stem in PAGE_STEMS):
                continue
            stat = path.stat()
            width: int | None = None
            height: int | None = None
            image_format: str | None = None
            color_mode: str | None = None
            try:
                from PIL import Image

                with Image.open(path) as image:
                    width, height = image.size
                    image_format = image.format
                    color_mode = image.mode
            except Exception:
                image_format = None
                color_mode = None
            records.append(
                {
                    "record_type": "page49_51_image_provenance_record",
                    "stage_id": STAGE_ID,
                    "token_block_id": TOKEN_BLOCK_ID,
                    "source_path": repo_relative(path),
                    "file_name": path.name,
                    "page_candidate": path.stem,
                    "extension": path.suffix.lower(),
                    "file_size_bytes": stat.st_size,
                    "sha256": sha256_file(path),
                    "width": width,
                    "height": height,
                    "image_format": image_format,
                    "color_mode": color_mode,
                    "raw_image_committed": False,
                    "ocr_performed": False,
                    "image_interpretation_performed": False,
                    "source_lock_status": "local_metadata_hash_locked",
                    "trusted_as_canonical": False,
                    "solve_claim": False,
                }
            )
    unique: dict[str, dict[str, Any]] = {record["source_path"]: record for record in records}
    return list(unique.values())


def inspect_text_references(search_roots: list[Path], limit: int = 32) -> list[dict[str, Any]]:
    needles = ["3N 3p 2l 36", "4F", "page 49", "pages 49", "token block", "Deep Web Hash"]
    records: list[dict[str, Any]] = []
    for root in search_roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if len(records) >= limit:
                break
            if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            if any(part in {"data/raw", ".git"} for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            hits = [needle for needle in needles if needle.lower() in text.lower()]
            if hits:
                records.append(
                    {
                        "record_type": "page49_51_text_reference_record",
                        "stage_id": STAGE_ID,
                        "token_block_id": TOKEN_BLOCK_ID,
                        "source_path": repo_relative(path),
                        "sha256": sha256_file(path),
                        "matched_terms": hits,
                        "raw_body_committed": False,
                        "source_lock_status": "metadata_hash_locked",
                        "solve_claim": False,
                    }
                )
    return records


def build_source_lock(
    *,
    search_roots: list[Path],
    out_source_lock: Path,
    out_image_provenance: Path,
    results_dir: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    image_records = inspect_page_images(search_roots)
    text_records = inspect_text_references(search_roots)
    source_status = "local_metadata_hash_locked" if len(image_records) >= 3 else "blocked_missing_page_image_metadata"
    source_lock = {
        "record_type": "page49_51_source_lock",
        "schema": "schemas/token-block/page49-51-source-lock-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "source_context": "External Stage 5AO Deep Research report plus Stage 5AP user-supplied token transcription; local page images are metadata-hash locked only.",
        "source_lock_status": source_status,
        "source_locked_page_image_count": len(image_records),
        "text_reference_record_count": len(text_records),
        "image_source_paths": [record["source_path"] for record in image_records],
        "text_reference_paths": [record["source_path"] for record in text_records],
        "raw_image_committed": False,
        "raw_body_committed": False,
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "trusted_as_canonical": False,
        "usable_as_experiment_seed": False,
        "solve_claim": False,
        "records": text_records,
    }
    provenance = {
        "record_type": "page49_51_image_provenance",
        "schema": "schemas/token-block/page49-51-image-provenance-v0.schema.json",
        "stage_id": STAGE_ID,
        "token_block_id": TOKEN_BLOCK_ID,
        "page_image_record_count": len(image_records),
        "page_candidates_present": sorted({record["page_candidate"] for record in image_records}),
        "source_variant_status": "local_metadata_only",
        "raw_image_committed": False,
        "generated_image_committed": False,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "broad_image_forensics_performed": False,
        "trusted_as_canonical": False,
        "solve_claim": False,
        "records": image_records,
        **FALSE_GUARDRAILS,
    }
    write_yaml(out_source_lock, source_lock)
    write_yaml(out_image_provenance, provenance)
    if results_dir is not None:
        write_json(results_dir / "source_lock_report.json", source_lock)
        write_json(results_dir / "image_provenance_report.json", provenance)
    return source_lock, provenance
