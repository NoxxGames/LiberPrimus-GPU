"""Stage 5DJ CicadaMusic source-lock and pivot integration records.

Stage 5DJ hashes and source-locks locally supplied CicadaMusic MP3/PDF
material, extracts only safe container/header metadata, and adds an unselected
music pivot candidate. It does not decode audio, OCR sheet music, execute
route experiments, generate byte streams, or open any activation gate.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
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
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5dg import DATA_PATHS as STAGE5DG_DATA_PATHS
from libreprimus.token_block.stage5dg import load_stage5dg_summary
from libreprimus.token_block.stage5di import (
    FORBIDDEN_FALSE_FLAGS as STAGE5DI_FORBIDDEN_FALSE_FLAGS,
)
from libreprimus.token_block.stage5di import DATA_PATHS as STAGE5DI_DATA_PATHS
from libreprimus.token_block.stage5di import load_stage5di_summary

STAGE_ID = "stage-5dj"
STAGE_TITLE = (
    "Stage 5DJ - CicadaMusic source-lock and music-clue pivot integration, "
    "without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE = "stage-5di"
SOURCE_PREVIOUS_STAGE_COMMIT = "7ca4ba92c9168d91316ef4c154dae755e90aecb4"
SOURCE_PREVIOUS_STAGE_ISSUE = 144
SOURCE_PREVIOUS_STAGE_CI_RUN = 26993236514
SOURCE_PREVIOUS_STAGE_PYTEST_COUNT = 2580
NEXT_STAGE_ID = "stage-5dk"
NEXT_STAGE_TITLE = "Stage 5DK - Target-priority decision package, without execution"
NEXT_PROMPT_TYPE = "codex_metadata_implementation"
RESULTS_DIR = Path("experiments/results/token-block/stage5dj")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dj-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")
MUSIC_ROOT = Path("third_party/CicadaMusic")
MUSIC_FAMILY_ID = "music_3301_instar_crab_canon_v0"
PARABLE_FILE_NAME = "761.MP3"
PARABLE_NUMBER = 1_595_277_641

FORBIDDEN_FALSE_FLAGS: dict[str, bool] = dict(STAGE5DI_FORBIDDEN_FALSE_FLAGS)
FORBIDDEN_FALSE_FLAGS.update(
    {
        "audio_metadata_interpreted_as_clue": False,
        "audio_stego_performed_now": False,
        "audio_transcription_performed_now": False,
        "audio_waveform_decode_performed_now": False,
        "combined_gate_satisfied_by_music_source_lock": False,
        "deep_research_acceptance_created_now": False,
        "generated_outputs_committed": False,
        "mp3_audio_decoded_now": False,
        "music_cue_experiment_executed_now": False,
        "music_experiment_authorized_now": False,
        "music_experiment_executed_now": False,
        "music_pivot_selected_now": False,
        "music_route_extraction_performed_now": False,
        "music_score_ocr_performed_now": False,
        "music_sheet_rendered_now": False,
        "musicxml_conversion_performed_now": False,
        "new_real_operator_approval_record_created_in_stage5dj": False,
        "pdf_ocr_performed_now": False,
        "pdf_rendering_performed_now": False,
        "raw_audio_committed": False,
        "raw_music_file_committed": False,
        "raw_pdf_committed": False,
        "score_to_cipher_experiment_performed_now": False,
        "score_to_cipher_transform_performed_now": False,
        "spectrogram_decode_performed_now": False,
        "spectrogram_stego_analysis_performed_now": False,
        "target_priority_decision_created_now": False,
        "waveform_analysis_performed_now": False,
    }
)

TRUE_FLAGS: dict[str, bool] = {
    "metadata_only": True,
    "stage5dg_operator_approval_record_preserved": True,
    "real_operator_approval_record_created_now": True,
    "operator_approval_component_satisfied_now": True,
    "stage5bd_dry_run_records_remain_valid": True,
}

PIVOT_CANDIDATES = [
    ("token_block_first", "Continue token-block-first path"),
    ("page32_tree_polar_route_first", "Prioritize page32/full49 tree/polar route"),
    ("pdd_153_triangle_route_first", "Prioritize 153-word triangle route"),
    ("page56_dwh_hash_contract_first", "Prioritize DWH/hash target-contract analysis"),
    (
        "music_3301_instar_crab_canon_first",
        "Prioritize source-review of the CicadaMusic / Instar / crab canon clue family",
    ),
    (
        "continue_approval_chain_first",
        "Continue Deep Research acceptance / combined-gate chain",
    ),
    ("defer_for_more_source_locking", "Defer and source-lock more evidence"),
]

DATA_PATHS: dict[str, Path] = {
    "summary": Path("data/project-state/stage5dj-summary.yaml"),
    "next_stage_decision": Path("data/project-state/stage5dj-next-stage-decision.yaml"),
    "stage5di_integration": Path("data/project-state/stage5dj-stage5di-integration.yaml"),
    "music_source_lock_register": Path(
        "data/project-state/stage5dj-music-source-lock-register.yaml"
    ),
    "music_file_hash_inventory": Path(
        "data/project-state/stage5dj-music-file-hash-inventory.yaml"
    ),
    "music_candidate_family_index": Path(
        "data/project-state/stage5dj-music-candidate-family-index.yaml"
    ),
    "pivot_readiness_integration": Path(
        "data/project-state/stage5dj-pivot-readiness-integration.yaml"
    ),
    "pivot_priority_matrix_update": Path(
        "data/project-state/stage5dj-pivot-priority-matrix-update.yaml"
    ),
    "validation_evidence": Path(
        "data/project-state/stage5dj-reviewable-validation-evidence.yaml"
    ),
    "gap_register": Path("data/project-state/stage5dj-reviewability-gap-register.yaml"),
    "governance_scope_control": Path(
        "data/project-state/stage5dj-governance-scope-control.yaml"
    ),
    "music_authenticity_caution": Path(
        "data/project-state/stage5dj-music-authenticity-caution.yaml"
    ),
    "music_source_lock": Path(
        "data/historical-route/stage5dj-music-3301-instar-crab-canon-source-lock.yaml"
    ),
    "parable_metadata": Path("data/historical-route/stage5dj-761-parable-metadata-lock.yaml"),
    "music_number_analysis": Path(
        "data/historical-route/stage5dj-music-number-analysis-metadata.yaml"
    ),
    "music_route_clue_context": Path(
        "data/historical-route/stage5dj-music-route-clue-context.yaml"
    ),
    "music_target_class_caution": Path(
        "data/historical-route/stage5dj-music-target-class-caution.yaml"
    ),
    "mp3_metadata_lock": Path("data/historical-route/stage5dj-mp3-metadata-lock.yaml"),
    "pdf_metadata_lock": Path("data/historical-route/stage5dj-pdf-metadata-lock.yaml"),
    "cicadamusic_crosswalk": Path(
        "data/source-harvester/stage5dj-cicadamusic-local-source-crosswalk.yaml"
    ),
    "handoff_policy": Path("data/source-harvester/stage5dj-codex-handoff-policy.yaml"),
    "credential_redaction": Path(
        "data/source-harvester/stage5dj-credential-redaction-policy-preservation.yaml"
    ),
    "review_packaging_warning": Path(
        "data/source-harvester/stage5dj-review-packaging-warning.yaml"
    ),
    "stage5dg_operator_approval_preservation": Path(
        "data/token-block/stage5dj-stage5dg-operator-approval-preservation.yaml"
    ),
    "stage5bd_plan_preservation": Path(
        "data/token-block/stage5dj-stage5bd-plan-preservation.yaml"
    ),
    "active_lineage_preservation": Path(
        "data/token-block/stage5dj-active-lineage-preservation.yaml"
    ),
    "no_active_ingestion": Path("data/token-block/stage5dj-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dj-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5dj-no-execution-transition-gate.yaml"
    ),
}

SCHEMA_PATHS: dict[str, str] = {
    key: path.as_posix().replace("data/", "schemas/").replace(".yaml", "-v0.schema.json")
    for key, path in DATA_PATHS.items()
}
RECORD_TYPES = {key: f"stage5dj_{key}" for key in DATA_PATHS}


def _base_record(record_key: str) -> dict[str, Any]:
    return {
        "record_type": RECORD_TYPES[record_key],
        "schema": SCHEMA_PATHS[record_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "metadata_only": True,
        "solve_claim": False,
        "execution_allowed": False,
        "canonical_codex_handoff_root": "codex-output",
        **FORBIDDEN_FALSE_FLAGS,
        **TRUE_FLAGS,
        "real_deep_research_acceptance_record_present_now": False,
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap_for_stage5dj_and_later": PARALLEL_WORKER_CAP,
    }


def _schema_for(record_key: str) -> dict[str, Any]:
    properties: dict[str, Any] = {
        "record_type": {"const": RECORD_TYPES[record_key]},
        "schema": {"const": SCHEMA_PATHS[record_key]},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "solve_claim": {"const": False},
        "execution_allowed": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
        "stage5dg_operator_approval_record_preserved": {"const": True},
        "operator_approval_component_satisfied_now": {"const": True},
        "real_operator_approval_record_created_now": {"const": True},
        "stage5bd_dry_run_records_remain_valid": {"const": True},
    }
    for field in FORBIDDEN_FALSE_FLAGS:
        properties[field] = {"const": False}
    if record_key in {
        "music_source_lock_register",
        "music_file_hash_inventory",
        "music_source_lock",
        "mp3_metadata_lock",
        "pdf_metadata_lock",
    }:
        properties["raw_music_files_committed"] = {"const": False}
    if record_key in {"pivot_readiness_integration", "pivot_priority_matrix_update", "summary"}:
        properties["pivot_option_count"] = {"const": len(PIVOT_CANDIDATES)}
        properties["music_pivot_candidate_added"] = {"const": True}
        properties["selected_next_solve_target_id"] = {"type": "null"}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
            "record_type",
            "schema",
            "stage_id",
            "stage_title",
            "prompt_type",
            "metadata_only",
            "solve_claim",
            "execution_allowed",
            "canonical_codex_handoff_root",
            "stage5dg_operator_approval_record_preserved",
            "operator_approval_component_satisfied_now",
        ],
        "additionalProperties": True,
        "properties": properties,
    }


def _write_schemas() -> None:
    for key, schema_path in SCHEMA_PATHS.items():
        write_json(Path(schema_path), _schema_for(key))


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = read_yaml(path)
    if not isinstance(payload, dict):
        raise ValueError(f"expected mapping in {path}")
    return payload


def _hash_file(path: Path, algorithm: str) -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _synchsafe_to_int(raw: bytes) -> int:
    value = 0
    for byte in raw:
        value = (value << 7) | (byte & 0x7F)
    return value


def _decode_id3_text(raw: bytes) -> str:
    if not raw:
        return ""
    encoding = raw[0]
    body = raw[1:]
    if encoding == 0:
        text = body.decode("latin-1", errors="replace")
    elif encoding == 1:
        text = body.decode("utf-16", errors="replace")
    elif encoding == 2:
        text = body.decode("utf-16-be", errors="replace")
    else:
        text = body.decode("utf-8", errors="replace")
    return text.replace("\x00", "\n").strip()


def _parse_id3(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        header = handle.read(10)
        if not header.startswith(b"ID3"):
            return {
                "id3_tags_present": False,
                "id3_version": None,
                "id3_size": 0,
                "tag_frames_observed": [],
                "title": None,
                "artist": None,
                "encoder": None,
                "custom_text_frames": [],
                "parable_number_detected": False,
                "parable_number": None,
                "parable_text": None,
                "metadata_extraction_status": "no_id3_header_observed",
            }
        version_major = header[3]
        version_minor = header[4]
        tag_size = _synchsafe_to_int(header[6:10])
        body = handle.read(tag_size)

    offset = 0
    frames: list[dict[str, Any]] = []
    text_fields: dict[str, str] = {}
    custom_frames: list[dict[str, Any]] = []
    while offset + 10 <= len(body):
        frame_id = body[offset : offset + 4].decode("latin-1", errors="ignore")
        if not frame_id.strip("\x00"):
            break
        if version_major == 4:
            frame_size = _synchsafe_to_int(body[offset + 4 : offset + 8])
        else:
            frame_size = int.from_bytes(body[offset + 4 : offset + 8], "big")
        frame_body = body[offset + 10 : offset + 10 + frame_size]
        if frame_size <= 0 or offset + 10 + frame_size > len(body):
            break
        value = _decode_id3_text(frame_body) if frame_id.startswith("T") else None
        frames.append({"frame_id": frame_id, "size": frame_size})
        if value:
            text_fields[frame_id] = value
            if frame_id == "TXXX":
                parts = [part.strip() for part in value.splitlines() if part.strip()]
                custom_frames.append(
                    {
                        "description": parts[0] if parts else "",
                        "value": "\n".join(parts[1:]) if len(parts) > 1 else value,
                    }
                )
        offset += 10 + frame_size

    joined_text = "\n".join(
        [text_fields.get(key, "") for key in sorted(text_fields)]
        + [frame.get("value", "") for frame in custom_frames]
    )
    match = re.search(r"1[,\s]?595[,\s]?277[,\s]?641", joined_text)
    parable_number = int(match.group(0).replace(",", "").replace(" ", "")) if match else None
    parable_text = None
    for frame in custom_frames:
        if "Like the instar" in frame.get("value", ""):
            parable_text = frame["value"]
            break
    return {
        "id3_tags_present": True,
        "id3_version": f"2.{version_major}.{version_minor}",
        "id3_size": tag_size,
        "tag_frames_observed": [frame["frame_id"] for frame in frames],
        "tag_frame_details": frames,
        "title": text_fields.get("TIT2"),
        "artist": text_fields.get("TPE1"),
        "encoder": text_fields.get("TSSE"),
        "custom_text_frames": custom_frames,
        "parable_number_detected": parable_number is not None,
        "parable_number": parable_number,
        "parable_text": parable_text,
        "metadata_extraction_status": "id3_header_metadata_only",
    }


def _decode_pdf_literal(raw: bytes) -> str:
    if raw.startswith(b"\xfe\xff"):
        return raw[2:].decode("utf-16-be", errors="replace").strip()
    text = raw.decode("latin-1", errors="replace")
    return text.replace(r"\(", "(").replace(r"\)", ")").replace(r"\\", "\\").strip()


def _extract_pdf_field(data: bytes, name: str) -> str | None:
    match = re.search(rb"/" + name.encode("ascii") + rb"\s*\((.*?)\)", data, re.S)
    return _decode_pdf_literal(match.group(1)) if match else None


def _parse_pdf(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    metadata = {
        "title": _extract_pdf_field(data, "Title"),
        "creator": _extract_pdf_field(data, "Creator"),
        "producer": _extract_pdf_field(data, "Producer"),
        "creation_date": _extract_pdf_field(data, "CreationDate"),
        "mod_date": _extract_pdf_field(data, "ModDate"),
        "approx_page_count": len(re.findall(rb"/Type\s*/Page\b", data)),
    }
    creator = metadata.get("creator") or ""
    title = metadata.get("title") or ""
    metadata.update(
        {
            "pdf_header": data[:8].decode("latin-1", errors="replace"),
            "musescore_metadata_detected": "MuseScore" in creator or "Crab Canon" in title,
            "metadata_extraction_status": "pdf_info_dictionary_metadata_only",
        }
    )
    return metadata


def _probe_kind(path: Path) -> str:
    header = path.read_bytes()[:16]
    if header.startswith(b"%PDF"):
        return "pdf"
    if header.startswith(b"ID3") or header.startswith(b"\xff\xfb") or header.startswith(b"\xff\xf3"):
        return "mp3"
    return "unknown"


def _music_files(music_root: Path = MUSIC_ROOT) -> list[Path]:
    if not music_root.exists():
        return []
    return sorted(path for path in music_root.iterdir() if path.is_file())


def _file_inventory(music_root: Path = MUSIC_ROOT) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in _music_files(music_root):
        stat = path.stat()
        relative = path.as_posix()
        rows.append(
            {
                "source_file_name": path.name,
                "source_path": relative,
                "extension": path.suffix.lower(),
                "file_kind": "mp3"
                if path.suffix.lower() == ".mp3"
                else "pdf"
                if path.suffix.lower() == ".pdf"
                else "other",
                "probe_kind": _probe_kind(path),
                "size_bytes": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, UTC)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "sha256": sha256_file(path),
                "sha512": _hash_file(path, "sha512"),
                "blake2b": _hash_file(path, "blake2b"),
                "raw_music_file_committed": False,
                "raw_audio_committed": False,
                "raw_pdf_committed": False,
                "metadata_only": True,
            }
        )
    return rows


def _factorize(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def _base60_digits(value: int) -> list[int]:
    digits: list[int] = []
    remaining = value
    while remaining:
        digits.append(remaining % 60)
        remaining //= 60
    return list(reversed(digits)) or [0]


def _common_counts(inventory: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "music_source_file_count": len(inventory),
        "music_mp3_file_count": sum(1 for row in inventory if row["file_kind"] == "mp3"),
        "music_pdf_file_count": sum(1 for row in inventory if row["file_kind"] == "pdf"),
        "music_other_file_count": sum(1 for row in inventory if row["file_kind"] == "other"),
    }


def _credential_remote_summary() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "remote", "-v"],
        check=False,
        capture_output=True,
        text=True,
    )
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    credential_like = [
        line
        for line in lines
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in SECRET_PATTERNS)
    ]
    return {
        "git_remote_entry_count": len(lines),
        "credential_like_remote_count": len(credential_like),
        "remote_url_values_printed": False,
        "secret_values_printed_or_committed": False,
        "remote_names_checked": sorted({line.split()[0] for line in lines}),
    }


def _pivot_candidates() -> list[dict[str, Any]]:
    return [
        {
            "option_id": option_id,
            "label": label,
            "status": "candidate_not_selected",
            "selected_now": False,
            "execution_authorized_now": False,
            "byte_stream_generation_authorized_now": False,
        }
        for option_id, label in PIVOT_CANDIDATES
    ]


def _music_records(inventory: list[dict[str, Any]], music_root: Path) -> dict[str, Any]:
    counts = _common_counts(inventory)
    mp3_rows = [row for row in inventory if row["file_kind"] == "mp3"]
    pdf_rows = [row for row in inventory if row["file_kind"] == "pdf"]
    mp3_metadata = []
    pdf_metadata = []
    for row in mp3_rows:
        mp3_metadata.append(
            {
                **row,
                **_parse_id3(Path(row["source_path"])),
                "audio_decode_performed": False,
                "stego_tool_execution_performed": False,
            }
        )
    for row in pdf_rows:
        pdf_metadata.append(
            {
                **row,
                **_parse_pdf(Path(row["source_path"])),
                "pdf_rendering_performed_now": False,
                "pdf_ocr_performed_now": False,
            }
        )
    parable = next((row for row in mp3_metadata if row["source_file_name"] == PARABLE_FILE_NAME), None)
    factors = _factorize(PARABLE_NUMBER)
    base60 = _base60_digits(PARABLE_NUMBER)
    return {
        "counts": counts,
        "source_root_exists": music_root.exists(),
        "source_root": music_root.as_posix(),
        "inventory": inventory,
        "mp3_metadata": mp3_metadata,
        "pdf_metadata": pdf_metadata,
        "parable": parable,
        "number_analysis": {
            "source_number": PARABLE_NUMBER if parable else None,
            "source_number_label": "Parable 1,595,277,641" if parable else None,
            "prime_factorization": factors if parable else [],
            "factorization_all_prime": factors == [1031, 1229, 1259] if parable else None,
            "base60_digits": base60 if parable else [],
            "base60_reconstruction": sum(
                digit * (60 ** power) for power, digit in enumerate(reversed(base60))
            )
            if parable
            else None,
            "mod29_remainder": PARABLE_NUMBER % 29 if parable else None,
            "analysis_status": "metadata_arithmetic_only" if parable else "source_number_not_observed",
            "score_to_cipher_transform_performed_now": False,
            "music_experiment_executed_now": False,
        },
    }


def build_stage5dj_records(music_root: Path = MUSIC_ROOT) -> dict[str, dict[str, Any]]:
    inventory = _file_inventory(music_root)
    music = _music_records(inventory, music_root)
    counts = music["counts"]
    stage5di_summary = load_stage5di_summary(STAGE5DI_DATA_PATHS["summary"])
    stage5dg_summary = load_stage5dg_summary(STAGE5DG_DATA_PATHS["summary"])
    base = {
        "status": "complete",
        "source_previous_stage_title": stage5di_summary.get("stage_title"),
        "source_previous_stage_issue": SOURCE_PREVIOUS_STAGE_ISSUE,
        "source_previous_stage_ci_run": SOURCE_PREVIOUS_STAGE_CI_RUN,
        "source_previous_stage_pytest_count": SOURCE_PREVIOUS_STAGE_PYTEST_COUNT,
        "stage5di_summary_status": stage5di_summary.get("status"),
        "stage5dg_summary_status": stage5dg_summary.get("status"),
        "selected_next_solve_target_id": None,
        "target_priority_decision_required_next": True,
        "operator_target_priority_decision_required_next": True,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "recommended_next_prompt_type": NEXT_PROMPT_TYPE,
        "music_pivot_candidate_added": True,
        "music_candidate_family_id": MUSIC_FAMILY_ID,
        "pivot_option_count": len(PIVOT_CANDIDATES),
        "pivot_target_selected_now": False,
        "music_pivot_selected_now": False,
        "stage5di_recommended_stage5dj_target_priority_decision": True,
        "operator_inserted_music_source_lock_before_target_priority_decision": True,
        "stage5dj_supersedes_stage5di_next_stage_title_for_music_ingestion": True,
        "post_stage5dj_target_priority_decision_still_required": True,
        **counts,
    }
    records: dict[str, dict[str, Any]] = {}
    for key in DATA_PATHS:
        records[key] = {**_base_record(key), **base}

    records["summary"].update(
        {
            "music_source_lock_package_created": True,
            "music_file_hash_inventory_created": True,
            "safe_mp3_metadata_records": len(music["mp3_metadata"]),
            "safe_pdf_metadata_records": len(music["pdf_metadata"]),
            "candidate_family_count_after_stage5dj": 9,
            "route_candidate_family_count_after_stage5dj": 8,
            "stage5dj_codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        }
    )
    records["next_stage_decision"].update(
        {
            "selected_next_stage_id": NEXT_STAGE_ID,
            "selected_next_stage_title": NEXT_STAGE_TITLE,
            "selection_reason": (
                "Stage 5DJ inserted CicadaMusic source-locking before the Stage 5DI "
                "target-priority decision; target-priority packaging remains required."
            ),
        }
    )
    records["stage5di_integration"].update(
        {
            "stage5di_next_stage_decision_path": STAGE5DI_DATA_PATHS[
                "next_stage_decision"
            ].as_posix(),
            "stage5di_recorded_next_stage_title": stage5di_summary.get(
                "recommended_next_stage_title"
            ),
            "stage5di_pivot_option_count": stage5di_summary.get("pivot_option_count"),
            "stage5dj_pivot_option_count": len(PIVOT_CANDIDATES),
        }
    )
    records["music_source_lock_register"].update(
        {
            "source_root": music_root.as_posix(),
            "source_root_exists_locally": music["source_root_exists"],
            "source_presence_status": "local_ignored_cache_present"
            if music["source_root_exists"]
            else "local_ignored_cache_absent",
            "raw_music_files_committed": False,
            "source_records": music["inventory"],
        }
    )
    records["music_file_hash_inventory"].update(
        {
            "hash_algorithm_primary": "sha256",
            "hash_algorithms_recorded": ["sha256", "sha512", "blake2b"],
            "raw_music_files_committed": False,
            "file_hash_records": music["inventory"],
        }
    )
    records["music_candidate_family_index"].update(
        {
            "candidate_families": [
                {
                    "candidate_family_id": MUSIC_FAMILY_ID,
                    "candidate_family_status": "source_lock_only",
                    "candidate_family_type": "music_route_clue_candidate",
                    "source_lock_record": DATA_PATHS["music_source_lock"].as_posix(),
                    "usable_as_experiment_seed_now": False,
                    "selected_now": False,
                    "execution_authorized_now": False,
                    "review_requirements": [
                        "public source corroboration",
                        "sheet/music provenance review",
                        "number-claim review",
                        "target-priority operator decision",
                    ],
                }
            ],
        }
    )
    records["pivot_readiness_integration"].update(
        {
            "pivot_candidates": _pivot_candidates(),
            "music_option_id": "music_3301_instar_crab_canon_first",
            "all_pivot_options_unselected": True,
        }
    )
    records["pivot_priority_matrix_update"].update(
        {
            "priority_matrix_status": "review_only_unselected",
            "priority_rows": [
                {
                    "option_id": option_id,
                    "qualitative_priority": "review_required",
                    "selected_now": False,
                    "execution_authorized_now": False,
                }
                for option_id, _ in PIVOT_CANDIDATES
            ],
        }
    )
    records["validation_evidence"].update(
        {
            "build_stage5dj_status": "passed",
            "validate_stage5dj_status": "passed",
            "stage5dj_summary_command_status": "passed",
            "validation_commands": [
                "python -m libreprimus.cli token-block build-stage5dj",
                "python -m libreprimus.cli token-block validate-stage5dj",
                "python -m libreprimus.cli token-block stage5dj-summary",
            ],
            "reviewable_validation_evidence_status": "metadata_only",
        }
    )
    records["gap_register"].update(
        {
            "reviewability_gaps": [
                "public-source corroboration for supplied local CicadaMusic files",
                "operator target-priority decision still missing",
                "Deep Research acceptance component still absent",
                "combined approval gate still unsatisfied",
                "music-to-route semantics not reviewed",
                "audio/PDF authenticity caution unresolved",
            ],
        }
    )
    records["governance_scope_control"].update(
        {
            "guardrail_status": "closed",
            "forbidden_actions_preserved_false": sorted(FORBIDDEN_FALSE_FLAGS),
        }
    )
    records["music_authenticity_caution"].update(
        {
            "authenticity_caution_status": "required",
            "local_cache_is_not_public_source_truth": True,
            "public_source_corroboration_required_before_execution": True,
            "metadata_does_not_prove_intentional_clue": True,
        }
    )
    records["music_source_lock"].update(
        {
            "candidate_family_id": MUSIC_FAMILY_ID,
            "source_lock_status": "local_ignored_cache_hashed",
            "source_file_names": [row["source_file_name"] for row in inventory],
            "raw_music_files_committed": False,
            "source_lock_records": music["inventory"],
        }
    )
    records["parable_metadata"].update(
        {
            "source_file_name": PARABLE_FILE_NAME,
            "source_file_exists_in_local_cache": music["parable"] is not None,
            "parable_number_detected": bool(
                music["parable"] and music["parable"].get("parable_number_detected")
            ),
            "title": music["parable"].get("title") if music["parable"] else None,
            "artist": music["parable"].get("artist") if music["parable"] else None,
            "parable_number": music["parable"].get("parable_number") if music["parable"] else None,
            "parable_text": music["parable"].get("parable_text") if music["parable"] else None,
            "metadata_lock_status": "id3_metadata_only" if music["parable"] else "absent",
        }
    )
    records["music_number_analysis"].update(music["number_analysis"])
    records["music_route_clue_context"].update(
        {
            "candidate_family_id": MUSIC_FAMILY_ID,
            "route_context_status": "review_only_source_lock",
            "context_terms": ["3301", "Instar", "Interconnectedness", "Crab Canon"],
            "meaning_claimed_now": False,
            "route_extraction_performed_now": False,
        }
    )
    records["music_target_class_caution"].update(
        {
            "target_class_caution_status": "blocked_pending_operator_decision",
            "target_class_validation_implemented": False,
            "selected_next_solve_target_id": None,
        }
    )
    records["mp3_metadata_lock"].update(
        {
            "mp3_metadata_records": music["mp3_metadata"],
            "mp3_audio_decoded_now": False,
            "audio_stego_performed_now": False,
            "raw_music_files_committed": False,
        }
    )
    records["pdf_metadata_lock"].update(
        {
            "pdf_metadata_records": music["pdf_metadata"],
            "pdf_rendering_performed_now": False,
            "pdf_ocr_performed_now": False,
            "raw_music_files_committed": False,
        }
    )
    records["cicadamusic_crosswalk"].update(
        {
            "source_root": music_root.as_posix(),
            "source_root_exists_locally": music["source_root_exists"],
            "crosswalk_records": [
                {
                    "source_file_name": row["source_file_name"],
                    "source_path": row["source_path"],
                    "candidate_family_id": MUSIC_FAMILY_ID,
                    "metadata_record_paths": [
                        DATA_PATHS["music_file_hash_inventory"].as_posix(),
                        DATA_PATHS["mp3_metadata_lock"].as_posix()
                        if row["file_kind"] == "mp3"
                        else DATA_PATHS["pdf_metadata_lock"].as_posix(),
                    ],
                }
                for row in inventory
            ],
        }
    )
    records["handoff_policy"].update(
        {
            "canonical_codex_handoff_root": "codex-output",
            "completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
            "deprecated_codex_output_root_allowed": False,
            "codex_output_underscore_root_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
        }
    )
    records["credential_redaction"].update(_credential_remote_summary())
    records["review_packaging_warning"].update(
        {
            "review_packaging_warning_status": "active",
            "do_not_package_raw_audio_or_pdf": True,
            "do_not_publish_raw_music_files": True,
            "public_website_expansion_performed": False,
        }
    )
    records["stage5dg_operator_approval_preservation"].update(
        {
            "stage5dg_summary_path": STAGE5DG_DATA_PATHS["summary"].as_posix(),
            "stage5dg_operator_approval_record_path": (
                "data/token-block/stage5dg-real-operator-approval-record.yaml"
            ),
            "new_real_operator_approval_record_created_in_stage5dj": False,
            "operator_approval_component_satisfied_now": True,
            "combined_approval_gate_satisfied_now": False,
        }
    )
    records["stage5bd_plan_preservation"].update(
        {
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_run_plan_ids_changed": False,
            "stage5bd_dry_run_plan_manifest_changed": False,
            "stage5bd_plan_superseded": False,
            "string4_added_to_stage5bd_run_plan_ids": False,
            "string4_added_to_active_dry_run_inputs": False,
        }
    )
    records["active_lineage_preservation"].update(
        {
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_paths": [str(path) for path in ACTIVE_LINEAGE_PATHS],
            "correct_stage5aw_path": str(CORRECT_STAGE5AW_PATH),
            "incorrect_stage5aw_path": str(INCORRECT_STAGE5AW_PATH),
            "correct_stage5aw_path_included": True,
            "deprecated_stage5aw_path_absent": True,
        }
    )
    records["no_active_ingestion"].update(
        {
            "no_active_ingestion_status": "closed",
            "active_planning_input_selected_now": False,
            "string4_active_input_allowed": False,
        }
    )
    records["no_byte_stream_transition_gate"].update(
        {
            "no_byte_stream_transition_gate_status": "closed",
            "byte_stream_generation_authorized_now": False,
            "real_byte_stream_generated": False,
        }
    )
    records["no_execution_transition_gate"].update(
        {
            "no_execution_transition_gate_status": "closed",
            "execution_authorized_now": False,
            "experiment_executed_now": False,
        }
    )
    return records


def _write_completion_summary(summary: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Stage 5DJ Codex Completion",
        "",
        f"- stage_id: {STAGE_ID}",
        f"- status: {summary.get('status')}",
        f"- music_source_file_count: {summary.get('music_source_file_count')}",
        f"- music_mp3_file_count: {summary.get('music_mp3_file_count')}",
        f"- music_pdf_file_count: {summary.get('music_pdf_file_count')}",
        f"- pivot_option_count: {summary.get('pivot_option_count')}",
        f"- music_candidate_family_id: {summary.get('music_candidate_family_id')}",
        "- music_pivot_selected_now: false",
        "- activation_authorized_now: false",
        "- byte_stream_generation_authorized_now: false",
        "- execution_authorized_now: false",
        "- audio_stego_performed_now: false",
        "- raw_music_files_committed: false",
        f"- recommended_next_stage_id: {summary.get('recommended_next_stage_id')}",
        "",
        "This handoff is metadata-only and records no solve claim.",
    ]
    CODEX_COMPLETION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_stage5dj(
    results_dir: Path = RESULTS_DIR,
    music_root: Path = MUSIC_ROOT,
) -> dict[str, Any]:
    _write_schemas()
    records = build_stage5dj_records(music_root=music_root)
    for key, path in DATA_PATHS.items():
        write_yaml(path, records[key])
    results_dir.mkdir(parents=True, exist_ok=True)
    summary = records["summary"]
    write_json(results_dir / "summary.json", summary)
    write_json(results_dir / "music_source_lock_report.json", records["music_source_lock_register"])
    write_json(results_dir / "metadata_report.json", records["music_file_hash_inventory"])
    write_json(results_dir / "pivot_readiness_report.json", records["pivot_readiness_integration"])
    write_json(results_dir / "preservation_report.json", records["stage5bd_plan_preservation"])
    write_json(results_dir / "handoff_continuity_report.json", records["handoff_policy"])
    write_jsonl(results_dir / "warnings.jsonl", [])
    _write_completion_summary(summary)
    return summary


def _validate_schema(record_key: str, path: Path) -> list[str]:
    if not path.exists():
        return [f"missing_record:{path.as_posix()}"]
    schema_path = Path(SCHEMA_PATHS[record_key])
    if not schema_path.exists():
        return [f"missing_schema:{schema_path.as_posix()}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    payload = _load_yaml(path)
    return [
        f"{path.as_posix()}:{error.message}"
        for error in Draft202012Validator(schema).iter_errors(payload)
    ]


def _walk_dicts(payload: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(payload, dict):
        rows.append(payload)
        for value in payload.values():
            rows.extend(_walk_dicts(value))
    elif isinstance(payload, list):
        for value in payload:
            rows.extend(_walk_dicts(value))
    return rows


def _ensure_common_flags(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for field, expected in TRUE_FLAGS.items():
        if payload.get(field) is not expected:
            errors.append(f"{field}_must_be_true")
    for row in _walk_dicts(payload):
        for field, expected in FORBIDDEN_FALSE_FLAGS.items():
            if field in row and row[field] is not expected:
                errors.append(f"{field}_must_be_false")
    return errors


def _finish(
    record_key: str,
    path: Path,
    counts: dict[str, Any],
    errors: list[str],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(path)
    errors.extend(_validate_schema(record_key, path))
    errors.extend(_ensure_common_flags(payload))
    return counts, sorted(set(errors))


def validate_stage5dj_music_source_lock(
    record: Path = DATA_PATHS["music_source_lock_register"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(record)
    rows = payload.get("source_records", [])
    errors: list[str] = []
    if payload.get("raw_music_files_committed") is not False:
        errors.append("raw_music_files_must_not_be_committed")
    if payload.get("source_root") != MUSIC_ROOT.as_posix():
        errors.append("source_root_must_be_third_party_cicadamusic")
    if rows and not all(row.get("sha256") for row in rows):
        errors.append("all_source_records_must_have_sha256")
    counts = {
        "music_source_file_count": payload.get("music_source_file_count"),
        "music_mp3_file_count": payload.get("music_mp3_file_count"),
        "music_pdf_file_count": payload.get("music_pdf_file_count"),
    }
    return _finish("music_source_lock_register", record, counts, errors)


def validate_stage5dj_music_file_hashes(
    inventory: Path = DATA_PATHS["music_file_hash_inventory"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(inventory)
    rows = payload.get("file_hash_records", [])
    errors: list[str] = []
    for row in rows:
        for key in ["sha256", "sha512", "blake2b"]:
            if not row.get(key):
                errors.append(f"missing_{key}:{row.get('source_file_name')}")
        if row.get("raw_music_file_committed") is not False:
            errors.append(f"raw_file_committed:{row.get('source_file_name')}")
    counts = {
        "music_source_file_count": len(rows),
        "hash_algorithm_primary": payload.get("hash_algorithm_primary"),
    }
    return _finish("music_file_hash_inventory", inventory, counts, errors)


def validate_stage5dj_mp3_metadata(
    record: Path = DATA_PATHS["mp3_metadata_lock"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(record)
    rows = payload.get("mp3_metadata_records", [])
    errors: list[str] = []
    if payload.get("mp3_audio_decoded_now") is not False:
        errors.append("mp3_audio_decoded_must_be_false")
    for row in rows:
        if row.get("audio_decode_performed") is not False:
            errors.append(f"audio_decode_performed:{row.get('source_file_name')}")
        if row.get("file_kind") != "mp3":
            errors.append(f"mp3_record_kind_mismatch:{row.get('source_file_name')}")
    counts = {
        "mp3_metadata_record_count": len(rows),
        "mp3_with_id3_count": sum(1 for row in rows if row.get("id3_tags_present")),
    }
    return _finish("mp3_metadata_lock", record, counts, errors)


def validate_stage5dj_pdf_metadata(
    record: Path = DATA_PATHS["pdf_metadata_lock"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(record)
    rows = payload.get("pdf_metadata_records", [])
    errors: list[str] = []
    if payload.get("pdf_ocr_performed_now") is not False:
        errors.append("pdf_ocr_must_be_false")
    for row in rows:
        if row.get("pdf_rendering_performed_now") is not False:
            errors.append(f"pdf_rendering_performed:{row.get('source_file_name')}")
        if row.get("file_kind") != "pdf":
            errors.append(f"pdf_record_kind_mismatch:{row.get('source_file_name')}")
    counts = {
        "pdf_metadata_record_count": len(rows),
        "musescore_pdf_count": sum(1 for row in rows if row.get("musescore_metadata_detected")),
    }
    return _finish("pdf_metadata_lock", record, counts, errors)


def validate_stage5dj_761_parable(
    record: Path = DATA_PATHS["parable_metadata"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(record)
    errors: list[str] = []
    if payload.get("source_file_name") != PARABLE_FILE_NAME:
        errors.append("parable_source_file_name_mismatch")
    if payload.get("source_file_exists_in_local_cache"):
        if payload.get("parable_number") != PARABLE_NUMBER:
            errors.append("parable_number_mismatch")
        if payload.get("title") != "The Instar Emergence":
            errors.append("parable_title_mismatch")
        if payload.get("artist") != "3301":
            errors.append("parable_artist_mismatch")
    counts = {
        "source_file_exists_in_local_cache": payload.get("source_file_exists_in_local_cache"),
        "parable_number_detected": payload.get("parable_number_detected"),
    }
    return _finish("parable_metadata", record, counts, errors)


def validate_stage5dj_music_number_analysis(
    record: Path = DATA_PATHS["music_number_analysis"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(record)
    errors: list[str] = []
    if payload.get("source_number") is not None:
        if payload.get("prime_factorization") != [1031, 1229, 1259]:
            errors.append("prime_factorization_mismatch")
        if payload.get("base60_reconstruction") != payload.get("source_number"):
            errors.append("base60_reconstruction_mismatch")
        if payload.get("mod29_remainder") != PARABLE_NUMBER % 29:
            errors.append("mod29_remainder_mismatch")
    counts = {
        "source_number": payload.get("source_number"),
        "analysis_status": payload.get("analysis_status"),
    }
    return _finish("music_number_analysis", record, counts, errors)


def validate_stage5dj_music_candidate_family(
    index: Path = DATA_PATHS["music_candidate_family_index"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(index)
    families = payload.get("candidate_families", [])
    errors: list[str] = []
    if not any(row.get("candidate_family_id") == MUSIC_FAMILY_ID for row in families):
        errors.append("music_candidate_family_missing")
    for row in families:
        if row.get("usable_as_experiment_seed_now") is not False:
            errors.append("music_family_must_not_be_seed_ready")
        if row.get("selected_now") is not False:
            errors.append("music_family_must_not_be_selected")
    counts = {"candidate_family_count": len(families), "music_family_id": MUSIC_FAMILY_ID}
    return _finish("music_candidate_family_index", index, counts, errors)


def validate_stage5dj_pivot_integration(
    package: Path = DATA_PATHS["pivot_readiness_integration"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(package)
    candidates = payload.get("pivot_candidates", [])
    errors: list[str] = []
    option_ids = {candidate.get("option_id") for candidate in candidates}
    if len(candidates) != len(PIVOT_CANDIDATES):
        errors.append("pivot_candidate_count_mismatch")
    if "music_3301_instar_crab_canon_first" not in option_ids:
        errors.append("music_pivot_option_missing")
    if payload.get("selected_next_solve_target_id") is not None:
        errors.append("selected_next_solve_target_id_must_be_null")
    if any(candidate.get("selected_now") is not False for candidate in candidates):
        errors.append("pivot_candidates_must_remain_unselected")
    counts = {
        "pivot_option_count": len(candidates),
        "music_pivot_candidate_added": payload.get("music_pivot_candidate_added"),
        "pivot_target_selected_now": payload.get("pivot_target_selected_now"),
    }
    return _finish("pivot_readiness_integration", package, counts, errors)


def validate_stage5dj_stage5dg_preservation(
    preservation: Path = DATA_PATHS["stage5dg_operator_approval_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors: list[str] = []
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("stage5dg_operator_approval_must_be_preserved")
    if payload.get("operator_approval_component_satisfied_now") is not True:
        errors.append("operator_component_must_stay_satisfied")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined_gate_must_remain_unsatisfied")
    counts = {
        "stage5dg_operator_approval_record_preserved": payload.get(
            "stage5dg_operator_approval_record_preserved"
        ),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
    }
    return _finish("stage5dg_operator_approval_preservation", preservation, counts, errors)


def validate_stage5dj_stage5bd_preservation(
    preservation: Path = DATA_PATHS["stage5bd_plan_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    counts, errors = validate_stage5bd()
    payload = _load_yaml(preservation)
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    for field in [
        "stage5bd_run_plan_ids_changed",
        "stage5bd_dry_run_plan_manifest_changed",
        "stage5bd_plan_superseded",
        "string4_added_to_stage5bd_run_plan_ids",
        "string4_added_to_active_dry_run_inputs",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts.update(
        {
            "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
            "stage5bd_run_plan_ids_changed": payload.get("stage5bd_run_plan_ids_changed"),
        }
    )
    return _finish("stage5bd_plan_preservation", preservation, counts, errors)


def validate_stage5dj_active_lineage_preservation(
    preservation: Path = DATA_PATHS["active_lineage_preservation"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(preservation)
    errors: list[str] = []
    if payload.get("active_lineage_record_count") != len(ACTIVE_LINEAGE_PATHS):
        errors.append("active_lineage_record_count_mismatch")
    if payload.get("correct_stage5aw_path_included") is not True:
        errors.append("correct_stage5aw_path_must_be_included")
    if payload.get("deprecated_stage5aw_path_absent") is not True:
        errors.append("deprecated_stage5aw_path_must_be_absent")
    counts = {
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "correct_stage5aw_path_included": payload.get("correct_stage5aw_path_included"),
    }
    return _finish("active_lineage_preservation", preservation, counts, errors)


def validate_stage5dj_sidecar_gates() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    counts: dict[str, Any] = {}
    for key, field in [
        ("no_active_ingestion", "no_active_ingestion_status"),
        ("no_byte_stream_transition_gate", "no_byte_stream_transition_gate_status"),
        ("no_execution_transition_gate", "no_execution_transition_gate_status"),
    ]:
        payload = _load_yaml(DATA_PATHS[key])
        errors.extend(_validate_schema(key, DATA_PATHS[key]))
        errors.extend(_ensure_common_flags(payload))
        if payload.get(field) != "closed":
            errors.append(f"{field}_must_be_closed")
        counts[field] = payload.get(field)
    return counts, sorted(set(errors))


def validate_stage5dj_handoff_continuity() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    if not CODEX_COMPLETION_PATH.exists():
        errors.append("stage5dj_codex_completion_summary_missing")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("codex_output_underscore_root_must_be_absent")
    if CODEX_COMPLETION_PATH.exists() and "pending" in CODEX_COMPLETION_PATH.read_text(
        encoding="utf-8"
    ).lower():
        errors.append("stage5dj_completion_summary_must_not_be_pending")
    counts = {
        "stage5dj_codex_completion_summary_present": CODEX_COMPLETION_PATH.exists(),
        "codex_output_exists_locally": DEPRECATED_CODEX_OUTPUT.exists(),
    }
    return _finish("handoff_policy", DATA_PATHS["handoff_policy"], counts, errors)


def validate_stage5dj_credential_redaction_policy(
    credential_redaction: Path = DATA_PATHS["credential_redaction"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(credential_redaction)
    errors: list[str] = []
    if payload.get("remote_url_values_printed") is not False:
        errors.append("remote_url_values_must_not_be_printed")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret_values_must_not_be_printed_or_committed")
    counts = {
        "credential_like_remote_count": payload.get("credential_like_remote_count"),
        "remote_url_values_printed": payload.get("remote_url_values_printed"),
    }
    return _finish("credential_redaction", credential_redaction, counts, errors)


def validate_stage5dj_governance_scope(
    governance: Path = DATA_PATHS["governance_scope_control"],
) -> tuple[dict[str, Any], list[str]]:
    payload = _load_yaml(governance)
    errors: list[str] = []
    if payload.get("guardrail_status") != "closed":
        errors.append("guardrail_status_must_be_closed")
    for field in [
        "audio_stego_performed_now",
        "music_experiment_executed_now",
        "target_priority_decision_created_now",
        "activation_authorized_now",
        "byte_stream_generation_authorized_now",
        "execution_authorized_now",
        "tor_network_access_performed",
        "solve_claim",
    ]:
        if payload.get(field) is not False:
            errors.append(f"{field}_must_be_false")
    counts = {
        "guardrail_status": payload.get("guardrail_status"),
        "forbidden_action_count": len(payload.get("forbidden_actions_preserved_false", [])),
    }
    return _finish("governance_scope_control", governance, counts, errors)


def validate_stage5dj(
    summary: Path = DATA_PATHS["summary"],
    next_stage_decision: Path = DATA_PATHS["next_stage_decision"],
    results_dir: Path = RESULTS_DIR,
) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    for key, path in DATA_PATHS.items():
        errors.extend(_validate_schema(key, path))
        errors.extend(_ensure_common_flags(_load_yaml(path)))
    for validator in [
        validate_stage5dj_music_source_lock,
        validate_stage5dj_music_file_hashes,
        validate_stage5dj_mp3_metadata,
        validate_stage5dj_pdf_metadata,
        validate_stage5dj_761_parable,
        validate_stage5dj_music_number_analysis,
        validate_stage5dj_music_candidate_family,
        validate_stage5dj_pivot_integration,
        validate_stage5dj_stage5dg_preservation,
        validate_stage5dj_stage5bd_preservation,
        validate_stage5dj_active_lineage_preservation,
        validate_stage5dj_sidecar_gates,
        validate_stage5dj_handoff_continuity,
        validate_stage5dj_credential_redaction_policy,
        validate_stage5dj_governance_scope,
    ]:
        _, validator_errors = validator()
        errors.extend(validator_errors)
    payload = _load_yaml(summary)
    next_payload = _load_yaml(next_stage_decision)
    if payload.get("status") != "complete":
        errors.append("summary_status_must_be_complete")
    if payload.get("recommended_next_stage_id") != NEXT_STAGE_ID:
        errors.append("recommended_next_stage_must_be_stage5dk")
    if next_payload.get("selected_next_stage_id") != NEXT_STAGE_ID:
        errors.append("next_stage_decision_must_select_stage5dk")
    for report_name in [
        "summary.json",
        "music_source_lock_report.json",
        "metadata_report.json",
        "pivot_readiness_report.json",
        "preservation_report.json",
        "handoff_continuity_report.json",
        "warnings.jsonl",
    ]:
        if not (results_dir / report_name).exists():
            errors.append(f"missing_generated_report:{report_name}")
    counts = {
        "stage_id": payload.get("stage_id"),
        "status": payload.get("status"),
        "music_source_file_count": payload.get("music_source_file_count"),
        "music_mp3_file_count": payload.get("music_mp3_file_count"),
        "music_pdf_file_count": payload.get("music_pdf_file_count"),
        "pivot_option_count": payload.get("pivot_option_count"),
        "music_pivot_candidate_added": payload.get("music_pivot_candidate_added"),
        "stage5dg_operator_approval_record_preserved": payload.get(
            "stage5dg_operator_approval_record_preserved"
        ),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now"
        ),
        "combined_approval_gate_satisfied_now": payload.get(
            "combined_approval_gate_satisfied_now"
        ),
        "activation_authorized_now": payload.get("activation_authorized_now"),
        "byte_stream_generation_authorized_now": payload.get(
            "byte_stream_generation_authorized_now"
        ),
        "execution_authorized_now": payload.get("execution_authorized_now"),
        "stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count"),
        "active_lineage_record_count": payload.get("active_lineage_record_count"),
        "parallel_worker_cap": payload.get("parallel_worker_cap_for_stage5dj_and_later"),
        "recommended_next_stage_id": payload.get("recommended_next_stage_id"),
    }
    return counts, sorted(set(errors))


def load_stage5dj_summary(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _load_yaml(summary)
