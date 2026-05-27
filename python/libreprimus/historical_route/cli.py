"""Typer CLI for Stage 5BF historical route source-lock records."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from libreprimus.historical_route.models import DATA_PATHS, FALLBACK_ARCHIVE, PREFERRED_ARCHIVE, RESULTS_DIR, UPSTREAM_URL
from libreprimus.historical_route.stage5bi import (
    DATA_PATHS as STAGE5BI_DATA_PATHS,
    build_stage5bi_records,
    summarize_stage5bi,
    validate_stage5bi,
)
from libreprimus.historical_route.stage5bf import (
    build_annual_route_inventory,
    build_deep_research_readiness,
    build_specialized_artifact_records,
    build_stage5bf_summary,
    build_technique_taxonomy,
    build_token_block_impact,
    build_trust_classifications,
    classify_artifacts,
    inventory_archive,
    locate_archive,
    validate_stage5bf,
)

console = Console()


def register(root_app: typer.Typer) -> None:
    app = typer.Typer(help="Historical route source-lock commands.")

    @app.command("locate-stage5bf-archive")
    def locate_stage5bf_archive(
        preferred_relative_path: Path = typer.Option(PREFERRED_ARCHIVE),
        fallback_absolute_path: Path = typer.Option(FALLBACK_ARCHIVE),
        upstream_url: str = typer.Option(UPSTREAM_URL),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out: Path = typer.Option(DATA_PATHS["archive_location"]),
    ) -> None:
        payload = locate_archive(
            preferred_relative_path=preferred_relative_path,
            fallback_absolute_path=fallback_absolute_path,
            upstream_url=upstream_url,
            results_dir=results_dir,
            out=out,
        )
        console.print(f"archive_available={str(payload['archive_available']).lower()}")
        console.print(f"selected_archive_path={payload['selected_archive_path']}")
        console.print(f"archive_tree_digest={payload['local_archive_tree_digest']}")

    @app.command("inventory-stage5bf-archive")
    def inventory_stage5bf_archive(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out_tree_summary: Path = typer.Option(DATA_PATHS["tree_summary"]),
        out_inventory_summary: Path = typer.Option(DATA_PATHS["inventory_summary"]),
    ) -> None:
        payload = inventory_archive(
            archive_location=archive_location,
            results_dir=results_dir,
            out_tree_summary=out_tree_summary,
            out_inventory_summary=out_inventory_summary,
        )
        console.print(f"total_file_count={payload['tree_summary']['total_file_count']}")
        console.print(f"archive_tree_digest={payload['tree_summary']['archive_tree_digest']}")

    @app.command("classify-stage5bf-artifacts")
    def classify_stage5bf_artifacts(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        tree_summary: Path = typer.Option(DATA_PATHS["tree_summary"]),
        inventory_summary: Path = typer.Option(DATA_PATHS["inventory_summary"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out_high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        out_family_taxonomy: Path = typer.Option(DATA_PATHS["family_taxonomy"]),
        out_trust_policy: Path = typer.Option(DATA_PATHS["trust_policy"]),
    ) -> None:
        payload = classify_artifacts(
            archive_location=archive_location,
            tree_summary=tree_summary,
            inventory_summary=inventory_summary,
            results_dir=results_dir,
            out_high_priority_index=out_high_priority_index,
            out_family_taxonomy=out_family_taxonomy,
            out_trust_policy=out_trust_policy,
        )
        console.print(f"high_priority_artifact_count={payload['high_priority_index']['artifact_count']}")

    @app.command("build-stage5bf-annual-route-inventory")
    def build_stage5bf_annual_route_inventory(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out: Path = typer.Option(DATA_PATHS["annual_route_inventory"]),
    ) -> None:
        payload = build_annual_route_inventory(
            archive_location=archive_location,
            high_priority_index=high_priority_index,
            results_dir=results_dir,
            out=out,
        )
        console.print(f"annual_route_years={len(payload['years'])}")

    @app.command("build-stage5bf-trust-classifications")
    def build_stage5bf_trust_classifications(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        trust_policy: Path = typer.Option(DATA_PATHS["trust_policy"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out: Path = typer.Option(DATA_PATHS["trust_classifications"]),
    ) -> None:
        payload = build_trust_classifications(
            archive_location=archive_location,
            high_priority_index=high_priority_index,
            trust_policy=trust_policy,
            results_dir=results_dir,
            out=out,
        )
        console.print(f"hash_locked_artifact_count={payload['hash_locked_artifact_count']}")

    @app.command("build-stage5bf-technique-taxonomy")
    def build_stage5bf_technique_taxonomy(
        annual_route_inventory: Path = typer.Option(DATA_PATHS["annual_route_inventory"]),
        trust_classifications: Path = typer.Option(DATA_PATHS["trust_classifications"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out: Path = typer.Option(DATA_PATHS["technique_taxonomy"]),
    ) -> None:
        payload = build_technique_taxonomy(
            annual_route_inventory=annual_route_inventory,
            trust_classifications=trust_classifications,
            results_dir=results_dir,
            out=out,
        )
        console.print(f"technique_count={len(payload['techniques'])}")

    @app.command("build-stage5bf-specialized-artifact-records")
    def build_stage5bf_specialized_artifact_records(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        trust_classifications: Path = typer.Option(DATA_PATHS["trust_classifications"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out_pgp: Path = typer.Option(DATA_PATHS["pgp"]),
        out_stego: Path = typer.Option(DATA_PATHS["stego"]),
        out_outguess: Path = typer.Option(DATA_PATHS["outguess"]),
        out_openpuff: Path = typer.Option(DATA_PATHS["openpuff"]),
        out_magic_squares: Path = typer.Option(DATA_PATHS["magic_squares"]),
        out_hex_jpeg: Path = typer.Option(DATA_PATHS["hex_jpeg"]),
        out_onion: Path = typer.Option(DATA_PATHS["onion"]),
        out_book_codes: Path = typer.Option(DATA_PATHS["book_codes"]),
        out_network_byte: Path = typer.Option(DATA_PATHS["network_byte"]),
        out_liber_primus: Path = typer.Option(DATA_PATHS["liber_primus"]),
    ) -> None:
        payload = build_specialized_artifact_records(
            archive_location=archive_location,
            high_priority_index=high_priority_index,
            trust_classifications=trust_classifications,
            results_dir=results_dir,
            out_pgp=out_pgp,
            out_stego=out_stego,
            out_outguess=out_outguess,
            out_openpuff=out_openpuff,
            out_magic_squares=out_magic_squares,
            out_hex_jpeg=out_hex_jpeg,
            out_onion=out_onion,
            out_book_codes=out_book_codes,
            out_network_byte=out_network_byte,
            out_liber_primus=out_liber_primus,
        )
        console.print(f"pgp_candidate_count={payload['pgp']['pgp_candidate_count']}")
        console.print(f"stego_candidate_count={payload['stego']['candidate_count']}")

    @app.command("build-stage5bf-token-block-impact")
    def build_stage5bf_token_block_impact(
        technique_taxonomy: Path = typer.Option(DATA_PATHS["technique_taxonomy"]),
        trust_classifications: Path = typer.Option(DATA_PATHS["trust_classifications"]),
        stage5bd_summary: Path = typer.Option(Path("data/project-state/stage5bd-summary.yaml")),
        stage5bd_dry_run_policy: Path = typer.Option(Path("data/token-block/stage5bd-dry-run-policy.yaml")),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out_impact: Path = typer.Option(DATA_PATHS["token_block_impact"]),
        out_source_gaps: Path = typer.Option(DATA_PATHS["source_gaps"]),
    ) -> None:
        payload = build_token_block_impact(
            technique_taxonomy=technique_taxonomy,
            trust_classifications=trust_classifications,
            stage5bd_summary=stage5bd_summary,
            stage5bd_dry_run_policy=stage5bd_dry_run_policy,
            results_dir=results_dir,
            out_impact=out_impact,
            out_source_gaps=out_source_gaps,
        )
        console.print(f"source_gap_count={payload['source_gaps']['source_gap_count']}")

    @app.command("build-stage5bf-deep-research-readiness")
    def build_stage5bf_deep_research_readiness(
        annual_route_inventory: Path = typer.Option(DATA_PATHS["annual_route_inventory"]),
        high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        trust_classifications: Path = typer.Option(DATA_PATHS["trust_classifications"]),
        technique_taxonomy: Path = typer.Option(DATA_PATHS["technique_taxonomy"]),
        token_block_impact: Path = typer.Option(DATA_PATHS["token_block_impact"]),
        source_gaps: Path = typer.Option(DATA_PATHS["source_gaps"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
        out_readiness: Path = typer.Option(DATA_PATHS["readiness"]),
        out_dwh_context: Path = typer.Option(DATA_PATHS["dwh_context"]),
    ) -> None:
        payload = build_deep_research_readiness(
            annual_route_inventory=annual_route_inventory,
            high_priority_index=high_priority_index,
            trust_classifications=trust_classifications,
            technique_taxonomy=technique_taxonomy,
            token_block_impact=token_block_impact,
            source_gaps=source_gaps,
            results_dir=results_dir,
            out_readiness=out_readiness,
            out_dwh_context=out_dwh_context,
        )
        console.print(f"ready_for_deep_research_review={str(payload['readiness']['ready_for_deep_research_review']).lower()}")

    @app.command("build-stage5bf-summary")
    def build_summary_command(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        tree_summary: Path = typer.Option(DATA_PATHS["tree_summary"]),
        inventory_summary: Path = typer.Option(DATA_PATHS["inventory_summary"]),
        annual_route_inventory: Path = typer.Option(DATA_PATHS["annual_route_inventory"]),
        high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        family_taxonomy: Path = typer.Option(DATA_PATHS["family_taxonomy"]),
        trust_policy: Path = typer.Option(DATA_PATHS["trust_policy"]),
        trust_classifications: Path = typer.Option(DATA_PATHS["trust_classifications"]),
        pgp: Path = typer.Option(DATA_PATHS["pgp"]),
        stego: Path = typer.Option(DATA_PATHS["stego"]),
        outguess: Path = typer.Option(DATA_PATHS["outguess"]),
        openpuff: Path = typer.Option(DATA_PATHS["openpuff"]),
        magic_squares: Path = typer.Option(DATA_PATHS["magic_squares"]),
        hex_jpeg: Path = typer.Option(DATA_PATHS["hex_jpeg"]),
        onion: Path = typer.Option(DATA_PATHS["onion"]),
        book_codes: Path = typer.Option(DATA_PATHS["book_codes"]),
        network_byte: Path = typer.Option(DATA_PATHS["network_byte"]),
        liber_primus: Path = typer.Option(DATA_PATHS["liber_primus"]),
        technique_taxonomy: Path = typer.Option(DATA_PATHS["technique_taxonomy"]),
        token_block_impact: Path = typer.Option(DATA_PATHS["token_block_impact"]),
        source_gaps: Path = typer.Option(DATA_PATHS["source_gaps"]),
        readiness: Path = typer.Option(DATA_PATHS["readiness"]),
        dwh_context: Path = typer.Option(DATA_PATHS["dwh_context"]),
        out_guardrail: Path = typer.Option(DATA_PATHS["guardrail"]),
        out_next_stage: Path = typer.Option(DATA_PATHS["next_stage"]),
        out_summary: Path = typer.Option(DATA_PATHS["summary"]),
    ) -> None:
        payload = build_stage5bf_summary(
            archive_location=archive_location,
            tree_summary=tree_summary,
            inventory_summary=inventory_summary,
            annual_route_inventory=annual_route_inventory,
            high_priority_index=high_priority_index,
            family_taxonomy=family_taxonomy,
            trust_policy=trust_policy,
            trust_classifications=trust_classifications,
            pgp=pgp,
            stego=stego,
            outguess=outguess,
            openpuff=openpuff,
            magic_squares=magic_squares,
            hex_jpeg=hex_jpeg,
            onion=onion,
            book_codes=book_codes,
            network_byte=network_byte,
            liber_primus=liber_primus,
            technique_taxonomy=technique_taxonomy,
            token_block_impact=token_block_impact,
            source_gaps=source_gaps,
            readiness=readiness,
            dwh_context=dwh_context,
            out_guardrail=out_guardrail,
            out_next_stage=out_next_stage,
            out_summary=out_summary,
        )
        console.print("stage5bf_summary_written=true")
        console.print(f"high_priority_artifact_count={payload['high_priority_artifact_count']}")

    @app.command("validate-stage5bf")
    def validate_stage5bf_command(
        archive_location: Path = typer.Option(DATA_PATHS["archive_location"]),
        tree_summary: Path = typer.Option(DATA_PATHS["tree_summary"]),
        inventory_summary: Path = typer.Option(DATA_PATHS["inventory_summary"]),
        annual_route_inventory: Path = typer.Option(DATA_PATHS["annual_route_inventory"]),
        high_priority_index: Path = typer.Option(DATA_PATHS["high_priority_index"]),
        family_taxonomy: Path = typer.Option(DATA_PATHS["family_taxonomy"]),
        trust_policy: Path = typer.Option(DATA_PATHS["trust_policy"]),
        trust_classifications: Path = typer.Option(DATA_PATHS["trust_classifications"]),
        pgp: Path = typer.Option(DATA_PATHS["pgp"]),
        stego: Path = typer.Option(DATA_PATHS["stego"]),
        outguess: Path = typer.Option(DATA_PATHS["outguess"]),
        openpuff: Path = typer.Option(DATA_PATHS["openpuff"]),
        magic_squares: Path = typer.Option(DATA_PATHS["magic_squares"]),
        hex_jpeg: Path = typer.Option(DATA_PATHS["hex_jpeg"]),
        onion: Path = typer.Option(DATA_PATHS["onion"]),
        book_codes: Path = typer.Option(DATA_PATHS["book_codes"]),
        network_byte: Path = typer.Option(DATA_PATHS["network_byte"]),
        liber_primus: Path = typer.Option(DATA_PATHS["liber_primus"]),
        technique_taxonomy: Path = typer.Option(DATA_PATHS["technique_taxonomy"]),
        token_block_impact: Path = typer.Option(DATA_PATHS["token_block_impact"]),
        source_gaps: Path = typer.Option(DATA_PATHS["source_gaps"]),
        readiness: Path = typer.Option(DATA_PATHS["readiness"]),
        dwh_context: Path = typer.Option(DATA_PATHS["dwh_context"]),
        guardrail: Path = typer.Option(DATA_PATHS["guardrail"]),
        next_stage_decision: Path = typer.Option(DATA_PATHS["next_stage"]),
        summary: Path = typer.Option(DATA_PATHS["summary"]),
        results_dir: Path = typer.Option(RESULTS_DIR),
    ) -> None:
        result = validate_stage5bf(
            archive_location=archive_location,
            tree_summary=tree_summary,
            inventory_summary=inventory_summary,
            annual_route_inventory=annual_route_inventory,
            high_priority_index=high_priority_index,
            family_taxonomy=family_taxonomy,
            trust_policy=trust_policy,
            trust_classifications=trust_classifications,
            pgp=pgp,
            stego=stego,
            outguess=outguess,
            openpuff=openpuff,
            magic_squares=magic_squares,
            hex_jpeg=hex_jpeg,
            onion=onion,
            book_codes=book_codes,
            network_byte=network_byte,
            liber_primus=liber_primus,
            technique_taxonomy=technique_taxonomy,
            token_block_impact=token_block_impact,
            source_gaps=source_gaps,
            readiness=readiness,
            dwh_context=dwh_context,
            guardrail=guardrail,
            next_stage_decision=next_stage_decision,
            summary=summary,
            results_dir=results_dir,
        )
        for key, value in result.items():
            if key != "validation_errors":
                console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")

    @app.command("stage5bi-build")
    def stage5bi_build() -> None:
        payloads = build_stage5bi_records()
        summary = payloads["summary"]
        console.print("stage5bi_build=true")
        console.print(f"fandom_page_triage_count={summary['fandom_page_triage_count']}")
        console.print(f"item_source_lock_candidate_count={summary['item_source_lock_candidate_count']}")
        console.print(
            f"original_archive_crosswalk_candidate_count={summary['original_archive_crosswalk_candidate_count']}"
        )
        console.print(f"verified_archive_crosswalk_count={summary['verified_archive_crosswalk_count']}")
        console.print(f"source_gap_count={summary['source_gap_count']}")
        console.print(f"negative_control_count={summary['negative_control_count']}")
        console.print(f"spreadsheet_found={str(summary['spreadsheet_found']).lower()}")

    @app.command("stage5bi-validate")
    def stage5bi_validate(
        page_triage: Path = typer.Option(STAGE5BI_DATA_PATHS["page_triage"]),
        item_candidates: Path = typer.Option(STAGE5BI_DATA_PATHS["item_candidates"]),
        archive_crosswalk: Path = typer.Option(STAGE5BI_DATA_PATHS["archive_crosswalk"]),
        media_policy: Path = typer.Option(STAGE5BI_DATA_PATHS["media_policy"]),
        surface_context: Path = typer.Option(STAGE5BI_DATA_PATHS["surface_context"]),
        negative_controls: Path = typer.Option(STAGE5BI_DATA_PATHS["negative_controls"]),
        source_gaps: Path = typer.Option(STAGE5BI_DATA_PATHS["source_gaps"]),
        guardrail: Path = typer.Option(STAGE5BI_DATA_PATHS["guardrail"]),
        token_block_context: Path = typer.Option(STAGE5BI_DATA_PATHS["token_block_context"]),
        surface_token_block_context: Path = typer.Option(STAGE5BI_DATA_PATHS["surface_token_block_context"]),
        spreadsheet_reconciliation: Path = typer.Option(STAGE5BI_DATA_PATHS["spreadsheet_reconciliation"]),
        spreadsheet_source_lock: Path = typer.Option(STAGE5BI_DATA_PATHS["spreadsheet_source_lock"]),
        crosswalk_summary: Path = typer.Option(STAGE5BI_DATA_PATHS["crosswalk_summary"]),
        summary: Path = typer.Option(STAGE5BI_DATA_PATHS["summary"]),
        next_stage: Path = typer.Option(STAGE5BI_DATA_PATHS["next_stage"]),
    ) -> None:
        result = validate_stage5bi(
            {
                "page_triage": page_triage,
                "item_candidates": item_candidates,
                "archive_crosswalk": archive_crosswalk,
                "media_policy": media_policy,
                "surface_context": surface_context,
                "negative_controls": negative_controls,
                "source_gaps": source_gaps,
                "guardrail": guardrail,
                "token_block_context": token_block_context,
                "surface_token_block_context": surface_token_block_context,
                "spreadsheet_reconciliation": spreadsheet_reconciliation,
                "spreadsheet_source_lock": spreadsheet_source_lock,
                "crosswalk_summary": crosswalk_summary,
                "summary": summary,
                "next_stage": next_stage,
            }
        )
        for key, value in result.items():
            if key != "validation_errors":
                console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")

    @app.command("stage5bi-summary")
    def stage5bi_summary(summary: Path = typer.Option(STAGE5BI_DATA_PATHS["summary"])) -> None:
        payload = summarize_stage5bi(summary)
        console.print(f"stage_id={payload.get('stage_id')}")
        console.print(f"status={payload.get('status')}")
        console.print(f"fandom_page_triage_count={payload.get('fandom_page_triage_count')}")
        console.print(f"item_source_lock_candidate_count={payload.get('item_source_lock_candidate_count')}")
        console.print(
            f"original_archive_crosswalk_candidate_count={payload.get('original_archive_crosswalk_candidate_count')}"
        )
        console.print(f"verified_archive_crosswalk_count={payload.get('verified_archive_crosswalk_count')}")
        console.print(f"source_gap_count={payload.get('source_gap_count')}")
        console.print(f"negative_control_count={payload.get('negative_control_count')}")
        console.print(f"spreadsheet_found={str(payload.get('spreadsheet_found')).lower()}")

    root_app.add_typer(app, name="historical-route")
