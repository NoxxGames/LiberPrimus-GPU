from __future__ import annotations

from pathlib import Path

from libreprimus.consistency.check_docs import check_docs_consistency


def _write_docs(tmp_path: Path, *, readme_extra: str = "", catalog_extra: str = "") -> dict[str, Path]:
    readme = tmp_path / "README.md"
    status = tmp_path / "STATUS.md"
    roadmap = tmp_path / "ROADMAP.md"
    agents = tmp_path / "AGENTS.md"
    catalog = tmp_path / "CIPHER_CATALOG.md"
    readme.write_text(
        "# Title\n\n"
        "No Liber Primus page is claimed solved.\n\n"
        "## Current status\n\n"
        "Stage 2B complete. Stage 2C complete. Next Stage 2D.\n"
        + ("Line\n" * 60)
        + readme_extra,
        encoding="utf-8",
    )
    status.write_text("# Status\n\nStage 2D current.\n" + ("Line\n" * 30), encoding="utf-8")
    roadmap.write_text("# Roadmap\n\nStage 2D next.\n" + ("Line\n" * 30), encoding="utf-8")
    agents.write_text(
        "data/raw/ generated outputs canonical corpus Push after successful commit raw-data-free",
        encoding="utf-8",
    )
    catalog.write_text("CPU reference transforms only.\n" + catalog_extra, encoding="utf-8")
    return {
        "readme_path": readme,
        "status_path": status,
        "roadmap_path": roadmap,
        "agents_path": agents,
        "cipher_catalog_path": catalog,
    }


def test_current_docs_pass() -> None:
    assert not [result for result in check_docs_consistency() if result.is_failure]


def test_stale_readme_stage2b_next_sample_fails(tmp_path: Path) -> None:
    paths = _write_docs(tmp_path, readme_extra="Next milestone: Stage 2B\n")
    paths["readme_path"].write_text("# stale\nNext milestone: Stage 2B\n", encoding="utf-8")

    failures = check_docs_consistency(**paths)

    assert any(result.check_name.startswith("readme_") for result in failures if result.is_failure)


def test_readme_claiming_unsolved_page_solved_fails(tmp_path: Path) -> None:
    paths = _write_docs(tmp_path, readme_extra="An unsolved page is claimed solved.\n")

    failures = check_docs_consistency(**paths)

    assert any(result.check_name == "readme_no_unsolved_solve_claim" for result in failures if result.is_failure)


def test_cipher_catalog_claiming_cuda_search_fails(tmp_path: Path) -> None:
    paths = _write_docs(tmp_path, catalog_extra="generic search is implemented\nsupports_gpu=true\n")

    failures = check_docs_consistency(**paths)

    assert any(result.check_name == "cipher_catalog_no_search_cuda_claims" for result in failures if result.is_failure)
