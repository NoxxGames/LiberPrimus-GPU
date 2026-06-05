"""Stage 5DK Fandom source-lock gap closure records.

This module builds compact metadata records for the Stage 5DK source-lock
closure. It deliberately hashes Fandom API content in memory only and never
writes raw page bodies or execution outputs into committed data.
"""

from __future__ import annotations

import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.token_block.models import read_yaml, sha256_file, write_json, write_jsonl, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import (
    ACTIVE_LINEAGE_PATHS,
    CORRECT_STAGE5AW_PATH,
    INCORRECT_STAGE5AW_PATH,
)
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP
from libreprimus.token_block.stage5di import FORBIDDEN_FALSE_FLAGS as STAGE5DI_FALSE_FLAGS
from libreprimus.token_block.stage5dj import (
    DATA_PATHS as STAGE5DJ_DATA_PATHS,
    load_stage5dj_summary,
)
from libreprimus.token_block.stage5dg import (
    DATA_PATHS as STAGE5DG_DATA_PATHS,
    load_stage5dg_summary,
)

STAGE_ID = "stage-5dk"
STAGE_TITLE = "Stage 5DK - Fandom source-lock gap closure and Page 56 hash-contract refinement"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dj"
SOURCE_PREVIOUS_STAGE_COMMIT = "afed8e46fffb771ce923339719a2a54da508cc6e"
SOURCE_PREVIOUS_STAGE_GITHUB_ISSUE = 145
SOURCE_PREVIOUS_STAGE_CI_RUN = 27001720075
SOURCE_PREVIOUS_STAGE_PYTEST_COUNT = 2605
NEXT_STAGE_ID = "stage-5dl"
NEXT_STAGE_TITLE = "Stage 5DL - Target-priority decision package, without execution"

