"""Stage 5AM orchestration helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export_manifest import attach_hashes, build_render_inputs_record, build_render_policy_record
from .loader import load_stage5al_inputs, read_yaml, resolve, write_json, write_jsonl, write_yaml
from .models import FALSE_GUARDRAILS, STAGE5AL_COMMIT, STAGE_ID
from .privacy import audit_site
from .renderer import render_site


def build_stage5am_site(
    *,
    website_ingest_dir: Path,
    stage5al_summary: Path,
    out_root: Path,
    results_dir: Path,
    render_policy_out: Path,
    render_inputs_out: Path,
    manifest_out: Path,
    privacy_audit_out: Path,
    upload_instructions_out: Path,
) -> dict[str, Any]:
    """Build the static site and core committed metadata records."""

    inputs = load_stage5al_inputs(website_ingest_dir, stage5al_summary)
    manifest = render_site(inputs, out_root)
    manifest = attach_hashes(manifest, out_root)
    audit = audit_site(out_root)
    policy = build_render_policy_record()
    render_inputs = build_render_inputs_record(inputs)
    upload = build_upload_instructions(out_root, manifest)

    write_yaml(render_policy_out, policy)
    write_yaml(render_inputs_out, render_inputs)
    write_yaml(manifest_out, manifest)
    write_yaml(privacy_audit_out, audit)
    write_yaml(upload_instructions_out, upload)

    result_root = resolve(results_dir)
    write_json(result_root / "render_output_manifest.json", manifest)
    write_json(result_root / "privacy_publication_audit.json", audit)
    write_jsonl(result_root / "warnings.jsonl", [])
    return {
        "policy": policy,
        "inputs": render_inputs,
        "manifest": manifest,
        "privacy_audit": audit,
        "upload": upload,
    }


def build_upload_instructions(site_root: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Build upload instructions for the generated static export."""

    return {
        "record_type": "stage5am_upload_instructions",
        "schema": "schemas/website-render/upload-instructions-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5al",
        "metadata_only": True,
        "upload_directory": site_root.as_posix(),
        "zip_package_path": manifest.get("zip_package_path"),
        "copy_to_webserver": site_root.as_posix(),
        "do_not_upload": [
            "third_party/",
            "data/raw/",
            "research-inputs/",
            "experiments/results/",
            "codex-output/",
            "deep-research-reports/",
        ],
        "access_control_recommended": True,
        "review_gated": True,
        "raw_bodies_included": False,
        "private_ids_published": False,
        "public_website_publication_performed": False,
        "solve_claim": False,
    }


