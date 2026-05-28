from jsonschema import Draft202012Validator

from test_stage5bj_crosswalk_closure import load_json, load_yaml


SCHEMA_TO_DATA = [
    (
        "schemas/historical-route/stage5bj-crosswalk-closure-plan-v0.schema.json",
        "data/historical-route/stage5bj-crosswalk-closure-plan.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-original-archive-crosswalk-closure-v0.schema.json",
        "data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-2014-exact-surface-source-lock-v0.schema.json",
        "data/historical-route/stage5bj-2014-exact-surface-source-locks.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-fandom-page-body-crosswalk-v0.schema.json",
        "data/historical-route/stage5bj-fandom-page-body-crosswalk.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-boards-thread-crosswalk-v0.schema.json",
        "data/historical-route/stage5bj-boards-thread-crosswalk.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-high-priority-candidate-status-v0.schema.json",
        "data/historical-route/stage5bj-high-priority-candidate-status.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-media-equivalence-closure-v0.schema.json",
        "data/historical-route/stage5bj-media-equivalence-closure.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-source-gap-update-v0.schema.json",
        "data/historical-route/stage5bj-source-gap-update.yaml",
    ),
    (
        "schemas/historical-route/stage5bj-guardrail-v0.schema.json",
        "data/historical-route/stage5bj-guardrail.yaml",
    ),
    (
        "schemas/token-block/stage5bj-token-block-lineage-preservation-v0.schema.json",
        "data/token-block/stage5bj-token-block-lineage-preservation.yaml",
    ),
    (
        "schemas/token-block/stage5bj-2014-surface-context-closure-v0.schema.json",
        "data/token-block/stage5bj-2014-surface-context-closure.yaml",
    ),
    (
        "schemas/source-harvester/stage5bj-local-archive-inspection-summary-v0.schema.json",
        "data/source-harvester/stage5bj-local-archive-inspection-summary.yaml",
    ),
    (
        "schemas/source-harvester/stage5bj-source-snapshot-inspection-summary-v0.schema.json",
        "data/source-harvester/stage5bj-source-snapshot-inspection-summary.yaml",
    ),
    ("schemas/project-state/stage5bj-summary-v0.schema.json", "data/project-state/stage5bj-summary.yaml"),
    (
        "schemas/project-state/stage5bj-next-stage-decision-v0.schema.json",
        "data/project-state/stage5bj-next-stage-decision.yaml",
    ),
]


def test_stage5bj_yaml_records_validate_against_schemas() -> None:
    for schema_path, data_path in SCHEMA_TO_DATA:
        schema = load_json(schema_path)
        payload = load_yaml(data_path)
        Draft202012Validator(schema).validate(payload)