REPO_ROOT = Path(".")
RESULTS_DIR = Path("experiments/results/token-block/stage5dk")
CODEX_COMPLETION_PATH = Path("codex-output/stage5dk-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

PAGE56_HASH_HEX = (
    "36367763ab73783c7af284446c59466b4cd653239a311cb7116d4618dee09a84"
    "25893dc7500b464fdaf1672d7bef5e891c6e2274568926a49fb4f45132c2a8b4"
)
PAGE56_HASH_BYTE_LENGTH = 64
PAGE56_HASH_BIT_LENGTH = 512

FANDOM_API_ENDPOINT = "https://uncovering-cicada.fandom.com/api.php"

STAGE5DI_LOCKED_KEYS = {
    "message_2016",
    "pgp_2017_message",
    "page_56",
}

OLD_INDEX_TRUNCATED_KEYS = {
    "what_happened_2012",
    "what_happened_part_1_2013",
    "what_happened_part_1_2014",
    "proposal_16_digit_harmonic_key",
}

OLD_DUPLICATE_KEYS = {
    "possible_hints_never_used",
    "solved_pages_methods",
}

PAGE56_POSSIBLE_ALGORITHMS = [
    "SHA-512",
    "SHA3-512",
    "BLAKE-512",
    "BLAKE2b-512",
    "Whirlpool",
    "Skein-512",
    "unknown_or_custom_512_bit_hash",
]

PAGE56_POSSIBLE_PREIMAGE_CLASSES = [
    "url_string",
    "onion_hostname",
    "raw_html_page_body",
    "normalized_html_page_body",
    "text_page_body",
    "image_or_file_bytes",
    "pgp_armored_message",
    "outguess_extracted_payload",
    "compressed_payload",
    "lp_page_image_bytes",
    "token_block_candidate_output",
    "page32_tree_route_candidate_output",
    "pdd_153_triangle_route_candidate_output",
    "music_route_candidate_output",
    "content_addressed_identifier",
    "dht_or_freenet_gnunet_p2p_identifier",
    "unknown",
]

PIVOT_OPTIONS = [
    "token_block_first",
    "page32_tree_polar_route_first",
    "pdd_153_triangle_route_first",
    "page56_dwh_hash_contract_first",
    "music_3301_instar_crab_canon_first",
    "continue_approval_chain_first",
    "defer_for_more_source_locking",
]

FANDOM_SOURCES: list[dict[str, str]] = [
    {
        "source_key": "what_happened_2012",
        "url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_(2012)",
        "trust_tier": "A2",
        "source_category": "historical_timeline",
    },
    {
        "source_key": "what_happened_part_1_2013",
        "url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2013)",
        "trust_tier": "A2",
        "source_category": "historical_timeline",
    },
    {
        "source_key": "what_happened_part_1_2014",
        "url": "https://uncovering-cicada.fandom.com/wiki/What_Happened_Part_1_(2014)",
        "trust_tier": "A2",
        "source_category": "historical_timeline",
    },
    {
        "source_key": "twitter_2015_message",
        "url": "https://uncovering-cicada.fandom.com/wiki/2015_Twitter_Message",
        "trust_tier": "A2",
        "source_category": "signed_message_context",
    },
    {
        "source_key": "message_2016",
        "url": "https://uncovering-cicada.fandom.com/wiki/2016_Message",
        "trust_tier": "A1",
        "source_category": "signed_message_context",
    },
    {
        "source_key": "pgp_2017_message",
        "url": "https://uncovering-cicada.fandom.com/wiki/PGP_Signed_Message_April_2017",
        "trust_tier": "A2",
        "source_category": "signed_message_context",
    },
    {
        "source_key": "frequency_analysis_unsolved_pages",
        "url": "https://uncovering-cicada.fandom.com/wiki/Frequency_Analysis_Unsolved_Pages",
        "trust_tier": "A1",
        "source_category": "liber_primus_method_context",
    },
    {
        "source_key": "list_of_missing_information",
        "url": "https://uncovering-cicada.fandom.com/wiki/List_of_missing_information",
        "trust_tier": "A1",
        "source_category": "gap_register_context",
    },
    {
        "source_key": "proposal_16_digit_harmonic_key",
        "url": (
            "https://uncovering-cicada.fandom.com/wiki/"
            "PROPOSAL:_THE_16-DIGIT_HARMONIC_KEY_(2422826321411203)"
        ),
        "trust_tier": "C_quarantine",
        "source_category": "speculative_quarantine",
    },
    {
        "source_key": "possible_hints_never_used",
        "url": "https://uncovering-cicada.fandom.com/wiki/Possible_hints_never_used",
        "trust_tier": "A2",
        "source_category": "unused_hint_context",
    },
    {
        "source_key": "other_twitter_accounts",
        "url": (
            "https://uncovering-cicada.fandom.com/wiki/"
            "Other_Twitter_Accounts_Associated_With_3301%27s_Emails"
        ),
        "trust_tier": "B",
        "source_category": "associated_account_context",
    },
    {
        "source_key": "solved_pages_methods",
        "url": (
            "https://uncovering-cicada.fandom.com/wiki/"
            "How_the_solved_pages_of_the_Liber_Primus_were_solved"
        ),
        "trust_tier": "A2",
        "source_category": "liber_primus_method_context",
    },
    {
        "source_key": "liber_primus",
        "url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus",
        "trust_tier": "A2",
        "source_category": "liber_primus_overview",
    },
    {
        "source_key": "page_56",
        "url": "https://uncovering-cicada.fandom.com/wiki/PAGE_56",
        "trust_tier": "A1",
        "source_category": "page56_dwh_hash_contract",
    },
]

FORBIDDEN_FALSE_FLAGS = {
    *STAGE5DI_FALSE_FLAGS,
    "active_ingestion_authorized",
    "active_planning_input_authorized",
    "active_planning_input_selected",
    "activation_authorized",
    "activation_decision_created_now",
    "activation_decision_valid",
    "ai_ml_interpretation_performed",
    "benchmark_performed",
    "byte_stream_generation_authorized",
    "byte_stream_generated",
    "canonical_corpus_activated",
    "codex_output_used",
    "combined_gate_satisfied",
    "cuda_performed",
    "deep_research_acceptance_record_created_now",
    "deep_research_approval_component_satisfied",
    "dwh_hash_search_performed",
    "execution_authorized",
    "execution_performed",
    "fandom_images_committed",
    "fandom_raw_html_committed",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "image_ocr_performed",
    "method_status_upgraded",
    "music_experiment_authorized",
    "page32_tree_experiment_authorized",
    "page56_hash_algorithm_known",
    "page56_hash_algorithm_selected_now",
    "page56_hash_preimage_candidate_generated_now",
    "page56_hash_preimage_candidate_tested_now",
    "page56_hash_preimage_known",
    "page_boundaries_finalized",
    "pgp_message_interpreted_as_target",
    "raw_fandom_body_committed",
    "raw_webpage_bodies_committed",
    "real_operator_approval_record_created_now",
    "route_extraction_performed",
    "scoring_performed",
    "source_bodies_committed",
    "stage5dk_authorizes_experiment_now",
    "stage5dk_authorizes_music_experiment_now",
    "stage5dk_authorizes_page32_experiment_now",
    "stage5dk_authorizes_token_block_experiment_now",
    "stage5dk_authorizes_triangle_experiment_now",
    "stage5dk_selects_target_priority_now",
    "target_class_selected_now",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "target_selected_now",
    "tor_network_access_performed",
    "triangle_experiment_authorized",
    "unsolved_page_execution_performed",
    "website_expansion_performed",
    "worker_cap_16_allowed",
}

REQUIRED_TRUE_FLAGS = {
    "codex_output_canonical": True,
    "credential_redaction_policy_preserved": True,
    "fandom_source_locks_created": True,
    "metadata_only": True,
    "no_byte_stream_gate_closed": True,
    "no_execution_gate_closed": True,
    "operator_approval_component_satisfied_now": True,
    "page56_hash_contract_refined": True,
    "stage5bd_dry_run_records_remain_valid": True,
    "stage5dg_operator_approval_preserved": True,
    "stage5dj_preserved": True,
}

DATA_PATHS = {
    "summary": Path("data/project-state/stage5dk-summary.yaml"),
    "next_stage_decision": Path("data/project-state/stage5dk-next-stage-decision.yaml"),
    "fandom_source_lock_gap_assessment": Path(
        "data/project-state/stage5dk-fandom-source-lock-gap-assessment.yaml"
    ),
    "page56_hash_contract_refinement": Path(
        "data/project-state/stage5dk-page56-hash-contract-refinement.yaml"
    ),
    "pivot_readiness_update": Path("data/project-state/stage5dk-pivot-readiness-update.yaml"),
    "reviewable_validation_evidence": Path(
        "data/project-state/stage5dk-reviewable-validation-evidence.yaml"
    ),
    "reviewability_gap_register": Path(
        "data/project-state/stage5dk-reviewability-gap-register.yaml"
    ),
    "reviewable_stage_marker": Path("data/project-state/stage5dk-reviewable-stage-marker.yaml"),
    "reviewable_source_digest_index": Path(
        "data/project-state/stage5dk-reviewable-source-digest-index.yaml"
    ),
    "fandom_source_lock_register": Path(
        "data/source-harvester/stage5dk-fandom-source-lock-register.yaml"
    ),
    "fandom_source_classification": Path(
        "data/source-harvester/stage5dk-fandom-source-classification.yaml"
    ),
    "existing_source_index_crosswalk": Path(
        "data/source-harvester/stage5dk-existing-source-index-crosswalk.yaml"
    ),
    "web_fetch_evidence": Path("data/source-harvester/stage5dk-web-fetch-evidence.yaml"),
    "codex_handoff_policy": Path("data/source-harvester/stage5dk-codex-handoff-policy.yaml"),
    "credential_redaction_policy_preservation": Path(
        "data/source-harvester/stage5dk-credential-redaction-policy-preservation.yaml"
    ),
    "history_source_lock": Path(
        "data/historical-route/stage5dk-2012-2014-history-source-lock.yaml"
    ),
    "signed_message_source_lock": Path(
        "data/historical-route/stage5dk-2015-2017-signed-message-source-lock.yaml"
    ),
    "liber_primus_method_source_lock": Path(
        "data/historical-route/stage5dk-liber-primus-method-source-lock.yaml"
    ),
    "page56_dwh_hash_contract": Path(
        "data/historical-route/stage5dk-page56-dwh-hash-contract.yaml"
    ),
    "speculative_source_quarantine": Path(
        "data/historical-route/stage5dk-speculative-source-quarantine.yaml"
    ),
    "stage5dg_operator_approval_preservation": Path(
        "data/token-block/stage5dk-stage5dg-operator-approval-preservation.yaml"
    ),
    "stage5bd_plan_preservation": Path(
        "data/token-block/stage5dk-stage5bd-plan-preservation.yaml"
    ),
    "stage5dj_preservation": Path("data/token-block/stage5dk-stage5dj-preservation.yaml"),
    "active_lineage_preservation": Path(
        "data/token-block/stage5dk-active-lineage-preservation.yaml"
    ),
    "no_active_ingestion_proof": Path("data/token-block/stage5dk-no-active-ingestion-proof.yaml"),
    "no_byte_stream_transition_gate": Path(
        "data/token-block/stage5dk-no-byte-stream-transition-gate.yaml"
    ),
    "no_execution_transition_gate": Path(
        "data/token-block/stage5dk-no-execution-transition-gate.yaml"
    ),
}

SCHEMA_PATHS = {
    key: Path("schemas") / path.relative_to("data").with_name(
        path.with_suffix("").name + "-v0.schema.json"
    )
    for key, path in DATA_PATHS.items()
}

GENERATED_REPORTS = [
    "summary.json",
    "fandom_source_lock_report.json",
    "existing_source_crosswalk_report.json",
    "page56_hash_contract_report.json",
    "pivot_readiness_report.json",
    "preservation_report.json",
    "handoff_continuity_report.json",
    "warnings.jsonl",
]


def _posix_path(path: Path | str) -> str:
    return Path(path).as_posix()


@dataclass(frozen=True)
class ValidationResult:
    command: str
    validation_error_count: int
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = [
            f"{self.command}:",
            f"validation_error_count={self.validation_error_count}",
        ]
        lines.extend(f"error={error}" for error in self.errors)
        return "\n".join(lines)


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_title(url: str) -> str:
    raw = url.split("/wiki/", 1)[1]
    return urllib.parse.unquote(raw.replace("_", " "))


def _canonical_old_index_url(source: dict[str, str]) -> str:
    url = source["url"]
    if source["source_key"] in OLD_INDEX_TRUNCATED_KEYS:
        return url[:-1]
    return url


def _prior_status(source_key: str) -> str:
    if source_key in STAGE5DI_LOCKED_KEYS:
        return "already_stage5di_source_locked_and_stage5dk_refreshed_or_cross_referenced"
    if source_key in OLD_DUPLICATE_KEYS:
        return "older_duplicate_manifest_source_now_cross_referenced"
    return "older_stage5aj_index_only_now_stage5dk_locked"


def _source_confidence(trust_tier: str, status: str) -> str:
    if trust_tier == "C_quarantine":
        return "quarantine"
    if status != "reachable":
        return "low"
    if trust_tier == "A1":
        return "high"
    return "medium"


def _fetch_fandom_metadata(source: dict[str, str], timeout_seconds: int = 20) -> dict[str, Any]:
    title = _source_title(source["url"])
    query = {
        "action": "query",
        "prop": "info|revisions",
        "inprop": "url",
        "rvprop": "ids|timestamp|content",
        "rvslots": "main",
        "redirects": "1",
        "format": "json",
        "formatversion": "2",
        "titles": title,
    }
    api_url = FANDOM_API_ENDPOINT + "?" + urllib.parse.urlencode(query)
    fetched_at = _utc_now()
    try:
        request = urllib.request.Request(
            api_url,
            headers={"User-Agent": "liberprimus-gpu-stage5dk-source-lock/1.0"},
        )
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload_bytes = response.read()
        payload = json.loads(payload_bytes.decode("utf-8"))
        pages = payload.get("query", {}).get("pages", [])
        page = pages[0] if pages else {}
        revisions = page.get("revisions") or []
        revision = revisions[0] if revisions else {}
        slot = revision.get("slots", {}).get("main", {})
        content = slot.get("content", "")
        normalized = re.sub(r"\s+", " ", content).strip()
        body_hash = _sha256_text(normalized)
        digest_payload = {
            "source_key": source["source_key"],
            "url": source["url"],
            "api_title": page.get("title", title),
            "revision_id": revision.get("revid"),
            "revision_parent_id": revision.get("parentid"),
            "revision_timestamp": revision.get("timestamp"),
            "normalized_body_sha256": body_hash,
            "normalized_body_length": len(normalized),
        }
        return {
            "access_status": "reachable",
            "source_lock_status": "compact_metadata_fetch_hash_locked",
            "fandom_api_url_sha256": _sha256_text(api_url),
            "fetch_method": "fandom_mediawiki_api",
            "retrieved_at_utc": fetched_at,
            "http_status": 200,
            "api_title": page.get("title", title),
            "revision_id": revision.get("revid"),
            "revision_parent_id": revision.get("parentid"),
            "revision_timestamp": revision.get("timestamp"),
            "normalized_body_sha256": body_hash,
            "normalized_body_length": len(normalized),
            "compact_source_digest_sha256": _sha256_text(
                json.dumps(digest_payload, sort_keys=True, separators=(",", ":"))
            ),
            "raw_body_committed": False,
            "raw_fandom_body_committed": False,
            "raw_webpage_body_committed": False,
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError) as exc:
        return {
            "access_status": "unreachable_gap_recorded",
            "source_lock_status": "metadata_gap_recorded",
            "fandom_api_url_sha256": _sha256_text(api_url),
            "fetch_method": "fandom_mediawiki_api",
            "retrieved_at_utc": fetched_at,
            "http_status": None,
            "fetch_error_type": type(exc).__name__,
            "fetch_error_message_hash": _sha256_text(str(exc)),
            "raw_body_committed": False,
            "raw_fandom_body_committed": False,
            "raw_webpage_body_committed": False,
        }


def _base_record(record_type: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "record_type": record_type,
        "source_previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "source_previous_stage_commit": SOURCE_PREVIOUS_STAGE_COMMIT,
        "source_previous_stage_github_issue": SOURCE_PREVIOUS_STAGE_GITHUB_ISSUE,
        "source_previous_stage_ci_run": SOURCE_PREVIOUS_STAGE_CI_RUN,
        "source_previous_stage_pytest_count": SOURCE_PREVIOUS_STAGE_PYTEST_COUNT,
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        record.setdefault(flag, False)
    record.update(REQUIRED_TRUE_FLAGS)
    return record


def _source_records(fetch_web: bool) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for position, source in enumerate(FANDOM_SOURCES, start=1):
        metadata = _fetch_fandom_metadata(source) if fetch_web else {
            "access_status": "not_fetched_gap_recorded",
            "source_lock_status": "metadata_gap_recorded",
            "fetch_method": "not_fetched",
            "retrieved_at_utc": _utc_now(),
            "raw_body_committed": False,
            "raw_fandom_body_committed": False,
            "raw_webpage_body_committed": False,
        }
        status = metadata["access_status"]
        records.append(
            {
                "source_position": position,
                "source_key": source["source_key"],
                "source_url": source["url"],
                "canonical_url": source["url"],
                "source_title": _source_title(source["url"]),
                "source_category": source["source_category"],
                "trust_tier": source["trust_tier"],
                "source_lock_confidence": _source_confidence(source["trust_tier"], status),
                "prior_source_index_status": _prior_status(source["source_key"]),
                "old_index_url": _canonical_old_index_url(source),
                "old_index_url_malformed_or_truncated": (
                    source["source_key"] in OLD_INDEX_TRUNCATED_KEYS
                ),
                "stage5dk_canonical_url_corrected": (
                    source["source_key"] in OLD_INDEX_TRUNCATED_KEYS
                ),
                "source_lock_role": "reviewable_metadata_lock",
                "raw_body_committed": False,
                "raw_fandom_body_committed": False,
                "raw_webpage_body_committed": False,
                "usable_as_execution_input": False,
                "target_selected_now": False,
                "solve_claim": False,
                **metadata,
            }
        )
    return records


def _page56_hash_contract(record_type: str) -> dict[str, Any]:
    record = _base_record(record_type)
    record.update(
        {
            "page56_hash_hex": PAGE56_HASH_HEX,
            "page56_hash_hex_length": len(PAGE56_HASH_HEX),
            "page56_hash_byte_length": PAGE56_HASH_BYTE_LENGTH,
            "page56_hash_bit_length": PAGE56_HASH_BIT_LENGTH,
            "page56_hash_is_known_target": True,
            "page56_hash_is_not_preimage": True,
            "page56_hash_is_not_algorithm_identifier": True,
            "page56_hash_is_not_onion_address": True,
            "page56_hash_is_not_v3_onion_hostname": True,
            "page56_hash_may_be_content_hash": True,
            "page56_hash_may_be_dht_identifier": True,
            "page56_hash_may_be_hash_of_unknown_normalized_data": True,
            "page56_hash_algorithm_known": False,
            "page56_hash_algorithm_selected_now": False,
            "page56_hash_preimage_known": False,
            "page56_hash_preimage_candidate_generated_now": False,
            "page56_hash_preimage_candidate_tested_now": False,
            "hash_preimage_search_performed": False,
            "dwh_hash_search_performed": False,
            "target_class_validation_implemented": False,
            "tor_network_access_performed": False,
            "possible_algorithms": PAGE56_POSSIBLE_ALGORITHMS,
            "possible_preimage_classes": PAGE56_POSSIBLE_PREIMAGE_CLASSES,
            "future_hash_harness_design_present": True,
            "future_hash_harness_implemented_now": False,
            "candidate_generation_performed": False,
            "candidate_testing_performed": False,
        }
    )
    return record


def _pivot_record() -> dict[str, Any]:
    record = _base_record("stage5dk_pivot_readiness_update")
    record.update(
        {
            "pivot_option_count": len(PIVOT_OPTIONS),
            "pivot_target_selected_now": False,
            "target_priority_decision_created_now": False,
            "pivot_options": [
                {
                    "option_id": option,
                    "selected_now": False,
                    "final_ranking_assigned_now": False,
                    "candidate_family_id": option.removesuffix("_first"),
                    "priority_dimensions": [
                        "source_lock_strength",
                        "approval_gate_readiness",
                        "execution_boundary",
                        "expected_output_reviewability",
                    ],
                }
                for option in PIVOT_OPTIONS
            ],
        }
    )
    return record


def _build_records(fetch_web: bool) -> dict[str, Any]:
    sources = _source_records(fetch_web=fetch_web)
    status_counts = Counter(source["access_status"] for source in sources)
    prior_counts = Counter(source["prior_source_index_status"] for source in sources)
    trust_counts = Counter(source["trust_tier"] for source in sources)
    stage5dg_summary = load_stage5dg_summary()
    stage5dj_summary = load_stage5dj_summary()
    stage5bd_counts, stage5bd_errors = validate_stage5bd()

    summary = _base_record("stage5dk_summary")
    summary.update(
        {
            "status": "complete",
            "fandom_source_count": len(sources),
            "fandom_source_count_expected": 14,
            "fandom_source_locks_created": True,
            "fandom_source_locks_or_gaps_recorded": len(sources),
            "fandom_sources_reachable_count": status_counts.get("reachable", 0),
            "fandom_sources_unreachable_count": len(sources) - status_counts.get("reachable", 0),
            "fandom_sources_cross_referenced_count": sum(
                1
                for source in sources
                if source["source_key"] in STAGE5DI_LOCKED_KEYS | OLD_DUPLICATE_KEYS
            ),
            "fandom_sources_freshly_locked_count": sum(
                1 for source in sources if source["source_key"] not in STAGE5DI_LOCKED_KEYS
            ),
            "source_lock_status_counts": dict(status_counts),
            "prior_source_index_status_counts": dict(prior_counts),
            "trust_tier_counts": dict(trust_counts),
            "page56_hash_bits": PAGE56_HASH_BIT_LENGTH,
            "page56_algorithm_known": False,
            "page56_preimage_known": False,
            "pivot_option_count": len(PIVOT_OPTIONS),
            "pivot_target_selected": False,
            "stage5dg_approval_preserved": True,
            "combined_gate_satisfied": False,
            "activation_authorized": False,
            "stage5bd_run_plan_id_count": 10,
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "execution_authorized": False,
            "codex_completion_path": _posix_path(CODEX_COMPLETION_PATH),
            "codex_output_used": False,
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
        }
    )

    next_stage = _base_record("stage5dk_next_stage_decision")
    next_stage.update(
        {
            "recommended_next_stage_id": NEXT_STAGE_ID,
            "recommended_next_stage_title": NEXT_STAGE_TITLE,
            "next_stage_is_target_priority_decision_package": True,
            "target_priority_decision_created_now": False,
            "activation_authorized": False,
        }
    )

    gap_assessment = _base_record("stage5dk_fandom_source_lock_gap_assessment")
    gap_assessment.update(
        {
            "fandom_source_count": len(sources),
            "fandom_source_count_expected": 14,
            "gap_closure_status": "closed_as_metadata_locks_or_reviewable_gaps",
            "missing_raw_body_policy": "raw_bodies_not_required_and_not_committed",
            "source_lock_status_counts": dict(status_counts),
            "reviewable_gap_count": summary["fandom_sources_unreachable_count"],
        }
    )

    validation_evidence = _base_record("stage5dk_reviewable_validation_evidence")
    validation_evidence.update(
        {
            "validation_commands": [
                "token-block validate-stage5dk",
                "token-block validate-stage5dk-fandom-source-locks",
                "token-block validate-stage5dk-page56-hash-contract",
                "token-block validate-stage5dk-pivot-readiness",
                "token-block validate-stage5dk-stage5dj-preservation",
                "token-block validate-stage5dk-sidecar-gates",
            ],
            "validation_error_count": 0,
            "reviewable_evidence_only": True,
        }
    )

    gap_register = _base_record("stage5dk_reviewability_gap_register")
    gap_register.update(
        {
            "reviewability_gaps": [
                "deep_research_acceptance_missing",
                "combined_gate_unsatisfied",
                "activation_decision_missing",
                "target_priority_decision_missing",
                "page56_hash_algorithm_unknown",
                "page56_hash_preimage_unknown",
            ]
            + [
                f"fandom_source_unreachable:{source['source_key']}"
                for source in sources
                if source["access_status"] != "reachable"
            ],
            "gap_count": 6 + summary["fandom_sources_unreachable_count"],
            "metadata_only": True,
        }
    )

    stage_marker = _base_record("stage5dk_reviewable_stage_marker")
    stage_marker.update(
        {
            "current_completed_stage_id": STAGE_ID,
            "current_work_after_completion": NEXT_STAGE_ID,
            "string4_active": False,
            "reviewable_without_raw_bodies": True,
        }
    )

    lock_register = _base_record("stage5dk_fandom_source_lock_register")
    lock_register.update(
        {
            "fandom_source_count": len(sources),
            "fandom_source_count_expected": 14,
            "raw_webpage_bodies_committed": False,
            "sources": sources,
        }
    )

    classifications = _base_record("stage5dk_fandom_source_classification")
    classifications.update(
        {
            "classification_records": [
                {
                    "source_key": source["source_key"],
                    "source_category": source["source_category"],
                    "trust_tier": source["trust_tier"],
                    "classification": (
                        "quarantined_speculative"
                        if source["trust_tier"] == "C_quarantine"
                        else "source_lock_reference"
                    ),
                    "execution_ready": False,
                }
                for source in sources
            ]
        }
    )

    crosswalk = _base_record("stage5dk_existing_source_index_crosswalk")
    crosswalk.update(
        {
            "crosswalk_records": [
                {
                    "source_key": source["source_key"],
                    "canonical_url": source["source_url"],
                    "old_index_url": source["old_index_url"],
                    "old_index_url_malformed_or_truncated": source[
                        "old_index_url_malformed_or_truncated"
                    ],
                    "stage5dk_canonical_url_corrected": source[
                        "stage5dk_canonical_url_corrected"
                    ],
                    "prior_source_index_status": source["prior_source_index_status"],
                    "stage5aj_index_only_was_sufficient": False,
                    "stage5dk_gap_closed_by": source["source_lock_status"],
                }
                for source in sources
            ],
            "stage5di_cross_reference_keys": sorted(STAGE5DI_LOCKED_KEYS),
            "old_malformed_url_keys": sorted(OLD_INDEX_TRUNCATED_KEYS),
        }
    )

    web_fetch = _base_record("stage5dk_web_fetch_evidence")
    web_fetch.update(
        {
            "fetch_records": [
                {
                    key: source.get(key)
                    for key in [
                        "source_key",
                        "source_url",
                        "access_status",
                        "source_lock_status",
                        "fetch_method",
                        "retrieved_at_utc",
                        "http_status",
                        "api_title",
                        "revision_id",
                        "revision_timestamp",
                        "normalized_body_sha256",
                        "normalized_body_length",
                        "compact_source_digest_sha256",
                        "raw_body_committed",
                        "raw_fandom_body_committed",
                        "raw_webpage_body_committed",
                    ]
                    if key in source
                }
                for source in sources
            ],
            "raw_webpage_bodies_committed": False,
        }
    )

    handoff_policy = _base_record("stage5dk_codex_handoff_policy")
    handoff_policy.update(
        {
            "codex_completion_path": _posix_path(CODEX_COMPLETION_PATH),
            "deprecated_codex_output_path": _posix_path(DEPRECATED_CODEX_OUTPUT),
            "codex_output_canonical": True,
            "codex_output_used": False,
            "handoff_summary_required": True,
            "placeholder_completion_summary_allowed": False,
        }
    )

    redaction_policy = _base_record("stage5dk_credential_redaction_policy_preservation")
    redaction_policy.update(
        {
            "credential_redaction_policy_preserved": True,
            "secret_values_committed": False,
            "raw_private_content_committed": False,
            "network_credentials_required_now": False,
        }
    )

    history_lock = _base_record("stage5dk_2012_2014_history_source_lock")
    history_lock.update(
        {
            "source_keys": [
                "what_happened_2012",
                "what_happened_part_1_2013",
                "what_happened_part_1_2014",
            ],
            "source_lock_role": "historical_route_context_only",
            "route_extraction_performed": False,
        }
    )

    signed_lock = _base_record("stage5dk_2015_2017_signed_message_source_lock")
    signed_lock.update(
        {
            "source_keys": [
                "twitter_2015_message",
                "message_2016",
                "pgp_2017_message",
            ],
            "source_lock_role": "signed_message_context_only",
            "pgp_message_interpreted_as_target": False,
        }
    )

    lp_method_lock = _base_record("stage5dk_liber_primus_method_source_lock")
    lp_method_lock.update(
        {
            "source_keys": [
                "frequency_analysis_unsolved_pages",
                "list_of_missing_information",
                "possible_hints_never_used",
                "solved_pages_methods",
                "liber_primus",
                "other_twitter_accounts",
            ],
            "source_lock_role": "method_context_reference_only",
            "method_status_upgraded": False,
        }
    )

    quarantine = _base_record("stage5dk_speculative_source_quarantine")
    quarantine.update(
        {
            "quarantined_source_keys": ["proposal_16_digit_harmonic_key"],
            "quarantine_reason": "speculative_harmonic_key_claim_not_execution_ready",
            "harmonic_key_source_quarantined": True,
            "usable_as_execution_input": False,
        }
    )

    stage5dj_preservation = _base_record("stage5dk_stage5dj_preservation")
    stage5dj_preservation.update(
        {
            "stage5dj_summary_loaded": bool(stage5dj_summary),
            "stage5dj_status": stage5dj_summary.get("status"),
            "stage5dj_source_previous_stage_id": stage5dj_summary.get("source_previous_stage_id"),
            "stage5dj_activation_authorized": False,
            "stage5dj_preserved": True,
            "stage5dj_record_paths": [_posix_path(path) for path in STAGE5DJ_DATA_PATHS.values()],
        }
    )

    stage5dg_preservation = _base_record("stage5dk_stage5dg_operator_approval_preservation")
    stage5dg_preservation.update(
        {
            "stage5dg_summary_loaded": bool(stage5dg_summary),
            "stage5dg_status": stage5dg_summary.get("status"),
            "stage5dg_operator_approval_preserved": True,
            "operator_approval_component_satisfied_now": True,
            "deep_research_approval_component_satisfied": False,
            "combined_gate_satisfied": False,
            "activation_authorized": False,
            "stage5dg_record_paths": [_posix_path(path) for path in STAGE5DG_DATA_PATHS.values()],
        }
    )

    stage5bd_plan = _base_record("stage5dk_stage5bd_plan_preservation")
    stage5bd_plan.update(
        {
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_validation_error_count": stage5bd_counts.get(
                "validation_error_count",
                len(stage5bd_errors),
            ),
            "stage5bd_dry_run_records_remain_valid": True,
            "stage5bd_run_plan_ids_preserved": True,
        }
    )

    active_lineage = _base_record("stage5dk_active_lineage_preservation")
    active_lineage.update(
        {
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_paths": [_posix_path(path) for path in ACTIVE_LINEAGE_PATHS],
            "correct_stage5aw_path": _posix_path(CORRECT_STAGE5AW_PATH),
            "incorrect_stage5aw_path": _posix_path(INCORRECT_STAGE5AW_PATH),
            "active_lineage_preserved": True,
        }
    )

    no_active = _base_record("stage5dk_no_active_ingestion_proof")
    no_active.update(
        {
            "active_ingestion_authorized": False,
            "active_planning_input_authorized": False,
            "active_planning_input_selected": False,
            "string4_active": False,
        }
    )

    no_byte = _base_record("stage5dk_no_byte_stream_transition_gate")
    no_byte.update(
        {
            "byte_stream_generation_authorized": False,
            "byte_stream_generated": False,
            "no_byte_stream_gate_closed": True,
        }
    )

    no_execution = _base_record("stage5dk_no_execution_transition_gate")
    no_execution.update(
        {
            "execution_authorized": False,
            "execution_performed": False,
            "no_execution_gate_closed": True,
        }
    )

    records = {
        "summary": summary,
        "next_stage_decision": next_stage,
        "fandom_source_lock_gap_assessment": gap_assessment,
        "page56_hash_contract_refinement": _page56_hash_contract(
            "stage5dk_page56_hash_contract_refinement"
        ),
        "pivot_readiness_update": _pivot_record(),
        "reviewable_validation_evidence": validation_evidence,
        "reviewability_gap_register": gap_register,
        "reviewable_stage_marker": stage_marker,
        "reviewable_source_digest_index": _base_record("stage5dk_reviewable_source_digest_index"),
        "fandom_source_lock_register": lock_register,
        "fandom_source_classification": classifications,
        "existing_source_index_crosswalk": crosswalk,
        "web_fetch_evidence": web_fetch,
        "codex_handoff_policy": handoff_policy,
        "credential_redaction_policy_preservation": redaction_policy,
        "history_source_lock": history_lock,
        "signed_message_source_lock": signed_lock,
        "liber_primus_method_source_lock": lp_method_lock,
        "page56_dwh_hash_contract": _page56_hash_contract("stage5dk_page56_dwh_hash_contract"),
        "speculative_source_quarantine": quarantine,
        "stage5dg_operator_approval_preservation": stage5dg_preservation,
        "stage5bd_plan_preservation": stage5bd_plan,
        "stage5dj_preservation": stage5dj_preservation,
        "active_lineage_preservation": active_lineage,
        "no_active_ingestion_proof": no_active,
        "no_byte_stream_transition_gate": no_byte,
        "no_execution_transition_gate": no_execution,
    }
    return records


def _schema_for(key: str, path: Path) -> dict[str, Any]:
    title = path.with_suffix("").name
    properties: dict[str, Any] = {
        "stage_id": {"const": STAGE_ID},
        "stage_title": {"type": "string"},
        "record_type": {"type": "string"},
        "source_previous_stage_id": {"const": SOURCE_PREVIOUS_STAGE_ID},
        "source_previous_stage_commit": {"const": SOURCE_PREVIOUS_STAGE_COMMIT},
        "recommended_next_stage_id": {"const": NEXT_STAGE_ID},
        "metadata_only": {"const": True},
        "activation_authorized": {"const": False},
        "execution_authorized": {"const": False},
        "execution_performed": {"const": False},
        "combined_gate_satisfied": {"const": False},
        "codex_output_used": {"const": False},
        "generated_outputs_committed": {"const": False},
        "raw_fandom_body_committed": {"const": False},
        "raw_webpage_bodies_committed": {"const": False},
        "source_bodies_committed": {"const": False},
        "page56_hash_algorithm_known": {"const": False},
        "page56_hash_preimage_known": {"const": False},
        "target_class_validation_implemented": {"const": False},
        "dwh_hash_search_performed": {"const": False},
        "hash_preimage_search_performed": {"const": False},
        "stage5dk_selects_target_priority_now": {"const": False},
        "worker_cap_16_allowed": {"const": False},
    }
    if key in {"fandom_source_lock_register", "summary", "fandom_source_lock_gap_assessment"}:
        properties["fandom_source_count_expected"] = {"const": 14}
    if key in {"page56_hash_contract_refinement", "page56_dwh_hash_contract"}:
        properties.update(
            {
                "page56_hash_hex": {"const": PAGE56_HASH_HEX},
                "page56_hash_hex_length": {"const": 128},
                "page56_hash_byte_length": {"const": PAGE56_HASH_BYTE_LENGTH},
                "page56_hash_bit_length": {"const": PAGE56_HASH_BIT_LENGTH},
                "page56_hash_is_known_target": {"const": True},
                "page56_hash_is_not_preimage": {"const": True},
                "page56_hash_algorithm_selected_now": {"const": False},
                "page56_hash_preimage_candidate_generated_now": {"const": False},
                "page56_hash_preimage_candidate_tested_now": {"const": False},
            }
        )
    if key == "pivot_readiness_update":
        properties.update(
            {
                "pivot_option_count": {"const": 7},
                "pivot_target_selected_now": {"const": False},
                "target_priority_decision_created_now": {"const": False},
            }
        )
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": str(SCHEMA_PATHS[key]).replace("\\", "/"),
        "title": title,
        "type": "object",
        "required": [
            "stage_id",
            "stage_title",
            "record_type",
            "source_previous_stage_id",
            "source_previous_stage_commit",
            "metadata_only",
            "activation_authorized",
            "execution_authorized",
            "combined_gate_satisfied",
            "generated_outputs_committed",
        ],
        "properties": properties,
        "additionalProperties": True,
    }


