"""Stage 5DS expanded music/Ouroboros/token-block static source-lock records."""

from __future__ import annotations

import hashlib
import json
import math
import mimetypes
import re
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from libreprimus.operator_console.source_browser.loaders import build_source_index
from libreprimus.operator_console.source_browser.validators import (
    source_browser_summary,
    validate_manual_records,
    validate_source_index,
)
from libreprimus.token_block.models import PRIMARY_ALPHABET, read_yaml, sha256_file, write_json, write_yaml
from libreprimus.token_block.preflight_runner.stage5bd import validate_stage5bd
from libreprimus.token_block.stage5ca import ACTIVE_LINEAGE_PATHS
from libreprimus.token_block.stage5cm import PARALLEL_WORKER_CAP, SECRET_PATTERNS
from libreprimus.token_block.stage5dj import _parse_id3, _parse_pdf, _probe_kind
from libreprimus.token_block.stage5dr import DATA_PATHS as STAGE5DR_DATA_PATHS
from libreprimus.token_block.stage5dr import validate_stage5dr

STAGE_ID = "stage-5ds"
STAGE_TITLE = (
    "Stage 5DS - Expanded Music / Ouroboros / self-reference / token-block "
    "static-context source-lock addendum, without execution"
)
PROMPT_TYPE = "codex_metadata_implementation"
SOURCE_PREVIOUS_STAGE_ID = "stage-5dr"
SOURCE_PREVIOUS_STAGE_COMMIT = "9d15b12b3b4b34b2029fbb1ff46544e50eaed762"
SOURCE_PREVIOUS_ISSUE = 153
SOURCE_PREVIOUS_CI_RUN = 27112689258
NEXT_STAGE_ID = "stage-5dt"
NEXT_STAGE_TITLE = "Stage 5DT - Operator Console source-review readiness planning, without execution"

COMMUNITY_ROOT = Path("third_party/CicadaMusic/community-theory")
ORIGINAL_MUSIC_ROOT = Path("third_party/CicadaMusic")
CODEX_COMPLETION_PATH = Path("codex-output/stage5ds-codex-completion.md")
DEPRECATED_CODEX_OUTPUT = Path("codex_output")

PROJECT_STATE_DIR = Path("data/project-state")
SOURCE_HARVESTER_DIR = Path("data/source-harvester")
HISTORICAL_ROUTE_DIR = Path("data/historical-route")
TOKEN_BLOCK_DIR = Path("data/token-block")

DATA_PATHS: dict[str, Path] = {
    "summary": PROJECT_STATE_DIR / "stage5ds-summary.yaml",
    "next_stage_decision": PROJECT_STATE_DIR / "stage5ds-next-stage-decision.yaml",
    "stage5dr_preservation": PROJECT_STATE_DIR / "stage5ds-stage5dr-preservation.yaml",
    "reviewable_validation_evidence": PROJECT_STATE_DIR
    / "stage5ds-reviewable-validation-evidence.yaml",
    "reviewability_gap_register": PROJECT_STATE_DIR / "stage5ds-reviewability-gap-register.yaml",
    "scope_control": PROJECT_STATE_DIR / "stage5ds-scope-control.yaml",
    "chatgpt_context_update_summary": PROJECT_STATE_DIR
    / "stage5ds-chatgpt-context-update-summary.yaml",
    "operator_inserted_addendum_routing": PROJECT_STATE_DIR
    / "stage5ds-operator-inserted-addendum-routing.yaml",
    "source_browser_loadability_summary": PROJECT_STATE_DIR
    / "stage5ds-source-browser-loadability-summary.yaml",
    "evidence_status_classification_policy": PROJECT_STATE_DIR
    / "stage5ds-evidence-status-classification-policy.yaml",
    "music_source_lock_register": SOURCE_HARVESTER_DIR
    / "stage5ds-music-community-theory-source-lock-register.yaml",
    "music_file_inventory": SOURCE_HARVESTER_DIR
    / "stage5ds-music-community-theory-file-inventory.yaml",
    "music_messages_source_lock": SOURCE_HARVESTER_DIR
    / "stage5ds-music-messages-source-lock.yaml",
    "music_message_attachment_anchor_index": SOURCE_HARVESTER_DIR
    / "stage5ds-music-message-attachment-anchor-index.yaml",
    "music_audio_metadata_locks": SOURCE_HARVESTER_DIR
    / "stage5ds-music-audio-metadata-locks.yaml",
    "music_pdf_metadata_locks": SOURCE_HARVESTER_DIR
    / "stage5ds-music-pdf-metadata-locks.yaml",
    "music_image_source_locks": SOURCE_HARVESTER_DIR / "stage5ds-music-image-source-locks.yaml",
    "original_cicada_music_stage5dj_crosslink": SOURCE_HARVESTER_DIR
    / "stage5ds-original-cicada-music-stage5dj-crosslink.yaml",
    "ouroboros_web_source_lock_register": SOURCE_HARVESTER_DIR
    / "stage5ds-ouroboros-web-source-lock-register.yaml",
    "raw_source_noncommit_proof": SOURCE_HARVESTER_DIR
    / "stage5ds-raw-source-noncommit-proof.yaml",
    "codex_handoff_policy": SOURCE_HARVESTER_DIR / "stage5ds-codex-handoff-policy.yaml",
    "credential_redaction_policy_preservation": SOURCE_HARVESTER_DIR
    / "stage5ds-credential-redaction-policy-preservation.yaml",
    "stage5dg_preservation": TOKEN_BLOCK_DIR / "stage5ds-stage5dg-preservation.yaml",
    "stage5bd_preservation": TOKEN_BLOCK_DIR / "stage5ds-stage5bd-preservation.yaml",
    "active_lineage_preservation": TOKEN_BLOCK_DIR
    / "stage5ds-active-lineage-preservation.yaml",
    "no_active_ingestion_proof": TOKEN_BLOCK_DIR / "stage5ds-no-active-ingestion-proof.yaml",
    "no_byte_stream_transition_proof": TOKEN_BLOCK_DIR
    / "stage5ds-no-byte-stream-transition-proof.yaml",
    "no_token_block_execution_proof": TOKEN_BLOCK_DIR
    / "stage5ds-no-token-block-execution-proof.yaml",
    "token_block_static_machine_code_scope_control": TOKEN_BLOCK_DIR
    / "stage5ds-token-block-static-machine-code-scope-control.yaml",
    "operator_console_stage5dr_preservation": TOKEN_BLOCK_DIR
    / "stage5ds-operator-console-stage5dr-preservation.yaml",
}

MUSIC_CANDIDATE_PATHS: dict[str, Path] = {
    "instar_parable_id3_gp_product_candidate": HISTORICAL_ROUTE_DIR
    / "stage5ds-instar-parable-id3-gp-product-candidate-v1.yaml",
    "instar_title_761_duration_167_bridge": HISTORICAL_ROUTE_DIR
    / "stage5ds-instar-title-761-duration-167-bridge-v1.yaml",
    "interconnectedness_772_277_table_canon_number": HISTORICAL_ROUTE_DIR
    / "stage5ds-interconnectedness-772-277-table-canon-number-v1.yaml",
    "interconnectedness_table_canon_29_note_gp_mapping": HISTORICAL_ROUTE_DIR
    / "stage5ds-interconnectedness-table-canon-29-note-gp-mapping-v1.yaml",
    "instar_205_beats_prime205_1259_poem_line": HISTORICAL_ROUTE_DIR
    / "stage5ds-instar-205-beats-prime205-1259-poem-line-v1.yaml",
    "instar_csharp_gsharp_hexachord_axis": HISTORICAL_ROUTE_DIR
    / "stage5ds-instar-csharp-gsharp-hexachord-axis-v1.yaml",
    "instar_reverse_section_augmentation_canon": HISTORICAL_ROUTE_DIR
    / "stage5ds-instar-reverse-section-augmentation-canon-v1.yaml",
    "interconnectedness_guitar_tab_prime_fret_strings": HISTORICAL_ROUTE_DIR
    / "stage5ds-interconnectedness-guitar-tab-prime-fret-strings-v1.yaml",
    "interconnectedness_547_beats_137_measures": HISTORICAL_ROUTE_DIR
    / "stage5ds-interconnectedness-547-beats-137-measures-v0.yaml",
    "music_transform_grammar_for_cipher_methods": HISTORICAL_ROUTE_DIR
    / "stage5ds-music-transform-grammar-for-cipher-methods-v1.yaml",
    "music_direct_pitch_substitution_quarantine": HISTORICAL_ROUTE_DIR
    / "stage5ds-music-direct-pitch-substitution-quarantine-v0.yaml",
}

OUROBOROS_CANDIDATE_PATHS: dict[str, Path] = {
    "ouroboros_gp_167_music_cycle": HISTORICAL_ROUTE_DIR
    / "stage5ds-ouroboros-gp-167-music-cycle-candidate-v0.yaml",
    "pdd153_ouroboros_167_mod153_offset14": HISTORICAL_ROUTE_DIR
    / "stage5ds-pdd153-ouroboros-167-mod153-offset14-candidate-v0.yaml",
    "pdd153_56311_ouroboric_cycle": HISTORICAL_ROUTE_DIR
    / "stage5ds-pdd153-56311-ouroboric-cycle-candidate-v0.yaml",
    "ouroboros_see_also_transform_context": HISTORICAL_ROUTE_DIR
    / "stage5ds-ouroboros-see-also-transform-context-v0.yaml",
    "ouroboros_see_also_gp_arithmetic_scan": HISTORICAL_ROUTE_DIR
    / "stage5ds-ouroboros-see-also-gp-arithmetic-scan-v0.yaml",
    "strange_loop_gp463_page32_bridge": HISTORICAL_ROUTE_DIR
    / "stage5ds-strange-loop-gp463-page32-bridge-candidate-v0.yaml",
    "self_reference_gp529_square23": HISTORICAL_ROUTE_DIR
    / "stage5ds-self-reference-gp529-square23-candidate-v0.yaml",
    "self_fulfilling_prophecy_gp841_square29": HISTORICAL_ROUTE_DIR
    / "stage5ds-self-fulfilling-prophecy-gp841-square29-candidate-v0.yaml",
    "infinite_loop_gp409_page33_dot_bridge": HISTORICAL_ROUTE_DIR
    / "stage5ds-infinite-loop-gp409-page33-dot-bridge-candidate-v0.yaml",
    "quine_fixed_point_self_reproduction": HISTORICAL_ROUTE_DIR
    / "stage5ds-quine-fixed-point-self-reproduction-candidate-v0.yaml",
    "mobius_ouroboros_one_boundary_transform": HISTORICAL_ROUTE_DIR
    / "stage5ds-mobius-ouroboros-one-boundary-transform-candidate-v1.yaml",
    "escher_dragon_tail_bite_self_reference": HISTORICAL_ROUTE_DIR
    / "stage5ds-escher-dragon-tail-bite-self-reference-candidate-v0.yaml",
    "endless_knot_interdependence_no_beginning": HISTORICAL_ROUTE_DIR
    / "stage5ds-endless-knot-interdependence-no-beginning-candidate-v0.yaml",
    "enso_circle_open_closed_boundary": HISTORICAL_ROUTE_DIR
    / "stage5ds-enso-circle-open-closed-boundary-candidate-v0.yaml",
    "three_hares_rotational_shared_parts": HISTORICAL_ROUTE_DIR
    / "stage5ds-three-hares-rotational-shared-parts-candidate-v0.yaml",
    "valknut_triple_knot_runic_context": HISTORICAL_ROUTE_DIR
    / "stage5ds-valknut-triple-knot-runic-context-candidate-v0.yaml",
    "amphisbaena_bidirectional_serpent_route": HISTORICAL_ROUTE_DIR
    / "stage5ds-amphisbaena-bidirectional-serpent-route-candidate-v0.yaml",
}

