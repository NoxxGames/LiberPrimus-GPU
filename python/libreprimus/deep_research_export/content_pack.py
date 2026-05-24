"""Build the Stage 5AN private Deep Research content pack."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Any

from .file_selection import sanitize_text, select_research_input_files, slugify
from .hashing import dir_size_bytes, file_count, sha256_file
from .inputs import ensure_clean_dir, load_website_ingest, records, repo_relative, resolve, write_json, write_jsonl, write_yaml
from .models import (
    CONTENT_PACK_ROOT,
    FALSE_GUARDRAILS,
    METADATA_SITE_ROOT,
    PRIVATE_CONTENT_MANIFEST_URL,
    PRIVATE_CONTENT_URL,
    STAGE5AM_COMMIT,
    STAGE_ID,
    WEBSITE_INGEST_DIR,
)
from .publication_gates import build_publication_gate_audit
from .safe_extracts import generate_safe_extracts, write_redaction_log


def build_content_pack(
    *,
    metadata_site_root: Path = METADATA_SITE_ROOT,
    website_ingest_dir: Path = WEBSITE_INGEST_DIR,
    research_input_roots: list[Path],
    safe_local_source_roots: list[Path],
    out_root: Path = CONTENT_PACK_ROOT,
    policy_out: Path,
    inputs_out: Path,
    manifest_summary_out: Path,
    file_selection_summary_out: Path,
    publication_gate_audit_out: Path,
) -> dict[str, Any]:
    """Build ignored private pack files and committed compact records."""

    pack_root = ensure_clean_dir(out_root)
    (pack_root / ".gitkeep").touch()
    files_root = pack_root / "files"
    metadata_root = pack_root / "metadata"
    safe_extract_root = pack_root / "safe-extracts"
    files_root.mkdir(parents=True, exist_ok=True)
    metadata_root.mkdir(parents=True, exist_ok=True)

    ingest = load_website_ingest(website_ingest_dir)
    bundle_records = records(ingest, "bundles")
    source_records = records(ingest, "source_cards")
    content_records = records(ingest, "content")
    claim_records = records(ingest, "claims")
    gate_records = records(ingest, "publication_gates")
    selected, excluded = select_research_input_files(research_input_roots)
    safe_extracts, safe_extract_findings = generate_safe_extracts(safe_local_source_roots, safe_extract_root)
    excluded.extend(safe_extract_findings)

    metadata_files = _write_metadata_files(metadata_root, ingest)
    included_files: list[dict[str, Any]] = []
    redaction_records: list[dict[str, str]] = []
    lookup = _content_lookup(content_records)
    for item in selected:
        source_path = Path(item["source_path"])
        source = resolve(source_path)
        try:
            relative_input = source_path.relative_to("research-inputs")
        except ValueError:
            relative_input = Path(slugify(item["source_path"])).with_suffix(source_path.suffix)
        destination = files_root / "research-inputs" / relative_input
        findings = _copy_text_file(source, destination)
        redaction_records.extend({"path": repo_relative(destination), "finding": finding} for finding in findings)
        included_files.append(
            _included_file_record(
                path=destination,
                pack_root=pack_root,
                source_path=item["source_path"],
                metadata=lookup.get(item["source_path"], {}),
                defaults=item,
            )
        )
    for item in safe_extracts:
        source = resolve(Path(item["source_path"]))
        destination = files_root / "safe-extracts" / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        included_files.append(
            _included_file_record(
                path=destination,
                pack_root=pack_root,
                source_path=item["source_path"],
                metadata={},
                defaults=item,
            )
        )
    for path in metadata_files:
        included_files.append(
            _included_file_record(
                path=path,
                pack_root=pack_root,
                source_path=repo_relative(path),
                metadata={},
                defaults={
                    "path_kind": "committed_metadata_copy",
                    "publication_status": "private_deep_research_only",
                    "review_status": "review_required",
                    "raw_source_origin": "stage5al_committed_metadata",
                    "content_kind": "metadata_json",
                },
            )
        )

    write_redaction_log(pack_root / "redaction-log.jsonl", redaction_records)
    write_jsonl(pack_root / "excluded-files.jsonl", excluded)
    manifest = _sanitize_payload(
        _pack_manifest(
            pack_root=pack_root,
            included_files=included_files,
            bundle_records=bundle_records,
            source_records=source_records,
            content_records=content_records,
            claim_records=claim_records,
            gate_records=gate_records,
        )
    )
    write_yaml(pack_root / "deep-research-content-pack-stage5an-manifest.yaml", manifest)
    write_json(pack_root / "deep-research-content-pack-stage5an-manifest.json", manifest)
    hashes = _hash_records(pack_root)
    write_jsonl(pack_root / "deep-research-content-pack-stage5an-hashes.jsonl", hashes)
    _write_readme(pack_root)
    zip_path = _zip_pack(pack_root)
    manifest["content_pack_zip_path"] = repo_relative(zip_path)
    manifest["content_pack_zip_sha256"] = sha256_file(zip_path)
    manifest = _sanitize_payload(manifest)
    write_yaml(pack_root / "deep-research-content-pack-stage5an-manifest.yaml", manifest)
    write_json(pack_root / "deep-research-content-pack-stage5an-manifest.json", manifest)

    status_counts = _status_counts(included_files)
    policy = _policy_record()
    inputs = _inputs_record(
        metadata_site_root=metadata_site_root,
        website_ingest_dir=website_ingest_dir,
        research_input_roots=research_input_roots,
        safe_local_source_roots=safe_local_source_roots,
        bundle_count=len(bundle_records),
        source_count=len(source_records),
        content_count=len(content_records),
        claim_count=len(claim_records),
    )
    file_selection = {
        "record_type": "stage5an_file_selection_summary",
        "schema": "schemas/deep-research-export/file-selection-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5al",
        "selected_file_count": len(selected),
        "safe_extracts_generated_count": len(safe_extracts),
        "metadata_file_count": len(metadata_files),
        "excluded_raw_third_party_count": len([record for record in excluded if "raw" in record.get("reason", "")]),
        "excluded_forbidden_file_count": len([record for record in excluded if "forbidden" in record.get("reason", "")]),
        "excluded_file_count": len(excluded),
        "raw_third_party_files_included": False,
        "raw_archives_included": False,
        "raw_workbooks_included": False,
        "raw_images_included": False,
        "raw_pdfs_docx_included": False,
        "raw_audio_video_included": False,
        "solve_claim": False,
    }
    audit = build_publication_gate_audit(gate_records=gate_records, included_files=included_files, excluded_records=excluded)
    summary = {
        "record_type": "stage5an_content_pack_manifest_summary",
        "schema": "schemas/deep-research-export/content-pack-manifest-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "content_pack_generated": True,
        "content_pack_path": repo_relative(pack_root),
        "content_pack_zip_created": zip_path.exists(),
        "content_pack_zip_path": repo_relative(zip_path),
        "content_pack_file_count": file_count(pack_root),
        "content_pack_size_bytes": dir_size_bytes(pack_root),
        "included_bundle_count": len(bundle_records),
        "included_source_count": len(source_records),
        "included_claim_count": len(claim_records),
        "included_content_record_count": len(content_records),
        "included_private_extract_count": len(selected),
        "included_metadata_file_count": len(metadata_files),
        "safe_extracts_generated_count": len(safe_extracts),
        "publication_gate_records": len(gate_records),
        "private_deep_research_only_count": status_counts.get("private_deep_research_only", 0),
        "generated_extract_review_required_count": status_counts.get("generated_extract_review_required", 0),
        "blocked_private_or_sensitive_count": status_counts.get("blocked_private_or_sensitive", 0),
        "raw_source_never_publish_count": status_counts.get("raw_source_never_publish", 0),
        "public_website_ready_count": status_counts.get("public_website_ready", 0),
        "raw_third_party_files_included": False,
        "included_files": included_files,
        "solve_claim": False,
    }
    write_yaml(policy_out, policy)
    write_yaml(inputs_out, inputs)
    write_yaml(manifest_summary_out, summary)
    write_yaml(file_selection_summary_out, file_selection)
    write_yaml(publication_gate_audit_out, audit)
    return {
        "manifest": manifest,
        "summary": summary,
        "file_selection": file_selection,
        "publication_gate_audit": audit,
    }


def _write_metadata_files(metadata_root: Path, ingest: dict[str, Any]) -> list[Path]:
    files = {
        "source-cards.json": ingest["source_cards"],
        "content-index.json": ingest["content"],
        "claim-index.json": ingest["claims"],
        "research-bundles.json": ingest["bundles"],
        "publication-gates.json": ingest["publication_gates"],
        "missing-sources.json": ingest["missing_sources"],
        "deep-research-export.json": ingest["deep_research_export"],
    }
    written: list[Path] = []
    for name, payload in files.items():
        path = metadata_root / name
        write_json(path, _sanitize_payload(payload))
        written.append(path)
    return written


def _copy_text_file(source: Path, destination: Path) -> list[str]:
    text = source.read_text(encoding="utf-8", errors="replace")
    sanitized, findings = sanitize_text(text)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(sanitized, encoding="utf-8")
    return findings


def _content_lookup(content_records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        str(record.get("relative_path_or_ref", "")).split("#", 1)[0]: record
        for record in content_records
        if record.get("relative_path_or_ref")
    }


def _included_file_record(
    *,
    path: Path,
    pack_root: Path,
    source_path: str,
    metadata: dict[str, Any],
    defaults: dict[str, str],
) -> dict[str, Any]:
    rel = path.relative_to(pack_root).as_posix()
    source_id = metadata.get("source_id") or defaults.get("source_id") or "stage5an-private-content"
    bundle_id = metadata.get("bundle_id") or defaults.get("bundle_id") or "stage5an-private-content"
    publication_status = metadata.get("publication_status") or defaults.get("publication_status", "private_deep_research_only")
    return {
        "file_id": slugify(rel),
        "relative_path": rel,
        "relative_url": rel,
        "source_path": sanitize_text(source_path)[0],
        "source_id": source_id,
        "bundle_id": bundle_id,
        "content_kind": metadata.get("content_kind") or defaults.get("content_kind") or path.suffix.lower().lstrip("."),
        "sha256": sha256_file(path),
        "size_bytes": path.stat().st_size,
        "publication_status": publication_status,
        "public_website_publication_allowed": False,
        "review_status": metadata.get("review_status") or defaults.get("review_status", "review_required"),
        "path_kind": defaults.get("path_kind", metadata.get("path_kind", "generated_private_research_input")),
        "raw_source_origin": defaults.get("raw_source_origin", "generated_private_research_input"),
        "solve_claim": False,
    }


def _pack_manifest(
    *,
    pack_root: Path,
    included_files: list[dict[str, Any]],
    bundle_records: list[dict[str, Any]],
    source_records: list[dict[str, Any]],
    content_records: list[dict[str, Any]],
    claim_records: list[dict[str, Any]],
    gate_records: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "record_type": "stage5an_content_pack_manifest",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "stage5am_commit": STAGE5AM_COMMIT,
        "metadata_site_url": "http://liberprimus-gpu-data.info/index.html",
        "private_content_expected_url": PRIVATE_CONTENT_URL,
        "private_content_manifest_url": PRIVATE_CONTENT_MANIFEST_URL,
        "content_pack_path": repo_relative(pack_root),
        "included_files": included_files,
        "included_file_count": len(included_files),
        "included_bundle_count": len(bundle_records),
        "included_source_count": len(source_records),
        "included_content_record_count": len(content_records),
        "included_claim_count": len(claim_records),
        "publication_gate_records": len(gate_records),
        "raw_third_party_files_included": False,
        "raw_archives_included": False,
        "raw_workbooks_included": False,
        "raw_images_included": False,
        "raw_pdfs_docx_included": False,
        "raw_audio_video_included": False,
        "solve_claim": False,
    }


def _hash_records(pack_root: Path) -> list[dict[str, Any]]:
    records_out = []
    for path in sorted(pack_root.rglob("*")):
        if path.is_file() and path.name != "deep-research-content-pack-stage5an.zip":
            records_out.append(
                {
                    "path": path.relative_to(pack_root).as_posix(),
                    "sha256": sha256_file(path),
                    "size_bytes": path.stat().st_size,
                }
            )
    return records_out


def _write_readme(pack_root: Path) -> None:
    (pack_root / "README.md").write_text(
        "\n".join(
            [
                "# Stage 5AN Private Deep Research Content Pack",
                "",
                "PRIVATE DEEP RESEARCH CONTENT LIBRARY.",
                "Review-gated. Not public evidence. No solve claims.",
                "Do not mirror publicly without manual review.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _zip_pack(pack_root: Path) -> Path:
    zip_path = pack_root / "deep-research-content-pack-stage5an.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(pack_root.rglob("*")):
            if path.is_file() and path != zip_path:
                archive.write(path, path.relative_to(pack_root).as_posix())
    return zip_path


def _policy_record() -> dict[str, Any]:
    return {
        "record_type": "stage5an_content_pack_policy",
        "schema": "schemas/deep-research-export/content-pack-policy-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "metadata_only_policy": False,
        "private_deep_research_content_allowed": True,
        "public_website_publication_allowed": False,
        "raw_third_party_files_included_by_default": False,
        "safe_extracts_allowed": True,
        "allowed_private_extensions": sorted([".csv", ".html", ".json", ".jsonl", ".md", ".tsv", ".txt", ".yaml", ".yml"]),
        "excluded_raw_extensions": sorted([".7z", ".avi", ".db", ".docx", ".gif", ".jpg", ".jpeg", ".mp3", ".mp4", ".pdf", ".png", ".rar", ".sqlite", ".sqlite3", ".tar", ".webp", ".xls", ".xlsx", ".zip"]),
        "access_control_recommended": True,
        "robots_noindex_not_security": True,
        **FALSE_GUARDRAILS,
        "new_cuda_kernels_added": 0,
    }


def _inputs_record(
    *,
    metadata_site_root: Path,
    website_ingest_dir: Path,
    research_input_roots: list[Path],
    safe_local_source_roots: list[Path],
    bundle_count: int,
    source_count: int,
    content_count: int,
    claim_count: int,
) -> dict[str, Any]:
    return {
        "record_type": "stage5an_content_pack_inputs",
        "schema": "schemas/deep-research-export/content-pack-inputs-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "metadata_site_root": repo_relative(metadata_site_root),
        "website_ingest_dir": repo_relative(website_ingest_dir),
        "research_input_roots": [repo_relative(path) for path in research_input_roots],
        "safe_local_source_roots": [repo_relative(path) for path in safe_local_source_roots],
        "source_card_count": source_count,
        "content_record_count": content_count,
        "claim_record_count": claim_count,
        "bundle_count": bundle_count,
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "solve_claim": False,
    }


def _status_counts(records_in: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records_in:
        status = str(record.get("publication_status", "unknown"))
        counts[status] = counts.get(status, 0) + 1
    return counts


def _sanitize_payload(payload: Any) -> Any:
    if isinstance(payload, dict):
        return {str(key): _sanitize_payload(value) for key, value in payload.items()}
    if isinstance(payload, list):
        return [_sanitize_payload(item) for item in payload]
    if isinstance(payload, str):
        return sanitize_text(payload)[0]
    return payload
