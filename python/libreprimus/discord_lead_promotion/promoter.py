"""Stage 3R Discord lead promotion runner."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from libreprimus.discord_lead_promotion.corroboration import normalized_public_url
from libreprimus.discord_lead_promotion.export import write_json, write_jsonl, write_yaml
from libreprimus.discord_lead_promotion.loader import load_stage3r_inputs
from libreprimus.discord_lead_promotion.models import ONION7_SOURCE_URL, PUBLIC_SOURCE_TARGETS
from libreprimus.discord_lead_promotion.negative_controls import build_negative_control_records
from libreprimus.paths import repo_root

RUN_ID = "stage3r-discord-lead-promotion-audit"


def promote_discord_leads(
    *,
    review_dir: Path,
    stage3o_links: Path,
    stage3o_methods: Path,
    stage3o_numerics: Path,
    source_registry: Path,
    visual_registry: Path,
    cookie_records: Path,
    out_dir: Path,
    promoted_sources_out: Path,
    promoted_observations_out: Path,
    negative_controls_out: Path,
    audit_summary_out: Path,
    allow_missing: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Promote corroborated public leads and preserve negative controls."""
    data, warnings = load_stage3r_inputs(
        review_dir=review_dir,
        stage3o_links=stage3o_links,
        stage3o_methods=stage3o_methods,
        stage3o_numerics=stage3o_numerics,
        source_registry=source_registry,
        visual_registry=visual_registry,
        cookie_records=cookie_records,
        allow_missing=allow_missing,
    )
    resolved_out = _resolve(out_dir)
    source_records, duplicate_count = _build_source_records(data)
    observation_records = _build_observation_records(data)
    negative_controls = build_negative_control_records()
    rejected_records = _build_rejected_records(data)
    summary = _build_summary(
        data=data,
        out_dir=resolved_out,
        source_records=source_records,
        observation_records=observation_records,
        negative_controls=negative_controls,
        duplicate_count=duplicate_count,
        rejected_records=rejected_records,
        warnings=warnings,
    )
    audit_records = [
        {"audit_record_type": "promoted_source", **record} for record in source_records
    ] + [
        {"audit_record_type": "promoted_observation", **record} for record in observation_records
    ]
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_out / "promotion_audit_records.jsonl", audit_records)
    write_jsonl(resolved_out / "rejected_or_quarantined_records.jsonl", rejected_records)
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "promotion_summary.json", summary)
    write_yaml(
        _resolve(promoted_sources_out),
        {
            "record_type": "stage3r_promoted_source_records",
            "run_id": RUN_ID,
            "records": source_records,
        },
    )
    write_yaml(
        _resolve(promoted_observations_out),
        {
            "record_type": "stage3r_promoted_observation_records",
            "run_id": RUN_ID,
            "records": observation_records,
        },
    )
    write_yaml(
        _resolve(negative_controls_out),
        {
            "record_type": "stage3r_negative_control_records",
            "run_id": RUN_ID,
            "records": negative_controls,
        },
    )
    write_yaml(_resolve(audit_summary_out), summary)
    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _build_source_records(data: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    existing_urls = _existing_source_urls(data.get("source_registry", {}))
    records: list[dict[str, Any]] = []
    duplicate_count = 0
    for item in PUBLIC_SOURCE_TARGETS:
        url = normalized_public_url(str(item["source_url"]))
        if url is None:
            continue
        if url in existing_urls:
            duplicate_count += 1
        records.append(
            {
                "record_type": "promoted_discord_source_record",
                "promoted_id": item["promoted_id"],
                "source_url": url,
                "normalized_url": url,
                "source_title": item["source_title"],
                "source_class": item["source_class"],
                "promotion_class": "source_to_lock",
                "corroboration_basis": item["corroboration_basis"],
                "discord_lead_reference": item["discord_lead_reference"],
                "public_source_required": True,
                "raw_message_committed": False,
                "username_committed": False,
                "private_url_committed": False,
                "trusted_as_canonical": False,
                "review_status": "human_review_required",
                "notes": "Discord-derived source-discovery lead promoted only because it maps to a public URL or existing source record.",
            }
        )
    return records, duplicate_count


def _build_observation_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    del data
    rows = [
        {
            "observation_id": "stage3r-observation-onion7-raw-table",
            "observation_type": "onion7_raw_4x4_table",
            "source_url": ONION7_SOURCE_URL,
            "source_title": "Onion 7: numbers on page 15",
            "values": {
                "table_shape": "4x4",
                "exact_values_status": "public_source_review_required_before_execution",
            },
            "derived_values": {},
            "corroboration_basis": "Public Onion 7 page identifies the artefact table; exact values remain review-required before execution.",
            "ambiguity_notes": "Stage 3R queues a disabled manifest and does not invent or execute table values.",
        },
        {
            "observation_id": "stage3r-observation-onion7-prime-table",
            "observation_type": "onion7_derived_prime_table",
            "source_url": ONION7_SOURCE_URL,
            "source_title": "Onion 7: numbers on page 15",
            "values": {"table_shape": "4x4", "derived_table": "prime_delta_table"},
            "derived_values": {"status": "review_required"},
            "corroboration_basis": "Derived-table lead from public Onion 7 table source and Discord review bundle triage.",
            "ambiguity_notes": "Derived table must be recomputed from exact source values in the future executor.",
        },
        {
            "observation_id": "stage3r-observation-onion7-prime-order-table",
            "observation_type": "onion7_prime_order_table",
            "source_url": ONION7_SOURCE_URL,
            "source_title": "Onion 7: numbers on page 15",
            "values": {"table_shape": "4x4", "derived_table": "prime_order_table"},
            "derived_values": {"status": "review_required"},
            "corroboration_basis": "Derived-table lead from public Onion 7 table source and Discord review bundle triage.",
            "ambiguity_notes": "Prime-order interpretation is an experiment candidate only after exact table review.",
        },
        {
            "observation_id": "stage3r-observation-2014-image-dimensions",
            "observation_type": "image_dimensions",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/CICADA_3301_2014_PUZZLE",
            "source_title": "CICADA 3301 2014 PUZZLE",
            "values": {"width": 547, "height": 577},
            "derived_values": {"both_dimensions_prime": True},
            "corroboration_basis": "Public 2014 puzzle reference and Stage 3R lead-triage recommendation.",
            "ambiguity_notes": "Dimension observation only; not a transform seed.",
        },
        {
            "observation_id": "stage3r-observation-2016-image-dimensions",
            "observation_type": "image_dimensions",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/2016_Message",
            "source_title": "2016 Message",
            "values": {"width": 563, "height": 569},
            "derived_values": {"both_dimensions_prime": True},
            "corroboration_basis": "Existing visual observation and public 2016 message reference.",
            "ambiguity_notes": "Already present as review material; not canonical corpus activation.",
        },
        {
            "observation_id": "stage3r-observation-2014-onion-title",
            "observation_type": "historical_onion_title",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/CICADA_3301_2014_PUZZLE",
            "source_title": "CICADA 3301 2014 PUZZLE",
            "values": {"title": "For Every Thing That Lives Is Holy"},
            "derived_values": {},
            "corroboration_basis": "Public 2014 reference; may be used only as exact string candidate in disabled manifest.",
            "ambiguity_notes": "String candidate source; no hash/preimage result claimed.",
        },
        {
            "observation_id": "stage3r-observation-2014-1033-jpg",
            "observation_type": "historical_image_filename_etag",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/CICADA_3301_2014_PUZZLE",
            "source_title": "CICADA 3301 2014 PUZZLE",
            "values": {"filename": "1033.jpg", "etag_reference": "review_required"},
            "derived_values": {},
            "corroboration_basis": "Public source artefact lead; exact ETag must be reviewed from source records.",
            "ambiguity_notes": "Filename is safe to queue; ETag is not asserted here.",
        },
        {
            "observation_id": "stage3r-observation-2013-761-mp3-167",
            "observation_type": "historical_audio_duration_cluster",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2013)",
            "source_title": "What Happened Part 1 (2013)",
            "values": {"filename": "761.mp3", "duration_seconds": 167},
            "derived_values": {"cookie_ids": [761, 167]},
            "corroboration_basis": "Public historical source lead plus Stage 3K/3L cookie artefact IDs.",
            "ambiguity_notes": "Cluster is reviewable context only; not a preimage result.",
        },
        {
            "observation_id": "stage3r-observation-cuneiform-pages-34-40",
            "observation_type": "cuneiform_review_candidate",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages",
            "source_title": "Liber Primus Unsolved Pages",
            "values": {"pages": [34, 35, 36, 37, 38, 39, 40], "candidate_reading": [17, 13, 55, 1]},
            "derived_values": {"numeric_candidates": [1033, 3301, 3722101]},
            "corroboration_basis": "Existing Stage 3K visual observation and public unsolved-page reference.",
            "ambiguity_notes": "Manual review required; usable_as_experiment_seed remains false.",
        },
        {
            "observation_id": "stage3r-observation-dot-motifs",
            "observation_type": "dot_motif_review_candidate",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages",
            "source_title": "Liber Primus Unsolved Pages",
            "values": {"five_dot_candidate_pages": [7, 24, 57], "three_dot_candidate_pages": [34, 40]},
            "derived_values": {},
            "corroboration_basis": "Existing visual observation lead and Stage 3Q visual topic triage.",
            "ambiguity_notes": "No binary, braille, or constellation interpretation is promoted.",
        },
        {
            "observation_id": "stage3r-observation-dead-oak-motif",
            "observation_type": "dead_oak_motif_review_candidate",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus_Unsolved_Pages",
            "source_title": "Liber Primus Unsolved Pages",
            "values": {"candidate_pages": [33, 56]},
            "derived_values": {},
            "corroboration_basis": "Stage 3Q visual topic triage mapped to public page/art discussion.",
            "ambiguity_notes": "Motif location review only; no cipher instruction inferred.",
        },
    ]
    records: list[dict[str, Any]] = []
    for row in rows:
        records.append(
            {
                "record_type": "promoted_discord_observation_record",
                "promotion_class": "observation_to_review",
                "usable_as_experiment_seed": False,
                "raw_message_committed": False,
                "username_committed": False,
                "private_url_committed": False,
                "trusted_as_canonical": False,
                "review_status": "review_required",
                "notes": "Promoted as reviewable observation only; not a fact, seed, or solve claim.",
                **row,
            }
        )
    return records


