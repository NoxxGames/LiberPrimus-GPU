from __future__ import annotations

import json
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate

TOKEN_SCHEMA_DIR = Path("schemas/token-block")
STEGO_SCHEMA_DIR = Path("schemas/stego")
PROJECT_SCHEMA_DIR = Path("schemas/project-state")


def _schema(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_stage5ap_committed_token_block_schemas_validate() -> None:
    validate(_yaml(Path("data/token-block/stage5ap-page49-51-source-lock.yaml")), _schema(TOKEN_SCHEMA_DIR / "page49-51-source-lock-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-page49-51-image-provenance.yaml")), _schema(TOKEN_SCHEMA_DIR / "page49-51-image-provenance-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-token-block-canonical-transcription.yaml")), _schema(TOKEN_SCHEMA_DIR / "token-block-transcription-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-token-block-coordinate-records.yaml")), _schema(TOKEN_SCHEMA_DIR / "token-block-coordinate-record-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-token-block-alphabet-registry.yaml")), _schema(TOKEN_SCHEMA_DIR / "token-block-alphabet-registry-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-token-block-mapping-preflight.yaml")), _schema(TOKEN_SCHEMA_DIR / "token-block-mapping-preflight-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-token-block-null-control-plan.yaml")), _schema(TOKEN_SCHEMA_DIR / "token-block-null-control-plan-v0.schema.json"))
    validate(_yaml(Path("data/token-block/stage5ap-token-block-dwh-context.yaml")), _schema(TOKEN_SCHEMA_DIR / "token-block-dwh-context-v0.schema.json"))
    validate(_yaml(Path("data/project-state/stage5ap-summary.yaml")), _schema(PROJECT_SCHEMA_DIR / "stage5ap-summary-v0.schema.json"))


def test_stage5ap_committed_stego_schemas_validate() -> None:
    validate(_yaml(Path("data/stego/stage5ap-outguess-positive-control-policy.yaml")), _schema(STEGO_SCHEMA_DIR / "outguess-positive-control-policy-v0.schema.json"))
    validate(_yaml(Path("data/stego/stage5ap-outguess-toolchain-readiness.yaml")), _schema(STEGO_SCHEMA_DIR / "outguess-toolchain-readiness-v0.schema.json"))
    validate(_yaml(Path("data/stego/stage5ap-outguess-positive-control-matrix.yaml")), _schema(STEGO_SCHEMA_DIR / "outguess-positive-control-matrix-v0.schema.json"))
    validate(_yaml(Path("data/stego/stage5ap-outguess-historical-fixture-readiness.yaml")), _schema(STEGO_SCHEMA_DIR / "outguess-historical-fixture-readiness-v0.schema.json"))
    validate(_yaml(Path("data/stego/stage5ap-outguess-guardrail.yaml")), _schema(STEGO_SCHEMA_DIR / "outguess-guardrail-v0.schema.json"))


def test_stage5ap_summary_schema_rejects_solve_claim() -> None:
    payload = _yaml(Path("data/project-state/stage5ap-summary.yaml"))
    payload["solve_claim"] = True
    try:
        validate(payload, _schema(PROJECT_SCHEMA_DIR / "stage5ap-summary-v0.schema.json"))
    except ValidationError:
        return
    raise AssertionError("schema accepted solve_claim=true")