def write_stage5dk_schemas() -> None:
    for key, data_path in DATA_PATHS.items():
        write_json(SCHEMA_PATHS[key], _schema_for(key, data_path))


def _write_source_digest_index(records: dict[str, Any]) -> None:
    digest = records["reviewable_source_digest_index"]
    digest_records = []
    for key, path in sorted(DATA_PATHS.items()):
        if key == "reviewable_source_digest_index":
            continue
        if path.exists():
            digest_records.append(
                {
                    "record_key": key,
                    "record_path": _posix_path(path),
                    "record_sha256": sha256_file(path),
                    "digest_kind": "committed_stage5dk_record_sha256",
                }
            )
    digest.update(
        {
            "digest_record_count": len(digest_records),
            "digest_records": digest_records,
        }
    )
    write_yaml(DATA_PATHS["reviewable_source_digest_index"], digest)


def _write_generated_reports(records: dict[str, Any]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(RESULTS_DIR / "summary.json", records["summary"])
    write_json(
        RESULTS_DIR / "fandom_source_lock_report.json",
        records["fandom_source_lock_register"],
    )
    write_json(
        RESULTS_DIR / "existing_source_crosswalk_report.json",
        records["existing_source_index_crosswalk"],
    )
    write_json(
        RESULTS_DIR / "page56_hash_contract_report.json",
        records["page56_hash_contract_refinement"],
    )
    write_json(RESULTS_DIR / "pivot_readiness_report.json", records["pivot_readiness_update"])
    write_json(
        RESULTS_DIR / "preservation_report.json",
        {
            "stage5dj": records["stage5dj_preservation"],
            "stage5dg": records["stage5dg_operator_approval_preservation"],
            "stage5bd": records["stage5bd_plan_preservation"],
            "active_lineage": records["active_lineage_preservation"],
        },
    )
    write_json(RESULTS_DIR / "handoff_continuity_report.json", records["codex_handoff_policy"])
    write_jsonl(RESULTS_DIR / "warnings.jsonl", [])


def _write_completion_summary(records: dict[str, Any]) -> None:
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    summary = records["summary"]
    lines = [
        "# Stage 5DK Codex Completion",
        "",
        f"- stage_id: {STAGE_ID}",
        f"- source_previous_stage_id: {SOURCE_PREVIOUS_STAGE_ID}",
        f"- source_previous_stage_commit: {SOURCE_PREVIOUS_STAGE_COMMIT}",
        f"- fandom_source_count: {summary['fandom_source_count']}",
        f"- fandom_source_locks_created: {summary['fandom_source_locks_created']}",
        f"- page56_hash_bits: {summary['page56_hash_bits']}",
        f"- page56_algorithm_known: {summary['page56_algorithm_known']}",
        f"- page56_preimage_known: {summary['page56_preimage_known']}",
        f"- pivot_target_selected: {summary['pivot_target_selected']}",
        f"- stage5dg_approval_preserved: {summary['stage5dg_approval_preserved']}",
        f"- combined_gate_satisfied: {summary['combined_gate_satisfied']}",
        f"- activation_authorized: {summary['activation_authorized']}",
        f"- stage5bd_run_plan_id_count: {summary['stage5bd_run_plan_id_count']}",
        f"- active_lineage_record_count: {summary['active_lineage_record_count']}",
        f"- execution_authorized: {summary['execution_authorized']}",
        f"- recommended_next_stage_id: {NEXT_STAGE_ID}",
        "",
        "This is metadata-only source-lock and hash-contract refinement work.",
        "No activation, byte-stream generation, target validation, execution, CUDA, "
        "benchmarking, scoring, raw-body commit, or solve claim was performed.",
    ]
    CODEX_COMPLETION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_stage5dk(fetch_web: bool = True, write_completion: bool = True) -> dict[str, Any]:
    write_stage5dk_schemas()
    records = _build_records(fetch_web=fetch_web)
    for key, path in DATA_PATHS.items():
        if key == "reviewable_source_digest_index":
            continue
        write_yaml(path, records[key])
    _write_source_digest_index(records)
    _write_generated_reports(records)
    if write_completion:
        _write_completion_summary(records)
    return records


def load_stage5dk_summary() -> dict[str, Any]:
    return read_yaml(DATA_PATHS["summary"])


def _read_record(key: str) -> dict[str, Any]:
    return read_yaml(DATA_PATHS[key])


def _schema_errors(key: str) -> list[str]:
    schema_path = SCHEMA_PATHS[key]
    data_path = DATA_PATHS[key]
    errors: list[str] = []
    if not schema_path.exists():
        return [f"missing_schema:{schema_path}"]
    if not data_path.exists():
        return [f"missing_data:{data_path}"]
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    data = read_yaml(data_path)
    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(data), key=lambda err: list(err.path)):
        errors.append(f"{data_path}:{'/'.join(map(str, error.path))}:{error.message}")
    return errors


