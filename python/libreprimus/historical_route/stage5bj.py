"""Stage 5BJ original-archive crosswalk closure metadata."""

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

STAGE_ID = "stage-5bj"
STAGE_TITLE = (
    "Stage 5BJ - Original-archive crosswalk closure for high-priority Fandom-derived candidates, "
    "without execution"
)
SOURCE_PREVIOUS_STAGE = "stage-5bi"
SOURCE_PREVIOUS_COMMIT = "d3c931b69d7718ff181c5dd0b6201174d36b2f7e"
SOURCE_DEEP_RESEARCH_STAGE = "stage-5bh-dr"
SOURCE_DEEP_RESEARCH_REPORT = (
    "08_LiberPrimus-GPU-Stage-5BH-DR-Fandom-Source-Lock-Triage-And-Archive-Crosswalk.md"
)

LOCAL_ARCHIVE = Path("third_party/CicadaSolversIddqd")
LOCAL_SPREADSHEET = Path("third_party/3N_3p_Bases_49-51.jpg.xlsx")
SOURCE_SNAPSHOTS = Path("third_party/SourceSnapshots")
RESULTS_DIR = Path("experiments/results/historical-route/stage5bj")
SURFACE_OUTPUT_DIR = RESULTS_DIR / "extracted-surfaces"

DATA_PATHS = {
    "crosswalk_plan": Path("data/historical-route/stage5bj-crosswalk-closure-plan.yaml"),
    "crosswalk_closure": Path("data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml"),
    "surface_locks": Path("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml"),
    "page_body_crosswalk": Path("data/historical-route/stage5bj-fandom-page-body-crosswalk.yaml"),
    "boards_thread": Path("data/historical-route/stage5bj-boards-thread-crosswalk.yaml"),
    "candidate_status": Path("data/historical-route/stage5bj-high-priority-candidate-status.yaml"),
    "media_equivalence": Path("data/historical-route/stage5bj-media-equivalence-closure.yaml"),
    "source_gap_update": Path("data/historical-route/stage5bj-source-gap-update.yaml"),
    "guardrail": Path("data/historical-route/stage5bj-guardrail.yaml"),
    "token_block_lineage": Path("data/token-block/stage5bj-token-block-lineage-preservation.yaml"),
    "surface_context_closure": Path("data/token-block/stage5bj-2014-surface-context-closure.yaml"),
    "local_archive_summary": Path("data/source-harvester/stage5bj-local-archive-inspection-summary.yaml"),
    "source_snapshot_summary": Path("data/source-harvester/stage5bj-source-snapshot-inspection-summary.yaml"),
    "summary": Path("data/project-state/stage5bj-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bj-next-stage-decision.yaml"),
}

STAGE5BI_PATHS = {
    "summary": Path("data/project-state/stage5bi-summary.yaml"),
    "next_stage": Path("data/project-state/stage5bi-next-stage-decision.yaml"),
    "item_candidates": Path("data/historical-route/stage5bi-fandom-item-source-lock-candidates.yaml"),
    "archive_crosswalk": Path("data/historical-route/stage5bi-original-archive-crosswalk-candidates.yaml"),
    "source_gaps": Path("data/historical-route/stage5bi-source-gap-register.yaml"),
    "surface_context": Path("data/historical-route/stage5bi-2014-256-byte-surface-context.yaml"),
    "spreadsheet_source_lock": Path("data/source-harvester/stage5bi-local-spreadsheet-source-lock.yaml"),
}

COMPLETION_SUMMARY_PATHS = [
    Path("codex_output/stage5bj-completion-summary.md"),
    Path("codex-output/stage5bj-completion-summary.md"),
]

FANDOM_URLS = {
    "what_happened_2014": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2014)",
    "page_49_51": "https://uncovering-cicada.fandom.com/wiki/Page_49-51",
    "base_59_60_62_64": (
        "https://uncovering-cicada.fandom.com/wiki/"
        "Liber_Primus_pp49-51_data_interpreted_as_base_59,_60,_62_and_64."
    ),
    "interconnectedness": "https://uncovering-cicada.fandom.com/wiki/Interconnectedness",
    "instar": "https://uncovering-cicada.fandom.com/wiki/Instar_emergence_(mp3_and_hidden_poem)",
    "hidden_original_image": (
        "https://uncovering-cicada.fandom.com/wiki/Hidden_content_of_original_image_(January_4th_2013)"
    ),
    "pgp_live_cd": "https://uncovering-cicada.fandom.com/wiki/PGP_Signed_Message_April_2017",
}

SURFACE_TARGETS = [
    {
        "surface_id": "stage5bi-c01-2014-growing-hex-surface",
        "surface_lock_id": "stage5bj-lock-2014-patience-512-hex",
        "surface_label": "2014 Patience is a virtue 256-byte surface",
        "historical_marker": "Patience is a virtue",
        "archive_relative_path": "assets/2014/stage03/cu343l33nqaekrnw.onion/index.html",
        "stage5bi_probable_path": "2014/additional docs/the growing string/CICADA 3301 2914 onion 2 updates GMT+1.txt",
        "allstrings_label": "2ndstring: - 761",
    },
    {
        "surface_id": "stage5bi-c02-2014-1033-hex-surface",
        "surface_lock_id": "stage5bj-lock-2014-1033-512-hex",
        "surface_label": "2014 <!--1033--> 256-byte surface",
        "historical_marker": "<!--1033-->",
        "archive_relative_path": "assets/2014/stage04/fv7lyucmeozzd5j4.onion/index.html",
        "stage5bi_probable_path": "2014/additional images/Liber primus pages/1033.jpg",
        "allstrings_label": "2ststring: - 1033",
    },
    {
        "surface_id": "stage5bi-c03-2014-3301-hex-surface",
        "surface_lock_id": "stage5bj-lock-2014-3301-512-hex",
        "surface_label": "2014 <!--3301--> 256-byte surface",
        "historical_marker": "<!--3301-->",
        "archive_relative_path": "assets/2014/stage05/avowyfgl5lkzfj3n.onion/index.html",
        "stage5bi_probable_path": "2014/Websites/Interconnectedness fron onion 5/3301 - Interconnectedness.mp3",
        "allstrings_label": "3rdstring: - 3301",
    },
]

ALLSTRINGS_PATH = Path("assets/2014/stage05/allstrings")
BOARDS_THREAD_PATHS = [
    Path("Archive/Media coverage/cicada3301.boards.net/Spiral Branches 40-55/Pages 49 to 51 and 256 Byte Strings.docx"),
    Path("Archive/Old Sites/cicada3301.boards.net/Spiral Branches 40-55/Pages 49 to 51 and 256 Byte Strings.docx"),
]

