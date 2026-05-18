from __future__ import annotations

from pathlib import Path

from libreprimus.consistency.state_drift import DEFAULT_OPERATIONAL_FILES, check_state_drift_consistency


def test_stage3y_state_drift_passes_current_repo() -> None:
    failures = [result for result in check_state_drift_consistency() if result.is_failure]

    assert failures == []


def test_stage3y_state_drift_fails_if_staged_plan_missing(tmp_path: Path) -> None:
    _write_minimal_operational_docs(tmp_path)
    (tmp_path / "docs/roadmap/staged-plan.md").unlink()

    failures = [result for result in check_state_drift_consistency(root=tmp_path) if result.is_failure]

    assert any(result.check_name == "file_present" for result in failures)


def test_stage3y_state_drift_fails_if_staged_plan_omits_cuda_deferred(tmp_path: Path) -> None:
    _write_minimal_operational_docs(tmp_path)
    staged_plan = tmp_path / "docs/roadmap/staged-plan.md"
    staged_plan.write_text(_staged_plan_text(cuda_text="CUDA acceleration is active."), encoding="utf-8")

    failures = [result for result in check_state_drift_consistency(root=tmp_path) if result.is_failure]

    assert any(result.check_name == "staged_plan_cuda_deferred" for result in failures)


def _write_minimal_operational_docs(root: Path) -> None:
    for relative in DEFAULT_OPERATIONAL_FILES:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if relative == "docs/roadmap/staged-plan.md":
            path.write_text(_staged_plan_text(), encoding="utf-8")
        elif relative == "pyproject.toml":
            path.write_text('[project]\ndescription = "Current bounded Liber Primus workbench"\n', encoding="utf-8")
        else:
            path.write_text(
                "\n".join(
                    [
                        "Stage 3V complete.",
                        "Stage 3W state consolidation and anti-drift hardening.",
                        "Stage 3X CLI modularisation complete.",
                        "Stage 3Y result synthesis and method-retirement ledger.",
                        "Canonical corpus is inactive.",
                        "Page boundaries are reviewable.",
                        "CUDA is deferred.",
                        "No solve claim.",
                        "Raw data and generated outputs are not committed.",
                        "Discord raw logs are local private ignored material and are not committed.",
                        "Local page images are not committed.",
                    ]
                ),
                encoding="utf-8",
            )


def _staged_plan_text(*, cuda_text: str = "CUDA is deferred.") -> str:
    return "\n".join(
        [
            "# Staged Plan",
            "Stage 3V complete.",
            "Stage 3W complete.",
            "Stage 3X complete.",
            "Current stage: Stage 3Y result synthesis.",
            "Canonical corpus is inactive.",
            "Page boundaries are reviewable.",
            cuda_text,
            "No solve claims.",
            "Raw and generated outputs are ignored and not committed.",
            "Discord raw logs are local private ignored material.",
            "Direction-change policy.",
            "Update policy.",
        ]
    )
