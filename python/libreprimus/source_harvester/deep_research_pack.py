"""Stage 5AI private Deep Research pack metadata."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .export import read_records, write_json, write_yaml
from .models import (
    RESEARCH_BUNDLE_PLAN_PATH,
    STAGE5AI_BUNDLE_ROOT,
    STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH,
    STAGE5AI_ID,
    STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
    STAGE5AI_OUTPUT_DIR,
    STAGE5AI_REPORTS,
    STAGE5AI_SOURCE_STAGE_ID,
)


def build_deep_research_pack_index(
    *,
    bundle_root: Path = STAGE5AI_BUNDLE_ROOT,
    results_dir: Path = STAGE5AI_OUTPUT_DIR,
    out: Path = STAGE5AI_DEEP_RESEARCH_PACK_FORMAT_PATH,
    bundle_plan_path: Path = RESEARCH_BUNDLE_PLAN_PATH,
) -> dict[str, Any]:
    """Build a deterministic private Deep Research pack index."""

    plan = read_records(bundle_plan_path)
    packs = []
    for bundle in sorted(plan, key=lambda item: item.get("recommended_deep_research_order", 999)):
        bundle_id = bundle["bundle_id"]
        bundle_dir = bundle_root / bundle_id
        packs.append(
            {
                "bundle_id": bundle_id,
                "title": bundle["title"],
                "sequential_order": bundle.get("recommended_deep_research_order"),
                "manifest_path": f"{bundle_id}/manifest.yaml",
                "deep_research_context_path": f"{bundle_id}/deep_research_context.md",
                "known_questions_path": f"{bundle_id}/known_questions.md",
                "do_not_assume_path": f"{bundle_id}/do_not_assume.md",
                "manifest_exists": (bundle_dir / "manifest.yaml").exists(),
                "known_questions_exists": (bundle_dir / "known_questions.md").exists(),
                "do_not_assume_exists": (bundle_dir / "do_not_assume.md").exists(),
                "private_deep_research_allowed": True,
                "public_website_ready": False,
                "solve_claim": False,
            }
        )
    index = {
        "record_type": "stage5ai_deep_research_pack_index",
        "schema": "schemas/source-harvester/deep-research-pack-format-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "deep_research_pack_records": len(packs),
        "packs": packs,
        "website_expansion_performed": False,
        "solve_claim": False,
    }
    write_json(bundle_root / "deep_research_pack_index.json", index)
    write_json(results_dir / STAGE5AI_REPORTS["deep_research_pack"], index)
    summary = {
        "record_type": "stage5ai_deep_research_pack_format",
        "schema": "schemas/source-harvester/deep-research-pack-format-v0.schema.json",
        "stage_id": STAGE5AI_ID,
        "source_stage_id": STAGE5AI_SOURCE_STAGE_ID,
        "local_inventory_stage_id": STAGE5AI_LOCAL_INVENTORY_STAGE_ID,
        "deep_research_pack_records": len(packs),
        "sequential_order_present": all(pack["sequential_order"] for pack in packs),
        "do_not_assume_files_present": all(pack["do_not_assume_exists"] for pack in packs),
        "known_questions_files_present": all(pack["known_questions_exists"] for pack in packs),
        "private_deep_research_allowed": True,
        "website_expansion_performed": False,
        "solve_claim": False,
    }
    write_yaml(out, summary)
    return {**summary, "packs": packs}
