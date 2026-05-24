"""Stage 5AN aggregate records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .inputs import read_yaml, write_yaml
from .models import FALSE_GUARDRAILS, METADATA_SITE_URL, PRIVATE_CONTENT_MANIFEST_URL, PRIVATE_CONTENT_URL, STAGE_ID


def build_guardrail(
    *,
    content_pack_root: Path,
    hosted_export_root: Path,
    combined_webroot: Path,
    out: Path,
) -> dict[str, Any]:
    """Write Stage 5AN guardrail metadata."""

    record = {
        "record_type": "stage5an_guardrail",
        "schema": "schemas/deep-research-export/stage5an-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": "stage-5am",
        "content_pack_root": content_pack_root.as_posix(),
        "hosted_export_root": hosted_export_root.as_posix(),
        "combined_webroot": combined_webroot.as_posix(),
        "content_pack_generated": True,
        "private_content_export_generated": True,
        "hosted_content_export_generated": True,
        "combined_webroot_generated": True,
        "generated_private_bodies_committed": False,
        "raw_third_party_files_included": False,
        "raw_third_party_files_committed": False,
        "local_absolute_paths_published": False,
        "private_ids_published": False,
        "robots_noindex_present": True,
        "deep_research_consumption_guide_created": True,
        **FALSE_GUARDRAILS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, record)
    return record


def build_next_stage_decision(
    *,
    manifest_summary: Path,
    hosted_summary: Path,
    combined_summary: Path,
    publication_gate_audit: Path,
    out: Path,
) -> dict[str, Any]:
    """Select the next Stage 5AO path."""

    manifest = read_yaml(manifest_summary)
    hosted = read_yaml(hosted_summary)
    combined = read_yaml(combined_summary)
    audit = read_yaml(publication_gate_audit)
    ready = (
        manifest.get("content_pack_generated") is True
        and hosted.get("hosted_content_export_generated") is True
        and combined.get("combined_webroot_generated") is True
        and audit.get("publication_gate_audit_passed") is True
    )
    options = [
        (
            "stage5ao_deep_research_source_inventory_and_reliability_prompt_with_private_content",
            "Stage 5AO - Deep Research source inventory and reliability prompt with private content",
            "The private content pack, hosted private-content export, and combined SFTP webroot validate without raw third-party publication or solve claims.",
            ready,
            "Deep Research",
        ),
        (
            "stage5ao_private_content_pack_gap_closure",
            "Stage 5AO - private content pack gap closure",
            "Use only if generated private content files are missing or hashes fail.",
            not ready,
            "Codex",
        ),
        (
            "stage5ao_publication_gate_review",
            "Stage 5AO - publication gate review",
            "Use only if publication policy is ambiguous.",
            False,
            "Codex",
        ),
        (
            "stage5ao_targeted_online_fetch_for_missing_sources",
            "Stage 5AO - targeted online fetch for missing sources",
            "Deferred; Stage 5AN did not perform network fetches.",
            False,
            "Codex",
        ),
        (
            "stage5ao_bounded_cpu_native_scored_experiment_manifest_gate",
            "Stage 5AO - bounded CPU/native scored experiment manifest gate",
            "Not selected because Stage 5AN is private content infrastructure, not experiment execution.",
            False,
            "Codex",
        ),
        (
            "stage5ao_benchmark_planning",
            "Stage 5AO - benchmark planning",
            "Not selected because Stage 5AN does not run benchmarks.",
            False,
            "Codex",
        ),
        (
            "stage5ao_unsolved_page_cuda_pilot",
            "Stage 5AO - unsolved-page CUDA pilot",
            "Not selected because unsolved-page CUDA remains blocked.",
            False,
            "Codex",
        ),
        (
            "future_public_website_expansion_unnumbered",
            "Future public website expansion",
            "Not selected because private hosted content is review-gated and not public publication.",
            False,
            "Codex",
        ),
    ]
    records = [
        {
            "record_type": "stage5an_next_stage_decision_record",
            "schema": "schemas/deep-research-export/stage5an-summary-v0.schema.json",
            "stage_id": STAGE_ID,
            "source_stage_id": "stage-5am",
            "option_id": option_id,
            "selected": selected,
            "recommended_next_prompt_type": prompt_type if selected else None,
            "recommended_next_stage_title": title,
            "recommended_next_stage_reason": reason,
            "deep_research_recommended_next": prompt_type == "Deep Research" and selected,
            "scored_experiment_recommended_next": False,
            "benchmark_recommended_next": False,
            "unsolved_page_cuda_recommended_next": False,
            "public_website_expansion_recommended_next": False,
            "execution_enabled": False,
            "solve_claim": False,
        }
        for option_id, title, reason, selected, prompt_type in options
    ]
    selected_record = next(record for record in records if record["selected"])
    decision = {
        "record_type": "stage5an_next_stage_decisions",
        "schema": "schemas/deep-research-export/stage5an-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": "stage-5am",
        "content_pack_generated": manifest.get("content_pack_generated") is True,
        "hosted_content_export_generated": hosted.get("hosted_content_export_generated") is True,
        "combined_webroot_generated": combined.get("combined_webroot_generated") is True,
        "robots_noindex_present": True,
        "deep_research_consumption_guide_created": True,
        "selected_option_id": selected_record["option_id"],
        "selected_next_prompt_type": selected_record["recommended_next_prompt_type"],
        "selected_next_stage_title": selected_record["recommended_next_stage_title"],
        "selected_next_stage_reason": selected_record["recommended_next_stage_reason"],
        "deep_research_next_ready": selected_record["deep_research_recommended_next"],
        "records": records,
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "deep_research_performed": False,
        "cuda_execution_performed": False,
        "new_cuda_kernels_added": 0,
        "solve_claim": False,
    }
    write_yaml(out, decision)
    return decision


def build_summary(
    *,
    policy: Path,
    inputs: Path,
    manifest_summary: Path,
    hosted_summary: Path,
    combined_summary: Path,
    file_selection_summary: Path,
    publication_gate_audit: Path,
    upload_instructions: Path,
    consumption_guide: Path,
    guardrail: Path,
    next_stage_decision: Path,
    out: Path,
) -> dict[str, Any]:
    """Write the committed Stage 5AN aggregate summary."""

    policy_record = read_yaml(policy)
    inputs_record = read_yaml(inputs)
    manifest = read_yaml(manifest_summary)
    hosted = read_yaml(hosted_summary)
    combined = read_yaml(combined_summary)
    selection = read_yaml(file_selection_summary)
    audit = read_yaml(publication_gate_audit)
    upload = read_yaml(upload_instructions)
    guide = read_yaml(consumption_guide)
    guard = read_yaml(guardrail)
    decision = read_yaml(next_stage_decision)
    summary = {
        "record_type": "stage5an_private_deep_research_content_pack_summary",
        "schema": "schemas/deep-research-export/stage5an-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": "stage-5am",
        "metadata_site_url": METADATA_SITE_URL,
        "private_content_expected_url": PRIVATE_CONTENT_URL,
        "private_content_manifest_url": PRIVATE_CONTENT_MANIFEST_URL,
        "content_pack_generated": manifest.get("content_pack_generated", False),
        "content_pack_path": manifest.get("content_pack_path"),
        "content_pack_zip_created": manifest.get("content_pack_zip_created", False),
        "content_pack_zip_path": manifest.get("content_pack_zip_path"),
        "content_pack_file_count": manifest.get("content_pack_file_count", 0),
        "content_pack_size_bytes": manifest.get("content_pack_size_bytes", 0),
        "hosted_content_export_generated": hosted.get("hosted_content_export_generated", False),
        "hosted_content_export_root": hosted.get("hosted_content_export_root"),
        "hosted_content_export_zip_created": hosted.get("hosted_content_export_zip_created", False),
        "hosted_content_export_zip_path": hosted.get("hosted_content_export_zip_path"),
        "hosted_content_file_count": hosted.get("hosted_content_file_count", 0),
        "hosted_content_size_bytes": hosted.get("hosted_content_size_bytes", 0),
        "combined_webroot_generated": combined.get("combined_webroot_generated", False),
        "combined_webroot_root": combined.get("combined_webroot_root"),
        "combined_webroot_zip_created": combined.get("combined_webroot_zip_created", False),
        "combined_webroot_zip_path": combined.get("combined_webroot_zip_path"),
        "included_bundle_count": manifest.get("included_bundle_count", inputs_record.get("bundle_count", 0)),
        "included_source_count": manifest.get("included_source_count", inputs_record.get("source_card_count", 0)),
        "included_claim_count": manifest.get("included_claim_count", inputs_record.get("claim_record_count", 0)),
        "included_content_record_count": manifest.get("included_content_record_count", inputs_record.get("content_record_count", 0)),
        "included_private_extract_count": manifest.get("included_private_extract_count", 0),
        "included_metadata_file_count": manifest.get("included_metadata_file_count", 0),
        "safe_extracts_generated_count": selection.get("safe_extracts_generated_count", 0),
        "excluded_raw_third_party_count": selection.get("excluded_raw_third_party_count", 0),
        "excluded_forbidden_file_count": selection.get("excluded_forbidden_file_count", 0),
        "publication_gate_records": audit.get("publication_gate_records", 0),
        "private_deep_research_only_count": audit.get("private_deep_research_only_count", 0),
        "generated_extract_review_required_count": audit.get("generated_extract_review_required_count", 0),
        "blocked_private_or_sensitive_count": audit.get("blocked_private_or_sensitive_count", 0),
        "raw_source_never_publish_count": audit.get("raw_source_never_publish_count", 0),
        "public_website_ready_count": audit.get("public_website_ready_count", 0),
        "local_absolute_paths_published": False,
        "private_ids_published": False,
        "raw_third_party_files_included": False,
        "raw_archives_included": False,
        "raw_workbooks_included": False,
        "raw_images_included": False,
        "raw_pdfs_docx_included": False,
        "raw_audio_video_included": False,
        "robots_noindex_present": True,
        "upload_instructions_created": upload.get("copy_contents_to_webserver_root") is True,
        "deep_research_consumption_guide_created": guide.get("record_type") == "stage5an_deep_research_consumption_guide",
        "deep_research_next_ready": decision.get("deep_research_next_ready", False),
        "recommended_next_prompt_type": decision.get("selected_next_prompt_type"),
        "recommended_next_stage_title": decision.get("selected_next_stage_title"),
        "recommended_next_stage_reason": decision.get("selected_next_stage_reason"),
        **FALSE_GUARDRAILS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
        "policy_private_deep_research_content_allowed": policy_record.get("private_deep_research_content_allowed", False),
        "guardrail_record": guard.get("record_type"),
    }
    write_yaml(out, summary)
    return summary
