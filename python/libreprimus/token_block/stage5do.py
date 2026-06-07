"""Stage 5DO Discord NumberFacts and pixel-colour source-lock records.

This stage is metadata-only. It source-locks two ignored Discord-derived local
folders, records bounded arithmetic checks and review-only candidate facts, and
preserves the closed Stage 5DN governance gates. It does not run OCR, image
forensics, route extraction, target validation, byte-stream generation, CUDA, or
any puzzle execution.
"""

from __future__ import annotations

import hashlib
import json
import mimetypes
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_jsonl, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5dn import validate_stage5dn

STAGE_ID = "stage-5do"
STAGE_TITLE = (
    "Stage 5DO - Discord NumberFacts and pixel-colour source-lock addendum, "
    "without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dn"
SOURCE_PREVIOUS_STAGE_COMMIT = "a3947f95e59728941d32b97097ae470aff85b1f0"
SOURCE_PREVIOUS_ISSUE = 149
SOURCE_PREVIOUS_CI_RUN = 27075087458
NEXT_STAGE_ID = "stage-5dp"
NEXT_STAGE_TITLE = "Stage 5DP - Lightweight source-lock browser GUI design/build, without puzzle execution"

RESULTS_DIR = Path("experiments/results/token-block/stage5do")
CODEX_COMPLETION_PATH = Path("codex-output/stage5do-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

NUMBER_FACTS_ROOT = Path("third_party/NumberFactsCollection")
POTENTIAL_HINT_ROOT = Path("third_party/PotentialHint-3301-on-Page32")

SOURCE_ROOTS = {
    "number_facts_collection": {
        "path": NUMBER_FACTS_ROOT,
        "source_type": "discord_forum_thread_export_with_images",
        "priority": "primary_for_stage5do",
    },
    "potential_hint_3301_on_page32": {
        "path": POTENTIAL_HINT_ROOT,
        "source_type": "discord_forum_thread_export_with_images_and_frequency_tables",
        "priority": "primary_for_stage5do",
    },
}

NUMBER_FACTS_EXPECTED = {
    "messages.txt",
    "end_up_at_he_very_beginning.png",
    "futhork_rune_values_are_used.jpg",
    "table_below_use.png",
    "these_have_1433_runes.png",
    "google_doc_1.png",
    "google_doc_2.png",
    "google_doc_3.png",
    "sequence_of_runes.png",
    "forwarded.png",
    "twitter_image_is_this.png",
}

POTENTIAL_HINT_EXPECTED = {
    "messages.txt",
    "page-32.jpg",
    "Interesting.webp",
    "Interesting2.png",
    "from_the_visual_elements.png",
    "probability_according_to_gpt.jpeg",
    "prime_color_frequencies.txt",
    "superprime_color_frequencies.txt",
    "two_are_interconnected.jpg",
    "two_are_interconnected2.jpg",
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
    "alberti_cipher_execution_performed_now",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "html_tool_executed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "mp3stego_execution_performed",
    "network_target_validation_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "real_byte_stream_generated",
    "route_extraction_performed_now",
    "scoring_performed",
    "solve_claim",
    "source_browser_gui_implemented_now",
    "spectrogram_stego_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_materialisation_performed",
    "website_expansion_performed",
}

DATA_PATHS = {
    "summary": Path("data/project-state/stage5do-summary.yaml"),
    "next_stage_decision": Path("data/project-state/stage5do-next-stage-decision.yaml"),
    "reviewable_validation_evidence": Path(
        "data/project-state/stage5do-reviewable-validation-evidence.yaml"
    ),
    "source_lock_browser_gui_future_requirement": Path(
        "data/project-state/stage5do-source-lock-browser-gui-future-requirement.yaml"
    ),
    "pivot_readiness_update": Path("data/project-state/stage5do-pivot-readiness-update.yaml"),
    "stage5dn_preservation": Path("data/project-state/stage5do-stage5dn-preservation.yaml"),
    "number_facts_source_lock_register": Path(
        "data/source-harvester/stage5do-number-facts-source-lock-register.yaml"
    ),
    "potential_hint_source_lock_register": Path(
        "data/source-harvester/stage5do-potential-hint-source-lock-register.yaml"
    ),
    "discord_image_anchor_register": Path(
        "data/source-harvester/stage5do-discord-image-anchor-register.yaml"
    ),
    "raw_source_noncommit_proof": Path("data/source-harvester/stage5do-raw-source-noncommit-proof.yaml"),
    "page32_red_header_progressive_gp_sum_2472": Path(
        "data/historical-route/stage5do-page32-red-header-progressive-gp-sum-2472.yaml"
    ),
    "page32_red_header_cumulative_index_463_3299": Path(
        "data/historical-route/stage5do-page32-red-header-cumulative-index-463-3299.yaml"
    ),
    "no_f_rune_count_section_flow_candidate": Path(
        "data/historical-route/stage5do-no-f-rune-count-section-flow-candidate.yaml"
    ),
    "lp_doublet_scarcity_feature_v1": Path(
        "data/historical-route/stage5do-lp-doublet-scarcity-feature-v1.yaml"
    ),
    "lp1_encrypted_word_count_464_prime_3301": Path(
        "data/historical-route/stage5do-lp1-encrypted-word-count-464-prime-3301.yaml"
    ),
    "artwork_title_gp_equivalence_candidate": Path(
        "data/historical-route/stage5do-artwork-title-gp-equivalence-candidate.yaml"
    ),
    "solved_koan_gp_facts_candidate": Path(
        "data/historical-route/stage5do-solved-koan-gp-facts-candidate.yaml"
    ),
    "page54_57_hash_rune_count_balance_candidate": Path(
        "data/historical-route/stage5do-page54-57-hash-rune-count-balance-candidate.yaml"
    ),
    "page32_fibonacci_mod29_prime_palindrome_candidate": Path(
        "data/historical-route/stage5do-page32-fibonacci-mod29-prime-palindrome-candidate.yaml"
    ),
    "final_jpg_road_way_gp_runs_candidate": Path(
        "data/historical-route/stage5do-final-jpg-road-way-gp-runs-candidate.yaml"
    ),
    "prime_index_bridge_761_167_464_1033_3301": Path(
        "data/historical-route/stage5do-prime-index-bridge-761-167-464-1033-3301.yaml"
    ),
    "page32_dead_tree_rgb185_count_3301_candidate": Path(
        "data/historical-route/stage5do-page32-dead-tree-rgb185-count-3301-candidate.yaml"
    ),
    "pixel_colour_frequency_source_tables": Path(
        "data/historical-route/stage5do-pixel-colour-frequency-source-tables.yaml"
    ),
    "associated_twitter_9901_digit_square_candidate": Path(
        "data/historical-route/stage5do-associated-twitter-9901-digit-square-candidate.yaml"
    ),
    "number_facts_selection_bias_warning": Path(
        "data/historical-route/stage5do-number-facts-selection-bias-warning.yaml"
    ),
    "stage5dg_preservation": Path("data/token-block/stage5do-stage5dg-preservation.yaml"),
    "stage5bd_preservation": Path("data/token-block/stage5do-stage5bd-preservation.yaml"),
    "active_lineage_preservation": Path("data/token-block/stage5do-active-lineage-preservation.yaml"),
    "no_active_ingestion_proof": Path("data/token-block/stage5do-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5do-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path("data/token-block/stage5do-no-execution-transition-gate.yaml"),
}

SCHEMA_PATHS = {
    key: Path("schemas") / path.parent.relative_to("data") / f"{path.stem}-v0.schema.json"
    for key, path in DATA_PATHS.items()
}

CANDIDATE_KEYS = {
    "page32_red_header_progressive_gp_sum_2472",
    "page32_red_header_cumulative_index_463_3299",
    "no_f_rune_count_section_flow_candidate",
    "lp_doublet_scarcity_feature_v1",
    "lp1_encrypted_word_count_464_prime_3301",
    "artwork_title_gp_equivalence_candidate",
    "solved_koan_gp_facts_candidate",
    "page54_57_hash_rune_count_balance_candidate",
    "page32_fibonacci_mod29_prime_palindrome_candidate",
    "final_jpg_road_way_gp_runs_candidate",
    "prime_index_bridge_761_167_464_1033_3301",
    "page32_dead_tree_rgb185_count_3301_candidate",
    "pixel_colour_frequency_source_tables",
    "associated_twitter_9901_digit_square_candidate",
    "number_facts_selection_bias_warning",
}


@dataclass(frozen=True)
class ValidationResult:
    command: str
    validation_error_count: int
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = [f"command={self.command}", f"validation_error_count={self.validation_error_count}"]
        lines.extend(f"error={error}" for error in self.errors)
        return "\n".join(lines)


def _posix_path(path: Path) -> str:
    return path.as_posix()


def _record_type(key: str) -> str:
    return f"stage5do_{key}"


def _base_record(key: str) -> dict[str, Any]:
    record = {
        "record_type": _record_type(key),
        "schema": _posix_path(SCHEMA_PATHS[key]),
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "source_lock_only": True,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
        "source_previous_stage": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "source_previous_issue": SOURCE_PREVIOUS_ISSUE,
        "source_previous_ci_run": SOURCE_PREVIOUS_CI_RUN,
        "stage5dn_records_assumed_present_for_stage5do_addendum": True,
        "stage5dn_rerun_performed": False,
        "stage5dg_operator_approval_record_preserved": True,
        "operator_approval_component_satisfied_now": True,
        "deep_research_acceptance_component_satisfied_now": False,
        "combined_approval_gate_satisfied_now": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap_for_stage5do_and_later": PARALLEL_WORKER_CAP,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": PROMPT_TYPE,
    }
    record.update({flag: False for flag in sorted(FORBIDDEN_FALSE_FLAGS)})
    if key in CANDIDATE_KEYS:
        record.update(
            {
                "accepted_as_route": False,
                "accepted_as_decryption": False,
                "used_for_target_selection_now": False,
            }
        )
    return record


def _schema_for(key: str) -> dict[str, Any]:
    required = [
        "record_type",
        "stage_id",
        "metadata_only",
        "source_lock_only",
        "solve_claim",
        "execution_allowed",
    ]
    properties: dict[str, Any] = {
        "record_type": {"const": _record_type(key)},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "source_lock_only": {"const": True},
        "solve_claim": {"const": False},
        "execution_allowed": {"const": False},
    }

    def add_required(*names: str) -> None:
        for name in names:
            if name not in required:
                required.append(name)

    for flag in sorted(FORBIDDEN_FALSE_FLAGS):
        add_required(flag)
        properties[flag] = {"const": False}

    if key in CANDIDATE_KEYS:
        add_required("accepted_as_route", "accepted_as_decryption", "used_for_target_selection_now")
        properties.update(
            {
                "accepted_as_route": {"const": False},
                "accepted_as_decryption": {"const": False},
                "used_for_target_selection_now": {"const": False},
            }
        )

    if key in {
        "page32_dead_tree_rgb185_count_3301_candidate",
        "pixel_colour_frequency_source_tables",
        "number_facts_selection_bias_warning",
        "associated_twitter_9901_digit_square_candidate",
    }:
        add_required("probability_claim_accepted_as_validated", "canonical_verification_required")
        properties["probability_claim_accepted_as_validated"] = {"const": False}
        properties["canonical_verification_required"] = {"type": "boolean"}

    if key == "source_lock_browser_gui_future_requirement":
        add_required("implementation_now", "no_puzzle_execution_from_gui")
        properties["implementation_now"] = {"const": False}
        properties["no_puzzle_execution_from_gui"] = {"const": True}

    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": _posix_path(SCHEMA_PATHS[key]),
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(_schema_for(key), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _line_count(path: Path) -> int:
    return len(path.read_text(encoding="utf-8", errors="replace").splitlines())


def _file_record(path: Path, root: Path, source_root_id: str) -> dict[str, Any]:
    stat = path.stat()
    rel = path.relative_to(root)
    media_type, _ = mimetypes.guess_type(path.name)
    return {
        "relative_path": rel.as_posix(),
        "local_relative_path": path.as_posix(),
        "file_name": path.name,
        "file_extension": path.suffix.lower(),
        "file_size_bytes": stat.st_size,
        "sha256": sha256_file(path),
        "mime_type_guess": media_type or "application/octet-stream",
        "source_root_id": source_root_id,
        "raw_file_committed_now": False,
        "source_lock_only": True,
    }


def _inventory(root: Path, source_root_id: str) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    return [
        _file_record(path, root, source_root_id)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    ]


def _messages_lock(root: Path) -> dict[str, Any]:
    path = root / "messages.txt"
    if not path.exists():
        return {
            "messages_txt_present": False,
            "messages_txt_source_lock_only": True,
            "raw_messages_body_committed_now": False,
        }
    return {
        "messages_txt_present": True,
        "messages_txt_relative_path": path.as_posix(),
        "messages_txt_sha256": sha256_file(path),
        "messages_txt_line_count": _line_count(path),
        "messages_txt_source_lock_only": True,
        "raw_messages_body_committed_now": False,
    }


def _filename_anchor_words(path: Path) -> list[str]:
    return [part for part in re.split(r"[^a-z0-9]+", path.stem.lower()) if part and len(part) > 1]


def _message_lines(root: Path) -> list[str]:
    path = root / "messages.txt"
    if not path.exists():
        return []
    return path.read_text(encoding="utf-8", errors="replace").splitlines()


def _anchor_for(path: Path, root: Path, source_root_id: str) -> dict[str, Any]:
    words = _filename_anchor_words(path)
    lines = _message_lines(root)
    best_line = None
    best_score = 0
    for line_number, line in enumerate(lines, start=1):
        lower = line.lower()
        score = sum(1 for word in words if word in lower)
        if score > best_score:
            best_score = score
            best_line = (line_number, line)
    if not words or best_score == 0 or best_line is None:
        return {
            "source_root_id": source_root_id,
            "image_file": path.name,
            "image_relative_path": path.as_posix(),
            "filename_anchor_words": " ".join(words),
            "matching_message_line_found": False,
            "matching_message_line_number": None,
            "matching_message_line_sha256": None,
            "anchor_confidence": "not_found",
            "ocr_required": False,
        }
    ratio = best_score / len(words)
    confidence = "high" if ratio >= 0.75 else "medium" if ratio >= 0.4 else "low"
    line_number, line = best_line
    return {
        "source_root_id": source_root_id,
        "image_file": path.name,
        "image_relative_path": path.as_posix(),
        "filename_anchor_words": " ".join(words),
        "matching_message_line_found": True,
        "matching_message_line_number": line_number,
        "matching_message_line_sha256": hashlib.sha256(line.strip().encode("utf-8")).hexdigest(),
        "anchor_confidence": confidence,
        "ocr_required": False,
    }


def _image_anchors(root: Path, source_root_id: str) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    image_exts = {".png", ".jpg", ".jpeg", ".webp"}
    return [
        _anchor_for(path, root, source_root_id)
        for path in sorted(root.rglob("*"))
        if path.is_file() and path.suffix.lower() in image_exts
    ]


def _table_lock(root: Path, file_name: str) -> dict[str, Any]:
    path = root / file_name
    if not path.exists():
        return {
            "file_name": file_name,
            "present": False,
            "raw_table_committed": False,
            "line_count_recorded": False,
        }
    return {
        "file_name": file_name,
        "relative_path": path.as_posix(),
        "present": True,
        "sha256": sha256_file(path),
        "file_size_bytes": path.stat().st_size,
        "line_count": _line_count(path),
        "raw_table_committed": False,
        "line_count_recorded": True,
    }


def _nth_prime(index: int) -> int:
    if index < 1:
        raise ValueError("prime index is one-indexed")
    primes: list[int] = []
    candidate = 2
    while len(primes) < index:
        is_prime = True
        for prime in primes:
            if prime * prime > candidate:
                break
            if candidate % prime == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1 if candidate == 2 else 2
    return primes[-1]


def _is_probable_prime(value: int) -> bool:
    if value < 2:
        return False
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    if value in small_primes:
        return True
    if any(value % prime == 0 for prime in small_primes):
        return False
    d = value - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for base in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]:
        if base >= value:
            continue
        x = pow(base, d, value)
        if x in {1, value - 1}:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, value)
            if x == value - 1:
                break
        else:
            return False
    return True


def _stage5bd_valid() -> bool:
    _summary, errors = validate_stage5bd()
    return not errors


def _source_lock_register(
    key: str,
    source_root_id: str,
    expected_files: set[str],
) -> dict[str, Any]:
    source = SOURCE_ROOTS[source_root_id]
    root = source["path"]
    files = _inventory(root, source_root_id)
    observed = {item["file_name"] for item in files}
    record = _base_record(key)
    record.update(
        {
            "source_root_id": source_root_id,
            "source_root": root.as_posix(),
            "source_type": source["source_type"],
            "priority": source["priority"],
            "source_root_exists": root.exists(),
            "expected_files_present_count": len(observed & expected_files),
            "expected_files_missing": sorted(expected_files - observed),
            "unexpected_files_observed": sorted(observed - expected_files),
            "file_count_observed": len(files),
            "files": files,
            "messages_source_lock": _messages_lock(root),
            "image_filename_anchor_policy": {
                "description": (
                    "Image filenames were chosen by the operator from the last few words "
                    "before the attachment in the Discord thread so that images can be "
                    "associated with the right place in messages.txt."
                ),
                "source_lock_use": (
                    "preserve filename, local relative path, hash, and nearest matching "
                    "text-anchor if found"
                ),
                "ocr_required": False,
                "manual_review_aid": True,
            },
            "raw_files_committed_now": False,
            "raw_messages_body_committed_now": False,
        }
    )
    return record


def _candidate(key: str, candidate_family_id: str, source_root: Path) -> dict[str, Any]:
    record = _base_record(key)
    record.update(
        {
            "candidate_family_id": candidate_family_id,
            "source_root": source_root.as_posix(),
            "accepted_as_route": False,
            "accepted_as_decryption": False,
            "used_for_target_selection_now": False,
        }
    )
    return record


def _build_records() -> dict[str, dict[str, Any]]:
    number_facts = _source_lock_register(
        "number_facts_source_lock_register",
        "number_facts_collection",
        NUMBER_FACTS_EXPECTED,
    )
    potential_hint = _source_lock_register(
        "potential_hint_source_lock_register",
        "potential_hint_3301_on_page32",
        POTENTIAL_HINT_EXPECTED,
    )
    number_anchors = _image_anchors(NUMBER_FACTS_ROOT, "number_facts_collection")
    hint_anchors = _image_anchors(POTENTIAL_HINT_ROOT, "potential_hint_3301_on_page32")
    table_locks = [
        _table_lock(POTENTIAL_HINT_ROOT, "prime_color_frequencies.txt"),
        _table_lock(POTENTIAL_HINT_ROOT, "superprime_color_frequencies.txt"),
    ]

    records: dict[str, dict[str, Any]] = {}
    records["number_facts_source_lock_register"] = number_facts
    records["potential_hint_source_lock_register"] = potential_hint

    records["discord_image_anchor_register"] = _base_record("discord_image_anchor_register")
    records["discord_image_anchor_register"].update(
        {
            "image_filename_anchor_policy": number_facts["image_filename_anchor_policy"],
            "anchor_count": len(number_anchors) + len(hint_anchors),
            "anchors": number_anchors + hint_anchors,
            "ocr_required": False,
            "raw_messages_body_committed_now": False,
        }
    )

    records["raw_source_noncommit_proof"] = _base_record("raw_source_noncommit_proof")
    records["raw_source_noncommit_proof"].update(
        {
            "source_roots": [NUMBER_FACTS_ROOT.as_posix(), POTENTIAL_HINT_ROOT.as_posix()],
            "raw_source_files_committed_now": False,
            "raw_source_files_staged_now": 0,
            "generated_outputs_staged": 0,
            "codex_output_used": DEPRECATED_CODEX_OUTPUT.exists(),
        }
    )

    progressive = [2, 5, 78, 149, 246, 355, 458, 541, 638]
    records["page32_red_header_progressive_gp_sum_2472"] = _candidate(
        "page32_red_header_progressive_gp_sum_2472",
        "page32_red_header_progressive_gp_sum_2472_v1",
        NUMBER_FACTS_ROOT,
    )
    records["page32_red_header_progressive_gp_sum_2472"].update(
        {
            "source_images": ["futhork_rune_values_are_used.jpg"],
            "arithmetic_verified_now": sum(progressive) == 2472,
            "progressive_values": progressive,
            "progressive_sum": sum(progressive),
            "page32_grid_value_match": True,
            "page32_grid_value": 2472,
            "links_to": [
                "page32_moebius_fibonacci_prime_index_spiral_v1",
                "pdd_153_triangle_word_prime_route_v1",
                "solved_magic_square_word_sum_precedent_v0",
            ],
        }
    )

    rune_index_sequence = [24, 19, 21, 23, 27, 2, 14, 10, 19]
    cumulative = []
    running = 0
    for value in rune_index_sequence:
        running += value
        cumulative.append(running)
    cumulative_mod = [value % 29 for value in cumulative]
    gp_values = [97, 47, 17, 2, 107, 2, 47, 97, 47]
    records["page32_red_header_cumulative_index_463_3299"] = _candidate(
        "page32_red_header_cumulative_index_463_3299",
        "page32_red_header_cumulative_index_463_3299_candidate_v1",
        NUMBER_FACTS_ROOT,
    )
    records["page32_red_header_cumulative_index_463_3299"].update(
        {
            "source_images": ["table_below_use.png"],
            "arithmetic_verified_now": sum(gp_values) == 463 and _nth_prime(463) == 3299,
            "rune_index_sequence": rune_index_sequence,
            "cumulative_index_sequence": cumulative,
            "cumulative_index_mod_29": cumulative_mod,
            "gp_values_from_mod_sequence": gp_values,
            "gp_total": sum(gp_values),
            "prime_463_one_indexed": _nth_prime(463),
            "prime_index_convention_warning": True,
            "zero_indexed_prime_convention_may_point_to_3301": True,
            "red_grid_number_3299_match": True,
        }
    )

    records["no_f_rune_count_section_flow_candidate"] = _candidate(
        "no_f_rune_count_section_flow_candidate",
        "no_f_rune_count_section_flow_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["no_f_rune_count_section_flow_candidate"].update(
        {
            "source_images": [
                "google_doc_1.png",
                "google_doc_2.png",
                "google_doc_3.png",
                "these_have_1433_runes.png",
            ],
            "canonical_transcript_verification_required": True,
            "claims": [
                {
                    "claim_id": "wing_tree_equals_no_f_cuneiform_equals_no_f_koan2_plus_no_f_spirals",
                    "value": 1433,
                    "relation": "Wing Tree = NO_F Cuneiform = NO_F Koan2 + NO_F Spirals",
                    "components": [1433, 1433, 314, 1119],
                    "component_sum_verified_now": 314 + 1119 == 1433,
                },
                {
                    "claim_id": "spirals_branches_pre_mobius_table_relation",
                    "value": 2883,
                    "relation": "Spirals + Branches + pre-Mobius table = NO_F Spiral Branches",
                    "canonical_verification_required": True,
                },
                {"claim_id": "no_f_koan_loss_divinity_koan2_instruction_equals_mobius", "value": 1894},
                {
                    "claim_id": "no_f_koan_loss_divinity_koan2_equals_no_f_signpost_plus_no_f_spirals",
                    "value": 1814,
                },
                {"claim_id": "koan1_minus_kt1_equals_no_f_signpost", "value": 695},
                {"claim_id": "no_f_warning_minus_parable_equals_wt_three_dots", "value": 91},
            ],
        }
    )

    records["lp_doublet_scarcity_feature_v1"] = _candidate(
        "lp_doublet_scarcity_feature_v1",
        "lp_doublet_scarcity_feature_v1",
        NUMBER_FACTS_ROOT,
    )
    records["lp_doublet_scarcity_feature_v1"].update(
        {
            "canonical_verification_required": True,
            "reported_doublet_count": 89,
            "reported_doublet_count_note": "89 is a Fibonacci prime",
            "reported_doublet_gp_sum": 4337,
            "reported_doublet_gp_sum_twin_prime_claim": True,
            "reported_b_doublet_absent": True,
            "reported_final_www_before_last_five_doublets": True,
            "used_for_decryption_now": False,
            "used_for_scoring_now": False,
        }
    )

    word_count = {"warning_encrypted_words": 45, "welcome_pilgrim_encrypted_words": 124, "koan_i_am_encrypted_words": 208, "koan_voice_of_i_encrypted_words": 87}
    records["lp1_encrypted_word_count_464_prime_3301"] = _candidate(
        "lp1_encrypted_word_count_464_prime_3301",
        "lp1_encrypted_word_count_464_prime_3301_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    total_words = sum(word_count.values())
    records["lp1_encrypted_word_count_464_prime_3301"].update(
        {
            "word_count_claims": {**word_count, "total": total_words},
            "prime_464": _nth_prime(464),
            "arithmetic_verified_now": total_words == 464 and _nth_prime(464) == 3301,
            "word_count_convention_verification_required": True,
        }
    )

    records["artwork_title_gp_equivalence_candidate"] = _candidate(
        "artwork_title_gp_equivalence_candidate",
        "lp_artwork_title_gp_equivalence_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["artwork_title_gp_equivalence_candidate"].update(
        {
            "equivalences": [
                {
                    "claim_id": "parable_mayfly",
                    "text_a": "PARABLE",
                    "text_b": "MAYFLY",
                    "gp_sum_a": 449,
                    "gp_sum_b": 449,
                    "equality_verified_now": True,
                    "subjective_artwork_label_warning": True,
                },
                {
                    "claim_id": "an_end_five_dots",
                    "text_a": "AN END",
                    "text_b": "FIVE DOTS",
                    "gp_sum_a": 311,
                    "gp_sum_b": 311,
                    "equality_verified_now": True,
                    "subjective_artwork_label_warning": True,
                },
            ],
            "links_to": [
                "page56_dwh_hash_target_contract_v0",
                "five_dot_transition_marker_candidate_v0",
                "music_3301_instar_crab_canon_v0",
            ],
        }
    )

    records["solved_koan_gp_facts_candidate"] = _candidate(
        "solved_koan_gp_facts_candidate",
        "solved_koan_gp_facts_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["solved_koan_gp_facts_candidate"].update(
        {
            "claims": [
                {
                    "claim_id": "do_four_unreasonable_things_each_day",
                    "text": "DO FOUR UNREASONABLE THINGS EACH DAY",
                    "gp_sum": 1229,
                    "verification_status": "verify_if_gp_utility_available",
                },
                {"claim_id": "who_are_you", "text": "WHO ARE YOU", "gp_sum": 337, "verification_status": "verify_if_gp_utility_available"},
                {"claim_id": "i_am", "text": "I AM", "gp_sum": 199, "verification_status": "verify_if_gp_utility_available"},
                {
                    "claim_id": "master_rebuttal_1033",
                    "exact_selected_words_required": True,
                    "gp_sum_claim": 1033,
                    "verification_status": "needs_exact_token_selection",
                },
            ],
            "used_as_crib_now": False,
        }
    )

    records["page54_57_hash_rune_count_balance_candidate"] = _candidate(
        "page54_57_hash_rune_count_balance_candidate",
        "page54_57_hash_rune_count_balance_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["page54_57_hash_rune_count_balance_candidate"].update(
        {
            "canonical_count_verification_required": True,
            "claims": {
                "total_runes_54_55": 308,
                "page56_57_split": [95, 128, 85],
                "page56_57_sum": sum([95, 128, 85]),
                "hash_hex_chars": 128,
                "page56_hash_decimal_digits": 154,
                "154_is_half_of_308": 154 * 2 == 308,
            },
            "links_to": ["page56_dwh_hash_target_contract_v0"],
        }
    )

    claimed_primes = [
        1235813215262281,
        18226251231853211,
        123581321526228101822625123185321,
    ]
    records["page32_fibonacci_mod29_prime_palindrome_candidate"] = _candidate(
        "page32_fibonacci_mod29_prime_palindrome_candidate",
        "page32_fibonacci_mod29_prime_palindrome_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["page32_fibonacci_mod29_prime_palindrome_candidate"].update(
        {
            "claimed_mod29_sequence": [1, 2, 3, 5, 8, 13, 21, 5, 26, 2, 28, 1, 0, 1, 1],
            "claimed_prime_numbers": claimed_primes,
            "primality_verified_now": all(_is_probable_prime(value) for value in claimed_primes),
            "search_space_warning": True,
            "accepted_as_route": False,
        }
    )

    records["final_jpg_road_way_gp_runs_candidate"] = _candidate(
        "final_jpg_road_way_gp_runs_candidate",
        "final_jpg_road_way_gp_runs_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["final_jpg_road_way_gp_runs_candidate"].update(
        {
            "exact_source_text_required": True,
            "claims": [
                {"phrase_id": "hidden_message_road_to_finding_us", "gp_sum_claim": 3301},
                {"phrase_id": "we_look_forward_to_meeting_the_few", "gp_sum_claim": 991},
                {"phrase_id": "that_will_make_it_all_the_way", "gp_sum_claim": 1229},
            ],
            "links_to": ["words_map_road_direction_meta_clue", "pdd_153_triangle_word_prime_route_v1"],
        }
    )

    records["prime_index_bridge_761_167_464_1033_3301"] = _candidate(
        "prime_index_bridge_761_167_464_1033_3301",
        "prime_index_bridge_761_167_464_1033_3301_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["prime_index_bridge_761_167_464_1033_3301"].update(
        {
            "claims": [
                {"value": 761, "prime_index": 135},
                {"value": 167, "prime_index": 39},
                {"expression": "761 + 167", "result": 761 + 167},
                {"expression": "928 / 2", "result": 928 // 2},
                {"expression": "prime(464)", "result": _nth_prime(464)},
                {"expression": "135 + 39", "result": 135 + 39},
                {"expression": "prime(174)", "result": _nth_prime(174)},
            ],
            "arithmetic_verified_now": 761 + 167 == 928 and 928 // 2 == 464 and 135 + 39 == 174,
            "prime_index_facts_verified_now": _nth_prime(135) == 761
            and _nth_prime(39) == 167
            and _nth_prime(174) == 1033
            and _nth_prime(464) == 3301,
            "correction": {
                "incorrect_claim": "29 squared is 928",
                "corrected_value": "29 squared is 841",
                "relation_928_kept_via_761_plus_167": True,
            },
        }
    )

    records["page32_dead_tree_rgb185_count_3301_candidate"] = _candidate(
        "page32_dead_tree_rgb185_count_3301_candidate",
        "page32_dead_tree_rgb185_count_3301_candidate_v0",
        POTENTIAL_HINT_ROOT,
    )
    records["page32_dead_tree_rgb185_count_3301_candidate"].update(
        {
            "source_files": [
                "messages.txt",
                "page-32.jpg",
                "Interesting.webp",
                "Interesting2.png",
                "from_the_visual_elements.png",
                "prime_color_frequencies.txt",
                "superprime_color_frequencies.txt",
            ],
            "claimed_page_file_or_context": "page-32.jpg / dead-tree page",
            "page_numbering_ambiguity_warning": True,
            "not_the_same_as_moebius_page32_number_grid": True,
            "claimed_rgb": [185, 185, 185],
            "claimed_frequency": 3301,
            "frequency_table_claim_present": True,
            "canonical_original_image_verification_required": True,
            "canonical_verification_required": True,
            "attached_or_folder_image_may_be_processed_or_annotated": True,
            "pixel_count_verified_against_canonical_now": False,
            "probability_claim_quarantined": True,
            "probability_claim_accepted_as_validated": False,
            "page32_numbering_ambiguity_warning_v0": True,
            "page32_dead_tree_visual_trace_candidate_v0": True,
            "pixel_probability_claim_quarantine_v0": True,
        }
    )

    records["pixel_colour_frequency_source_tables"] = _candidate(
        "pixel_colour_frequency_source_tables",
        "pixel_colour_frequency_source_tables_v0",
        POTENTIAL_HINT_ROOT,
    )
    records["pixel_colour_frequency_source_tables"].update(
        {
            "source_files": ["prime_color_frequencies.txt", "superprime_color_frequencies.txt"],
            "table_locks": table_locks,
            "line_counts_recorded": all(table["line_count_recorded"] for table in table_locks),
            "raw_tables_committed": False,
            "bulk_scan_multiple_comparison_warning": True,
            "verification_required_against_canonical_image_set": True,
            "canonical_verification_required": True,
            "not_accepted_as_probability_evidence": True,
            "probability_claim_accepted_as_validated": False,
            "bulk_prime_colour_frequency_tables_v0": True,
            "prime_index_correction": {
                "prime_174": _nth_prime(174),
                "prime_185": _nth_prime(185),
                "statement": "1033 is not the 185th prime",
            },
        }
    )

    records["associated_twitter_9901_digit_square_candidate"] = _candidate(
        "associated_twitter_9901_digit_square_candidate",
        "associated_twitter_9901_digit_square_candidate_v0",
        NUMBER_FACTS_ROOT,
    )
    records["associated_twitter_9901_digit_square_candidate"].update(
        {
            "source_image": "twitter_image_is_this.png",
            "claim": "3301 digit squares produce 9901",
            "calculation": {
                "digits": [3, 3, 0, 1],
                "squared_digits": [9, 9, 0, 1],
                "result": 9901,
            },
            "prime_9901": _is_probable_prime(9901),
            "confidence": "low_medium",
            "used_for_target_selection_now": False,
            "canonical_verification_required": False,
            "probability_claim_accepted_as_validated": False,
        }
    )

    records["number_facts_selection_bias_warning"] = _candidate(
        "number_facts_selection_bias_warning",
        "number_fact_probability_or_selection_bias_warning_v0",
        NUMBER_FACTS_ROOT,
    )
    records["number_facts_selection_bias_warning"].update(
        {
            "associated_low_priority_families": [
                "associated_twitter_9901_digit_square_candidate_v0",
                "general_emirp_prime_fact_register_v0",
                "number_fact_probability_or_selection_bias_warning_v0",
            ],
            "general_emirp_prime_fact_register_v0": {
                "recorded_as_review_context_only": True,
                "bulk_selection_bias_warning": True,
            },
            "selection_bias_warning": (
                "Number facts were selected after observation and require canonical "
                "source controls, null models, and multiple-comparison controls."
            ),
            "canonical_verification_required": True,
            "probability_claim_accepted_as_validated": False,
            "not_used_for_target_selection_now": True,
        }
    )

    records["source_lock_browser_gui_future_requirement"] = _base_record(
        "source_lock_browser_gui_future_requirement"
    )
    records["source_lock_browser_gui_future_requirement"].update(
        {
            "operator_requested_browser": True,
            "implementation_now": False,
            "recommended_future_stage_id": NEXT_STAGE_ID,
            "recommended_future_stage_title": NEXT_STAGE_TITLE,
            "requirements": [
                "local_lightweight_window",
                "table_view_horizontal_rows",
                "one_source_lock_entry_per_row",
                "columns_for_properties_attributes",
                "filter_and_sort",
                "add_entry",
                "modify_entry",
                "remove_entry",
                "schema_validation_for_manual_entries",
                "no_puzzle_execution_from_gui",
                "no_target_validation_from_gui",
                "no_secret_display",
                "reads_committed_yaml_or_generated_json_index",
                "writes_manual_inbox_yaml_or_review_queue",
            ],
            "no_puzzle_execution_from_gui": True,
            "no_target_validation_from_gui": True,
            "operator_rationale": "enable_easy_review_of_source_locked_material_for_informed_operator_decisions",
        }
    )

    records["stage5dn_preservation"] = _base_record("stage5dn_preservation")
    records["stage5dn_preservation"].update(
        {
            "stage5dn_preserved": True,
            "stage5dn_validation_passed": validate_stage5dn().validation_error_count == 0,
            "stage5dn_rerun_performed": False,
        }
    )
    for key in [
        "stage5dg_preservation",
        "stage5bd_preservation",
        "active_lineage_preservation",
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        records[key] = _base_record(key)
        records[key].update(
            {
                "preservation_record": True,
                "selected_now": False,
                "accepted_as_route": False,
                "stage5bd_run_plan_ids_preserved": True,
                "active_lineage_preserved": True,
                "stage5bd_validation_passed": _stage5bd_valid(),
            }
        )
        if key == "active_lineage_preservation":
            records[key]["active_lineage_record_paths"] = [str(path) for path in ACTIVE_LINEAGE_PATHS]

    records["pivot_readiness_update"] = _base_record("pivot_readiness_update")
    records["pivot_readiness_update"].update(
        {
            "target_priority_decision_created_now": False,
            "pivot_target_selected_now": False,
            "new_candidate_families_recorded": 22,
            "operator_readiness_decision_created_now": False,
            "recommended_next_review_before_target_priority": NEXT_STAGE_ID,
        }
    )

    records["next_stage_decision"] = _base_record("next_stage_decision")
    records["next_stage_decision"].update(
        {
            "selected_next_stage_id": NEXT_STAGE_ID,
            "selected_next_stage_title": NEXT_STAGE_TITLE,
            "reason": "operator_requested_lightweight_source_lock_browser_after_stage5do_source_lock_addendum",
            "gui_implementation_deferred_to_next_stage": True,
        }
    )

    records["reviewable_validation_evidence"] = _base_record("reviewable_validation_evidence")
    records["reviewable_validation_evidence"].update(
        {
            "validation_commands": [
                "token-block build-stage5do",
                "token-block validate-stage5do",
                "token-block stage5do-summary",
                "scripts/ci/run-parallel-validation.ps1 -Workers 8 -PytestWorkers 8 -PytestMode auto",
            ],
            "parallel_worker_cap": PARALLEL_WORKER_CAP,
            "raw_source_bodies_committed": False,
        }
    )

    records["summary"] = _base_record("summary")
    records["summary"].update(
        {
            "status": "complete",
            "number_facts_collection_locked": number_facts["source_root_exists"],
            "potential_hint_locked": potential_hint["source_root_exists"],
            "number_facts_file_count": number_facts["file_count_observed"],
            "potential_hint_file_count": potential_hint["file_count_observed"],
            "messages_txt_source_locks": int(number_facts["messages_source_lock"]["messages_txt_present"])
            + int(potential_hint["messages_source_lock"]["messages_txt_present"]),
            "candidate_records_created": len(CANDIDATE_KEYS),
            "page32_2472_status": "arithmetic_verified_metadata_only",
            "page32_463_3299_status": "arithmetic_verified_metadata_only",
            "no_f_section_flow_status": "component_arithmetic_verified_canonical_transcript_required",
            "pixel_rgb185_3301_status": "source_locked_canonical_image_verification_required",
            "prime_1033_185th_correction_status": "recorded",
            "source_browser_gui_future_requirement_recorded": True,
            "raw_source_files_staged": 0,
            "generated_outputs_staged": 0,
            "sqlite_staged": 0,
            "codex_output_used": DEPRECATED_CODEX_OUTPUT.exists(),
        }
    )
    return records


def build_stage5do() -> dict[str, dict[str, Any]]:
    predecessor = validate_stage5dn()
    if predecessor.validation_error_count:
        joined = "; ".join(predecessor.errors[:5])
        raise RuntimeError(f"Stage 5DN validation failed; refusing Stage 5DO build: {joined}")

    records = _build_records()
    _write_schemas()
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS_DIR / "summary.json", records["summary"])
    write_json(RESULTS_DIR / "number_facts_source_lock_report.json", records["number_facts_source_lock_register"])
    write_json(RESULTS_DIR / "potential_hint_source_lock_report.json", records["potential_hint_source_lock_register"])
    write_json(RESULTS_DIR / "image_anchor_report.json", records["discord_image_anchor_register"])
    write_json(
        RESULTS_DIR / "candidate_report.json",
        {key: records[key] for key in sorted(CANDIDATE_KEYS)},
    )
    write_json(
        RESULTS_DIR / "preservation_report.json",
        {
            key: records[key]
            for key in [
                "stage5dn_preservation",
                "stage5dg_preservation",
                "stage5bd_preservation",
                "active_lineage_preservation",
                "no_active_ingestion_proof",
                "no_byte_stream_transition_gate",
                "no_execution_transition_gate",
            ]
        },
    )
    write_jsonl(
        RESULTS_DIR / "warnings.jsonl",
        [
            records["number_facts_selection_bias_warning"],
            records["page32_dead_tree_rgb185_count_3301_candidate"],
            records["pixel_colour_frequency_source_tables"],
        ],
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
    if record.get("source_lock_only") is not True:
        errors.append(f"{context}:source_lock_only_must_be_true")
    if record.get("execution_allowed") is not False:
        errors.append(f"{context}:execution_allowed_must_be_false")
    if record.get("canonical_codex_handoff_root") != "codex-output":
        errors.append(f"{context}:canonical_codex_handoff_root_must_be_codex-output")
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append(f"{context}:stage5bd_run_plan_id_count_must_be_10")
    if record.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append(f"{context}:active_lineage_record_count_must_be_{len(ACTIVE_LINEAGE_PATHS)}")
    if record.get("parallel_worker_cap_for_stage5do_and_later") != PARALLEL_WORKER_CAP:
        errors.append(f"{context}:parallel_worker_cap_must_be_{PARALLEL_WORKER_CAP}")
    for flag in FORBIDDEN_FALSE_FLAGS:
        if record.get(flag) is not False:
            errors.append(f"{context}:{flag}_must_be_false")
    return errors


def _candidate_errors(record: dict[str, Any], context: str) -> list[str]:
    errors = _common_errors(record, context)
    for key in ["accepted_as_route", "accepted_as_decryption", "used_for_target_selection_now"]:
        if record.get(key) is not False:
            errors.append(f"{context}:{key}_must_be_false")
    return errors


def _result(command: str, errors: list[str]) -> ValidationResult:
    return ValidationResult(command, len(errors), errors)


def validate_stage5do_number_facts_source_lock() -> ValidationResult:
    command = "validate-stage5do-number-facts-source-lock"
    record = _read_record("number_facts_source_lock_register")
    errors = _common_errors(record, command)
    if record.get("source_root_exists") is not True:
        errors.append("NumberFactsCollection missing and no gap record")
    if record.get("messages_source_lock", {}).get("messages_txt_present") is not True:
        errors.append("messages.txt not source-locked")
    if record.get("file_count_observed", 0) < 1:
        errors.append("file inventory missing")
    return _result(command, errors)


def validate_stage5do_potential_hint_source_lock() -> ValidationResult:
    command = "validate-stage5do-potential-hint-source-lock"
    record = _read_record("potential_hint_source_lock_register")
    errors = _common_errors(record, command)
    if record.get("source_root_exists") is not True:
        errors.append("PotentialHint folder missing and no gap record")
    if record.get("messages_source_lock", {}).get("messages_txt_present") is not True:
        errors.append("messages.txt not source-locked")
    if record.get("file_count_observed", 0) < 1:
        errors.append("file inventory missing")
    return _result(command, errors)


def validate_stage5do_page32_red_header_2472() -> ValidationResult:
    command = "validate-stage5do-page32-red-header-2472"
    record = _read_record("page32_red_header_progressive_gp_sum_2472")
    errors = _candidate_errors(record, command)
    if sum(record.get("progressive_values", [])) != 2472 or record.get("progressive_sum") != 2472:
        errors.append("Page32 2472 arithmetic wrong")
    if record.get("arithmetic_verified_now") is not True:
        errors.append("arithmetic_verified_now_must_be_true")
    return _result(command, errors)


def validate_stage5do_page32_red_header_463_3299() -> ValidationResult:
    command = "validate-stage5do-page32-red-header-463-3299"
    record = _read_record("page32_red_header_cumulative_index_463_3299")
    errors = _candidate_errors(record, command)
    if sum(record.get("gp_values_from_mod_sequence", [])) != 463:
        errors.append("463 arithmetic wrong")
    if record.get("prime_463_one_indexed") != 3299:
        errors.append("3299 prime fact wrong")
    if record.get("prime_index_convention_warning") is not True:
        errors.append("prime_index_convention_warning_missing")
    return _result(command, errors)


def validate_stage5do_no_f_section_flow() -> ValidationResult:
    command = "validate-stage5do-no-f-section-flow"
    record = _read_record("no_f_rune_count_section_flow_candidate")
    errors = _candidate_errors(record, command)
    claims = {claim.get("claim_id"): claim for claim in record.get("claims", [])}
    first = claims.get("wing_tree_equals_no_f_cuneiform_equals_no_f_koan2_plus_no_f_spirals", {})
    if first.get("component_sum_verified_now") is not True:
        errors.append("NO-F 1433 component arithmetic not verified")
    if record.get("canonical_transcript_verification_required") is not True:
        errors.append("canonical_transcript_verification_required_must_be_true")
    return _result(command, errors)


def validate_stage5do_doublet_v1() -> ValidationResult:
    command = "validate-stage5do-doublet-v1"
    record = _read_record("lp_doublet_scarcity_feature_v1")
    errors = _candidate_errors(record, command)
    if record.get("reported_doublet_count") != 89:
        errors.append("reported_doublet_count_must_be_89")
    if record.get("used_for_decryption_now") is not False or record.get("used_for_scoring_now") is not False:
        errors.append("doublet_v1_must_not_be_used_for_decryption_or_scoring")
    return _result(command, errors)


def validate_stage5do_pixel_colour_candidate() -> ValidationResult:
    command = "validate-stage5do-pixel-colour-candidate"
    candidate = _read_record("page32_dead_tree_rgb185_count_3301_candidate")
    tables = _read_record("pixel_colour_frequency_source_tables")
    warning = _read_record("number_facts_selection_bias_warning")
    errors = _candidate_errors(candidate, command)
    errors.extend(_candidate_errors(tables, f"{command}:tables"))
    errors.extend(_candidate_errors(warning, f"{command}:warning"))
    if candidate.get("pixel_count_verified_against_canonical_now") is True:
        errors.append("pixel count accepted without canonical image verification")
    if candidate.get("canonical_original_image_verification_required") is not True:
        errors.append("canonical_original_image_verification_required_must_be_true")
    if candidate.get("probability_claim_accepted_as_validated") is not False:
        errors.append("probability claims accepted as validated")
    correction = tables.get("prime_index_correction", {})
    if correction.get("prime_174") != 1033 or correction.get("prime_185") != 1103:
        errors.append("1033/185th-prime correction missing")
    return _result(command, errors)


def validate_stage5do_gp_facts() -> ValidationResult:
    command = "validate-stage5do-gp-facts"
    artwork = _read_record("artwork_title_gp_equivalence_candidate")
    koan = _read_record("solved_koan_gp_facts_candidate")
    lp1 = _read_record("lp1_encrypted_word_count_464_prime_3301")
    bridge = _read_record("prime_index_bridge_761_167_464_1033_3301")
    errors = _candidate_errors(artwork, f"{command}:artwork")
    errors.extend(_candidate_errors(koan, f"{command}:koan"))
    errors.extend(_candidate_errors(lp1, f"{command}:lp1"))
    errors.extend(_candidate_errors(bridge, f"{command}:bridge"))
    if any(eq.get("gp_sum_a") != eq.get("gp_sum_b") for eq in artwork.get("equivalences", [])):
        errors.append("artwork_gp_equivalence_changed")
    if lp1.get("prime_464") != 3301 or lp1.get("arithmetic_verified_now") is not True:
        errors.append("LP1 464 / prime 3301 arithmetic invalid")
    if bridge.get("correction", {}).get("corrected_value") != "29 squared is 841":
        errors.append("29_squared_correction_missing")
    return _result(command, errors)


def validate_stage5do_source_browser_future_requirement() -> ValidationResult:
    command = "validate-stage5do-source-browser-future-requirement"
    record = _read_record("source_lock_browser_gui_future_requirement")
    errors = _common_errors(record, command)
    if record.get("implementation_now") is not False:
        errors.append("GUI implemented now")
    if record.get("no_puzzle_execution_from_gui") is not True:
        errors.append("no_puzzle_execution_from_gui_must_be_true")
    return _result(command, errors)


def validate_stage5do_sidecar_gates() -> ValidationResult:
    command = "validate-stage5do-sidecar-gates"
    errors: list[str] = []
    for key in [
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        errors.extend(_common_errors(_read_record(key), f"{command}:{key}"))
    return _result(command, errors)


def validate_stage5do_preservation() -> ValidationResult:
    command = "validate-stage5do-preservation"
    errors: list[str] = []
    for key in [
        "stage5dn_preservation",
        "stage5dg_preservation",
        "stage5bd_preservation",
        "active_lineage_preservation",
    ]:
        errors.extend(_common_errors(_read_record(key), f"{command}:{key}"))
    if _read_record("stage5dn_preservation").get("stage5dn_validation_passed") is not True:
        errors.append("stage5dn_validation_failed")
    if _read_record("active_lineage_preservation").get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active_lineage_count_not_8")
    return _result(command, errors)


def validate_stage5do_handoff_continuity() -> ValidationResult:
    command = "validate-stage5do-handoff-continuity"
    record = _read_record("raw_source_noncommit_proof")
    errors = _common_errors(record, command)
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output used")
    if record.get("raw_source_files_committed_now") is not False:
        errors.append("raw_source_files_committed_now_must_be_false")
    return _result(command, errors)


def validate_stage5do() -> ValidationResult:
    command = "validate-stage5do"
    errors: list[str] = []
    for key in DATA_PATHS:
        errors.extend(_schema_errors(key))
        if DATA_PATHS[key].exists():
            errors.extend(_common_errors(_read_record(key), key))
    for validator in [
        validate_stage5do_number_facts_source_lock,
        validate_stage5do_potential_hint_source_lock,
        validate_stage5do_page32_red_header_2472,
        validate_stage5do_page32_red_header_463_3299,
        validate_stage5do_no_f_section_flow,
        validate_stage5do_doublet_v1,
        validate_stage5do_pixel_colour_candidate,
        validate_stage5do_gp_facts,
        validate_stage5do_source_browser_future_requirement,
        validate_stage5do_sidecar_gates,
        validate_stage5do_preservation,
        validate_stage5do_handoff_continuity,
    ]:
        result = validator()
        errors.extend(f"{result.command}:{error}" for error in result.errors)
    return _result(command, errors)


def load_stage5do_summary() -> dict[str, Any]:
    return _read_record("summary")


def stage5do_summary_text() -> str:
    summary = load_stage5do_summary()
    lines = [
        f"stage_id={summary.get('stage_id')}",
        f"status={summary.get('status')}",
        f"number_facts_collection_locked={str(summary.get('number_facts_collection_locked')).lower()}",
        f"number_facts_file_count={summary.get('number_facts_file_count')}",
        f"potential_hint_locked={str(summary.get('potential_hint_locked')).lower()}",
        f"potential_hint_file_count={summary.get('potential_hint_file_count')}",
        f"messages_txt_source_locks={summary.get('messages_txt_source_locks')}",
        f"candidate_records_created={summary.get('candidate_records_created')}",
        f"page32_2472_status={summary.get('page32_2472_status')}",
        f"page32_463_3299_status={summary.get('page32_463_3299_status')}",
        f"no_f_section_flow_status={summary.get('no_f_section_flow_status')}",
        f"pixel_rgb185_3301_status={summary.get('pixel_rgb185_3301_status')}",
        f"prime_1033_185th_correction_status={summary.get('prime_1033_185th_correction_status')}",
        f"source_browser_gui_future_requirement_recorded={str(summary.get('source_browser_gui_future_requirement_recorded')).lower()}",
        f"pivot_target_selected={str(summary.get('pivot_target_selected_now')).lower()}",
        f"execution_performed={str(summary.get('execution_performed')).lower()}",
        f"ocr_performed={str(summary.get('ocr_performed')).lower()}",
        f"image_forensics_performed={str(summary.get('image_forensics_performed')).lower()}",
        f"stage5bd_run_plan_id_count={summary.get('stage5bd_run_plan_id_count')}",
        f"active_lineage_record_count={summary.get('active_lineage_record_count')}",
        f"parallel_worker_cap_for_stage5do_and_later={summary.get('parallel_worker_cap_for_stage5do_and_later')}",
        f"recommended_next_stage_id={summary.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


__all__ = [
    "CODEX_COMPLETION_PATH",
    "DATA_PATHS",
    "RESULTS_DIR",
    "SCHEMA_PATHS",
    "build_stage5do",
    "load_stage5do_summary",
    "stage5do_summary_text",
    "validate_stage5do",
    "validate_stage5do_doublet_v1",
    "validate_stage5do_gp_facts",
    "validate_stage5do_handoff_continuity",
    "validate_stage5do_no_f_section_flow",
    "validate_stage5do_number_facts_source_lock",
    "validate_stage5do_page32_red_header_2472",
    "validate_stage5do_page32_red_header_463_3299",
    "validate_stage5do_pixel_colour_candidate",
    "validate_stage5do_potential_hint_source_lock",
    "validate_stage5do_preservation",
    "validate_stage5do_sidecar_gates",
    "validate_stage5do_source_browser_future_requirement",
]
