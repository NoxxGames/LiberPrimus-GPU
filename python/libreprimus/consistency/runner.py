"""Consistency suite runner."""

from __future__ import annotations

from pathlib import Path

from libreprimus.consistency.check_docs import check_docs_consistency
from libreprimus.consistency.check_ignored_outputs import check_ignored_output_consistency
from libreprimus.consistency.check_manifests import check_manifest_consistency
from libreprimus.consistency.check_registry import check_registry_consistency
from libreprimus.consistency.check_result_store import check_result_store_consistency
from libreprimus.consistency.check_schemas import check_schema_consistency
from libreprimus.consistency.check_archive_visual import check_archive_visual_consistency
from libreprimus.consistency.check_hash_preimage import check_hash_preimage_consistency
from libreprimus.consistency.check_image_analysis import check_image_analysis_consistency
from libreprimus.consistency.check_image_transforms import check_image_transform_consistency
from libreprimus.consistency.check_discord_ingestion import check_discord_ingestion_consistency
from libreprimus.consistency.check_discord_promotion import check_discord_promotion_consistency
from libreprimus.consistency.check_discord_review import check_discord_review_consistency
from libreprimus.consistency.check_discord_leads import check_discord_leads_consistency
from libreprimus.consistency.export import write_summary
from libreprimus.consistency.models import ConsistencyCheckResult, ConsistencyCheckSuiteResult

CHECK_GROUPS = {
    "registry": check_registry_consistency,
    "manifests": check_manifest_consistency,
    "schemas": check_schema_consistency,
    "docs": check_docs_consistency,
    "ignored_outputs": check_ignored_output_consistency,
    "result_store": check_result_store_consistency,
    "archive_visual": check_archive_visual_consistency,
    "hash_preimage": check_hash_preimage_consistency,
    "image_analysis": check_image_analysis_consistency,
    "image_transforms": check_image_transform_consistency,
    "discord_ingestion": check_discord_ingestion_consistency,
    "discord_promotion": check_discord_promotion_consistency,
    "discord_review": check_discord_review_consistency,
    "discord_leads": check_discord_leads_consistency,
}


def run_consistency_suite(
    groups: list[str] | None = None,
    *,
    out: Path | None = None,
    allow_missing_generated: bool = True,
) -> ConsistencyCheckSuiteResult:
    selected = groups or list(CHECK_GROUPS)
    results: list[ConsistencyCheckResult] = []
    for group in selected:
        if group == "result_store":
            results.extend(
                check_result_store_consistency(allow_missing_generated=allow_missing_generated)
            )
            continue
        results.extend(CHECK_GROUPS[group]())
    suite = ConsistencyCheckSuiteResult("stage2d-consistency-suite", results)
    if out is not None:
        write_summary(out, suite)
    return suite