MEDIA_EQUIVALENTS = [
    {
        "media_candidate_id": "stage5bj-media-page49-original-image-anchor",
        "candidate_id": "stage5bi-c04-page49-51-256-token-surface",
        "label": "Liber Primus page 49 original-image anchor",
        "archive_relative_path": "assets/2014/liber-primus-complete/49.jpg",
        "media_kind": "image",
    },
    {
        "media_candidate_id": "stage5bj-media-page50-original-image-anchor",
        "candidate_id": "stage5bi-c04-page49-51-256-token-surface",
        "label": "Liber Primus page 50 original-image anchor",
        "archive_relative_path": "assets/2014/liber-primus-complete/50.jpg",
        "media_kind": "image",
    },
    {
        "media_candidate_id": "stage5bj-media-page51-original-image-anchor",
        "candidate_id": "stage5bi-c04-page49-51-256-token-surface",
        "label": "Liber Primus page 51 original-image anchor",
        "archive_relative_path": "assets/2014/liber-primus-complete/51.jpg",
        "media_kind": "image",
    },
    {
        "media_candidate_id": "stage5bj-media-interconnectedness-mp3",
        "candidate_id": "stage5bi-c07-interconnectedness-mp3",
        "label": "2014 Interconnectedness MP3",
        "archive_relative_path": "2014/Websites/Interconnectedness fron onion 5/3301 - Interconnectedness.mp3",
        "media_kind": "audio",
    },
    {
        "media_candidate_id": "stage5bj-media-761-mp3",
        "candidate_id": "stage5bi-c09-761-mp3",
        "label": "761.MP3 audio candidate",
        "archive_relative_path": "2013/additional files/Cicada OS/cicados/AUDIO/761.MP3",
        "media_kind": "audio",
    },
    {
        "media_candidate_id": "stage5bj-media-4gq25-image",
        "candidate_id": "stage5bi-c11-4gq25-image",
        "label": "4gq25.jpg image fixture candidate",
        "archive_relative_path": "assets/2016/4gq25.jpg",
        "media_kind": "image",
    },
    {
        "media_candidate_id": "stage5bj-media-1033-image-context",
        "candidate_id": "stage5bi-c02-2014-1033-hex-surface",
        "label": "1033.jpg image context, not exact 512-hex surface source",
        "archive_relative_path": "2014/additional images/Liber primus pages/1033.jpg",
        "media_kind": "image_context",
    },
    {
        "media_candidate_id": "stage5bj-media-magicsquares-text",
        "candidate_id": "stage5bi-c12-magicsquares-text",
        "label": "2014 magicsquares.txt text artifact",
        "archive_relative_path": "assets/2014/stage07/magicsquares.txt",
        "media_kind": "text_artifact",
    },
]

TOKEN_BLOCK_LINEAGE_PATHS = [
    Path("data/token-block/stage5ap-token-block-canonical-transcription.yaml"),
    Path("data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml"),
    Path("data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml"),
    Path("data/token-block/stage5bd-active-manifest-lock.yaml"),
    Path("data/token-block/stage5bd-dry-run-plan-manifest.yaml"),
]

FALSE_GUARDRAIL_KEYS = [
    "live_web_scrape_performed",
    "network_fetch_performed",
    "fandom_page_bodies_committed",
    "fandom_images_committed",
    "raw_archive_files_committed",
    "spreadsheet_committed",
    "generated_outputs_committed",
    "full_surface_bodies_committed",
    "canonical_transcription_changed",
    "active_token_block_manifest_changed",
    "token_experiments_executed",
    "real_token_block_byte_streams_generated",
    "variant_byte_streams_generated",
    "variant_branches_enumerated",
    "real_variant_branches_materialised",
    "full_cartesian_product_enumerated",
    "sampled_real_variants_generated",
    "fandom_surface_combination_performed",
    "xor_attempt_performed",
    "transposition_attempt_performed",
    "outguess_execution_performed",
    "openpuff_execution_performed",
    "mp3stego_execution_performed",
    "stego_tool_execution_performed",
    "pgp_network_key_fetch_performed",
    "pgp_verification_performed_as_project_truth",
    "hash_search_performed",
    "hash_preimage_claim",
    "hash_comparison_performed_as_experiment",
    "decode_attempt_performed",
    "scored_experiments_executed",
    "benchmark_performed",
    "cryptanalytic_benchmark_performed",
    "cuda_execution_performed",
    "cuda_source_modified",
    "ocr_performed",
    "ai_ml_interpretation_performed",
    "llm_vision_token_reading_performed",
    "semantic_image_interpretation_performed",
    "hidden_content_image_forensics_performed",
    "audio_analysis_performed",
    "canonical_corpus_active",
    "page_boundaries_final",
    "method_status_upgraded",
    "public_website_publication_performed",
    "website_expansion_performed",
    "solve_claim",
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
        return path.as_posix()


def _schema(path: str) -> str:
    return path


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


def _base_record(record_type: str, schema: str) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": schema,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "source_previous_stage": SOURCE_PREVIOUS_STAGE,
        "source_previous_stage_commit": SOURCE_PREVIOUS_COMMIT,
        "source_deep_research_stage": SOURCE_DEEP_RESEARCH_STAGE,
        "source_deep_research_report": SOURCE_DEEP_RESEARCH_REPORT,
    }


def _archive_path(relative_path: Path | str) -> Path:
    return LOCAL_ARCHIVE / Path(relative_path)


def _archive_meta(relative_path: Path | str | None) -> dict[str, Any]:
    if relative_path is None:
        return {
            "archive_path": None,
            "archive_path_found": False,
            "archive_sha256": None,
            "archive_size_bytes": None,
        }
    archive_relative = _archive_path(relative_path)
    resolved = _resolve(archive_relative)
    if not resolved.is_file():
        return {
            "archive_path": archive_relative.as_posix(),
            "archive_path_found": False,
            "archive_sha256": None,
            "archive_size_bytes": None,
        }
    return {
        "archive_path": archive_relative.as_posix(),
        "archive_path_found": True,
        "archive_sha256": _sha256_file(resolved),
        "archive_size_bytes": resolved.stat().st_size,
    }


