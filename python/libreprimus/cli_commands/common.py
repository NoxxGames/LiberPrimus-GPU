"""Shared imports, defaults, and helpers for CLI command modules."""
# ruff: noqa: F401

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from libreprimus.corpus_candidate.export import write_corpus_candidate_outputs
from libreprimus.corpus_candidate.generator import build_rtkd_corpus_candidate
from libreprimus.corpus_candidate.separator_inventory import observed_separator_inventory
from libreprimus.corpus_candidate.summary import load_summary as load_candidate_summary
from libreprimus.corpus_candidate.validation import validate_corpus_candidate
from libreprimus.legacy_workbook.export import extract_workbook, write_extraction, write_json
from libreprimus.legacy_workbook.paths import default_output_dir, resolve_workbook_path
from libreprimus.legacy_pastebin.export import (
    extract_legacy_pastebin,
    write_extraction as write_pastebin_extraction,
)
from libreprimus.legacy_pastebin.loader import (
    default_output_dir as default_pastebin_output_dir,
    resolve_input_path,
)
from libreprimus.alignment.export import (
    write_json as write_alignment_json,
    write_jsonl as write_alignment_jsonl,
    write_stage0d_followup_outputs,
    write_stage0d_outputs,
)
from libreprimus.alignment.boundary_audit import audit_page_boundaries
from libreprimus.alignment.models import PageBoundaryCandidate
from libreprimus.alignment.page_boundaries import infer_boundaries_from_alignment_file
from libreprimus.alignment.pastebin_to_transcript import (
    align_pastebin_to_transcript,
    align_pastebin_to_transcript_followup,
    build_alignment_records,
    glyph_variant_observations,
)
from libreprimus.paths import package_root, repo_root
from libreprimus.profiles.gematria_profile import load_gematria_profile, validate_gematria_profile
from libreprimus.profiles.glyph_variant_profile import load_glyph_variant_profile, validate_glyph_variant_profile
from libreprimus.profiles.separator_grammar import load_separator_grammar, validate_separator_grammar
from libreprimus.solved_fixtures.export import write_json as write_fixture_json
from libreprimus.solved_fixtures.export import write_reproduction_outputs
from libreprimus.solved_fixtures.fixture_loader import load_fixtures
from libreprimus.solved_fixtures.reproduction import (
    reproduce_atbash_family_fixtures,
    reproduce_direct_translation_fixtures,
    reproduce_prime_stream_fixtures,
    reproduce_vigenere_fixtures,
)
from libreprimus.solved_fixtures.summary import load_summary as load_fixture_summary
from libreprimus.solved_fixtures.validation import validate_fixture_dir, validate_reproduction_results
from libreprimus.solved_baselines.export import write_manifest_run_outputs
from libreprimus.solved_baselines.manifest_loader import load_manifest
from libreprimus.solved_baselines.runner import run_manifest
from libreprimus.solved_baselines.summary import load_summary as load_baseline_summary
from libreprimus.solved_baselines.validation import validate_manifest_file
from libreprimus.result_store.import_solved_baseline import import_solved_baseline
from libreprimus.result_store.summary import load_summary as load_result_store_summary
from libreprimus.result_store.validation import (
    validate_result_store,
    validate_result_store_manifest_file,
)
from libreprimus.result_store.sqlite_sink import table_counts
from libreprimus.consistency.runner import run_consistency_suite
from libreprimus.experiments.dry_run_planner import build_dry_run_plan
from libreprimus.experiments.export import write_dry_run_outputs, write_summary as write_dry_run_summary
from libreprimus.experiments.manifest_loader import load_exploratory_manifest
from libreprimus.experiments.summary import load_plan_records, load_summary as load_dry_run_summary
from libreprimus.experiment_execution.cpu_runner import run_cpu_execution_manifest
from libreprimus.experiment_execution.execution_planner import build_execution_plan
from libreprimus.experiment_execution.manifest_loader import load_cpu_execution_manifest
from libreprimus.experiment_execution.result_export import (
    write_aggregate_summary as write_execution_aggregate_summary,
    write_execution_outputs,
)
from libreprimus.experiment_execution.summary import (
    load_result_records as load_execution_result_records,
    load_summary as load_execution_summary,
)
from libreprimus.experiment_proposals.approval_gate import evaluate_approval_gate
from libreprimus.experiment_proposals.approval_records import load_approval_record
from libreprimus.experiment_proposals.export import (
    write_review_packet_outputs,
    write_summary as write_review_packet_summary,
)
from libreprimus.experiment_proposals.proposal_loader import load_experiment_proposal
from libreprimus.experiment_proposals.review_packet import build_review_packet
from libreprimus.experiment_proposals.summary import (
    load_review_packets,
    load_summary as load_review_packet_summary,
)
from libreprimus.approval_execution.execution_bridge import (
    build_approval_execution_plan,
    run_approval_execution_request,
)
from libreprimus.approval_execution.request_loader import load_approval_execution_request
from libreprimus.approval_execution.result_export import (
    write_approval_execution_outputs,
    write_summary as write_approval_execution_summary,
)
from libreprimus.approval_execution.summary import (
    load_result_records as load_approval_execution_result_records,
    load_summary as load_approval_execution_summary,
)
from libreprimus.approval_readiness.export import (
    write_approval_readiness_outputs,
    write_summary as write_approval_readiness_summary,
)
from libreprimus.approval_readiness.packet_generator import build_approval_readiness_packet
from libreprimus.approval_readiness.readiness_analyzer import analyze_approval_readiness
from libreprimus.approval_readiness.summary import (
    load_packets as load_approval_readiness_packets,
    load_summary as load_approval_readiness_summary,
)
from libreprimus.bounded_experiments.policy_loader import load_operator_policy
from libreprimus.bounded_experiments.queue_loader import load_bounded_queue
from libreprimus.bounded_experiments.runner import (
    check_queue_paths as check_bounded_queue_paths,
    run_all as run_all_bounded_experiments,
    run_next as run_next_bounded_experiment,
)
from libreprimus.bounded_experiments.summary import (
    load_results as load_bounded_experiment_results,
    load_summary as load_bounded_experiment_summary,
)
from libreprimus.bounded_execution.reset_advance_ablation import run_reset_advance_ablation_from_paths
from libreprimus.bounded_execution.runner import run_caesar_affine_from_paths
from libreprimus.bounded_execution.summary import load_summary as load_bounded_run_summary
from libreprimus.bounded_execution.mersenne_stream_probe import run_mersenne_stream_probe_from_paths
from libreprimus.bounded_execution.prime_offset_sweep import run_prime_offset_sweep_from_paths
from libreprimus.bounded_execution.vigenere_key_pack import run_vigenere_key_pack_from_paths
from libreprimus.bounded_execution.vigenere_key_list import run_vigenere_key_list_from_paths
from libreprimus.candidate_inspection.analysis import inspect_results, rerank_candidates
from libreprimus.candidate_inspection.loader import load_candidate_records
from libreprimus.candidate_inspection.report import (
    write_inspection_markdown,
    write_json as write_inspection_json,
    write_jsonl as write_inspection_jsonl,
)
from libreprimus.candidate_inspection.summary import to_summary_payload
from libreprimus.candidate_inspection.validation import validate_no_full_dump_in_markdown, validate_summary_payload
from libreprimus.scoring.calibration import run_scoring_calibration
from libreprimus.scoring.crib_checks import DEFAULT_CRIBS_PATH, crib_check, load_cribs
from libreprimus.method_backlog.dry_run import dry_run_stage3e_queue
from libreprimus.history.image_locks import scan_local_images, validate_image_locks
from libreprimus.history.source_records import validate_source_records
from libreprimus.hash_preimage.candidate_packs import expand_candidate_pack, load_candidate_packs
from libreprimus.hash_preimage.runner import run_hash_preimage
from libreprimus.hash_preimage.summary import load_summary as load_hash_preimage_summary
from libreprimus.hash_preimage.validation import validate_candidate_packs
from libreprimus.image_analysis.runner import analyze_local_pages
from libreprimus.image_analysis.summary import load_summary as load_image_analysis_summary
from libreprimus.image_analysis.validation import validate_results as validate_image_analysis_results
from libreprimus.image_transforms.runner import run_local_page_transforms
from libreprimus.image_transforms.summary import load_summary as load_image_transform_summary
from libreprimus.image_transforms.validation import validate_results as validate_image_transform_results
from libreprimus.discord_ingestion.html_scanner import scan_discord_archive
from libreprimus.discord_ingestion.summary import load_summary as load_discord_ingestion_summary
from libreprimus.discord_ingestion.validation import (
    export_aggregate_records as export_discord_aggregate_records,
    validate_results as validate_discord_ingestion_results,
)
from libreprimus.discord_promotion.promoter import promote_discord_sources
from libreprimus.discord_promotion.summary import load_summary as load_discord_promotion_summary
from libreprimus.discord_promotion.validation import validate_promoted_records
from libreprimus.discord_review.runner import build_review_bundles
from libreprimus.discord_review.summary import load_summary as load_discord_review_summary
from libreprimus.discord_review.validation import validate_bundles as validate_discord_review_bundles
from libreprimus.discord_lead_promotion.manifest_builder import build_post_discord_manifests
from libreprimus.discord_lead_promotion.promoter import promote_discord_leads
from libreprimus.discord_lead_promotion.summary import load_summary as load_discord_lead_summary
from libreprimus.discord_lead_promotion.validation import validate_stage3r_outputs
from libreprimus.post_discord.cookie_signed_variant_pack import (
    DEFAULT_COOKIES as DEFAULT_STAGE3U_COOKIES,
    DEFAULT_MANIFEST as DEFAULT_STAGE3U_COOKIE_MANIFEST,
    DEFAULT_OUTPUT_DIR as DEFAULT_STAGE3U_POST_DISCORD_DIR,
    load_cookie_signed_summary,
    run_cookie_signed_variant_pack,
    validate_cookie_manifest,
)
from libreprimus.post_discord.gp_rune_claim_verifier import (
    DEFAULT_MANIFEST as DEFAULT_STAGE3T_GP_RUNE_MANIFEST,
    DEFAULT_OUTPUT_DIR as DEFAULT_STAGE3T_POST_DISCORD_DIR,
    DEFAULT_PROMOTED_OBSERVATIONS as DEFAULT_STAGE3T_PROMOTED_OBSERVATIONS,
    DEFAULT_VISUAL_OBSERVATIONS as DEFAULT_STAGE3T_VISUAL_OBSERVATIONS,
    load_gp_rune_summary,
    run_gp_rune_verifier,
    validate_gp_rune_manifest,
)
from libreprimus.post_discord.models import DEFAULT_MANIFEST as DEFAULT_STAGE3S_ONION7_MANIFEST
from libreprimus.post_discord.models import DEFAULT_OUTPUT_DIR as DEFAULT_STAGE3S_POST_DISCORD_DIR
from libreprimus.post_discord.onion7_seed_pack import run_onion7_seed_pack
from libreprimus.post_discord.summary import load_summary as load_post_discord_summary
from libreprimus.post_discord.validation import validate_manifest as validate_post_discord_manifest
from libreprimus.stego.outguess_export import write_json as write_stego_json
from libreprimus.stego.outguess_manifest import validate_manifest_and_artifacts as validate_outguess_manifest
from libreprimus.stego.outguess_runner import (
    DEFAULT_ARTIFACTS as DEFAULT_STAGE3V_ARTIFACTS,
    DEFAULT_MANIFEST as DEFAULT_STAGE3V_MANIFEST,
    DEFAULT_OUTPUT_DIR as DEFAULT_STAGE3V_OUTPUT_DIR,
    run_outguess_regression,
)
from libreprimus.stego.outguess_summary import load_summary as load_outguess_summary
from libreprimus.stego.outguess_tool import detect_outguess, tool_record
from libreprimus.visual_observations.validation import (
    summarize_observations,
    validate_cookie_records,
    validate_visual_records,
)
from libreprimus.reference_sources.summary import build_stage1c_reference_summary, write_stage1c_reference_outputs
from libreprimus.transcript_sources.export import write_jsonl as write_transcript_jsonl
from libreprimus.transcript_sources.rtkd_master import parse_rtkd_master
from libreprimus.transcript_sources.scream314_reference import parse_scream314_reference
from libreprimus.toolchain import ToolStatus, collect_toolchain
from libreprimus.transforms.registry import load_registry, resolve_transform
from libreprimus.transforms.validation import validate_registry_file


