from __future__ import annotations

import json

from jsonschema import Draft202012Validator

from test_stage5dx_common import ensure_stage5dx_built, load_yaml


def test_stage5dx_overlay_file_validates_each_overlay_against_schema() -> None:
    ensure_stage5dx_built()
    schema = json.loads(
        open("schemas/operator-console/source-browser-number-fact-enrichment-overlay-v0.schema.json", encoding="utf-8").read()
    )
    collection = load_yaml(
        "data/operator-console/source-browser/number-fact-overlays/"
        "stage5dx-review-batch-002-visual-transform-overlays.yaml"
    )
    validator = Draft202012Validator(schema)

    assert collection["record_type"] == "source_browser_number_fact_enrichment_overlay_collection"
    assert collection["reviewed_entry_count"] == 20
    assert collection["overlay_count"] == 23
    for overlay in collection["overlays"]:
        validator.validate(overlay)
        assert overlay["usable_for_decision_now"] is False
        assert {"proof", "route_seed", "execution_seed", "solve_claim"} <= set(overlay["not_allowed_as"])
        assert overlay["relation"]
        assert overlay["why_stored"]
        assert overlay["verification_status"]
        assert overlay["risk_notes"]


def test_stage5dx_summary_schema_rejects_solve_claim() -> None:
    ensure_stage5dx_built()
    schema = json.loads(open("schemas/project-state/stage5dx-summary-v0.schema.json", encoding="utf-8").read())
    summary = load_yaml("data/project-state/stage5dx-summary.yaml")
    summary["solve_claim"] = True

    errors = list(Draft202012Validator(schema).iter_errors(summary))

    assert errors