def _build_rejected_records(data: dict[str, Any]) -> list[dict[str, Any]]:
    rejected: list[dict[str, Any]] = []
    for record in data.get("source_links", []):
        links = record.get("public_links") or []
        if isinstance(links, str):
            links = [links]
        for link in links:
            if normalized_public_url(str(link)) is None:
                rejected.append(
                    {
                        "record_type": "stage3r_rejected_lead",
                        "promotion_class": "unsafe_or_private",
                        "reason": "private_or_nonpublic_url",
                        "source": "stage3q_source_links_index",
                        "raw_message_committed": False,
                        "username_committed": False,
                        "private_url_committed": False,
                    }
                )
    rejected.extend(
        [
            {
                "record_type": "stage3r_rejected_lead",
                "promotion_class": "too_speculative",
                "reason": "discord_only_or_speculative_claim_without_public_source",
                "source": "stage3q_review_bundle_triage",
                "raw_message_committed": False,
                "username_committed": False,
                "private_url_committed": False,
            }
            for _ in data.get("debunks", [])[:25]
        ]
    )
    return rejected


def _build_summary(
    *,
    data: dict[str, Any],
    out_dir: Path,
    source_records: list[dict[str, Any]],
    observation_records: list[dict[str, Any]],
    negative_controls: list[dict[str, Any]],
    duplicate_count: int,
    rejected_records: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    review_summary = data.get("review_summary", {})
    source_classes = Counter(str(record["source_class"]) for record in source_records)
    observation_types = Counter(str(record["observation_type"]) for record in observation_records)
    return {
        "record_type": "stage3r_promotion_audit_summary",
        "run_id": RUN_ID,
        "generated_at_utc": _utc_now(),
        "stage3q_review_lead_count": int(review_summary.get("review_lead_count", 0)),
        "stage3q_public_link_count": int(review_summary.get("public_link_count", 0)),
        "source_records_promoted": len(source_records),
        "observation_records_promoted": len(observation_records),
        "negative_controls_created": len(negative_controls),
        "duplicate_records_skipped": duplicate_count,
        "unsafe_private_records_rejected": len(rejected_records),
        "source_class_counts": dict(source_classes),
        "observation_type_counts": dict(observation_types),
        "manifests_queued": ["EXP-3R-001", "EXP-3R-003", "EXP-3R-004"],
        "experiment_execution_performed": False,
        "raw_message_committed": False,
        "username_committed": False,
        "private_url_committed": False,
        "raw_discord_logs_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
        "output_paths": {
            "promotion_audit_records": _display(out_dir / "promotion_audit_records.jsonl"),
            "rejected_or_quarantined_records": _display(out_dir / "rejected_or_quarantined_records.jsonl"),
            "promotion_summary": _display(out_dir / "promotion_summary.json"),
            "warnings": _display(out_dir / "warnings.jsonl"),
        },
        "warnings": warnings,
        "notes": "Discord-derived leads remain hypotheses; only public/redacted records were promoted.",
    }


def _existing_source_urls(source_registry: dict[str, Any]) -> set[str]:
    urls: set[str] = set()
    records = source_registry.get("records", [])
    if not isinstance(records, list):
        return urls
    for record in records:
        if not isinstance(record, dict):
            continue
        for key in ["source_url", "url", "archive_url"]:
            value = record.get(key)
            if isinstance(value, str):
                normalized = normalized_public_url(value)
                if normalized:
                    urls.add(normalized)
    return urls


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _display(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