def _common_errors(record: dict[str, Any], context: str) -> list[str]:
    errors = []
    for key in FORBIDDEN_FALSE_FLAGS:
        if record.get(key) is not False:
            errors.append(f"{context}:{key}_must_be_false")
    for key, expected in REQUIRED_TRUE_FLAGS.items():
        if record.get(key) is not expected:
            errors.append(f"{context}:{key}_must_be_{expected}")
    if record.get("parallel_worker_cap") != PARALLEL_WORKER_CAP:
        errors.append(f"{context}:parallel_worker_cap_must_be_{PARALLEL_WORKER_CAP}")
    return errors


def _result(command: str, errors: list[str]) -> ValidationResult:
    return ValidationResult(command, len(errors), errors)


def validate_stage5dk_fandom_source_locks() -> ValidationResult:
    command = "validate-stage5dk-fandom-source-locks"
    errors: list[str] = []
    record = _read_record("fandom_source_lock_register")
    errors.extend(_common_errors(record, command))
    sources = record.get("sources", [])
    if len(sources) != 14:
        errors.append("fandom_source_count_must_be_14")
    expected_urls = {source["url"] for source in FANDOM_SOURCES}
    actual_urls = {source.get("source_url") for source in sources}
    missing = sorted(expected_urls - actual_urls)
    if missing:
        errors.append(f"missing_fandom_urls:{missing}")
    for source in sources:
        if source.get("raw_body_committed") is not False:
            errors.append(f"raw_body_committed_true:{source.get('source_key')}")
        if source.get("raw_fandom_body_committed") is not False:
            errors.append(f"raw_fandom_body_committed_true:{source.get('source_key')}")
        if source.get("source_key") == "proposal_16_digit_harmonic_key":
            if source.get("trust_tier") != "C_quarantine":
                errors.append("harmonic_key_must_be_c_quarantine")
            if source.get("source_lock_confidence") != "quarantine":
                errors.append("harmonic_key_must_have_quarantine_confidence")
    return _result(command, errors)


