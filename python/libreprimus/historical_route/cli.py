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
from libreprimus.historical_route.stage5bj import (
    DATA_PATHS as STAGE5BJ_DATA_PATHS,
    build_stage5bj_records,
    summarize_stage5bj,
    validate_stage5bj,
)
from libreprimus.historical_route.stage5bk import (
    DATA_PATHS as STAGE5BK_DATA_PATHS,
    FALLBACK_IDDQD_V2,
    PREFERRED_IDDQD_V2,
    RESULTS_DIR as STAGE5BK_RESULTS_DIR,
    TOKEN_BLOCK_RESULTS_DIR as STAGE5BK_TOKEN_BLOCK_RESULTS_DIR,
    UPSTREAM_URL as STAGE5BK_UPSTREAM_URL,
    build_stage5bk_iddqd_v2_source_lock,
    build_stage5bk_planning_constraints,
    build_stage5bk_records,
    build_stage5bk_summary,
    build_stage5bk_token_block_impact,
    inventory_stage5bk_iddqd_v2,
    locate_stage5bk_iddqd_v2,
    summarize_stage5bk,
    validate_stage5bk,
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

    @app.command("stage5bj-build")
    def stage5bj_build() -> None:
        payloads = build_stage5bj_records()
        summary = payloads["summary"]
        console.print("stage5bj_build=true")
        console.print(f"crosswalk_closure_record_count={summary['crosswalk_closure_record_count']}")
        console.print(f"exact_512_hex_surface_locked_count={summary['exact_512_hex_surface_locked_count']}")
        console.print(f"surface_source_file_found_count={summary['surface_source_file_found_count']}")
        console.print(f"fandom_page_body_crosswalk_count={summary['fandom_page_body_crosswalk_count']}")
        console.print(f"boards_thread_found={str(summary['boards_thread_found']).lower()}")
        console.print(f"media_equivalence_record_count={summary['media_equivalence_record_count']}")
        console.print(f"source_gap_closed_count={summary['source_gap_closed_count']}")
        console.print(f"source_gap_carried_forward_count={summary['source_gap_carried_forward_count']}")
        console.print(f"new_source_gap_count={summary['new_source_gap_count']}")

    @app.command("stage5bj-validate")
    def stage5bj_validate(
        crosswalk_plan: Path = typer.Option(STAGE5BJ_DATA_PATHS["crosswalk_plan"]),
        crosswalk_closure: Path = typer.Option(STAGE5BJ_DATA_PATHS["crosswalk_closure"]),
        surface_locks: Path = typer.Option(STAGE5BJ_DATA_PATHS["surface_locks"]),
        page_body_crosswalk: Path = typer.Option(STAGE5BJ_DATA_PATHS["page_body_crosswalk"]),
        boards_thread: Path = typer.Option(STAGE5BJ_DATA_PATHS["boards_thread"]),
        candidate_status: Path = typer.Option(STAGE5BJ_DATA_PATHS["candidate_status"]),
        media_equivalence: Path = typer.Option(STAGE5BJ_DATA_PATHS["media_equivalence"]),
        source_gap_update: Path = typer.Option(STAGE5BJ_DATA_PATHS["source_gap_update"]),
        guardrail: Path = typer.Option(STAGE5BJ_DATA_PATHS["guardrail"]),
        token_block_lineage: Path = typer.Option(STAGE5BJ_DATA_PATHS["token_block_lineage"]),
        surface_context_closure: Path = typer.Option(STAGE5BJ_DATA_PATHS["surface_context_closure"]),
        local_archive_summary: Path = typer.Option(STAGE5BJ_DATA_PATHS["local_archive_summary"]),
        source_snapshot_summary: Path = typer.Option(STAGE5BJ_DATA_PATHS["source_snapshot_summary"]),
        summary: Path = typer.Option(STAGE5BJ_DATA_PATHS["summary"]),
        next_stage: Path = typer.Option(STAGE5BJ_DATA_PATHS["next_stage"]),
    ) -> None:
        result = validate_stage5bj(
            {
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
                "local_archive_summary": local_archive_summary,
                "source_snapshot_summary": source_snapshot_summary,
                "summary": summary,
                "next_stage": next_stage,
            }
        )
        for key, value in result.items():
            if key != "validation_errors":
                console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")

    @app.command("stage5bj-summary")
    def stage5bj_summary(summary: Path = typer.Option(STAGE5BJ_DATA_PATHS["summary"])) -> None:
        payload = summarize_stage5bj(summary)
        console.print(f"stage_id={payload.get('stage_id')}")
        console.print(f"status={payload.get('status')}")
        console.print(f"crosswalk_closure_record_count={payload.get('crosswalk_closure_record_count')}")
        console.print(f"exact_512_hex_surface_locked_count={payload.get('exact_512_hex_surface_locked_count')}")
        console.print(f"surface_source_file_found_count={payload.get('surface_source_file_found_count')}")
        console.print(f"fandom_page_body_crosswalk_count={payload.get('fandom_page_body_crosswalk_count')}")
        console.print(f"boards_thread_found={str(payload.get('boards_thread_found')).lower()}")
        console.print(f"media_equivalence_record_count={payload.get('media_equivalence_record_count')}")
        console.print(f"source_gap_closed_count={payload.get('source_gap_closed_count')}")
        console.print(f"source_gap_carried_forward_count={payload.get('source_gap_carried_forward_count')}")
        console.print(f"new_source_gap_count={payload.get('new_source_gap_count')}")
        console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")

    @app.command("locate-stage5bk-iddqd-v2")
    def locate_stage5bk_iddqd_v2_command(
        preferred_relative_path: Path = typer.Option(PREFERRED_IDDQD_V2),
        fallback_relative_path: Path = typer.Option(FALLBACK_IDDQD_V2),
        upstream_url: str = typer.Option(STAGE5BK_UPSTREAM_URL),
        prior_stage4e_source_delta: Path = typer.Option(
            Path("data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml")
        ),
        results_dir: Path = typer.Option(STAGE5BK_RESULTS_DIR),
        out: Path = typer.Option(STAGE5BK_DATA_PATHS["source_root"]),
    ) -> None:
        payload = locate_stage5bk_iddqd_v2(
            preferred_relative_path=preferred_relative_path,
            fallback_relative_path=fallback_relative_path,
            upstream_url=upstream_url,
            prior_stage4e_source_delta=prior_stage4e_source_delta,
            results_dir=results_dir,
            out=out,
        )
        console.print(f"iddqd_v2_source_root_found={str(payload['source_root_found']).lower()}")
        console.print(f"iddqd_v2_selected_path={payload['selected_path']}")
        console.print(f"source_root_status={payload['source_root_status']}")

    @app.command("inventory-stage5bk-iddqd-v2")
    def inventory_stage5bk_iddqd_v2_command(
        source_root: Path = typer.Option(STAGE5BK_DATA_PATHS["source_root"]),
        results_dir: Path = typer.Option(STAGE5BK_RESULTS_DIR),
        out_tree_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["tree_summary"]),
        out_candidate_index: Path = typer.Option(STAGE5BK_DATA_PATHS["candidate_index"]),
    ) -> None:
        payload = inventory_stage5bk_iddqd_v2(
            source_root=source_root,
            results_dir=results_dir,
            out_tree_summary=out_tree_summary,
            out_candidate_index=out_candidate_index,
        )
        tree = payload["tree_summary"]
        index = payload["candidate_index"]
        console.print(f"iddqd_v2_total_file_count={tree['total_file_count']}")
        console.print(f"iddqd_v2_tree_digest={tree['tree_digest']}")
        console.print(f"candidate_found_count={index['candidate_found_count']}")

    @app.command("build-stage5bk-iddqd-v2-source-lock")
    def build_stage5bk_iddqd_v2_source_lock_command(
        source_root: Path = typer.Option(STAGE5BK_DATA_PATHS["source_root"]),
        tree_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["tree_summary"]),
        candidate_index: Path = typer.Option(STAGE5BK_DATA_PATHS["candidate_index"]),
        stage5bj_surface_locks: Path = typer.Option(
            Path("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml")
        ),
        stage5ap_mapping: Path = typer.Option(Path("data/token-block/stage5ap-token-block-mapping-preflight.yaml")),
        stage5ap_transcription: Path = typer.Option(
            Path("data/token-block/stage5ap-token-block-canonical-transcription.yaml")
        ),
        results_dir: Path = typer.Option(STAGE5BK_RESULTS_DIR),
        out_byte_strings: Path = typer.Option(STAGE5BK_DATA_PATHS["byte_strings"]),
        out_transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["transcription"]),
        out_translation_key_lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["translation_key_lineage"]),
        out_positive_control_context: Path = typer.Option(STAGE5BK_DATA_PATHS["positive_control_context"]),
        out_source_gaps: Path = typer.Option(STAGE5BK_DATA_PATHS["iddqd_v2_source_gaps"]),
        out_string4_crosswalk: Path = typer.Option(STAGE5BK_DATA_PATHS["string4_crosswalk"]),
    ) -> None:
        payload = build_stage5bk_iddqd_v2_source_lock(
            source_root=source_root,
            tree_summary=tree_summary,
            candidate_index=candidate_index,
            stage5bj_surface_locks=stage5bj_surface_locks,
            stage5ap_mapping=stage5ap_mapping,
            stage5ap_transcription=stage5ap_transcription,
            results_dir=results_dir,
            out_byte_strings=out_byte_strings,
            out_transcription=out_transcription,
            out_translation_key_lineage=out_translation_key_lineage,
            out_positive_control_context=out_positive_control_context,
            out_source_gaps=out_source_gaps,
            out_string4_crosswalk=out_string4_crosswalk,
        )
        console.print(f"byte_string_count={payload['byte_strings']['byte_string_count']}")
        console.print(f"exact_512_hex_string_count={payload['byte_strings']['exact_512_hex_string_count']}")
        console.print(
            "string4_page49_crosswalk_created="
            f"{str(payload['string4_crosswalk']['source_string4_found']).lower()}"
        )

    @app.command("build-stage5bk-planning-constraints")
    def build_stage5bk_planning_constraints_command(
        stage5bf_technique_taxonomy: Path = typer.Option(
            Path("data/historical-route/stage5bf-historical-technique-taxonomy.yaml")
        ),
        stage5bf_token_block_impact: Path = typer.Option(
            Path("data/historical-route/stage5bf-token-block-planning-impact.yaml")
        ),
        stage5bf_source_gaps: Path = typer.Option(Path("data/historical-route/stage5bf-source-gap-register.yaml")),
        stage5bj_summary: Path = typer.Option(Path("data/project-state/stage5bj-summary.yaml")),
        stage5bj_surface_locks: Path = typer.Option(
            Path("data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml")
        ),
        stage5bj_crosswalk_closure: Path = typer.Option(
            Path("data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml")
        ),
        stage5bj_page_body_crosswalk: Path = typer.Option(
            Path("data/historical-route/stage5bj-fandom-page-body-crosswalk.yaml")
        ),
        stage5bj_source_gaps: Path = typer.Option(Path("data/historical-route/stage5bj-source-gap-update.yaml")),
        iddqd_v2_byte_strings: Path = typer.Option(STAGE5BK_DATA_PATHS["byte_strings"]),
        iddqd_v2_transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["transcription"]),
        iddqd_v2_translation_key_lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["translation_key_lineage"]),
        results_dir: Path = typer.Option(STAGE5BK_RESULTS_DIR),
        out_policy: Path = typer.Option(STAGE5BK_DATA_PATHS["constraint_policy"]),
        out_family_status: Path = typer.Option(STAGE5BK_DATA_PATHS["family_status"]),
        out_authenticity: Path = typer.Option(STAGE5BK_DATA_PATHS["authenticity"]),
        out_stego: Path = typer.Option(STAGE5BK_DATA_PATHS["stego"]),
        out_numeric: Path = typer.Option(STAGE5BK_DATA_PATHS["numeric"]),
        out_book_code: Path = typer.Option(STAGE5BK_DATA_PATHS["book_code"]),
        out_network_byte: Path = typer.Option(STAGE5BK_DATA_PATHS["network_byte"]),
        out_lp_transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["lp_transcription"]),
        out_dwh: Path = typer.Option(STAGE5BK_DATA_PATHS["dwh"]),
        out_gap_severity: Path = typer.Option(STAGE5BK_DATA_PATHS["gap_severity"]),
        out_crosswalk_errata: Path = typer.Option(STAGE5BK_DATA_PATHS["crosswalk_errata"]),
    ) -> None:
        payload = build_stage5bk_planning_constraints(
            stage5bf_technique_taxonomy=stage5bf_technique_taxonomy,
            stage5bf_token_block_impact=stage5bf_token_block_impact,
            stage5bf_source_gaps=stage5bf_source_gaps,
            stage5bj_summary=stage5bj_summary,
            stage5bj_surface_locks=stage5bj_surface_locks,
            stage5bj_crosswalk_closure=stage5bj_crosswalk_closure,
            stage5bj_page_body_crosswalk=stage5bj_page_body_crosswalk,
            stage5bj_source_gaps=stage5bj_source_gaps,
            iddqd_v2_byte_strings=iddqd_v2_byte_strings,
            iddqd_v2_transcription=iddqd_v2_transcription,
            iddqd_v2_translation_key_lineage=iddqd_v2_translation_key_lineage,
            results_dir=results_dir,
            out_policy=out_policy,
            out_family_status=out_family_status,
            out_authenticity=out_authenticity,
            out_stego=out_stego,
            out_numeric=out_numeric,
            out_book_code=out_book_code,
            out_network_byte=out_network_byte,
            out_lp_transcription=out_lp_transcription,
            out_dwh=out_dwh,
            out_gap_severity=out_gap_severity,
            out_crosswalk_errata=out_crosswalk_errata,
        )
        console.print(
            f"historical_family_planning_status_count="
            f"{payload['family_status']['historical_family_planning_status_count']}"
        )
        console.print(f"source_gap_severity_record_count={payload['gap_severity']['source_gap_severity_record_count']}")
        console.print(f"stage5bj_crosswalk_errata_count={payload['crosswalk_errata']['stage5bj_crosswalk_errata_count']}")

    @app.command("build-stage5bk-token-block-impact")
    def build_stage5bk_token_block_impact_command(
        constraint_policy: Path = typer.Option(STAGE5BK_DATA_PATHS["constraint_policy"]),
        family_status: Path = typer.Option(STAGE5BK_DATA_PATHS["family_status"]),
        gap_severity: Path = typer.Option(STAGE5BK_DATA_PATHS["gap_severity"]),
        string4_crosswalk: Path = typer.Option(STAGE5BK_DATA_PATHS["string4_crosswalk"]),
        stage5bd_summary: Path = typer.Option(Path("data/project-state/stage5bd-summary.yaml")),
        stage5bj_lineage: Path = typer.Option(Path("data/token-block/stage5bj-token-block-lineage-preservation.yaml")),
        results_dir: Path = typer.Option(STAGE5BK_TOKEN_BLOCK_RESULTS_DIR),
        out_token_block_update: Path = typer.Option(STAGE5BK_DATA_PATHS["token_block_update"]),
        out_surface_context: Path = typer.Option(STAGE5BK_DATA_PATHS["surface_context"]),
        out_lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["lineage"]),
        out_future_dry_run_impact: Path = typer.Option(STAGE5BK_DATA_PATHS["future_dry_run_impact"]),
    ) -> None:
        payload = build_stage5bk_token_block_impact(
            constraint_policy=constraint_policy,
            family_status=family_status,
            gap_severity=gap_severity,
            string4_crosswalk=string4_crosswalk,
            stage5bd_summary=stage5bd_summary,
            stage5bj_lineage=stage5bj_lineage,
            results_dir=results_dir,
            out_token_block_update=out_token_block_update,
            out_surface_context=out_surface_context,
            out_lineage=out_lineage,
            out_future_dry_run_impact=out_future_dry_run_impact,
        )
        console.print("token_block_historical_constraint_update_created=true")
        console.print(
            "future_token_block_execution_remains_blocked="
            f"{str(payload['token_block_update']['future_token_block_execution_remains_blocked']).lower()}"
        )

    @app.command("build-stage5bk-summary")
    def build_stage5bk_summary_command(
        source_root: Path = typer.Option(STAGE5BK_DATA_PATHS["source_root"]),
        tree_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["tree_summary"]),
        candidate_index: Path = typer.Option(STAGE5BK_DATA_PATHS["candidate_index"]),
        byte_strings: Path = typer.Option(STAGE5BK_DATA_PATHS["byte_strings"]),
        transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["transcription"]),
        translation_key_lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["translation_key_lineage"]),
        positive_control_context: Path = typer.Option(STAGE5BK_DATA_PATHS["positive_control_context"]),
        iddqd_v2_source_gaps: Path = typer.Option(STAGE5BK_DATA_PATHS["iddqd_v2_source_gaps"]),
        constraint_policy: Path = typer.Option(STAGE5BK_DATA_PATHS["constraint_policy"]),
        family_status: Path = typer.Option(STAGE5BK_DATA_PATHS["family_status"]),
        authenticity: Path = typer.Option(STAGE5BK_DATA_PATHS["authenticity"]),
        stego: Path = typer.Option(STAGE5BK_DATA_PATHS["stego"]),
        numeric: Path = typer.Option(STAGE5BK_DATA_PATHS["numeric"]),
        book_code: Path = typer.Option(STAGE5BK_DATA_PATHS["book_code"]),
        network_byte: Path = typer.Option(STAGE5BK_DATA_PATHS["network_byte"]),
        lp_transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["lp_transcription"]),
        dwh: Path = typer.Option(STAGE5BK_DATA_PATHS["dwh"]),
        gap_severity: Path = typer.Option(STAGE5BK_DATA_PATHS["gap_severity"]),
        crosswalk_errata: Path = typer.Option(STAGE5BK_DATA_PATHS["crosswalk_errata"]),
        token_block_update: Path = typer.Option(STAGE5BK_DATA_PATHS["token_block_update"]),
        surface_context: Path = typer.Option(STAGE5BK_DATA_PATHS["surface_context"]),
        string4_crosswalk: Path = typer.Option(STAGE5BK_DATA_PATHS["string4_crosswalk"]),
        lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["lineage"]),
        future_dry_run_impact: Path = typer.Option(STAGE5BK_DATA_PATHS["future_dry_run_impact"]),
        results_dir: Path = typer.Option(STAGE5BK_RESULTS_DIR),
        out_source_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["source_summary"]),
        out_codex_policy: Path = typer.Option(STAGE5BK_DATA_PATHS["codex_policy"]),
        out_guardrail: Path = typer.Option(STAGE5BK_DATA_PATHS["guardrail"]),
        out_next_stage: Path = typer.Option(STAGE5BK_DATA_PATHS["next_stage"]),
        out_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["summary"]),
    ) -> None:
        payload = build_stage5bk_summary(
            source_root=source_root,
            tree_summary=tree_summary,
            candidate_index=candidate_index,
            byte_strings=byte_strings,
            transcription=transcription,
            translation_key_lineage=translation_key_lineage,
            positive_control_context=positive_control_context,
            iddqd_v2_source_gaps=iddqd_v2_source_gaps,
            constraint_policy=constraint_policy,
            family_status=family_status,
            authenticity=authenticity,
            stego=stego,
            numeric=numeric,
            book_code=book_code,
            network_byte=network_byte,
            lp_transcription=lp_transcription,
            dwh=dwh,
            gap_severity=gap_severity,
            crosswalk_errata=crosswalk_errata,
            token_block_update=token_block_update,
            surface_context=surface_context,
            string4_crosswalk=string4_crosswalk,
            lineage=lineage,
            future_dry_run_impact=future_dry_run_impact,
            results_dir=results_dir,
            out_source_summary=out_source_summary,
            out_codex_policy=out_codex_policy,
            out_guardrail=out_guardrail,
            out_next_stage=out_next_stage,
            out_summary=out_summary,
        )
        console.print("stage5bk_summary_written=true")
        console.print(f"iddqd_v2_total_file_count={payload['iddqd_v2_total_file_count']}")
        console.print(f"byte_string_count={payload['iddqd_v2_byte_string_count']}")
        console.print(f"recommended_next_stage_title={payload['recommended_next_stage_title']}")

    @app.command("validate-stage5bk")
    def validate_stage5bk_command(
        source_root: Path = typer.Option(STAGE5BK_DATA_PATHS["source_root"]),
        tree_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["tree_summary"]),
        candidate_index: Path = typer.Option(STAGE5BK_DATA_PATHS["candidate_index"]),
        byte_strings: Path = typer.Option(STAGE5BK_DATA_PATHS["byte_strings"]),
        transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["transcription"]),
        translation_key_lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["translation_key_lineage"]),
        positive_control_context: Path = typer.Option(STAGE5BK_DATA_PATHS["positive_control_context"]),
        iddqd_v2_source_gaps: Path = typer.Option(STAGE5BK_DATA_PATHS["iddqd_v2_source_gaps"]),
        constraint_policy: Path = typer.Option(STAGE5BK_DATA_PATHS["constraint_policy"]),
        family_status: Path = typer.Option(STAGE5BK_DATA_PATHS["family_status"]),
        authenticity: Path = typer.Option(STAGE5BK_DATA_PATHS["authenticity"]),
        stego: Path = typer.Option(STAGE5BK_DATA_PATHS["stego"]),
        numeric: Path = typer.Option(STAGE5BK_DATA_PATHS["numeric"]),
        book_code: Path = typer.Option(STAGE5BK_DATA_PATHS["book_code"]),
        network_byte: Path = typer.Option(STAGE5BK_DATA_PATHS["network_byte"]),
        lp_transcription: Path = typer.Option(STAGE5BK_DATA_PATHS["lp_transcription"]),
        dwh: Path = typer.Option(STAGE5BK_DATA_PATHS["dwh"]),
        gap_severity: Path = typer.Option(STAGE5BK_DATA_PATHS["gap_severity"]),
        crosswalk_errata: Path = typer.Option(STAGE5BK_DATA_PATHS["crosswalk_errata"]),
        token_block_update: Path = typer.Option(STAGE5BK_DATA_PATHS["token_block_update"]),
        surface_context: Path = typer.Option(STAGE5BK_DATA_PATHS["surface_context"]),
        string4_crosswalk: Path = typer.Option(STAGE5BK_DATA_PATHS["string4_crosswalk"]),
        lineage: Path = typer.Option(STAGE5BK_DATA_PATHS["lineage"]),
        future_dry_run_impact: Path = typer.Option(STAGE5BK_DATA_PATHS["future_dry_run_impact"]),
        source_summary: Path = typer.Option(STAGE5BK_DATA_PATHS["source_summary"]),
        codex_policy: Path = typer.Option(STAGE5BK_DATA_PATHS["codex_policy"]),
        guardrail: Path = typer.Option(STAGE5BK_DATA_PATHS["guardrail"]),
        next_stage_decision: Path = typer.Option(STAGE5BK_DATA_PATHS["next_stage"]),
        summary: Path = typer.Option(STAGE5BK_DATA_PATHS["summary"]),
        results_dir: Path = typer.Option(STAGE5BK_RESULTS_DIR),
    ) -> None:
        result = validate_stage5bk(
            {
                "source_root": source_root,
                "tree_summary": tree_summary,
                "candidate_index": candidate_index,
                "byte_strings": byte_strings,
                "transcription": transcription,
                "translation_key_lineage": translation_key_lineage,
                "positive_control_context": positive_control_context,
                "iddqd_v2_source_gaps": iddqd_v2_source_gaps,
                "constraint_policy": constraint_policy,
                "family_status": family_status,
                "authenticity": authenticity,
                "stego": stego,
                "numeric": numeric,
                "book_code": book_code,
                "network_byte": network_byte,
                "lp_transcription": lp_transcription,
                "dwh": dwh,
                "gap_severity": gap_severity,
                "crosswalk_errata": crosswalk_errata,
                "token_block_update": token_block_update,
                "surface_context": surface_context,
                "string4_crosswalk": string4_crosswalk,
                "lineage": lineage,
                "future_dry_run_impact": future_dry_run_impact,
                "source_summary": source_summary,
                "codex_policy": codex_policy,
                "guardrail": guardrail,
                "next_stage": next_stage_decision,
                "summary": summary,
                "results_dir": results_dir,
            }
        )
        for key, value in result.items():
            if key != "validation_errors":
                console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")

    @app.command("stage5bk-build")
    def stage5bk_build() -> None:
        payloads = build_stage5bk_records()
        summary = payloads["summary"]
        console.print("stage5bk_build=true")
        console.print(f"iddqd_v2_total_file_count={summary['iddqd_v2_total_file_count']}")
        console.print(f"byte_string_count={summary['iddqd_v2_byte_string_count']}")
        console.print(f"source_gap_severity_record_count={summary['source_gap_severity_record_count']}")
        console.print(f"stage5bj_crosswalk_errata_count={summary['stage5bj_crosswalk_errata_count']}")

    @app.command("stage5bk-validate")
    def stage5bk_validate_alias() -> None:
        result = validate_stage5bk()
        for key, value in result.items():
            if key != "validation_errors":
                console.print(f"{key}={str(value).lower() if isinstance(value, bool) else value}")

    @app.command("stage5bk-summary")
    def stage5bk_summary(summary: Path = typer.Option(STAGE5BK_DATA_PATHS["summary"])) -> None:
        payload = summarize_stage5bk(summary)
        console.print(f"stage_id={payload.get('stage_id')}")
        console.print(f"status={payload.get('status')}")
        console.print(f"iddqd_v2_selected_path={payload.get('iddqd_v2_selected_path')}")
        console.print(f"iddqd_v2_total_file_count={payload.get('iddqd_v2_total_file_count')}")
        console.print(f"iddqd_v2_byte_string_count={payload.get('iddqd_v2_byte_string_count')}")
        console.print(f"source_gap_severity_record_count={payload.get('source_gap_severity_record_count')}")
        console.print(f"stage5bj_crosswalk_errata_count={payload.get('stage5bj_crosswalk_errata_count')}")
        console.print(f"recommended_next_stage_title={payload.get('recommended_next_stage_title')}")

    root_app.add_typer(app, name="historical-route")