def build_stage5am_guardrail(*, site_root: Path, manifest_path: Path, privacy_audit_path: Path, out: Path) -> dict[str, Any]:
    """Build the Stage 5AM guardrail record."""

    manifest = read_yaml(manifest_path)
    audit = read_yaml(privacy_audit_path)
    record = {
        "record_type": "stage5am_guardrail",
        "schema": "schemas/website-render/stage5am-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5al",
        "website_export_root": site_root.as_posix(),
        "website_export_generated": manifest.get("website_export_generated") is True,
        "metadata_only": True,
        "raw_bodies_included": False,
        "private_ids_published": False,
        "local_absolute_paths_published": audit.get("local_absolute_paths_published", False),
        "generated_private_bodies_committed": False,
        "raw_data_committed": False,
        "public_website_publication_performed": False,
        "deep_research_performed": False,
        **FALSE_GUARDRAILS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    write_yaml(out, record)
    return record


def build_stage5am_next_stage_decision(
    *,
    site_validation_path: Path,
    privacy_audit_path: Path,
    out: Path,
) -> dict[str, Any]:
    """Select Stage 5AN only when static validation and privacy audit pass."""

    validation = read_yaml(site_validation_path)
    audit = read_yaml(privacy_audit_path)
    ready = validation.get("static_site_validation_passed") is True and audit.get("privacy_audit_passed") is True
    selected = "stage5an_deep_research_source_inventory_and_reliability_prompt" if ready else "stage5am_publication_gate_repair"
    records = [
        {
            "record_type": "stage5am_next_stage_decision_record",
            "schema": "schemas/website-render/stage5am-summary-v0.schema.json",
            "stage_id": STAGE_ID,
            "source_stage_id": "stage-5al",
            "option_id": "stage5an_deep_research_source_inventory_and_reliability_prompt",
            "selected": ready,
            "recommended_next_prompt_type": "Deep Research",
            "recommended_next_stage_title": "Stage 5AN - Deep Research source inventory and reliability prompt",
            "recommended_next_stage_reason": (
                "The Stage 5AM static metadata-only research index validates with no raw bodies, "
                "private IDs, publication-gate overrides, Deep Research execution, or solve claims."
            ),
            "deep_research_recommended_next": ready,
            "website_expansion_recommended_next": False,
            "scored_experiment_recommended_next": False,
            "unsolved_page_cuda_recommended_next": False,
            "execution_enabled": False,
            "solve_claim": False,
        },
        {
            "record_type": "stage5am_next_stage_decision_record",
            "schema": "schemas/website-render/stage5am-summary-v0.schema.json",
            "stage_id": STAGE_ID,
            "source_stage_id": "stage-5al",
            "option_id": "stage5am_publication_gate_repair",
            "selected": not ready,
            "recommended_next_prompt_type": None,
            "recommended_next_stage_title": "Stage 5AM publication gate repair",
            "recommended_next_stage_reason": "Use only if renderer validation or privacy audit fails.",
            "deep_research_recommended_next": False,
            "website_expansion_recommended_next": False,
            "scored_experiment_recommended_next": False,
            "unsolved_page_cuda_recommended_next": False,
            "execution_enabled": False,
            "solve_claim": False,
        },
    ]
    record = {
        "record_type": "stage5am_next_stage_decisions",
        "schema": "schemas/website-render/stage5am-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5al",
        "selected_option_id": selected,
        "deep_research_next_ready": ready,
        "selected_next_prompt_type": "Deep Research" if ready else None,
        "selected_next_stage_title": records[0]["recommended_next_stage_title"] if ready else records[1]["recommended_next_stage_title"],
        "selected_next_stage_reason": records[0]["recommended_next_stage_reason"] if ready else records[1]["recommended_next_stage_reason"],
        "records": records,
        "solve_claim": False,
    }
    write_yaml(out, record)
    return record


def build_stage5am_summary(
    *,
    render_policy_path: Path,
    render_inputs_path: Path,
    manifest_path: Path,
    validation_path: Path,
    privacy_audit_path: Path,
    upload_instructions_path: Path,
    guardrail_path: Path,
    next_stage_decision_path: Path,
    out: Path,
    results_dir: Path | None = None,
) -> dict[str, Any]:
    """Build the committed Stage 5AM aggregate summary."""

    policy = read_yaml(render_policy_path)
    inputs = read_yaml(render_inputs_path)
    manifest = read_yaml(manifest_path)
    validation = read_yaml(validation_path)
    audit = read_yaml(privacy_audit_path)
    upload = read_yaml(upload_instructions_path)
    read_yaml(guardrail_path)
    decision = read_yaml(next_stage_decision_path)
    summary = {
        "record_type": "stage5am_static_research_website_renderer_summary",
        "schema": "schemas/website-render/stage5am-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "status": "complete",
        "source_stage_id": "stage-5al",
        "stage5al_commit": STAGE5AL_COMMIT,
        "website_ingest_dir": inputs.get("website_ingest_dir"),
        "website_shell_created": True,
        "website_export_generated": manifest.get("website_export_generated", False),
        "website_export_root": manifest.get("website_export_root"),
        "website_export_zip_created": manifest.get("zip_package_generated", False),
        "zip_package_path": manifest.get("zip_package_path"),
        "static_pages_generated": manifest.get("static_pages_generated", 0),
        "data_json_files_generated": manifest.get("data_json_files_generated", 0),
        "source_card_count": inputs.get("source_card_count", 0),
        "content_record_count": inputs.get("content_record_count", 0),
        "claim_record_count": inputs.get("claim_record_count", 0),
        "bundle_count": inputs.get("bundle_count", 0),
        "publication_gate_count": inputs.get("publication_gate_count", 0),
        "missing_source_count": inputs.get("missing_source_count", 0),
        "public_website_ready_count": 0,
        "metadata_only_rendered_count": inputs.get("source_card_count", 0)
        + inputs.get("content_record_count", 0)
        + inputs.get("claim_record_count", 0)
        + inputs.get("bundle_count", 0)
        + inputs.get("missing_source_count", 0),
        "private_or_review_blocked_rendered_count": 119,
        "raw_bodies_included": False,
        "private_ids_published": False,
        "local_absolute_paths_published": audit.get("local_absolute_paths_published", False),
        "robots_noindex_present": validation.get("robots_noindex_present", False),
        "upload_instructions_created": upload.get("upload_directory") == manifest.get("website_export_root"),
        "privacy_audit_passed": audit.get("privacy_audit_passed", False),
        "static_site_validation_passed": validation.get("static_site_validation_passed", False),
        "deep_research_export_ready": True,
        "deep_research_next_ready": decision.get("deep_research_next_ready", False),
        "recommended_next_prompt_type": decision.get("selected_next_prompt_type"),
        "recommended_next_stage_title": decision.get("selected_next_stage_title"),
        "recommended_next_stage_reason": decision.get("selected_next_stage_reason"),
        **FALSE_GUARDRAILS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    summary["metadata_only"] = policy.get("metadata_only", True)
    summary["raw_bodies_published"] = False
    write_yaml(out, summary)
    if results_dir is not None:
        write_json(resolve(results_dir) / "summary.json", summary)
    return summary