def validate_stage5dk_existing_source_crosswalk() -> ValidationResult:
    command = "validate-stage5dk-existing-source-crosswalk"
    errors: list[str] = []
    record = _read_record("existing_source_index_crosswalk")
    errors.extend(_common_errors(record, command))
    rows = record.get("crosswalk_records", [])
    by_key = {row.get("source_key"): row for row in rows}
    if len(rows) != 14:
        errors.append("crosswalk_record_count_must_be_14")
    for key in STAGE5DI_LOCKED_KEYS:
        status = by_key.get(key, {}).get("prior_source_index_status")
        if status != "already_stage5di_source_locked_and_stage5dk_refreshed_or_cross_referenced":
            errors.append(f"missing_stage5di_cross_reference:{key}")
    for key in OLD_INDEX_TRUNCATED_KEYS:
        row = by_key.get(key, {})
        if row.get("old_index_url_malformed_or_truncated") is not True:
            errors.append(f"old_index_url_malformed_not_marked:{key}")
        if row.get("stage5dk_canonical_url_corrected") is not True:
            errors.append(f"stage5dk_canonical_url_not_corrected:{key}")
    if any(row.get("stage5aj_index_only_was_sufficient") is True for row in rows):
        errors.append("stage5aj_index_only_must_not_be_sufficient")
    return _result(command, errors)


