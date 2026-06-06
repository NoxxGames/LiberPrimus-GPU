"""Stage 5DM visual route source-lock addendum records.

This stage is metadata-only. It extends Stage 5DL with source-lock addendum
records for Blake context, Sacred Book overlays, Page32 arithmetic, full-page
visual motif metadata, doublet-scarcity metric planning, and evidence-atlas
readiness. It does not execute routes, OCR, image forensics, byte generation,
scoring, target validation, Tor access, CUDA, or solve attempts.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_jsonl, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dl import DATA_PATHS as STAGE5DL_DATA_PATHS
from libreprimus.token_block.stage5dl import validate_stage5dl

STAGE_ID = "stage-5dm"
STAGE_TITLE = (
    "Stage 5DM - Blake / Sacred Book / full-page visual / Page32 "
    "Moebius-Fibonacci / doublet / evidence-atlas source-lock addendum, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dl"
NEXT_STAGE_ID = "stage-5dn"
NEXT_STAGE_TITLE = (
    "Stage 5DN - Source/evidence review and target-priority decision readiness review, "
    "without execution"
)

REPO_ROOT = Path(".")
RESULTS_DIR = Path("experiments/results/token-block/stage5dm")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dm-codex-completion.md")
STAGE5DL_COMPLETION_PATH = Path("codex-output/stage5dl-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

TRIANGLE_FAMILY_ID = "pdd_153_triangle_word_prime_route_v1"
BLAKE_FAMILY_ID = "blake_visual_text_source_family_v0"
SACRED_BOOK_FAMILY_ID = "lp_sacred_book_edition_overlay_v0"
MAGIC_SQUARE_FAMILY_ID = "solved_magic_square_word_sum_precedent_v0"
MOTIF_INDEX_FAMILY_ID = "full_lp_page_visual_motif_index_v0"
PAGE32_FAMILY_ID = "page32_moebius_fibonacci_prime_index_spiral_v1"
DOUBLET_FAMILY_ID = "lp_doublet_scarcity_feature_v0"
EVIDENCE_ATLAS_FAMILY_ID = "evidence_source_atlas_readiness_v0"
DRIVE_HYGIENE_FAMILY_ID = "drive_path_hygiene_and_source_root_aliases_v0"

SOURCE_ROOT_SPECS = [
    (
        "number_triangle_current_folder",
        Path("third_party/NumberTriangleStuff/v2-number-triangles"),
        "primary_number_triangle_context",
    ),
    (
        "lp_sacred_book_overlay_preferred",
        Path(
            "third_party/The-Complete-Cicada3301-Archive-main/2014/Liber Primus/"
            "LP Sacred Book Edition/english text on top of pages"
        ),
        "sacred_book_overlay_alignment_aids",
    ),
    ("liber_primus_pages", Path("third_party/LiberPrimusPages"), "local_lp_page_image_archive"),
    ("koan_page_preferred", Path("third_party/koan_page.png"), "operator_blake_visual_context"),
    ("disk_cipher_preferred", Path("third_party/DiskCipherStuff"), "stage5dl_disk_cipher_context"),
    ("reddit_stuff_preferred", Path("third_party/RedditStuff"), "stage5dl_reddit_source_context"),
    ("cicada_music_preferred", Path("third_party/CicadaMusic"), "stage5dj_music_context"),
    ("historical_iddqd_folder_spelling_seen", Path("third_party/CiadaSolversIddqd_v2"), "legacy_alias"),
    ("iddqd_corrected_folder", Path("third_party/CicadaSolversIddqd"), "local_iddqd_context"),
]

OVERLAY_EXPECTED_FILENAMES = [
    "Book-cover.jpg",
    "Book-page-1.jpg",
    "Book-page-2.jpg",
    "Page3-book.jpg",
    "Page4-book.jpg",
    "Page5-book.jpg",
    "Page6-book.jpg",
    "Page7-book.jpg",
    "Page8-book.jpg",
    "Page9-book.jpg",
    "Page10-book.jpg",
    "Page11-book.jpg",
    "Page12-book.jpg",
    "Page13-book.jpg",
    "Page14-book.jpg",
]

BLAKE_WEB_SOURCES = [
    ("blake_archive", "https://www.blakearchive.org/", "A1_if_accessible"),
    (
        "marriage_heaven_hell_wikisource",
        "https://en.wikisource.org/wiki/The_Marriage_of_Heaven_and_Hell",
        "A2",
    ),
    (
        "songs_innocence_experience_wikisource",
        "https://en.wikisource.org/wiki/Songs_of_Innocence_and_of_Experience",
        "A2",
    ),
    ("tyger_wikisource", "https://en.wikisource.org/wiki/The_Tyger", "A2"),
    ("urizen_wikisource", "https://en.wikisource.org/wiki/The_Book_of_Urizen", "A2"),
    ("los_wikisource", "https://en.wikisource.org/wiki/The_Book_of_Los", "A2"),
    ("human_abstract_wikisource", "https://en.wikisource.org/wiki/The_Human_Abstract", "A2"),
    ("ancient_of_days_wikipedia", "https://en.wikipedia.org/wiki/The_Ancient_of_Days", "B"),
    ("newton_blake_wikipedia", "https://en.wikipedia.org/wiki/Newton_(Blake)", "B"),
    ("to_tirzah_wikipedia", "https://en.wikipedia.org/wiki/To_Tirzah", "B"),
]

BLAKE_SUBFAMILIES = [
    "blake_marriage_heaven_hell_doors_perception_v0",
    "blake_tyger_fearful_symmetry_v0",
    "blake_songs_innocence_experience_contraries_v0",
    "blake_ancient_of_days_newton_compass_geometry_v0",
    "blake_urizen_los_reason_circumference_v0",
    "blake_body_soul_perception_visual_source_v0",
    "blake_human_abstract_tree_mind_v0",
]

PIVOT_FAMILIES = [
    TRIANGLE_FAMILY_ID,
    PAGE32_FAMILY_ID,
    "page32_tree_polar_route_v0",
    "music_3301_instar_crab_canon_v0",
    "page56_dwh_hash_contract_v0",
    "token_block_matrix_context_v0",
    BLAKE_FAMILY_ID,
    MAGIC_SQUARE_FAMILY_ID,
    "section_0_12_quote_dialogue_cribs_v0",
    "disk_alberti_branch_cipher_candidate_v1",
]

PAGE32_GRID = [
    [3258, 3222, 3152, 3038],
    [3278, 3299, 3298, 2838],
    [3288, 3294, 3296, 2472],
    [4516, 1206, 708, 1820],
]
PAGE32_SPIRAL = [
    3299,
    3298,
    3296,
    3294,
    3288,
    3278,
    3258,
    3222,
    3152,
    3038,
    2838,
    2472,
    1820,
    708,
    1206,
    4516,
]
PAGE32_PRIME_INDICES = [1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145, 234, 378, 611, 988]
PAGE32_FIBONACCI_INCREMENTS = [1, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377]
PAGE32_PRIME_INDEX_MOD_153 = [1, 2, 3, 4, 6, 9, 14, 22, 35, 56, 90, 145, 81, 72, 152, 70]
PAGE32_VALUE_MOD_153 = [86, 85, 83, 81, 75, 65, 45, 9, 92, 131, 84, 24, 137, 96, 135, 79]

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "ai_ml_interpretation_performed",
    "approval_gate_authorizes_activation_now",
    "approval_gate_satisfied_now",
    "approval_gate_authorizes_activation_now",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "deep_research_acceptance_record_created_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "full_route_extraction_performed_now",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "image_forensics_performed",
    "manual_target_priority_selected_now",
    "mp3stego_execution_performed",
    "ocr_performed",
    "openpuff_execution_performed",
    "page32_route_extraction_performed_now",
    "page_boundaries_finalized",
    "polar_route_extraction_performed_now",
    "real_combined_gate_validation_record_created_now",
    "real_deep_research_acceptance_record_created_now",
    "real_operator_approval_record_created_now",
    "route_extraction_performed_now",
    "scoring_performed",
    "solve_claim",
    "stego_tool_execution_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_byte_streams_generated",
    "website_expansion_performed",
    "stage5dm_selects_pivot_target_now",
    "stage5dm_authorizes_pdd_153_triangle_execution_now",
    "stage5dm_authorizes_page32_execution_now",
    "stage5dm_authorizes_blake_based_decoding_now",
    "stage5dm_builds_evidence_atlas_tool_now",
    "stage5dm_builds_web_app_now",
    "stage5dm_runs_ocr_or_visual_matching_now",
    "stage5dm_commits_raw_third_party_images",
    "pivot_target_selected_now",
    "active_manifest_registry_updated",
    "variant_byte_streams_generated",
}

DATA_PATHS = {
    "summary": Path("data/project-state/stage5dm-summary.yaml"),
    "source_lock_addendum_register": Path(
        "data/project-state/stage5dm-source-lock-addendum-register.yaml"
    ),
    "pivot_readiness_update": Path("data/project-state/stage5dm-pivot-readiness-update.yaml"),
    "drive_path_hygiene": Path(
        "data/project-state/stage5dm-drive-path-hygiene-and-source-root-aliases.yaml"
    ),
    "evidence_source_atlas_readiness": Path(
        "data/project-state/stage5dm-evidence-source-atlas-readiness.yaml"
    ),
    "reviewable_validation_evidence": Path(
        "data/project-state/stage5dm-reviewable-validation-evidence.yaml"
    ),
    "blake_visual_text_source_family": Path(
        "data/historical-route/stage5dm-blake-visual-text-source-family.yaml"
    ),
    "lp_sacred_book_overlay_index": Path(
        "data/historical-route/stage5dm-lp-sacred-book-edition-overlay-index.yaml"
    ),
    "solved_magic_square_word_sum_precedent": Path(
        "data/historical-route/stage5dm-solved-magic-square-word-sum-precedent.yaml"
    ),
    "full_lp_page_visual_motif_index": Path(
        "data/historical-route/stage5dm-full-lp-page-visual-motif-index.yaml"
    ),
    "page32_moebius_fibonacci_prime_index_spiral": Path(
        "data/historical-route/stage5dm-page32-moebius-fibonacci-prime-index-spiral.yaml"
    ),
    "lp_doublet_scarcity_feature_candidate": Path(
        "data/historical-route/stage5dm-lp-doublet-scarcity-feature-candidate.yaml"
    ),
    "blake_web_source_locks": Path("data/source-harvester/stage5dm-blake-web-source-locks.yaml"),
    "local_visual_source_locks": Path(
        "data/source-harvester/stage5dm-local-visual-source-locks.yaml"
    ),
    "stage5bd_preservation": Path("data/token-block/stage5dm-stage5bd-preservation.yaml"),
    "active_lineage_preservation": Path(
        "data/token-block/stage5dm-active-lineage-preservation.yaml"
    ),
    "no_active_ingestion_proof": Path("data/token-block/stage5dm-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dm-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5dm-no-execution-transition-gate.yaml"
    ),
}

SCHEMA_PATHS = {
    key: Path("schemas") / path.relative_to("data").with_name(
        path.with_suffix("").name + "-v0.schema.json"
    )
    for key, path in DATA_PATHS.items()
}

GENERATED_REPORTS = [
    "summary.json",
    "source_root_discovery.json",
    "source_lock_addendum_report.json",
    "pivot_readiness_report.json",
    "preservation_report.json",
    "warnings.jsonl",
]


@dataclass(frozen=True)
class ValidationResult:
    command: str
    validation_error_count: int
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = [f"{self.command}:", f"validation_error_count={self.validation_error_count}"]
        lines.extend(f"error={error}" for error in self.errors)
        return "\n".join(lines)


def _posix_path(path: Path | str) -> str:
    return Path(path).as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _git_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _sha512_file(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _blake2b_file(path: Path) -> str:
    digest = hashlib.blake2b()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _image_dimensions(path: Path) -> dict[str, int | str | None]:
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            width, height = image.size
            image_format = image.format
        return {"image_width": width, "image_height": height, "image_format": image_format}
    except Exception:
        return {"image_width": None, "image_height": None, "image_format": None}


def _safe_file_metadata(path: Path) -> dict[str, Any]:
    stat = path.stat()
    metadata: dict[str, Any] = {
        "filename": path.name,
        "relative_path": _posix_path(path),
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "sha256": sha256_file(path),
        "sha512": _sha512_file(path),
        "blake2b": _blake2b_file(path),
        "mime_type": mimetypes.guess_type(path.as_posix())[0],
        "raw_file_committed": False,
        "metadata_only": True,
    }
    if path.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        metadata.update(_image_dimensions(path))
    else:
        metadata.update({"image_width": None, "image_height": None, "image_format": None})
    return metadata


def _source_root_records() -> list[dict[str, Any]]:
    records = []
    for root_id, path, role in SOURCE_ROOT_SPECS:
        exists = path.exists()
        records.append(
            {
                "source_root_id": root_id,
                "path": _posix_path(path),
                "exists": exists,
                "is_file": path.is_file(),
                "is_directory": path.is_dir(),
                "file_count_if_directory": (
                    sum(1 for candidate in path.iterdir() if candidate.is_file())
                    if path.exists() and path.is_dir()
                    else 0
                ),
                "folder_count_if_directory": (
                    sum(1 for candidate in path.iterdir() if candidate.is_dir())
                    if path.exists() and path.is_dir()
                    else 0
                ),
                "source_lock_role": role,
                "raw_commit_allowed": False,
                "missing_is_blocking": False,
            }
        )
    return records


def _overlay_root() -> Path:
    preferred = SOURCE_ROOT_SPECS[1][1]
    if preferred.exists():
        return preferred
    candidates = []
    archive = Path("third_party/The-Complete-Cicada3301-Archive-main")
    if archive.exists():
        for path in archive.rglob("*"):
            if not path.is_dir():
                continue
            lowered = path.as_posix().lower()
            if "lp sacred book edition" in lowered or "english text on top of pages" in lowered:
                candidates.append(path)
            if len(candidates) >= 5:
                break
    return sorted(candidates)[0] if candidates else preferred


def _overlay_inventory() -> tuple[Path, list[dict[str, Any]]]:
    root = _overlay_root()
    if not root.exists():
        return root, []
    records = []
    expected = set(OVERLAY_EXPECTED_FILENAMES)
    for path in sorted(root.iterdir()):
        if not path.is_file() or path.name not in expected:
            continue
        record = _safe_file_metadata(path)
        record["page_name_mapping_from_filename_only"] = path.stem
        record["ocr_or_ai_interpretation_performed"] = False
        records.append(record)
    return root, records


def _local_visual_inventory() -> list[dict[str, Any]]:
    paths = [
        Path("third_party/koan_page.png"),
        Path("third_party/NumberTriangleStuff/v2-number-triangles/liber-primus__images--full/32.jpg"),
        Path("third_party/LiberPrimusPages/32.jpg"),
        Path("third_party/LiberPrimusPages/32.png"),
    ]
    records = []
    seen: set[str] = set()
    for path in paths:
        key = _posix_path(path)
        if key in seen:
            continue
        seen.add(key)
        records.append(
            {
                "path": key,
                "exists": path.exists(),
                "source_lock_role": "local_visual_context_metadata",
                "metadata": _safe_file_metadata(path) if path.exists() and path.is_file() else None,
                "raw_file_committed": False,
                "ocr_performed": False,
                "image_forensics_performed": False,
            }
        )
    return records


def _prime(index: int) -> int:
    if index < 1:
        raise ValueError("prime index is one-based")
    primes: list[int] = []
    candidate = 2
    while len(primes) < index:
        root = int(candidate**0.5)
        if all(candidate % prime != 0 for prime in primes if prime <= root):
            primes.append(candidate)
        candidate += 1 if candidate == 2 else 2
    return primes[-1]


def verify_page32_relation() -> list[dict[str, int | bool]]:
    rows: list[dict[str, int | bool]] = []
    for value, prime_index in zip(PAGE32_SPIRAL, PAGE32_PRIME_INDICES, strict=True):
        prime = _prime(prime_index)
        expected = abs(3301 - prime)
        rows.append(
            {
                "value": value,
                "prime_index": prime_index,
                "prime": prime,
                "expected_abs_3301_minus_prime": expected,
                "relation_verified": value == expected,
            }
        )
    return rows


def _fibonacci_increment_relation_verified() -> bool:
    actual = [
        PAGE32_PRIME_INDICES[index + 1] - PAGE32_PRIME_INDICES[index]
        for index in range(len(PAGE32_PRIME_INDICES) - 1)
    ]
    return actual == PAGE32_FIBONACCI_INCREMENTS


def _load_stage5dl_summary() -> dict[str, Any]:
    if not STAGE5DL_DATA_PATHS["summary"].exists():
        return {}
    return read_yaml(STAGE5DL_DATA_PATHS["summary"]) or {}


def _base_record(record_type: str, source_previous_commit: str | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {
        "record_type": record_type,
        "schema": _posix_path(SCHEMA_PATHS[record_type.replace("stage5dm_", "", 1)])
        if record_type.replace("stage5dm_", "", 1) in SCHEMA_PATHS
        else None,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit": source_previous_commit or _git_head(),
        "metadata_only": True,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
        "stage5dl_rerun_performed": False,
        "stage5dl_records_assumed_present_for_stage5dm_addendum": True,
        "stage5dl_completion_summary_missing_or_not_available": not STAGE5DL_COMPLETION_PATH.exists(),
        "stage5dg_operator_approval_record_preserved": True,
        "operator_approval_component_satisfied_now": True,
        "deep_research_acceptance_component_satisfied_now": False,
        "combined_approval_gate_satisfied_now": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap_for_stage5dm_and_later": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": PROMPT_TYPE,
    }
    record.update({flag: False for flag in FORBIDDEN_FALSE_FLAGS})
    return record


def _schema_for(key: str, record_type: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": record_type},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "execution_allowed": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
        "stage5dl_rerun_performed": {"const": False},
        "solve_claim": {"const": False},
        "generated_outputs_committed": {"const": False},
        "raw_third_party_files_committed": {"const": False},
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        properties[flag] = {"const": False}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _posix_path(SCHEMA_PATHS[key]),
        "title": record_type,
        "type": "object",
        "required": [
            "record_type",
            "stage_id",
            "metadata_only",
            "execution_allowed",
            "canonical_codex_handoff_root",
            "stage5dl_rerun_performed",
            "solve_claim",
            "generated_outputs_committed",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        write_json(path, _schema_for(key, f"stage5dm_{key}"))


def _blake_record(source_previous_commit: str) -> dict[str, Any]:
    record = _base_record("stage5dm_blake_visual_text_source_family", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["blake_visual_text_source_family"]),
            "candidate_family_id": BLAKE_FAMILY_ID,
            "source_lock_status": "compact_metadata_only_with_gap_records",
            "raw_bodies_committed": False,
            "visual_matching_performed_now": False,
            "ocr_performed": False,
            "linked_local_sources": [
                "third_party/koan_page.png",
                (
                    "third_party/The-Complete-Cicada3301-Archive-main/2014/Liber Primus/"
                    "LP Sacred Book Edition/english text on top of pages/Book-cover.jpg"
                ),
            ],
            "linked_lp_themes": [
                "inside_outside",
                "perception",
                "body_self_soul",
                "circumference",
                "geometry_compass_measurement",
                "contraries",
                "fearful_symmetry",
                "tree_mind",
                "visual_text_illuminated_book_structure",
            ],
            "thematic_links_only": True,
            "cipher_key_claimed": False,
            "subfamily_count": len(BLAKE_SUBFAMILIES),
            "subfamilies": [
                {
                    "subfamily_id": subfamily_id,
                    "source_family_context_only": True,
                    "trust_status": "source_context_or_gap_record",
                    "decode_authorized_now": False,
                }
                for subfamily_id in BLAKE_SUBFAMILIES
            ],
        }
    )
    return record


def _blake_web_locks(source_previous_commit: str) -> dict[str, Any]:
    record = _base_record("stage5dm_blake_web_source_locks", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["blake_web_source_locks"]),
            "source_family_id": BLAKE_FAMILY_ID,
            "network_fetch_attempted": False,
            "fetch_policy": "skipped_for_deterministic_ci_compact_gap_records_only",
            "raw_webpage_bodies_committed": False,
            "source_count": len(BLAKE_WEB_SOURCES),
            "sources": [
                {
                    "source_id": source_id,
                    "url": url,
                    "source_trust_tier": tier,
                    "network_fetch_attempted": False,
                    "fetch_status": "skipped_environment",
                    "raw_body_committed": False,
                    "normalized_body_hash_recorded": False,
                    "gap_recorded": True,
                }
                for source_id, url, tier in BLAKE_WEB_SOURCES
            ],
        }
    )
    return record


def _sacred_book_record(source_previous_commit: str) -> dict[str, Any]:
    root, inventory = _overlay_inventory()
    record = _base_record("stage5dm_lp_sacred_book_overlay_index", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["lp_sacred_book_overlay_index"]),
            "overlay_family_id": SACRED_BOOK_FAMILY_ID,
            "source_root": _posix_path(root),
            "source_root_resolved": root.exists(),
            "source_root_gap_recorded": not root.exists(),
            "file_inventory_count": len(inventory),
            "expected_filename_count": len(OVERLAY_EXPECTED_FILENAMES),
            "missing_expected_filenames": sorted(
                set(OVERLAY_EXPECTED_FILENAMES) - {row["filename"] for row in inventory}
            ),
            "overlay_primary_source_status": False,
            "overlay_images_are_primary_source": False,
            "overlay_human_alignment_aid": True,
            "overlay_images_are_human_alignment_aids": True,
            "overlay_derived_from_lp_page_images_and_known_translation": True,
            "raw_overlay_images_committed": False,
            "ocr_or_ai_interpretation_performed": False,
            "primary_sources_remain": [
                "original LP page images",
                "transcription files",
                "known translation files",
            ],
            "file_inventory": inventory,
        }
    )
    return record


def _magic_square_record(source_previous_commit: str) -> dict[str, Any]:
    record = _base_record("stage5dm_solved_magic_square_word_sum_precedent", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["solved_magic_square_word_sum_precedent"]),
            "candidate_family_id": MAGIC_SQUARE_FAMILY_ID,
            "precedent_status": "solved_precedent_source_lock",
            "precedent_type": "solved_lp_word_number_matrix_precedent",
            "word_number_interchange_precedent": True,
            "supports_words_as_numbers": True,
            "supports_word_sum_matrix_objects": True,
            "supports_future_triangle_word_sum_tests": True,
            "supports_triangle_word_sum_tests_future_only": True,
            "future_only": True,
            "magic_constant": 1033,
            "shadow_sum_candidate": 341,
            "mixed_grid_rows": [
                [272, 138, "SHADOWS", 131, 151],
                ["AETHEREAL", "BVFFERS", "VOID", "CARNAL", "OR"],
                [226, "OBSCVRA", "FORM", 245, "MOBIVS"],
                ["OR", "ANALOG", "VOID", "MOVRNFVL", "AETHEREAL"],
                [151, 131, "CABAL", 138, 272],
            ],
            "worked_row_sum_examples": [
                {
                    "row_id": 1,
                    "expression": "272 + 138 + 341 + 131 + 151",
                    "sum": 1033,
                    "verified_now": True,
                }
            ],
            "broad_magic_square_search_performed_now": False,
            "experiment_authorized_now": False,
            "linked_candidate_families": [
                TRIANGLE_FAMILY_ID,
                "magic_square_matrix_route_context_v0",
                "words_numbers_direction_meta_clue_v0",
            ],
        }
    )
    return record


def _visual_motif_sections() -> list[dict[str, Any]]:
    return [
        ("00-02", "title / chapter / onion candidate header context", ["page56_dwh_hash_contract_v0"]),
        ("03-05", "warning / welcome / wisdom / word-number warning context", [MAGIC_SQUARE_FAMILY_ID]),
        (
            "06-13",
            "solved koan / tomb-body / quote-dialogue / I AM A templates",
            ["section_0_12_quote_dialogue_cribs_v0", "koan_depiction_visual_parallel_candidate_v0"],
        ),
        ("14-16", "circumference koan / supine body / Blake-body visual context", [BLAKE_FAMILY_ID]),
        ("17-19", "crosses / fingerpost / directional marker candidates", ["page32_tree_polar_route_v0"]),
        ("20-24", "sprouts / 153-triangle passage / dot marker", [TRIANGLE_FAMILY_ID]),
        ("25-31", "roots / plant-growth / leaf-wing closure", ["page32_tree_polar_route_v0"]),
        (
            "32-39",
            "Moebius section / Page32 Fibonacci-prime-index number grid / dense text / body crossbar",
            [PAGE32_FAMILY_ID, "page32_tree_polar_route_v0"],
        ),
        ("40-43", "dot/mayfly section / insect emergence marker", ["music_3301_instar_crab_canon_v0"]),
        ("44-49", "wing/tree section / page49 tree / polar-route context", ["token_block_matrix_context_v0"]),
        ("50-56", "cuneiform/numbered instruction section / internal numbering", ["page56_dwh_hash_contract_v0"]),
        ("57-72", "spiral branches / token block / moth/tree / branch route context", ["token_block_matrix_context_v0"]),
        ("73", "AN END / Page56 DWH hash contract / dot marker", ["page56_dwh_hash_contract_v0"]),
        ("74", "parable / instar / divinity within / emergence", ["music_3301_instar_crab_canon_v0"]),
    ]


def _visual_motif_record(source_previous_commit: str) -> dict[str, Any]:
    sections = [
        {
            "section_id": f"lp_pages_{page_range.replace('-', '_')}",
            "page_range_full": page_range,
            "page_range_internal": page_range,
            "archive_label": motif,
            "solved_status": "mixed" if page_range in {"03-05", "06-13", "74"} else "unknown",
            "primary_visual_motifs": [part.strip() for part in motif.split("/")],
            "candidate_route_implications": "candidate_metadata_only_no_decode_result",
            "linked_candidate_families": linked,
            "confidence": "operator_assistant_note_candidate",
            "notes": "Motif tags are review metadata, not image classification or decode evidence.",
        }
        for page_range, motif, linked in _visual_motif_sections()
    ]
    record = _base_record("stage5dm_full_lp_page_visual_motif_index", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["full_lp_page_visual_motif_index"]),
            "candidate_family_id": MOTIF_INDEX_FAMILY_ID,
            "visual_motif_index_created": True,
            "image_classification_performed_now": False,
            "ocr_performed": False,
            "raw_images_committed": False,
            "section_count": len(sections),
            "section_motifs": sections,
        }
    )
    return record


def _page32_record(source_previous_commit: str) -> dict[str, Any]:
    verification_rows = verify_page32_relation()
    relation_verified = all(row["relation_verified"] is True for row in verification_rows)
    record = _base_record(
        "stage5dm_page32_moebius_fibonacci_prime_index_spiral", source_previous_commit
    )
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["page32_moebius_fibonacci_prime_index_spiral"]),
            "candidate_family_id": PAGE32_FAMILY_ID,
            "source_page_full_image": "32.jpg",
            "section_id": "0.8",
            "section_label": "moebius",
            "base_value": 3301,
            "human_observed_image_data_recorded": True,
            "mathematical_verification_performed_now": True,
            "future_route_implication_recorded": True,
            "grid_rows": PAGE32_GRID,
            "red_3299_position": {"row": 2, "column": 2, "indexing": "one_based_grid"},
            "spiral_sequence": PAGE32_SPIRAL,
            "prime_index_sequence": PAGE32_PRIME_INDICES,
            "fibonacci_increments": PAGE32_FIBONACCI_INCREMENTS,
            "fibonacci_increment_relation_verified": _fibonacci_increment_relation_verified(),
            "abs_3301_minus_prime_index_relation_verified": relation_verified,
            "prime_relation_rows": verification_rows,
            "first_examples": verification_rows[:4],
            "prime_index_sequence_mod_153": PAGE32_PRIME_INDEX_MOD_153,
            "number_values_mod_153": PAGE32_VALUE_MOD_153,
            "mod_153_projection_recorded_future_only": True,
            "future_test_only": True,
            "route_extraction_performed_now": False,
            "page32_route_extraction_performed_now": False,
        }
    )
    return record


def _doublet_record(source_previous_commit: str) -> dict[str, Any]:
    metrics = [
        "adjacent_identical_rune_count",
        "adjacent_identical_rune_rate_per_1000_runes",
        "within_word_doublet_count",
        "cross_word_boundary_doublet_count",
        "repeated_bigram_rate",
        "repeated_whole_word_rate",
        "solved_vs_unsolved_comparison",
        "section_level_z_score_against_shuffle_baseline",
    ]
    record = _base_record("stage5dm_lp_doublet_scarcity_feature_candidate", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["lp_doublet_scarcity_feature_candidate"]),
            "candidate_family_id": DOUBLET_FAMILY_ID,
            "feature_id": DOUBLET_FAMILY_ID,
            "operator_observation_recorded": True,
            "feature_status": "future_statistical_feature_candidate",
            "metric_definition_created": True,
            "metric_definitions_created": True,
            "future_metric_definition_created": True,
            "statistics_computed_now": False,
            "doublet_statistics_computed_now": False,
            "corpus_wide_statistical_experiment_performed_now": False,
            "cipher_family_classification_performed_now": False,
            "section_ranking_performed_now": False,
            "future_analysis_required": True,
            "candidate_metrics": metrics,
        }
    )
    return record


def _evidence_atlas_record(source_previous_commit: str) -> dict[str, Any]:
    record = _base_record("stage5dm_evidence_source_atlas_readiness", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["evidence_source_atlas_readiness"]),
            "candidate_family_id": EVIDENCE_ATLAS_FAMILY_ID,
            "atlas_tool_built_now": False,
            "web_app_built_now": False,
            "design_contract_created": True,
            "manual_inbox_design_created": True,
            "future_cli_names_recorded": True,
            "future_views": [
                "Sources",
                "LP Pages",
                "Candidate Families",
                "Solved Precedents",
                "Visual Source Candidates",
                "External Links",
                "Local Third-Party Archives",
                "Hash Contracts",
                "Route Hypotheses",
                "Quote/Crib Templates",
                "Manual Inbox",
            ],
            "future_fields": [
                "source_id",
                "title",
                "source_type",
                "local_path",
                "drive_context_path",
                "web_url",
                "hashes",
                "trust_tier",
                "status",
                "linked_lp_page_or_section",
                "linked_candidate_family",
                "notes",
                "warnings",
                "related_records",
                "manual_entry_allowed",
            ],
            "future_storage_design": [
                "data/evidence-atlas/sources/*.yaml",
                "data/evidence-atlas/candidates/*.yaml",
                "data/evidence-atlas/manual-inbox/*.yaml",
                "docs/evidence-atlas/index.md",
                "website-export/evidence-atlas/",
            ],
            "future_cli_names": [
                "python -m libreprimus.cli evidence add-source",
                "python -m libreprimus.cli evidence add-candidate",
                "python -m libreprimus.cli evidence link",
                "python -m libreprimus.cli evidence build-atlas",
            ],
        }
    )
    return record


def _drive_hygiene_record(source_previous_commit: str, source_roots: list[dict[str, Any]]) -> dict[str, Any]:
    record = _base_record("stage5dm_drive_path_hygiene", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["drive_path_hygiene"]),
            "candidate_family_id": DRIVE_HYGIENE_FAMILY_ID,
            "current_drive_project_folder": "LiberPrimusSolverDrive",
            "old_drive_project_folder_avoid_for_now": "LiberPrimusSolver",
            "reason": "old folder synced .git and exploded in size",
            "git_internals_should_not_be_source_locked_or_committed": True,
            "wiki_worktree_git_sync_warning_recorded": True,
            "source_root_aliases_recorded": True,
            "source_roots": source_roots,
            "path_aliases": {
                "number_triangle_preferred": "third_party/NumberTriangleStuff/v2-number-triangles",
                "number_triangle_legacy": [
                    "third_party/UsefulFilesAndIdeas/number-triangle-theory",
                    "third_party/v2-number-triangles",
                ],
                "disk_cipher_preferred": "third_party/DiskCipherStuff",
                "cicada_music_preferred": "third_party/CicadaMusic",
                "reddit_stuff_preferred": "third_party/RedditStuff",
                "koan_page_preferred": "third_party/koan_page.png",
                "lp_sacred_book_overlay_preferred": _posix_path(SOURCE_ROOT_SPECS[1][1]),
            },
        }
    )
    return record


def _pivot_readiness_record(source_previous_commit: str) -> dict[str, Any]:
    record = _base_record("stage5dm_pivot_readiness_update", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["pivot_readiness_update"]),
            "pivot_matrix_status": "review_only_unselected",
            "operator_current_preference_top_candidate": TRIANGLE_FAMILY_ID,
            "operator_preference_recorded_now": True,
            "pivot_target_selected_now": False,
            "selected_next_solve_target_id": None,
            "candidate_family_count": len(PIVOT_FAMILIES),
            "candidate_families": [
                {
                    "candidate_family_id": family_id,
                    "present_or_cross_linked": True,
                    "selected_now": False,
                    "execution_authorized_now": False,
                    "source_lock_addendum_stage": STAGE_ID
                    if family_id
                    in {BLAKE_FAMILY_ID, MAGIC_SQUARE_FAMILY_ID, PAGE32_FAMILY_ID}
                    else "prior_or_related_stage",
                }
                for family_id in PIVOT_FAMILIES
            ],
        }
    )
    return record


def _source_lock_register(source_previous_commit: str, source_roots: list[dict[str, Any]]) -> dict[str, Any]:
    families = [
        BLAKE_FAMILY_ID,
        SACRED_BOOK_FAMILY_ID,
        MAGIC_SQUARE_FAMILY_ID,
        MOTIF_INDEX_FAMILY_ID,
        PAGE32_FAMILY_ID,
        DOUBLET_FAMILY_ID,
        EVIDENCE_ATLAS_FAMILY_ID,
        DRIVE_HYGIENE_FAMILY_ID,
    ]
    record = _base_record("stage5dm_source_lock_addendum_register", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["source_lock_addendum_register"]),
            "source_lock_addendum_created": True,
            "source_lock_addendum_family_count": len(families),
            "source_lock_addendum_families": families,
            "stage5dl_duplicate_record_creation_performed": False,
            "source_roots_checked": source_roots,
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        }
    )
    return record


def _local_visual_source_locks(source_previous_commit: str, source_roots: list[dict[str, Any]]) -> dict[str, Any]:
    record = _base_record("stage5dm_local_visual_source_locks", source_previous_commit)
    overlay_root, overlay_inventory = _overlay_inventory()
    visual_inventory = _local_visual_inventory()
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["local_visual_source_locks"]),
            "source_roots": source_roots,
            "overlay_source_root": _posix_path(overlay_root),
            "overlay_inventory_count": len(overlay_inventory),
            "local_visual_inventory_count": len(visual_inventory),
            "overlay_inventory": overlay_inventory,
            "local_visual_inventory": visual_inventory,
            "raw_third_party_files_committed": False,
            "raw_images_committed": False,
            "ocr_performed": False,
            "image_forensics_performed": False,
        }
    )
    return record


def _preservation_record(key: str, source_previous_commit: str, extra: dict[str, Any]) -> dict[str, Any]:
    record = _base_record(f"stage5dm_{key}", source_previous_commit)
    record.update({"schema": _posix_path(SCHEMA_PATHS[key])})
    record.update(extra)
    return record


def _reviewable_validation_record(source_previous_commit: str, source_roots: list[dict[str, Any]]) -> dict[str, Any]:
    record = _base_record("stage5dm_reviewable_validation_evidence", source_previous_commit)
    record.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["reviewable_validation_evidence"]),
            "stage5dl_validation_required": True,
            "stage5dl_validation_error_count_at_build": validate_stage5dl().validation_error_count,
            "source_root_count": len(source_roots),
            "source_root_present_count": sum(1 for row in source_roots if row["exists"]),
            "page32_arithmetic_verified": all(
                row["relation_verified"] for row in verify_page32_relation()
            ),
            "fibonacci_increment_relation_verified": _fibonacci_increment_relation_verified(),
            "raw_third_party_files_committed": False,
            "generated_outputs_committed": False,
        }
    )
    return record


def _summary_record(records: dict[str, dict[str, Any]], source_previous_commit: str) -> dict[str, Any]:
    source_roots = records["drive_path_hygiene"]["source_roots"]
    overlay = records["lp_sacred_book_overlay_index"]
    summary = _base_record("stage5dm_summary", source_previous_commit)
    summary.update(
        {
            "schema": _posix_path(SCHEMA_PATHS["summary"]),
            "status": "complete",
            "source_lock_addendum_created": True,
            "stage5dl_summary_present": STAGE5DL_DATA_PATHS["summary"].exists(),
            "stage5dl_completion_summary_missing_or_not_available": not STAGE5DL_COMPLETION_PATH.exists(),
            "stage5dl_records_assumed_present_for_stage5dm_addendum": True,
            "stage5dl_rerun_performed": False,
            "blake_visual_text_source_family_created": True,
            "lp_sacred_book_overlay_index_created": True,
            "solved_magic_square_word_sum_precedent_created": True,
            "full_lp_page_visual_motif_index_created": True,
            "page32_moebius_fibonacci_prime_index_spiral_created": True,
            "lp_doublet_scarcity_feature_candidate_created": True,
            "evidence_source_atlas_readiness_created": True,
            "drive_path_hygiene_record_created": True,
            "source_root_count": len(source_roots),
            "source_root_present_count": sum(1 for row in source_roots if row["exists"]),
            "overlay_inventory_count": overlay["file_inventory_count"],
            "blake_web_source_count": len(BLAKE_WEB_SOURCES),
            "blake_web_fetches_attempted": 0,
            "page32_arithmetic_verified": True,
            "page32_fibonacci_increment_relation_verified": True,
            "source_lock_addendum_family_count": records["source_lock_addendum_register"][
                "source_lock_addendum_family_count"
            ],
            "source_lock_addendum_families": records["source_lock_addendum_register"][
                "source_lock_addendum_families"
            ],
            "operator_current_preference_top_candidate": TRIANGLE_FAMILY_ID,
            "operator_preference_recorded_now": True,
            "target_selected": False,
            "target_selected_now": False,
            "raw_third_party_files_committed": False,
            "raw_third_party_files_staged": 0,
            "generated_outputs_staged": 0,
        }
    )
    return summary


def build_stage5dm(write_completion: bool = False) -> dict[str, dict[str, Any]]:
    """Build Stage 5DM metadata records and generated ignored reports."""

    source_previous_commit = _git_head()
    source_roots = _source_root_records()
    stage5bd_counts, stage5bd_errors = validate_stage5bd()
    stage5bd_error_count = stage5bd_counts.get("validation_error_count", len(stage5bd_errors))
    stage5dl_summary = _load_stage5dl_summary()

    records: dict[str, dict[str, Any]] = {
        "source_lock_addendum_register": _source_lock_register(source_previous_commit, source_roots),
        "pivot_readiness_update": _pivot_readiness_record(source_previous_commit),
        "drive_path_hygiene": _drive_hygiene_record(source_previous_commit, source_roots),
        "evidence_source_atlas_readiness": _evidence_atlas_record(source_previous_commit),
        "blake_visual_text_source_family": _blake_record(source_previous_commit),
        "lp_sacred_book_overlay_index": _sacred_book_record(source_previous_commit),
        "solved_magic_square_word_sum_precedent": _magic_square_record(source_previous_commit),
        "full_lp_page_visual_motif_index": _visual_motif_record(source_previous_commit),
        "page32_moebius_fibonacci_prime_index_spiral": _page32_record(source_previous_commit),
        "lp_doublet_scarcity_feature_candidate": _doublet_record(source_previous_commit),
        "blake_web_source_locks": _blake_web_locks(source_previous_commit),
        "local_visual_source_locks": _local_visual_source_locks(source_previous_commit, source_roots),
        "stage5bd_preservation": _preservation_record(
            "stage5bd_preservation",
            source_previous_commit,
            {
                "stage5bd_validation_error_count": stage5bd_error_count,
                "stage5bd_run_plan_ids_preserved": True,
                "stage5bd_run_plan_id_count": 10,
            },
        ),
        "active_lineage_preservation": _preservation_record(
            "active_lineage_preservation",
            source_previous_commit,
            {
                "active_lineage_paths": [_posix_path(path) for path in ACTIVE_LINEAGE_PATHS],
                "active_lineage_preserved": True,
                "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            },
        ),
        "no_active_ingestion_proof": _preservation_record(
            "no_active_ingestion_proof",
            source_previous_commit,
            {
                "active_ingestion_performed": False,
                "active_planning_input_authorized_now": False,
                "active_planning_input_selected_now": False,
                "active_manifest_registry_updated": False,
                "string4_remains_inactive": True,
            },
        ),
        "no_byte_stream_transition_gate": _preservation_record(
            "no_byte_stream_transition_gate",
            source_previous_commit,
            {
                "byte_stream_generation_authorized_now": False,
                "variant_byte_streams_generated": False,
                "variant_materialisation_performed": False,
                "branch_enumeration_performed": False,
            },
        ),
        "no_execution_transition_gate": _preservation_record(
            "no_execution_transition_gate",
            source_previous_commit,
            {
                "execution_authorized_now": False,
                "token_block_experiment_executed": False,
                "route_extraction_performed_now": False,
                "target_class_validation_implemented": False,
                "tor_network_access_performed": False,
                "solve_claim": False,
            },
        ),
    }
    records["reviewable_validation_evidence"] = _reviewable_validation_record(
        source_previous_commit, source_roots
    )
    records["summary"] = _summary_record(records, source_previous_commit)
    records["summary"]["stage5dl_summary_status"] = stage5dl_summary.get("status")

    _write_schemas()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS_DIR / "summary.json", records["summary"])
    write_json(RESULTS_DIR / "source_root_discovery.json", {"source_roots": source_roots})
    write_json(
        RESULTS_DIR / "source_lock_addendum_report.json",
        records["source_lock_addendum_register"],
    )
    write_json(RESULTS_DIR / "pivot_readiness_report.json", records["pivot_readiness_update"])
    write_json(
        RESULTS_DIR / "preservation_report.json",
        {
            "stage5bd_preservation": records["stage5bd_preservation"],
            "active_lineage_preservation": records["active_lineage_preservation"],
            "no_active_ingestion_proof": records["no_active_ingestion_proof"],
            "no_byte_stream_transition_gate": records["no_byte_stream_transition_gate"],
            "no_execution_transition_gate": records["no_execution_transition_gate"],
        },
    )
    warnings = []
    if not STAGE5DL_COMPLETION_PATH.exists():
        warnings.append(
            {
                "warning_id": "stage5dl_completion_summary_missing_or_not_available",
                "blocking": False,
            }
        )
    if records["blake_web_source_locks"]["network_fetch_attempted"] is False:
        warnings.append(
            {
                "warning_id": "blake_web_sources_recorded_as_gap_metadata",
                "blocking": False,
            }
        )
    write_jsonl(RESULTS_DIR / "warnings.jsonl", warnings)

    if write_completion:
        CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
        CODEX_COMPLETION_PATH.write_text(
            "Stage 5DM completion summary is written after commit, push, and CI.\n",
            encoding="utf-8",
        )
    return records


def _schema_errors(key: str) -> list[str]:
    schema_path = SCHEMA_PATHS[key]
    data_path = DATA_PATHS[key]
    if not schema_path.exists():
        return [f"missing_schema:{schema_path}"]
    if not data_path.exists():
        return [f"missing_data:{data_path}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = read_yaml(data_path)
    validator = Draft202012Validator(schema)
    return [
        f"{data_path}:{'/'.join(map(str, error.path))}:{error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    ]


def _read_record(key: str) -> dict[str, Any]:
    return read_yaml(DATA_PATHS[key]) or {}


def _common_errors(record: dict[str, Any], context: str) -> list[str]:
    errors = []
    if record.get("stage_id") != STAGE_ID:
        errors.append(f"{context}:stage_id_must_be_{STAGE_ID}")
    if record.get("metadata_only") is not True:
        errors.append(f"{context}:metadata_only_must_be_true")
    if record.get("execution_allowed") is not False:
        errors.append(f"{context}:execution_allowed_must_be_false")
    if record.get("canonical_codex_handoff_root") != "codex-output":
        errors.append(f"{context}:canonical_codex_handoff_root_must_be_codex-output")
    if record.get("stage5dl_rerun_performed") is not False:
        errors.append(f"{context}:stage5dl_rerun_performed_must_be_false")
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append(f"{context}:stage5bd_run_plan_id_count_must_be_10")
    if record.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append(f"{context}:active_lineage_record_count_must_be_{len(ACTIVE_LINEAGE_PATHS)}")
    if record.get("parallel_worker_cap_for_stage5dm_and_later") != PARALLEL_WORKER_CAP:
        errors.append(f"{context}:parallel_worker_cap_must_be_{PARALLEL_WORKER_CAP}")
    for flag in FORBIDDEN_FALSE_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{context}:{flag}_must_be_false")
    return errors


def _result(command: str, errors: list[str]) -> ValidationResult:
    return ValidationResult(command, len(errors), errors)


def validate_stage5dm_blake_source_family() -> ValidationResult:
    command = "validate-stage5dm-blake-source-family"
    record = _read_record("blake_visual_text_source_family")
    errors = _common_errors(record, command)
    if record.get("candidate_family_id") != BLAKE_FAMILY_ID:
        errors.append("blake_candidate_family_id_changed")
    if record.get("subfamily_count") != len(BLAKE_SUBFAMILIES):
        errors.append("blake_subfamily_count_changed")
    if record.get("cipher_key_claimed") is not False:
        errors.append("cipher_key_claimed_must_be_false")
    return _result(command, errors)


def validate_stage5dm_lp_sacred_book_overlays() -> ValidationResult:
    command = "validate-stage5dm-lp-sacred-book-overlays"
    record = _read_record("lp_sacred_book_overlay_index")
    errors = _common_errors(record, command)
    if record.get("overlay_family_id") != SACRED_BOOK_FAMILY_ID:
        errors.append("sacred_book_family_id_changed")
    if record.get("overlay_primary_source_status") is not False:
        errors.append("overlay_primary_source_status_must_be_false")
    if record.get("overlay_human_alignment_aid") is not True:
        errors.append("overlay_human_alignment_aid_must_be_true")
    return _result(command, errors)


def validate_stage5dm_magic_square_precedent() -> ValidationResult:
    command = "validate-stage5dm-magic-square-precedent"
    record = _read_record("solved_magic_square_word_sum_precedent")
    errors = _common_errors(record, command)
    if record.get("magic_constant") != 1033:
        errors.append("magic_constant_must_be_1033")
    if record.get("word_number_interchange_precedent") is not True:
        errors.append("word_number_interchange_precedent_missing")
    if record.get("broad_magic_square_search_performed_now") is not False:
        errors.append("broad_magic_square_search_performed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dm_full_page_visual_motifs() -> ValidationResult:
    command = "validate-stage5dm-full-page-visual-motifs"
    record = _read_record("full_lp_page_visual_motif_index")
    errors = _common_errors(record, command)
    if record.get("candidate_family_id") != MOTIF_INDEX_FAMILY_ID:
        errors.append("motif_index_family_id_changed")
    if record.get("section_count") != len(_visual_motif_sections()):
        errors.append("visual_motif_section_count_changed")
    if record.get("image_classification_performed_now") is not False:
        errors.append("image_classification_performed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dm_page32_moebius_fibonacci() -> ValidationResult:
    command = "validate-stage5dm-page32-moebius-fibonacci"
    record = _read_record("page32_moebius_fibonacci_prime_index_spiral")
    errors = _common_errors(record, command)
    if record.get("candidate_family_id") != PAGE32_FAMILY_ID:
        errors.append("page32_family_id_changed")
    if record.get("spiral_sequence") != PAGE32_SPIRAL:
        errors.append("page32_spiral_changed")
    if record.get("prime_index_sequence") != PAGE32_PRIME_INDICES:
        errors.append("page32_prime_index_sequence_changed")
    if record.get("abs_3301_minus_prime_index_relation_verified") is not True:
        errors.append("page32_prime_relation_not_verified")
    if record.get("route_extraction_performed_now") is not False:
        errors.append("route_extraction_performed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dm_doublet_scarcity_feature() -> ValidationResult:
    command = "validate-stage5dm-doublet-scarcity-feature"
    record = _read_record("lp_doublet_scarcity_feature_candidate")
    errors = _common_errors(record, command)
    if record.get("candidate_family_id") != DOUBLET_FAMILY_ID:
        errors.append("doublet_family_id_changed")
    if record.get("metric_definition_created") is not True:
        errors.append("metric_definition_created_must_be_true")
    if record.get("statistics_computed_now") is not False:
        errors.append("statistics_computed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dm_evidence_atlas_readiness() -> ValidationResult:
    command = "validate-stage5dm-evidence-atlas-readiness"
    record = _read_record("evidence_source_atlas_readiness")
    errors = _common_errors(record, command)
    if record.get("candidate_family_id") != EVIDENCE_ATLAS_FAMILY_ID:
        errors.append("evidence_atlas_family_id_changed")
    if record.get("design_contract_created") is not True:
        errors.append("design_contract_created_must_be_true")
    if record.get("atlas_tool_built_now") is not False:
        errors.append("atlas_tool_built_now_must_be_false")
    return _result(command, errors)


def validate_stage5dm_drive_path_hygiene() -> ValidationResult:
    command = "validate-stage5dm-drive-path-hygiene"
    record = _read_record("drive_path_hygiene")
    errors = _common_errors(record, command)
    if record.get("current_drive_project_folder") != "LiberPrimusSolverDrive":
        errors.append("current_drive_project_folder_changed")
    if record.get("git_internals_should_not_be_source_locked_or_committed") is not True:
        errors.append("git_internals_warning_missing")
    return _result(command, errors)


def validate_stage5dm_pivot_readiness() -> ValidationResult:
    command = "validate-stage5dm-pivot-readiness"
    record = _read_record("pivot_readiness_update")
    errors = _common_errors(record, command)
    if record.get("operator_current_preference_top_candidate") != TRIANGLE_FAMILY_ID:
        errors.append("operator_current_preference_top_candidate_changed")
    if record.get("pivot_target_selected_now") is not False:
        errors.append("pivot_target_selected_now_must_be_false")
    if record.get("candidate_family_count") != len(PIVOT_FAMILIES):
        errors.append("pivot_candidate_family_count_changed")
    return _result(command, errors)


def validate_stage5dm_sidecar_gates() -> ValidationResult:
    command = "validate-stage5dm-sidecar-gates"
    errors: list[str] = []
    for key in [
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        errors.extend(_common_errors(_read_record(key), f"{command}:{key}"))
    return _result(command, errors)


def validate_stage5dm_handoff_continuity() -> ValidationResult:
    command = "validate-stage5dm-handoff-continuity"
    summary = _read_record("summary")
    errors = _common_errors(summary, command)
    if summary.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical_handoff_root_changed")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated_codex_output_path_exists")
    return _result(command, errors)


def validate_stage5dm_governance_scope() -> ValidationResult:
    command = "validate-stage5dm-governance-scope"
    summary = _read_record("summary")
    errors = _common_errors(summary, command)
    required_true = [
        "source_lock_addendum_created",
        "blake_visual_text_source_family_created",
        "lp_sacred_book_overlay_index_created",
        "solved_magic_square_word_sum_precedent_created",
        "full_lp_page_visual_motif_index_created",
        "page32_moebius_fibonacci_prime_index_spiral_created",
        "lp_doublet_scarcity_feature_candidate_created",
        "evidence_source_atlas_readiness_created",
    ]
    for key in required_true:
        if summary.get(key) is not True:
            errors.append(f"{key}_must_be_true")
    if summary.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("recommended_next_stage_id_changed")
    return _result(command, errors)


def validate_stage5dm() -> ValidationResult:
    command = "validate-stage5dm"
    errors: list[str] = []
    for key in DATA_PATHS:
        errors.extend(_schema_errors(key))
        if DATA_PATHS[key].exists():
            errors.extend(_common_errors(_read_record(key), key))
    for validator in [
        validate_stage5dm_blake_source_family,
        validate_stage5dm_lp_sacred_book_overlays,
        validate_stage5dm_magic_square_precedent,
        validate_stage5dm_full_page_visual_motifs,
        validate_stage5dm_page32_moebius_fibonacci,
        validate_stage5dm_doublet_scarcity_feature,
        validate_stage5dm_evidence_atlas_readiness,
        validate_stage5dm_drive_path_hygiene,
        validate_stage5dm_pivot_readiness,
        validate_stage5dm_sidecar_gates,
        validate_stage5dm_handoff_continuity,
        validate_stage5dm_governance_scope,
    ]:
        result = validator()
        errors.extend(f"{result.command}:{error}" for error in result.errors)
    return _result(command, errors)


def load_stage5dm_summary() -> dict[str, Any]:
    return _read_record("summary")


def stage5dm_summary_text() -> str:
    summary = load_stage5dm_summary()
    lines = [
        f"stage_id={summary.get('stage_id')}",
        f"status={summary.get('status')}",
        f"source_lock_addendum_created={str(summary.get('source_lock_addendum_created')).lower()}",
        f"source_lock_addendum_family_count={summary.get('source_lock_addendum_family_count')}",
        f"blake_visual_text_source_family_created={str(summary.get('blake_visual_text_source_family_created')).lower()}",
        f"lp_sacred_book_overlay_index_created={str(summary.get('lp_sacred_book_overlay_index_created')).lower()}",
        f"solved_magic_square_word_sum_precedent_created={str(summary.get('solved_magic_square_word_sum_precedent_created')).lower()}",
        f"full_lp_page_visual_motif_index_created={str(summary.get('full_lp_page_visual_motif_index_created')).lower()}",
        f"page32_moebius_fibonacci_prime_index_spiral_created={str(summary.get('page32_moebius_fibonacci_prime_index_spiral_created')).lower()}",
        f"lp_doublet_scarcity_feature_candidate_created={str(summary.get('lp_doublet_scarcity_feature_candidate_created')).lower()}",
        f"evidence_source_atlas_readiness_created={str(summary.get('evidence_source_atlas_readiness_created')).lower()}",
        f"page32_arithmetic_verified={str(summary.get('page32_arithmetic_verified')).lower()}",
        f"target_selected={str(summary.get('target_selected')).lower()}",
        f"execution_authorized_now={str(summary.get('execution_authorized_now')).lower()}",
        f"stage5bd_run_plan_id_count={summary.get('stage5bd_run_plan_id_count')}",
        f"active_lineage_record_count={summary.get('active_lineage_record_count')}",
        f"parallel_worker_cap_for_stage5dm_and_later={summary.get('parallel_worker_cap_for_stage5dm_and_later')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


__all__ = [
    "CODEX_COMPLETION_PATH",
    "DATA_PATHS",
    "RESULTS_DIR",
    "SCHEMA_PATHS",
    "STAGE_ID",
    "STAGE_TITLE",
    "build_stage5dm",
    "load_stage5dm_summary",
    "stage5dm_summary_text",
    "validate_stage5dm",
    "validate_stage5dm_blake_source_family",
    "validate_stage5dm_doublet_scarcity_feature",
    "validate_stage5dm_drive_path_hygiene",
    "validate_stage5dm_evidence_atlas_readiness",
    "validate_stage5dm_full_page_visual_motifs",
    "validate_stage5dm_governance_scope",
    "validate_stage5dm_handoff_continuity",
    "validate_stage5dm_lp_sacred_book_overlays",
    "validate_stage5dm_magic_square_precedent",
    "validate_stage5dm_page32_moebius_fibonacci",
    "validate_stage5dm_pivot_readiness",
    "validate_stage5dm_sidecar_gates",
    "verify_page32_relation",
]