console = Console()

DEFAULT_GEMATRIA_PROFILE = Path("data/profiles/gematria/gematria-primus-v0.json")
DEFAULT_GLYPH_VARIANT_PROFILE = Path("data/profiles/glyph-variants/glyph-variants-v0.json")
DEFAULT_SEPARATOR_GRAMMAR = Path("data/profiles/separators/rtkd-separator-grammar-v0.json")
DEFAULT_CORPUS_CANDIDATE_DIR = Path("data/normalized/corpus-candidates/rtkd-master-v0-candidate")
DEFAULT_DIRECT_FIXTURE_DIR = Path("data/fixtures/solved-pages/direct-translation-v0")
DEFAULT_DIRECT_BASELINE_DIR = Path("data/normalized/solved-baselines/direct-translation-v0")
DEFAULT_ATBASH_FIXTURE_DIR = Path("data/fixtures/solved-pages/atbash-family-v0")
DEFAULT_ATBASH_BASELINE_DIR = Path("data/normalized/solved-baselines/atbash-family-v0")
DEFAULT_VIGENERE_FIXTURE_DIR = Path("data/fixtures/solved-pages/vigenere-v0")
DEFAULT_VIGENERE_BASELINE_DIR = Path("data/normalized/solved-baselines/vigenere-v0")
DEFAULT_PRIME_STREAM_FIXTURE_DIR = Path("data/fixtures/solved-pages/prime-stream-v0")
DEFAULT_PRIME_STREAM_BASELINE_DIR = Path("data/normalized/solved-baselines/prime-stream-v0")
DEFAULT_REFERENCE_SUMMARY_DIR = Path("data/normalized/reference-summaries/stage-1c")
DEFAULT_TRANSFORM_REGISTRY = Path("data/transform-registry/cpu-reference-transforms-v0.json")
DEFAULT_SOLVED_BASELINE_MANIFEST = Path(
    "experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml"
)
DEFAULT_STAGE2A_RESULTS_DIR = Path("experiments/results/solved-baselines/stage2a")
DEFAULT_RESULT_STORE_MANIFEST = Path("experiments/manifests/result-store/stage2b-solved-baseline-import.yaml")
DEFAULT_STAGE2B_RESULT_STORE_DIR = Path("experiments/results/result-store/stage2b")
DEFAULT_STAGE2B_SQLITE = DEFAULT_STAGE2B_RESULT_STORE_DIR / "results.sqlite3"
DEFAULT_STAGE2D_CONSISTENCY_SUMMARY = Path(
    "experiments/results/consistency/stage2d/consistency_summary.json"
)
DEFAULT_EXPLORATORY_MANIFEST_DIR = Path("experiments/manifests/exploratory")
DEFAULT_STAGE2E_DRY_RUN_DIR = Path("experiments/results/exploratory-dry-runs/stage2e")
DEFAULT_CPU_EXECUTION_MANIFEST_DIR = Path("experiments/manifests/cpu-execution")
DEFAULT_STAGE2F_EXECUTION_DIR = Path("experiments/results/cpu-execution/stage2f")
DEFAULT_STAGE2G_PROPOSAL_DIR = Path("experiments/proposals/stage2g")
DEFAULT_STAGE2G_REVIEW_DIR = Path("experiments/results/proposal-reviews/stage2g")
DEFAULT_STAGE2H_REQUEST_DIR = Path("experiments/proposals/stage2h")
DEFAULT_STAGE2H_APPROVAL_EXECUTION_DIR = Path("experiments/results/approval-gated-execution/stage2h")
DEFAULT_STAGE2I_PROPOSAL_DIR = Path("experiments/proposals/stage2i")
DEFAULT_STAGE2I_READINESS_DIR = Path("experiments/results/approval-readiness/stage2i")
DEFAULT_STAGE2J_POLICY = Path("experiments/policies/operator-policy-v0.yaml")
DEFAULT_STAGE2J_QUEUE = Path("experiments/queues/stage2j-bounded-cpu-queue.yaml")
DEFAULT_STAGE2J_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage2j")
DEFAULT_STAGE3A_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3a")
DEFAULT_STAGE3B_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3b")
DEFAULT_STAGE3B_INSPECTION_MD = Path("research-log/2026-05-16-stage-3b-stage3a-lead-inspection.md")
DEFAULT_STAGE3C_CALIBRATION_RESULTS_DIR = Path("experiments/results/scoring-calibration/stage3c")
DEFAULT_STAGE3D_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3d")
DEFAULT_STAGE3E_QUEUE = Path("experiments/queues/stage3e-bounded-cpu-queue.yaml")
DEFAULT_STAGE3E_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3e")
DEFAULT_STAGE3F_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3f")
DEFAULT_STAGE3G_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3g")
DEFAULT_STAGE3H_QUEUE = Path("experiments/queues/stage3h-bounded-cpu-queue.yaml")
DEFAULT_STAGE3H_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3h")
DEFAULT_STAGE3J_QUEUE = Path("experiments/queues/stage3j-bounded-cpu-queue.yaml")
DEFAULT_STAGE3J_BOUNDED_RESULTS_DIR = Path("experiments/results/bounded-auto-runs/stage3j")

def _resolve_existing_path(path: Path, label: str) -> Path:
    resolved = path if path.is_absolute() else repo_root() / path
    if not resolved.is_file():
        console.print(f"[red]{label} not found: {resolved}[/red]")
        raise typer.Exit(2)
    return resolved


def _resolve_output_path(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path



__all__ = [name for name in globals() if not name.startswith("__")]
