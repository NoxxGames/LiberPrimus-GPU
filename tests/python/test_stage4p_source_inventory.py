from __future__ import annotations

import json
from pathlib import Path

from libreprimus.result_store.source_inventory import build_source_inventory_from_manifest


def test_source_inventory_marks_missing_generated_output(tmp_path: Path) -> None:
    manifest = _manifest(
        tmp_path,
        [
            {
                "source_id": "missing",
                "source_stage_id": "stage-test",
                "result_source_kind": "synthetic_test_fixture",
                "source_path": str(tmp_path / "missing.json"),
                "optional_generated": True,
                "method_family": "unknown",
            }
        ],
    )
    records, warnings = build_source_inventory_from_manifest(manifest, out_dir=tmp_path / "out")
    assert records[0]["source_presence_status"] == "optional_generated_missing"
    assert warnings


def test_source_inventory_skips_raw_required_paths(tmp_path: Path) -> None:
    manifest = _manifest(
        tmp_path,
        [
            {
                "source_id": "raw",
                "source_stage_id": "stage-test",
                "result_source_kind": "bounded_experiment_summary",
                "source_path": "data/raw/transcripts/example.txt",
                "raw_required": True,
            }
        ],
    )
    records, _ = build_source_inventory_from_manifest(manifest, out_dir=tmp_path / "out")
    assert records[0]["source_presence_status"] == "skipped_raw_required"
    assert records[0]["raw_data_processed"] is False


def test_source_inventory_is_deterministic(tmp_path: Path) -> None:
    source = tmp_path / "summary.json"
    source.write_text(json.dumps({"record_type": "synthetic_summary"}), encoding="utf-8")
    manifest = _manifest(
        tmp_path,
        [
            {
                "source_id": "present",
                "source_stage_id": "stage-test",
                "result_source_kind": "synthetic_test_fixture",
                "source_path": str(source),
                "required": True,
            }
        ],
    )
    first, _ = build_source_inventory_from_manifest(manifest, out_dir=tmp_path / "one")
    second, _ = build_source_inventory_from_manifest(manifest, out_dir=tmp_path / "two")
    assert first == second


def _manifest(tmp_path: Path, sources: list[dict]) -> Path:
    manifest = tmp_path / "manifest.yaml"
    manifest.write_text(
        "\n".join(
            [
                "record_type: result_store_unification_manifest",
                "cpu_only: true",
                "cuda_used: false",
                "cuda_required: false",
                "no_solve_claim: true",
                "canonical_corpus_active: false",
                "page_boundaries_final: false",
                "generated_outputs_committed: false",
                "raw_data_processed: false",
                "new_experiment_executed: false",
                "new_scorer_added: false",
                "sources:",
            ]
        )
        + "\n"
        + "\n".join("  - " + json.dumps(source) for source in sources)
        + "\n",
        encoding="utf-8",
    )
    return manifest
