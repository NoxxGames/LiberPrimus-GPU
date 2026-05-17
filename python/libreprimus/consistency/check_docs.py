"""Documentation consistency checks."""

from __future__ import annotations

from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "docs"
README = repo_root() / "README.md"
STATUS = repo_root() / "STATUS.md"
ROADMAP = repo_root() / "ROADMAP.md"
AGENTS = repo_root() / "AGENTS.md"
CIPHER_CATALOG = repo_root() / "CIPHER_CATALOG.md"


def check_docs_consistency(
    *,
    readme_path: Path = README,
    status_path: Path = STATUS,
    roadmap_path: Path = ROADMAP,
    agents_path: Path = AGENTS,
    cipher_catalog_path: Path = CIPHER_CATALOG,
) -> list[ConsistencyCheckResult]:
    results: list[ConsistencyCheckResult] = []
    readme = _read(readme_path)
    status = _read(status_path)
    roadmap = _read(roadmap_path)
    agents = _read(agents_path)
    catalog = _read(cipher_catalog_path)

    _require(results, "readme_stage2b", "Stage 2B" in readme and "complete" in readme.lower(), "README mentions Stage 2B complete.", readme_path)
    _require(results, "readme_stage2c", "Stage 2C" in readme and "complete" in readme.lower(), "README mentions Stage 2C complete.", readme_path)
    _require(results, "readme_stage2d_next", "Stage 2D" in readme, "README points to Stage 2D.", readme_path)
    _require(results, "readme_stage2e", "Stage 2E" in readme and "complete" in readme.lower(), "README mentions Stage 2E complete.", readme_path)
    _require(results, "readme_stage2f_next", "Stage 2F" in readme, "README points to Stage 2F.", readme_path)
    _require(results, "readme_stage2f", "Stage 2F" in readme and "complete" in readme.lower(), "README mentions Stage 2F complete.", readme_path)
    _require(results, "readme_stage2g_next", "Stage 2G" in readme, "README points to Stage 2G.", readme_path)
    _require(results, "readme_stage2g", "Stage 2G" in readme and "complete" in readme.lower(), "README mentions Stage 2G complete.", readme_path)
    _require(results, "readme_stage2h_next", "Stage 2H" in readme, "README points to Stage 2H.", readme_path)
    _require(results, "readme_stage2h", "Stage 2H" in readme and "complete" in readme.lower(), "README mentions Stage 2H complete.", readme_path)
    _require(results, "readme_stage2i", "Stage 2I" in readme and "complete" in readme.lower(), "README mentions Stage 2I complete.", readme_path)
    _require(results, "readme_stage2j", "Stage 2J" in readme and "complete" in readme.lower(), "README mentions Stage 2J complete.", readme_path)
    _require(results, "readme_stage3a", "Stage 3A" in readme and "complete" in readme.lower(), "README mentions Stage 3A complete.", readme_path)
    _require(results, "readme_stage3b", "Stage 3B" in readme and "complete" in readme.lower(), "README mentions Stage 3B complete.", readme_path)
    _require(results, "readme_stage3c", "Stage 3C" in readme and "complete" in readme.lower(), "README mentions Stage 3C complete.", readme_path)
    _require(results, "readme_stage3d", "Stage 3D" in readme and "complete" in readme.lower(), "README mentions Stage 3D complete.", readme_path)
    _require(results, "readme_stage3e", "Stage 3E" in readme and "complete" in readme.lower(), "README mentions Stage 3E complete.", readme_path)
    _require(results, "readme_stage3f", "Stage 3F" in readme and "complete" in readme.lower(), "README mentions Stage 3F complete.", readme_path)
    _require(results, "readme_stage3g_next", "Stage 3G" in readme, "README points to Stage 3G.", readme_path)
    _require(results, "status_stage2d", "Stage 2D" in status, "STATUS mentions Stage 2D.", status_path)
    _require(results, "status_stage2e", "Stage 2E" in status, "STATUS mentions Stage 2E.", status_path)
    _require(results, "status_stage2f", "Stage 2F" in status, "STATUS mentions Stage 2F.", status_path)
    _require(results, "status_stage2g", "Stage 2G" in status, "STATUS mentions Stage 2G.", status_path)
    _require(results, "status_stage2h", "Stage 2H" in status, "STATUS mentions Stage 2H.", status_path)
    _require(results, "status_stage2i", "Stage 2I" in status, "STATUS mentions Stage 2I.", status_path)
    _require(results, "status_stage2j", "Stage 2J" in status, "STATUS mentions Stage 2J.", status_path)
    _require(results, "status_stage3a", "Stage 3A" in status, "STATUS mentions Stage 3A.", status_path)
    _require(results, "status_stage3b", "Stage 3B" in status, "STATUS mentions Stage 3B.", status_path)
    _require(results, "status_stage3c", "Stage 3C" in status, "STATUS mentions Stage 3C.", status_path)
    _require(results, "status_stage3d", "Stage 3D" in status, "STATUS mentions Stage 3D.", status_path)
    _require(results, "status_stage3e", "Stage 3E" in status, "STATUS mentions Stage 3E.", status_path)
    _require(results, "status_stage3f", "Stage 3F" in status, "STATUS mentions Stage 3F.", status_path)
    _require(results, "roadmap_stage2d", "Stage 2D" in roadmap, "ROADMAP mentions Stage 2D.", roadmap_path)
    _require(results, "roadmap_stage2e", "Stage 2E" in roadmap, "ROADMAP mentions Stage 2E.", roadmap_path)
    _require(results, "roadmap_stage2f", "Stage 2F" in roadmap, "ROADMAP mentions Stage 2F.", roadmap_path)
    _require(results, "roadmap_stage2g", "Stage 2G" in roadmap, "ROADMAP mentions Stage 2G.", roadmap_path)
    _require(results, "roadmap_stage2h", "Stage 2H" in roadmap, "ROADMAP mentions Stage 2H.", roadmap_path)
    _require(results, "roadmap_stage2i", "Stage 2I" in roadmap, "ROADMAP mentions Stage 2I.", roadmap_path)
    _require(results, "roadmap_stage2j", "Stage 2J" in roadmap, "ROADMAP mentions Stage 2J.", roadmap_path)
    _require(results, "roadmap_stage3a", "Stage 3A" in roadmap, "ROADMAP mentions Stage 3A.", roadmap_path)
    _require(results, "roadmap_stage3b", "Stage 3B" in roadmap, "ROADMAP mentions Stage 3B.", roadmap_path)
    _require(results, "roadmap_stage3c", "Stage 3C" in roadmap, "ROADMAP mentions Stage 3C.", roadmap_path)
    _require(results, "roadmap_stage3d", "Stage 3D" in roadmap, "ROADMAP mentions Stage 3D.", roadmap_path)
    _require(results, "roadmap_stage3e", "Stage 3E" in roadmap, "ROADMAP mentions Stage 3E.", roadmap_path)
    _require(results, "roadmap_stage3f", "Stage 3F" in roadmap, "ROADMAP mentions Stage 3F.", roadmap_path)
    _require(results, "roadmap_stage3g", "Stage 3G" in roadmap, "ROADMAP mentions Stage 3G.", roadmap_path)
    for path, text, minimum in [
        (readme_path, readme, 50),
        (status_path, status, 20),
        (roadmap_path, roadmap, 20),
    ]:
        _require(
            results,
            "public_markdown_multiline",
            len(text.splitlines()) > minimum,
            f"{path.name} is readable multi-line Markdown.",
            path,
        )
    for phrase in [
        "data/raw/",
        "generated outputs",
        "canonical corpus",
        "Push after successful commit",
        "raw-data-free",
    ]:
        _require(
            results,
            "agents_safety_rules",
            phrase.lower() in agents.lower(),
            f"AGENTS.md includes safety rule phrase: {phrase}",
            agents_path,
        )
    lower_catalog = catalog.lower()
    unsafe_claims = [
        "search_enabled=true",
        "supports_gpu=true",
        "generic search is implemented",
        "cuda acceleration implemented",
    ]
    _require(
        results,
        "cipher_catalog_no_search_cuda_claims",
        not any(claim in lower_catalog for claim in unsafe_claims),
        "CIPHER_CATALOG does not claim search/CUDA implementation.",
        cipher_catalog_path,
    )
    lower_readme = readme.lower()
    _require(
        results,
        "readme_no_unsolved_solve_claim",
        "unsolved page is claimed solved" not in lower_readme
        and "no liber primus page is claimed solved" in lower_readme,
        "README does not claim an unsolved page solve.",
        readme_path,
    )
    return results


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def _require(
    results: list[ConsistencyCheckResult],
    name: str,
    condition: bool,
    message: str,
    path: Path,
) -> None:
    if condition:
        results.append(pass_result(GROUP, name, message, path=path))
    else:
        results.append(fail_result(GROUP, name, message, path=path))