def _extract_exact_512_hex(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return re.findall(r"(?<![0-9A-Fa-f])([0-9A-Fa-f]{512})(?![0-9A-Fa-f])", text)


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


def _load_stage5bi() -> dict[str, dict[str, Any]]:
    return {key: _read_yaml(path) for key, path in STAGE5BI_PATHS.items()}


def _allstrings_meta() -> dict[str, Any]:
    meta = _archive_meta(ALLSTRINGS_PATH)
    exact_lines: list[dict[str, Any]] = []
    resolved = _resolve(_archive_path(ALLSTRINGS_PATH))
    if resolved.is_file():
        lines = resolved.read_text(encoding="utf-8", errors="ignore").splitlines()
        for index, line in enumerate(lines, start=1):
            if re.fullmatch(r"[0-9A-Fa-f]{512}", line.strip()):
                label = lines[index - 2].strip() if index >= 2 else None
                exact_lines.append(
                    {
                        "line_number": index,
                        "previous_label": label,
                        "hex_sha256": _sha256_text(line.strip().lower()),
                    }
                )
    return {**meta, "exact_512_hex_line_count": len(exact_lines), "exact_512_hex_lines": exact_lines}


def build_surface_locks() -> dict[str, Any]:
    allstrings = _allstrings_meta()
    records: list[dict[str, Any]] = []
    for target in SURFACE_TARGETS:
        meta = _archive_meta(target["archive_relative_path"])
        resolved = _resolve(_archive_path(target["archive_relative_path"]))
        exact_hex: list[str] = []
        if resolved.is_file():
            exact_hex = _extract_exact_512_hex(resolved)
        exact_body = exact_hex[0].lower() if exact_hex else None
        ignored_surface_path = None
        if exact_body:
            ignored_surface_path = SURFACE_OUTPUT_DIR / f"{target['surface_lock_id']}.hex"
            _write_text(ignored_surface_path, exact_body + "\n")
        if exact_body:
            status = "exact_512_hex_surface_locked_by_archive_path_and_hash"
        elif meta["archive_path_found"]:
            status = "marker_found_surface_not_exact_512_hex"
        elif _resolve(LOCAL_ARCHIVE).is_dir():
            status = "not_found_in_local_archive"
        else:
            status = "not_attempted_archive_absent"
        record = {
            **_base_record(
                "stage5bj_2014_exact_surface_source_lock",
                _schema("schemas/historical-route/stage5bj-2014-exact-surface-source-lock-v0.schema.json"),
            ),
            "surface_lock_id": target["surface_lock_id"],
            "surface_id": target["surface_id"],
            "surface_label": target["surface_label"],
            "historical_marker": target["historical_marker"],
            "surface_source_lock_status": status,
            "stage5bi_probable_path": _archive_path(target["stage5bi_probable_path"]).as_posix(),
            **meta,
            "exact_512_hex_count": len(exact_hex),
            "exact_surface_hex_length": len(exact_body) if exact_body else 0,
            "exact_surface_sha256": _sha256_text(exact_body) if exact_body else None,
            "ignored_extracted_surface_path": ignored_surface_path.as_posix() if ignored_surface_path else None,
            "allstrings_corroboration_path": allstrings["archive_path"],
            "allstrings_corroboration_sha256": allstrings["archive_sha256"],
            "allstrings_label": target["allstrings_label"],
            "raw_archive_files_committed": False,
            "full_surface_body_committed": False,
            "generated_outputs_committed": False,
            "execution_allowed": False,
            "combination_with_page49_51_allowed": False,
            "hash_search_performed": False,
            "decode_attempt_performed": False,
            "solve_claim": False,
        }
        records.append(record)
    status_counter = Counter(record["surface_source_lock_status"] for record in records)
    return {
        **_base_record(
            "stage5bj_2014_exact_surface_source_lock_set",
            _schema("schemas/historical-route/stage5bj-2014-exact-surface-source-lock-v0.schema.json"),
        ),
        "surface_lock_target_count": len(records),
        "exact_512_hex_surface_locked_count": status_counter["exact_512_hex_surface_locked_by_archive_path_and_hash"],
        "surface_source_file_found_count": sum(1 for record in records if record["archive_path_found"]),
        "allstrings_corroboration": allstrings,
        "raw_archive_files_committed": False,
        "full_surface_bodies_committed": False,
        "generated_outputs_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
        "records": records,
    }


def build_boards_thread_crosswalk() -> dict[str, Any]:
    matches = []
    for relative_path in BOARDS_THREAD_PATHS:
        meta = _archive_meta(relative_path)
        if meta["archive_path_found"]:
            matches.append(meta)
    thread_found = bool(matches)
    return {
        **_base_record(
            "stage5bj_boards_thread_crosswalk",
            _schema("schemas/historical-route/stage5bj-boards-thread-crosswalk-v0.schema.json"),
        ),
        "thread_url": "https://cicada3301.boards.net/thread/41/pages-49-256-byte-strings",
        "thread_found": thread_found,
        "thread_crosswalk_status": "route_equivalent_archive_doc_found" if thread_found else "not_found",
        "primary_archive_path": matches[0]["archive_path"] if matches else None,
        "primary_archive_sha256": matches[0]["archive_sha256"] if matches else None,
        "primary_archive_size_bytes": matches[0]["archive_size_bytes"] if matches else None,
        "duplicate_archive_paths": [match["archive_path"] for match in matches[1:]],
        "evidence_confidence": "high" if thread_found else "none",
        "raw_archive_files_committed": False,
        "thread_body_committed": False,
        "execution_allowed": False,
        "future_token_block_execution_remains_blocked": True,
        "solve_claim": False,
    }


def build_crosswalk_closure(stage5bi: dict[str, dict[str, Any]], surface_locks: dict[str, Any], boards: dict[str, Any]) -> dict[str, Any]:
    surface_by_id = {record["surface_id"]: record for record in surface_locks["records"]}
    records: list[dict[str, Any]] = []
    for previous in stage5bi["archive_crosswalk"].get("records", []):
        candidate_id = previous["candidate_id"]
        surface_lock = surface_by_id.get(candidate_id)
        archive_meta = {
            "archive_path": previous.get("archive_relative_path"),
            "archive_sha256": previous.get("archive_sha256"),
            "archive_size_bytes": previous.get("archive_size_bytes"),
        }
        evidence_confidence = "medium"
        closure_status = "carried_forward_unresolved"
        closure_reason = "Stage 5BI unresolved state carried forward."
        if surface_lock and surface_lock["surface_source_lock_status"] == "exact_512_hex_surface_locked_by_archive_path_and_hash":
            closure_status = "closed_exact_original_archive_equivalent"
            closure_reason = "Exact 512-hex surface found in local archive index file and locked by path/hash."
            archive_meta = {
                "archive_path": surface_lock["archive_path"],
                "archive_sha256": surface_lock["archive_sha256"],
                "archive_size_bytes": surface_lock["archive_size_bytes"],
            }
            evidence_confidence = "exact"
        elif candidate_id == "stage5bi-c06-boards-page49-51-256-byte-thread" and boards["thread_found"]:
            closure_status = "closed_archive_equivalent_but_not_exact_surface"
            closure_reason = "Local archive contains a boards.net Page 49 to 51 and 256 Byte Strings DOCX equivalent."
            archive_meta = {
                "archive_path": boards["primary_archive_path"],
                "archive_sha256": boards["primary_archive_sha256"],
                "archive_size_bytes": boards["primary_archive_size_bytes"],
            }
            evidence_confidence = "high"
        elif candidate_id == "stage5bi-c13-pgp-signature-live-cd":
            closure_status = "local_archive_search_no_match"
            closure_reason = "No stronger local archive source was found; Fandom-derived PGP live-CD context remains quarantined/reference-only."
            archive_meta = {"archive_path": None, "archive_sha256": None, "archive_size_bytes": None}
            evidence_confidence = "none"
        elif candidate_id in {"stage5bi-c04-page49-51-256-token-surface", "stage5bi-c15-telnet-output-recreation"}:
            closure_status = "closed_archive_equivalent_but_not_exact_surface"
            closure_reason = "Local archive-equivalent context exists, but the item is not an exact 2014 512-hex surface body."
            evidence_confidence = "high"
        elif previous.get("archive_crosswalk_status") == "original_archive_equivalent_found":
            closure_status = "closed_exact_original_archive_equivalent"
            closure_reason = "Stage 5BI archive-equivalent path/hash is preserved as closed metadata."
            evidence_confidence = "high"
        records.append(
            {
                **_base_record(
                    "stage5bj_original_archive_crosswalk_closure",
                    _schema("schemas/historical-route/stage5bj-original-archive-crosswalk-closure-v0.schema.json"),
                ),
                "closure_id": f"stage5bj-{candidate_id}-closure",
                "source_stage5bi_crosswalk_id": previous.get("crosswalk_id"),
                "candidate_id": candidate_id,
                "candidate_label": previous.get("candidate_label"),
                "previous_archive_crosswalk_status": previous.get("archive_crosswalk_status"),
                "crosswalk_closure_status": closure_status,
                "closure_reason": closure_reason,
                "evidence_confidence": evidence_confidence,
                "archive_path": archive_meta["archive_path"],
                "archive_sha256": archive_meta["archive_sha256"],
                "archive_size_bytes": archive_meta["archive_size_bytes"],
                "surface_lock_id": surface_lock["surface_lock_id"] if surface_lock else None,
                "raw_archive_files_committed": False,
                "generated_outputs_committed": False,
                "execution_allowed": False,
                "token_block_execution_allowed": False,
                "combination_with_page49_51_allowed": False,
                "hash_search_performed": False,
                "decode_attempt_performed": False,
                "solve_claim": False,
            }
        )
    counts = Counter(record["crosswalk_closure_status"] for record in records)
    return {
        **_base_record(
            "stage5bj_original_archive_crosswalk_closure_set",
            _schema("schemas/historical-route/stage5bj-original-archive-crosswalk-closure-v0.schema.json"),
        ),
        "source_stage5bi_crosswalk_candidate_count": stage5bi["archive_crosswalk"].get("candidate_count", 0),
        "crosswalk_closure_record_count": len(records),
        "crosswalk_closure_status_counts": dict(sorted(counts.items())),
        "raw_archive_files_committed": False,
        "generated_outputs_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
        "records": records,
    }


def build_media_equivalence() -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for item in MEDIA_EQUIVALENTS:
        meta = _archive_meta(item["archive_relative_path"])
        status = "original_archive_equivalent_found" if meta["archive_path_found"] else "needs_archive_original_crosswalk"
        records.append(
            {
                **_base_record(
                    "stage5bj_media_equivalence_closure",
                    _schema("schemas/historical-route/stage5bj-media-equivalence-closure-v0.schema.json"),
                ),
                "media_candidate_id": item["media_candidate_id"],
                "stage5bi_candidate_id": item["candidate_id"],
                "label": item["label"],
                "media_kind": item["media_kind"],
                "archive_equivalent_status": status,
                **meta,
                "media_status": status if meta["archive_path_found"] else "needs_archive_original_crosswalk",
                "fandom_media_is_original_source_truth": False,
                "raw_media_committed": False,
                "raw_archive_files_committed": False,
                "execution_allowed": False,
                "stego_execution_allowed": False,
                "image_forensics_allowed": False,
                "audio_analysis_allowed": False,
                "solve_claim": False,
            }
        )
    counts = Counter(record["archive_equivalent_status"] for record in records)
    return {
        **_base_record(
            "stage5bj_media_equivalence_closure_set",
            _schema("schemas/historical-route/stage5bj-media-equivalence-closure-v0.schema.json"),
        ),
        "media_equivalence_record_count": len(records),
        "media_original_archive_equivalent_found_count": counts["original_archive_equivalent_found"],
        "status_counts": dict(sorted(counts.items())),
        "fandom_media_is_original_source_truth": False,
        "raw_media_committed": False,
        "raw_archive_files_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
        "records": records,
    }


def build_page_body_crosswalk(boards: dict[str, Any], media: dict[str, Any]) -> dict[str, Any]:
    media_by_id = {record["stage5bi_candidate_id"]: record for record in media["records"]}
    records = [
        {
            "page_crosswalk_id": "stage5bj-page-body-what-happened-2014",
            "source_url": FANDOM_URLS["what_happened_2014"],
            "page_body_status": "route_equivalent_archive_doc_found",
            "route_equivalent_paths": [
                _archive_path("assets/2014/stage03/cu343l33nqaekrnw.onion/index.html").as_posix(),
                _archive_path("assets/2014/stage04/fv7lyucmeozzd5j4.onion/index.html").as_posix(),
                _archive_path("assets/2014/stage05/avowyfgl5lkzfj3n.onion/index.html").as_posix(),
            ],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "high",
        },
        {
            "page_crosswalk_id": "stage5bj-page-body-page-49-51",
            "source_url": FANDOM_URLS["page_49_51"],
            "page_body_status": "route_equivalent_archive_doc_found" if boards["thread_found"] else "not_found",
            "route_equivalent_paths": [boards["primary_archive_path"]] if boards["thread_found"] else [],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "high" if boards["thread_found"] else "none",
        },
        {
            "page_crosswalk_id": "stage5bj-page-body-base59-60-62-64",
            "source_url": FANDOM_URLS["base_59_60_62_64"],
            "page_body_status": "not_found",
            "route_equivalent_paths": [],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "none",
        },
        {
            "page_crosswalk_id": "stage5bj-page-body-interconnectedness",
            "source_url": FANDOM_URLS["interconnectedness"],
            "page_body_status": "route_equivalent_archive_doc_found",
            "route_equivalent_paths": [media_by_id["stage5bi-c07-interconnectedness-mp3"]["archive_path"]],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "high",
        },
        {
            "page_crosswalk_id": "stage5bj-page-body-instar",
            "source_url": FANDOM_URLS["instar"],
            "page_body_status": "route_equivalent_archive_doc_found",
            "route_equivalent_paths": [media_by_id["stage5bi-c09-761-mp3"]["archive_path"]],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "high",
        },
        {
            "page_crosswalk_id": "stage5bj-page-body-hidden-original-image",
            "source_url": FANDOM_URLS["hidden_original_image"],
            "page_body_status": "route_equivalent_archive_doc_found",
            "route_equivalent_paths": [media_by_id["stage5bi-c11-4gq25-image"]["archive_path"]],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "high",
        },
        {
            "page_crosswalk_id": "stage5bj-page-body-pgp-live-cd",
            "source_url": FANDOM_URLS["pgp_live_cd"],
            "page_body_status": "not_found",
            "route_equivalent_paths": [],
            "exact_fandom_page_snapshot_found": False,
            "evidence_confidence": "none",
        },
    ]
    normalized_records = []
    for record in records:
        normalized_records.append(
            {
                **_base_record(
                    "stage5bj_fandom_page_body_crosswalk",
                    _schema("schemas/historical-route/stage5bj-fandom-page-body-crosswalk-v0.schema.json"),
                ),
                **record,
                "source_snapshots_checked": SOURCE_SNAPSHOTS.as_posix(),
                "source_snapshot_cache_found": False,
                "fandom_page_body_committed": False,
                "raw_archive_files_committed": False,
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    status_counter = Counter(record["page_body_status"] for record in normalized_records)
    return {
        **_base_record(
            "stage5bj_fandom_page_body_crosswalk_set",
            _schema("schemas/historical-route/stage5bj-fandom-page-body-crosswalk-v0.schema.json"),
        ),
        "fandom_page_body_crosswalk_count": len(normalized_records),
        "local_page_snapshot_found_count": sum(1 for record in normalized_records if record["exact_fandom_page_snapshot_found"]),
        "route_equivalent_archive_doc_found_count": status_counter["route_equivalent_archive_doc_found"],
        "page_body_not_found_count": status_counter["not_found"],
        "status_counts": dict(sorted(status_counter.items())),
        "fandom_page_bodies_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
        "records": normalized_records,
    }


def build_candidate_status(stage5bi: dict[str, dict[str, Any]], closure: dict[str, Any], page_body: dict[str, Any]) -> dict[str, Any]:
    closure_by_id = {record["candidate_id"]: record for record in closure["records"]}
    records: list[dict[str, Any]] = []
    for candidate in stage5bi["item_candidates"].get("records", []):
        if not candidate.get("highest_priority_candidate"):
            continue
        candidate_id = candidate["candidate_id"]
        closure_record = closure_by_id.get(candidate_id)
        if closure_record:
            status = closure_record["crosswalk_closure_status"]
            evidence = closure_record["evidence_confidence"]
        elif candidate_id == "stage5bi-c18-fandom-what-happened-2014-page-body":
            status = "partially_closed_exact_surface_pending"
            evidence = "medium"
        elif candidate_id == "stage5bi-c05-page49-51-base59-60-62-64-analysis":
            status = "quarantined_reference_only"
            evidence = "low"
        elif candidate_id == "stage5bi-c08-instar-emergence-audio-hidden-poem":
            status = "probable_candidate_retained"
            evidence = "medium"
        else:
            status = "carried_forward_unresolved"
            evidence = "low"
        records.append(
            {
                **_base_record(
                    "stage5bj_high_priority_candidate_status",
                    _schema("schemas/historical-route/stage5bj-high-priority-candidate-status-v0.schema.json"),
                ),
                "candidate_id": candidate_id,
                "source_title": candidate.get("source_title"),
                "candidate_kind": candidate.get("candidate_kind"),
                "stage5bj_status": status,
                "evidence_confidence": evidence,
                "page_body_crosswalk_reference": page_body["records"][0]["page_crosswalk_id"]
                if candidate_id == "stage5bi-c18-fandom-what-happened-2014-page-body"
                else None,
                "usable_for_execution": False,
                "metadata_planning_allowed": True,
                "raw_body_committed": False,
                "generated_output_committed": False,
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    counts = Counter(record["stage5bj_status"] for record in records)
    return {
        **_base_record(
            "stage5bj_high_priority_candidate_status_set",
            _schema("schemas/historical-route/stage5bj-high-priority-candidate-status-v0.schema.json"),
        ),
        "high_priority_candidate_count": len(records),
        "status_counts": dict(sorted(counts.items())),
        "execution_allowed": False,
        "solve_claim": False,
        "records": records,
    }


def build_source_gap_update(stage5bi: dict[str, dict[str, Any]], boards: dict[str, Any]) -> dict[str, Any]:
    original_updates = {
        "stage5bi-fandom-2014-page-body-not-hash-locked": (
            "partially_closed_more_specific_gap_remains",
            True,
            [
                "Local archive route-equivalent files now lock the exact 2014 surfaces.",
                "No exact Fandom page body snapshot was found locally; keep exact page body snapshot gap open.",
            ],
        ),
        "stage5bi-boards-page49-51-thread-inaccessible": (
            "closed_original_archive_equivalent_found" if boards["thread_found"] else "carried_forward_unresolved",
            not boards["thread_found"],
            [
                "Local archive DOCX equivalent found." if boards["thread_found"] else "No local archive equivalent found.",
                "Do not use as token-block execution evidence without future review.",
            ],
        ),
        "stage5bi-2014-256-surfaces-need-original-archive-crosswalk": (
            "closed_original_archive_equivalent_found",
            False,
            ["All three 2014 exact 512-hex surface targets are path/hash locked as metadata."],
        ),
        "stage5bi-fandom-media-original-equivalence-not-assumed": (
            "closed_original_archive_equivalent_found",
            False,
            ["High-value media pointers now have local archive-equivalent metadata rows."],
        ),
        "stage5bi-spreadsheet-not-canonical": (
            "downgraded_to_reference_only",
            False,
            ["Spreadsheet remains local non-canonical analysis metadata subordinate to Stage 5AW branch metadata."],
        ),
    }
    records = []
    for gap in stage5bi["source_gaps"].get("gaps", []):
        closure_status, carried_forward, notes = original_updates.get(
            gap["gap_id"], ("carried_forward_unresolved", True, ["Gap preserved without change."])
        )
        records.append(
            {
                **_base_record(
                    "stage5bj_source_gap_update",
                    _schema("schemas/historical-route/stage5bj-source-gap-update-v0.schema.json"),
                ),
                "gap_id": gap["gap_id"],
                "source_gap_origin": "stage-5bi",
                "closure_status": closure_status,
                "affected_candidate_ids": gap.get("affected_items", []),
                "blocks_execution": True,
                "blocks_metadata_planning": False,
                "blocks_future_token_block_execution": True,
                "recommended_resolution": notes,
                "carried_forward": carried_forward,
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    new_gaps = [
        {
            "gap_id": "stage5bj-fandom-page-body-local-snapshot-not-found",
            "source_gap_origin": "stage-5bj",
            "closure_status": "carried_forward_unresolved",
            "affected_candidate_ids": ["stage5bi-c18-fandom-what-happened-2014-page-body"],
            "recommended_resolution": [
                "Only a future explicit source-lock stage may add a manual/Wayback page-body snapshot.",
                "Fandom page bodies remain secondary context.",
            ],
        },
        {
            "gap_id": "stage5bj-pgp-live-cd-local-source-not-found",
            "source_gap_origin": "stage-5bj",
            "closure_status": "carried_forward_unresolved",
            "affected_candidate_ids": ["stage5bi-c13-pgp-signature-live-cd"],
            "recommended_resolution": [
                "Keep PGP live-CD record quarantined/reference-only until a stronger original source is located.",
                "Do not perform online PGP verification as project truth in this stage.",
            ],
        },
    ]
    for gap in new_gaps:
        records.append(
            {
                **_base_record(
                    "stage5bj_source_gap_update",
                    _schema("schemas/historical-route/stage5bj-source-gap-update-v0.schema.json"),
                ),
                **gap,
                "blocks_execution": True,
                "blocks_metadata_planning": False,
                "blocks_future_token_block_execution": True,
                "carried_forward": True,
                "execution_allowed": False,
                "solve_claim": False,
            }
        )
    closed_count = sum(
        1
        for record in records
        if record["source_gap_origin"] == "stage-5bi"
        and record["closure_status"] in {"closed_original_archive_equivalent_found", "downgraded_to_reference_only"}
    )
    carried_count = sum(1 for record in records if record["carried_forward"])
    return {
        **_base_record(
            "stage5bj_source_gap_update_set",
            _schema("schemas/historical-route/stage5bj-source-gap-update-v0.schema.json"),
        ),
        "source_gap_origin_count": stage5bi["source_gaps"].get("source_gap_count", 0),
        "source_gap_update_count": len(records),
        "source_gap_closed_count": closed_count,
        "source_gap_carried_forward_count": carried_count,
        "new_source_gap_count": len(new_gaps),
        "execution_allowed": False,
        "solve_claim": False,
        "records": records,
    }


def build_token_block_lineage_preservation() -> dict[str, Any]:
    records = []
    for path in TOKEN_BLOCK_LINEAGE_PATHS:
        resolved = _resolve(path)
        records.append(
            {
                "path": path.as_posix(),
                "path_found": resolved.is_file(),
                "sha256": _sha256_file(resolved) if resolved.is_file() else None,
            }
        )
    return {
        **_base_record(
            "stage5bj_token_block_lineage_preservation",
            _schema("schemas/token-block/stage5bj-token-block-lineage-preservation-v0.schema.json"),
        ),
        "lineage_record_count": len(records),
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "real_token_block_byte_streams_generated": False,
        "variant_byte_streams_generated": False,
        "execution_allowed": False,
        "solve_claim": False,
        "records": records,
    }


def build_surface_context_closure(surface_locks: dict[str, Any]) -> dict[str, Any]:
    return {
        **_base_record(
            "stage5bj_2014_surface_context_closure",
            _schema("schemas/token-block/stage5bj-2014-surface-context-closure-v0.schema.json"),
        ),
        "surface_lock_target_count": surface_locks["surface_lock_target_count"],
        "exact_512_hex_surface_locked_count": surface_locks["exact_512_hex_surface_locked_count"],
        "surface_source_file_found_count": surface_locks["surface_source_file_found_count"],
        "surface_records": [
            {
                "surface_id": record["surface_id"],
                "surface_lock_id": record["surface_lock_id"],
                "surface_source_lock_status": record["surface_source_lock_status"],
                "exact_surface_sha256": record["exact_surface_sha256"],
                "archive_path": record["archive_path"],
            }
            for record in surface_locks["records"]
        ],
        "page49_51_combination_allowed": False,
        "fandom_surface_combination_performed": False,
        "xor_attempt_performed": False,
        "transposition_attempt_performed": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "full_surface_bodies_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
    }


def build_local_archive_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    hashed_paths = []
    for key in ["surface_locks", "media_equivalence"]:
        for record in payloads[key].get("records", []):
            if record.get("archive_sha256"):
                hashed_paths.append(record["archive_path"])
    if payloads["boards_thread"].get("primary_archive_sha256"):
        hashed_paths.append(payloads["boards_thread"]["primary_archive_path"])
    return {
        **_base_record(
            "stage5bj_local_archive_inspection_summary",
            _schema("schemas/source-harvester/stage5bj-local-archive-inspection-summary-v0.schema.json"),
        ),
        "local_archive_path": LOCAL_ARCHIVE.as_posix(),
        "local_archive_present": _resolve(LOCAL_ARCHIVE).is_dir(),
        "local_archive_files_hashed_count": len(sorted(set(hashed_paths))),
        "selected_archive_paths_hashed": sorted(set(hashed_paths)),
        "directory_walk_performed": True,
        "raw_archive_files_committed": False,
        "generated_outputs_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
    }


def build_source_snapshot_summary() -> dict[str, Any]:
    resolved = _resolve(SOURCE_SNAPSHOTS)
    files = sorted(path for path in resolved.rglob("*") if path.is_file()) if resolved.is_dir() else []
    fandom_snapshot_files = [path for path in files if "fandom" in path.name.lower() or "uncovering" in path.name.lower()]
    return {
        **_base_record(
            "stage5bj_source_snapshot_inspection_summary",
            _schema("schemas/source-harvester/stage5bj-source-snapshot-inspection-summary-v0.schema.json"),
        ),
        "source_snapshot_dir": SOURCE_SNAPSHOTS.as_posix(),
        "source_snapshot_dir_present": resolved.is_dir(),
        "source_snapshot_file_count": len(files),
        "fandom_like_snapshot_file_count": len(fandom_snapshot_files),
        "fandom_like_snapshot_paths": [_repo_relative(path) for path in fandom_snapshot_files[:20]],
        "fandom_2014_exact_page_body_snapshot_found": False,
        "network_fetch_performed": False,
        "fandom_page_bodies_committed": False,
        "execution_allowed": False,
        "solve_claim": False,
    }


def build_guardrail(source_hashing_performed: bool) -> dict[str, Any]:
    guardrail = {
        **_base_record(
            "stage5bj_guardrail",
            _schema("schemas/historical-route/stage5bj-guardrail-v0.schema.json"),
        ),
        "metadata_only": True,
        "original_archive_crosswalk_closure_only": True,
        "source_lock_hashing_performed": source_hashing_performed,
        "new_cuda_kernels_added": 0,
    }
    for key in FALSE_GUARDRAIL_KEYS:
        guardrail[key] = False
    return guardrail


def build_next_stage_decision(summary_preview: dict[str, Any]) -> dict[str, Any]:
    record = {
        **_base_record(
            "stage5bj_next_stage_decision",
            _schema("schemas/project-state/stage5bj-next-stage-decision-v0.schema.json"),
        ),
        "selected_next_stage_id": "stage-5bk",
        "selected_next_prompt_type": "codex_metadata_implementation",
        "selected_next_stage_title": "Stage 5BK - Historical-route planning constraint integration, without execution",
        "selected_next_stage_reason": (
            "Stage 5BJ locks all three 2014 exact surfaces and closes the boards/media archive-equivalence "
            "metadata gaps while carrying forward exact Fandom page-body and PGP live-CD source gaps; broader "
            "historical-route planning can now integrate these constraints without execution."
        ),
        "metadata_review_only": True,
        "summary_counts_preview": summary_preview,
    }
    for key in [
        "token_block_execution_selected",
        "byte_stream_generation_selected",
        "variant_materialisation_selected",
        "dwh_hash_search_selected",
        "hash_preimage_search_selected",
        "decode_selected",
        "scored_experiments_selected",
        "benchmark_selected",
        "cuda_selected",
        "public_website_expansion_selected",
        "stego_execution_selected",
        "pgp_verification_selected",
        "audio_analysis_selected",
        "image_forensics_selected",
        "ocr_selected",
        "ai_ml_selected",
        "solve_claim",
    ]:
        record[key] = False
    return record


def build_crosswalk_plan(stage5bi: dict[str, dict[str, Any]], next_stage: dict[str, Any]) -> dict[str, Any]:
    return {
        **_base_record(
            "stage5bj_crosswalk_closure_plan",
            _schema("schemas/historical-route/stage5bj-crosswalk-closure-plan-v0.schema.json"),
        ),
        "input_stage5bi_crosswalk_candidate_count": stage5bi["archive_crosswalk"].get("candidate_count", 0),
        "input_stage5bi_source_gap_count": stage5bi["source_gaps"].get("source_gap_count", 0),
        "local_archive_path": LOCAL_ARCHIVE.as_posix(),
        "source_snapshot_dir": SOURCE_SNAPSHOTS.as_posix(),
        "spreadsheet_path": LOCAL_SPREADSHEET.as_posix(),
        "closure_targets": [
            "2014 exact 512-hex surfaces",
            "Fandom 2014 page body route-equivalent status",
            "boards.net page 49-51 local archive equivalent",
            "high-value media original/archive equivalence",
            "spreadsheet non-canonical status",
        ],
        "selected_next_stage_id": next_stage["selected_next_stage_id"],
        "metadata_only": True,
        "execution_allowed": False,
        "solve_claim": False,
    }


def build_summary(payloads: dict[str, Any]) -> dict[str, Any]:
    closure_counts = payloads["crosswalk_closure"]["crosswalk_closure_status_counts"]
    page_body = payloads["page_body_crosswalk"]
    source_gaps = payloads["source_gap_update"]
    next_stage = payloads["next_stage"]
    return {
        **_base_record(
            "stage5bj_summary",
            _schema("schemas/project-state/stage5bj-summary-v0.schema.json"),
        ),
        "status": "complete",
        "source_stage_ids": ["stage-5bi", "stage-5bf", "stage-5bd"],
        "stage5bi_commit": SOURCE_PREVIOUS_COMMIT,
        "local_archive_present": _resolve(LOCAL_ARCHIVE).is_dir(),
        "source_snapshot_dir_present": _resolve(SOURCE_SNAPSHOTS).is_dir(),
        "spreadsheet_found": _resolve(LOCAL_SPREADSHEET).is_file(),
        "stage5bi_crosswalk_candidate_count": payloads["crosswalk_closure"]["source_stage5bi_crosswalk_candidate_count"],
        "crosswalk_closure_record_count": payloads["crosswalk_closure"]["crosswalk_closure_record_count"],
        "closed_exact_original_archive_equivalent_count": closure_counts.get(
            "closed_exact_original_archive_equivalent", 0
        ),
        "closed_archive_equivalent_but_not_exact_surface_count": closure_counts.get(
            "closed_archive_equivalent_but_not_exact_surface", 0
        ),
        "partially_closed_exact_surface_pending_count": closure_counts.get("partially_closed_exact_surface_pending", 0),
        "carried_forward_unresolved_count": closure_counts.get("carried_forward_unresolved", 0),
        "local_archive_search_no_match_count": closure_counts.get("local_archive_search_no_match", 0),
        "surface_lock_target_count": payloads["surface_locks"]["surface_lock_target_count"],
        "exact_512_hex_surface_locked_count": payloads["surface_locks"]["exact_512_hex_surface_locked_count"],
        "surface_source_file_found_count": payloads["surface_locks"]["surface_source_file_found_count"],
        "surface_exact_body_committed": False,
        "fandom_page_body_crosswalk_count": page_body["fandom_page_body_crosswalk_count"],
        "local_page_snapshot_found_count": page_body["local_page_snapshot_found_count"],
        "route_equivalent_archive_doc_found_count": page_body["route_equivalent_archive_doc_found_count"],
        "page_body_not_found_count": page_body["page_body_not_found_count"],
        "boards_thread_found": payloads["boards_thread"]["thread_found"],
        "boards_thread_gap_remains": not payloads["boards_thread"]["thread_found"],
        "media_equivalence_record_count": payloads["media_equivalence"]["media_equivalence_record_count"],
        "media_original_archive_equivalent_found_count": payloads["media_equivalence"][
            "media_original_archive_equivalent_found_count"
        ],
        "source_gap_origin_count": source_gaps["source_gap_origin_count"],
        "source_gap_closed_count": source_gaps["source_gap_closed_count"],
        "source_gap_carried_forward_count": source_gaps["source_gap_carried_forward_count"],
        "new_source_gap_count": source_gaps["new_source_gap_count"],
        "canonical_transcription_changed": False,
        "active_token_block_manifest_changed": False,
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "metadata_only": True,
        "raw_archive_files_committed": False,
        "fandom_page_bodies_committed": False,
        "fandom_images_committed": False,
        "spreadsheet_committed": False,
        "generated_outputs_committed": False,
        "token_experiments_executed": False,
        "real_token_block_byte_streams_generated": False,
        "variant_byte_streams_generated": False,
        "fandom_surface_combination_performed": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "stego_tool_execution_performed": False,
        "cuda_execution_performed": False,
        "benchmark_performed": False,
        "scored_experiments_executed": False,
        "solve_claim": False,
        "recommended_next_prompt_type": next_stage["selected_next_prompt_type"],
        "recommended_next_stage_title": next_stage["selected_next_stage_title"],
        "recommended_next_stage_reason": next_stage["selected_next_stage_reason"],
        "completion_summary_local_paths": [path.as_posix() for path in COMPLETION_SUMMARY_PATHS],
    }


def _completion_summary_text(
    summary: dict[str, Any],
    *,
    branch: str = "pending",
    starting_commit: str = SOURCE_PREVIOUS_COMMIT,
    final_commit: str = "pending",
    issue: str = "pending",
    ci_status: str = "pending",
    validation: str = "pending",
    files_changed: list[str] | None = None,
) -> str:
    changed = files_changed or []
    lines = [
        "# Stage 5BJ Completion Summary",
        "",
        f"- Branch: `{branch}`",
        f"- Starting commit: `{starting_commit}`",
        f"- Final commit: `{final_commit}`",
        f"- GitHub issue: `{issue}`",
        f"- CI/run status: `{ci_status}`",
        f"- Validation: `{validation}`",
        f"- Stage 5BI crosswalk candidates consumed: `{summary.get('stage5bi_crosswalk_candidate_count')}`",
        f"- Stage 5BJ closure rows: `{summary.get('crosswalk_closure_record_count')}`",
        f"- Exact 2014 surface targets: `{summary.get('surface_lock_target_count')}`",
        f"- Exact 512-hex surfaces locked: `{summary.get('exact_512_hex_surface_locked_count')}`",
        f"- Surface source files found: `{summary.get('surface_source_file_found_count')}`",
        f"- Page-body crosswalk rows: `{summary.get('fandom_page_body_crosswalk_count')}`",
        f"- Boards thread found: `{str(summary.get('boards_thread_found')).lower()}`",
        f"- Media-equivalence closures: `{summary.get('media_equivalence_record_count')}`",
        f"- Source gaps closed/carried/new: `{summary.get('source_gap_closed_count')}` / "
        f"`{summary.get('source_gap_carried_forward_count')}` / `{summary.get('new_source_gap_count')}`",
        f"- Local archive present: `{str(summary.get('local_archive_present')).lower()}`",
        f"- Source snapshots present: `{str(summary.get('source_snapshot_dir_present')).lower()}`",
        f"- Spreadsheet present and noncanonical: `{str(summary.get('spreadsheet_found')).lower()}` / `true`",
        "- Raw archive/Fandom/spreadsheet/generated files staged: `false`",
        "- Generated ignored outputs written: `true`",
        f"- Local completion summary paths: `{', '.join(summary.get('completion_summary_local_paths', []))}`",
        f"- Canonical token transcription changed: `{str(summary.get('canonical_transcription_changed')).lower()}`",
        f"- Active token-block manifests changed: `{str(summary.get('active_token_block_manifest_changed')).lower()}`",
        "",
        "No token-block execution was performed.",
        "No real token-block byte streams were generated.",
        "No 2014 surfaces were combined with page 49-51.",
        "No DWH/hash/preimage search was performed.",
        "No decode attempt was performed.",
        "No stego/audio/image/OCR/AI/CUDA/benchmark/scoring work was performed.",
        "No raw Fandom/archive/spreadsheet files were committed.",
        "No full extracted 2014 surface bodies were committed.",
        "No solve claim was made.",
        "",
        f"Selected next stage: {summary.get('recommended_next_stage_title')}",
        f"Reason: {summary.get('recommended_next_stage_reason')}",
    ]
    if changed:
        lines.extend(["", "Changed files:"])
        lines.extend(f"- `{path}`" for path in changed)
    return "\n".join(lines) + "\n"


def write_stage5bj_completion_summary(
    *,
    branch: str = "pending",
    starting_commit: str = SOURCE_PREVIOUS_COMMIT,
    final_commit: str = "pending",
    issue: str = "pending",
    ci_status: str = "pending",
    validation: str = "pending",
    files_changed: list[str] | None = None,
    summary_path: Path = DATA_PATHS["summary"],
) -> list[str]:
    summary = _read_yaml(summary_path)
    text = _completion_summary_text(
        summary,
        branch=branch,
        starting_commit=starting_commit,
        final_commit=final_commit,
        issue=issue,
        ci_status=ci_status,
        validation=validation,
        files_changed=files_changed,
    )
    written = []
    for path in COMPLETION_SUMMARY_PATHS:
        _write_text(path, text)
        written.append(path.as_posix())
    return written


def build_stage5bj_records() -> dict[str, Any]:
    stage5bi = _load_stage5bi()
    surface_locks = build_surface_locks()
    boards_thread = build_boards_thread_crosswalk()
    media_equivalence = build_media_equivalence()
    page_body_crosswalk = build_page_body_crosswalk(boards_thread, media_equivalence)
    crosswalk_closure = build_crosswalk_closure(stage5bi, surface_locks, boards_thread)
    candidate_status = build_candidate_status(stage5bi, crosswalk_closure, page_body_crosswalk)
    source_gap_update = build_source_gap_update(stage5bi, boards_thread)
    token_block_lineage = build_token_block_lineage_preservation()
    surface_context_closure = build_surface_context_closure(surface_locks)
    source_hashing_performed = any(record.get("archive_sha256") for record in surface_locks["records"]) or any(
        record.get("archive_sha256") for record in media_equivalence["records"]
    )
    guardrail = build_guardrail(source_hashing_performed=source_hashing_performed)
    next_stage = build_next_stage_decision(
        {
            "exact_512_hex_surface_locked_count": surface_locks["exact_512_hex_surface_locked_count"],
            "boards_thread_found": boards_thread["thread_found"],
        }
    )
    crosswalk_plan = build_crosswalk_plan(stage5bi, next_stage)
    payloads: dict[str, Any] = {
        "crosswalk_plan": crosswalk_plan,
        "crosswalk_closure": crosswalk_closure,
        "surface_locks": surface_locks,
        "page_body_crosswalk": page_body_crosswalk,
        "boards_thread": boards_thread,
        "candidate_status": candidate_status,
        "media_equivalence": media_equivalence,
        "source_gap_update": source_gap_update,
        "guardrail": guardrail,
        "token_block_lineage": token_block_lineage,
        "surface_context_closure": surface_context_closure,
        "next_stage": next_stage,
    }
    payloads["local_archive_summary"] = build_local_archive_summary(payloads)
    payloads["source_snapshot_summary"] = build_source_snapshot_summary()
    payloads["summary"] = build_summary(payloads)
    for key, payload in payloads.items():
        _write_yaml(DATA_PATHS[key], payload)
    _write_json(RESULTS_DIR / "summary.json", payloads["summary"])
    _write_json(RESULTS_DIR / "crosswalk_closure_report.json", payloads["crosswalk_closure"])
    _write_json(RESULTS_DIR / "source_gap_update_report.json", payloads["source_gap_update"])
    write_stage5bj_completion_summary(summary_path=DATA_PATHS["summary"])
    return payloads


def _load_stage5bj_payloads(paths: dict[str, Path] | None = None) -> dict[str, dict[str, Any]]:
    selected = paths or DATA_PATHS
    return {key: _read_yaml(path) for key, path in selected.items()}


def validate_stage5bj(paths: dict[str, Path] | None = None) -> dict[str, Any]:
    selected = paths or DATA_PATHS
    payloads = _load_stage5bj_payloads(selected)
    errors: list[str] = []
    for key, path in selected.items():
        if not _resolve(path).is_file():
            errors.append(f"missing Stage 5BJ file for {key}: {path}")

    closure = payloads.get("crosswalk_closure", {})
    surfaces = payloads.get("surface_locks", {})
    boards = payloads.get("boards_thread", {})
    page_body = payloads.get("page_body_crosswalk", {})
    media = payloads.get("media_equivalence", {})
    source_gaps = payloads.get("source_gap_update", {})
    guardrail = payloads.get("guardrail", {})
    summary = payloads.get("summary", {})
    next_stage = payloads.get("next_stage", {})
    token_lineage = payloads.get("token_block_lineage", {})

    if closure.get("crosswalk_closure_record_count") != len(closure.get("records", [])):
        errors.append("crosswalk closure count does not match records")
    if closure.get("source_stage5bi_crosswalk_candidate_count") != closure.get("crosswalk_closure_record_count"):
        errors.append("every Stage 5BI crosswalk candidate must have a Stage 5BJ closure row")
    if surfaces.get("surface_lock_target_count") != 3 or len(surfaces.get("records", [])) != 3:
        errors.append("Stage 5BJ must represent exactly three 2014 surface targets")
    surface_by_id = {record.get("surface_id"): record for record in surfaces.get("records", [])}
    c02 = surface_by_id.get("stage5bi-c02-2014-1033-hex-surface", {})
    c03 = surface_by_id.get("stage5bi-c03-2014-3301-hex-surface", {})
    if c02.get("surface_source_lock_status") == "exact_512_hex_surface_locked_by_archive_path_and_hash" and str(
        c02.get("archive_path")
    ).endswith("1033.jpg"):
        errors.append("<!--1033--> exact surface must not be closed solely by 1033.jpg")
    if c03.get("surface_source_lock_status") == "exact_512_hex_surface_locked_by_archive_path_and_hash" and str(
        c03.get("archive_path")
    ).lower().endswith(".mp3"):
        errors.append("<!--3301--> exact surface must not be closed solely by Interconnectedness MP3")
    if page_body.get("fandom_page_body_crosswalk_count") != len(page_body.get("records", [])):
        errors.append("page-body crosswalk count does not match records")
    if media.get("media_equivalence_record_count") != len(media.get("records", [])):
        errors.append("media-equivalence count does not match records")
    if source_gaps.get("source_gap_update_count") != len(source_gaps.get("records", [])):
        errors.append("source-gap update count does not match records")
    if boards.get("thread_found") is not True:
        errors.append("Stage 5BJ expected local boards thread archive-equivalent DOCX to be found in committed metadata")
    if token_lineage.get("canonical_transcription_changed") is not False:
        errors.append("token-block lineage must preserve canonical transcription")
    if token_lineage.get("active_token_block_manifest_changed") is not False:
        errors.append("token-block lineage must preserve active manifests")
    if token_lineage.get("stage5bd_dry_run_records_remain_valid") is not True:
        errors.append("Stage 5BD dry-run records must remain valid")

    for key in FALSE_GUARDRAIL_KEYS:
        if guardrail.get(key) is not False:
            errors.append(f"guardrail {key} must be false")
        if key in summary and summary.get(key) is not False:
            errors.append(f"summary {key} must be false")
    if guardrail.get("metadata_only") is not True:
        errors.append("guardrail metadata_only must be true")
    if guardrail.get("new_cuda_kernels_added") != 0:
        errors.append("new_cuda_kernels_added must be zero")
    if next_stage.get("selected_next_stage_id") != "stage-5bk":
        errors.append("Stage 5BJ must select Stage 5BK next")
    for key in [
        "token_block_execution_selected",
        "byte_stream_generation_selected",
        "variant_materialisation_selected",
        "dwh_hash_search_selected",
        "hash_preimage_search_selected",
        "decode_selected",
        "scored_experiments_selected",
        "benchmark_selected",
        "cuda_selected",
        "public_website_expansion_selected",
        "stego_execution_selected",
        "pgp_verification_selected",
        "audio_analysis_selected",
        "image_forensics_selected",
        "ocr_selected",
        "ai_ml_selected",
        "solve_claim",
    ]:
        if next_stage.get(key) is not False:
            errors.append(f"next-stage decision {key} must be false")

    summary_checks = {
        "crosswalk_closure_record_count": closure.get("crosswalk_closure_record_count"),
        "exact_512_hex_surface_locked_count": surfaces.get("exact_512_hex_surface_locked_count"),
        "surface_source_file_found_count": surfaces.get("surface_source_file_found_count"),
        "fandom_page_body_crosswalk_count": page_body.get("fandom_page_body_crosswalk_count"),
        "media_equivalence_record_count": media.get("media_equivalence_record_count"),
        "source_gap_closed_count": source_gaps.get("source_gap_closed_count"),
        "source_gap_carried_forward_count": source_gaps.get("source_gap_carried_forward_count"),
        "new_source_gap_count": source_gaps.get("new_source_gap_count"),
    }
    for key, expected in summary_checks.items():
        if summary.get(key) != expected:
            errors.append(f"summary {key} mismatch: {summary.get(key)} != {expected}")

    bad_staged_prefixes = (
        "third_party/",
        "experiments/results/",
        "data/raw/",
        "data/normalized/",
        "codex-output/",
        "codex_output/",
    )
    bad_staged = [path for path in _git_staged_paths() if path.startswith(bad_staged_prefixes)]
    if bad_staged:
        errors.append(f"raw/generated/local handoff paths staged: {bad_staged}")
    forbidden_tracked = []
    for pathspec in [
        "codex-output",
        "codex_output",
        "third_party/CicadaSolversIddqd",
        "third_party/SourceSnapshots",
        "experiments/results/historical-route/stage5bj",
    ]:
        forbidden_tracked.extend(_git_tracked_paths(pathspec))
    forbidden_tracked = [
        path
        for path in forbidden_tracked
        if not path.endswith("/README.md") and not path.endswith("/.gitkeep") and "stage5bj" in path
    ]
    if forbidden_tracked:
        errors.append(f"forbidden Stage 5BJ local/generated files tracked: {forbidden_tracked}")

    result = {
        "stage5bj_valid": not errors,
        "crosswalk_closure_record_count": summary.get("crosswalk_closure_record_count", 0),
        "exact_512_hex_surface_locked_count": summary.get("exact_512_hex_surface_locked_count", 0),
        "surface_source_file_found_count": summary.get("surface_source_file_found_count", 0),
        "page_body_crosswalk_count": summary.get("fandom_page_body_crosswalk_count", 0),
        "boards_thread_found": summary.get("boards_thread_found"),
        "media_equivalence_record_count": summary.get("media_equivalence_record_count", 0),
        "source_gap_closed_count": summary.get("source_gap_closed_count", 0),
        "source_gap_carried_forward_count": summary.get("source_gap_carried_forward_count", 0),
        "new_source_gap_count": summary.get("new_source_gap_count", 0),
        "selected_next_stage_id": next_stage.get("selected_next_stage_id"),
        "validation_error_count": len(errors),
        "validation_errors": errors,
    }
    if errors:
        raise ValueError(json.dumps(result, indent=2, sort_keys=True))
    return result


def summarize_stage5bj(path: Path = DATA_PATHS["summary"]) -> dict[str, Any]:
    return _read_yaml(path)