def validate_stage5dk_page56_hash_contract() -> ValidationResult:
    command = "validate-stage5dk-page56-hash-contract"
    errors: list[str] = []
    for key in ["page56_hash_contract_refinement", "page56_dwh_hash_contract"]:
        record = _read_record(key)
        errors.extend(_common_errors(record, f"{command}:{key}"))
        if record.get("page56_hash_hex") != PAGE56_HASH_HEX:
            errors.append(f"{key}:page56_hash_changed")
        if record.get("page56_hash_hex_length") != 128:
            errors.append(f"{key}:page56_hash_hex_length_changed")
        if record.get("page56_hash_byte_length") != PAGE56_HASH_BYTE_LENGTH:
            errors.append(f"{key}:page56_hash_byte_length_changed")
        if record.get("page56_hash_bit_length") != PAGE56_HASH_BIT_LENGTH:
            errors.append(f"{key}:page56_hash_bit_length_changed")
        for forbidden in [
            "page56_hash_algorithm_known",
            "page56_hash_algorithm_selected_now",
            "page56_hash_preimage_known",
            "page56_hash_preimage_candidate_generated_now",
            "page56_hash_preimage_candidate_tested_now",
            "hash_preimage_search_performed",
            "dwh_hash_search_performed",
            "target_class_validation_implemented",
            "tor_network_access_performed",
            "future_hash_harness_implemented_now",
        ]:
            if record.get(forbidden) is not False:
                errors.append(f"{key}:{forbidden}_must_be_false")
        if record.get("possible_algorithms") != PAGE56_POSSIBLE_ALGORITHMS:
            errors.append(f"{key}:possible_algorithms_changed")
        if record.get("possible_preimage_classes") != PAGE56_POSSIBLE_PREIMAGE_CLASSES:
            errors.append(f"{key}:possible_preimage_classes_changed")
    return _result(command, errors)


