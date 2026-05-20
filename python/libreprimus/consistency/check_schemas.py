"""Schema consistency checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "schemas"
SCHEMA_ROOT = repo_root() / "schemas"
RESULTS_SCHEMA_DOC = repo_root() / "RESULTS_SCHEMA.md"
EXPECTED_SCHEMA_FILES = [
    "corpus/solved-page-fixture-v0.schema.json",
    "corpus/solved-baseline-run-manifest-v0.schema.json",
    "experiments/exploratory-experiment-manifest-v0.schema.json",
    "experiments/exploratory-dry-run-plan-v0.schema.json",
    "experiments/exploratory-transform-space-v0.schema.json",
    "experiments/exploratory-safety-gate-v0.schema.json",
    "experiments/exploratory-corpus-slice-v0.schema.json",
    "experiments/cpu-execution-manifest-v0.schema.json",
    "experiments/cpu-execution-plan-v0.schema.json",
    "experiments/cpu-execution-result-v0.schema.json",
    "experiments/synthetic-corpus-record-v0.schema.json",
    "experiments/execution-safety-gate-v0.schema.json",
    "experiments/experiment-proposal-v0.schema.json",
    "experiments/experiment-review-packet-v0.schema.json",
    "experiments/experiment-approval-record-v0.schema.json",
    "experiments/experiment-review-checklist-v0.schema.json",
    "experiments/approval-gated-execution-request-v0.schema.json",
    "experiments/approval-gated-execution-plan-v0.schema.json",
    "experiments/approval-gated-execution-result-v0.schema.json",
    "experiments/approval-readiness-packet-v0.schema.json",
    "experiments/operator-policy-v0.schema.json",
    "experiments/post-discord-experiment-manifest-v0.schema.json",
    "experiments/gp-rune-claim-record-v0.schema.json",
    "experiments/bounded-experiment-queue-v0.schema.json",
    "experiments/bounded-experiment-item-v0.schema.json",
    "experiments/policy-check-result-v0.schema.json",
    "experiments/bounded-auto-run-result-v0.schema.json",
    "experiments/bounded-candidate-record-v0.schema.json",
    "experiments/bounded-experiment-run-summary-v0.schema.json",
    "scoring/minimal-triage-score-v0.schema.json",
    "scoring/scoring-control-record-v0.schema.json",
    "scoring/scoring-calibration-summary-v0.schema.json",
    "scoring/crib-check-result-v0.schema.json",
    "results/experiment-run-record-v0.schema.json",
    "results/experiment-run-summary-v0.schema.json",
    "results/experiment-result-store-manifest-v0.schema.json",
    "results/sqlite-result-store-v0.schema.json",
    "stego/stego-artifact-record-v0.schema.json",
    "stego/outguess-regression-manifest-v0.schema.json",
    "stego/outguess-extraction-record-v0.schema.json",
    "stego/outguess-regression-summary-v0.schema.json",
    "stego/outguess-tool-record-v0.schema.json",
    "history/discord-full-review-channel-record-v0.schema.json",
    "history/discord-full-review-message-record-v0.schema.json",
    "history/discord-full-review-shard-record-v0.schema.json",
    "history/discord-full-review-index-record-v0.schema.json",
    "history/discord-full-review-summary-v0.schema.json",
    "visual/lp-page-gallery-record-v0.schema.json",
    "visual/discord-image-reference-v0.schema.json",
    "benchmarks/cpu-benchmark-plan-v0.schema.json",
    "benchmarks/cpu-benchmark-smoke-record-v0.schema.json",
    "benchmarks/benchmark-environment-record-v0.schema.json",
    "benchmarks/cuda-parity-benchmark-readiness-v0.schema.json",
    "benchmarks/stage4q-benchmark-parity-summary-v0.schema.json",
    "cuda/cuda-target-plan-record-v0.schema.json",
    "cuda/cuda-parity-scaffold-record-v0.schema.json",
    "cuda/cuda-implementation-gate-record-v0.schema.json",
    "cuda/cuda-non-target-record-v0.schema.json",
    "cuda/cuda-planning-summary-v0.schema.json",
    "cuda/cuda-parity-harness-record-v0.schema.json",
    "cuda/cuda-parity-fixture-record-v0.schema.json",
    "cuda/cuda-backend-capability-record-v0.schema.json",
    "cuda/cuda-future-kernel-parity-matrix-v0.schema.json",
    "cuda/stage5b-cuda-parity-harness-summary-v0.schema.json",
    "cuda/cuda-build-profile-record-v0.schema.json",
    "cuda/cuda-toolchain-detection-record-v0.schema.json",
    "cuda/cuda-device-detection-record-v0.schema.json",
    "cuda/cuda-smoke-build-record-v0.schema.json",
    "cuda/stage5c-cuda-build-device-summary-v0.schema.json",
    "native-cpu/native-cpu-backend-capability-record-v0.schema.json",
    "native-cpu/native-cpu-threading-record-v0.schema.json",
    "native-cpu/native-cpu-parity-record-v0.schema.json",
    "native-cpu/native-cpu-diagnostic-record-v0.schema.json",
    "native-cpu/stage5d-native-cpu-summary-v0.schema.json",
    "cuda/cuda-first-kernel-contract-record-v0.schema.json",
    "cuda/cuda-adapter-selection-record-v0.schema.json",
    "cuda/cuda-native-parity-adapter-record-v0.schema.json",
    "cuda/cuda-implementation-readiness-record-v0.schema.json",
    "cuda/stage5e-first-kernel-contract-summary-v0.schema.json",
]
EXPECTED_DOC_TERMS = [
    "experiment-run-record-v0",
    "experiment-run-summary-v0",
    "exploratory-experiment-manifest-v0",
    "exploratory-dry-run-plan-v0",
    "cpu-execution-manifest-v0",
    "cpu-execution-result-v0",
    "experiment-proposal-v0",
    "experiment-review-packet-v0",
    "approval-gated-execution-request-v0",
    "approval-gated-execution-result-v0",
    "approval-readiness-packet-v0",
    "operator-policy-v0",
    "post-discord-experiment-manifest-v0",
    "gp-rune-claim-record-v0",
    "bounded-experiment-queue-v0",
    "policy-check-result-v0",
    "bounded-auto-run-result-v0",
    "bounded-candidate-record-v0",
    "bounded-experiment-run-summary-v0",
    "minimal-triage-score-v0",
    "scoring-control-record-v0",
    "scoring-calibration-summary-v0",
    "crib-check-result-v0",
    "solved-page-fixture",
    "solved-baseline-run-manifest-v0",
    "stego-artifact-record-v0",
    "outguess-regression-manifest-v0",
    "outguess-extraction-record-v0",
    "outguess-regression-summary-v0",
    "outguess-tool-record-v0",
    "discord-full-review-channel-record-v0",
    "discord-full-review-message-record-v0",
    "discord-full-review-shard-record-v0",
    "discord-full-review-index-record-v0",
    "discord-full-review-summary-v0",
    "lp-page-gallery-record-v0",
    "discord-image-reference-v0",
    "cpu-benchmark-plan-v0",
    "cpu-benchmark-smoke-record-v0",
    "benchmark-environment-record-v0",
    "cuda-parity-benchmark-readiness-v0",
    "stage4q-benchmark-parity-summary-v0",
    "cuda-target-plan-record-v0",
    "cuda-parity-scaffold-record-v0",
    "cuda-implementation-gate-record-v0",
    "cuda-non-target-record-v0",
    "cuda-planning-summary-v0",
    "cuda-parity-harness-record-v0",
    "cuda-parity-fixture-record-v0",
    "cuda-backend-capability-record-v0",
    "cuda-future-kernel-parity-matrix-v0",
    "stage5b-cuda-parity-harness-summary-v0",
    "cuda-build-profile-record-v0",
    "cuda-toolchain-detection-record-v0",
    "cuda-device-detection-record-v0",
    "cuda-smoke-build-record-v0",
    "stage5c-cuda-build-device-summary-v0",
    "native-cpu-backend-capability-record-v0",
    "native-cpu-threading-record-v0",
    "native-cpu-parity-record-v0",
    "native-cpu-diagnostic-record-v0",
    "stage5d-native-cpu-summary-v0",
    "cuda-first-kernel-contract-record-v0",
    "cuda-adapter-selection-record-v0",
    "cuda-native-parity-adapter-record-v0",
    "cuda-implementation-readiness-record-v0",
    "stage5e-first-kernel-contract-summary-v0",
]


def check_schema_consistency(
    schema_root: Path = SCHEMA_ROOT,
    *,
    results_schema_doc: Path = RESULTS_SCHEMA_DOC,
) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    schema_files = sorted(schema_root.rglob("*.schema.json"))
    if not schema_files:
        return [fail_result(GROUP, "schema_files_exist", "No schema files found.", path=schema_root)]
    results.append(pass_result(GROUP, "schema_files_exist", "Schema files found.", data={"count": len(schema_files)}))

    payloads: list[tuple[Path, dict[str, Any]]] = []
    for path in schema_files:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ValueError("Schema must be a JSON object.")
            payloads.append((path, payload))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            results.append(fail_result(GROUP, "schema_json_parse", str(exc), path=path))
    if not any(result.check_name == "schema_json_parse" and result.is_failure for result in results):
        results.append(pass_result(GROUP, "schema_json_parse", "All schemas parse as JSON."))

    for relative in EXPECTED_SCHEMA_FILES:
        path = schema_root / relative
        if path.is_file():
            results.append(pass_result(GROUP, "expected_schema_exists", f"Expected schema exists: {relative}"))
        else:
            results.append(fail_result(GROUP, "expected_schema_exists", f"Missing schema: {relative}", path=path))

    _check_unique_metadata(results, payloads)
    _check_record_types_unique(results, payloads)
    _check_trusted_as_canonical(results, payloads)

    doc_text = results_schema_doc.read_text(encoding="utf-8") if results_schema_doc.is_file() else ""
    missing_terms = [term for term in EXPECTED_DOC_TERMS if term not in doc_text]
    if missing_terms:
        results.append(
            fail_result(
                GROUP,
                "results_schema_doc_terms",
                f"RESULTS_SCHEMA.md is missing schema terms: {missing_terms}",
                path=results_schema_doc,
            )
        )
    else:
        results.append(pass_result(GROUP, "results_schema_doc_terms", "RESULTS_SCHEMA.md mentions key schemas."))
    return results


def _check_unique_metadata(
    results: list[ConsistencyCheckResult],
    payloads: list[tuple[Path, dict[str, Any]]],
) -> None:
    seen: dict[str, Path] = {}
    duplicates: list[str] = []
    for path, payload in payloads:
        for key in ["$id", "title"]:
            value = payload.get(key)
            if not value:
                continue
            label = f"{key}:{value}"
            if label in seen:
                duplicates.append(label)
            seen[label] = path
    if duplicates:
        results.append(fail_result(GROUP, "schema_metadata_unique", f"Duplicate schema metadata: {duplicates}"))
    else:
        results.append(pass_result(GROUP, "schema_metadata_unique", "Schema $id/title values are unique."))


def _record_type_const(payload: dict[str, Any]) -> str | None:
    properties = payload.get("properties", {})
    if not isinstance(properties, dict):
        return None
    record_type = properties.get("record_type", {})
    if isinstance(record_type, dict) and isinstance(record_type.get("const"), str):
        return str(record_type["const"])
    return None


def _check_record_types_unique(
    results: list[ConsistencyCheckResult],
    payloads: list[tuple[Path, dict[str, Any]]],
) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for _, payload in payloads:
        record_type = _record_type_const(payload)
        if record_type is None:
            continue
        if record_type in seen:
            duplicates.add(record_type)
        seen.add(record_type)
    if duplicates:
        results.append(fail_result(GROUP, "schema_record_types_unique", f"Duplicate record_type consts: {sorted(duplicates)}"))
    else:
        results.append(pass_result(GROUP, "schema_record_types_unique", "Schema record_type constants are unique."))


def _check_trusted_as_canonical(
    results: list[ConsistencyCheckResult],
    payloads: list[tuple[Path, dict[str, Any]]],
) -> None:
    failures: list[str] = []
    for path, payload in payloads:
        properties = payload.get("properties", {})
        if not isinstance(properties, dict) or "trusted_as_canonical" not in properties:
            continue
        trusted = properties.get("trusted_as_canonical")
        if not isinstance(trusted, dict) or trusted.get("const") is not False:
            failures.append(str(path))
    if failures:
        results.append(
            fail_result(
                GROUP,
                "trusted_as_canonical_false",
                f"Schemas permit trusted_as_canonical drift: {failures}",
            )
        )
    else:
        results.append(
            pass_result(
                GROUP,
                "trusted_as_canonical_false",
                "Schemas with trusted_as_canonical require false.",
            )
        )