TOKEN_STATIC_PATHS: dict[str, Path] = {
    "machine_code_static_sanity": HISTORICAL_ROUTE_DIR
    / "stage5ds-token-block-machine-code-static-sanity-candidate-v0.yaml",
    "base_neighbor_static_scan": HISTORICAL_ROUTE_DIR
    / "stage5ds-token-block-base-neighbor-static-scan-v0.yaml",
    "vm_or_table_surface": HISTORICAL_ROUTE_DIR
    / "stage5ds-token-block-vm-or-table-surface-candidate-v0.yaml",
    "quine_context_crosslink": HISTORICAL_ROUTE_DIR
    / "stage5ds-token-block-quine-context-crosslink-v0.yaml",
}

DATA_PATHS.update(MUSIC_CANDIDATE_PATHS)
DATA_PATHS.update(OUROBOROS_CANDIDATE_PATHS)
DATA_PATHS.update(TOKEN_STATIC_PATHS)

SCHEMA_PATHS: dict[str, Path] = {
    "summary": Path("schemas/project-state/stage5ds-summary-v0.schema.json"),
    "next_stage_decision": Path("schemas/project-state/stage5ds-next-stage-decision-v0.schema.json"),
    "scope_control": Path("schemas/project-state/stage5ds-scope-control-v0.schema.json"),
    "reviewable_validation_evidence": Path(
        "schemas/project-state/stage5ds-reviewable-validation-evidence-v0.schema.json"
    ),
    "chatgpt_context_update_summary": Path(
        "schemas/project-state/stage5ds-chatgpt-context-update-summary-v0.schema.json"
    ),
    "music_source_lock_register": Path(
        "schemas/source-harvester/"
        "stage5ds-music-community-theory-source-lock-register-v0.schema.json"
    ),
    "music_file_inventory": Path(
        "schemas/source-harvester/stage5ds-music-community-theory-file-inventory-v0.schema.json"
    ),
    "music_message_attachment_anchor_index": Path(
        "schemas/source-harvester/"
        "stage5ds-music-message-attachment-anchor-index-v0.schema.json"
    ),
    "music_candidate_record": Path(
        "schemas/historical-route/stage5ds-music-candidate-record-v0.schema.json"
    ),
    "ouroboros_transform_context_record": Path(
        "schemas/historical-route/stage5ds-ouroboros-transform-context-record-v0.schema.json"
    ),
    "token_block_static_context_record": Path(
        "schemas/historical-route/stage5ds-token-block-static-context-record-v0.schema.json"
    ),
    "token_block_static_machine_code_scope_control": Path(
        "schemas/token-block/stage5ds-token-block-static-machine-code-scope-control-v0.schema.json"
    ),
}

FORBIDDEN_FALSE_FLAGS = {
    "activation_authorized_now",
    "activation_decision_valid_now",
    "active_ingestion_performed",
    "active_manifest_registry_updated",
    "active_planning_input_authorized_now",
    "active_planning_input_selected_now",
    "active_token_block_manifest_changed",
    "alberti_html_executed_now",
    "audio_stego_performed",
    "benchmark_performed",
    "branch_enumeration_performed",
    "byte_stream_generation_authorized_now",
    "canonical_corpus_active",
    "codex_output_used",
    "combined_approval_gate_satisfied_now",
    "cuda_execution_performed",
    "decode_attempt_performed",
    "decryption_attempt_performed_now",
    "direct_music_substitution_executed",
    "disk_cipher_execution_performed_now",
    "dwh_hash_search_performed",
    "execution_authorized_now",
    "execution_performed",
    "full_cartesian_product_enumerated",
    "generated_outputs_committed",
    "hash_preimage_search_performed",
    "hidden_content_image_forensics_performed",
    "html_tool_executed_now",
    "image_forensics_performed",
    "known_plaintext_attack_performed_now",
    "machine_code_execution_performed_now",
    "mayfly_route_extraction_performed_now",
    "midi_route_extraction_performed_now",
    "mp3stego_execution_performed",
    "music_route_extraction_performed_now",
    "native_code_execution_performed_now",
    "network_target_validation_performed_now",
    "ocr_performed",
    "openpuff_execution_performed",
    "operator_readiness_decision_created_now",
    "page32_route_extraction_performed_now",
    "page56_hash_preimage_tested_now",
    "page_boundaries_finalized",
    "pdf_ocr_or_hidden_content_rendering_performed",
    "pivot_target_selected_now",
    "probability_claim_accepted_as_validated",
    "raw_files_committed_now",
    "raw_third_party_files_committed",
    "real_byte_stream_generated",
    "route_extraction_performed_now",
    "scoring_performed",
    "semantic_image_interpretation_performed",
    "solve_claim",
    "spectrogram_stego_performed",
    "target_class_validation_implemented",
    "target_priority_decision_created_now",
    "token_block_experiment_executed",
    "token_block_variant_byte_streams_generated",
    "tor_network_access_performed",
    "triangle_route_extraction_performed_now",
    "variant_byte_streams_generated",
    "variant_materialisation_performed",
    "vm_bytecode_execution_performed_now",
    "website_expansion_performed",
}

REQUIRED_STAGE_FLAGS = {
    "metadata_only": True,
    "source_lock_only": True,
    "puzzle_execution_allowed": False,
    "solve_claim": False,
}

GP_PHRASE_VALUES = {
    "LIKE THE INSTAR TUNNELING TO THE SURFACE": 1259,
    "WE MUST SHED OUR OWN CIRCUMFERENCES": 1031,
    "FIND THE DIVINITY WITHIN AND EMERGE": 1229,
    "THE INSTAR EMERGENCE": 761,
    "INTERCONNECTEDNESS": 772,
    "DIVINITY": 376,
    "OUROBOROS": 167,
    "STRANGE LOOP": 463,
    "SELF REFERENCE": 529,
    "SELF FULFILLING PROPHECY": 841,
    "INFINITE LOOP": 409,
    "THREE HARES": 401,
    "MOBIUS STRIP": 423,
    "ENSO": 156,
    "AUTOCANNIBALISM": 751,
}

STAGE5DS_CONTEXT_SECTION = """\
## Stage 5DS expanded music/Ouroboros/token-block static addendum

- Stage 5DS source-locks expanded CicadaMusic/community-theory files, music arithmetic candidates, Ouroboros/self-reference transform context, and token-block primary60 static machine-code sanity only.
- Stage 5DS is metadata/source-lock only: no target selection, active ingestion, byte-stream generation, audio/stego/OCR/image forensics, route extraction, machine/VM execution, scoring, CUDA, or solve claim.
- The operator inserted this addendum before Stage 5DR's planned source-review readiness stage; the next stage is Stage 5DT source-review readiness planning.
- Preserve the Stage 5DR GUI follow-up state: the details panel is now right-side/right-dock usability work, not an authorization surface.
- Music candidates remain review-only. Direct pitch substitution is quarantined. Guitar-tab prime strings and GP/product facts need future independent review before any bounded planning.
- Ouroboros/self-reference/Quine/Mobius records are symbolic transform context only, not route extraction evidence.
- Token-block static context records preserve the 32x8 primary60 facts, first 16 bytes `cbe7a7ba61ed7eb75cf99cdef704b7d4`, and byte-stream SHA-256 metadata only; no generated byte stream is committed or executed.
"""

EXPECTED_MUSIC_FILES = {
    "messages.txt",
    "READ ME FIRST - Cicada 3301 Music Guide.pdf",
    "Interconnectedness (6-18-2025).pdf",
    "Interconnectedness (10-11-2025).pdf",
    "Interconnectedness Prime Groups (10-12-2025).pdf",
    "Interconnectedness, Guitar Tab (10-14-2025).pdf",
    "Interconnectedness Canon (10-15-2025).pdf",
    "Interconnectedness Crab Canon (6-18-2025).pdf",
    "Potential Canon, Instar.pdf",
    "Instar Emergence (6-19-2025).mp3",
    "Interconnectedness.mp3",
}

GUITAR_FRET_STRINGS = [
    355330003553333,
    37302523,
    230032303,
    53033303,
    230303,
    333032303,
    300323,
    252323,
    32303,
    353,
    32023,
]


@dataclass
class Stage5DSValidationResult:
    validation_error_count: int
    counts: dict[str, Any]
    errors: list[str]

    def to_cli_text(self) -> str:
        lines = ["command=validate-stage5ds"]
        for key, value in self.counts.items():
            lines.append(f"{key}={_format(value)}")
        lines.append(f"validation_error_count={self.validation_error_count}")
        for error in self.errors:
            lines.append(f"error={error}")
        return "\n".join(lines)


def build_stage5ds() -> dict[str, dict[str, Any]]:
    stage5dr_result = validate_stage5dr()
    if stage5dr_result.validation_error_count:
        raise RuntimeError("Stage 5DR validation must pass before Stage 5DS")
    _stage5bd_counts, stage5bd_errors = validate_stage5bd()
    if stage5bd_errors:
        raise RuntimeError("Stage 5BD preservation validation must pass before Stage 5DS")

    _write_schemas()
    inventory = _file_inventory(COMMUNITY_ROOT)
    messages = _messages_record(inventory)
    anchors = _attachment_anchors(inventory, messages)
    audio_rows = _audio_metadata_records(inventory)
    pdf_rows = _pdf_metadata_records(inventory)
    image_rows = _image_source_records(inventory)
    token_static = _token_static_summary()

    records: dict[str, dict[str, Any]] = {}
    records["music_source_lock_register"] = _music_source_lock_register(inventory)
    records["music_file_inventory"] = _music_file_inventory_record(inventory)
    records["music_messages_source_lock"] = messages
    records["music_message_attachment_anchor_index"] = _anchor_index_record(anchors)
    records["music_audio_metadata_locks"] = _metadata_collection_record(
        "stage5ds_music_audio_metadata_locks",
        "Stage 5DS community-theory MP3 metadata locks",
        audio_rows,
    )
    records["music_pdf_metadata_locks"] = _metadata_collection_record(
        "stage5ds_music_pdf_metadata_locks",
        "Stage 5DS community-theory PDF metadata locks",
        pdf_rows,
    )
    records["music_image_source_locks"] = _metadata_collection_record(
        "stage5ds_music_image_source_locks",
        "Stage 5DS community-theory image source locks",
        image_rows,
    )
    records["original_cicada_music_stage5dj_crosslink"] = _original_music_crosslink()
    records["ouroboros_web_source_lock_register"] = _ouroboros_web_source_register()
    records["raw_source_noncommit_proof"] = _raw_source_noncommit_proof(inventory)
    records["codex_handoff_policy"] = _codex_handoff_policy()
    records["credential_redaction_policy_preservation"] = _credential_redaction_policy()

    records.update(_music_candidate_records())
    records.update(_ouroboros_candidate_records())
    records.update(_token_static_records(token_static))
    records.update(_preservation_records(token_static))
    _write_records(records)

    _update_chatgpt_context()
    source_browser_record = _source_browser_loadability_summary()
    records["source_browser_loadability_summary"] = source_browser_record
    records["chatgpt_context_update_summary"] = _chatgpt_context_update_summary()
    records["operator_inserted_addendum_routing"] = _operator_routing_record()
    records["evidence_status_classification_policy"] = _evidence_status_policy()
    records["reviewability_gap_register"] = _gap_register(inventory)
    records["stage5dr_preservation"] = _stage5dr_preservation_record()
    records["reviewable_validation_evidence"] = _reviewable_validation_evidence(source_browser_record)
    records["scope_control"] = _scope_control_record()
    records["next_stage_decision"] = _next_stage_decision()
    records["summary"] = _summary_record(inventory, token_static, source_browser_record)

    _update_operational_file_map()
    _write_records(records)
    write_completion_summary()
    return records