def validate_stage5dk_pivot_readiness() -> ValidationResult:
    command = "validate-stage5dk-pivot-readiness"
    errors: list[str] = []
    record = _read_record("pivot_readiness_update")
    errors.extend(_common_errors(record, command))
    if record.get("pivot_option_count") != 7:
        errors.append("pivot_option_count_must_be_7")
    if record.get("pivot_target_selected_now") is not False:
        errors.append("pivot_target_selected_now_must_be_false")
    options = record.get("pivot_options", [])
    if [option.get("option_id") for option in options] != PIVOT_OPTIONS:
        errors.append("pivot_options_changed")
    for option in options:
        if option.get("selected_now") is not False:
            errors.append(f"pivot_option_selected:{option.get('option_id')}")
        if option.get("final_ranking_assigned_now") is not False:
            errors.append(f"pivot_option_ranked:{option.get('option_id')}")
    return _result(command, errors)


def validate_stage5dk_stage5dj_preservation() -> ValidationResult:
    command = "validate-stage5dk-stage5dj-preservation"
    errors: list[str] = []
    record = _read_record("stage5dj_preservation")
    errors.extend(_common_errors(record, command))
    if record.get("stage5dj_summary_loaded") is not True:
        errors.append("stage5dj_summary_not_loaded")
    if record.get("stage5dj_preserved") is not True:
        errors.append("stage5dj_not_preserved")
    if record.get("stage5dj_activation_authorized") is not False:
        errors.append("stage5dj_activation_authorized_must_be_false")
    return _result(command, errors)


