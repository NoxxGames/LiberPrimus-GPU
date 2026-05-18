"""Stage 3O Discord promotion and Wiki mirror consistency checks."""

from __future__ import annotations

import subprocess
from pathlib import Path

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.discord_promotion.validation import validate_promoted_records
from libreprimus.paths import repo_root

GROUP = "discord_promotion"
PROMOTED_LINKS = repo_root() / "data/observations/discord/promoted-public-source-links-stage3o.yaml"
PROMOTED_METHODS = repo_root() / "data/observations/discord/promoted-method-claim-candidates-stage3o.yaml"
PROMOTED_NUMERICS = repo_root() / "data/observations/discord/promoted-numeric-observation-candidates-stage3o.yaml"
WIKI_HOME = repo_root() / "docs/wiki-source/Home.md"
WIKI_SIDEBAR = repo_root() / "docs/wiki-source/_Sidebar.md"
TUTORIAL_DIR = repo_root() / "tutorials"
WIKI_SOURCE_DIR = repo_root() / "docs/wiki-source"


def check_discord_promotion_consistency(root: Path = repo_root()) -> list[ConsistencyCheckResult]:
    """Run raw-log-free Stage 3O consistency checks."""
    results: list[ConsistencyCheckResult] = []

    counts, errors = validate_promoted_records(
        links=PROMOTED_LINKS,
        methods=PROMOTED_METHODS,
        numerics=PROMOTED_NUMERICS,
        allow_empty=True,
    )
    if errors:
        for error in errors:
            results.append(fail_result(GROUP, "promoted_records_valid", error))
    else:
        results.append(
            pass_result(
                GROUP,
                "promoted_records_valid",
                f"Promoted Discord records are redacted and reviewable: {counts}.",
            )
        )

    for path in [
        "third_party/LiberPrimusDiscordChats/example.html",
        "experiments/results/discord-promotion/stage3o/promotion_candidates.jsonl",
        "experiments/results/wiki-sync/stage3o/wiki-sync-report.json",
        ".wiki-worktree/Home.md",
    ]:
        if _is_ignored(root, path):
            results.append(pass_result(GROUP, "stage3o_path_ignored", f"Ignored path is ignored: {path}", path=path))
        else:
            results.append(fail_result(GROUP, "stage3o_path_ignored", f"Expected ignored path is trackable: {path}", path=path))

    for path in [
        PROMOTED_LINKS,
        PROMOTED_METHODS,
        PROMOTED_NUMERICS,
        WIKI_HOME,
        WIKI_SIDEBAR,
        repo_root() / "scripts/github/sync-tutorials-to-wiki.ps1",
        repo_root() / "scripts/github/validate-wiki-source.ps1",
    ]:
        rel_path = path.relative_to(root).as_posix()
        if _is_ignored(root, rel_path):
            results.append(fail_result(GROUP, "stage3o_path_trackable", f"Expected committed path is ignored: {rel_path}", path=rel_path))
        else:
            results.append(pass_result(GROUP, "stage3o_path_trackable", f"Committed path is trackable: {rel_path}", path=rel_path))

    wiki_errors = _validate_wiki_source()
    if not wiki_errors:
        results.append(pass_result(GROUP, "wiki_source_valid", "Wiki source validates."))
    else:
        for error in wiki_errors:
            results.append(fail_result(GROUP, "wiki_source_valid", error))

    return results


def _is_ignored(root: Path, path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", "--", path],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def _validate_wiki_source() -> list[str]:
    errors: list[str] = []
    if not WIKI_HOME.is_file():
        errors.append("missing Home.md")
    if not WIKI_SIDEBAR.is_file():
        errors.append("missing _Sidebar.md")
    if not TUTORIAL_DIR.is_dir():
        errors.append("missing tutorials directory")
        return errors
    for tutorial in sorted(TUTORIAL_DIR.glob("*.md")):
        page = WIKI_SOURCE_DIR / _wiki_page_name(tutorial.name)
        if not page.is_file():
            errors.append(f"missing wiki page for {tutorial.name}")
            continue
        text = page.read_text(encoding="utf-8")
        if "repository tutorial file is the source of truth" not in text:
            errors.append(f"missing source-of-truth notice in {page.name}")
        if "record_type: discord_extracted_link" in text or '"record_type": "discord_extracted_link"' in text:
            errors.append(f"possible generated output dump in {page.name}")
    return errors


def _wiki_page_name(file_name: str) -> str:
    stem = Path(file_name).stem
    parts = []
    for part in stem.split("-"):
        parts.append(part if part.isdigit() else part.capitalize())
    return f"{' '.join(parts)}.md"
