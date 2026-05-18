from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

REPO = Path(__file__).resolve().parents[2]


def _schema(path: str) -> dict:
    return json.loads((REPO / path).read_text(encoding="utf-8"))


def test_stage3r_schemas_validate_sample_records() -> None:
    source_schema = _schema("schemas/history/promoted-discord-source-record-v0.schema.json")
    observation_schema = _schema("schemas/history/promoted-discord-observation-record-v0.schema.json")
    negative_schema = _schema("schemas/history/negative-control-record-v0.schema.json")
    manifest_schema = _schema("schemas/experiments/post-discord-experiment-manifest-v0.schema.json")

    Draft202012Validator(source_schema).validate(
        {
            "record_type": "promoted_discord_source_record",
            "promoted_id": "stage3r-source-test",
            "source_url": "https://github.com/example/repo",
            "normalized_url": "https://github.com/example/repo",
            "source_title": "Example",
            "source_class": "strong_community_technical",
            "promotion_class": "source_to_lock",
            "corroboration_basis": "public URL",
            "discord_lead_reference": "synthetic",
            "public_source_required": True,
            "raw_message_committed": False,
            "username_committed": False,
            "private_url_committed": False,
            "trusted_as_canonical": False,
            "review_status": "human_review_required",
            "notes": "",
        }
    )
    Draft202012Validator(observation_schema).validate(
        {
            "record_type": "promoted_discord_observation_record",
            "observation_id": "stage3r-observation-test",
            "observation_type": "onion7_raw_4x4_table",
            "source_url": "https://uncovering-cicada.fandom.com/wiki/Onion_7:_numbers_on_page_15",
            "source_title": "Onion 7",
            "values": {"shape": "4x4"},
            "derived_values": {},
            "promotion_class": "observation_to_review",
            "corroboration_basis": "public source",
            "ambiguity_notes": "",
            "usable_as_experiment_seed": False,
            "raw_message_committed": False,
            "username_committed": False,
            "private_url_committed": False,
            "trusted_as_canonical": False,
            "review_status": "review_required",
            "notes": "",
        }
    )
    Draft202012Validator(negative_schema).validate(
        {
            "record_type": "negative_control_record",
            "negative_control_id": "stage3r-negative-test",
            "false_positive_class": "qr_noise",
            "description": "synthetic",
            "source_url": "",
            "basis": "test",
            "recommended_use": "negative control",
            "raw_message_committed": False,
            "username_committed": False,
            "private_url_committed": False,
            "trusted_as_canonical": False,
            "solve_claim": False,
            "notes": "",
        }
    )
    Draft202012Validator(manifest_schema).validate(
        {
            "record_type": "post_discord_experiment_manifest",
            "experiment_id": "EXP-3R-001",
            "description": "synthetic",
            "hypothesis": "synthetic",
            "source_basis": [],
            "candidate_count_cap": 576,
            "execution_enabled": False,
            "cpu_only": True,
            "cuda_enabled": False,
            "cloud_execution": False,
            "paid_services": False,
            "generated_outputs_committed": False,
            "no_solve_claim": True,
            "canonical_corpus_active": False,
            "page_boundaries_final": False,
            "required_inputs": [],
            "controls": [],
            "stop_conditions": [],
            "notes": "",
        }
    )


def test_gp_rune_claim_schema_requires_noncanonical_no_solve_policy() -> None:
    schema = _schema("schemas/experiments/gp-rune-claim-record-v0.schema.json")
    Draft202012Validator(schema).validate(
        {
            "record_type": "gp_rune_claim_record",
            "claim_id": "claim-test",
            "source_basis": "synthetic",
            "claim_type": "gp_sum",
            "target_span": "locked span pending",
            "claimed_value": 3301,
            "value_type": "integer",
            "computation_policy": "future exact recomputation",
            "verification_status": "missing_source_span",
            "trusted_as_canonical": False,
            "no_solve_claim": True,
            "notes": "",
        }
    )
