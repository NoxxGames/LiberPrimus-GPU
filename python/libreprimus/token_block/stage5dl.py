"""Stage 5DL triangle/disk/quote/koan source-lock records.

This stage is metadata-only.  It inventories local ignored source roots and
writes compact source-lock records; it does not execute route extraction,
HTML/PDF/image tooling, crib attacks, byte-stream generation, or scoring.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_jsonl, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dk import DATA_PATHS as STAGE5DK_DATA_PATHS

STAGE_ID = "stage-5dl"
STAGE_TITLE = "Stage 5DL - Triangle / Disk / Quote / Koan source-lock refresh, without execution"
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dk"
SOURCE_PREVIOUS_STAGE_ISSUE = 146
SOURCE_PREVIOUS_STAGE_CI_RUN = 27036919161
SOURCE_PREVIOUS_STAGE_PYTEST_COUNT = 2634
NEXT_STAGE_ID = "stage-5dm"
NEXT_STAGE_TITLE = "Stage 5DM - Target-priority decision package, without execution"
NEXT_PROMPT_TYPE = "codex_metadata_implementation"

REPO_ROOT = Path(".")
RESULTS_DIR = Path("experiments/results/token-block/stage5dl")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dl-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

TRIANGLE_FAMILY_ID = "pdd_153_triangle_word_prime_route_v1"
TRIANGLE_SUBFAMILIES = [
    "pdd_153_triangle_shell_route_v1",
    "pdd_153_triangle_way_anchor_route_v1",
    "pdd_153_triangle_prime_mask_route_v1",
    "pdd_153_triangle_2016_prime_layer_route_v1",
    "pdd_153_triangle_fibonacci_prime_index_route_v1",
    "pdd_153_triangle_56311_wynn_way_route_v1",
]

CANDIDATE_FAMILIES = [
    TRIANGLE_FAMILY_ID,
    *TRIANGLE_SUBFAMILIES,
    "disk_alberti_branch_cipher_candidate_v1",
    "section_0_12_quote_dialogue_cribs_v0",
    "koan_depiction_visual_parallel_candidate_v0",
]

PIVOT_OPTIONS = [
    ("pdd_153_triangle_word_prime_route_first", "top_operator_preference_pending_decision"),
    ("page32_tree_polar_route_first", "high"),
    ("music_3301_instar_crab_canon_first", "high_or_medium_high"),
    ("page56_dwh_hash_contract_first", "medium_high_final_target"),
    ("token_block_first", "medium"),
    ("disk_alberti_branch_cipher_first", "support_candidate_not_primary"),
    ("section_0_12_quote_dialogue_cribs_first", "support_candidate_not_primary"),
    ("defer_for_more_source_locking", "available"),
]

PRESENT_PRIMES_UNDER_153 = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
]
MISSING_PRIMES_UNDER_153 = [
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
]

SOURCE_ROOT_SPECS = [
    ("number_triangle_primary", Path("third_party/NumberTriangleStuff"), True, None),
    (
        "number_triangle_primary_content_root",
        Path("third_party/NumberTriangleStuff/v2-number-triangles"),
        False,
        Path("third_party/NumberTriangleStuff"),
    ),
    (
        "number_triangle_legacy_usefulfiles",
        Path("third_party/UsefulFilesAndIdeas/number-triangle-theory"),
        False,
        Path("third_party/NumberTriangleStuff"),
    ),
    (
        "number_triangle_legacy_top_level_v2",
        Path("third_party/v2-number-triangles"),
        False,
        Path("third_party/NumberTriangleStuff"),
    ),
    ("disk_cipher_primary", Path("third_party/DiskCipherStuff"), True, None),
    ("disk_cipher_spelling_hazard", Path("third_party/DiskCypherStuff"), False, Path("third_party/DiskCipherStuff")),
    ("reddit_primary", Path("third_party/RedditStuff"), True, None),
    ("koan_page_primary", Path("third_party/koan_page.png"), True, None),
    ("iddqd_v2_misspelled_archive", Path("third_party/CiadaSolversIddqd_v2"), False, None),
    ("iddqd_v2_corrected_archive", Path("third_party/CicadaSolversIddqd_v2"), False, None),
]

REDDIT_EXPECTED_FOLDERS = {
    "FibonacciSequence": "fibonacci_sequence_3301.jpeg",
    "PrimeGPSums": "prime_gp_sums.jpg",
    "Layered_primes": "layered_primes.jpg",
}

LP_PAGE_CANDIDATE_PATHS = [
    Path("third_party/NumberTriangleStuff/v2-number-triangles/liber-primus__images--full/14.jpg"),
    Path("third_party/NumberTriangleStuff/v2-number-triangles/liber-primus__images--full/15.jpg"),
    Path("third_party/NumberTriangleStuff/v2-number-triangles/liber-primus__images--full/16.jpg"),
    Path("third_party/CiadaSolversIddqd_v2/liber-primus__images--full/14.jpg"),
    Path("third_party/CiadaSolversIddqd_v2/liber-primus__images--full/15.jpg"),
    Path("third_party/CiadaSolversIddqd_v2/liber-primus__images--full/16.jpg"),
]

DATA_PATHS = {
    "summary": Path("data/project-state/stage5dl-summary.yaml"),
    "next_stage_decision": Path("data/project-state/stage5dl-next-stage-decision.yaml"),
    "pivot_readiness_update": Path("data/project-state/stage5dl-pivot-readiness-update.yaml"),
    "candidate_family_priority_update": Path(
        "data/project-state/stage5dl-candidate-family-priority-update.yaml"
    ),
    "reviewable_validation_evidence": Path(
        "data/project-state/stage5dl-reviewable-validation-evidence.yaml"
    ),
    "reviewability_gap_register": Path("data/project-state/stage5dl-reviewability-gap-register.yaml"),
    "local_source_path_aliases": Path("data/project-state/stage5dl-local-source-path-aliases.yaml"),
    "source_digest_index": Path("data/project-state/stage5dl-source-digest-index.yaml"),
    "number_triangle_source_lock": Path(
        "data/historical-route/stage5dl-number-triangle-v1-source-lock.yaml"
    ),
    "triangle_way_anchor": Path("data/historical-route/stage5dl-triangle-way-anchor-source-lock.yaml"),
    "triangle_prime_mask": Path("data/historical-route/stage5dl-triangle-prime-mask-source-lock.yaml"),
    "triangle_2016_prime_layer": Path(
        "data/historical-route/stage5dl-triangle-2016-prime-layer-source-lock.yaml"
    ),
    "triangle_fibonacci_prime_index": Path(
        "data/historical-route/stage5dl-triangle-fibonacci-prime-index-source-lock.yaml"
    ),
    "triangle_56311_wynn_way": Path(
        "data/historical-route/stage5dl-triangle-56311-wynn-way-source-lock.yaml"
    ),
    "disk_alberti_branch": Path("data/historical-route/stage5dl-disk-alberti-branch-source-lock.yaml"),
    "quote_dialogue_cribs": Path("data/historical-route/stage5dl-section-0-12-quote-dialogue-cribs.yaml"),
    "koan_visual_parallel": Path("data/historical-route/stage5dl-koan-depiction-visual-parallel.yaml"),
    "cross_family_route_evidence_index": Path(
        "data/historical-route/stage5dl-cross-family-route-evidence-index.yaml"
    ),
    "local_source_lock_register": Path(
        "data/source-harvester/stage5dl-local-source-lock-register.yaml"
    ),
    "reddit_thread_image_source_lock_register": Path(
        "data/source-harvester/stage5dl-reddit-thread-image-source-lock-register.yaml"
    ),
    "number_triangle_local_archive_crosswalk": Path(
        "data/source-harvester/stage5dl-number-triangle-local-archive-crosswalk.yaml"
    ),
    "disk_cipher_local_archive_crosswalk": Path(
        "data/source-harvester/stage5dl-disk-cipher-local-archive-crosswalk.yaml"
    ),
    "koan_page_local_source_lock": Path(
        "data/source-harvester/stage5dl-koan-page-local-source-lock.yaml"
    ),
    "stage5dg_approval_preservation": Path(
        "data/token-block/stage5dl-stage5dg-approval-preservation.yaml"
    ),
    "stage5bd_plan_preservation": Path("data/token-block/stage5dl-stage5bd-plan-preservation.yaml"),
    "active_lineage_preservation": Path("data/token-block/stage5dl-active-lineage-preservation.yaml"),
    "no_active_ingestion_proof": Path("data/token-block/stage5dl-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dl-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path("data/token-block/stage5dl-no-execution-transition-gate.yaml"),
}

SCHEMA_PATHS = {
    key: Path("schemas") / path.relative_to("data").with_name(
        path.with_suffix("").name + "-v0.schema.json"
    )
    for key, path in DATA_PATHS.items()
}

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "ai_ml_interpretation_performed",
    "approval_gate_authorizes_activation_now",
    "approval_gate_satisfied_now",
    "audio_stego_performed_now",
    "audio_transcription_performed_now",
    "audio_waveform_decode_performed_now",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "canonical_transcription_changed",
    "codex_output_used",
    "combined_approval_gate_authorizes_activation_now",
    "combined_approval_gate_satisfied_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "deep_research_acceptance_created_now",
    "deep_research_acceptance_component_satisfied_now",
    "dry_run_ingestion_authorized_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "experiment_authorized_now",
    "experiment_executed_now",
    "experiments_authorized_now",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "historical_route_execution_performed",
    "html_tool_execution_performed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "manifest_supersession_authorized_now",
    "manifest_supersession_performed",
    "meaning_claimed_now",
    "method_status_upgraded",
    "model_claims_validated_now",
    "mp3stego_execution_performed",
    "music_cue_experiment_executed_now",
    "music_experiment_authorized_now",
    "music_experiment_executed_now",
    "music_route_extraction_performed_now",
    "music_score_ocr_performed_now",
    "music_sheet_rendered_now",
    "musicxml_conversion_performed_now",
    "new_active_planning_input_created",
    "new_real_operator_approval_record_created_in_stage5dl",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_target_priority_decision_created_now",
    "page_boundaries_finalized",
    "pdf_ocr_performed_now",
    "pdf_rendering_performed_now",
    "pivot_target_selected_now",
    "polar_route_extraction_performed_now",
    "raw_body_committed",
    "raw_disk_cipher_files_committed",
    "raw_koan_image_committed",
    "raw_music_file_committed",
    "raw_number_triangle_files_committed",
    "raw_pdf_committed",
    "raw_reddit_images_committed",
    "real_byte_stream_generated",
    "real_deep_research_acceptance_record_created_now",
    "route_extraction_performed_now",
    "score_to_cipher_experiment_performed_now",
    "score_to_cipher_transform_performed_now",
    "scoring_performed",
    "solve_claim",
    "spectrogram_decode_performed_now",
    "spectrogram_stego_analysis_performed_now",
    "stego_tool_execution_performed",
    "string4_active_input_allowed",
    "string4_added_to_active_dry_run_inputs",
    "string4_added_to_stage5bd_run_plan_ids",
    "string4_byte_stream_generation_allowed",
    "string4_dry_run_ingestion_allowed_now",
    "string4_execution_input_allowed",
    "string4_sidecar_active",
    "string4_sidecar_planning_ingestion_activated",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "token_block_transform_performed_now",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "visual_match_claimed_now",
    "website_expansion_performed",
    "waveform_analysis_performed_now",
    "way_anchor_route_executed_now",
}

REQUIRED_TRUE_FLAGS = {
    "metadata_only": True,
    "stage5dg_operator_approval_record_preserved": True,
    "real_operator_approval_record_created_now": False,
    "operator_approval_component_satisfied_now": True,
    "stage5di_recent_clue_source_lock_preserved": True,
    "stage5dj_music_source_lock_preserved": True,
}

GENERATED_REPORTS = [
    "summary.json",
    "source_lock_report.json",
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
        lines = [
            f"{self.command}:",
            f"validation_error_count={self.validation_error_count}",
        ]
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


def _file_kind(path: Path) -> str:
    ext = path.suffix.lower()
    if ext in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return "image"
    if ext in {".txt", ".md", ".csv", ".json", ".yaml", ".yml"}:
        return "text"
    if ext == ".pdf":
        return "pdf"
    if ext == ".rtf":
        return "rtf"
    if ext in {".html", ".htm"}:
        return "html"
    if ext in {".zip", ".tar", ".gz", ".7z", ".rar"}:
        return "archive"
    return "other"


def _blake2b_file(path: Path) -> str:
    digest = hashlib.blake2b()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _sha512_file(path: Path) -> str:
    digest = hashlib.sha512()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _image_dimensions(path: Path) -> dict[str, int | str | None]:
    if _file_kind(path) != "image":
        return {"image_width": None, "image_height": None, "image_format": None}
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            width, height = image.size
            image_format = image.format
        return {"image_width": width, "image_height": height, "image_format": image_format}
    except Exception:
        return {"image_width": None, "image_height": None, "image_format": None}


def _source_file_metadata(path: Path) -> dict[str, Any]:
    stat = path.stat()
    metadata = {
        "source_file_name": path.name,
        "source_path": _posix_path(path),
        "extension": path.suffix.lower(),
        "file_kind": _file_kind(path),
        "size_bytes": stat.st_size,
        "modified_utc": datetime.fromtimestamp(stat.st_mtime, UTC)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "sha256": sha256_file(path),
        "sha512": _sha512_file(path),
        "blake2b": _blake2b_file(path),
        "raw_file_committed": False,
        "metadata_only": True,
    }
    metadata.update(_image_dimensions(path))
    return metadata


def _iter_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    if root.is_file():
        return [root]
    return sorted(path for path in root.rglob("*") if path.is_file())


def _read_short_url(path: Path) -> str | None:
    if not path.exists() or path.stat().st_size > 1024:
        return None
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if "\n" in text:
        text = text.splitlines()[0].strip()
    return text if text.startswith(("http://", "https://")) else None


def _line_count(path: Path) -> int | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        return len(path.read_text(encoding="utf-8", errors="replace").splitlines())
    except OSError:
        return None


def _source_presence_status(path: Path, preferred: bool, superseded_by: Path | None) -> str:
    if not path.exists():
        return "absent"
    if superseded_by is not None and superseded_by.exists():
        return "superseded"
    if preferred:
        return "local_ignored_cache_present"
    return "alias_only"


def _source_root_aliases() -> list[dict[str, Any]]:
    records = []
    for alias_id, path, preferred, superseded_by in SOURCE_ROOT_SPECS:
        records.append(
            {
                "alias_id": alias_id,
                "path": _posix_path(path),
                "exists_locally": path.exists(),
                "is_file": path.is_file(),
                "is_dir": path.is_dir(),
                "preferred_for_stage5dl": preferred and path.exists(),
                "superseded_by": _posix_path(superseded_by) if superseded_by else None,
                "source_presence_status": _source_presence_status(path, preferred, superseded_by),
                "raw_files_committed": False,
            }
        )
    return records


def _preferred_inventory() -> list[dict[str, Any]]:
    roots = [
        Path("third_party/NumberTriangleStuff"),
        Path("third_party/DiskCipherStuff"),
        Path("third_party/RedditStuff"),
        Path("third_party/koan_page.png"),
    ]
    seen: set[str] = set()
    records: list[dict[str, Any]] = []
    for root in roots:
        for path in _iter_files(root):
            posix = _posix_path(path)
            if posix in seen:
                continue
            seen.add(posix)
            records.append(_source_file_metadata(path))
    return records


def _files_under(prefix: str, inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [row for row in inventory if row["source_path"].startswith(prefix)]


def _files_by_basename(inventory: list[dict[str, Any]], names: set[str]) -> list[dict[str, Any]]:
    return [row for row in inventory if row["source_file_name"] in names]


def _lp_page_candidates(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_path = {row["source_path"]: row for row in inventory}
    candidates = []
    for path in LP_PAGE_CANDIDATE_PATHS:
        row = by_path.get(_posix_path(path))
        candidates.append(
            {
                "path": _posix_path(path),
                "exists_locally": row is not None or path.exists(),
                "metadata": row if row is not None else (_source_file_metadata(path) if path.exists() else None),
                "visual_analysis_performed": False,
                "ocr_performed": False,
            }
        )
    return candidates


def _load_stage5dk_summary() -> dict[str, Any]:
    path = STAGE5DK_DATA_PATHS["summary"]
    if not path.exists():
        raise FileNotFoundError("Stage 5DL requires completed data/project-state/stage5dk-summary.yaml")
    summary = read_yaml(path) or {}
    if summary.get("stage_id") != SOURCE_PREVIOUS_STAGE_ID or summary.get("status") != "complete":
        raise ValueError("Stage 5DK summary is absent or incomplete; Stage 5DL must wait.")
    return summary


def _base_record(record_type: str, source_previous_commit: str | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {
        "record_type": record_type,
        "schema": _posix_path(
            SCHEMA_PATHS.get(
                record_type.removeprefix("stage5dl_"),
                Path("schemas/token-block/stage5dl-generic-v0.schema.json"),
            )
        ),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit": source_previous_commit or _git_head(),
        "source_previous_stage_issue": SOURCE_PREVIOUS_STAGE_ISSUE,
        "source_previous_stage_ci_run": SOURCE_PREVIOUS_STAGE_CI_RUN,
        "source_previous_stage_pytest_count": SOURCE_PREVIOUS_STAGE_PYTEST_COUNT,
        "stage5dk_summary_status": "complete",
        "metadata_only": True,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
        "stage5dg_operator_approval_record_preserved": True,
        "real_operator_approval_record_created_now": False,
        "operator_approval_component_satisfied_now": True,
        "stage5di_recent_clue_source_lock_preserved": True,
        "stage5dj_music_source_lock_preserved": True,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": 8,
        "parallel_worker_cap_for_stage5dl_and_later": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
    }
    for flag in sorted(FORBIDDEN_FALSE_FLAGS):
        record[flag] = False
    return record


def _record_with_schema_key(record_type: str, key: str, source_previous_commit: str) -> dict[str, Any]:
    record = _base_record(record_type, source_previous_commit)
    record["schema"] = _posix_path(SCHEMA_PATHS[key])
    return record


def _pivot_options() -> list[dict[str, Any]]:
    return [
        {
            "option_id": option_id,
            "qualitative_priority": priority,
            "selected_now": False,
            "execution_authorized_now": False,
        }
        for option_id, priority in PIVOT_OPTIONS
    ]


def _build_reddit_records(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for folder, image_name in REDDIT_EXPECTED_FOLDERS.items():
        folder_path = Path("third_party/RedditStuff") / folder
        image_path = folder_path / image_name
        url_path = folder_path / "url.txt"
        image_meta = next(
            (row for row in inventory if row["source_path"] == _posix_path(image_path)),
            None,
        )
        url_meta = next((row for row in inventory if row["source_path"] == _posix_path(url_path)), None)
        records.append(
            {
                "reddit_folder": folder,
                "folder_path": _posix_path(folder_path),
                "folder_exists": folder_path.exists(),
                "url_txt_path": _posix_path(url_path),
                "url_txt_exists": url_path.exists(),
                "url": _read_short_url(url_path),
                "image_path": _posix_path(image_path),
                "image_exists": image_path.exists(),
                "image_metadata": image_meta,
                "url_metadata": url_meta,
                "network_fetch_performed": False,
                "raw_reddit_images_committed": False,
            }
        )
    return records


def _build_records() -> dict[str, Any]:
    stage5dk_summary = _load_stage5dk_summary()
    source_previous_commit = _git_head()
    stage5bd_counts, stage5bd_errors = validate_stage5bd()
    aliases = _source_root_aliases()
    inventory = _preferred_inventory()
    reddit_records = _build_reddit_records(inventory)
    lp_page_candidates = _lp_page_candidates(inventory)

    number_triangle_present = Path("third_party/NumberTriangleStuff").exists()
    disk_present = Path("third_party/DiskCipherStuff").exists()
    reddit_present = Path("third_party/RedditStuff").exists()
    koan_present = Path("third_party/koan_page.png").exists()
    triangle_fallback_present = any(
        Path(path).exists()
        for path in [
            "third_party/UsefulFilesAndIdeas/number-triangle-theory",
            "third_party/v2-number-triangles",
        ]
    )
    if not number_triangle_present and not triangle_fallback_present:
        raise FileNotFoundError("NumberTriangleStuff and triangle fallback folders are absent.")

    summary = _record_with_schema_key("stage5dl_summary", "summary", source_previous_commit)
    summary.update(
        {
            "status": "complete",
            "source_previous_stage_status_consumed": stage5dk_summary.get("status"),
            "source_previous_stage_commit_observed_at_build": source_previous_commit,
            "source_previous_stage_issue_observed": SOURCE_PREVIOUS_STAGE_ISSUE,
            "source_previous_stage_ci_run_observed": SOURCE_PREVIOUS_STAGE_CI_RUN,
            "operator_future_priority_preference_recorded": True,
            "operator_stated_preference_observed": True,
            "operator_preferred_future_target_family_id": TRIANGLE_FAMILY_ID,
            "operator_preference_records_future_priority_only": True,
            "operator_preference_selects_target_now": False,
            "operator_preference_authorizes_execution_now": False,
            "selected_next_solve_target_id": None,
            "pivot_target_selected_now": False,
            "target_priority_decision_created_now": False,
            "operator_target_priority_decision_created_now": False,
            "number_triangle_v1_source_locked": number_triangle_present,
            "disk_cipher_bridge_source_locked": disk_present,
            "reddit_prime_thread_images_source_locked": reddit_present,
            "quote_dialogue_cribs_source_locked": True,
            "koan_depiction_visual_candidate_source_locked": koan_present,
            "candidate_family_count_added_or_updated": len(CANDIDATE_FAMILIES),
            "candidate_families_added_or_updated": CANDIDATE_FAMILIES,
            "raw_third_party_files_staged": 0,
            "generated_outputs_staged": 0,
            "codex_output_used": False,
        }
    )

    next_stage = _record_with_schema_key("stage5dl_next_stage_decision", "next_stage_decision", source_previous_commit)
    next_stage.update(
        {
            "selected_next_stage_id": NEXT_STAGE_ID,
            "selected_next_stage_title": NEXT_STAGE_TITLE,
            "selected_next_prompt_type": NEXT_PROMPT_TYPE,
            "target_priority_decision_required_next": True,
            "operator_target_priority_decision_required_next": True,
            "stage5dl_selects_target_now": False,
        }
    )

    pivot = _record_with_schema_key("stage5dl_pivot_readiness_update", "pivot_readiness_update", source_previous_commit)
    pivot.update(
        {
            "priority_matrix_status": "review_only_unselected",
            "selected_next_solve_target_id": None,
            "target_priority_decision_required_next": True,
            "operator_target_priority_decision_required_next": True,
            "pivot_option_count": len(PIVOT_OPTIONS),
            "pivot_options": _pivot_options(),
            "priority_rationale": [
                "153_word_body_equals_t17",
                "center_word_41_is_wynn",
                "telnet_prime_sequence_contains_41",
                "present_prime_mask_hits_center_and_single_rune_anchor",
                "2016_layered_prime_values_mod_153_hit_anchor_positions",
                "disk_56311_sequence_from_center_hits_way_word52",
                "way_anchor_derived_from_heading_minus_reversed_word52",
                "operator_stated_triangle_should_be_top_priority",
            ],
            "priority_caveats": [
                "no_route_extraction_performed",
                "no_negative_controls_run",
                "way_result_requires_geometric_word52_justification",
                "disk_model_high_degrees_of_freedom",
                "quote_cribs_are_candidate_not_plaintext",
                "koan_visual_correspondence_not_image_matched",
            ],
        }
    )

    priority_update = _record_with_schema_key(
        "stage5dl_candidate_family_priority_update",
        "candidate_family_priority_update",
        source_previous_commit,
    )
    priority_update.update(
        {
            "candidate_family_count": len(CANDIDATE_FAMILIES),
            "candidate_families": [
                {
                    "candidate_family_id": family_id,
                    "candidate_family_status": "source_lock_only",
                    "operator_future_priority_preference": (
                        "top_priority_after_source_locking"
                        if family_id == TRIANGLE_FAMILY_ID
                        else "supporting_or_subfamily_context"
                    ),
                    "selected_now": False,
                    "execution_authorized_now": False,
                    "usable_as_experiment_seed_now": False,
                }
                for family_id in CANDIDATE_FAMILIES
            ],
            "formal_target_priority_decision_created_now": False,
        }
    )

    gaps = []
    for path, present, blocking in [
        ("third_party/NumberTriangleStuff", number_triangle_present, True),
        ("third_party/DiskCipherStuff", disk_present, False),
        ("third_party/RedditStuff", reddit_present, False),
        ("third_party/koan_page.png", koan_present, False),
    ]:
        if not present:
            gaps.append(
                {
                    "gap_id": path.replace("/", "_").replace(".", "_"),
                    "source_path": path,
                    "gap_status": "source_missing_blocking" if blocking else "source_missing_non_blocking",
                    "blocks_stage5dl": blocking,
                }
            )
    gaps.extend(
        [
            {
                "gap_id": "triangle_claims_need_future_reproducible_transcription_crosswalk",
                "gap_status": "reviewability_gap",
                "blocks_stage5dl": False,
            },
            {
                "gap_id": "quote_dialogue_cribs_need_future_crib_test",
                "gap_status": "future_review_required",
                "blocks_stage5dl": False,
            },
            {
                "gap_id": "koan_visual_similarity_unverified_by_image_forensics",
                "gap_status": "future_review_required",
                "blocks_stage5dl": False,
            },
        ]
    )

    reviewability = _record_with_schema_key(
        "stage5dl_reviewability_gap_register", "reviewability_gap_register", source_previous_commit
    )
    reviewability.update(
        {
            "gap_count": len(gaps),
            "blocking_gap_count": sum(1 for gap in gaps if gap.get("blocks_stage5dl")),
            "gaps": gaps,
        }
    )

    validation_evidence = _record_with_schema_key(
        "stage5dl_reviewable_validation_evidence",
        "reviewable_validation_evidence",
        source_previous_commit,
    )
    validation_evidence.update(
        {
            "stage5dk_predecessor_validated": True,
            "stage5dk_summary_path": _posix_path(STAGE5DK_DATA_PATHS["summary"]),
            "stage5dk_summary_status": stage5dk_summary.get("status"),
            "stage5bd_validation_error_count": stage5bd_counts.get(
                "validation_error_count",
                len(stage5bd_errors),
            ),
            "local_source_root_count": len(aliases),
            "local_source_file_inventory_count": len(inventory),
            "reddit_folder_count": len(reddit_records),
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "validation_scope": "metadata_only_no_execution",
        }
    )

    alias_record = _record_with_schema_key(
        "stage5dl_local_source_path_aliases", "local_source_path_aliases", source_previous_commit
    )
    alias_record.update(
        {
            "alias_count": len(aliases),
            "path_aliases": aliases,
            "number_triangle_preferred_path": "third_party/NumberTriangleStuff",
            "disk_cipher_preferred_path": "third_party/DiskCipherStuff",
            "ciada_spelling_hazard_recorded": True,
        }
    )

    digest_index = _record_with_schema_key("stage5dl_source_digest_index", "source_digest_index", source_previous_commit)
    digest_index.update(
        {
            "source_file_count": len(inventory),
            "source_file_records": inventory,
            "raw_files_committed": False,
            "generated_outputs_committed": False,
        }
    )

    number_files = _files_under("third_party/NumberTriangleStuff", inventory)
    number_triangle = _record_with_schema_key(
        "stage5dl_pdd_153_triangle_word_prime_route_v1",
        "number_triangle_source_lock",
        source_previous_commit,
    )
    number_triangle.update(
        {
            "candidate_family_id": TRIANGLE_FAMILY_ID,
            "candidate_family_type": "word_triangle_prime_route_candidate",
            "candidate_family_status": "source_lock_only",
            "operator_future_priority_preference": "top_priority_after_source_locking",
            "operator_priority_preference": "top_priority_after_source_locking",
            "formal_target_priority_decision_created_now": False,
            "selected_now": False,
            "execution_authorized_now": False,
            "usable_as_experiment_seed_now": False,
            "source_section_id": "0.6.1",
            "source_heading_runes": "\u16c7\u16de\u16a6",
            "source_transcription_required": True,
            "triangle_body_section_id": "0.6.1",
            "triangle_heading_runes": "\u16c7\u16de\u16a6",
            "triangle_body_word_count": 153,
            "body_word_count": 153,
            "body_word_count_equals_triangle_number": True,
            "triangle_number_identity": "T17",
            "triangle_number_n": 17,
            "triangle_row_count": 17,
            "triangle_center_word_index": 41,
            "center_word_index": 41,
            "triangle_center_coordinate": "row_9_col_5",
            "center_word_coordinate": {"row": 9, "column": 5},
            "triangle_center_rune": "\u16b9",
            "center_word_runes": "\u16b9",
            "center_word_latin": "W",
            "single_rune_word_positions": [25, 41, 53, 91, 106],
            "single_rune_positions_claimed": [25, 41, 53, 91, 106],
            "subfamilies": TRIANGLE_SUBFAMILIES,
            "source_paths_used_for_verification": sorted({row["source_path"] for row in number_files[:30]}),
            "verified_from_local_transcription": False,
            "verification_status": "operator_assistant_prior_analysis_pending_reverification",
            "source_lock_status": "source_lock_only",
            "route_extraction_performed_now": False,
        }
    )

    way_anchor = _record_with_schema_key(
        "stage5dl_pdd_153_triangle_way_anchor_route_v1",
        "triangle_way_anchor",
        source_previous_commit,
    )
    way_anchor.update(
        {
            "candidate_family_id": "pdd_153_triangle_way_anchor_route_v1",
            "source_lock_only": True,
            "heading_values_ordinal_gp": [13, 23, 2],
            "word52_runes": "\u16b3\u16e0\u16b7",
            "word52_values_ordinal_gp": [5, 28, 6],
            "word52_reversed_values_ordinal_gp": [6, 28, 5],
            "heading_minus_reversed_word52_mod29": [7, 24, 26],
            "derived_runes": "\u16b9\u16aa\u16a3",
            "derived_latin": "WAY",
            "way_result": "WAY",
            "way_result_runes": "\u16b9\u16aa\u16a3",
            "calculation_status": "source_locked_candidate",
            "ordinal_values_not_prime_values": True,
            "heading_minus_reversed_word52_mod29_claim_recorded": True,
            "word52_selection_requires_geometric_justification": True,
            "false_positive_controls_required_later": True,
            "used_as_key_now": False,
            "route_extraction_performed_now": False,
        }
    )

    prime_mask = _record_with_schema_key(
        "stage5dl_pdd_153_triangle_prime_mask_route_v1",
        "triangle_prime_mask",
        source_previous_commit,
    )
    prime_mask.update(
        {
            "candidate_family_id": "pdd_153_triangle_prime_mask_route_v1",
            "source_claim_type": "fandom_possible_hints_telnet_primes",
            "source_lock_only": True,
            "mask_applies_to_body_word_positions_1_to_153": True,
            "present_prime_positions_under_153": PRESENT_PRIMES_UNDER_153,
            "missing_prime_positions_under_153": MISSING_PRIMES_UNDER_153,
            "present_prime_count_under_153": len(PRESENT_PRIMES_UNDER_153),
            "missing_prime_count_under_153": len(MISSING_PRIMES_UNDER_153),
            "present_prime_sequence_ends_before_jump_to_1229": True,
            "present_prime_sequence_contains_41": True,
            "prime_mask_route_status": "candidate_not_executed",
            "prime_41_hits_triangle_center": True,
            "word_41_is_triangle_center": True,
            "prime_53_hits_single_rune_anchor": True,
            "word_53_single_rune_anchor": True,
            "prime_71_same_column_as_41": True,
            "word_71_same_column_as_word_41": True,
            "prime_71_coordinate": "row_12_col_5",
            "future_extraction_required": True,
            "extraction_performed_now": False,
            "verification_status": "pending_reverification",
        }
    )

    prime_layer = _record_with_schema_key(
        "stage5dl_pdd_153_triangle_2016_prime_layer_route_v1",
        "triangle_2016_prime_layer",
        source_previous_commit,
    )
    prime_layer.update(
        {
            "candidate_family_id": "pdd_153_triangle_2016_prime_layer_route_v1",
            "source_claim_type": "reddit_and_fandom_2016_layered_prime_gp_sums",
            "source_lock_only": True,
            "applies_to_triangle_by_mod_153_projection": True,
            "mod_projection_is_candidate_only": True,
            "layered_prime_values": [2819, 2039, 1277],
            "layered_prime_indices": [410, 309, 206],
            "layered_prime_index_differences": [101, 103],
            "layered_prime_values_mod_153": [65, 50, 53],
            "layered_prime_indices_mod_153": [104, 3, 53],
            "index_difference_positions_under_153": [101, 103],
            "layered_prime_values_count": 3,
            "layered_prime_indexes_count": 3,
            "index_difference_count": 2,
            "index_differences_are_101_103": True,
            "index_differences_in_missing_prime_mask": True,
            "source_lock_status": "source_lock_only",
            "why_it_matters": [
                "59_is_the_17th_prime_in_2016_analysis_context",
                "153_equals_T17_for_triangle_body",
                "1277_mod_153_and_206_mod_153_hit_53_single_rune_anchor",
                "101_and_103_are_in_missing_prime_mask_under_153",
            ],
            "future_control_test_required": True,
            "route_extraction_performed_now": False,
        }
    )

    fib = _record_with_schema_key(
        "stage5dl_pdd_153_triangle_fibonacci_prime_index_route_v1",
        "triangle_fibonacci_prime_index",
        source_previous_commit,
    )
    fib.update(
        {
            "candidate_family_id": "pdd_153_triangle_fibonacci_prime_index_route_v1",
            "source_claim_type": "reddit_fibonacci_sequence_3301_image_and_thread",
            "source_lock_only": True,
            "base_prime": 3301,
            "base_prime_index": 464,
            "fibonacci_walk_start_prime": 3301,
            "fibonacci_walk_start_prime_index": 464,
            "fibonacci_gaps_observed": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144],
            "highlighted_prime_index_rows": [
                {
                    "label": "2016_sentences_1_3_plus_f",
                    "fibonacci_gap": 13,
                    "prime_index": 431,
                    "prime_value": 3001,
                },
                {
                    "label": "2016_sentence_4",
                    "fibonacci_gap": 21,
                    "prime_index": 410,
                    "prime_value": 2819,
                },
                {
                    "label": "2016_remainder_minus_f",
                    "fibonacci_gap": 34,
                    "prime_index": 376,
                    "prime_value": 2579,
                },
                {
                    "label": "2017_message",
                    "fibonacci_gap": 55,
                    "prime_index": 321,
                    "prime_value": 2131,
                },
            ],
            "highlighted_row_count": 4,
            "highlighted_prime_indices_mod_153": [125, 104, 70, 15],
            "highlighted_prime_values_mod_153": [94, 65, 131, 142],
            "source_lock_status": "source_lock_only",
            "uses_f_adjustment": True,
            "plus_f_minus_f_manipulation_is_weakest_link": True,
            "f_adjustment_caveat_recorded": True,
            "fibonacci_candidate_confidence": "medium_low_to_medium",
            "selected_now": False,
            "route_extraction_performed_now": False,
        }
    )

    bridge = _record_with_schema_key(
        "stage5dl_pdd_153_triangle_56311_wynn_way_route_v1",
        "triangle_56311_wynn_way",
        source_previous_commit,
    )
    bridge.update(
        {
            "candidate_family_id": "pdd_153_triangle_56311_wynn_way_route_v1",
            "source_lock_only": True,
            "source_bridge": "disk_alberti_branch_cipher_candidate_v0",
            "bridge_type": "disk_sequence_to_triangle_center_to_way_anchor",
            "disk_sequence": [5, 6, 3, 11],
            "sequence_56311_recorded": True,
            "disk_sequence_source_family": "disk_alberti_branch_cipher_candidate_v0",
            "cumulative_from_one": [5, 11, 14, 25],
            "cumulative_from_center_41": [46, 52, 55, 66],
            "cumulative_from_anchor_25": [30, 36, 39, 50],
            "center_word_41_is_wynn": True,
            "wynn_center_bridge_recorded": True,
            "center_plus_sequence_hits_word52": True,
            "sequence_from_center_hits_word52": True,
            "word52_is_way_anchor_word": True,
            "word52_way_anchor_recorded": True,
            "disk_model_flexibility_caveat_recorded": True,
            "programmatic_reproduction_required_later": True,
            "candidate_summary": "W/WYNN at center plus 56311 reaches word52, which derives WAY",
            "source_lock_status": "source_lock_only",
            "route_extraction_performed_now": False,
        }
    )

    disk_names = {
        "Alberti_LP.pdf",
        "Claudes_Alberti_LP_summary.md.pdf",
        "Ivis_Alberti_LP summary.pdf",
        "test1.pdf",
        "Bookcover_inv.pdf",
        "Rule changes from base M.pdf",
        "Alberti_statisticsGr.rtf",
        "message_bodies.txt",
        "alberti_v26_branchfix.html",
        "39_1_clear.webp",
        "P39_1row_ext.webp",
        "p.39_new.webp",
    }
    disk_files = _files_under("third_party/DiskCipherStuff", inventory)
    disk = _record_with_schema_key(
        "stage5dl_disk_alberti_branch_cipher_candidate_v0",
        "disk_alberti_branch",
        source_previous_commit,
    )
    disk.update(
        {
            "candidate_family_id": "disk_alberti_branch_cipher_candidate_v0",
            "source_root": "third_party/DiskCipherStuff",
            "source_lock_only": True,
            "files_present_count": len(disk_files),
            "required_named_file_records": _files_by_basename(disk_files, disk_names),
            "branching_file_records": [
                row for row in disk_files if row["source_file_name"].lower().startswith("branching")
            ],
            "candidate_concepts_recorded": [
                "Alberti-style disk",
                "WYNN special handling",
                "5-6-3-11 sequence",
                "dots as branch points",
                "circumference_rotation_flip_concepts",
                "p39_fragments_euler_totient_circumference_wynn_prime_number_fish_phi",
            ],
            "html_tool_execution_performed_now": False,
            "html_execution_performed": False,
            "rtf_active_content_execution_performed_now": False,
            "pdf_rendering_performed_now": False,
            "image_forensics_performed": False,
            "disk_cipher_experiment_executed": False,
            "model_claims_validated_now": False,
            "wynn_claim_recorded": True,
            "branching_claim_recorded": True,
            "sequence_56311_claim_recorded": True,
            "p39_claims_recorded_as_community_theory": True,
            "disk_candidate_confidence": "low_to_medium",
            "manual_branching_false_positive_risk": "high",
            "requires_programmatic_reproduction_before_experiment": True,
            "requires_future_programmatic_reproduction": True,
        }
    )

    quote = _record_with_schema_key(
        "stage5dl_section_0_12_quote_dialogue_cribs_v0",
        "quote_dialogue_cribs",
        source_previous_commit,
    )
    quote.update(
        {
            "candidate_family_id": "section_0_12_quote_dialogue_cribs_v0",
            "source_section_id": "0.12.0",
            "source_lock_only": True,
            "quote_dialogue_structure_candidate": True,
            "known_plaintext_solved_koan_precedent_recorded": True,
            "solved_quote_templates": [
                "HE SAID",
                "HE ANSWERED",
                "THE MASTER SAID",
                "ASKED THE MASTER",
                "REPLIED THE MASTER",
                "I AM A",
            ],
            "solved_precedents": [
                {
                    "section_id": "0.2",
                    "translation_line_id": "a-koan-a-man",
                    "plaintext_excerpt_short": "HE ASKED AGAIN / REPLIED THE MASTER / I AM A...",
                    "phrase_type": ["he_answered", "i_am_a_quote_start", "replied_the_master"],
                },
                {
                    "section_id": "0.4",
                    "translation_line_id": "a-koan-during-circumference",
                    "plaintext_excerpt_short": "THE MASTER SAID / HE SAID",
                    "phrase_type": ["he_said", "the_master_said"],
                },
            ],
            "candidates": [
                {
                    "candidate_id": "section_0_12_candidate_a",
                    "section_id": "0.12.0",
                    "line_id_if_available": None,
                    "position_relative_to_quote": "before_opening_quote",
                    "ciphertext": "\u16c1\u16bb \u16df\u16da\u16be\u16cf",
                    "ciphertext_words": ["\u16c1\u16bb", "\u16df\u16da\u16be\u16cf"],
                    "ciphertext_word_lengths": [2, 4],
                    "proposed_plaintext": "HE SAID",
                    "proposed_plaintext_word_lengths": [2, 4],
                    "word_length_pattern": [2, 4],
                    "quote_boundary_relation": "immediately_before_opening_quote",
                    "reasoning_summary": "short quote-boundary phrase matches solved koan dialogue template",
                    "confidence": "medium",
                    "requires_future_crib_test": True,
                    "solved_now": False,
                },
                {
                    "candidate_id": "section_0_12_candidate_b",
                    "section_id": "0.12.0",
                    "line_id_if_available": None,
                    "position_relative_to_quote": "after_closing_quote",
                    "ciphertext": "\u16a0\u16a2 \u16c9\u16a0\u16ab\u16de\u16a0\u16e1\u16c4\u16be",
                    "ciphertext_words": [
                        "\u16a0\u16a2",
                        "\u16c9\u16a0\u16ab\u16de\u16a0\u16e1\u16c4\u16be",
                    ],
                    "ciphertext_word_lengths": [2, 8],
                    "proposed_plaintext": "HE ANSWERED",
                    "proposed_plaintext_word_lengths": [2, 8],
                    "word_length_pattern": [2, 8],
                    "quote_boundary_relation": "immediately_after_large_quote",
                    "reasoning_summary": "length and position match solved dialogue-response precedent",
                    "confidence": "medium_high",
                    "requires_future_crib_test": True,
                    "solved_now": False,
                },
            ],
            "he_said_candidate_recorded": True,
            "he_answered_candidate_recorded": True,
            "candidate_a_proposed_plaintext": "HE SAID",
            "candidate_b_proposed_plaintext": "HE ANSWERED",
            "i_am_a_quote_template_relevant": True,
            "i_am_a_precedent_recorded": True,
            "i_am_a_used_as_future_crib_only": True,
            "i_am_a_applied_now": False,
            "the_master_said_candidate_status": "weak_pending_direct_boundary_match",
            "cribs_applied_now": False,
            "decryption_performed_now": False,
            "known_plaintext_attack_performed_now": False,
            "crib_solved_now": False,
            "quote_crib_solved_now": False,
            "route_extraction_performed_now": False,
        }
    )

    koan_meta = next(
        (row for row in inventory if row["source_path"] == "third_party/koan_page.png"),
        None,
    )
    koan = _record_with_schema_key(
        "stage5dl_koan_page_depiction_correspondence_v0",
        "koan_visual_parallel",
        source_previous_commit,
    )
    koan.update(
        {
            "candidate_family_id": "koan_depiction_visual_parallel_candidate_v0",
            "source_path": "third_party/koan_page.png",
            "koan_page_source_path": "third_party/koan_page.png",
            "source_lock_only": True,
            "source_metadata": koan_meta,
            "visual_correspondence_status": "candidate_only",
            "operator_claim_recorded": True,
            "operator_observed_similarity_to_lp_body_depictions": True,
            "visual_similarity_claim_source": "operator_observation",
            "visual_similarity_claim_status": "human_observation_unverified",
            "visual_similarity_not_verified_by_image_forensics": True,
            "lp_page_14_15_16_candidate_paths_checked": True,
            "lp_page_14_15_16_candidate_records": lp_page_candidates,
            "solved_koan_relationships": [
                "0.2 A KOAN",
                "0.4 A KOAN",
                "quote-dialogue structure",
                "I AM A quote forms",
                "body/figure depictions",
            ],
            "ocr_performed": False,
            "image_forensics_performed": False,
            "ai_ml_interpretation_performed": False,
            "visual_match_claimed_now": False,
        }
    )

    cross_family = _record_with_schema_key(
        "stage5dl_cross_family_route_evidence_index",
        "cross_family_route_evidence_index",
        source_previous_commit,
    )
    cross_family.update(
        {
            "candidate_family_count": len(CANDIDATE_FAMILIES),
            "primary_future_family_id": TRIANGLE_FAMILY_ID,
            "supporting_family_ids": [
                "disk_alberti_branch_cipher_candidate_v1",
                "section_0_12_quote_dialogue_cribs_v0",
                "koan_depiction_visual_parallel_candidate_v0",
            ],
            "dinkus_visual_marker_candidate_status": "preserved_low_confidence",
            "red_grid_marker_candidate_status": "preserved_low_to_medium_confidence",
            "used_for_route_now": False,
            "target_priority_decision_created_now": False,
        }
    )

    local_source_register = _record_with_schema_key(
        "stage5dl_local_source_lock_register",
        "local_source_lock_register",
        source_previous_commit,
    )
    local_source_register.update(
        {
            "source_root_count": len(aliases),
            "source_roots": aliases,
            "source_file_count": len(inventory),
            "source_file_records": inventory,
            "raw_files_committed": False,
        }
    )

    reddit_register = _record_with_schema_key(
        "stage5dl_reddit_thread_image_source_lock_register",
        "reddit_thread_image_source_lock_register",
        source_previous_commit,
    )
    reddit_register.update(
        {
            "reddit_folder_count": len(reddit_records),
            "reddit_folders": reddit_records,
            "network_fetch_performed": False,
            "raw_reddit_images_committed": False,
        }
    )

    number_crosswalk = _record_with_schema_key(
        "stage5dl_number_triangle_local_archive_crosswalk",
        "number_triangle_local_archive_crosswalk",
        source_previous_commit,
    )
    number_crosswalk.update(
        {
            "preferred_source_root": "third_party/NumberTriangleStuff",
            "preferred_source_root_present": number_triangle_present,
            "legacy_source_roots": [
                row
                for row in aliases
                if row["alias_id"]
                in {
                    "number_triangle_primary_content_root",
                    "number_triangle_legacy_usefulfiles",
                    "number_triangle_legacy_top_level_v2",
                    "iddqd_v2_misspelled_archive",
                    "iddqd_v2_corrected_archive",
                }
            ],
            "file_count_under_preferred_root": len(number_files),
            "message_file_line_count": _line_count(
                Path("third_party/NumberTriangleStuff/v2-number-triangles/messages.txt")
            ),
            "raw_number_triangle_files_committed": False,
        }
    )

    disk_crosswalk = _record_with_schema_key(
        "stage5dl_disk_cipher_local_archive_crosswalk",
        "disk_cipher_local_archive_crosswalk",
        source_previous_commit,
    )
    disk_crosswalk.update(
        {
            "preferred_source_root": "third_party/DiskCipherStuff",
            "preferred_source_root_present": disk_present,
            "nested_content_root_observed": "third_party/DiskCipherStuff/DiskCipherStuff",
            "disk_cypher_spelling_alias_present": Path("third_party/DiskCypherStuff").exists(),
            "file_count_under_preferred_root": len(disk_files),
            "html_files_recorded_not_executed": [
                row["source_path"] for row in disk_files if row["file_kind"] == "html"
            ],
            "raw_disk_cipher_files_committed": False,
        }
    )

    koan_source_lock = _record_with_schema_key(
        "stage5dl_koan_page_local_source_lock",
        "koan_page_local_source_lock",
        source_previous_commit,
    )
    koan_source_lock.update(
        {
            "source_path": "third_party/koan_page.png",
            "source_present": koan_present,
            "source_metadata": koan_meta,
            "raw_koan_image_committed": False,
            "image_forensics_performed": False,
            "ocr_performed": False,
        }
    )

    stage5dg_preservation = _record_with_schema_key(
        "stage5dl_stage5dg_approval_preservation",
        "stage5dg_approval_preservation",
        source_previous_commit,
    )
    stage5dg_preservation.update(
        {
            "stage5dg_operator_approval_record_preserved": True,
            "real_operator_approval_record_created_now": False,
            "operator_approval_component_satisfied_now": True,
            "deep_research_acceptance_present_now": False,
            "combined_approval_gate_satisfied_now": False,
            "activation_authorized_now": False,
            "stage5dg_record_path": "data/token-block/stage5dg-real-operator-approval-record.yaml",
        }
    )

    stage5bd_plan = _record_with_schema_key(
        "stage5dl_stage5bd_plan_preservation",
        "stage5bd_plan_preservation",
        source_previous_commit,
    )
    stage5bd_plan.update(
        {
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_validation_error_count": stage5bd_counts.get(
                "validation_error_count",
                len(stage5bd_errors),
            ),
            "stage5bd_run_plan_ids_preserved": True,
            "stage5bd_dry_run_records_remain_valid": True,
            "string4_added_to_stage5bd_run_plan_ids": False,
        }
    )

    active_lineage = _record_with_schema_key(
        "stage5dl_active_lineage_preservation",
        "active_lineage_preservation",
        source_previous_commit,
    )
    active_lineage.update(
        {
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_paths": [_posix_path(path) for path in ACTIVE_LINEAGE_PATHS],
            "correct_stage5aw_path": _posix_path(CORRECT_STAGE5AW_PATH),
            "incorrect_stage5aw_path": _posix_path(INCORRECT_STAGE5AW_PATH),
            "active_lineage_preserved": True,
        }
    )

    no_active = _record_with_schema_key(
        "stage5dl_no_active_ingestion_proof",
        "no_active_ingestion_proof",
        source_previous_commit,
    )
    no_active.update(
        {
            "active_ingestion_authorized": False,
            "active_planning_input_authorized": False,
            "active_planning_input_selected": False,
            "string4_active": False,
            "no_active_ingestion_gate_closed": True,
        }
    )

    no_byte = _record_with_schema_key(
        "stage5dl_no_byte_stream_transition_gate",
        "no_byte_stream_transition_gate",
        source_previous_commit,
    )
    no_byte.update(
        {
            "byte_stream_generation_authorized": False,
            "byte_stream_generated": False,
            "variant_byte_streams_generated": False,
            "no_byte_stream_gate_closed": True,
        }
    )

    no_execution = _record_with_schema_key(
        "stage5dl_no_execution_transition_gate",
        "no_execution_transition_gate",
        source_previous_commit,
    )
    no_execution.update(
        {
            "execution_authorized": False,
            "execution_performed": False,
            "route_extraction_performed_now": False,
            "no_execution_gate_closed": True,
        }
    )

    records = {
        "summary": summary,
        "next_stage_decision": next_stage,
        "pivot_readiness_update": pivot,
        "candidate_family_priority_update": priority_update,
        "reviewable_validation_evidence": validation_evidence,
        "reviewability_gap_register": reviewability,
        "local_source_path_aliases": alias_record,
        "source_digest_index": digest_index,
        "number_triangle_source_lock": number_triangle,
        "triangle_way_anchor": way_anchor,
        "triangle_prime_mask": prime_mask,
        "triangle_2016_prime_layer": prime_layer,
        "triangle_fibonacci_prime_index": fib,
        "triangle_56311_wynn_way": bridge,
        "disk_alberti_branch": disk,
        "quote_dialogue_cribs": quote,
        "koan_visual_parallel": koan,
        "cross_family_route_evidence_index": cross_family,
        "local_source_lock_register": local_source_register,
        "reddit_thread_image_source_lock_register": reddit_register,
        "number_triangle_local_archive_crosswalk": number_crosswalk,
        "disk_cipher_local_archive_crosswalk": disk_crosswalk,
        "koan_page_local_source_lock": koan_source_lock,
        "stage5dg_approval_preservation": stage5dg_preservation,
        "stage5bd_plan_preservation": stage5bd_plan,
        "active_lineage_preservation": active_lineage,
        "no_active_ingestion_proof": no_active,
        "no_byte_stream_transition_gate": no_byte,
        "no_execution_transition_gate": no_execution,
    }
    return records


def _schema_for(key: str, path: Path) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "stage_id": {"const": STAGE_ID},
        "stage_title": {"const": STAGE_TITLE},
        "prompt_type": {"const": PROMPT_TYPE},
        "record_type": {"type": "string"},
        "source_previous_stage": {"const": SOURCE_PREVIOUS_STAGE_ID},
        "metadata_only": {"const": True},
        "execution_allowed": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
        "stage5dk_summary_status": {"const": "complete"},
        "stage5dg_operator_approval_record_preserved": {"const": True},
        "operator_approval_component_satisfied_now": {"const": True},
        "stage5bd_run_plan_id_count": {"const": 10},
        "active_lineage_record_count": {"const": 8},
        "parallel_worker_cap_for_stage5dl_and_later": {"const": PARALLEL_WORKER_CAP},
        "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        properties[flag] = {"const": False}
    if key == "summary":
        properties.update(
            {
                "status": {"const": "complete"},
                "operator_preferred_future_target_family_id": {"const": TRIANGLE_FAMILY_ID},
                "selected_next_solve_target_id": {"type": "null"},
                "candidate_family_count_added_or_updated": {"const": len(CANDIDATE_FAMILIES)},
            }
        )
    if key == "number_triangle_source_lock":
        properties.update(
            {
                "candidate_family_id": {"const": TRIANGLE_FAMILY_ID},
                "triangle_body_word_count": {"const": 153},
                "triangle_row_count": {"const": 17},
                "triangle_center_word_index": {"const": 41},
                "selected_now": {"const": False},
            }
        )
    if key == "triangle_way_anchor":
        properties["derived_latin"] = {"const": "WAY"}
    if key == "triangle_prime_mask":
        properties.update(
            {
                "present_prime_count_under_153": {"const": 20},
                "missing_prime_count_under_153": {"const": 16},
                "prime_41_hits_triangle_center": {"const": True},
                "prime_53_hits_single_rune_anchor": {"const": True},
            }
        )
    if key == "triangle_2016_prime_layer":
        properties.update(
            {
                "layered_prime_values": {"const": [2819, 2039, 1277]},
                "layered_prime_indices": {"const": [410, 309, 206]},
            }
        )
    if key == "triangle_fibonacci_prime_index":
        properties.update(
            {
                "fibonacci_walk_start_prime": {"const": 3301},
                "fibonacci_walk_start_prime_index": {"const": 464},
                "f_adjustment_caveat_recorded": {"const": True},
            }
        )
    if key == "disk_alberti_branch":
        properties.update(
            {
                "source_root": {"const": "third_party/DiskCipherStuff"},
                "html_execution_performed": {"const": False},
                "disk_cipher_experiment_executed": {"const": False},
            }
        )
    if key == "quote_dialogue_cribs":
        properties.update(
            {
                "candidate_family_id": {"const": "section_0_12_quote_dialogue_cribs_v0"},
                "candidate_a_proposed_plaintext": {"const": "HE SAID"},
                "candidate_b_proposed_plaintext": {"const": "HE ANSWERED"},
            }
        )
    if key == "koan_visual_parallel":
        properties.update(
            {
                "source_path": {"const": "third_party/koan_page.png"},
                "operator_observed_similarity_to_lp_body_depictions": {"const": True},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _posix_path(path),
        "title": path.with_suffix("").name,
        "type": "object",
        "required": [
            "stage_id",
            "stage_title",
            "prompt_type",
            "record_type",
            "source_previous_stage",
            "source_previous_stage_commit",
            "metadata_only",
            "execution_allowed",
            "canonical_codex_handoff_root",
            "stage5dk_summary_status",
            "generated_outputs_committed",
            "solve_claim",
            "execution_authorized_now",
            "recommended_next_stage_id",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def write_stage5dl_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        write_json(path, _schema_for(key, path))


def _write_generated_reports(records: dict[str, Any]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS_DIR / "summary.json", records["summary"])
    write_json(
        RESULTS_DIR / "source_lock_report.json",
        {
            "number_triangle": records["number_triangle_source_lock"],
            "disk": records["disk_alberti_branch"],
            "reddit": records["reddit_thread_image_source_lock_register"],
            "quote": records["quote_dialogue_cribs"],
            "koan": records["koan_visual_parallel"],
        },
    )
    write_json(RESULTS_DIR / "pivot_readiness_report.json", records["pivot_readiness_update"])
    write_json(
        RESULTS_DIR / "preservation_report.json",
        {
            "stage5dg": records["stage5dg_approval_preservation"],
            "stage5bd": records["stage5bd_plan_preservation"],
            "active_lineage": records["active_lineage_preservation"],
            "no_active": records["no_active_ingestion_proof"],
            "no_byte": records["no_byte_stream_transition_gate"],
            "no_execution": records["no_execution_transition_gate"],
        },
    )
    write_jsonl(RESULTS_DIR / "warnings.jsonl", [])


def _write_initial_completion_summary(records: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = records["summary"]
    checklist = [
        ("Stage 5DK predecessor consumed", summary["stage5dk_summary_status"] == "complete"),
        (
            "NumberTriangleStuff present or fallback recorded",
            summary["number_triangle_v1_source_locked"],
        ),
        ("DiskCipherStuff present or gap recorded", summary["disk_cipher_bridge_source_locked"]),
        ("RedditStuff folders inventoried", summary["reddit_prime_thread_images_source_locked"]),
        ("koan_page.png inventoried or gap recorded", summary["koan_depiction_visual_candidate_source_locked"]),
        ("pdd_153_triangle_word_prime_route_v1 recorded", True),
        ("pdd_153_triangle_prime_mask_route_v1 recorded", True),
        ("pdd_153_triangle_2016_prime_layer_route_v1 recorded", True),
        ("pdd_153_triangle_fibonacci_prime_index_route_v1 recorded", True),
        ("pdd_153_triangle_56311_wynn_way_route_v1 recorded", True),
        ("section_0_12_quote_dialogue_cribs_v0 recorded", True),
        ("koan_depiction_visual_parallel_candidate_v0 recorded", True),
        ("Operator future top-priority preference recorded", True),
        ("No target selected", summary["pivot_target_selected_now"] is False),
        ("No execution performed", summary["execution_authorized_now"] is False),
        ("No route extraction performed", summary["route_extraction_performed_now"] is False),
        ("No OCR/image forensics performed", summary["ocr_performed"] is False),
        ("No raw third-party files committed", True),
        ("Stage 5BD count remains 10", summary["stage5bd_run_plan_id_count"] == 10),
        ("Active lineage count remains 8", summary["active_lineage_record_count"] == 8),
        ("CI passed", False),
    ]
    lines = [
        "# Stage 5DL Codex Completion",
        "",
        "Stage 5DL complete.",
        f"Starting commit: {summary['source_previous_stage_commit']}",
        "Stage commit: pending",
        "Final commit: pending",
        "GitHub issue: pending",
        "Final CI run: pending",
        "Replacement CI run if any: none",
        f"Source previous stage: {SOURCE_PREVIOUS_STAGE_ID}",
        f"Stage 5DK status consumed: {summary['stage5dk_summary_status']}",
        f"NumberTriangleStuff source locked: {summary['number_triangle_v1_source_locked']}",
        f"DiskCipherStuff source locked: {summary['disk_cipher_bridge_source_locked']}",
        f"RedditStuff source locked: {summary['reddit_prime_thread_images_source_locked']}",
        f"koan_page.png source locked: {summary['koan_depiction_visual_candidate_source_locked']}",
        f"Candidate family added/updated: {TRIANGLE_FAMILY_ID}",
        f"Subfamilies added/updated: {', '.join(TRIANGLE_SUBFAMILIES)}",
        "Operator future priority preference recorded: true",
        "Selected next solve target: null",
        "Pivot target selected now: false",
        "Target-priority decision created now: false",
        "Real operator approval preserved: true",
        "Deep Research acceptance present: false",
        "Combined gate satisfied: false",
        "Activation authorized: false",
        "Active input selected: false",
        "Byte streams generated: false",
        "Execution performed: false",
        "Stage 5BD run-plan IDs: 10",
        "Active lineage records: 8",
        "Pytest: pending",
        "Ruff: pending",
        "Parallel validation: pending",
        "Consistency: pending",
        "Raw third-party files staged: 0",
        "Generated outputs staged: 0",
        "codex-output staged: 0",
        "codex_output used: false",
        "Warnings: completion summary must be refreshed after final CI",
        f"Recommended next stage: {NEXT_STAGE_TITLE}",
        "",
        "Checklist:",
    ]
    lines.extend(f"- [{'x' if ok else ' '}] {label}." for label, ok in checklist)
    CODEX_COMPLETION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_stage5dl(write_completion: bool = True) -> dict[str, Any]:
    write_stage5dl_schemas()
    records = _build_records()
    for key, path in DATA_PATHS.items():
        write_yaml(path, records[key])
    _write_generated_reports(records)
    if write_completion:
        _write_initial_completion_summary(records)
    return records


def load_stage5dl_summary() -> dict[str, Any]:
    return read_yaml(DATA_PATHS["summary"])


def _read_record(key: str) -> dict[str, Any]:
    return read_yaml(DATA_PATHS[key])


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


def _common_errors(record: dict[str, Any], context: str) -> list[str]:
    errors = []
    if record.get("stage_id") != STAGE_ID:
        errors.append(f"{context}:stage_id_must_be_{STAGE_ID}")
    if record.get("source_previous_stage") != SOURCE_PREVIOUS_STAGE_ID:
        errors.append(f"{context}:source_previous_stage_must_be_{SOURCE_PREVIOUS_STAGE_ID}")
    if record.get("canonical_codex_handoff_root") != "codex-output":
        errors.append(f"{context}:canonical_codex_handoff_root_must_be_codex-output")
    for flag in FORBIDDEN_FALSE_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{context}:{flag}_must_be_false")
    for key, expected in REQUIRED_TRUE_FLAGS.items():
        if record.get(key) is not expected:
            errors.append(f"{context}:{key}_must_be_{expected}")
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append(f"{context}:stage5bd_run_plan_id_count_must_be_10")
    if record.get("active_lineage_record_count") != 8:
        errors.append(f"{context}:active_lineage_record_count_must_be_8")
    if record.get("parallel_worker_cap_for_stage5dl_and_later") != PARALLEL_WORKER_CAP:
        errors.append(f"{context}:parallel_worker_cap_must_be_{PARALLEL_WORKER_CAP}")
    return errors


def _result(command: str, errors: list[str]) -> ValidationResult:
    return ValidationResult(command, len(errors), errors)


def validate_stage5dl_number_triangle_v1() -> ValidationResult:
    command = "validate-stage5dl-number-triangle-v1"
    record = _read_record("number_triangle_source_lock")
    errors = _common_errors(record, command)
    checks = {
        "candidate_family_id": TRIANGLE_FAMILY_ID,
        "triangle_body_word_count": 153,
        "triangle_row_count": 17,
        "triangle_center_word_index": 41,
        "selected_now": False,
        "execution_authorized_now": False,
        "solve_claim": False,
    }
    for key, expected in checks.items():
        if record.get(key) != expected:
            errors.append(f"{key}_must_be_{expected}")
    if record.get("subfamilies") != TRIANGLE_SUBFAMILIES:
        errors.append("triangle_subfamilies_changed")
    if not record.get("source_paths_used_for_verification"):
        errors.append("missing_source_paths_used_for_verification")
    return _result(command, errors)


def validate_stage5dl_triangle_way_anchor() -> ValidationResult:
    command = "validate-stage5dl-triangle-way-anchor"
    record = _read_record("triangle_way_anchor")
    errors = _common_errors(record, command)
    if record.get("derived_latin") != "WAY" or record.get("way_result") != "WAY":
        errors.append("way_result_must_be_way")
    for key in ["used_as_key_now", "route_extraction_performed_now", "solve_claim"]:
        if record.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    return _result(command, errors)


def validate_stage5dl_triangle_prime_mask() -> ValidationResult:
    command = "validate-stage5dl-triangle-prime-mask"
    record = _read_record("triangle_prime_mask")
    errors = _common_errors(record, command)
    if record.get("present_prime_positions_under_153") != PRESENT_PRIMES_UNDER_153:
        errors.append("present_prime_positions_under_153_changed")
    if record.get("missing_prime_positions_under_153") != MISSING_PRIMES_UNDER_153:
        errors.append("missing_prime_positions_under_153_changed")
    for key in ["prime_41_hits_triangle_center", "prime_53_hits_single_rune_anchor"]:
        if record.get(key) is not True:
            errors.append(f"{key}_must_be_true")
    if record.get("extraction_performed_now") is not False:
        errors.append("extraction_performed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dl_triangle_2016_prime_layer() -> ValidationResult:
    command = "validate-stage5dl-triangle-2016-prime-layer"
    record = _read_record("triangle_2016_prime_layer")
    errors = _common_errors(record, command)
    expected = {
        "layered_prime_values": [2819, 2039, 1277],
        "layered_prime_indices": [410, 309, 206],
        "layered_prime_index_differences": [101, 103],
        "layered_prime_values_mod_153": [65, 50, 53],
        "layered_prime_indices_mod_153": [104, 3, 53],
    }
    for key, value in expected.items():
        if record.get(key) != value:
            errors.append(f"{key}_changed")
    if record.get("route_extraction_performed_now") is not False:
        errors.append("route_extraction_performed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dl_triangle_fibonacci_prime_index() -> ValidationResult:
    command = "validate-stage5dl-triangle-fibonacci-prime-index"
    record = _read_record("triangle_fibonacci_prime_index")
    errors = _common_errors(record, command)
    if record.get("base_prime") != 3301 or record.get("base_prime_index") != 464:
        errors.append("base_prime_or_index_changed")
    if record.get("highlighted_row_count") != 4:
        errors.append("highlighted_row_count_must_be_4")
    if record.get("plus_f_minus_f_manipulation_is_weakest_link") is not True:
        errors.append("f_adjustment_caveat_missing")
    if record.get("route_extraction_performed_now") is not False:
        errors.append("route_extraction_performed_now_must_be_false")
    return _result(command, errors)


def validate_stage5dl_triangle_56311_wynn_way() -> ValidationResult:
    command = "validate-stage5dl-triangle-56311-wynn-way"
    record = _read_record("triangle_56311_wynn_way")
    errors = _common_errors(record, command)
    if record.get("disk_sequence") != [5, 6, 3, 11]:
        errors.append("disk_sequence_changed")
    if record.get("cumulative_from_center_41") != [46, 52, 55, 66]:
        errors.append("cumulative_from_center_41_changed")
    for key in ["center_plus_sequence_hits_word52", "word52_is_way_anchor_word"]:
        if record.get(key) is not True:
            errors.append(f"{key}_must_be_true")
    return _result(command, errors)


def validate_stage5dl_disk_cipher_source_lock() -> ValidationResult:
    command = "validate-stage5dl-disk-cipher-source-lock"
    record = _read_record("disk_alberti_branch")
    errors = _common_errors(record, command)
    if record.get("source_root") != "third_party/DiskCipherStuff":
        errors.append("source_root_must_be_DiskCipherStuff")
    if record.get("html_execution_performed") is not False:
        errors.append("html_execution_performed_must_be_false")
    if record.get("disk_cipher_experiment_executed") is not False:
        errors.append("disk_cipher_experiment_executed_must_be_false")
    if record.get("manual_branching_false_positive_risk") != "high":
        errors.append("manual_branching_false_positive_risk_must_be_high")
    if record.get("requires_programmatic_reproduction_before_experiment") is not True:
        errors.append("requires_programmatic_reproduction_missing")
    return _result(command, errors)


def validate_stage5dl_quote_dialogue_cribs() -> ValidationResult:
    command = "validate-stage5dl-quote-dialogue-cribs"
    record = _read_record("quote_dialogue_cribs")
    errors = _common_errors(record, command)
    if record.get("candidate_a_proposed_plaintext") != "HE SAID":
        errors.append("candidate_a_plaintext_changed")
    if record.get("candidate_b_proposed_plaintext") != "HE ANSWERED":
        errors.append("candidate_b_plaintext_changed")
    for key in ["i_am_a_quote_template_relevant", "he_said_candidate_recorded", "he_answered_candidate_recorded"]:
        if record.get(key) is not True:
            errors.append(f"{key}_must_be_true")
    for key in ["cribs_applied_now", "decryption_performed_now", "solve_claim"]:
        if record.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    return _result(command, errors)


def validate_stage5dl_koan_depiction_source_lock() -> ValidationResult:
    command = "validate-stage5dl-koan-depiction-source-lock"
    record = _read_record("koan_visual_parallel")
    errors = _common_errors(record, command)
    if record.get("source_path") != "third_party/koan_page.png":
        errors.append("source_path_must_be_koan_page")
    if record.get("operator_observed_similarity_to_lp_body_depictions") is not True:
        errors.append("operator_observation_missing")
    for key in ["image_forensics_performed", "ocr_performed", "ai_ml_interpretation_performed", "solve_claim"]:
        if record.get(key) is not False:
            errors.append(f"{key}_must_be_false")
    return _result(command, errors)


def validate_stage5dl_local_source_crosswalks() -> ValidationResult:
    command = "validate-stage5dl-local-source-crosswalks"
    errors: list[str] = []
    for key in [
        "local_source_path_aliases",
        "local_source_lock_register",
        "reddit_thread_image_source_lock_register",
        "number_triangle_local_archive_crosswalk",
        "disk_cipher_local_archive_crosswalk",
        "koan_page_local_source_lock",
        "source_digest_index",
    ]:
        record = _read_record(key)
        errors.extend(_common_errors(record, f"{command}:{key}"))
    aliases = _read_record("local_source_path_aliases").get("path_aliases", [])
    by_path = {row.get("path"): row for row in aliases}
    if by_path.get("third_party/NumberTriangleStuff", {}).get("exists_locally") is not True:
        errors.append("NumberTriangleStuff_not_recorded_present")
    if by_path.get("third_party/RedditStuff", {}).get("exists_locally") is not True:
        errors.append("RedditStuff_not_recorded_present")
    reddit = _read_record("reddit_thread_image_source_lock_register")
    if reddit.get("reddit_folder_count") != 3:
        errors.append("reddit_folder_count_must_be_3")
    return _result(command, errors)


def validate_stage5dl_pivot_readiness() -> ValidationResult:
    command = "validate-stage5dl-pivot-readiness"
    record = _read_record("pivot_readiness_update")
    errors = _common_errors(record, command)
    if record.get("priority_matrix_status") != "review_only_unselected":
        errors.append("priority_matrix_status_changed")
    if record.get("selected_next_solve_target_id") is not None:
        errors.append("selected_next_solve_target_id_must_be_null")
    if record.get("pivot_option_count") != len(PIVOT_OPTIONS):
        errors.append("pivot_option_count_changed")
    for option in record.get("pivot_options", []):
        if option.get("selected_now") is not False:
            errors.append(f"pivot_option_selected:{option.get('option_id')}")
        if option.get("execution_authorized_now") is not False:
            errors.append(f"pivot_option_execution_authorized:{option.get('option_id')}")
    return _result(command, errors)


def validate_stage5dl_stage5dg_preservation() -> ValidationResult:
    command = "validate-stage5dl-stage5dg-preservation"
    record = _read_record("stage5dg_approval_preservation")
    errors = _common_errors(record, command)
    if record.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("stage5dg_operator_approval_not_preserved")
    if record.get("deep_research_acceptance_present_now") is not False:
        errors.append("deep_research_acceptance_present_now_must_be_false")
    if record.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined_gate_must_be_unsatisfied")
    return _result(command, errors)


def validate_stage5dl_stage5bd_preservation() -> ValidationResult:
    command = "validate-stage5dl-stage5bd-preservation"
    record = _read_record("stage5bd_plan_preservation")
    errors = _common_errors(record, command)
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    if record.get("stage5bd_validation_error_count") != 0:
        errors.append("stage5bd_validation_must_pass")
    return _result(command, errors)


def validate_stage5dl_active_lineage_preservation() -> ValidationResult:
    command = "validate-stage5dl-active-lineage-preservation"
    record = _read_record("active_lineage_preservation")
    errors = _common_errors(record, command)
    if record.get("active_lineage_record_count") != 8:
        errors.append("active_lineage_record_count_must_be_8")
    if record.get("active_lineage_preserved") is not True:
        errors.append("active_lineage_not_preserved")
    return _result(command, errors)


def validate_stage5dl_sidecar_gates() -> ValidationResult:
    command = "validate-stage5dl-sidecar-gates"
    errors: list[str] = []
    for key in [
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        record = _read_record(key)
        errors.extend(_common_errors(record, f"{command}:{key}"))
    return _result(command, errors)


def validate_stage5dl_handoff_continuity() -> ValidationResult:
    command = "validate-stage5dl-handoff-continuity"
    errors: list[str] = []
    summary = _read_record("summary")
    errors.extend(_common_errors(summary, command))
    if summary.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical_handoff_root_changed")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated_codex_output_path_exists")
    return _result(command, errors)


def validate_stage5dl_credential_redaction_policy() -> ValidationResult:
    command = "validate-stage5dl-credential-redaction-policy"
    errors: list[str] = []
    for key in ["local_source_lock_register", "reviewable_validation_evidence"]:
        record = _read_record(key)
        errors.extend(_common_errors(record, f"{command}:{key}"))
        if record.get("raw_body_committed") is not False:
            errors.append(f"{key}:raw_body_committed_must_be_false")
    return _result(command, errors)


def validate_stage5dl_governance_scope() -> ValidationResult:
    command = "validate-stage5dl-governance-scope"
    summary = _read_record("summary")
    errors = _common_errors(summary, command)
    checks = {
        "combined_approval_gate_satisfied_now": False,
        "activation_authorized_now": False,
        "active_planning_input_selected_now": False,
        "byte_stream_generation_authorized_now": False,
        "execution_authorized_now": False,
        "pivot_target_selected_now": False,
        "target_priority_decision_created_now": False,
        "operator_target_priority_decision_created_now": False,
        "route_extraction_performed_now": False,
        "triangle_route_extraction_performed_now": False,
        "known_plaintext_attack_performed_now": False,
        "image_forensics_performed": False,
        "ai_ml_interpretation_performed": False,
        "solve_claim": False,
    }
    for key, expected in checks.items():
        if summary.get(key) is not expected:
            errors.append(f"{key}_must_be_{expected}")
    if summary.get("selected_next_solve_target_id") is not None:
        errors.append("selected_next_solve_target_id_must_be_null")
    return _result(command, errors)


def validate_stage5dl() -> ValidationResult:
    command = "validate-stage5dl"
    errors: list[str] = []
    for key in DATA_PATHS:
        errors.extend(_schema_errors(key))
        if DATA_PATHS[key].exists():
            errors.extend(_common_errors(_read_record(key), key))
    validators = [
        validate_stage5dl_number_triangle_v1,
        validate_stage5dl_triangle_way_anchor,
        validate_stage5dl_triangle_prime_mask,
        validate_stage5dl_triangle_2016_prime_layer,
        validate_stage5dl_triangle_fibonacci_prime_index,
        validate_stage5dl_triangle_56311_wynn_way,
        validate_stage5dl_disk_cipher_source_lock,
        validate_stage5dl_quote_dialogue_cribs,
        validate_stage5dl_koan_depiction_source_lock,
        validate_stage5dl_local_source_crosswalks,
        validate_stage5dl_pivot_readiness,
        validate_stage5dl_stage5dg_preservation,
        validate_stage5dl_stage5bd_preservation,
        validate_stage5dl_active_lineage_preservation,
        validate_stage5dl_sidecar_gates,
        validate_stage5dl_handoff_continuity,
        validate_stage5dl_credential_redaction_policy,
        validate_stage5dl_governance_scope,
    ]
    for validator in validators:
        result = validator()
        errors.extend(f"{result.command}:{error}" for error in result.errors)
    return _result(command, errors)


def stage5dl_summary_text() -> str:
    summary = load_stage5dl_summary()
    lines = [
        f"stage_id={summary['stage_id']}",
        f"status={summary['status']}",
        f"source_previous_stage={summary['source_previous_stage']}",
        f"stage5dk_summary_status={summary['stage5dk_summary_status']}",
        f"number_triangle_v1_source_locked={str(summary['number_triangle_v1_source_locked']).lower()}",
        f"disk_cipher_bridge_source_locked={str(summary['disk_cipher_bridge_source_locked']).lower()}",
        f"reddit_prime_thread_images_source_locked={str(summary['reddit_prime_thread_images_source_locked']).lower()}",
        f"quote_dialogue_cribs_source_locked={str(summary['quote_dialogue_cribs_source_locked']).lower()}",
        f"koan_depiction_visual_candidate_source_locked={str(summary['koan_depiction_visual_candidate_source_locked']).lower()}",
        f"candidate_family_count_added_or_updated={summary['candidate_family_count_added_or_updated']}",
        f"operator_preferred_future_target_family_id={summary['operator_preferred_future_target_family_id']}",
        f"pivot_target_selected_now={str(summary['pivot_target_selected_now']).lower()}",
        f"target_priority_decision_created_now={str(summary['target_priority_decision_created_now']).lower()}",
        f"stage5bd_run_plan_id_count={summary['stage5bd_run_plan_id_count']}",
        f"active_lineage_record_count={summary['active_lineage_record_count']}",
        f"execution_authorized_now={str(summary['execution_authorized_now']).lower()}",
        f"recommended_next_stage_id={summary['recommended_next_stage_id']}",
    ]
    return "\n".join(lines)


__all__ = [
    "CODEX_COMPLETION_PATH",
    "DATA_PATHS",
    "NEXT_STAGE_ID",
    "SCHEMA_PATHS",
    "STAGE_ID",
    "TRIANGLE_FAMILY_ID",
    "TRIANGLE_SUBFAMILIES",
    "build_stage5dl",
    "load_stage5dl_summary",
    "stage5dl_summary_text",
    "validate_stage5dl",
    "validate_stage5dl_active_lineage_preservation",
    "validate_stage5dl_credential_redaction_policy",
    "validate_stage5dl_disk_cipher_source_lock",
    "validate_stage5dl_governance_scope",
    "validate_stage5dl_handoff_continuity",
    "validate_stage5dl_koan_depiction_source_lock",
    "validate_stage5dl_local_source_crosswalks",
    "validate_stage5dl_number_triangle_v1",
    "validate_stage5dl_pivot_readiness",
    "validate_stage5dl_quote_dialogue_cribs",
    "validate_stage5dl_sidecar_gates",
    "validate_stage5dl_stage5bd_preservation",
    "validate_stage5dl_stage5dg_preservation",
    "validate_stage5dl_triangle_2016_prime_layer",
    "validate_stage5dl_triangle_56311_wynn_way",
    "validate_stage5dl_triangle_fibonacci_prime_index",
    "validate_stage5dl_triangle_prime_mask",
    "validate_stage5dl_triangle_way_anchor",
]
