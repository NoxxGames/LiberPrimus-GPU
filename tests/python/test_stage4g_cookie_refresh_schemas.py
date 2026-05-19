from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


SCHEMAS = [
    "schemas/web/cookie-refresh-manifest-v0.schema.json",
    "schemas/web/cookie-refresh-candidate-record-v0.schema.json",
    "schemas/web/cookie-refresh-summary-v0.schema.json",
]


def test_stage4g_schemas_parse() -> None:
    for schema_path in SCHEMAS:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)


def test_stage4g_candidate_schema_requires_source_basis() -> None:
    schema = json.loads(Path("schemas/web/cookie-refresh-candidate-record-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    record = _candidate_record()
    record["source_basis"] = ""
    assert list(validator.iter_errors(record))


def test_stage4g_candidate_schema_rejects_fuzzy_partial_and_cuda_flags() -> None:
    schema = json.loads(Path("schemas/web/cookie-refresh-candidate-record-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for key in ("fuzzy_matching", "partial_matching", "cuda_used", "hashcat_used"):
        record = _candidate_record()
        record[key] = True
        assert list(validator.iter_errors(record)), key


def test_stage4g_summary_schema_enforces_no_solve_claim() -> None:
    schema = json.loads(Path("schemas/web/cookie-refresh-summary-v0.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    record = {
        "record_type": "cookie_refresh_summary",
        "stage": "stage4g",
        "experiment_id": "exp_stage4b_cookie_pack_v2",
        "target_cookie_count": 1,
        "source_backed_base_string_count": 1,
        "byte_variant_count": 1,
        "algorithms_run": ["sha256"],
        "generated_candidates_before_dedup": 1,
        "candidates_after_dedup": 1,
        "duplicate_count": 0,
        "previous_pack_duplicate_count": 0,
        "comparison_count": 1,
        "exact_match_count": 0,
        "candidate_count_upper_bound": 384,
        "exact_match_only": True,
        "fuzzy_matching": False,
        "partial_matching": False,
        "hashcat_used": False,
        "cuda_used": False,
        "cloud_execution": False,
        "no_solve_claim": False,
        "trusted_as_canonical": False,
        "generated_outputs_committed": False,
    }
    assert list(validator.iter_errors(record))


def _candidate_record() -> dict:
    return {
        "record_type": "cookie_refresh_candidate_record",
        "experiment_id": "exp_stage4b_cookie_pack_v2",
        "candidate_id": "stage4g-cookie-candidate-000001",
        "base_string_id": "base-1",
        "source_record_id": "source-1",
        "source_basis": "source-backed exact string",
        "raw_string_redacted_if_needed": "167",
        "byte_variant": "raw",
        "encoding": "utf-8",
        "algorithm": "sha256",
        "candidate_bytes_sha256": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "digest_hex": "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        "target_cookie_id": "cookie-2013-167-v0",
        "target_cookie_value": "6941f707ff39d259ff71657a79cb6b54c184d2f0455810109c1a960860bde0e6",
        "exact_match": False,
        "previous_pack_duplicate": False,
        "no_solve_claim": True,
        "cuda_used": False,
        "cloud_execution": False,
        "trusted_as_canonical": False,
        "exact_match_only": True,
        "fuzzy_matching": False,
        "partial_matching": False,
        "hashcat_used": False,
        "broad_search": False,
    }
