"""Stage 5BK historical-route planning constraint metadata."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from libreprimus.paths import repo_root

STAGE_ID = "stage-5bk"
STAGE_TITLE = (
    "Stage 5BK - Historical-route planning constraint integration and iddqd-v2 "
    "source-lock addendum, without execution"
)
SOURCE_PREVIOUS_STAGE = "stage-5bj"
SOURCE_PREVIOUS_COMMIT = "0103b24a4b3c77e2c88fba10f60ed5f6b9b1532d"
SOURCE_STAGE5BI_COMMIT = "d3c931b69d7718ff181c5dd0b6201174d36b2f7e"
UPSTREAM_URL = "https://github.com/cicada-solvers/iddqd"
PREFERRED_IDDQD_V2 = Path("third_party/CiadaSolversIddqd_v2")
FALLBACK_IDDQD_V2 = Path("third_party/CicadaSolversIddqd_v2")
RESULTS_DIR = Path("experiments/results/historical-route/stage5bk")
TOKEN_BLOCK_RESULTS_DIR = Path("experiments/results/token-block/stage5bk")
CODEX_COMPLETION_PATH = Path("codex-output/stage5bk-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

DATA_PATHS = {
    "source_root": Path("data/historical-route/stage5bk-iddqd-v2-local-source-root.yaml"),
    "tree_summary": Path("data/historical-route/stage5bk-iddqd-v2-tree-summary.yaml"),
    "candidate_index": Path("data/historical-route/stage5bk-iddqd-v2-source-candidate-index.yaml"),
    "byte_strings": Path("data/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock.yaml"),
    "transcription": Path("data/historical-route/stage5bk-iddqd-v2-transcription-source-lock.yaml"),
    "translation_key_lineage": Path("data/historical-route/stage5bk-iddqd-v2-translation-key-lineage.yaml"),
    "positive_control_context": Path("data/historical-route/stage5bk-iddqd-v2-positive-control-context.yaml"),
    "iddqd_v2_source_gaps": Path("data/historical-route/stage5bk-iddqd-v2-source-gap-register.yaml"),
    "constraint_policy": Path("data/historical-route/stage5bk-historical-planning-constraint-policy.yaml"),
    "family_status": Path("data/historical-route/stage5bk-historical-family-planning-status.yaml"),
    "authenticity": Path("data/historical-route/stage5bk-authenticity-gate-integration.yaml"),
    "stego": Path("data/historical-route/stage5bk-stego-positive-control-constraint-integration.yaml"),
    "numeric": Path("data/historical-route/stage5bk-numeric-and-magic-square-constraint-integration.yaml"),
    "book_code": Path("data/historical-route/stage5bk-book-code-and-text-reference-constraint-integration.yaml"),
    "network_byte": Path("data/historical-route/stage5bk-network-byte-channel-constraint-integration.yaml"),
    "lp_transcription": Path("data/historical-route/stage5bk-liber-primus-transcription-constraint-integration.yaml"),
    "dwh": Path("data/historical-route/stage5bk-dwh-quarantine-reaffirmation.yaml"),
    "gap_severity": Path("data/historical-route/stage5bk-source-gap-severity-register.yaml"),
    "crosswalk_errata": Path("data/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata.yaml"),
    "guardrail": Path("data/historical-route/stage5bk-guardrail.yaml"),
    "string4_crosswalk": Path("data/token-block/stage5bk-page49-51-string4-crosswalk.yaml"),
    "token_block_update": Path("data/token-block/stage5bk-token-block-historical-constraint-update.yaml"),
    "surface_context": Path("data/token-block/stage5bk-2014-surface-and-page49-context-integration.yaml"),
    "lineage": Path("data/token-block/stage5bk-token-block-lineage-preservation.yaml"),
    "future_dry_run_impact": Path("data/token-block/stage5bk-future-dry-run-planning-impact.yaml"),
    "source_summary": Path("data/source-harvester/stage5bk-local-source-root-integration-summary.yaml"),
    "codex_policy": Path("data/source-harvester/stage5bk-codex-handoff-policy-correction.yaml"),
    "summary": Path("data/project-state/stage5bk-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bk-next-stage-decision.yaml"),
}

SCHEMA_PATHS = {
    "source_root": "schemas/historical-route/stage5bk-iddqd-v2-local-source-root-v0.schema.json",
    "tree_summary": "schemas/historical-route/stage5bk-iddqd-v2-tree-summary-v0.schema.json",
    "candidate_index": "schemas/historical-route/stage5bk-iddqd-v2-source-candidate-index-v0.schema.json",
    "byte_strings": "schemas/historical-route/stage5bk-iddqd-v2-byte-strings-source-lock-v0.schema.json",
    "transcription": "schemas/historical-route/stage5bk-iddqd-v2-transcription-source-lock-v0.schema.json",
    "translation_key_lineage": "schemas/historical-route/stage5bk-iddqd-v2-translation-key-lineage-v0.schema.json",
    "positive_control_context": "schemas/historical-route/stage5bk-iddqd-v2-positive-control-context-v0.schema.json",
    "iddqd_v2_source_gaps": "schemas/historical-route/stage5bk-iddqd-v2-source-gap-register-v0.schema.json",
    "constraint_policy": "schemas/historical-route/stage5bk-historical-planning-constraint-policy-v0.schema.json",
    "family_status": "schemas/historical-route/stage5bk-historical-family-planning-status-v0.schema.json",
    "authenticity": "schemas/historical-route/stage5bk-authenticity-gate-integration-v0.schema.json",
    "stego": "schemas/historical-route/stage5bk-stego-positive-control-constraint-integration-v0.schema.json",
    "numeric": "schemas/historical-route/stage5bk-numeric-and-magic-square-constraint-integration-v0.schema.json",
    "book_code": "schemas/historical-route/stage5bk-book-code-and-text-reference-constraint-integration-v0.schema.json",
    "network_byte": "schemas/historical-route/stage5bk-network-byte-channel-constraint-integration-v0.schema.json",
    "lp_transcription": "schemas/historical-route/stage5bk-liber-primus-transcription-constraint-integration-v0.schema.json",
    "dwh": "schemas/historical-route/stage5bk-dwh-quarantine-reaffirmation-v0.schema.json",
    "gap_severity": "schemas/historical-route/stage5bk-source-gap-severity-register-v0.schema.json",
    "crosswalk_errata": "schemas/historical-route/stage5bk-stage5bj-crosswalk-review-and-errata-v0.schema.json",
    "guardrail": "schemas/historical-route/stage5bk-guardrail-v0.schema.json",
    "string4_crosswalk": "schemas/token-block/stage5bk-page49-51-string4-crosswalk-v0.schema.json",
    "token_block_update": "schemas/token-block/stage5bk-token-block-historical-constraint-update-v0.schema.json",
    "surface_context": "schemas/token-block/stage5bk-2014-surface-and-page49-context-integration-v0.schema.json",
    "lineage": "schemas/token-block/stage5bk-token-block-lineage-preservation-v0.schema.json",
    "future_dry_run_impact": "schemas/token-block/stage5bk-future-dry-run-planning-impact-v0.schema.json",
    "source_summary": "schemas/source-harvester/stage5bk-local-source-root-integration-summary-v0.schema.json",
    "codex_policy": "schemas/source-harvester/stage5bk-codex-handoff-policy-correction-v0.schema.json",
    "summary": "schemas/project-state/stage5bk-summary-v0.schema.json",
    "next_stage": "schemas/project-state/stage5bk-next-stage-decision-v0.schema.json",
}

HIGH_PRIORITY_FILES = [
    ("byte_strings", "byte-strings/byte-strings", "network_byte_channel_source"),
    (
        "transcription_master",
        "liber-primus__transcription--master/liber-primus__transcription--master.txt",
        "liber_primus_transcription",
    ),
    (
        "transcription_sentences",
        "liber-primus__transcription--sentences/liber-primus__transcription--sentences.txt",
        "liber_primus_transcription",
    ),
    ("translation", "liber-primus__translation/liber-primus__translation.txt", "translation_reference"),
    (
        "known_plain_text",
        "liber-primus__translation/liber-primus__known-plain-text.txt",
        "translation_reference",
    ),
    (
        "known_plain_text_headlines",
        "liber-primus__translation/liber-primus__known-plain-text--headlines.txt",
        "translation_reference",
    ),
    ("keys", "liber-primus__keys/liber-primus__keys.txt", "key_lineage_reference"),
    ("mabinogion_transcript", "2012/02/mabinogion_transcript", "book_code_reference"),
    ("mabinogion_translation", "2012/02/mabinogion_translation", "book_code_reference"),
    ("answering_machine_mp3", "2012/03/answering_machine_2143909608.mp3", "audio_fixture_candidate"),
    ("iso_3301", "2013/02/3301.iso", "archive_fixture_candidate"),
    ("folly", "2013/02/folly", "text_reference_candidate"),
    ("wisdom", "2013/02/wisdom", "text_reference_candidate"),
    ("mp3_761", "2013/02/761.MP3", "audio_fixture_candidate"),
    ("interconnectedness_mp3", "2014/05/3301 - Interconnectedness.mp3", "audio_fixture_candidate"),
    ("image_4gq25", "2016/01/4gq25.jpg", "image_fixture_candidate"),
    ("babelstone_font", "ttf/BabelStoneRunicBeorhtnoth.ttf", "font_reference"),
]

TREE_DIRECTORIES = [
    ("liber_primus_images_full", "liber-primus__images--full"),
    ("liber_primus_images_unsolved", "liber-primus__images--unsolved"),
    ("lp_outguessed", "lp_outguessed"),
]

FALSE_GUARDRAIL_KEYS = [
    "token_experiment_executed",
    "token_experiments_executed",
    "real_byte_stream_generated",
    "real_token_block_byte_streams_generated",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "full_cartesian_product_enumerated",
    "decoded_bytes_committed",
    "full_hex_body_committed",
    "raw_source_committed",
    "raw_archive_files_committed",
    "raw_iddqd_v2_files_committed",
    "generated_outputs_committed",
    "cuda_execution_performed",
    "cuda_source_modified",
    "scoring_performed",
    "scored_experiments_executed",
    "benchmark_performed",
    "solve_claim",
    "canonical_corpus_active",
    "page_boundaries_final",
    "active_token_block_manifest_changed",
    "codex_output_used",
    "dwh_hash_search_performed",
    "hash_search_performed",
    "hash_preimage_search_performed",
    "decode_attempt_performed",
    "outguess_execution_performed",
    "openpuff_execution_performed",
    "mp3stego_execution_performed",
    "stego_tool_execution_performed",
    "audio_analysis_performed",
    "image_forensics_performed",
    "ocr_performed",
    "ai_ml_interpretation_performed",
    "llm_vision_token_reading_performed",
    "public_website_publication_performed",
    "website_expansion_performed",
    "method_status_upgraded",
]


def _root() -> Path:
    return repo_root()


def _resolve(path: Path | str) -> Path:
    value = Path(path)
    if value.is_absolute():
        return value
    return _root() / value


def _repo_relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(_root().resolve()).as_posix()
    except ValueError:
        return path.as_posix().replace("\\", "/")


def _read_yaml(path: Path | str) -> dict[str, Any]:
    resolved = _resolve(path)
    if not resolved.is_file():
        return {}
    return yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}


def _write_yaml(path: Path | str, payload: dict[str, Any]) -> None:
    resolved = _resolve(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _write_json(path: Path | str, payload: Any) -> None:
    resolved = _resolve(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(path: Path | str, text: str) -> None:
    resolved = _resolve(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(text, encoding="utf-8")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _base_record(record_type: str, schema_key: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": SCHEMA_PATHS[schema_key],
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_stage_ids": ["stage-5bj", "stage-5bi", "stage-5bf", "stage-5bd"],
        "metadata_only": True,
        "solve_claim": False,
    }


def _file_meta(root: Path, relative_path: str | Path) -> dict[str, Any]:
    relative = Path(relative_path)
    resolved = _resolve(root / relative)
    repo_path = (root / relative).as_posix()
    if not resolved.is_file():
        return {
            "source_relative_path": relative.as_posix(),
            "source_repo_path": repo_path,
            "source_path_found": False,
            "source_sha256": None,
            "source_size_bytes": None,
            "media_type_hint": _media_type_hint(relative),
        }
    return {
        "source_relative_path": relative.as_posix(),
        "source_repo_path": repo_path,
        "source_path_found": True,
        "source_sha256": _sha256_file(resolved),
        "source_size_bytes": resolved.stat().st_size,
        "media_type_hint": _media_type_hint(relative),
    }


def _media_type_hint(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".gif", ".webp"}:
        return "image"
    if suffix in {".mp3", ".wav", ".flac", ".ogg"}:
        return "audio"
    if suffix in {".ttf", ".otf"}:
        return "font"
    if suffix in {".iso", ".zip", ".tar", ".gz", ".7z"}:
        return "archive_or_binary"
    if suffix in {".txt", ".md", ""}:
        return "text_or_extensionless"
    return "unknown"


def _git_staged_paths() -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=_root(),
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def _git_tracked_paths(pathspec: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "ls-files", pathspec],
            cwd=_root(),
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    return [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]


def locate_stage5bk_iddqd_v2(
    preferred_relative_path: Path = PREFERRED_IDDQD_V2,
    fallback_relative_path: Path = FALLBACK_IDDQD_V2,
    upstream_url: str = UPSTREAM_URL,
    prior_stage4e_source_delta: Path = Path("data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml"),
    results_dir: Path = RESULTS_DIR,
    out: Path = DATA_PATHS["source_root"],
) -> dict[str, Any]:
    preferred = Path(preferred_relative_path)
    fallback = Path(fallback_relative_path)
    preferred_present = _resolve(preferred).is_dir()
    fallback_present = _resolve(fallback).is_dir()
    selected = preferred if preferred_present else fallback if fallback_present else preferred
    selected_present = _resolve(selected).is_dir()
    prior = _read_yaml(prior_stage4e_source_delta)
    payload = {
        **_base_record("stage5bk_iddqd_v2_local_source_root", "source_root"),
        "preferred_relative_path": preferred.as_posix(),
        "fallback_relative_path": fallback.as_posix(),
        "selected_path": selected.as_posix(),
        "source_root_found": selected_present,
        "preferred_path_found": preferred_present,
        "fallback_path_found": fallback_present,
        "upstream_url": upstream_url,
        "prior_stage4e_source_delta": Path(prior_stage4e_source_delta).as_posix(),
        "prior_stage4e_remote_head": prior.get("remote_head_commit")
        or prior.get("source_delta", {}).get("remote_head_commit")
        or "0e3789ad2949c62ea7fb9e3e00ded93df3b3ce07",
        "source_root_status": "found_preferred_path" if preferred_present else "found_fallback_path" if fallback_present else "blocked_missing_local_root",
        "raw_source_committed": False,
        "raw_iddqd_v2_files_committed": False,
        "generated_outputs_committed": False,
        "execution_allowed": False,
        "codex_output_used": False,
    }
    _write_yaml(out, payload)
    _write_json(Path(results_dir) / "source_root.json", payload)
    return payload


def _tree_files(root: Path) -> list[Path]:
    resolved = _resolve(root)
    if not resolved.is_dir():
        return []
    return sorted([path for path in resolved.rglob("*") if path.is_file()], key=lambda item: _repo_relative(item).lower())


def _tree_digest(root: Path, files: list[Path]) -> tuple[str | None, int]:
    if not files:
        return None, 0
    digest = hashlib.sha256()
    total_size = 0
    root_resolved = _resolve(root).resolve()
    for file_path in files:
        relative = file_path.resolve().relative_to(root_resolved).as_posix()
        size = file_path.stat().st_size
        total_size += size
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(str(size).encode("ascii"))
        digest.update(b"\0")
        digest.update(_sha256_file(file_path).encode("ascii"))
        digest.update(b"\n")
    return digest.hexdigest(), total_size


def _directory_summary(root: Path, relative_dir: str) -> dict[str, Any]:
    directory = _resolve(root / relative_dir)
    if not directory.is_dir():
        return {
            "directory": relative_dir,
            "present": False,
            "file_count": 0,
            "total_size_bytes": 0,
            "tree_digest": None,
            "path_samples": [],
        }
    files = sorted([path for path in directory.rglob("*") if path.is_file()], key=lambda item: item.as_posix().lower())
    digest, total = _tree_digest(root, files)
    return {
        "directory": relative_dir,
        "present": True,
        "file_count": len(files),
        "total_size_bytes": total,
        "tree_digest": digest,
        "path_samples": [_repo_relative(path) for path in files[:10]],
    }


def inventory_stage5bk_iddqd_v2(
    source_root: Path = DATA_PATHS["source_root"],
    results_dir: Path = RESULTS_DIR,
    out_tree_summary: Path = DATA_PATHS["tree_summary"],
    out_candidate_index: Path = DATA_PATHS["candidate_index"],
) -> dict[str, dict[str, Any]]:
    root_record = _read_yaml(source_root)
    selected = Path(root_record.get("selected_path") or PREFERRED_IDDQD_V2)
    root_found = bool(root_record.get("source_root_found"))
    files = _tree_files(selected) if root_found else []
    digest, total_size = _tree_digest(selected, files)
    ext_counts = Counter(path.suffix.lower() or "<none>" for path in files)
    tree_summary = {
        **_base_record("stage5bk_iddqd_v2_tree_summary", "tree_summary"),
        "source_root_path": selected.as_posix(),
        "source_root_found": root_found,
        "total_file_count": len(files),
        "total_size_bytes": total_size,
        "tree_digest": digest,
        "extension_counts": dict(sorted(ext_counts.items())),
        "directory_summaries": [_directory_summary(selected, rel_dir) for _, rel_dir in TREE_DIRECTORIES],
        "raw_source_committed": False,
        "raw_iddqd_v2_files_committed": False,
        "generated_outputs_committed": False,
        "execution_allowed": False,
        "codex_output_used": False,
    }
    candidates = []
    for candidate_id, rel_path, category in HIGH_PRIORITY_FILES:
        meta = _file_meta(selected, rel_path)
        candidates.append(
            {
                "candidate_id": f"stage5bk-iddqd-v2-{candidate_id}",
                "source_category": category,
                "planning_role": _planning_role(category),
                "raw_body_committed": False,
                "execution_allowed": False,
                "solve_claim": False,
                **meta,
            }
        )
    for candidate_id, rel_dir in TREE_DIRECTORIES:
        summary = _directory_summary(selected, rel_dir)
        candidates.append(
            {
                "candidate_id": f"stage5bk-iddqd-v2-{candidate_id}",
                "source_category": "directory_tree",
                "planning_role": "positive_control_or_source_reference_only",
                "source_relative_path": rel_dir,
                "source_repo_path": (selected / rel_dir).as_posix(),
                "source_path_found": summary["present"],
                "directory_file_count": summary["file_count"],
                "directory_tree_digest": summary["tree_digest"],
                "raw_body_committed": False,
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    status_counts = Counter("found" if item["source_path_found"] else "missing" for item in candidates)
    candidate_index = {
        **_base_record("stage5bk_iddqd_v2_source_candidate_index", "candidate_index"),
        "source_root_path": selected.as_posix(),
        "source_root_found": root_found,
        "candidate_count": len(candidates),
        "candidate_found_count": status_counts["found"],
        "candidate_missing_count": status_counts["missing"],
        "status_counts": dict(sorted(status_counts.items())),
        "raw_source_committed": False,
        "raw_iddqd_v2_files_committed": False,
        "generated_outputs_committed": False,
        "execution_allowed": False,
        "records": candidates,
    }
    _write_yaml(out_tree_summary, tree_summary)
    _write_yaml(out_candidate_index, candidate_index)
    _write_json(Path(results_dir) / "tree_summary.json", tree_summary)
    _write_json(Path(results_dir) / "candidate_index.json", candidate_index)
    return {"tree_summary": tree_summary, "candidate_index": candidate_index}


def _planning_role(category: str) -> str:
    if category in {"audio_fixture_candidate", "image_fixture_candidate", "archive_fixture_candidate"}:
        return "positive_control_or_source_reference_only"
    if category == "network_byte_channel_source":
        return "source_lock_only_no_hash_search"
    if category == "font_reference":
        return "reference_only_font_not_shared"
    return "lineage_or_context_only"


def _parse_byte_strings(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="ignore")
    matches = list(re.finditer(r"String\s+(\d+)\s+-\s+([^\n\r*]+)", text, re.IGNORECASE))
    hex_values = re.findall(r"(?<![0-9A-Fa-f])([0-9A-Fa-f]{512})(?![0-9A-Fa-f])", text)
    records = []
    for index, hex_value in enumerate(hex_values, start=1):
        label_match = matches[index - 1] if index - 1 < len(matches) else None
        label = label_match.group(2).strip() if label_match else f"String {index}"
        records.append({"string_number": str(index), "label": label, "hex": hex_value})
    return records


def _stage5ap_primary60_hex(stage5ap_mapping: Path) -> str | None:
    payload = _read_yaml(stage5ap_mapping)
    values = [record.get("mapped_value") for record in payload.get("value_records", [])]
    if len(values) != 256 or any(not isinstance(value, int) or value < 0 or value > 255 for value in values):
        return None
    return bytes(values).hex().upper()


def _surface_hashes(stage5bj_surface_locks: Path) -> dict[int, dict[str, Any]]:
    payload = _read_yaml(stage5bj_surface_locks)
    records = payload.get("records", [])
    mapping: dict[int, dict[str, Any]] = {}
    for index, record in enumerate(records[:3], start=1):
        mapping[index] = {
            "surface_lock_id": record.get("surface_lock_id"),
            "surface_id": record.get("surface_id"),
            "surface_sha256": record.get("exact_surface_sha256"),
            "archive_path": record.get("archive_path"),
        }
    return mapping


def build_stage5bk_iddqd_v2_source_lock(
    source_root: Path = DATA_PATHS["source_root"],
    tree_summary: Path = DATA_PATHS["tree_summary"],
    candidate_index: Path = DATA_PATHS["candidate_index"],
    stage5bj_surface_locks: Path = Path("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml"),
    stage5ap_mapping: Path = Path("data/token-block/stage5ap-token-block-mapping-preflight.yaml"),
    stage5ap_transcription: Path = Path("data/token-block/stage5ap-token-block-canonical-transcription.yaml"),
    results_dir: Path = RESULTS_DIR,
    out_byte_strings: Path = DATA_PATHS["byte_strings"],
    out_transcription: Path = DATA_PATHS["transcription"],
    out_translation_key_lineage: Path = DATA_PATHS["translation_key_lineage"],
    out_positive_control_context: Path = DATA_PATHS["positive_control_context"],
    out_source_gaps: Path = DATA_PATHS["iddqd_v2_source_gaps"],
    out_string4_crosswalk: Path = DATA_PATHS["string4_crosswalk"],
) -> dict[str, dict[str, Any]]:
    root_payload = _read_yaml(source_root)
    root = Path(root_payload.get("selected_path") or PREFERRED_IDDQD_V2)
    root_found = bool(root_payload.get("source_root_found"))
    index_payload = _read_yaml(candidate_index)
    candidates = {item["candidate_id"].replace("stage5bk-iddqd-v2-", ""): item for item in index_payload.get("records", [])}

    byte_path = _resolve(root / "byte-strings/byte-strings")
    parsed_strings = _parse_byte_strings(byte_path) if root_found else []
    surfaces = _surface_hashes(stage5bj_surface_locks)
    records = []
    for parsed in parsed_strings:
        number = int(parsed["string_number"])
        hex_body = parsed["hex"]
        decoded = bytes.fromhex(hex_body)
        surface = surfaces.get(number)
        surface_match = bool(surface and surface.get("surface_sha256") == _sha256_text(hex_body.lower()))
        if number <= 3:
            crosswalk_status = "matches_stage5bj_exact_2014_surface" if surface_match else "source_hash_gap_for_stage5bj_surface"
        else:
            crosswalk_status = "metadata_crosswalk_to_stage5ap_primary60_mapping_only"
        records.append(
            {
                **_base_record("stage5bk_iddqd_v2_byte_string_source_lock", "byte_strings"),
                "byte_string_id": f"stage5bk-iddqd-v2-byte-string-{number}",
                "string_number": number,
                "source_label": parsed["label"],
                "hex_length": len(hex_body),
                "exact_512_hex": len(hex_body) == 512,
                "hex_sha256": _sha256_text(hex_body.lower()),
                "decoded_byte_length": len(decoded),
                "decoded_byte_sha256": _sha256_bytes(decoded),
                "decoded_byte_hash_role": "provenance_only_not_search",
                "surface_crosswalk_status": crosswalk_status,
                "stage5bj_surface_lock_id": surface.get("surface_lock_id") if surface else None,
                "stage5bj_surface_id": surface.get("surface_id") if surface else None,
                "stage5bj_surface_hash_match": surface_match if number <= 3 else None,
                "source_string_body_committed": False,
                "full_hex_body_committed": False,
                "decoded_byte_bodies_committed": False,
                "decoded_bytes_committed": False,
                "real_byte_stream_generated": False,
                "dwh_hash_search_performed": False,
                "hash_search_performed": False,
                "decode_attempt_performed": False,
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    count_512 = sum(1 for record in records if record["exact_512_hex"])
    byte_strings = {
        **_base_record("stage5bk_iddqd_v2_byte_strings_source_lock_set", "byte_strings"),
        "source_root_path": root.as_posix(),
        "byte_strings_source_path": (root / "byte-strings/byte-strings").as_posix(),
        "byte_strings_source_found": byte_path.is_file(),
        "byte_strings_source_sha256": _sha256_file(byte_path) if byte_path.is_file() else None,
        "byte_string_count": len(records),
        "exact_512_hex_string_count": count_512,
        "string1_to_3_stage5bj_crosswalk_count": sum(
            1 for record in records if record["string_number"] <= 3 and record["stage5bj_surface_hash_match"]
        ),
        "string4_page49_crosswalk_created": any(record["string_number"] == 4 for record in records),
        "source_string_bodies_committed": False,
        "full_hex_bodies_committed": False,
        "decoded_byte_bodies_committed": False,
        "decoded_bytes_committed": False,
        "raw_source_committed": False,
        "generated_outputs_committed": False,
        "real_byte_stream_generated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "execution_allowed": False,
        "records": records,
    }

    stage5ap_hex = _stage5ap_primary60_hex(stage5ap_mapping)
    string4 = next((record for record in records if record["string_number"] == 4), None)
    string4_crosswalk = {
        **_base_record("stage5bk_page49_51_string4_crosswalk", "string4_crosswalk"),
        "source_byte_string_id": string4.get("byte_string_id") if string4 else None,
        "source_string4_found": string4 is not None,
        "source_string4_hex_sha256": string4.get("hex_sha256") if string4 else None,
        "source_string4_decoded_byte_sha256": string4.get("decoded_byte_sha256") if string4 else None,
        "stage5ap_mapping_path": Path(stage5ap_mapping).as_posix(),
        "stage5ap_transcription_path": Path(stage5ap_transcription).as_posix(),
        "stage5ap_primary60_hex_sha256": _sha256_text(stage5ap_hex.lower()) if stage5ap_hex else None,
        "stage5ap_primary60_decoded_byte_sha256": _sha256_bytes(bytes.fromhex(stage5ap_hex)) if stage5ap_hex else None,
        "string4_matches_stage5ap_primary60_bytes": (
            string4.get("hex_sha256") == _sha256_text(stage5ap_hex.lower()) if string4 and stage5ap_hex else False
        ),
        "crosswalk_role": "metadata_only_provenance_crosswalk_not_active_input",
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "persisted_token_block_bytes_generated": False,
        "real_byte_stream_generated": False,
        "dwh_hash_search_performed": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "execution_allowed": False,
        "solve_claim": False,
    }

    transcription_records = []
    for key in ["transcription_master", "transcription_sentences"]:
        candidate = candidates.get(key)
        rel_path = candidate.get("source_relative_path") if candidate else ""
        resolved = _resolve(root / rel_path)
        line_count = 0
        if resolved.is_file():
            line_count = len(resolved.read_text(encoding="utf-8", errors="ignore").splitlines())
        transcription_records.append(
            {
                **_base_record("stage5bk_iddqd_v2_transcription_source_lock", "transcription"),
                "transcription_id": f"stage5bk-iddqd-v2-{key}",
                "source_role": "non_canonical_transcription_reference",
                "trusted_as_canonical": False,
                "body_committed": False,
                "line_count": line_count,
                "canonical_transcription_changed": False,
                "execution_allowed": False,
                **(candidate or {}),
            }
        )
    transcription = {
        **_base_record("stage5bk_iddqd_v2_transcription_source_lock_set", "transcription"),
        "transcription_source_lock_count": len(transcription_records),
        "transcription_files_found_count": sum(1 for record in transcription_records if record.get("source_path_found")),
        "trusted_as_canonical": False,
        "transcription_bodies_committed": False,
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "execution_allowed": False,
        "records": transcription_records,
    }

    lineage_keys = ["translation", "known_plain_text", "known_plain_text_headlines", "keys"]
    lineage_records = [
        {
            **_base_record("stage5bk_iddqd_v2_translation_key_source_lock", "translation_key_lineage"),
            "lineage_id": f"stage5bk-iddqd-v2-{key}",
            "lineage_role": "method_lineage_metadata_only",
            "body_committed": False,
            "solver_manifest_created": False,
            "execution_allowed": False,
            **(candidates.get(key) or {}),
        }
        for key in lineage_keys
    ]
    translation_key_lineage = {
        **_base_record("stage5bk_iddqd_v2_translation_key_lineage", "translation_key_lineage"),
        "lineage_record_count": len(lineage_records),
        "lineage_files_found_count": sum(1 for record in lineage_records if record.get("source_path_found")),
        "compact_key_facts": [
            "substitution_or_inverted_gematria_lineage_reference",
            "polyalphabetic_substitution_lineage_reference",
            "clear_text_f_is_not_encrypted_lineage_reference",
            "keys_divinity_and_firfumferenfe_lineage_reference",
            "prime_stream_phi_n_lineage_reference",
        ],
        "translation_or_key_bodies_committed": False,
        "solver_manifest_created": False,
        "execution_allowed": False,
        "solve_claim": False,
        "records": lineage_records,
    }

    positive_records = []
    for key in [
        "answering_machine_mp3",
        "iso_3301",
        "folly",
        "wisdom",
        "mp3_761",
        "interconnectedness_mp3",
        "image_4gq25",
        "babelstone_font",
    ]:
        candidate = candidates.get(key) or {}
        category = candidate.get("source_category")
        positive_records.append(
            {
                **_base_record("stage5bk_iddqd_v2_positive_control_context", "positive_control_context"),
                "context_id": f"stage5bk-iddqd-v2-{key}",
                "source_category": category,
                "readiness_state": "source_locked_metadata_only" if candidate.get("source_path_found") else "blocked_missing_local_file",
                "planning_role": _planning_role(str(category)),
                "positive_control_only": category in {"audio_fixture_candidate", "image_fixture_candidate", "archive_fixture_candidate"},
                "source_reference_only": category in {"font_reference", "text_reference_candidate"},
                "font_committed": False,
                "font_shared": False,
                "raw_binary_committed": False,
                "raw_image_committed": False,
                "raw_audio_committed": False,
                "outguess_execution_performed": False,
                "openpuff_execution_performed": False,
                "mp3stego_execution_performed": False,
                "audio_analysis_performed": False,
                "image_forensics_performed": False,
                "execution_allowed": False,
                "solve_claim": False,
                **candidate,
            }
        )
    for dir_id, rel_dir in TREE_DIRECTORIES:
        summary = _directory_summary(root, rel_dir)
        positive_records.append(
            {
                **_base_record("stage5bk_iddqd_v2_positive_control_context", "positive_control_context"),
                "context_id": f"stage5bk-iddqd-v2-{dir_id}",
                "source_category": "directory_tree",
                "readiness_state": "source_locked_tree_metadata_only" if summary["present"] else "blocked_missing_local_tree",
                "planning_role": "positive_control_or_source_reference_only",
                "positive_control_only": True,
                "source_reference_only": True,
                "raw_binary_committed": False,
                "raw_image_committed": False,
                "raw_audio_committed": False,
                "outguess_execution_performed": False,
                "openpuff_execution_performed": False,
                "mp3stego_execution_performed": False,
                "audio_analysis_performed": False,
                "image_forensics_performed": False,
                "execution_allowed": False,
                "solve_claim": False,
                **summary,
            }
        )
    positive_control_context = {
        **_base_record("stage5bk_iddqd_v2_positive_control_context_set", "positive_control_context"),
        "positive_control_context_count": len(positive_records),
        "source_locked_metadata_count": sum(
            1 for record in positive_records if str(record.get("readiness_state", "")).startswith("source_locked")
        ),
        "positive_control_only_count": sum(1 for record in positive_records if record.get("positive_control_only")),
        "font_committed": False,
        "font_shared": False,
        "raw_binary_committed": False,
        "raw_image_committed": False,
        "raw_audio_committed": False,
        "outguess_execution_performed": False,
        "openpuff_execution_performed": False,
        "mp3stego_execution_performed": False,
        "audio_analysis_performed": False,
        "image_forensics_performed": False,
        "execution_allowed": False,
        "records": positive_records,
    }

    missing_candidates = [
        item for item in index_payload.get("records", []) if not item.get("source_path_found") and item.get("source_category") != "directory_tree"
    ]
    gap_records = [
        {
            **_base_record("stage5bk_iddqd_v2_source_gap", "iddqd_v2_source_gaps"),
            "gap_id": f"stage5bk-iddqd-v2-missing-{item['candidate_id'].replace('stage5bk-iddqd-v2-', '')}",
            "severity": "medium",
            "source_gap_status": "missing_local_iddqd_v2_source",
            "source_relative_path": item.get("source_relative_path"),
            "blocks_execution": True,
            "blocks_metadata_planning": False,
            "recommended_resolution": "Provide the local file through an explicit ignored source-root policy.",
            "execution_allowed": False,
            "solve_claim": False,
        }
        for item in missing_candidates
    ]
    source_gaps = {
        **_base_record("stage5bk_iddqd_v2_source_gap_register", "iddqd_v2_source_gaps"),
        "source_gap_count": len(gap_records),
        "blocking_source_gap_count": sum(1 for record in gap_records if record["blocks_execution"]),
        "records": gap_records,
        "execution_allowed": False,
        "solve_claim": False,
    }

    for path, payload in [
        (out_byte_strings, byte_strings),
        (out_string4_crosswalk, string4_crosswalk),
        (out_transcription, transcription),
        (out_translation_key_lineage, translation_key_lineage),
        (out_positive_control_context, positive_control_context),
        (out_source_gaps, source_gaps),
    ]:
        _write_yaml(path, payload)
    _write_json(Path(results_dir) / "byte_strings_source_lock.json", byte_strings)
    _write_json(Path(results_dir) / "string4_crosswalk.json", string4_crosswalk)
    _write_json(Path(results_dir) / "positive_control_context.json", positive_control_context)
    return {
        "byte_strings": byte_strings,
        "string4_crosswalk": string4_crosswalk,
        "transcription": transcription,
        "translation_key_lineage": translation_key_lineage,
        "positive_control_context": positive_control_context,
        "source_gaps": source_gaps,
    }


def build_stage5bk_planning_constraints(
    stage5bf_technique_taxonomy: Path = Path("data/historical-route/stage5bf-historical-technique-taxonomy.yaml"),
    stage5bf_token_block_impact: Path = Path("data/historical-route/stage5bf-token-block-planning-impact.yaml"),
    stage5bf_source_gaps: Path = Path("data/historical-route/stage5bf-source-gap-register.yaml"),
    stage5bj_summary: Path = Path("data/project-state/stage5bj-summary.yaml"),
    stage5bj_surface_locks: Path = Path("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml"),
    stage5bj_crosswalk_closure: Path = Path("data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml"),
    stage5bj_page_body_crosswalk: Path = Path("data/historical-route/stage5bj-fandom-page-body-crosswalk.yaml"),
    stage5bj_source_gaps: Path = Path("data/historical-route/stage5bj-source-gap-update.yaml"),
    iddqd_v2_byte_strings: Path = DATA_PATHS["byte_strings"],
    iddqd_v2_transcription: Path = DATA_PATHS["transcription"],
    iddqd_v2_translation_key_lineage: Path = DATA_PATHS["translation_key_lineage"],
    results_dir: Path = RESULTS_DIR,
    out_policy: Path = DATA_PATHS["constraint_policy"],
    out_family_status: Path = DATA_PATHS["family_status"],
    out_authenticity: Path = DATA_PATHS["authenticity"],
    out_stego: Path = DATA_PATHS["stego"],
    out_numeric: Path = DATA_PATHS["numeric"],
    out_book_code: Path = DATA_PATHS["book_code"],
    out_network_byte: Path = DATA_PATHS["network_byte"],
    out_lp_transcription: Path = DATA_PATHS["lp_transcription"],
    out_dwh: Path = DATA_PATHS["dwh"],
    out_gap_severity: Path = DATA_PATHS["gap_severity"],
    out_crosswalk_errata: Path = DATA_PATHS["crosswalk_errata"],
) -> dict[str, dict[str, Any]]:
    taxonomy = _read_yaml(stage5bf_technique_taxonomy)
    stage5bf_gaps = _read_yaml(stage5bf_source_gaps)
    page_bodies = _read_yaml(stage5bj_page_body_crosswalk)
    stage5bj_gaps = _read_yaml(stage5bj_source_gaps)
    byte_strings = _read_yaml(iddqd_v2_byte_strings)
    transcription = _read_yaml(iddqd_v2_transcription)
    translation = _read_yaml(iddqd_v2_translation_key_lineage)

    policy_constraints = [
        "historical_route_records_are_planning_constraints_not_execution_inputs",
        "2014_exact_512_hex_surfaces_must_not_be_combined_with_page49_51_without_future_execution_gate",
        "iddqd_v2_byte_strings_are_source_lock_metadata_not_dwh_targets",
        "string4_page49_51_crosswalk_is_metadata_only_and_must_not_generate_token_block_bytes",
        "transcription_and_translation_records_are_non_canonical_lineage_metadata",
        "stego_audio_image_records_are_positive_control_or_source_reference_only",
        "DWH_relationship_remains_quarantined_until_explicit_review_and_null_controls",
        "codex_output_is_deprecated_and_must_not_be_used",
    ]
    policy = {
        **_base_record("stage5bk_historical_planning_constraint_policy", "constraint_policy"),
        "constraint_count": len(policy_constraints),
        "constraints": policy_constraints,
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "execution_allowed": False,
        "real_byte_stream_generated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "stego_tool_execution_performed": False,
        "cuda_execution_performed": False,
        "scoring_performed": False,
        "benchmark_performed": False,
        "codex_output_used": False,
    }

    family_templates = [
        ("authenticity_pgp_route", "blocked_authenticity_gate_required", "PGP authenticity remains a review gate."),
        ("stego_audio_positive_controls", "positive_control_only", "Historical stego/audio artifacts require fixtures and expected outputs."),
        ("numeric_magic_square_controls", "control_or_reference_only", "Numeric and magic-square routes require null controls."),
        ("book_code_text_reference", "reference_only", "Book-code and text-reference material is lineage context only."),
        ("network_byte_channel_surfaces", "blocked_execution", "Network byte channels are source locks, not DWH/hash-search inputs."),
        ("liber_primus_transcription_lineage", "non_canonical_reference", "iddqd-v2 transcriptions do not activate the canonical corpus."),
        ("dwh_quarantine", "quarantined", "DWH relationships remain quarantined."),
        ("token_block_page49_51_context", "blocked_execution", "Page 49-51 execution remains blocked by Stage 5BD gates."),
        ("iddqd_v2_positive_control_context", "source_lock_metadata_only", "Local iddqd-v2 metadata can inform future review."),
    ]
    family_records = [
        {
            **_base_record("stage5bk_historical_family_planning_status", "family_status"),
            "family_id": family_id,
            "planning_status": status,
            "constraint_reason": reason,
            "method_status_upgrade_allowed": False,
            "execution_allowed": False,
            "token_experiment_executed": False,
            "solve_claim": False,
        }
        for family_id, status, reason in family_templates
    ]
    family_status = {
        **_base_record("stage5bk_historical_family_planning_status_set", "family_status"),
        "historical_family_planning_status_count": len(family_records),
        "status_counts": dict(sorted(Counter(record["planning_status"] for record in family_records).items())),
        "records": family_records,
        "method_status_upgraded": False,
        "execution_allowed": False,
    }

    authenticity = _constraint_record(
        "stage5bk_authenticity_gate_integration",
        "authenticity",
        "authenticity_pgp_route",
        ["pgp_network_verification_blocked", "signed_message_claims_require_review"],
        {"stage5bf_technique_count": len(taxonomy.get("techniques", []))},
    )
    stego = _constraint_record(
        "stage5bk_stego_positive_control_constraint_integration",
        "stego",
        "stego_audio_positive_controls",
        ["outguess_positive_control_only", "openpuff_manual_required", "mp3stego_manual_required"],
        {"stego_tool_execution_performed": False},
    )
    numeric = _constraint_record(
        "stage5bk_numeric_and_magic_square_constraint_integration",
        "numeric",
        "numeric_magic_square_controls",
        ["null_controls_required", "multiple_testing_controls_required"],
        {"numeric_or_magic_square_execution_performed": False},
    )
    book_code = _constraint_record(
        "stage5bk_book_code_and_text_reference_constraint_integration",
        "book_code",
        "book_code_text_reference",
        ["source_text_edition_required", "reference_only_until_reviewed"],
        {"book_code_execution_performed": False},
    )
    network_byte = _constraint_record(
        "stage5bk_network_byte_channel_constraint_integration",
        "network_byte",
        "network_byte_channel_surfaces",
        ["source_lock_metadata_only", "dwh_hash_search_blocked", "preimage_search_blocked"],
        {
            "byte_string_count": byte_strings.get("byte_string_count", 0),
            "exact_512_hex_string_count": byte_strings.get("exact_512_hex_string_count", 0),
            "hash_search_performed": False,
            "dwh_hash_search_performed": False,
        },
    )
    lp_transcription = _constraint_record(
        "stage5bk_liber_primus_transcription_constraint_integration",
        "lp_transcription",
        "liber_primus_transcription_lineage",
        ["trusted_as_canonical_false", "canonical_corpus_inactive"],
        {
            "transcription_source_lock_count": transcription.get("transcription_source_lock_count", 0),
            "translation_lineage_record_count": translation.get("lineage_record_count", 0),
            "canonical_corpus_active": False,
            "canonical_transcription_changed": False,
            "active_token_block_manifest_changed": False,
        },
    )
    dwh = _constraint_record(
        "stage5bk_dwh_quarantine_reaffirmation",
        "dwh",
        "dwh_quarantine",
        ["DWH_relation_speculative", "hash_preimage_search_blocked", "null_controls_required"],
        {"dwh_quarantine_reaffirmed": True, "hash_preimage_search_performed": False},
    )

    stage5bj_gap_records = stage5bj_gaps.get("records", [])
    stage5bf_gap_records = stage5bf_gaps.get("records", [])
    gap_records = []
    for record in stage5bj_gap_records:
        gap_records.append(
            {
                **_base_record("stage5bk_source_gap_severity", "gap_severity"),
                "source_gap_id": record.get("gap_id"),
                "source_gap_origin": record.get("source_gap_origin", "stage-5bj"),
                "severity": "high" if record.get("carried_forward") else "medium",
                "blocks_execution": bool(record.get("blocks_execution", True)),
                "blocks_metadata_planning": bool(record.get("blocks_metadata_planning", False)),
                "closure_status": record.get("closure_status"),
                "recommended_resolution": record.get("recommended_resolution", []),
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    for record in stage5bf_gap_records:
        gap_records.append(
            {
                **_base_record("stage5bk_source_gap_severity", "gap_severity"),
                "source_gap_id": record.get("gap_id") or record.get("source_gap_id"),
                "source_gap_origin": "stage-5bf",
                "severity": "medium",
                "blocks_execution": True,
                "blocks_metadata_planning": False,
                "closure_status": record.get("gap_status", "carried_forward"),
                "recommended_resolution": record.get("recommended_resolution", []),
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    severity = {
        **_base_record("stage5bk_source_gap_severity_register", "gap_severity"),
        "source_gap_severity_record_count": len(gap_records),
        "blocking_source_gap_count": sum(1 for record in gap_records if record["blocks_execution"]),
        "severity_counts": dict(sorted(Counter(record["severity"] for record in gap_records).items())),
        "records": gap_records,
        "execution_allowed": False,
        "solve_claim": False,
    }

    suspicious = [
        record
        for record in page_bodies.get("records", [])
        if record.get("source_url") == "https://uncovering-cicada.fandom.com/wiki/Hidden_content_of_original_image_(January_4th_2013)"
    ]
    errata_records = []
    for record in suspicious:
        paths = record.get("route_equivalent_paths", [])
        warning_needed = any(str(path).endswith("assets/2016/4gq25.jpg") for path in paths)
        errata_records.append(
            {
                **_base_record("stage5bk_stage5bj_crosswalk_review_and_errata", "crosswalk_errata"),
                "errata_id": "stage5bk-stage5bj-hidden-content-4gq25-review-warning",
                "source_stage5bj_record_id": record.get("page_crosswalk_id"),
                "source_url": record.get("source_url"),
                "review_status": "planning_supersession_warning" if warning_needed else "no_errata_required",
                "warning": (
                    "Stage 5BJ linked a Fandom hidden-original-image page-body row to the 2016 4gq25 media fixture. "
                    "Stage 5BK treats that as media/source-reference context, not an exact Fandom page-body snapshot."
                    if warning_needed
                    else None
                ),
                "supersedes_for_planning": warning_needed,
                "route_equivalent_file_is_page_body_snapshot": False,
                "route_equivalent_file_is_media_fixture": warning_needed,
                "corrected_planning_status": "positive_control_only_or_source_reference_only",
                "execution_allowed": False,
                "image_forensics_performed": False,
                "solve_claim": False,
            }
        )
    crosswalk_errata = {
        **_base_record("stage5bk_stage5bj_crosswalk_review_and_errata_set", "crosswalk_errata"),
        "stage5bj_crosswalk_errata_count": len(errata_records),
        "planning_warning_count": sum(1 for record in errata_records if record.get("supersedes_for_planning")),
        "records": errata_records,
        "execution_allowed": False,
        "solve_claim": False,
    }

    outputs = {
        "policy": policy,
        "family_status": family_status,
        "authenticity": authenticity,
        "stego": stego,
        "numeric": numeric,
        "book_code": book_code,
        "network_byte": network_byte,
        "lp_transcription": lp_transcription,
        "dwh": dwh,
        "gap_severity": severity,
        "crosswalk_errata": crosswalk_errata,
    }
    for path, payload in [
        (out_policy, policy),
        (out_family_status, family_status),
        (out_authenticity, authenticity),
        (out_stego, stego),
        (out_numeric, numeric),
        (out_book_code, book_code),
        (out_network_byte, network_byte),
        (out_lp_transcription, lp_transcription),
        (out_dwh, dwh),
        (out_gap_severity, severity),
        (out_crosswalk_errata, crosswalk_errata),
    ]:
        _write_yaml(path, payload)
    _write_json(Path(results_dir) / "planning_constraints.json", outputs)
    _write_json(Path(results_dir) / "source_gap_severity.json", severity)
    _write_json(Path(results_dir) / "crosswalk_errata.json", crosswalk_errata)
    return outputs


def _constraint_record(
    record_type: str,
    schema_key: str,
    family_id: str,
    constraints: list[str],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        **_base_record(record_type, schema_key),
        "family_id": family_id,
        "constraint_count": len(constraints),
        "constraints": constraints,
        "planning_status": "blocked_or_reference_only",
        "execution_enabled": False,
        "execution_allowed": False,
        "token_experiment_executed": False,
        "real_byte_stream_generated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "stego_tool_execution_performed": False,
        "cuda_execution_performed": False,
        "scoring_performed": False,
        "benchmark_performed": False,
        "method_status_upgraded": False,
        "solve_claim": False,
        **(extra or {}),
    }


def build_stage5bk_token_block_impact(
    constraint_policy: Path = DATA_PATHS["constraint_policy"],
    family_status: Path = DATA_PATHS["family_status"],
    gap_severity: Path = DATA_PATHS["gap_severity"],
    string4_crosswalk: Path = DATA_PATHS["string4_crosswalk"],
    stage5bd_summary: Path = Path("data/project-state/stage5bd-summary.yaml"),
    stage5bj_lineage: Path = Path("data/token-block/stage5bj-token-block-lineage-preservation.yaml"),
    results_dir: Path = TOKEN_BLOCK_RESULTS_DIR,
    out_token_block_update: Path = DATA_PATHS["token_block_update"],
    out_surface_context: Path = DATA_PATHS["surface_context"],
    out_lineage: Path = DATA_PATHS["lineage"],
    out_future_dry_run_impact: Path = DATA_PATHS["future_dry_run_impact"],
) -> dict[str, dict[str, Any]]:
    policy = _read_yaml(constraint_policy)
    family = _read_yaml(family_status)
    gaps = _read_yaml(gap_severity)
    string4 = _read_yaml(string4_crosswalk)
    stage5bd = _read_yaml(stage5bd_summary)
    previous_lineage = _read_yaml(stage5bj_lineage)
    update = {
        **_base_record("stage5bk_token_block_historical_constraint_update", "token_block_update"),
        "historical_constraints_integrated": True,
        "historical_family_planning_status_count": family.get("historical_family_planning_status_count", 0),
        "blocking_source_gap_count": gaps.get("blocking_source_gap_count", 0),
        "string4_crosswalk_created": bool(string4.get("source_string4_found")),
        "string4_crosswalk_role": string4.get("crosswalk_role"),
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "token_experiment_executed": False,
        "real_byte_stream_generated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "execution_allowed": False,
        "solve_claim": False,
    }
    surface_context = {
        **_base_record("stage5bk_2014_surface_and_page49_context_integration", "surface_context"),
        "stage5bj_exact_2014_surfaces_available_as_metadata": True,
        "stage5bj_exact_2014_surfaces_count": 3,
        "page49_51_string4_crosswalk_available_as_metadata": bool(string4.get("source_string4_found")),
        "combination_with_page49_51_allowed": False,
        "dwh_hash_search_allowed": False,
        "future_execution_requires_new_explicit_authorisation": True,
        "execution_allowed": False,
        "real_byte_stream_generated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "solve_claim": False,
    }
    lineage = {
        **_base_record("stage5bk_token_block_lineage_preservation", "lineage"),
        "source_stage5bj_lineage": Path(stage5bj_lineage).as_posix(),
        "stage5bj_lineage_present": bool(previous_lineage),
        "active_stage5aw_branch_manifest_preserved": True,
        "active_stage5az_variant_family_manifest_preserved": True,
        "stage5bd_active_manifest_lock_preserved": True,
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "token_experiment_executed": False,
        "real_byte_stream_generated": False,
        "execution_allowed": False,
        "solve_claim": False,
    }
    future = {
        **_base_record("stage5bk_future_dry_run_planning_impact", "future_dry_run_impact"),
        "source_stage5bd_summary": Path(stage5bd_summary).as_posix(),
        "stage5bd_status": stage5bd.get("status"),
        "dry_run_plan_ids_remain_metadata_only": True,
        "new_constraints_for_future_dry_run": policy.get("constraints", []),
        "future_runner_must_cite_stage5bk_constraints": True,
        "execution_gate_default": "blocked",
        "token_experiment_executed": False,
        "real_byte_stream_generated": False,
        "variant_materialisation_performed": False,
        "full_cartesian_product_enumerated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "scoring_performed": False,
        "execution_allowed": False,
        "solve_claim": False,
    }
    for path, payload in [
        (out_token_block_update, update),
        (out_surface_context, surface_context),
        (out_lineage, lineage),
        (out_future_dry_run_impact, future),
    ]:
        _write_yaml(path, payload)
    _write_json(Path(results_dir) / "token_block_impact.json", {**update, "surface_context": surface_context})
    return {"token_block_update": update, "surface_context": surface_context, "lineage": lineage, "future_dry_run_impact": future}


def build_stage5bk_summary(
    source_root: Path = DATA_PATHS["source_root"],
    tree_summary: Path = DATA_PATHS["tree_summary"],
    candidate_index: Path = DATA_PATHS["candidate_index"],
    byte_strings: Path = DATA_PATHS["byte_strings"],
    transcription: Path = DATA_PATHS["transcription"],
    translation_key_lineage: Path = DATA_PATHS["translation_key_lineage"],
    positive_control_context: Path = DATA_PATHS["positive_control_context"],
    iddqd_v2_source_gaps: Path = DATA_PATHS["iddqd_v2_source_gaps"],
    constraint_policy: Path = DATA_PATHS["constraint_policy"],
    family_status: Path = DATA_PATHS["family_status"],
    authenticity: Path = DATA_PATHS["authenticity"],
    stego: Path = DATA_PATHS["stego"],
    numeric: Path = DATA_PATHS["numeric"],
    book_code: Path = DATA_PATHS["book_code"],
    network_byte: Path = DATA_PATHS["network_byte"],
    lp_transcription: Path = DATA_PATHS["lp_transcription"],
    dwh: Path = DATA_PATHS["dwh"],
    gap_severity: Path = DATA_PATHS["gap_severity"],
    crosswalk_errata: Path = DATA_PATHS["crosswalk_errata"],
    token_block_update: Path = DATA_PATHS["token_block_update"],
    surface_context: Path = DATA_PATHS["surface_context"],
    string4_crosswalk: Path = DATA_PATHS["string4_crosswalk"],
    lineage: Path = DATA_PATHS["lineage"],
    future_dry_run_impact: Path = DATA_PATHS["future_dry_run_impact"],
    results_dir: Path = RESULTS_DIR,
    out_source_summary: Path = DATA_PATHS["source_summary"],
    out_codex_policy: Path = DATA_PATHS["codex_policy"],
    out_guardrail: Path = DATA_PATHS["guardrail"],
    out_next_stage: Path = DATA_PATHS["next_stage"],
    out_summary: Path = DATA_PATHS["summary"],
) -> dict[str, Any]:
    root = _read_yaml(source_root)
    tree = _read_yaml(tree_summary)
    index = _read_yaml(candidate_index)
    byte = _read_yaml(byte_strings)
    trans = _read_yaml(transcription)
    transkey = _read_yaml(translation_key_lineage)
    positive = _read_yaml(positive_control_context)
    policy = _read_yaml(constraint_policy)
    family = _read_yaml(family_status)
    dwh_payload = _read_yaml(dwh)
    severity = _read_yaml(gap_severity)
    errata = _read_yaml(crosswalk_errata)
    update = _read_yaml(token_block_update)
    string4 = _read_yaml(string4_crosswalk)
    lineage_payload = _read_yaml(lineage)
    future = _read_yaml(future_dry_run_impact)

    source_summary = {
        **_base_record("stage5bk_local_source_root_integration_summary", "source_summary"),
        "iddqd_v2_selected_path": root.get("selected_path"),
        "iddqd_v2_source_root_found": root.get("source_root_found", False),
        "iddqd_v2_total_file_count": tree.get("total_file_count", 0),
        "iddqd_v2_tree_digest": tree.get("tree_digest"),
        "candidate_count": index.get("candidate_count", 0),
        "candidate_found_count": index.get("candidate_found_count", 0),
        "candidate_missing_count": index.get("candidate_missing_count", 0),
        "raw_source_committed": False,
        "raw_iddqd_v2_files_committed": False,
        "generated_outputs_committed": False,
        "codex_output_used": False,
    }
    codex_policy = {
        **_base_record("stage5bk_codex_handoff_policy_correction", "codex_policy"),
        "canonical_handoff_root": "codex-output",
        "deprecated_handoff_root": "codex_output",
        "deprecated_root_deleted_by_operator": not _resolve(DEPRECATED_CODEX_OUTPUT).exists(),
        "future_stages_must_use_deprecated_root": False,
        "historical_stage5bj_local_path_reference_preserved_as_historical_context": True,
        "codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "codex_output_used": False,
        "codex_output_committed": False,
        "codex_output_directory_created": False,
    }
    guardrail = {
        **_base_record("stage5bk_guardrail", "guardrail"),
        "planning_constraint_integration_only": True,
        "metadata_only": True,
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "no_execution_guardrail_false_keys": FALSE_GUARDRAIL_KEYS,
        **{key: False for key in FALSE_GUARDRAIL_KEYS},
    }
    summary = {
        **_base_record("stage5bk_summary", "summary"),
        "status": "complete",
        "iddqd_v2_source_root_found": root.get("source_root_found", False),
        "iddqd_v2_selected_path": root.get("selected_path"),
        "iddqd_v2_tree_digest": tree.get("tree_digest"),
        "iddqd_v2_total_file_count": tree.get("total_file_count", 0),
        "iddqd_v2_byte_strings_source_locked": byte.get("byte_strings_source_found", False),
        "iddqd_v2_byte_string_count": byte.get("byte_string_count", 0),
        "iddqd_v2_exact_512_hex_string_count": byte.get("exact_512_hex_string_count", 0),
        "iddqd_v2_string4_page49_crosswalk_created": string4.get("source_string4_found", False),
        "iddqd_v2_transcription_source_lock_created": bool(trans.get("transcription_source_lock_count")),
        "iddqd_v2_translation_key_lineage_created": bool(transkey.get("lineage_record_count")),
        "iddqd_v2_positive_control_context_created": bool(positive.get("positive_control_context_count")),
        "historical_planning_constraint_policy_created": bool(policy),
        "historical_family_planning_status_count": family.get("historical_family_planning_status_count", 0),
        "authenticity_gate_integration_created": bool(_read_yaml(authenticity)),
        "stego_positive_control_constraint_created": bool(_read_yaml(stego)),
        "numeric_magic_square_constraint_created": bool(_read_yaml(numeric)),
        "book_code_text_reference_constraint_created": bool(_read_yaml(book_code)),
        "network_byte_channel_constraint_created": bool(_read_yaml(network_byte)),
        "liber_primus_transcription_constraint_created": bool(_read_yaml(lp_transcription)),
        "dwh_quarantine_reaffirmed": dwh_payload.get("dwh_quarantine_reaffirmed", False),
        "source_gap_severity_record_count": severity.get("source_gap_severity_record_count", 0),
        "stage5bj_crosswalk_errata_count": errata.get("stage5bj_crosswalk_errata_count", 0),
        "token_block_historical_constraint_update_created": bool(update),
        "future_dry_run_planning_impact_created": bool(future),
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "stage5bd_dry_run_records_remain_valid": lineage_payload.get("stage5bd_dry_run_records_remain_valid", True),
        "future_token_block_execution_remains_blocked": update.get("future_token_block_execution_remains_blocked", True),
        "metadata_only": True,
        "raw_archive_files_committed": False,
        "raw_iddqd_v2_files_committed": False,
        "fandom_page_bodies_committed": False,
        "fandom_images_committed": False,
        "full_surface_bodies_committed": False,
        "decoded_byte_bodies_committed": False,
        "generated_outputs_committed": False,
        "token_experiments_executed": False,
        "real_token_block_byte_streams_generated": False,
        "variant_byte_streams_generated": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "stego_tool_execution_performed": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "scored_experiments_executed": False,
        "solve_claim": False,
        "parallel_validation_harness_used": True,
        "parallel_validation_run_passed": None,
        "consistency_checks_passed": None,
        "codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "codex_output_directory_used": False,
        "recommended_next_prompt_type": "deep_research_review",
        "recommended_next_stage_title": (
            "Stage 5BL - Deep Research review of historical-route planning constraints "
            "and iddqd-v2 source-lock integration, without execution"
        ),
        "recommended_next_stage_reason": (
            "Stage 5BK integrates iddqd-v2 source-lock metadata and historical-route "
            "constraints cleanly while preserving token-block execution gates; the next safe "
            "step is independent review, not execution."
        ),
    }
    next_stage = {
        **_base_record("stage5bk_next_stage_decision", "next_stage"),
        "selected_next_stage_id": "stage-5bl",
        "selected_next_prompt_type": summary["recommended_next_prompt_type"],
        "selected_next_stage_title": summary["recommended_next_stage_title"],
        "selected_next_stage_reason": summary["recommended_next_stage_reason"],
        "token_block_execution_selected": False,
        "byte_stream_generation_selected": False,
        "variant_materialisation_selected": False,
        "dwh_hash_search_selected": False,
        "hash_preimage_search_selected": False,
        "decode_selected": False,
        "scored_experiments_selected": False,
        "benchmark_selected": False,
        "cuda_selected": False,
        "public_website_expansion_selected": False,
        "stego_execution_selected": False,
        "pgp_verification_selected": False,
        "audio_analysis_selected": False,
        "image_forensics_selected": False,
        "ocr_selected": False,
        "ai_ml_selected": False,
        "canonical_corpus_activation_selected": False,
        "page_boundary_finalisation_selected": False,
        "solve_claim": False,
    }
    for path, payload in [
        (out_source_summary, source_summary),
        (out_codex_policy, codex_policy),
        (out_guardrail, guardrail),
        (out_next_stage, next_stage),
        (out_summary, summary),
    ]:
        _write_yaml(path, payload)
    _write_json(Path(results_dir) / "summary.json", summary)
    _write_text(
        CODEX_COMPLETION_PATH,
        "\n".join(
            [
                "# Stage 5BK Codex Completion",
                "",
                f"Stage: {STAGE_TITLE}",
                f"Selected iddqd-v2 path: {summary['iddqd_v2_selected_path']}",
                f"Tree files: {summary['iddqd_v2_total_file_count']}",
                f"Byte strings: {summary['iddqd_v2_byte_string_count']}",
                f"String 4 crosswalk created: {summary['iddqd_v2_string4_page49_crosswalk_created']}",
                "No token-block execution, byte-stream generation, DWH/hash search, stego/audio/image work, CUDA, scoring, benchmark, or solve claim was performed.",
                "Canonical handoff root: codex-output",
                "Deprecated root used: false",
                "",
            ]
        ),
    )
    return summary


def validate_stage5bk(paths: dict[str, Path] | None = None) -> dict[str, Any]:
    path_map = {**DATA_PATHS, **(paths or {})}
    errors: list[str] = []
    payloads: dict[str, dict[str, Any]] = {}
    required = [
        "source_root",
        "tree_summary",
        "candidate_index",
        "byte_strings",
        "transcription",
        "translation_key_lineage",
        "positive_control_context",
        "iddqd_v2_source_gaps",
        "constraint_policy",
        "family_status",
        "authenticity",
        "stego",
        "numeric",
        "book_code",
        "network_byte",
        "lp_transcription",
        "dwh",
        "gap_severity",
        "crosswalk_errata",
        "token_block_update",
        "surface_context",
        "string4_crosswalk",
        "lineage",
        "future_dry_run_impact",
        "source_summary",
        "codex_policy",
        "guardrail",
        "next_stage",
        "summary",
    ]
    for key in required:
        path = path_map[key]
        resolved = _resolve(path)
        if not resolved.is_file():
            errors.append(f"missing required Stage 5BK record: {path}")
            continue
        payloads[key] = _read_yaml(path)
    for key, payload in payloads.items():
        if payload.get("stage_id") != STAGE_ID:
            errors.append(f"{key} has wrong stage_id {payload.get('stage_id')!r}")
        _collect_forbidden_flag_errors(payload, key, errors)
    byte = payloads.get("byte_strings", {})
    if byte.get("byte_strings_source_found") and byte.get("byte_string_count") != 4:
        errors.append("byte-strings source is present but byte_string_count is not 4")
    if byte.get("byte_strings_source_found") and byte.get("exact_512_hex_string_count") != 4:
        errors.append("byte-strings source is present but exact_512_hex_string_count is not 4")
    string4 = payloads.get("string4_crosswalk", {})
    if string4.get("active_token_block_manifest_changed") is not False:
        errors.append("String 4 crosswalk changed active token-block manifest")
    if string4.get("persisted_token_block_bytes_generated") is not False:
        errors.append("String 4 crosswalk generated persisted token-block bytes")
    summary = payloads.get("summary", {})
    if summary:
        if summary.get("iddqd_v2_byte_string_count") != byte.get("byte_string_count"):
            errors.append("summary byte-string count mismatch")
        if summary.get("source_gap_severity_record_count") != payloads.get("gap_severity", {}).get(
            "source_gap_severity_record_count"
        ):
            errors.append("summary source-gap severity count mismatch")
        if summary.get("codex_output_directory_used") is not False:
            errors.append("summary says codex_output was used")
    if _resolve(DEPRECATED_CODEX_OUTPUT).exists():
        errors.append("deprecated codex_output directory exists")
    forbidden_staged_prefixes = [
        "third_party/CiadaSolversIddqd_v2",
        "third_party/CicadaSolversIddqd_v2",
        "experiments/results/historical-route/stage5bk",
        "experiments/results/token-block/stage5bk",
        "codex-output",
        "codex_output",
    ]
    staged = _git_staged_paths()
    for staged_path in staged:
        if any(staged_path.startswith(prefix) for prefix in forbidden_staged_prefixes):
            errors.append(f"forbidden generated/raw/codex path staged: {staged_path}")
    return {
        "stage5bk_valid": not errors,
        "validation_error_count": len(errors),
        "validation_errors": errors,
        "iddqd_v2_source_root_found": bool(payloads.get("source_root", {}).get("source_root_found")),
        "iddqd_v2_selected_path": payloads.get("source_root", {}).get("selected_path"),
        "byte_string_count": byte.get("byte_string_count", 0),
        "source_gap_severity_record_count": payloads.get("gap_severity", {}).get("source_gap_severity_record_count", 0),
        "stage5bj_crosswalk_errata_count": payloads.get("crosswalk_errata", {}).get("stage5bj_crosswalk_errata_count", 0),
        "codex_output_used": False,
    }


def _collect_forbidden_flag_errors(payload: Any, context: str, errors: list[str]) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in FALSE_GUARDRAIL_KEYS and value not in (False, 0, None):
                errors.append(f"{context}: forbidden flag {key}={value!r}")
            _collect_forbidden_flag_errors(value, context, errors)
    elif isinstance(payload, list):
        for item in payload:
            _collect_forbidden_flag_errors(item, context, errors)


def summarize_stage5bk(summary: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read_yaml(summary)


def build_stage5bk_records() -> dict[str, Any]:
    located = locate_stage5bk_iddqd_v2()
    inventory = inventory_stage5bk_iddqd_v2()
    source_locks = build_stage5bk_iddqd_v2_source_lock()
    constraints = build_stage5bk_planning_constraints()
    token_block = build_stage5bk_token_block_impact()
    summary = build_stage5bk_summary()
    return {
        "source_root": located,
        **inventory,
        **source_locks,
        **constraints,
        **token_block,
        "summary": summary,
    }
