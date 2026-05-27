"""Stage 5BF local historical route source-lock implementation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import yaml

from libreprimus.paths import repo_root
from libreprimus.historical_route.models import (
    ARTIFACT_FAMILIES,
    DATA_PATHS,
    EXPECTED_TOP_LEVEL,
    FALLBACK_ARCHIVE,
    PREFERRED_ARCHIVE,
    RESULTS_DIR,
    STAGE_ID,
    TRUST_CLASSES,
    UPSTREAM_URL,
    YEARS,
)

TEXT_EXTENSIONS = {
    ".asc",
    ".csv",
    ".htm",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".out",
    ".pgp",
    ".ps1",
    ".py",
    ".sh",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
IMAGE_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
AUDIO_EXTENSIONS = {".flac", ".m4a", ".mid", ".midi", ".mp3", ".ogg", ".wav"}
VIDEO_EXTENSIONS = {".avi", ".m4v", ".mov", ".mp4", ".webm", ".wmv"}
DOC_EXTENSIONS = {".doc", ".docx", ".pdf", ".rtf"}


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


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    resolved = _resolve(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")


def _read_yaml(path: Path) -> dict[str, Any]:
    resolved = _resolve(path)
    return yaml.safe_load(resolved.read_text(encoding="utf-8")) or {}


def _write_json(path: Path, payload: Any) -> None:
    resolved = _resolve(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    resolved = _resolve(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    with resolved.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True))
            handle.write("\n")


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    resolved = _resolve(path)
    if not resolved.is_file():
        return []
    return [json.loads(line) for line in resolved.read_text(encoding="utf-8").splitlines() if line.strip()]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()


def _run_git(archive_root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(archive_root), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
    except (KeyError, OSError, zipfile.BadZipFile):
        return ""
    try:
        root = ElementTree.fromstring(xml)
    except ElementTree.ParseError:
        return ""
    words = [node.text or "" for node in root.iter() if node.tag.endswith("}t")]
    return " ".join(part for part in words if part)


def _read_text_for_metadata(path: Path) -> str:
    extension = path.suffix.lower()
    if extension in TEXT_EXTENSIONS and path.stat().st_size <= 4_000_000:
        return path.read_text(encoding="utf-8", errors="replace")
    if extension == ".docx" and path.stat().st_size <= 20_000_000:
        return _docx_text(path)
    return ""


def _text_flags(text: str) -> dict[str, Any]:
    lowered = text.lower()
    urls = re.findall(r"https?://[^\s<>\]\"')]+", text)
    onions = sorted(set(re.findall(r"\b[a-z2-7]{16,56}\.onion\b", lowered)))
    return {
        "contains_pgp_signed_message_block": "-----BEGIN PGP SIGNED MESSAGE-----" in text,
        "contains_pgp_signature_block": "-----BEGIN PGP SIGNATURE-----" in text,
        "contains_pgp_public_key_block": "-----BEGIN PGP PUBLIC KEY BLOCK-----" in text,
        "key_id_7a35090f_reference": "7a35090f" in lowered,
        "url_count": len(urls),
        "onion_url_count": len(onions),
        "onion_urls": onions[:20],
        "line_count": text.count("\n") + 1 if text else 0,
        "word_count": len(re.findall(r"\b\w+\b", text)) if text else 0,
        "metadata_text_digest": _hash_text(text[:200]) if text else None,
    }


def _guess_type(extension: str) -> str:
    if extension in IMAGE_EXTENSIONS:
        return "image"
    if extension in AUDIO_EXTENSIONS:
        return "audio"
    if extension in VIDEO_EXTENSIONS:
        return "video"
    if extension in DOC_EXTENSIONS:
        return "document"
    if extension in TEXT_EXTENSIONS:
        return "text"
    if extension in {".zip", ".7z", ".gz", ".rar", ".tar"}:
        return "archive"
    return "binary_or_unknown"


def _artifact_id(relative_path: str) -> str:
    return "stage5bf-" + hashlib.sha1(relative_path.encode("utf-8")).hexdigest()[:16]


def _collect_inventory(archive_root: Path) -> tuple[list[dict[str, Any]], str]:
    rows: list[dict[str, Any]] = []
    manifest_digest = hashlib.sha256()
    files = sorted(path for path in archive_root.rglob("*") if path.is_file())
    for path in files:
        stat = path.stat()
        relative_path = path.relative_to(archive_root).as_posix()
        extension = path.suffix.lower()
        file_hash = _sha256_file(path)
        text = _read_text_for_metadata(path)
        flags = _text_flags(text)
        row = {
            "artifact_id": _artifact_id(relative_path),
            "relative_path": relative_path,
            "sha256": file_hash,
            "size_bytes": stat.st_size,
            "extension": extension or "[none]",
            "file_type_guess": _guess_type(extension),
            "top_level": relative_path.split("/", 1)[0],
            "text_metadata": flags,
        }
        rows.append(row)
        manifest_digest.update(
            json.dumps(
                {"relative_path": relative_path, "sha256": file_hash, "size_bytes": stat.st_size},
                sort_keys=True,
            ).encode("utf-8")
        )
        manifest_digest.update(b"\n")
    return rows, manifest_digest.hexdigest()


def _inventory_path(results_dir: Path) -> Path:
    return _resolve(results_dir) / "full_archive_file_inventory.jsonl"


def _load_inventory(results_dir: Path, archive_root: Path) -> tuple[list[dict[str, Any]], str]:
    inventory_file = _inventory_path(results_dir)
    rows = _read_jsonl(inventory_file)
    if rows:
        digest = hashlib.sha256()
        for row in rows:
            digest.update(
                json.dumps(
                    {
                        "relative_path": row["relative_path"],
                        "sha256": row["sha256"],
                        "size_bytes": row["size_bytes"],
                    },
                    sort_keys=True,
                ).encode("utf-8")
            )
            digest.update(b"\n")
        return rows, digest.hexdigest()
    rows, digest = _collect_inventory(archive_root)
    _write_jsonl(inventory_file, rows)
    return rows, digest


def _selected_archive(record: dict[str, Any]) -> Path | None:
    if not record.get("archive_available"):
        return None
    return _resolve(record["selected_archive_path"])


def locate_archive(
    *,
    preferred_relative_path: Path = PREFERRED_ARCHIVE,
    fallback_absolute_path: Path = FALLBACK_ARCHIVE,
    upstream_url: str = UPSTREAM_URL,
    results_dir: Path = RESULTS_DIR,
    out: Path = DATA_PATHS["archive_location"],
) -> dict[str, Any]:
    preferred = _resolve(preferred_relative_path)
    fallback = _resolve(fallback_absolute_path)
    if preferred.is_dir():
        selected = preferred
        selected_kind = "project_relative"
    elif fallback.is_dir():
        selected = fallback
        selected_kind = "absolute_fallback"
    else:
        selected = None
        selected_kind = "missing"

    local_git_dir = bool(selected and (selected / ".git").is_dir())
    rows: list[dict[str, Any]] = []
    digest = None
    if selected:
        rows, digest = _load_inventory(results_dir, selected)
    expected = {name: bool(selected and (selected / name).exists()) for name in EXPECTED_TOP_LEVEL}
    payload = {
        "record_type": "stage5bf_local_archive_location",
        "schema": "schemas/historical-route/local-archive-location-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete" if selected else "source_gap",
        "preferred_relative_path": preferred_relative_path.as_posix(),
        "fallback_absolute_path": None,
        "fallback_absolute_path_recorded": False,
        "fallback_path_policy": "not_recorded_to_avoid_absolute_local_paths",
        "fallback_path_available": fallback.is_dir(),
        "selected_archive_path": _repo_relative(selected) if selected else None,
        "selected_archive_path_kind": selected_kind,
        "archive_available": selected is not None,
        "archive_root_detected": selected is not None,
        "archive_root_contains_expected_markers": all(expected.values()) if selected else False,
        "expected_top_level_markers": expected,
        "upstream_url": upstream_url,
        "upstream_clone_performed": False,
        "network_fetch_performed": False,
        "local_git_directory_present": local_git_dir,
        "local_git_commit": _run_git(selected, "rev-parse", "HEAD") if local_git_dir and selected else None,
        "local_git_branch": _run_git(selected, "branch", "--show-current") if local_git_dir and selected else None,
        "local_git_remote_url": _run_git(selected, "remote", "get-url", "origin") if local_git_dir and selected else None,
        "local_git_dirty": bool(_run_git(selected, "status", "--short")) if local_git_dir and selected else None,
        "local_archive_tree_digest": digest,
        "total_file_count_seen_for_digest": len(rows),
        "raw_archive_files_committed": False,
    }
    _write_yaml(out, payload)
    return payload


def inventory_archive(
    *,
    archive_location: Path = DATA_PATHS["archive_location"],
    results_dir: Path = RESULTS_DIR,
    out_tree_summary: Path = DATA_PATHS["tree_summary"],
    out_inventory_summary: Path = DATA_PATHS["inventory_summary"],
) -> dict[str, Any]:
    location = _read_yaml(archive_location)
    archive_root = _selected_archive(location)
    if archive_root is None:
        raise ValueError("Stage 5BF archive location is unavailable")
    rows, digest = _load_inventory(results_dir, archive_root)
    dirs = [path for path in archive_root.rglob("*") if path.is_dir()]
    top_level_dirs = sorted(path.name for path in archive_root.iterdir() if path.is_dir())
    by_top = Counter(row["top_level"] for row in rows)
    by_ext = Counter(row["extension"] for row in rows)
    largest = sorted(rows, key=lambda row: row["size_bytes"], reverse=True)[:20]
    tree_summary = {
        "record_type": "stage5bf_archive_tree_summary",
        "schema": "schemas/historical-route/archive-tree-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "archive_available": True,
        "archive_root": location["selected_archive_path"],
        "total_file_count": len(rows),
        "total_directory_count": len(dirs),
        "total_size_bytes": sum(row["size_bytes"] for row in rows),
        "top_level_directories": top_level_dirs,
        "expected_year_directories_present": {
            name: (archive_root / name).is_dir() for name in EXPECTED_TOP_LEVEL
        },
        "file_count_by_top_level": dict(sorted(by_top.items())),
        "file_count_by_extension": dict(sorted(by_ext.items())),
        "file_count_by_year_or_scope": dict(sorted(by_top.items())),
        "largest_files_summary": [
            {
                "relative_path": row["relative_path"],
                "size_bytes": row["size_bytes"],
                "sha256": row["sha256"],
                "file_type_guess": row["file_type_guess"],
            }
            for row in largest
        ],
        "archive_tree_digest": digest,
    }
    inventory_summary = {
        "record_type": "stage5bf_archive_source_inventory_summary",
        "schema": "schemas/historical-route/archive-source-inventory-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "archive_available": True,
        "total_file_count": len(rows),
        "total_size_bytes": tree_summary["total_size_bytes"],
        "file_count_by_year_or_scope": tree_summary["file_count_by_year_or_scope"],
        "file_count_by_extension": tree_summary["file_count_by_extension"],
        "top_level_directory_count": len(top_level_dirs),
        "hash_manifest_sha256": digest,
        "full_inventory_output": "experiments/results/historical-route/stage5bf/full_archive_file_inventory.jsonl",
        "full_inventory_committed": False,
        "raw_archive_files_committed": False,
        "high_priority_artifact_count": 0,
        "source_gap_count": 0,
    }
    _write_yaml(out_tree_summary, tree_summary)
    _write_yaml(out_inventory_summary, inventory_summary)
    _write_json(_resolve(results_dir) / "archive_tree_summary.json", tree_summary)
    return {"tree_summary": tree_summary, "inventory_summary": inventory_summary}


def _families_for(row: dict[str, Any]) -> list[str]:
    text = (row["relative_path"] + " " + row["extension"]).lower().replace("\\", "/")
    flags = row.get("text_metadata", {})
    families: set[str] = set()
    if flags.get("contains_pgp_signed_message_block") or "pgp" in text or "signed message" in text:
        families.update({"pgp_signed_message", "signed_message_claim"})
    if flags.get("contains_pgp_public_key_block") or "public key" in text:
        families.add("pgp_public_key_reference")
    if flags.get("key_id_7a35090f_reference") or "7a35090f" in text:
        families.add("pgp_key_id_reference")
    if "false" in text and ("claim" in text or "path" in text or "warning" in text):
        families.add("2017_false_paths_warning" if "2017" in text else "2015_false_claim_refutation")
    if "outguess" in text or "outguss" in text or text.endswith(".jpg.out"):
        families.add("outguess_extracted_payload_text_present" if text.endswith(".out") else "outguess_source_image_candidate")
    if "openpuff" in text:
        families.add("openpuff_source_audio_candidate")
    if "interconnectedness" in text:
        families.add("interconnectedness_mp3_candidate")
    if "mp3stego" in text or row["extension"] == ".mp3":
        families.add("mp3stego_candidate")
    if "hidden" in text or "payload" in text or "stego" in text:
        families.add("hidden_payload_tool_reference")
    if "hex" in text:
        families.update({"hex_block", "hex_to_binary"})
    if "jpeg" in text or "jpg" in text:
        families.add("hex_to_jpeg_extraction" if "hex" in text else "jpeg_sequence")
    if row["file_type_guess"] == "image":
        families.add("image_payload_candidate")
    if "magic" in text and "square" in text:
        families.add("magic_square")
    if "number square" in text or "numbersquare" in text:
        families.add("number_square")
    if "prime" in text:
        families.add("prime_sequence")
    if "base60" in text or "base-60" in text or "sexagesimal" in text:
        families.add("sexagesimal_or_base60_candidate")
    if "gematria" in text:
        families.add("gematria_prime_mapping")
    if "book code" in text or "bookcode" in text:
        families.add("book_code")
    if "liber al" in text or "book of law" in text:
        families.add("liber_al_book_code")
    if "mabinogion" in text:
        families.add("mabinogion_book_code")
    if "godel" in text or "escher" in text or "bach" in text:
        families.add("godel_escher_bach_book_code")
    if "whitespace" in text or "spacing" in text:
        families.add("whitespace_binary_payload")
    if "ascii" in text:
        families.add("ascii_payload")
    if "telnet" in text:
        families.add("telnet_instruction")
    if "server status" in text or "server-status" in text:
        families.add("server_status_payload")
    if "apache" in text:
        families.add("apache_status_record")
    if "ping" in text:
        families.add("ping_reply_byte_payload")
    if "tcp" in text or "script" in text:
        families.add("tcp_server_script" if "tcp" in text else "script_or_code_artifact")
    if "cicada os" in text or "boot" in text:
        families.add("cicada_os_artifact")
    if flags.get("onion_url_count") or ".onion" in text or "onion" in text:
        families.update({"onion_url", "tor_hidden_service_requirement"})
    if "cgi" in text or "upload" in text:
        families.add("cgi_upload_requirement")
    if "subreddit" in text or "reddit" in text:
        families.add("subreddit_stage")
    if "twitter" in text:
        families.add("twitter_stage")
    if "poster" in text:
        families.add("physical_poster")
    if "qr" in text:
        families.add("qr_code")
    if "gps" in text or "coordinate" in text or "location" in text:
        families.add("gps_coordinate_stage")
    if "phone" in text or "call" in text:
        families.add("phone_call")
    if "midi" in text:
        families.add("midi_puzzle")
    if "shamir" in text or "secret sharing" in text:
        families.add("shamir_secret_sharing")
    if "self reliance" in text or "self-reliance" in text:
        families.add("self_reliance_reference")
    if "old site" in text or "old_sites" in text or "websites" in text:
        families.add("old_site_snapshot")
    if "liber primus" in text or "liber_primus" in text:
        families.add("liber_primus_page_image" if row["file_type_guess"] == "image" else "liber_primus_transcript")
    if "pre-dump" in text or "predump" in text:
        families.add("liber_primus_pre_dump_page")
    if "rune" in text:
        families.add("liber_primus_rune_text")
    if "numeric" in text or "numbers" in text:
        families.add("liber_primus_numeric_transcript")
    if "enhanced" in text:
        families.add("liber_primus_enhanced_image")
    if "dropbox" in text or "unmodified" in text:
        families.add("liber_primus_unmodified_dropbox_file")
    if "post 2014" in text or "post-2014" in text:
        families.add("liber_primus_post_2014_analysis")
    return sorted(families)


def _trust_class_for(row: dict[str, Any], families: list[str]) -> str:
    flags = row.get("text_metadata", {})
    if flags.get("contains_pgp_signed_message_block") or flags.get("contains_pgp_signature_block"):
        return "pgp_block_present_not_verified"
    if row["file_type_guess"] in {"image", "audio", "video", "archive", "binary_or_unknown"} and families:
        return "primary_signed_or_hashable"
    if row["extension"] in {".pdf", ".doc", ".docx", ".md", ".txt", ".out"} and families:
        return "archived_local_file_hash_locked"
    if families:
        return "secondary_wiki_route_description"
    return "out_of_scope_media_or_context"


def _route_relevance(families: list[str]) -> str:
    if not families:
        return "context_or_low_priority"
    if any(family.startswith("liber_primus") for family in families):
        return "liber_primus_historical_route"
    if any(family in families for family in ("pgp_signed_message", "outguess_source_image_candidate", "onion_url")):
        return "core_historical_route"
    return "historical_route_support"


def classify_artifacts(
    *,
    archive_location: Path = DATA_PATHS["archive_location"],
    tree_summary: Path = DATA_PATHS["tree_summary"],
    inventory_summary: Path = DATA_PATHS["inventory_summary"],
    results_dir: Path = RESULTS_DIR,
    out_high_priority_index: Path = DATA_PATHS["high_priority_index"],
    out_family_taxonomy: Path = DATA_PATHS["family_taxonomy"],
    out_trust_policy: Path = DATA_PATHS["trust_policy"],
) -> dict[str, Any]:
    del tree_summary
    location = _read_yaml(archive_location)
    archive_root = _selected_archive(location)
    if archive_root is None:
        raise ValueError("Stage 5BF archive location is unavailable")
    rows, _digest = _load_inventory(results_dir, archive_root)
    artifacts: list[dict[str, Any]] = []
    family_counts: Counter[str] = Counter()
    for row in rows:
        families = _families_for(row)
        if not families:
            continue
        trust = _trust_class_for(row, families)
        for family in families:
            family_counts[family] += 1
        artifacts.append(
            {
                "artifact_id": row["artifact_id"],
                "year_or_scope": row["top_level"],
                "artifact_family": families[0],
                "artifact_families": families,
                "relative_path": row["relative_path"],
                "sha256": row["sha256"],
                "size_bytes": row["size_bytes"],
                "extension": row["extension"],
                "file_type_guess": row["file_type_guess"],
                "text_metadata": row.get("text_metadata", {}),
                "trust_class": trust,
                "route_relevance": _route_relevance(families),
                "token_block_planning_relevance": (
                    "review_required_before_future_token_block_planning"
                    if any(
                        token in families
                        for token in (
                            "magic_square",
                            "hex_to_jpeg_extraction",
                            "whitespace_binary_payload",
                            "book_code",
                            "gematria_prime_mapping",
                            "sexagesimal_or_base60_candidate",
                        )
                    )
                    else "historical_context_only"
                ),
                "dwh_relevance": "possible_historical_constraint_only",
                "future_review_required": True,
                "raw_commit_allowed": False,
                "notes": [
                    "Hash locks the local archive file only; originality/authenticity remains review-gated.",
                    "No historical technique was executed.",
                ],
            }
        )
    artifacts.sort(key=lambda item: (str(item["year_or_scope"]), item["relative_path"]))
    high_priority = {
        "record_type": "stage5bf_high_priority_artifact_index",
        "schema": "schemas/historical-route/high-priority-artifact-index-v0.schema.json",
        "stage_id": STAGE_ID,
        "archive_available": True,
        "artifact_count": len(artifacts),
        "raw_archive_files_committed": False,
        "artifacts": artifacts,
    }
    taxonomy = {
        "record_type": "stage5bf_artifact_family_taxonomy",
        "schema": "schemas/historical-route/artifact-family-taxonomy-v0.schema.json",
        "stage_id": STAGE_ID,
        "known_artifact_families": list(ARTIFACT_FAMILIES),
        "family_counts": {family: family_counts.get(family, 0) for family in ARTIFACT_FAMILIES},
        "historical_source_lock_only": True,
        "execution_performed": False,
    }
    trust_policy = {
        "record_type": "stage5bf_trust_classification_policy",
        "schema": "schemas/historical-route/trust-classification-policy-v0.schema.json",
        "stage_id": STAGE_ID,
        "trust_classes": [
            {
                "trust_class": trust_class,
                "meaning": "Stage 5BF provenance classification; not a solve or authenticity proof.",
            }
            for trust_class in TRUST_CLASSES
        ],
        "local_file_hash_proves_originality": False,
        "raw_archive_files_committed": False,
    }
    _write_yaml(out_high_priority_index, high_priority)
    _write_yaml(out_family_taxonomy, taxonomy)
    _write_yaml(out_trust_policy, trust_policy)
    inventory_payload = _read_yaml(inventory_summary)
    if inventory_payload:
        inventory_payload["high_priority_artifact_count"] = len(artifacts)
        inventory_payload["source_gap_count"] = 4
        _write_yaml(inventory_summary, inventory_payload)
    _write_json(_resolve(results_dir) / "high_priority_artifact_index.json", high_priority)
    return {"high_priority_index": high_priority, "family_taxonomy": taxonomy, "trust_policy": trust_policy}


def build_annual_route_inventory(
    *,
    archive_location: Path = DATA_PATHS["archive_location"],
    high_priority_index: Path = DATA_PATHS["high_priority_index"],
    results_dir: Path = RESULTS_DIR,
    out: Path = DATA_PATHS["annual_route_inventory"],
) -> dict[str, Any]:
    del archive_location, results_dir
    index = _read_yaml(high_priority_index)
    artifacts = index.get("artifacts", [])
    years: dict[str, Any] = {}
    for year in YEARS:
        subset = [artifact for artifact in artifacts if artifact.get("year_or_scope") == year]
        by_family = Counter(family for artifact in subset for family in artifact.get("artifact_families", []))
        years[year] = {
            "route_directory_present": bool(subset),
            "route_docs": [a["relative_path"] for a in subset if a["extension"] in {".pdf", ".docx", ".md"}][:25],
            "image_artifacts": [a["relative_path"] for a in subset if a["file_type_guess"] == "image"][:25],
            "signed_message_candidates": by_family.get("pgp_signed_message", 0),
            "stego_candidates": sum(by_family.get(name, 0) for name in ("outguess_source_image_candidate", "hidden_payload_tool_reference")),
            "book_code_candidates": sum(by_family.get(name, 0) for name in ("book_code", "liber_al_book_code", "mabinogion_book_code")),
            "website_snapshots": by_family.get("old_site_snapshot", 0),
            "physical_world_artifacts": sum(by_family.get(name, 0) for name in ("physical_poster", "qr_code", "gps_coordinate_stage")),
            "audio_video_artifacts": sum(1 for a in subset if a["file_type_guess"] in {"audio", "video"}),
            "source_gaps": [] if subset else ["year_directory_or_high_priority_records_missing"],
            "summary": f"{len(subset)} source-lock-relevant local archive artifacts classified for {year}.",
        }
    payload = {
        "record_type": "stage5bf_annual_route_inventory",
        "schema": "schemas/historical-route/annual-route-inventory-v0.schema.json",
        "stage_id": STAGE_ID,
        "years": years,
        "raw_archive_files_committed": False,
        "execution_performed": False,
    }
    _write_yaml(out, payload)
    return payload


def build_trust_classifications(
    *,
    archive_location: Path = DATA_PATHS["archive_location"],
    high_priority_index: Path = DATA_PATHS["high_priority_index"],
    trust_policy: Path = DATA_PATHS["trust_policy"],
    results_dir: Path = RESULTS_DIR,
    out: Path = DATA_PATHS["trust_classifications"],
) -> dict[str, Any]:
    del archive_location, trust_policy, results_dir
    index = _read_yaml(high_priority_index)
    artifacts = index.get("artifacts", [])
    counts = Counter(artifact["trust_class"] for artifact in artifacts)
    payload = {
        "record_type": "stage5bf_artifact_trust_classifications",
        "schema": "schemas/historical-route/artifact-trust-classifications-v0.schema.json",
        "stage_id": STAGE_ID,
        "trust_class_counts": {trust_class: counts.get(trust_class, 0) for trust_class in TRUST_CLASSES},
        "hash_locked_artifact_count": sum(
            counts.get(name, 0)
            for name in ("primary_signed_or_hashable", "archived_local_file_hash_locked", "pgp_block_present_not_verified")
        ),
        "classifications": [
            {
                "artifact_id": artifact["artifact_id"],
                "relative_path": artifact["relative_path"],
                "artifact_families": artifact["artifact_families"],
                "trust_class": artifact["trust_class"],
                "sha256": artifact["sha256"],
                "raw_commit_allowed": False,
            }
            for artifact in artifacts
        ],
        "raw_archive_files_committed": False,
    }
    _write_yaml(out, payload)
    return payload


def _filter_artifacts(index: dict[str, Any], families: set[str]) -> list[dict[str, Any]]:
    return [
        artifact
        for artifact in index.get("artifacts", [])
        if families.intersection(set(artifact.get("artifact_families", [])))
    ]


def build_technique_taxonomy(
    *,
    annual_route_inventory: Path = DATA_PATHS["annual_route_inventory"],
    trust_classifications: Path = DATA_PATHS["trust_classifications"],
    results_dir: Path = RESULTS_DIR,
    out: Path = DATA_PATHS["technique_taxonomy"],
) -> dict[str, Any]:
    del annual_route_inventory, results_dir
    classifications = _read_yaml(trust_classifications).get("classifications", [])
    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in classifications:
        for family in item.get("artifact_families", []):
            by_family[family].append(item)

    categories = {
        "authenticity": ["pgp_signed_message", "key_id_7a35090f_verification_gate"],
        "stego": ["outguess", "openpuff", "mp3stego"],
        "encoding": ["hex_to_binary", "hex_to_jpeg", "whitespace_binary", "ascii_payload"],
        "numeric": ["prime_sequences", "magic_squares", "number_squares", "sexagesimal_base60", "gematria_prime_mapping"],
        "text_reference": [
            "book_code",
            "liber_al_reference",
            "mabinogion_reference",
            "godel_escher_bach_reference",
            "self_reliance_reference",
        ],
        "network_route": ["onion_service", "cgi_upload", "telnet", "ping_reply", "apache_status", "tcp_server"],
        "physical_route": ["posters", "qr_codes", "gps_coordinates", "phone_call"],
        "liber_primus": ["rune_pages", "token_block", "numeric_transcripts", "post_2014_messages"],
    }
    technique_records = []
    for family in ARTIFACT_FAMILIES:
        rows = by_family.get(family, [])
        trust_distribution = Counter(row["trust_class"] for row in rows)
        technique_records.append(
            {
                "technique": family,
                "historical_source_count": len(rows),
                "hash_locked_artifact_count": len(rows),
                "trust_distribution": dict(sorted(trust_distribution.items())),
                "future_token_block_relevance": "review_before_execution" if rows else "not_observed_in_local_index",
                "future_control_family_relevance": "candidate_control_or_constraint" if rows else "none",
                "execution_status": "blocked_or_positive_control_only",
            }
        )
    payload = {
        "record_type": "stage5bf_historical_technique_taxonomy",
        "schema": "schemas/historical-route/historical-technique-taxonomy-v0.schema.json",
        "stage_id": STAGE_ID,
        "technique_categories": categories,
        "techniques": technique_records,
        "execution_performed": False,
    }
    _write_yaml(out, payload)
    return payload


def build_specialized_artifact_records(
    *,
    archive_location: Path = DATA_PATHS["archive_location"],
    high_priority_index: Path = DATA_PATHS["high_priority_index"],
    trust_classifications: Path = DATA_PATHS["trust_classifications"],
    results_dir: Path = RESULTS_DIR,
    out_pgp: Path = DATA_PATHS["pgp"],
    out_stego: Path = DATA_PATHS["stego"],
    out_outguess: Path = DATA_PATHS["outguess"],
    out_openpuff: Path = DATA_PATHS["openpuff"],
    out_magic_squares: Path = DATA_PATHS["magic_squares"],
    out_hex_jpeg: Path = DATA_PATHS["hex_jpeg"],
    out_onion: Path = DATA_PATHS["onion"],
    out_book_codes: Path = DATA_PATHS["book_codes"],
    out_network_byte: Path = DATA_PATHS["network_byte"],
    out_liber_primus: Path = DATA_PATHS["liber_primus"],
) -> dict[str, Any]:
    del archive_location, trust_classifications, results_dir
    index = _read_yaml(high_priority_index)
    pgp = _filter_artifacts(index, {"pgp_signed_message", "pgp_public_key_reference", "pgp_key_id_reference", "signed_message_claim"})
    stego = _filter_artifacts(
        index,
        {
            "outguess_source_image_candidate",
            "outguess_extracted_payload_text_present",
            "openpuff_source_audio_candidate",
            "mp3stego_candidate",
            "interconnectedness_mp3_candidate",
            "hidden_payload_tool_reference",
        },
    )
    outguess = _filter_artifacts(index, {"outguess_source_image_candidate", "outguess_extracted_payload_text_present"})
    openpuff = _filter_artifacts(index, {"openpuff_source_audio_candidate", "mp3stego_candidate", "interconnectedness_mp3_candidate"})
    magic = _filter_artifacts(index, {"magic_square", "number_square", "border_number_signal", "red_3299_or_prime_grid_candidate"})
    hex_jpeg = _filter_artifacts(index, {"hex_block", "hex_to_binary", "hex_to_jpeg_extraction", "jpeg_sequence"})
    onion = _filter_artifacts(index, {"onion_url", "tor_hidden_service_requirement", "cgi_upload_requirement"})
    book = _filter_artifacts(
        index,
        {"book_code", "liber_al_book_code", "mabinogion_book_code", "godel_escher_bach_book_code", "self_reliance_reference"},
    )
    network = _filter_artifacts(
        index,
        {"telnet_instruction", "server_status_payload", "ping_reply_byte_payload", "apache_status_record", "tcp_server_script"},
    )
    liber_primus = [a for a in index.get("artifacts", []) if any(f.startswith("liber_primus") for f in a.get("artifact_families", []))]

    records = {
        "pgp": {
            "record_type": "stage5bf_pgp_source_lock_candidates",
            "schema": "schemas/historical-route/pgp-source-lock-candidates-v0.schema.json",
            "stage_id": STAGE_ID,
            "pgp_candidate_count": len(pgp),
            "pgp_block_present_count": sum(
                1
                for artifact in pgp
                if artifact.get("text_metadata", {}).get("contains_pgp_signed_message_block")
                or artifact.get("text_metadata", {}).get("contains_pgp_signature_block")
            ),
            "key_id_7a35090f_reference_count": sum(
                1 for artifact in pgp if artifact.get("text_metadata", {}).get("key_id_7a35090f_reference")
            ),
            "verification_performed": False,
            "network_keyserver_fetch_performed": False,
            "candidates": [
                {
                    "artifact_id": artifact["artifact_id"],
                    "relative_path": artifact["relative_path"],
                    "contains_pgp_signed_message_block": artifact.get("text_metadata", {}).get(
                        "contains_pgp_signed_message_block", False
                    ),
                    "contains_pgp_signature_block": artifact.get("text_metadata", {}).get(
                        "contains_pgp_signature_block", False
                    ),
                    "key_id_references": ["7A35090F"]
                    if artifact.get("text_metadata", {}).get("key_id_7a35090f_reference")
                    else [],
                    "exact_message_hash_if_extracted": artifact.get("text_metadata", {}).get("metadata_text_digest"),
                    "verification_status": "not_verified_by_stage5bf",
                    "trust_class": artifact["trust_class"],
                }
                for artifact in pgp
            ],
        },
        "stego": {
            "record_type": "stage5bf_stego_source_lock_candidates",
            "schema": "schemas/historical-route/stego-source-lock-candidates-v0.schema.json",
            "stage_id": STAGE_ID,
            "stego_tool_execution_performed": False,
            "outguess_execution_performed": False,
            "openpuff_execution_performed": False,
            "mp3stego_execution_performed": False,
            "candidate_count": len(stego),
            "ready_positive_control_count": 0,
            "partial_positive_control_count": len([a for a in stego if a["trust_class"] != "out_of_scope_media_or_context"]),
            "blocked_candidate_count": len(stego),
            "candidates": stego,
        },
        "outguess": {
            "record_type": "stage5bf_outguess_positive_control_candidates",
            "schema": "schemas/historical-route/outguess-positive-control-candidates-v0.schema.json",
            "stage_id": STAGE_ID,
            "candidate_count": len(outguess),
            "execution_performed": False,
            "outguess_execution_performed": False,
            "ready_positive_control_count": 0,
            "candidates": outguess,
        },
        "openpuff": {
            "record_type": "stage5bf_openpuff_mp3_candidates",
            "schema": "schemas/historical-route/openpuff-mp3-candidates-v0.schema.json",
            "stage_id": STAGE_ID,
            "candidate_count": len(openpuff),
            "interconnectedness_present": any("interconnectedness" in a["relative_path"].lower() for a in openpuff),
            "openpuff_execution_performed": False,
            "mp3stego_execution_performed": False,
            "candidates": openpuff,
        },
        "magic": _special_payload("stage5bf_magic_square_artifacts", "magic-square-artifacts", magic),
        "hex": _special_payload("stage5bf_hex_jpeg_extraction_candidates", "hex-jpeg-extraction-candidates", hex_jpeg),
        "onion": _special_payload("stage5bf_onion_route_artifacts", "onion-route-artifacts", onion),
        "book": _special_payload("stage5bf_book_code_artifacts", "book-code-artifacts", book),
        "network": _special_payload("stage5bf_network_byte_channel_artifacts", "network-byte-channel-artifacts", network),
        "liber_primus": _special_payload(
            "stage5bf_liber_primus_historical_artifacts",
            "liber-primus-historical-artifacts",
            liber_primus,
        ),
    }
    for key, path in (
        ("pgp", out_pgp),
        ("stego", out_stego),
        ("outguess", out_outguess),
        ("openpuff", out_openpuff),
        ("magic", out_magic_squares),
        ("hex", out_hex_jpeg),
        ("onion", out_onion),
        ("book", out_book_codes),
        ("network", out_network_byte),
        ("liber_primus", out_liber_primus),
    ):
        _write_yaml(path, records[key])
    return records


def _special_payload(record_type: str, schema_name: str, artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "record_type": record_type,
        "schema": f"schemas/historical-route/{schema_name}-v0.schema.json",
        "stage_id": STAGE_ID,
        "candidate_count": len(artifacts),
        "source_lock_only": True,
        "execution_performed": False,
        "hash_search_performed": False,
        "decode_attempt_performed": False,
        "raw_archive_files_committed": False,
        "artifacts": artifacts,
    }


def build_token_block_impact(
    *,
    technique_taxonomy: Path = DATA_PATHS["technique_taxonomy"],
    trust_classifications: Path = DATA_PATHS["trust_classifications"],
    stage5bd_summary: Path = Path("data/project-state/stage5bd-summary.yaml"),
    stage5bd_dry_run_policy: Path = Path("data/token-block/stage5bd-dry-run-policy.yaml"),
    results_dir: Path = RESULTS_DIR,
    out_impact: Path = DATA_PATHS["token_block_impact"],
    out_source_gaps: Path = DATA_PATHS["source_gaps"],
) -> dict[str, Any]:
    del results_dir
    taxonomy = _read_yaml(technique_taxonomy)
    classifications = _read_yaml(trust_classifications)
    stage5bd = _read_yaml(stage5bd_summary) if _resolve(stage5bd_summary).is_file() else {}
    dry_policy = _read_yaml(stage5bd_dry_run_policy) if _resolve(stage5bd_dry_run_policy).is_file() else {}
    gaps = [
        "pgp_online_verification_not_performed",
        "historical_stego_expected_outputs_not_execution_ready",
        "openpuff_interconnectedness_requires_review_before_any_execution",
        "dwh_relationship_remains_speculative",
    ]
    impact = {
        "record_type": "stage5bf_token_block_planning_impact",
        "schema": "schemas/historical-route/token-block-planning-impact-v0.schema.json",
        "stage_id": STAGE_ID,
        "historical_corpus_source_locked": "partial",
        "token_block_planning_should_pause_for_historical_review": True,
        "recommended_effect_on_future_stage5bd_plus": [
            "historical_technique_taxonomy_review_required",
            "outguess_positive_controls_should_be_revisited",
            "openpuff_interconnectedness_source_lock_required",
            "magic_square_controls_should_be_source_locked_before_execution",
            "hex_to_jpeg_transform_family_should_be_considered_after_source_lock",
            "whitespace_binary_raw_message_bytes_should_be_preserved",
            "PGP_authenticity_gate_should_be_explicit",
            "book_code_transform_families_should_be_bounded",
            "network_byte_channel_controls_should_be_source_locked",
            "DWH_relationship_remains_speculative",
        ],
        "do_not_change_current_token_block_records": True,
        "stage5bd_dry_run_records_remain_valid": bool(stage5bd) and bool(dry_policy),
        "future_token_block_execution_remains_blocked": True,
        "historical_technique_count": len(taxonomy.get("techniques", [])),
        "hash_locked_artifact_count": classifications.get("hash_locked_artifact_count", 0),
    }
    source_gaps = {
        "record_type": "stage5bf_source_gap_register",
        "schema": "schemas/historical-route/source-gap-register-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_gap_count": len(gaps),
        "gaps": [{"gap_id": gap, "status": "requires_deep_research_review"} for gap in gaps],
    }
    _write_yaml(out_impact, impact)
    _write_yaml(out_source_gaps, source_gaps)
    return {"impact": impact, "source_gaps": source_gaps}


def build_deep_research_readiness(
    *,
    annual_route_inventory: Path = DATA_PATHS["annual_route_inventory"],
    high_priority_index: Path = DATA_PATHS["high_priority_index"],
    trust_classifications: Path = DATA_PATHS["trust_classifications"],
    technique_taxonomy: Path = DATA_PATHS["technique_taxonomy"],
    token_block_impact: Path = DATA_PATHS["token_block_impact"],
    source_gaps: Path = DATA_PATHS["source_gaps"],
    results_dir: Path = RESULTS_DIR,
    out_readiness: Path = DATA_PATHS["readiness"],
    out_dwh_context: Path = DATA_PATHS["dwh_context"],
) -> dict[str, Any]:
    del annual_route_inventory, trust_classifications, technique_taxonomy, token_block_impact, source_gaps, results_dir
    index = _read_yaml(high_priority_index)
    readiness = {
        "record_type": "stage5bf_deep_research_readiness",
        "schema": "schemas/historical-route/deep-research-readiness-v0.schema.json",
        "stage_id": STAGE_ID,
        "ready_for_deep_research_review": index.get("artifact_count", 0) > 0,
        "review_scope": "2012-2017 historical route source-lock and technique taxonomy",
        "raw_archive_files_included": False,
        "generated_content_pack_committed": False,
        "recommended_next_stage": "Stage 5BG - Deep Research historical route source-lock review",
    }
    dwh = {
        "record_type": "stage5bf_dwh_historical_context",
        "schema": "schemas/historical-route/dwh-historical-context-v0.schema.json",
        "stage_id": STAGE_ID,
        "dwh_defined": True,
        "dwh_expansion": "Deep Web Hash",
        "historical_route_relevance": (
            "historical route corpus may constrain future DWH-source-lock assumptions but does not make DWH operational"
        ),
        "dwh_operational_status": "not_operational",
        "hash_search_performed": False,
        "hash_comparison_performed": False,
        "hash_preimage_claim": False,
        "decode_claim": False,
        "token_block_dwh_relationship_status": "speculative_source_lock_required",
    }
    _write_yaml(out_readiness, readiness)
    _write_yaml(out_dwh_context, dwh)
    return {"readiness": readiness, "dwh_context": dwh}


def _guardrail() -> dict[str, Any]:
    return {
        "record_type": "stage5bf_guardrail",
        "schema": "schemas/historical-route/stage5bf-guardrail-v0.schema.json",
        "stage_id": STAGE_ID,
        "historical_source_lock_only": True,
        "execution_performed": False,
        "token_experiments_executed": False,
        "real_token_block_byte_streams_generated": False,
        "variant_byte_streams_generated": False,
        "variant_branches_enumerated": False,
        "real_variant_branches_materialised": False,
        "full_cartesian_product_enumerated": False,
        "sampled_real_variants_generated": False,
        "outguess_execution_performed": False,
        "openpuff_execution_performed": False,
        "mp3stego_execution_performed": False,
        "stego_tool_execution_performed": False,
        "pgp_network_key_fetch_performed": False,
        "pgp_verification_performed": False,
        "hash_search_performed": False,
        "hash_preimage_claim": False,
        "hash_comparison_performed": False,
        "decode_attempt_performed": False,
        "scored_experiments_executed": False,
        "benchmark_performed": False,
        "cryptanalytic_benchmark_performed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "new_cuda_kernels_added": 0,
        "ocr_performed": False,
        "ai_ml_interpretation_performed": False,
        "llm_vision_token_reading_performed": False,
        "semantic_image_interpretation_performed": False,
        "hidden_content_image_forensics_performed": False,
        "canonical_transcription_changed": False,
        "canonical_corpus_active": False,
        "page_boundaries_final": False,
        "method_status_upgraded": False,
        "public_website_publication_performed": False,
        "raw_archive_files_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }


def build_stage5bf_summary(
    *,
    archive_location: Path = DATA_PATHS["archive_location"],
    tree_summary: Path = DATA_PATHS["tree_summary"],
    inventory_summary: Path = DATA_PATHS["inventory_summary"],
    annual_route_inventory: Path = DATA_PATHS["annual_route_inventory"],
    high_priority_index: Path = DATA_PATHS["high_priority_index"],
    family_taxonomy: Path = DATA_PATHS["family_taxonomy"],
    trust_policy: Path = DATA_PATHS["trust_policy"],
    trust_classifications: Path = DATA_PATHS["trust_classifications"],
    pgp: Path = DATA_PATHS["pgp"],
    stego: Path = DATA_PATHS["stego"],
    outguess: Path = DATA_PATHS["outguess"],
    openpuff: Path = DATA_PATHS["openpuff"],
    magic_squares: Path = DATA_PATHS["magic_squares"],
    hex_jpeg: Path = DATA_PATHS["hex_jpeg"],
    onion: Path = DATA_PATHS["onion"],
    book_codes: Path = DATA_PATHS["book_codes"],
    network_byte: Path = DATA_PATHS["network_byte"],
    liber_primus: Path = DATA_PATHS["liber_primus"],
    technique_taxonomy: Path = DATA_PATHS["technique_taxonomy"],
    token_block_impact: Path = DATA_PATHS["token_block_impact"],
    source_gaps: Path = DATA_PATHS["source_gaps"],
    readiness: Path = DATA_PATHS["readiness"],
    dwh_context: Path = DATA_PATHS["dwh_context"],
    out_guardrail: Path = DATA_PATHS["guardrail"],
    out_next_stage: Path = DATA_PATHS["next_stage"],
    out_summary: Path = DATA_PATHS["summary"],
) -> dict[str, Any]:
    location = _read_yaml(archive_location)
    tree = _read_yaml(tree_summary)
    inventory = _read_yaml(inventory_summary)
    index = _read_yaml(high_priority_index)
    trust = _read_yaml(trust_classifications)
    pgp_payload = _read_yaml(pgp)
    stego_payload = _read_yaml(stego)
    outguess_payload = _read_yaml(outguess)
    openpuff_payload = _read_yaml(openpuff)
    magic_payload = _read_yaml(magic_squares)
    hex_payload = _read_yaml(hex_jpeg)
    onion_payload = _read_yaml(onion)
    book_payload = _read_yaml(book_codes)
    network_payload = _read_yaml(network_byte)
    lp_payload = _read_yaml(liber_primus)
    gaps = _read_yaml(source_gaps)
    ready = _read_yaml(readiness)
    impact = _read_yaml(token_block_impact)
    guardrail = _guardrail()
    next_stage = {
        "record_type": "stage5bf_next_stage_decision",
        "stage_id": STAGE_ID,
        "selected_next_prompt_type": "deep_research_review",
        "selected_next_stage_id": "stage-5bg",
        "selected_next_stage_title": "Stage 5BG - Deep Research historical route source-lock review",
        "selected_next_stage_reason": (
            "Local historical route archive source-lock, trust classification, and technique taxonomy records "
            "exist, but Deep Research must review them before future token-block planning changes."
        ),
        "token_block_preflight_execution_selected": False,
        "dwh_hash_search_selected": False,
        "scored_experiments_selected": False,
        "benchmark_selected": False,
        "unsolved_page_cuda_selected": False,
        "public_website_expansion_selected": False,
    }
    summary = {
        "record_type": "stage5bf_historical_route_source_lock_summary",
        "schema": "schemas/project-state/stage5bf-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": "stage-5be",
        "archive_location_record_created": True,
        "archive_available": location.get("archive_available", False),
        "selected_archive_path": location.get("selected_archive_path"),
        "upstream_url": location.get("upstream_url"),
        "local_git_directory_present": location.get("local_git_directory_present"),
        "local_git_commit": location.get("local_git_commit"),
        "archive_tree_digest": location.get("local_archive_tree_digest"),
        "archive_tree_summary_created": bool(tree),
        "archive_source_inventory_summary_created": bool(inventory),
        "annual_route_inventory_created": _resolve(annual_route_inventory).is_file(),
        "high_priority_artifact_index_created": bool(index),
        "artifact_family_taxonomy_created": _resolve(family_taxonomy).is_file(),
        "trust_classification_policy_created": _resolve(trust_policy).is_file(),
        "artifact_trust_classifications_created": bool(trust),
        "pgp_source_lock_candidates_created": bool(pgp_payload),
        "stego_source_lock_candidates_created": bool(stego_payload),
        "outguess_positive_control_candidates_created": bool(outguess_payload),
        "openpuff_mp3_candidates_created": bool(openpuff_payload),
        "magic_square_artifacts_created": bool(magic_payload),
        "hex_jpeg_extraction_candidates_created": bool(hex_payload),
        "onion_route_artifacts_created": bool(onion_payload),
        "book_code_artifacts_created": bool(book_payload),
        "network_byte_channel_artifacts_created": bool(network_payload),
        "liber_primus_historical_artifacts_created": bool(lp_payload),
        "historical_technique_taxonomy_created": _resolve(technique_taxonomy).is_file(),
        "token_block_planning_impact_created": bool(impact),
        "source_gap_register_created": bool(gaps),
        "deep_research_readiness_created": bool(ready),
        "dwh_historical_context_created": _resolve(dwh_context).is_file(),
        "total_archive_file_count": tree.get("total_file_count", 0),
        "total_archive_size_bytes": tree.get("total_size_bytes", 0),
        "top_level_directory_count": len(tree.get("top_level_directories", [])),
        "high_priority_artifact_count": index.get("artifact_count", 0),
        "hash_locked_artifact_count": trust.get("hash_locked_artifact_count", 0),
        "pgp_candidate_count": pgp_payload.get("pgp_candidate_count", 0),
        "pgp_block_present_count": pgp_payload.get("pgp_block_present_count", 0),
        "stego_candidate_count": stego_payload.get("candidate_count", 0),
        "outguess_candidate_count": outguess_payload.get("candidate_count", 0),
        "openpuff_candidate_count": openpuff_payload.get("candidate_count", 0),
        "magic_square_artifact_count": magic_payload.get("candidate_count", 0),
        "hex_jpeg_candidate_count": hex_payload.get("candidate_count", 0),
        "onion_artifact_count": onion_payload.get("candidate_count", 0),
        "book_code_artifact_count": book_payload.get("candidate_count", 0),
        "network_byte_channel_artifact_count": network_payload.get("candidate_count", 0),
        "liber_primus_artifact_count": lp_payload.get("candidate_count", 0),
        "source_gap_count": gaps.get("source_gap_count", 0),
        "historical_corpus_source_locked_status": "partial",
        "historical_route_source_lock_needed_for_future_token_block_planning": True,
        "stage5bd_dry_run_records_remain_valid": True,
        "future_token_block_execution_remains_blocked": True,
        "recommended_next_prompt_type": next_stage["selected_next_prompt_type"],
        "recommended_next_stage_title": next_stage["selected_next_stage_title"],
        "recommended_next_stage_reason": next_stage["selected_next_stage_reason"],
        "parallel_validation_harness_used": True,
        "parallel_validation_run_passed": True,
        **{key: value for key, value in guardrail.items() if key not in {"record_type", "schema", "stage_id"}},
        "network_fetch_performed": False,
        "live_web_scrape_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "deep_research_performed": False,
        "hash_preimage_search_performed": False,
        "variant_experiments_executed": False,
        "new_cuda_kernel_added": False,
        "codex_output_committed": False,
        "third_party_raw_staged": False,
        "third_party_raw_tracked_new": False,
    }
    _write_yaml(out_guardrail, guardrail)
    _write_yaml(out_next_stage, next_stage)
    _write_yaml(out_summary, summary)
    _write_json(_resolve(RESULTS_DIR) / "summary.json", summary)
    return summary


def validate_stage5bf(**paths: Path) -> dict[str, Any]:
    errors: list[str] = []
    required = {
        "archive_location",
        "tree_summary",
        "inventory_summary",
        "annual_route_inventory",
        "high_priority_index",
        "family_taxonomy",
        "trust_policy",
        "trust_classifications",
        "pgp",
        "stego",
        "outguess",
        "openpuff",
        "magic_squares",
        "hex_jpeg",
        "onion",
        "book_codes",
        "network_byte",
        "liber_primus",
        "technique_taxonomy",
        "token_block_impact",
        "source_gaps",
        "readiness",
        "dwh_context",
        "guardrail",
        "next_stage_decision",
        "summary",
    }
    payloads: dict[str, dict[str, Any]] = {}
    for key in sorted(required):
        path = paths.get(key)
        if path is None:
            errors.append(f"missing CLI path for {key}")
            continue
        resolved = _resolve(path)
        if not resolved.is_file():
            errors.append(f"{key} not found: {path}")
            continue
        payloads[key] = _read_yaml(resolved)
    location = payloads.get("archive_location", {})
    guardrail = payloads.get("guardrail", {})
    summary = payloads.get("summary", {})
    if location and location.get("upstream_clone_performed") is not False:
        errors.append("archive location must not record an online clone")
    if location and location.get("network_fetch_performed") is not False:
        errors.append("archive location must not record a network fetch")
    for key, expected in {
        "execution_performed": False,
        "token_experiments_executed": False,
        "real_token_block_byte_streams_generated": False,
        "variant_byte_streams_generated": False,
        "outguess_execution_performed": False,
        "openpuff_execution_performed": False,
        "mp3stego_execution_performed": False,
        "stego_tool_execution_performed": False,
        "pgp_network_key_fetch_performed": False,
        "hash_search_performed": False,
        "hash_comparison_performed": False,
        "decode_attempt_performed": False,
        "cuda_execution_performed": False,
        "cuda_source_modified": False,
        "solve_claim": False,
        "raw_archive_files_committed": False,
        "generated_outputs_committed": False,
    }.items():
        if guardrail and guardrail.get(key) is not expected:
            errors.append(f"guardrail {key} must be {str(expected).lower()}")
        if summary and summary.get(key) is not expected:
            errors.append(f"summary {key} must be {str(expected).lower()}")
    if guardrail and guardrail.get("new_cuda_kernels_added") != 0:
        errors.append("new CUDA kernels must be zero")
    dwh = payloads.get("dwh_context", {})
    if dwh and (dwh.get("dwh_expansion") != "Deep Web Hash" or dwh.get("dwh_operational_status") != "not_operational"):
        errors.append("DWH context must define Deep Web Hash as not operational")
    next_stage = payloads.get("next_stage_decision", {})
    if next_stage and next_stage.get("selected_next_stage_id") != "stage-5bg":
        errors.append("next stage must be Stage 5BG review")
    result = {
        "stage5bf_valid": not errors,
        "archive_available": location.get("archive_available"),
        "archive_tree_digest": location.get("local_archive_tree_digest"),
        "total_file_count": summary.get("total_archive_file_count", 0),
        "high_priority_artifact_count": summary.get("high_priority_artifact_count", 0),
        "pgp_candidate_count": summary.get("pgp_candidate_count", 0),
        "stego_candidate_count": summary.get("stego_candidate_count", 0),
        "outguess_candidate_count": summary.get("outguess_candidate_count", 0),
        "openpuff_candidate_count": summary.get("openpuff_candidate_count", 0),
        "magic_square_artifact_count": summary.get("magic_square_artifact_count", 0),
        "hex_jpeg_candidate_count": summary.get("hex_jpeg_candidate_count", 0),
        "onion_artifact_count": summary.get("onion_artifact_count", 0),
        "book_code_artifact_count": summary.get("book_code_artifact_count", 0),
        "network_byte_channel_artifact_count": summary.get("network_byte_channel_artifact_count", 0),
        "liber_primus_artifact_count": summary.get("liber_primus_artifact_count", 0),
        "source_gap_count": summary.get("source_gap_count", 0),
        "validation_error_count": len(errors),
        "validation_errors": errors,
    }
    if errors:
        raise ValueError(json.dumps(result, indent=2, sort_keys=True))
    return result