def write_completion_summary(commit_hash: str | None = None, ci_status: str | None = None) -> None:
    summary = read_yaml(DATA_PATHS["summary"]) if DATA_PATHS["summary"].exists() else {}
    lines = [
        "# Stage 5DS Codex Completion Summary",
        "",
        f"stage_id: {STAGE_ID}",
        f"stage_title: {STAGE_TITLE}",
        f"status: {summary.get('status', 'complete')}",
        f"commit_hash: {commit_hash or summary.get('actual_starting_commit_observed') or 'pending'}",
        f"ci_status: {ci_status or 'pending'}",
        "",
        "## Counts",
        f"- music community files inventoried: {summary.get('music_community_theory_file_count')}",
        f"- music candidate records: {summary.get('music_candidate_records_created')}",
        f"- Ouroboros candidate records: {summary.get('ouroboros_candidate_records_created')}",
        f"- token-block static candidate records: {summary.get('token_block_static_candidate_records_created')}",
        f"- source browser entries loaded: {summary.get('source_browser_entries_loaded')}",
        "",
        "## Closed Gates",
        "- pivot_target_selected_now=false",
        "- byte_stream_generation_authorized_now=false",
        "- execution_performed=false",
        "- solve_claim=false",
        "- codex_output_used=false",
        "",
        "## Next",
        f"- recommended_next_stage_id: {NEXT_STAGE_ID}",
        f"- recommended_next_stage_title: {NEXT_STAGE_TITLE}",
    ]
    CODEX_COMPLETION_PATH.parent.mkdir(parents=True, exist_ok=True)
    CODEX_COMPLETION_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_stage5ds() -> Stage5DSValidationResult:
    checks = [
        validate_stage5ds_music_source_lock,
        validate_stage5ds_music_file_inventory,
        validate_stage5ds_music_message_anchors,
        validate_stage5ds_music_candidates,
        validate_stage5ds_ouroboros_context,
        validate_stage5ds_token_block_static_context,
        validate_stage5ds_chatgpt_context,
        validate_stage5ds_source_browser_loadability,
        validate_stage5ds_stage5dr_preservation,
        validate_stage5ds_stage5dg_preservation,
        validate_stage5ds_stage5bd_preservation,
        validate_stage5ds_active_lineage_preservation,
        validate_stage5ds_sidecar_gates,
        validate_stage5ds_handoff_continuity,
        validate_stage5ds_credential_redaction_policy,
        validate_stage5ds_scope_control,
    ]
    counts: dict[str, Any] = {}
    errors: list[str] = []
    for check in checks:
        result = check()
        counts.update(result.counts)
        errors.extend(result.errors)
    errors.extend(_validate_schemas())
    for key, path in DATA_PATHS.items():
        if not path.exists():
            errors.append(f"missing required Stage 5DS record {key}: {path.as_posix()}")
            continue
        payload = read_yaml(path)
        errors.extend(_validate_common_payload(path, payload))
    summary = read_yaml(DATA_PATHS["summary"]) if DATA_PATHS["summary"].exists() else {}
    counts.update(
        {
            "token_block_stage5ds_valid": not errors,
            "music_community_theory_source_lock_created": DATA_PATHS[
                "music_source_lock_register"
            ].exists(),
            "music_candidate_records_created": summary.get("music_candidate_records_created", 0),
            "ouroboros_candidate_records_created": summary.get(
                "ouroboros_candidate_records_created", 0
            ),
            "token_block_static_candidate_records_created": summary.get(
                "token_block_static_candidate_records_created", 0
            ),
            "chatgpt_context_updated": summary.get("chatgpt_context_updated", False),
            "source_browser_loadability_validated": summary.get(
                "source_browser_loadability_validated", False
            ),
            "pivot_target_selected_now": summary.get("pivot_target_selected_now", False),
            "byte_stream_generation_authorized_now": summary.get(
                "byte_stream_generation_authorized_now", False
            ),
            "execution_performed": summary.get("execution_performed", False),
            "stage5bd_run_plan_id_count": summary.get("stage5bd_run_plan_id_count", 0),
            "active_lineage_record_count": summary.get("active_lineage_record_count", 0),
            "recommended_next_stage_id": summary.get("recommended_next_stage_id", ""),
        }
    )
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_music_source_lock() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["music_source_lock_register"])
    errors = _required_false_errors(payload)
    if not payload.get("source_root_exists"):
        errors.append("community theory source root is not recorded as present")
    if payload.get("raw_source_files_committed") is not False:
        errors.append("raw_source_files_committed must be false")
    counts = {
        "music_community_theory_source_lock_created": payload.get("source_lock_created", False),
        "music_community_theory_file_count": payload.get("file_count", 0),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_music_file_inventory() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["music_file_inventory"])
    rows = payload.get("files") or []
    errors = _required_false_errors(payload)
    if not isinstance(rows, list) or not rows:
        errors.append("music file inventory must contain files")
    for row in rows:
        if len(str(row.get("sha256", ""))) != 64:
            errors.append(f"invalid sha256 for {row.get('relative_path')}")
        if row.get("raw_file_committed") is not False:
            errors.append(f"raw file committed flag not false for {row.get('relative_path')}")
    counts = {
        "music_file_inventory_count": len(rows) if isinstance(rows, list) else 0,
        "music_audio_file_count": payload.get("audio_file_count", 0),
        "music_pdf_file_count": payload.get("pdf_file_count", 0),
        "music_image_file_count": payload.get("image_file_count", 0),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_music_message_anchors() -> Stage5DSValidationResult:
    lock = _load(DATA_PATHS["music_messages_source_lock"])
    payload = _load(DATA_PATHS["music_message_attachment_anchor_index"])
    anchors = payload.get("anchors") or []
    errors = _required_false_errors(payload) + _required_false_errors(lock)
    if lock.get("messages_txt_present") and lock.get("line_count", 0) <= 0:
        errors.append("messages.txt line count must be positive when present")
    if not isinstance(anchors, list):
        errors.append("anchors must be a list")
    counts = {
        "music_message_anchor_count": len(anchors) if isinstance(anchors, list) else 0,
        "messages_txt_present": lock.get("messages_txt_present", False),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_music_candidates() -> Stage5DSValidationResult:
    errors: list[str] = []
    for path in MUSIC_CANDIDATE_PATHS.values():
        payload = _load(path)
        errors.extend(_required_false_errors(payload))
        if payload.get("candidate_status") not in {
            "source_locked_candidate_only",
            "quarantined_direct_substitution",
        }:
            errors.append(f"{path.as_posix()}: unexpected candidate status")
        if payload.get("execution_authorized_now") is not False:
            errors.append(f"{path.as_posix()}: execution_authorized_now must be false")
    product = _load(MUSIC_CANDIDATE_PATHS["instar_parable_id3_gp_product_candidate"])
    if product.get("prime_product") != 1595277641:
        errors.append("Instar parable product must equal 1595277641")
    guitar = _load(MUSIC_CANDIDATE_PATHS["interconnectedness_guitar_tab_prime_fret_strings"])
    if guitar.get("nonprime_exception", {}).get("value") != 32023:
        errors.append("guitar-tab nonprime exception 32023 must be recorded")
    quarantine = _load(MUSIC_CANDIDATE_PATHS["music_direct_pitch_substitution_quarantine"])
    if quarantine.get("direct_music_substitution_executed") is not False:
        errors.append("direct music substitution must remain unexecuted")
    counts = {"music_candidate_records_created": len(MUSIC_CANDIDATE_PATHS)}
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_ouroboros_context() -> Stage5DSValidationResult:
    errors: list[str] = []
    for path in OUROBOROS_CANDIDATE_PATHS.values():
        payload = _load(path)
        errors.extend(_required_false_errors(payload))
        if payload.get("candidate_status") != "source_locked_context_only":
            errors.append(f"{path.as_posix()}: unexpected Ouroboros candidate status")
    ouroboros = _load(OUROBOROS_CANDIDATE_PATHS["ouroboros_gp_167_music_cycle"])
    pdd = _load(OUROBOROS_CANDIDATE_PATHS["pdd153_ouroboros_167_mod153_offset14"])
    cycle = _load(OUROBOROS_CANDIDATE_PATHS["pdd153_56311_ouroboric_cycle"])
    if ouroboros.get("gp_sum") != 167:
        errors.append("Ouroboros GP sum must be 167")
    if pdd.get("offset") != 14:
        errors.append("167-153 offset must be 14")
    if cycle.get("closed_state_period") != 612:
        errors.append("PDD153 closed-state period must be 612")
    counts = {"ouroboros_candidate_records_created": len(OUROBOROS_CANDIDATE_PATHS)}
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_token_block_static_context() -> Stage5DSValidationResult:
    errors: list[str] = []
    for path in TOKEN_STATIC_PATHS.values():
        payload = _load(path)
        errors.extend(_required_false_errors(payload))
        if payload.get("candidate_status") != "source_locked_static_context_only":
            errors.append(f"{path.as_posix()}: unexpected token static status")
    scope = _load(DATA_PATHS["token_block_static_machine_code_scope_control"])
    errors.extend(_required_false_errors(scope))
    if scope.get("first_16_bytes_hex") != "cbe7a7ba61ed7eb75cf99cdef704b7d4":
        errors.append("token-block first 16 primary60 bytes mismatch")
    if scope.get("machine_code_execution_performed_now") is not False:
        errors.append("machine code execution must be false")
    counts = {
        "token_block_static_candidate_records_created": len(TOKEN_STATIC_PATHS),
        "token_block_primary60_sha256": scope.get("primary60_byte_stream_sha256", ""),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_chatgpt_context() -> Stage5DSValidationResult:
    context_path = Path("ChatGPT-ContextFile.md")
    errors: list[str] = []
    if not context_path.exists():
        errors.append("ChatGPT-ContextFile.md is missing")
        text = ""
    else:
        text = context_path.read_text(encoding="utf-8")
    for phrase in (
        "Stage 5DS expanded music/Ouroboros/token-block static addendum",
        "Stage 5DT source-review readiness planning",
        "right-side/right-dock",
        "cbe7a7ba61ed7eb75cf99cdef704b7d4",
    ):
        if phrase not in text:
            errors.append(f"ChatGPT context missing phrase: {phrase}")
    counts = {"chatgpt_context_updated": not errors}
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_source_browser_loadability() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["source_browser_loadability_summary"])
    errors = _required_false_errors(payload)
    if payload.get("source_browser_index_valid") is not True:
        errors.append("source browser index must be valid")
    if payload.get("stage5ds_entries_loaded", 0) < len(DATA_PATHS):
        errors.append("Stage 5DS entries loaded count is lower than required records")
    counts = {
        "source_browser_loadability_validated": payload.get(
            "source_browser_loadability_validated", False
        ),
        "stage5ds_entries_loaded": payload.get("stage5ds_entries_loaded", 0),
        "source_browser_entries_loaded": payload.get("source_browser_entries_loaded", 0),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_stage5dr_preservation() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["stage5dr_preservation"])
    result = validate_stage5dr()
    errors = _required_false_errors(payload)
    if result.validation_error_count:
        errors.append("Stage 5DR validation no longer passes")
    if payload.get("stage5dr_complete") is not True:
        errors.append("Stage 5DR completion must be preserved")
    counts = {
        "stage5dr_complete": payload.get("stage5dr_complete", False),
        "stage5dr_source_browser_entries_loaded": payload.get(
            "stage5dr_source_browser_entries_loaded", 0
        ),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_stage5dg_preservation() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["stage5dg_preservation"])
    errors = _required_false_errors(payload)
    if payload.get("stage5dg_operator_approval_record_preserved") is not True:
        errors.append("Stage 5DG operator approval record must be preserved")
    if payload.get("combined_approval_gate_satisfied_now") is not False:
        errors.append("combined approval gate must remain unsatisfied")
    counts = {
        "stage5dg_operator_approval_record_preserved": payload.get(
            "stage5dg_operator_approval_record_preserved", False
        ),
        "operator_approval_component_satisfied_now": payload.get(
            "operator_approval_component_satisfied_now", False
        ),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_stage5bd_preservation() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["stage5bd_preservation"])
    _counts, stage5bd_errors = validate_stage5bd()
    errors = _required_false_errors(payload) + stage5bd_errors
    if payload.get("stage5bd_run_plan_id_count") != 10:
        errors.append("Stage 5BD run plan count must remain 10")
    counts = {"stage5bd_run_plan_id_count": payload.get("stage5bd_run_plan_id_count", 0)}
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_active_lineage_preservation() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["active_lineage_preservation"])
    errors = _required_false_errors(payload)
    if payload.get("active_lineage_record_count") != 8:
        errors.append("active lineage record count must remain 8")
    counts = {"active_lineage_record_count": payload.get("active_lineage_record_count", 0)}
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_sidecar_gates() -> Stage5DSValidationResult:
    paths = (
        DATA_PATHS["no_active_ingestion_proof"],
        DATA_PATHS["no_byte_stream_transition_proof"],
        DATA_PATHS["no_token_block_execution_proof"],
    )
    errors: list[str] = []
    for path in paths:
        payload = _load(path)
        errors.extend(_required_false_errors(payload))
        if payload.get("gate_status") != "closed":
            errors.append(f"{path.as_posix()}: gate_status must be closed")
    counts = {
        "active_ingestion_performed": False,
        "byte_stream_generation_authorized_now": False,
        "token_block_experiment_executed": False,
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_handoff_continuity() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["codex_handoff_policy"])
    errors = _required_false_errors(payload)
    if payload.get("canonical_codex_handoff_root") != "codex-output":
        errors.append("canonical handoff root must be codex-output")
    if DEPRECATED_CODEX_OUTPUT.exists():
        errors.append("deprecated codex_output path must be absent")
    counts = {
        "canonical_codex_handoff_root": payload.get("canonical_codex_handoff_root", ""),
        "codex_output_used": False,
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_credential_redaction_policy() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["credential_redaction_policy_preservation"])
    errors = _required_false_errors(payload)
    if payload.get("credential_like_remote_count", 1) != 0:
        errors.append("credential-like remotes must not be present")
    if payload.get("secret_values_printed_or_committed") is not False:
        errors.append("secret values must not be printed or committed")
    counts = {
        "credential_like_remote_count": payload.get("credential_like_remote_count", 0),
        "credential_redaction_policy_preserved": payload.get(
            "credential_redaction_policy_preserved", False
        ),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def validate_stage5ds_scope_control() -> Stage5DSValidationResult:
    payload = _load(DATA_PATHS["scope_control"])
    errors = _required_false_errors(payload)
    if payload.get("metadata_only") is not True or payload.get("source_lock_only") is not True:
        errors.append("scope control must be metadata/source-lock only")
    counts = {
        "scope_control_valid": not errors,
        "pivot_target_selected_now": payload.get("pivot_target_selected_now", False),
        "execution_performed": payload.get("execution_performed", False),
    }
    return Stage5DSValidationResult(len(errors), counts, errors)


def stage5ds_summary_text() -> str:
    payload = _load(DATA_PATHS["summary"])
    lines = [
        "LiberPrimus Stage 5DS summary:",
        f"status={payload.get('status')}",
        f"music_community_theory_file_count={payload.get('music_community_theory_file_count')}",
        f"music_candidate_records_created={payload.get('music_candidate_records_created')}",
        f"ouroboros_candidate_records_created={payload.get('ouroboros_candidate_records_created')}",
        "token_block_static_candidate_records_created="
        f"{payload.get('token_block_static_candidate_records_created')}",
        f"source_browser_entries_loaded={payload.get('source_browser_entries_loaded')}",
        f"pivot_target_selected_now={_format(payload.get('pivot_target_selected_now'))}",
        "byte_stream_generation_authorized_now="
        f"{_format(payload.get('byte_stream_generation_authorized_now'))}",
        f"execution_performed={_format(payload.get('execution_performed'))}",
        f"stage5bd_run_plan_id_count={payload.get('stage5bd_run_plan_id_count')}",
        f"active_lineage_record_count={payload.get('active_lineage_record_count')}",
        f"recommended_next_stage_id={payload.get('recommended_next_stage_id')}",
    ]
    return "\n".join(lines)


def _write_schemas() -> None:
    for key, path in SCHEMA_PATHS.items():
        write_json(path, _schema_for(key))


def _schema_for(key: str) -> dict[str, Any]:
    required = ["record_type", "stage_id", "metadata_only", "source_lock_only", "solve_claim"]
    properties: dict[str, Any] = {
        "record_type": {"type": "string"},
        "stage_id": {"const": STAGE_ID},
        "metadata_only": {"const": True},
        "source_lock_only": {"const": True},
        "puzzle_execution_allowed": {"const": False},
        "solve_claim": {"const": False},
        "canonical_codex_handoff_root": {"const": "codex-output"},
    }
    for flag in FORBIDDEN_FALSE_FLAGS:
        properties[flag] = {"const": False}
    if key in {"music_candidate_record", "ouroboros_transform_context_record"}:
        required.extend(["candidate_family_id", "candidate_status"])
        properties["candidate_family_id"] = {"type": "string"}
        properties["candidate_status"] = {"type": "string"}
    if key == "token_block_static_context_record":
        required.extend(["candidate_family_id", "candidate_status"])
        properties["candidate_status"] = {"const": "source_locked_static_context_only"}
    if key == "music_file_inventory":
        required.extend(["files", "file_count"])
        properties["files"] = {"type": "array"}
        properties["file_count"] = {"type": "integer"}
    if key == "music_message_attachment_anchor_index":
        required.append("anchors")
        properties["anchors"] = {"type": "array"}
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": key.replace("_", " "),
        "type": "object",
        "required": required,
        "properties": properties,
        "additionalProperties": True,
    }


def _base_payload(record_type: str, schema: Path | None = None) -> dict[str, Any]:
    payload = {
        "record_type": record_type,
        "stage_id": STAGE_ID,
        "stage_title": STAGE_TITLE,
        "prompt_type": PROMPT_TYPE,
        "metadata_only": True,
        "source_lock_only": True,
        "puzzle_execution_allowed": False,
        "solve_claim": False,
        "canonical_codex_handoff_root": "codex-output",
        "previous_stage_id": SOURCE_PREVIOUS_STAGE_ID,
        "previous_stage_final_commit_prompt_value": SOURCE_PREVIOUS_STAGE_COMMIT,
        "actual_starting_commit_observed": _git_value("rev-parse", "HEAD"),
    }
    if schema is not None:
        payload["schema"] = schema.as_posix()
    payload.update({flag: False for flag in FORBIDDEN_FALSE_FLAGS})
    return payload


def _candidate_base(
    *,
    record_type: str,
    candidate_family_id: str,
    schema: Path,
    source_type: str,
    status: str,
) -> dict[str, Any]:
    return {
        **_base_payload(record_type, schema),
        "candidate_family_id": candidate_family_id,
        "source_type": source_type,
        "candidate_status": status,
        "review_state": "source_locked_review_only",
        "evidence_status": "candidate_context_only",
        "trusted_as_canonical": False,
        "usable_as_experiment_seed_now": False,
        "execution_authorized_now": False,
        "selected_now": False,
    }


def _file_inventory(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    rows: list[dict[str, Any]] = []
    for path in sorted(file_path for file_path in root.rglob("*") if file_path.is_file()):
        stat = path.stat()
        rel = path.as_posix()
        ext = path.suffix.lower()
        kind = _file_kind(ext)
        rows.append(
            {
                "file_name": path.name,
                "relative_path": rel,
                "extension": ext,
                "file_kind": kind,
                "mime_guess": mimetypes.guess_type(path.name)[0],
                "probe_kind": _safe_probe_kind(path),
                "size_bytes": stat.st_size,
                "modified_utc": datetime.fromtimestamp(stat.st_mtime, UTC)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
                "sha256": sha256_file(path),
                "raw_file_committed": False,
                "metadata_only": True,
            }
        )
    return rows


def _file_kind(ext: str) -> str:
    if ext == ".mp3":
        return "audio"
    if ext == ".pdf":
        return "pdf"
    if ext in {".png", ".jpg", ".jpeg"}:
        return "image"
    if ext == ".txt":
        return "text"
    return "other"


def _safe_probe_kind(path: Path) -> str:
    try:
        return _probe_kind(path)
    except Exception:
        return "metadata_probe_failed"


def _music_source_lock_register(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    paths = [row["relative_path"] for row in inventory]
    missing_expected = sorted(EXPECTED_MUSIC_FILES - {Path(path).name for path in paths})
    return {
        **_base_payload(
            "stage5ds_music_community_theory_source_lock_register",
            SCHEMA_PATHS["music_source_lock_register"],
        ),
        "source_lock_created": True,
        "source_root": COMMUNITY_ROOT.as_posix(),
        "source_root_exists": COMMUNITY_ROOT.exists(),
        "source_context": "local ignored CicadaMusic community-theory archive",
        "source_status": "local_ignored_metadata_locked",
        "raw_source_files_committed": False,
        "file_count": len(inventory),
        "audio_file_count": sum(1 for row in inventory if row["file_kind"] == "audio"),
        "pdf_file_count": sum(1 for row in inventory if row["file_kind"] == "pdf"),
        "image_file_count": sum(1 for row in inventory if row["file_kind"] == "image"),
        "text_file_count": sum(1 for row in inventory if row["file_kind"] == "text"),
        "source_paths": paths,
        "missing_expected_files": missing_expected,
        "notes": "Raw community-theory files remain ignored under third_party/.",
    }


def _music_file_inventory_record(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        **_base_payload(
            "stage5ds_music_community_theory_file_inventory",
            SCHEMA_PATHS["music_file_inventory"],
        ),
        "source_root": COMMUNITY_ROOT.as_posix(),
        "file_count": len(inventory),
        "audio_file_count": sum(1 for row in inventory if row["file_kind"] == "audio"),
        "pdf_file_count": sum(1 for row in inventory if row["file_kind"] == "pdf"),
        "image_file_count": sum(1 for row in inventory if row["file_kind"] == "image"),
        "text_file_count": sum(1 for row in inventory if row["file_kind"] == "text"),
        "raw_file_bodies_committed": False,
        "files": inventory,
    }


def _messages_record(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    path = COMMUNITY_ROOT / "messages.txt"
    lines: list[str] = []
    if path.exists():
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    row = next((item for item in inventory if item["relative_path"] == path.as_posix()), None)
    return {
        **_base_payload("stage5ds_music_messages_source_lock"),
        "source_path": path.as_posix(),
        "messages_txt_present": path.exists(),
        "source_sha256": row.get("sha256") if row else None,
        "size_bytes": row.get("size_bytes") if row else 0,
        "line_count": len(lines),
        "raw_message_body_committed": False,
        "line_anchor_policy": "line numbers and compact excerpts only; no raw Discord log body",
        "source_status": "local_ignored_metadata_locked" if path.exists() else "missing_local_source",
    }


def _attachment_anchors(
    inventory: list[dict[str, Any]], messages: dict[str, Any]
) -> list[dict[str, Any]]:
    path = Path(messages["source_path"])
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines() if path.exists() else []
    anchors: list[dict[str, Any]] = []
    for row in inventory:
        if row["file_kind"] == "text":
            continue
        words = _anchor_words(Path(row["file_name"]).stem)
        match = _find_anchor(lines, words)
        anchors.append(
            {
                "file_name": row["file_name"],
                "relative_path": row["relative_path"],
                "file_sha256": row["sha256"],
                "anchor_terms": words,
                "message_line_anchor_present": match is not None,
                "message_line_number_one_based": match[0] if match else None,
                "message_excerpt": match[1] if match else None,
                "raw_message_body_committed": False,
            }
        )
    return anchors


def _anchor_words(stem: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9]+", stem.lower())
    return [word for word in words if len(word) >= 3][:6]


def _find_anchor(lines: list[str], words: list[str]) -> tuple[int, str] | None:
    if not words:
        return None
    for index, line in enumerate(lines, start=1):
        lower = line.lower()
        if all(word in lower for word in words[: min(3, len(words))]):
            return index, line.strip()[:160]
    for index, line in enumerate(lines, start=1):
        lower = line.lower()
        if any(word in lower for word in words):
            return index, line.strip()[:160]
    return None


def _anchor_index_record(anchors: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        **_base_payload(
            "stage5ds_music_message_attachment_anchor_index",
            SCHEMA_PATHS["music_message_attachment_anchor_index"],
        ),
        "source_path": (COMMUNITY_ROOT / "messages.txt").as_posix(),
        "anchor_count": len(anchors),
        "anchors_with_line_matches": sum(1 for row in anchors if row["message_line_anchor_present"]),
        "anchors": anchors,
        "raw_message_body_committed": False,
    }


def _audio_metadata_records(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in [item for item in inventory if item["file_kind"] == "audio"]:
        path = Path(row["relative_path"])
        metadata = _safe_parse_audio(path)
        rows.append(
            {
                **row,
                **metadata,
                "audio_decode_performed": False,
                "audio_duration_metadata_verified_now": False,
                "stego_tool_execution_performed": False,
                "mp3stego_execution_performed": False,
                "spectrogram_stego_performed": False,
            }
        )
    return rows


def _safe_parse_audio(path: Path) -> dict[str, Any]:
    try:
        return _parse_id3(path)
    except Exception as exc:
        return {
            "id3_tags_present": False,
            "metadata_extraction_status": "id3_metadata_parse_failed",
            "metadata_error": str(exc)[:200],
        }


def _pdf_metadata_records(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in [item for item in inventory if item["file_kind"] == "pdf"]:
        path = Path(row["relative_path"])
        metadata = _safe_parse_pdf(path)
        rows.append(
            {
                **row,
                **metadata,
                "pdf_rendering_performed_now": False,
                "pdf_ocr_or_hidden_content_rendering_performed": False,
                "ocr_performed": False,
            }
        )
    return rows


def _safe_parse_pdf(path: Path) -> dict[str, Any]:
    try:
        return _parse_pdf(path)
    except Exception as exc:
        return {
            "metadata_extraction_status": "pdf_metadata_parse_failed",
            "metadata_error": str(exc)[:200],
        }


def _image_source_records(inventory: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in [item for item in inventory if item["file_kind"] == "image"]:
        image_metadata = _image_dimensions(Path(row["relative_path"]))
        rows.append(
            {
                **row,
                **image_metadata,
                "image_forensics_performed": False,
                "ocr_performed": False,
                "semantic_image_interpretation_performed": False,
            }
        )
    return rows


def _image_dimensions(path: Path) -> dict[str, Any]:
    try:
        from PIL import Image

        with Image.open(path) as image:
            return {
                "image_format": image.format,
                "width": image.width,
                "height": image.height,
                "colour_mode": image.mode,
                "metadata_extraction_status": "pillow_metadata_only",
            }
    except Exception as exc:
        return {
            "image_format": None,
            "width": None,
            "height": None,
            "colour_mode": None,
            "metadata_extraction_status": "image_metadata_parse_failed",
            "metadata_error": str(exc)[:200],
        }


def _metadata_collection_record(
    record_type: str, title: str, rows: list[dict[str, Any]]
) -> dict[str, Any]:
    return {
        **_base_payload(record_type),
        "title": title,
        "record_count": len(rows),
        "metadata_only_records": True,
        "raw_files_committed_now": False,
        "records": rows,
    }


def _original_music_crosslink() -> dict[str, Any]:
    original_paths = sorted(path.as_posix() for path in ORIGINAL_MUSIC_ROOT.iterdir() if path.is_file())
    return {
        **_base_payload("stage5ds_original_cicada_music_stage5dj_crosslink"),
        "source_type": "stage5dj_crosslink",
        "stage5dj_source_locked_original_music": True,
        "stage5dj_records_reused_not_duplicated": True,
        "original_music_root": ORIGINAL_MUSIC_ROOT.as_posix(),
        "original_music_root_paths": original_paths,
        "referenced_stage5dj_records": [
            "data/source-harvester/stage5dj-cicada-music-source-lock-register.yaml",
            "data/historical-route/stage5dj-instar-parable-id3-arithmetic-v1.yaml",
        ],
    }


def _ouroboros_web_source_register() -> dict[str, Any]:
    sources = [
        {
            "source_id": "ouroboros-symbol-general-reference",
            "url": "https://en.wikipedia.org/wiki/Ouroboros",
            "source_lock_status": "not_checked_in_stage5ds",
        },
        {
            "source_id": "strange-loop-general-reference",
            "url": "https://en.wikipedia.org/wiki/Strange_loop",
            "source_lock_status": "not_checked_in_stage5ds",
        },
        {
            "source_id": "quine-general-reference",
            "url": "https://en.wikipedia.org/wiki/Quine_(computing)",
            "source_lock_status": "not_checked_in_stage5ds",
        },
    ]
    return {
        **_base_payload("stage5ds_ouroboros_web_source_lock_register"),
        "source_type": "web_reference_candidates",
        "network_fetch_performed_now": False,
        "source_lock_status": "future_review_required",
        "sources": sources,
    }


def _raw_source_noncommit_proof(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    tracked = _git_lines("ls-files", "third_party/CicadaMusic", "third_party/SourceSnapshots")
    return {
        **_base_payload("stage5ds_raw_source_noncommit_proof"),
        "raw_source_root": COMMUNITY_ROOT.as_posix(),
        "inventory_file_count": len(inventory),
        "tracked_third_party_cicada_music_files": tracked,
        "raw_third_party_files_committed": False,
        "raw_files_committed_now": False,
        "raw_source_files_committed": False,
    }


def _codex_handoff_policy() -> dict[str, Any]:
    return {
        **_base_payload("stage5ds_codex_handoff_policy"),
        "canonical_codex_handoff_root": "codex-output",
        "deprecated_codex_output_path": "codex_output",
        "codex_output_used": DEPRECATED_CODEX_OUTPUT.exists(),
        "codex_output_absent": not DEPRECATED_CODEX_OUTPUT.exists(),
        "codex_completion_summary_path": CODEX_COMPLETION_PATH.as_posix(),
        "codex_completion_summary_committed": False,
    }


def _credential_redaction_policy() -> dict[str, Any]:
    lines = _git_lines("remote", "-v")
    credential_like = [
        line
        for line in lines
        if any(re.search(pattern, line, re.IGNORECASE) for pattern in SECRET_PATTERNS)
    ]
    return {
        **_base_payload("stage5ds_credential_redaction_policy_preservation"),
        "credential_redaction_policy_preserved": True,
        "git_remote_entry_count": len(lines),
        "credential_like_remote_count": len(credential_like),
        "remote_url_values_printed": False,
        "secret_values_printed_or_committed": False,
        "remote_names_checked": sorted({line.split()[0] for line in lines if line.strip()}),
    }


def _music_candidate_records() -> dict[str, dict[str, Any]]:
    product_factors = [1031, 1229, 1259]
    prime_rows = [_prime_fact(value) for value in product_factors]
    guitar_rows = [
        {
            "value": value,
            "is_prime": _is_prime(value),
            "factorization": _factorize(value),
        }
        for value in GUITAR_FRET_STRINGS
    ]
    records: dict[str, dict[str, Any]] = {
        "instar_parable_id3_gp_product_candidate": {
            **_music_candidate(
                "stage5ds-instar-parable-id3-gp-product",
                "Instar ID3 parable prime-product candidate",
            ),
            "source_paths": [
                "third_party/CicadaMusic/community-theory/Instar Emergence (6-19-2025).mp3",
                "third_party/CicadaMusic/Instar Emergence (6-19-2025).mp3",
            ],
            "prime_factors": prime_rows,
            "prime_product": math.prod(product_factors),
            "expected_prime_product": 1595277641,
            "product_matches_id3_parable_number": math.prod(product_factors) == 1595277641,
            "poem_line_gp_sums": [
                _gp_record("WE MUST SHED OUR OWN CIRCUMFERENCES"),
                _gp_record("FIND THE DIVINITY WITHIN AND EMERGE"),
                _gp_record("LIKE THE INSTAR TUNNELING TO THE SURFACE"),
            ],
            "review_blockers": [
                "needs independent source review of ID3 parable text",
                "needs declared GP transliteration contract before any use",
            ],
        },
        "instar_title_761_duration_167_bridge": {
            **_music_candidate(
                "stage5ds-instar-title-761-duration-167-bridge",
                "Instar title 761 and reverse 167 bridge candidate",
            ),
            "title_gp": _gp_record("THE INSTAR EMERGENCE"),
            "reverse_761": 167,
            "duration_family_seconds_claimed": 167,
            "duration_metadata_verified_now": False,
            "source_paths": [
                "third_party/CicadaMusic/community-theory/Instar Emergence (6-19-2025).mp3"
            ],
        },
        "interconnectedness_772_277_table_canon_number": {
            **_music_candidate(
                "stage5ds-interconnectedness-772-277-table-canon-number",
                "Interconnectedness 772/277 table-canon number candidate",
            ),
            "interconnectedness_gp": _gp_record("INTERCONNECTEDNESS"),
            "reverse_772": 277,
            "divinity_gp": _gp_record("DIVINITY"),
            "reverse_376": 673,
            "interconnectedness_reverse_sum": 1049,
            "divinity_reverse_sum": 1049,
            "source_paths": [
                "third_party/CicadaMusic/community-theory/Interconnectedness (10-11-2025).pdf"
            ],
        },
        "interconnectedness_table_canon_29_note_gp_mapping": {
            **_music_candidate(
                "stage5ds-interconnectedness-table-canon-29-note-gp-mapping",
                "Interconnectedness table canon 29-note GP mapping candidate",
            ),
            "note_count_claimed": 29,
            "unique_notes_claimed": "19/29",
            "axis_note_claimed": "G#4",
            "route_extraction_performed_now": False,
            "review_blockers": ["needs score/table review", "needs null controls"],
        },
        "instar_205_beats_prime205_1259_poem_line": {
            **_music_candidate(
                "stage5ds-instar-205-beats-prime205-1259-poem-line",
                "Instar 205 beats prime(205)=1259 poem-line candidate",
            ),
            "beat_count_claimed": 205,
            "prime_index": 205,
            "prime_at_index": 1259,
            "poem_line_gp_sum": _gp_record("LIKE THE INSTAR TUNNELING TO THE SURFACE"),
        },
        "instar_csharp_gsharp_hexachord_axis": {
            **_music_candidate(
                "stage5ds-instar-csharp-gsharp-hexachord-axis",
                "Instar C#/G# hexachord-axis candidate",
            ),
            "axis_notes_claimed": ["C#", "G#"],
            "transform_status": "future_review_only",
            "music_route_extraction_performed_now": False,
        },
        "instar_reverse_section_augmentation_canon": {
            **_music_candidate(
                "stage5ds-instar-reverse-section-augmentation-canon",
                "Instar reverse-section augmentation-canon candidate",
            ),
            "claimed_transform_context": [
                "reverse section",
                "augmentation canon",
                "musical mirror/self-reference context",
            ],
            "midi_route_extraction_performed_now": False,
        },
        "interconnectedness_guitar_tab_prime_fret_strings": {
            **_music_candidate(
                "stage5ds-interconnectedness-guitar-tab-prime-fret-strings",
                "Interconnectedness guitar-tab prime fret-string candidate",
            ),
            "source_paths": [
                "third_party/CicadaMusic/community-theory/Interconnectedness, Guitar Tab (10-14-2025).pdf"
            ],
            "fret_string_records": guitar_rows,
            "prime_string_count": sum(1 for row in guitar_rows if row["is_prime"]),
            "nonprime_exception": {
                "value": 32023,
                "factorization": [31, 1033],
            },
        },
        "interconnectedness_547_beats_137_measures": {
            **_music_candidate(
                "stage5ds-interconnectedness-547-beats-137-measures",
                "Interconnectedness 547 beats / 137 measures candidate",
            ),
            "beat_count_claimed": 547,
            "measure_count_claimed": 137,
            "number_status": "prime-family-context",
        },
        "music_transform_grammar_for_cipher_methods": {
            **_music_candidate(
                "stage5ds-music-transform-grammar-for-cipher-methods",
                "Music transform grammar for future cipher-method review",
            ),
            "allowed_future_terms": [
                "retrograde",
                "inversion",
                "augmentation",
                "canon",
                "axis note",
                "prime fret string",
            ],
            "execution_ready": False,
        },
        "music_direct_pitch_substitution_quarantine": {
            **_music_candidate(
                "stage5ds-music-direct-pitch-substitution-quarantine",
                "Direct pitch substitution quarantine",
                status="quarantined_direct_substitution",
            ),
            "quarantine_reason": "Direct substitution has high false-positive risk without a source-locked grammar.",
            "direct_music_substitution_executed": False,
            "usable_as_experiment_seed_now": False,
        },
    }
    return records


def _music_candidate(
    candidate_family_id: str, title: str, status: str = "source_locked_candidate_only"
) -> dict[str, Any]:
    return {
        **_candidate_base(
            record_type="stage5ds_music_candidate_record",
            candidate_family_id=candidate_family_id,
            schema=SCHEMA_PATHS["music_candidate_record"],
            source_type="expanded_music_community_theory",
            status=status,
        ),
        "title": title,
        "audio_stego_performed": False,
        "mp3stego_execution_performed": False,
        "spectrogram_stego_performed": False,
        "direct_music_substitution_executed": False,
    }


def _ouroboros_candidate_records() -> dict[str, dict[str, Any]]:
    scan_values = [_gp_record(phrase) for phrase in GP_PHRASE_VALUES if phrase in _ouroboros_scan_phrases()]
    records: dict[str, dict[str, Any]] = {
        "ouroboros_gp_167_music_cycle": {
            **_ouroboros_candidate(
                "stage5ds-ouroboros-gp-167-music-cycle",
                "Ouroboros GP 167 music-cycle candidate",
            ),
            "gp_sum": 167,
            "music_cycle_crosslink": "stage5ds-instar-title-761-duration-167-bridge",
            "source_paths": ["data/historical-route/stage5ds-instar-title-761-duration-167-bridge-v1.yaml"],
        },
        "pdd153_ouroboros_167_mod153_offset14": {
            **_ouroboros_candidate(
                "stage5ds-pdd153-ouroboros-167-mod153-offset14",
                "PDD153 Ouroboros 167 mod 153 offset-14 candidate",
            ),
            "gp_sum": 167,
            "pdd_modulus": 153,
            "offset": 14,
            "arithmetic": "167 - 153 = 14",
        },
        "pdd153_56311_ouroboric_cycle": {
            **_ouroboros_candidate(
                "stage5ds-pdd153-56311-ouroboric-cycle",
                "PDD153 56311 ouroboric cycle candidate",
            ),
            "sequence": [5, 6, 3, 11],
            "sequence_sum": 25,
            "gcd_sequence_sum_modulus": math.gcd(25, 153),
            "phase_count": 4,
            "closed_state_period": 612,
        },
        "ouroboros_see_also_transform_context": {
            **_ouroboros_candidate(
                "stage5ds-ouroboros-see-also-transform-context",
                "Ouroboros see-also transform context",
            ),
            "see_also_concepts": [
                "mobius_strip",
                "self_reference",
                "strange_loop",
                "infinite_loop",
                "quine",
                "self_fulfilling_prophecy",
                "endless_knot",
                "enso",
                "three_hares",
                "valknut",
                "amphisbaena",
                "escher_dragon",
            ],
        },
        "ouroboros_see_also_gp_arithmetic_scan": {
            **_ouroboros_candidate(
                "stage5ds-ouroboros-see-also-gp-arithmetic-scan",
                "Ouroboros see-also GP arithmetic scan",
            ),
            "gp_arithmetic_source": "stage5ds_operator_assistant_review_phrase_table",
            "gp_scan_records": scan_values,
        },
        "strange_loop_gp463_page32_bridge": {
            **_ouroboros_candidate(
                "stage5ds-strange-loop-gp463-page32-bridge",
                "Strange loop GP463 page32 bridge candidate",
            ),
            "gp_record": _gp_record("STRANGE LOOP"),
            "page_context": "page32",
        },
        "self_reference_gp529_square23": {
            **_ouroboros_candidate(
                "stage5ds-self-reference-gp529-square23",
                "Self-reference GP529 square-23 candidate",
            ),
            "gp_record": _gp_record("SELF REFERENCE"),
            "square_root": 23,
            "square_factorization": [23, 23],
        },
        "self_fulfilling_prophecy_gp841_square29": {
            **_ouroboros_candidate(
                "stage5ds-self-fulfilling-prophecy-gp841-square29",
                "Self-fulfilling prophecy GP841 square-29 candidate",
            ),
            "gp_record": _gp_record("SELF FULFILLING PROPHECY"),
            "square_root": 29,
            "square_factorization": [29, 29],
        },
        "infinite_loop_gp409_page33_dot_bridge": {
            **_ouroboros_candidate(
                "stage5ds-infinite-loop-gp409-page33-dot-bridge",
                "Infinite loop GP409 page33/dot bridge candidate",
            ),
            "gp_record": _gp_record("INFINITE LOOP"),
            "dot_or_page33_context": "review_only",
        },
        "quine_fixed_point_self_reproduction": {
            **_ouroboros_candidate(
                "stage5ds-quine-fixed-point-self-reproduction",
                "Quine fixed-point self-reproduction candidate",
            ),
            "transform_context": "fixed_point_self_reference",
        },
        "mobius_ouroboros_one_boundary_transform": {
            **_ouroboros_candidate(
                "stage5ds-mobius-ouroboros-one-boundary-transform",
                "Mobius/Ouroboros one-boundary transform candidate",
            ),
            "gp_record": _gp_record("MOBIUS STRIP"),
            "boundary_claim_status": "symbolic_context_only",
        },
        "escher_dragon_tail_bite_self_reference": {
            **_ouroboros_candidate(
                "stage5ds-escher-dragon-tail-bite-self-reference",
                "Escher dragon tail-bite self-reference candidate",
            ),
            "symbolic_context": "self_reference_dragon_tail_bite",
        },
        "endless_knot_interdependence_no_beginning": {
            **_ouroboros_candidate(
                "stage5ds-endless-knot-interdependence-no-beginning",
                "Endless knot interdependence/no-beginning candidate",
            ),
            "symbolic_context": "interdependent_no_beginning_or_end",
        },
        "enso_circle_open_closed_boundary": {
            **_ouroboros_candidate(
                "stage5ds-enso-circle-open-closed-boundary",
                "Enso open/closed boundary candidate",
            ),
            "gp_record": _gp_record("ENSO"),
        },
        "three_hares_rotational_shared_parts": {
            **_ouroboros_candidate(
                "stage5ds-three-hares-rotational-shared-parts",
                "Three hares rotational shared-parts candidate",
            ),
            "gp_record": _gp_record("THREE HARES"),
        },
        "valknut_triple_knot_runic_context": {
            **_ouroboros_candidate(
                "stage5ds-valknut-triple-knot-runic-context",
                "Valknut triple-knot runic context candidate",
            ),
            "symbolic_context": "triple_knot_runic_context_review_only",
        },
        "amphisbaena_bidirectional_serpent_route": {
            **_ouroboros_candidate(
                "stage5ds-amphisbaena-bidirectional-serpent-route",
                "Amphisbaena bidirectional serpent-route candidate",
            ),
            "symbolic_context": "bidirectional_route_review_only",
        },
    }
    return records


def _ouroboros_candidate(candidate_family_id: str, title: str) -> dict[str, Any]:
    return {
        **_candidate_base(
            record_type="stage5ds_ouroboros_transform_context_record",
            candidate_family_id=candidate_family_id,
            schema=SCHEMA_PATHS["ouroboros_transform_context_record"],
            source_type="ouroboros_self_reference_transform_context",
            status="source_locked_context_only",
        ),
        "title": title,
        "route_extraction_performed_now": False,
        "probability_claim_accepted_as_validated": False,
    }


def _ouroboros_scan_phrases() -> set[str]:
    return {
        "OUROBOROS",
        "STRANGE LOOP",
        "SELF REFERENCE",
        "SELF FULFILLING PROPHECY",
        "INFINITE LOOP",
        "THREE HARES",
        "MOBIUS STRIP",
        "ENSO",
        "AUTOCANNIBALISM",
    }


def _token_static_summary() -> dict[str, Any]:
    mapping = read_yaml(Path("data/token-block/stage5ap-token-block-mapping-preflight.yaml"))
    values = [int(row["mapped_value"]) for row in mapping.get("value_records", [])]
    byte_stream = bytes(values)
    return {
        "token_count": len(values),
        "row_count": 32,
        "column_count": 8,
        "unique_token_count": len({row["token"] for row in mapping.get("value_records", [])}),
        "primary60_mapping_formula": mapping.get("mapping_formula"),
        "alphabet": PRIMARY_ALPHABET,
        "alphabet_length": len(PRIMARY_ALPHABET),
        "known_mapping_checks": mapping.get("known_mapping_checks", []),
        "all_values_in_byte_range": all(0 <= value <= 255 for value in values),
        "first_16_bytes_hex": byte_stream[:16].hex(),
        "primary60_byte_stream_sha256": hashlib.sha256(byte_stream).hexdigest(),
        "full_byte_stream_committed": False,
    }


def _token_static_records(token_static: dict[str, Any]) -> dict[str, dict[str, Any]]:
    static_base = {
        "token_block_static_source_paths": [
            "data/token-block/stage5ap-token-block-canonical-transcription.yaml",
            "data/token-block/stage5ap-token-block-mapping-preflight.yaml",
            "data/token-block/stage5aw-repaired-token-variant-branch-manifest.yaml",
            "data/token-block/stage5bo-errata-aware-token-option-universe.yaml",
            "data/token-block/stage5az-repaired-bounded-variant-family-manifest.yaml",
        ],
        **token_static,
        "variant_byte_streams_generated": False,
        "real_byte_stream_generated": False,
        "machine_code_execution_performed_now": False,
        "vm_bytecode_execution_performed_now": False,
    }
    return {
        "machine_code_static_sanity": {
            **_token_static_candidate(
                "stage5ds-token-block-machine-code-static-sanity",
                "Token-block static machine-code sanity candidate",
            ),
            **static_base,
            "native_code_likelihood": "low",
            "native_code_likelihood_reason": "First byte 0xcb resembles far return/lret and raises privileged I/O risk.",
            "vm_or_table_likelihood": "medium",
        },
        "base_neighbor_static_scan": {
            **_token_static_candidate(
                "stage5ds-token-block-base-neighbor-static-scan",
                "Token-block base-neighbor static scan",
            ),
            **static_base,
            "base58_status": "invalid_due_suffix_x_index_59",
            "base59_status": "invalid_due_suffix_x_index_59",
            "base60_status": "clean",
            "base61_to_base64_status": "overflow_or_modulo_required",
        },
        "vm_or_table_surface": {
            **_token_static_candidate(
                "stage5ds-token-block-vm-or-table-surface",
                "Token-block VM/table surface candidate",
            ),
            **static_base,
            "candidate_surface": "vm_or_lookup_table_review_only",
        },
        "quine_context_crosslink": {
            **_token_static_candidate(
                "stage5ds-token-block-quine-context-crosslink",
                "Token-block Quine/self-reference context crosslink",
            ),
            **static_base,
            "crosslinked_context_records": [
                "stage5ds-quine-fixed-point-self-reproduction",
                "stage5ds-ouroboros-see-also-transform-context",
            ],
        },
    }


def _token_static_candidate(candidate_family_id: str, title: str) -> dict[str, Any]:
    return {
        **_candidate_base(
            record_type="stage5ds_token_block_static_context_record",
            candidate_family_id=candidate_family_id,
            schema=SCHEMA_PATHS["token_block_static_context_record"],
            source_type="token_block_static_context",
            status="source_locked_static_context_only",
        ),
        "title": title,
        "branch_enumeration_performed": False,
        "byte_stream_generation_authorized_now": False,
        "token_block_experiment_executed": False,
    }


def _preservation_records(token_static: dict[str, Any]) -> dict[str, dict[str, Any]]:
    stage5dr_summary = read_yaml(STAGE5DR_DATA_PATHS["summary"])
    return {
        "stage5dg_preservation": {
            **_base_payload("stage5ds_stage5dg_preservation"),
            "stage5dg_operator_approval_record_preserved": True,
            "operator_approval_component_satisfied_now": True,
            "deep_research_acceptance_component_satisfied_now": False,
            "combined_approval_gate_satisfied_now": False,
            "activation_authorized_now": False,
        },
        "stage5bd_preservation": {
            **_base_payload("stage5ds_stage5bd_preservation"),
            "stage5bd_run_plan_id_count": 10,
            "stage5bd_run_plan_ids_preserved": True,
            "stage5bd_run_plan_registry_path": "data/token-block/stage5bd-run-plan-id-registry.yaml",
            "active_manifest_registry_updated": False,
        },
        "active_lineage_preservation": {
            **_base_payload("stage5ds_active_lineage_preservation"),
            "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
            "active_lineage_paths_preserved": [
                path.as_posix() if isinstance(path, Path) else str(path)
                for path in ACTIVE_LINEAGE_PATHS
            ],
            "active_planning_input_authorized_now": False,
            "active_planning_input_selected_now": False,
        },
        "no_active_ingestion_proof": {
            **_base_payload("stage5ds_no_active_ingestion_proof"),
            "gate_status": "closed",
            "active_ingestion_performed": False,
            "active_planning_input_authorized_now": False,
        },
        "no_byte_stream_transition_proof": {
            **_base_payload("stage5ds_no_byte_stream_transition_proof"),
            "gate_status": "closed",
            "byte_stream_generation_authorized_now": False,
            "real_byte_stream_generated": False,
            "variant_byte_streams_generated": False,
        },
        "no_token_block_execution_proof": {
            **_base_payload("stage5ds_no_token_block_execution_proof"),
            "gate_status": "closed",
            "execution_authorized_now": False,
            "execution_performed": False,
            "token_block_experiment_executed": False,
        },
        "token_block_static_machine_code_scope_control": {
            **_base_payload(
                "stage5ds_token_block_static_machine_code_scope_control",
                SCHEMA_PATHS["token_block_static_machine_code_scope_control"],
            ),
            **token_static,
            "candidate_status": "static_metadata_only",
            "machine_code_execution_performed_now": False,
            "native_code_execution_performed_now": False,
            "vm_bytecode_execution_performed_now": False,
            "full_byte_stream_committed": False,
        },
        "operator_console_stage5dr_preservation": {
            **_base_payload("stage5ds_operator_console_stage5dr_preservation"),
            "stage5dr_details_panel_preserved": True,
            "stage5dr_source_browser_entries_loaded": stage5dr_summary.get(
                "source_browser_entries_loaded"
            ),
            "stage5dr_source_browser_records_scanned": stage5dr_summary.get(
                "source_browser_records_scanned"
            ),
            "source_browser_performs_analysis": False,
            "source_browser_runs_ocr": False,
            "source_browser_runs_image_forensics": False,
            "source_browser_runs_ai_image_interpretation": False,
            "source_browser_executes_source_files": False,
            "source_browser_modifies_raw_third_party_files": False,
        },
    }


def _source_browser_loadability_summary() -> dict[str, Any]:
    source_result = validate_source_index()
    manual_result = validate_manual_records()
    index = build_source_index()
    summary = source_browser_summary(index)
    stage5ds_entries = [entry for entry in index.entries if entry.stage_id == STAGE_ID]
    return {
        **_base_payload("stage5ds_source_browser_loadability_summary"),
        "source_browser_loadability_validated": source_result.ok and manual_result.ok,
        "source_browser_index_valid": source_result.ok,
        "manual_entries_valid": manual_result.ok,
        "source_browser_entries_loaded": summary["entries_loaded"],
        "source_browser_records_scanned": summary["records_scanned"],
        "stage5ds_entries_loaded": len(stage5ds_entries),
        "stage5ds_categories": sorted({entry.category for entry in stage5ds_entries}),
        "source_browser_missing_paths": summary["missing_paths"],
        "source_browser_warning_count": summary["warnings"],
        "source_browser_validation_error_count": len(source_result.errors) + len(manual_result.errors),
        "source_browser_validation_errors": source_result.errors + manual_result.errors,
    }


def _stage5dr_preservation_record() -> dict[str, Any]:
    stage5dr_summary = read_yaml(STAGE5DR_DATA_PATHS["summary"])
    return {
        **_base_payload("stage5ds_stage5dr_preservation"),
        "stage5dr_complete": stage5dr_summary.get("status") == "complete",
        "stage5dr_source_browser_entries_loaded": stage5dr_summary.get(
            "source_browser_entries_loaded"
        ),
        "stage5dr_source_browser_records_scanned": stage5dr_summary.get(
            "source_browser_records_scanned"
        ),
        "stage5dq_baseline_entries_preserved": stage5dr_summary.get(
            "stage5dq_source_browser_entries_loaded_count"
        ),
        "stage5dq_baseline_records_preserved": stage5dr_summary.get(
            "stage5dq_source_records_scanned_count"
        ),
        "stage5dr_bottom_details_panel_spans_categories_and_table": stage5dr_summary.get(
            "bottom_details_panel_spans_categories_and_table"
        ),
        "stage5dr_details_panel_hideable": stage5dr_summary.get("details_panel_hideable"),
        "stage5dr_details_panel_structured_sections": stage5dr_summary.get(
            "details_panel_structured_sections"
        ),
        "stage5dr_image_thumbnails_in_details_panel": stage5dr_summary.get(
            "image_thumbnails_in_details_panel"
        ),
        "stage5dr_table_context_menu_added": stage5dr_summary.get("table_context_menu_added"),
        "stage5dr_status_unspecified_display_added": stage5dr_summary.get(
            "status_unspecified_display_added"
        ),
        "stage5dr_puzzle_execution_allowed": False,
        "stage5dr_source_lock_record_semantics_rewritten": False,
        "stage5dr_raw_source_files_mutated_by_gui": False,
        "stage5dr_gui_followup_right_side_details_panel_note": True,
    }


def _reviewable_validation_evidence(source_browser_record: dict[str, Any]) -> dict[str, Any]:
    return {
        **_base_payload(
            "stage5ds_reviewable_validation_evidence",
            SCHEMA_PATHS["reviewable_validation_evidence"],
        ),
        "validators_recorded": [
            "validate-stage5ds",
            "validate-stage5ds-music-source-lock",
            "validate-stage5ds-music-file-inventory",
            "validate-stage5ds-music-message-anchors",
            "validate-stage5ds-music-candidates",
            "validate-stage5ds-ouroboros-context",
            "validate-stage5ds-token-block-static-context",
            "validate-stage5ds-chatgpt-context",
            "validate-stage5ds-source-browser-loadability",
            "validate-stage5ds-scope-control",
        ],
        "source_browser_loadability_validated": source_browser_record.get(
            "source_browser_loadability_validated"
        ),
        "reviewability_gap_register_path": DATA_PATHS["reviewability_gap_register"].as_posix(),
        "metadata_only_validation": True,
    }


def _gap_register(inventory: list[dict[str, Any]]) -> dict[str, Any]:
    missing_expected = sorted(EXPECTED_MUSIC_FILES - {row["file_name"] for row in inventory})
    gaps = [
        {
            "gap_id": "audio-duration-metadata-unavailable",
            "status": "open_reviewability_gap",
            "notes": "No safe local duration metadata tool was used in Stage 5DS.",
        },
        {
            "gap_id": "web-source-locks-not-network-fetched",
            "status": "future_source_review_required",
            "notes": "Ouroboros/self-reference web references are candidate URLs only.",
        },
    ]
    gaps.extend(
        {
            "gap_id": f"missing-expected-community-file-{index}",
            "status": "local_source_missing",
            "file_name": file_name,
        }
        for index, file_name in enumerate(missing_expected, start=1)
    )
    return {
        **_base_payload("stage5ds_reviewability_gap_register"),
        "gap_count": len(gaps),
        "missing_expected_file_count": len(missing_expected),
        "gaps": gaps,
    }


def _scope_control_record() -> dict[str, Any]:
    return {
        **_base_payload("stage5ds_scope_control", SCHEMA_PATHS["scope_control"]),
        "metadata_only": True,
        "source_lock_only": True,
        "stage5ds_is_readiness_stage": False,
        "stage5ds_is_source_lock_addendum": True,
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
    }


def _operator_routing_record() -> dict[str, Any]:
    return {
        **_base_payload("stage5ds_operator_inserted_addendum_routing"),
        "stage5dr_recommended_stage5ds_source_review_readiness": True,
        "operator_inserted_expanded_music_ouroboros_token_static_addendum_first": True,
        "source_review_readiness_planning_still_required_after_this_stage": True,
        "recommended_next_stage_after_stage5ds": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "target_priority_decision_created_now": False,
        "operator_readiness_decision_created_now": False,
    }


def _evidence_status_policy() -> dict[str, Any]:
    return {
        **_base_payload("stage5ds_evidence_status_classification_policy"),
        "policy_status": "active_for_stage5ds_records",
        "candidate_records_are_evidence": False,
        "source_locked_metadata_is_route_evidence": False,
        "review_only_status_required": True,
        "score_or_probability_claims_allowed": False,
        "probability_claim_accepted_as_validated": False,
    }


def _chatgpt_context_update_summary() -> dict[str, Any]:
    return {
        **_base_payload(
            "stage5ds_chatgpt_context_update_summary",
            SCHEMA_PATHS["chatgpt_context_update_summary"],
        ),
        "chatgpt_context_path": "ChatGPT-ContextFile.md",
        "chatgpt_context_updated": True,
        "stage5ds_section_present": True,
        "right_side_stage5dr_gui_note_present": True,
        "raw_source_body_included": False,
    }


def _next_stage_decision() -> dict[str, Any]:
    return {
        **_base_payload(
            "stage5ds_next_stage_decision",
            SCHEMA_PATHS["next_stage_decision"],
        ),
        "status": "complete",
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "stage5dr_source_review_readiness_planning_still_required": True,
        "pivot_target_selected_now": False,
        "active_planning_input_selected_now": False,
        "execution_authorized_now": False,
    }


def _summary_record(
    inventory: list[dict[str, Any]],
    token_static: dict[str, Any],
    source_browser_record: dict[str, Any],
) -> dict[str, Any]:
    return {
        **_base_payload("stage5ds_summary", SCHEMA_PATHS["summary"]),
        "status": "complete",
        "music_community_theory_source_lock_created": True,
        "music_community_theory_file_count": len(inventory),
        "music_audio_file_count": sum(1 for row in inventory if row["file_kind"] == "audio"),
        "music_pdf_file_count": sum(1 for row in inventory if row["file_kind"] == "pdf"),
        "music_image_file_count": sum(1 for row in inventory if row["file_kind"] == "image"),
        "music_candidate_records_created": len(MUSIC_CANDIDATE_PATHS),
        "ouroboros_candidate_records_created": len(OUROBOROS_CANDIDATE_PATHS),
        "token_block_static_candidate_records_created": len(TOKEN_STATIC_PATHS),
        "chatgpt_context_updated": True,
        "source_browser_loadability_validated": source_browser_record.get(
            "source_browser_loadability_validated"
        ),
        "source_browser_entries_loaded": source_browser_record.get("source_browser_entries_loaded"),
        "source_browser_records_scanned": source_browser_record.get("source_browser_records_scanned"),
        "stage5ds_entries_loaded": source_browser_record.get("stage5ds_entries_loaded"),
        "stage5bd_run_plan_id_count": 10,
        "active_lineage_record_count": len(ACTIVE_LINEAGE_PATHS),
        "parallel_worker_cap": PARALLEL_WORKER_CAP,
        "token_block_primary60_first_16_bytes_hex": token_static["first_16_bytes_hex"],
        "token_block_primary60_sha256": token_static["primary60_byte_stream_sha256"],
        "recommended_next_stage_id": NEXT_STAGE_ID,
        "recommended_next_stage_title": NEXT_STAGE_TITLE,
        "stage5dr_recommended_stage5ds_source_review_readiness": True,
        "operator_inserted_expanded_music_ouroboros_token_static_addendum_first": True,
        "source_review_readiness_planning_still_required_after_this_stage": True,
    }


def _gp_record(phrase: str) -> dict[str, Any]:
    value = GP_PHRASE_VALUES[phrase]
    return {
        "phrase": phrase,
        "gp_sum": value,
        "factorization": _factorize(value),
        "is_prime": _is_prime(value),
        "gp_arithmetic_source": "stage5ds_operator_assistant_review_phrase_table",
        "unsupported_Q_K_terms_not_silently_normalized": True,
    }


def _prime_fact(value: int) -> dict[str, Any]:
    return {"value": value, "is_prime": _is_prime(value), "factorization": _factorize(value)}


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value in {2, 3}:
        return True
    if value % 2 == 0 or value % 3 == 0:
        return False
    divisor = 5
    while divisor * divisor <= value:
        if value % divisor == 0 or value % (divisor + 2) == 0:
            return False
        divisor += 6
    return True


def _factorize(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    remaining = value
    while divisor * divisor <= remaining:
        while remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
        divisor += 1 if divisor == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return factors


def _update_chatgpt_context() -> None:
    path = Path("ChatGPT-ContextFile.md")
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    heading = "## Stage 5DS expanded music/Ouroboros/token-block static addendum"
    if heading in text:
        prefix = text.split(heading, 1)[0].rstrip()
        text = prefix + "\n\n" + STAGE5DS_CONTEXT_SECTION
    else:
        text = text.rstrip() + "\n\n" + STAGE5DS_CONTEXT_SECTION
    text = text.replace(
        "Stage 5DR details panel spans the category list and table",
        "Stage 5DR GUI follow-up keeps the details panel as right-side/right-dock source review UI",
    )
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _update_operational_file_map() -> None:
    path = Path("data/project-state/operational-file-map.yaml")
    if not path.exists():
        return
    payload = read_yaml(path)
    records = payload.get("records", [])
    existing = {record.get("path") for record in records if isinstance(record, dict)}
    additions = [
        {
            "path": DATA_PATHS["summary"].as_posix(),
            "category": "active_data_record",
            "purpose": "Stage 5DS metadata-only source-lock addendum summary.",
            "source_of_truth_rank": 1,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "stage_specific",
            "mutable_or_reference_only": "reference_only",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "codex_agent",
            "notes": "Records expanded music/Ouroboros/token-block static context without execution.",
        },
        {
            "path": "ChatGPT-ContextFile.md",
            "category": "operational_status_doc",
            "purpose": "Concise assistant context handoff including Stage 5DS high-value facts.",
            "source_of_truth_rank": 2,
            "last_meaningful_update_stage": STAGE_ID,
            "expected_update_frequency": "every_stage",
            "mutable_or_reference_only": "mutable",
            "mirror_or_generated_relationships": "source",
            "staleness_check_level": "strict",
            "owner_context": "codex_agent",
            "notes": "Must not contain raw source bodies or generated byte streams.",
        },
    ]
    changed = False
    for addition in additions:
        if addition["path"] not in existing:
            records.append(addition)
            changed = True
    if changed:
        payload["records"] = records
        write_yaml(path, payload)


def _write_records(records: dict[str, dict[str, Any]]) -> None:
    for key, payload in records.items():
        write_yaml(DATA_PATHS[key], payload)


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = read_yaml(path)
    return payload if isinstance(payload, dict) else {}


def _validate_schemas() -> list[str]:
    errors: list[str] = []
    schema_pairs = [
        (DATA_PATHS["summary"], SCHEMA_PATHS["summary"]),
        (DATA_PATHS["next_stage_decision"], SCHEMA_PATHS["next_stage_decision"]),
        (DATA_PATHS["scope_control"], SCHEMA_PATHS["scope_control"]),
        (
            DATA_PATHS["reviewable_validation_evidence"],
            SCHEMA_PATHS["reviewable_validation_evidence"],
        ),
        (
            DATA_PATHS["chatgpt_context_update_summary"],
            SCHEMA_PATHS["chatgpt_context_update_summary"],
        ),
        (DATA_PATHS["music_source_lock_register"], SCHEMA_PATHS["music_source_lock_register"]),
        (DATA_PATHS["music_file_inventory"], SCHEMA_PATHS["music_file_inventory"]),
        (
            DATA_PATHS["music_message_attachment_anchor_index"],
            SCHEMA_PATHS["music_message_attachment_anchor_index"],
        ),
        (
            DATA_PATHS["token_block_static_machine_code_scope_control"],
            SCHEMA_PATHS["token_block_static_machine_code_scope_control"],
        ),
    ]
    schema_pairs.extend(
        (path, SCHEMA_PATHS["music_candidate_record"]) for path in MUSIC_CANDIDATE_PATHS.values()
    )
    schema_pairs.extend(
        (path, SCHEMA_PATHS["ouroboros_transform_context_record"])
        for path in OUROBOROS_CANDIDATE_PATHS.values()
    )
    schema_pairs.extend(
        (path, SCHEMA_PATHS["token_block_static_context_record"])
        for path in TOKEN_STATIC_PATHS.values()
    )
    for record_path, schema_path in schema_pairs:
        if not record_path.exists() or not schema_path.exists():
            errors.append(f"schema pair missing: {record_path.as_posix()} / {schema_path.as_posix()}")
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        payload = read_yaml(record_path)
        validator = Draft202012Validator(schema)
        errors.extend(
            f"{record_path.as_posix()}: schema error: {error.message}"
            for error in validator.iter_errors(payload)
        )
    return errors


def _validate_common_payload(path: Path, payload: Any) -> list[str]:
    if not isinstance(payload, dict):
        return [f"{path.as_posix()}: record must be a mapping"]
    errors: list[str] = []
    if payload.get("stage_id") != STAGE_ID:
        errors.append(f"{path.as_posix()}: stage_id must be {STAGE_ID}")
    for key, expected in REQUIRED_STAGE_FLAGS.items():
        if payload.get(key) != expected:
            errors.append(f"{path.as_posix()}: {key} must be {expected}")
    errors.extend(_required_false_errors(payload, path.as_posix()))
    return errors


def _required_false_errors(payload: dict[str, Any], prefix: str = "record") -> list[str]:
    errors: list[str] = []
    for key, value in _iter_items(payload):
        if key in FORBIDDEN_FALSE_FLAGS and value is not False:
            errors.append(f"{prefix}: {key} must be false")
    return errors


def _iter_items(value: Any) -> list[tuple[str, Any]]:
    items: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            items.append((str(key), item))
            items.extend(_iter_items(item))
    elif isinstance(value, list):
        for item in value:
            items.extend(_iter_items(item))
    return items


def _git_value(*args: str) -> str | None:
    result = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _git_lines(*args: str) -> list[str]:
    result = subprocess.run(["git", *args], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _format(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)