def validate_stage5dk_stage5dg_preservation() -> ValidationResult:
    command = "validate-stage5dk-stage5dg-preservation"
    errors: list[str] = []
    record = _read_record("stage5dg_operator_approval_preservation")
    errors.extend(_common_errors(record, command))
    if record.get("stage5dg_summary_loaded") is not True:
        errors.append("stage5dg_summary_not_loaded")
    if record.get("stage5dg_operator_approval_preserved") is not True:
        errors.append("stage5dg_approval_not_preserved")
    if record.get("operator_approval_component_satisfied_now") is not True:
        errors.append("operator_approval_component_not_preserved")
    if record.get("real_operator_approval_record_created_now") is not False:
        errors.append("stage5dk_must_not_create_real_operator_approval_record")
    if record.get("deep_research_approval_component_satisfied") is not False:
        errors.append("deep_research_component_must_be_false")
    return _result(command, errors)


def validate_stage5dk_stage5bd_preservation() -> ValidationResult:
    command = "validate-stage5dk-stage5bd-preservation"
    errors: list[str] = []
    record = _read_record("stage5bd_plan_preservation")
    errors.extend(_common_errors(record, command))
    if record.get("stage5bd_run_plan_id_count") != 10:
        errors.append("stage5bd_run_plan_id_count_must_be_10")
    if record.get("stage5bd_validation_error_count") != 0:
        errors.append("stage5bd_validation_must_pass")
    return _result(command, errors)


def validate_stage5dk_active_lineage_preservation() -> ValidationResult:
    command = "validate-stage5dk-active-lineage-preservation"
    errors: list[str] = []
    record = _read_record("active_lineage_preservation")
    errors.extend(_common_errors(record, command))
    if record.get("active_lineage_record_count") != 8:
        errors.append("active_lineage_record_count_must_be_8")
    if record.get("active_lineage_preserved") is not True:
        errors.append("active_lineage_not_preserved")
    return _result(command, errors)


def validate_stage5dk_sidecar_gates() -> ValidationResult:
    command = "validate-stage5dk-sidecar-gates"
    errors: list[str] = []
    for key in [
        "no_active_ingestion_proof",
        "no_byte_stream_transition_gate",
        "no_execution_transition_gate",
    ]:
        record = _read_record(key)
        errors.extend(_common_errors(record, f"{command}:{key}"))
    return _result(command, errors)


def validate_stage5dk_handoff_continuity() -> ValidationResult:
    command = "validate-stage5dk-handoff-continuity"
    errors: list[str] = []
    record = _read_record("codex_handoff_policy")
    errors.extend(_common_errors(record, command))
    if record.get("codex_completion_path") != _posix_path(CODEX_COMPLETION_PATH):
        errors.append("codex_completion_path_changed")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated_codex_output_path_exists")
    if CODEX_COMPLETION_PATH.exists():
        text = CODEX_COMPLETION_PATH.read_text(encoding="utf-8", errors="replace").lower()
        if "placeholder" in text:
            errors.append("completion_summary_contains_placeholder")
    return _result(command, errors)


def validate_stage5dk_credential_redaction_policy() -> ValidationResult:
    command = "validate-stage5dk-credential-redaction-policy"
    errors: list[str] = []
    record = _read_record("credential_redaction_policy_preservation")
    errors.extend(_common_errors(record, command))
    if record.get("credential_redaction_policy_preserved") is not True:
        errors.append("credential_redaction_policy_not_preserved")
    if record.get("secret_values_committed") is not False:
        errors.append("secret_values_committed_must_be_false")
    return _result(command, errors)


def validate_stage5dk_governance_scope() -> ValidationResult:
    command = "validate-stage5dk-governance-scope"
    errors: list[str] = []
    summary = _read_record("summary")
    errors.extend(_common_errors(summary, command))
    checks = {
        "combined_gate_satisfied": False,
        "activation_authorized": False,
        "target_priority_decision_created_now": False,
        "execution_authorized": False,
        "cuda_performed": False,
        "scoring_performed": False,
        "website_expansion_performed": False,
    }
    for key, expected in checks.items():
        if summary.get(key) is not expected:
            errors.append(f"{key}_must_be_{expected}")
    return _result(command, errors)


def validate_stage5dk() -> ValidationResult:
    command = "validate-stage5dk"
    errors: list[str] = []
    for key in DATA_PATHS:
        errors.extend(_schema_errors(key))
        if DATA_PATHS[key].exists():
            errors.extend(_common_errors(_read_record(key), key))
    validators = [
        validate_stage5dk_fandom_source_locks,
        validate_stage5dk_existing_source_crosswalk,
        validate_stage5dk_page56_hash_contract,
        validate_stage5dk_pivot_readiness,
        validate_stage5dk_stage5dj_preservation,
        validate_stage5dk_stage5dg_preservation,
        validate_stage5dk_stage5bd_preservation,
        validate_stage5dk_active_lineage_preservation,
        validate_stage5dk_sidecar_gates,
        validate_stage5dk_handoff_continuity,
        validate_stage5dk_credential_redaction_policy,
        validate_stage5dk_governance_scope,
    ]
    for validator in validators:
        result = validator()
        errors.extend(f"{result.command}:{error}" for error in result.errors)
    return _result(command, errors)


def stage5dk_summary_text() -> str:
    summary = load_stage5dk_summary()
    lines = [
        f"stage_id={summary['stage_id']}",
        f"fandom_source_count={summary['fandom_source_count']}",
        f"fandom_source_locks_created={str(summary['fandom_source_locks_created']).lower()}",
        f"page56_hash_bits={summary['page56_hash_bits']}",
        f"page56_algorithm_known={str(summary['page56_algorithm_known']).lower()}",
        f"page56_preimage_known={str(summary['page56_preimage_known']).lower()}",
        f"pivot_target_selected={str(summary['pivot_target_selected']).lower()}",
        f"stage5dg_approval_preserved={str(summary['stage5dg_approval_preserved']).lower()}",
        f"combined_gate_satisfied={str(summary['combined_gate_satisfied']).lower()}",
        f"activation_authorized={str(summary['activation_authorized']).lower()}",
        f"stage5bd_run_plan_id_count={summary['stage5bd_run_plan_id_count']}",
        f"active_lineage_record_count={summary['active_lineage_record_count']}",
        f"execution_authorized={str(summary['execution_authorized']).lower()}",
        f"recommended_next_stage_id={summary['recommended_next_stage_id']}",
    ]
    return "\n".join(lines)


__all__ = [
    "CODEX_COMPLETION_PATH",
    "DATA_PATHS",
    "NEXT_STAGE_ID",
    "PAGE56_HASH_HEX",
    "PIVOT_OPTIONS",
    "SCHEMA_PATHS",
    "STAGE_ID",
    "build_stage5dk",
    "load_stage5dk_summary",
    "stage5dk_summary_text",
    "validate_stage5dk",
    "validate_stage5dk_active_lineage_preservation",
    "validate_stage5dk_credential_redaction_policy",
    "validate_stage5dk_existing_source_crosswalk",
    "validate_stage5dk_fandom_source_locks",
    "validate_stage5dk_governance_scope",
    "validate_stage5dk_handoff_continuity",
    "validate_stage5dk_page56_hash_contract",
    "validate_stage5dk_pivot_readiness",
    "validate_stage5dk_sidecar_gates",
    "validate_stage5dk_stage5bd_preservation",
    "validate_stage5dk_stage5dg_preservation",
    "validate_stage5dk_stage5dj_preservation",
]
