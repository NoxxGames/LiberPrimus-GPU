"""Stage 5AL private Deep Research export builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_yaml, resolve, write_json, write_yaml
from .models import (
    STAGE5AI_SUMMARY_PATH,
    STAGE5AJ_SUMMARY_PATH,
    STAGE5AK_SUMMARY_PATH,
    STAGE5AL_BUNDLE_ROOT,
    STAGE5AL_DEEP_RESEARCH_EXPORT_PATH,
    STAGE5AL_DEEP_RESEARCH_EXPORT_SUMMARY_PATH,
    STAGE5AL_FALSE_FLAGS,
    STAGE5AL_ID,
    STAGE5AL_OUTPUT_DIR,
    STAGE5AL_REPORTS,
    STAGE5AL_SOURCE_STAGE_ID,
    STAGE5AL_WEBSITE_INGEST_DIR,
)


def build_deep_research_export_stage5al(
    *,
    stage5ai_summary_path: Path = STAGE5AI_SUMMARY_PATH,
    stage5aj_summary_path: Path = STAGE5AJ_SUMMARY_PATH,
    stage5ak_summary_path: Path = STAGE5AK_SUMMARY_PATH,
    website_ingest_dir: Path = STAGE5AL_WEBSITE_INGEST_DIR,
    bundle_root: Path = STAGE5AL_BUNDLE_ROOT,
    results_dir: Path = STAGE5AL_OUTPUT_DIR,
    export_out: Path = STAGE5AL_DEEP_RESEARCH_EXPORT_PATH,
    summary_out: Path = STAGE5AL_DEEP_RESEARCH_EXPORT_SUMMARY_PATH,
) -> dict[str, Any]:
    """Build committed Deep Research export metadata and ignored private package files."""

    stage5ai = read_yaml(stage5ai_summary_path)
    stage5aj = read_yaml(stage5aj_summary_path)
    stage5ak = read_yaml(stage5ak_summary_path)
    ingest = _load_ingest(website_ingest_dir)
    bundles = ingest["bundles"].get("records", [])
    sources = ingest["source_cards"].get("records", [])
    claims = ingest["claims"].get("records", [])
    missing = ingest["missing"].get("records", [])
    gates = ingest["gates"].get("records", [])

    root = resolve(bundle_root)
    root.mkdir(parents=True, exist_ok=True)
    (root / ".gitkeep").touch()
    result_root = resolve(results_dir)
    result_root.mkdir(parents=True, exist_ok=True)

    export = {
        "record_type": "stage5al_deep_research_export",
        "schema": "schemas/website-ingest/deep-research-export-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "input_material_scope": [
            "Stage 5AI curated bundle metadata",
            "Stage 5AJ UsefulFilesAndIdeas metadata",
            "Stage 5AK community-facts claim metadata",
            "Stage 5AL website-ingest publication gates",
        ],
        "relative_path_or_ref": "research-inputs/stage5al/deep_research_master_context.md",
        "bundle_order": [
            {
                "bundle_id": record["bundle_id"],
                "title": record["title"],
                "relative_path_or_ref": record["relative_path_or_ref"],
                "private_deep_research_allowed": True,
                "website_publication_allowed": False,
            }
            for record in bundles
        ],
        "source_card_count": len(sources),
        "content_index_count": ingest["content"].get("record_count", 0),
        "claim_record_count": len(claims),
        "missing_source_count": len(missing),
        "publication_gate_count": len(gates),
        "private_review_blocked_paths": [
            "research-inputs/stage5ai/**",
            "research-inputs/stage5aj/**",
            "research-inputs/stage5ak/**",
            "research-inputs/stage5al/**",
            "third_party/**",
        ],
        "do_not_assume_summary": _do_not_assume_summary(),
        "known_questions_summary": _known_questions_summary(missing),
        "recommended_citation_policy": "Cite source_id, stage record path, publication gate, and source-lock status; do not cite raw ignored bodies.",
        "recommended_first_report_prompt_title": "Stage 5AM - Deep Research source inventory and reliability prompt",
        "what_not_to_analyze_yet": [
            "Do not perform OCR, image interpretation, stego/audio extraction, CUDA execution, or scored experiments.",
            "Do not treat private community claims as verified facts or solve evidence.",
            "Do not publish raw third-party files or generated extract bodies.",
        ],
        "stage5ai_consumed": stage5ai.get("status") == "complete",
        "stage5aj_consumed": stage5aj.get("status") == "complete",
        "stage5ak_consumed": stage5ak.get("status") == "complete",
        "deep_research_export_ready": True,
        "private_deep_research_allowed": True,
        "website_publication_allowed": False,
        "raw_content_publication_allowed": False,
        "generated_extract_publication_allowed": False,
        **STAGE5AL_FALSE_FLAGS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    summary = {
        "record_type": "stage5al_deep_research_export_summary",
        "schema": "schemas/website-ingest/stage5al-summary-v0.schema.json",
        "stage_id": STAGE5AL_ID,
        "status": "complete",
        "source_stage_id": STAGE5AL_SOURCE_STAGE_ID,
        "deep_research_export_ready": True,
        "bundle_count": len(bundles),
        "source_card_count": len(sources),
        "content_index_count": ingest["content"].get("record_count", 0),
        "claim_record_count": len(claims),
        "missing_source_count": len(missing),
        "do_not_assume_count": len(export["do_not_assume_summary"]),
        "known_questions_count": len(export["known_questions_summary"]),
        "recommended_first_report_prompt_title": export["recommended_first_report_prompt_title"],
        "private_generated_body_status": "ignored_not_committed",
        "public_website_ready_count": 0,
        **STAGE5AL_FALSE_FLAGS,
        "new_cuda_kernels_added": 0,
        "no_solve_claim": True,
    }
    _write_private_export_files(root, export, ingest)
    write_yaml(export_out, export)
    write_yaml(summary_out, summary)
    write_yaml(resolve(website_ingest_dir) / "deep-research-export.yaml", export)
    write_json(resolve(website_ingest_dir) / "deep-research-export.json", export)
    write_json(result_root / STAGE5AL_REPORTS["deep_research_export"], export)
    return {"export": export, "summary": summary}


def _load_ingest(website_ingest_dir: Path) -> dict[str, dict[str, Any]]:
    root = resolve(website_ingest_dir)
    return {
        "bundles": read_yaml(root / "research-bundles.yaml"),
        "source_cards": read_yaml(root / "source-cards.yaml"),
        "content": read_yaml(root / "content-index.yaml"),
        "claims": read_yaml(root / "community-claims.yaml"),
        "missing": read_yaml(root / "missing-sources.yaml"),
        "gates": read_yaml(root / "publication-gates.yaml"),
        "summary": read_yaml(root / "summary.yaml"),
    }


def _write_private_export_files(root: Path, export: dict[str, Any], ingest: dict[str, dict[str, Any]]) -> None:
    write_text(
        root / "deep_research_master_context.md",
        "\n".join(
            [
                "# Stage 5AL Private Deep Research Context",
                "",
                "Use the Stage 5AL website-ingest metadata package and publication gates.",
                "Do not read raw third_party files unless a future prompt explicitly allows it.",
                f"Recommended first report: {export['recommended_first_report_prompt_title']}.",
                "",
            ]
        ),
    )
    write_json(root / "deep_research_source_inventory.json", ingest["source_cards"])
    write_json(root / "deep_research_bundle_index.json", ingest["bundles"])
    write_json(root / "deep_research_claim_index.json", ingest["claims"])
    write_json(root / "deep_research_publication_gates.json", ingest["gates"])
    write_json(root / "deep_research_missing_sources.json", ingest["missing"])
    write_text(root / "do_not_assume_global.md", "\n".join(f"- {item}" for item in export["do_not_assume_summary"]) + "\n")
    write_text(root / "known_questions_global.md", "\n".join(f"- {item}" for item in export["known_questions_summary"]) + "\n")
    write_text(root / "citation_policy.md", export["recommended_citation_policy"] + "\n")
    write_text(
        root / "recommended_report_sequence.md",
        "\n".join(
            [
                "# Recommended Report Sequence",
                "",
                "1. Stage 5AM - Deep Research source inventory and reliability prompt.",
                "2. Publication-gate review only after private reliability triage.",
                "3. No scored experiments, CUDA, OCR, stego/audio, or hypothesis execution from this export.",
                "",
            ]
        ),
    )


def write_text(path: Path, text: str) -> None:
    target = resolve(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")


def _do_not_assume_summary() -> list[str]:
    return [
        "Metadata-only website ingest is not public publication.",
        "Private Deep Research readiness is not source truth or solve evidence.",
        "Community claims require source locks, transcript policy, coordinate policy, and null controls before tests.",
        "Raw third-party files and generated extract bodies remain ignored and uncommitted.",
        "No CUDA, benchmarks, scored experiments, OCR, AI/ML interpretation, image forensics, or stego/audio execution occurred.",
    ]


def _known_questions_summary(missing: list[dict[str, Any]]) -> list[str]:
    questions = [
        "Which Stage 5AI/5AJ/5AK source cards are reliable enough for future public metadata display?",
        "Which missing source records block reliability review?",
        "Which community number facts are post-hoc and need null-control framing?",
    ]
    priority_missing = [record["source_id"] for record in missing[:5] if record.get("source_id")]
    if priority_missing:
        questions.append("Prioritise missing-source reliability review for: " + ", ".join(priority_missing))
    return questions
