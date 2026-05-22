from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from libreprimus.prime_minus_one_native_contract.candidate_batch_mapping import build_candidate_batch_mapping
from libreprimus.prime_minus_one_native_contract.guardrails import build_guardrails
from libreprimus.prime_minus_one_native_contract.native_parity_preparation import build_native_parity_preparation
from libreprimus.prime_minus_one_native_contract.next_stage_decision import build_next_stage_decision
from libreprimus.prime_minus_one_native_contract.prime_schedule import build_prime_schedule
from libreprimus.prime_minus_one_native_contract.result_store_preflight import build_result_store_preflight
from libreprimus.prime_minus_one_native_contract.source_inventory import build_source_inventory
from libreprimus.prime_minus_one_native_contract.stream_contract import build_stream_contract


SCHEMA_CASES = (
    ("schemas/cuda/prime-minus-one-source-inventory-record-v0.schema.json", build_source_inventory, "source_inventory_out"),
    ("schemas/cuda/prime-minus-one-stream-contract-record-v0.schema.json", build_stream_contract, "stream_contract_out"),
    ("schemas/cuda/prime-minus-one-schedule-record-v0.schema.json", build_prime_schedule, "prime_schedule_out"),
    ("schemas/cuda/prime-minus-one-candidate-batch-mapping-record-v0.schema.json", build_candidate_batch_mapping, "candidate_batch_mapping_out"),
    ("schemas/cuda/prime-minus-one-native-parity-preparation-record-v0.schema.json", build_native_parity_preparation, "native_parity_preparation_out"),
    ("schemas/cuda/prime-minus-one-result-store-preflight-record-v0.schema.json", build_result_store_preflight, "result_store_preflight_out"),
    ("schemas/cuda/prime-minus-one-guardrail-record-v0.schema.json", build_guardrails, "guardrail_out"),
    ("schemas/cuda/prime-minus-one-next-stage-decision-record-v0.schema.json", build_next_stage_decision, "next_stage_decision_out"),
)


def test_stage5w_record_schemas_validate(tmp_path: Path) -> None:
    for schema_path, builder, output_kwarg in SCHEMA_CASES:
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        records = builder(**{output_kwarg: tmp_path / f"{output_kwarg}.yaml", "out_dir": tmp_path})
        for record in records:
            validator.validate(record)

