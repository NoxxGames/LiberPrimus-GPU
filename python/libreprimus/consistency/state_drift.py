"""State-drift checks for long-lived project context."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.paths import repo_root

GROUP = "state_drift"

DEFAULT_OPERATIONAL_FILES = (
    "README.md",
    "STATUS.md",
    "ROADMAP.md",
    "AGENTS.md",
    "ARCHITECTURE.md",
    "CUDA_NOTES.md",
    "RESULTS_SCHEMA.md",
    "EXPERIMENTS.md",
    "TESTING.md",
    "docs/roadmap/staged-plan.md",
    "docs/onboarding/start-here.md",
    "docs/onboarding/source-of-truth-map.md",
    "docs/onboarding/codex-navigation-map.md",
    "docs/onboarding/deep-research-handoff-map.md",
    "docs/onboarding/contributor-module-map.md",
    "docs/onboarding/private-generated-data-map.md",
    "pyproject.toml",
    "docker/README.md",
)

REQUIRED_ONBOARDING_FILES = (
    "docs/onboarding/start-here.md",
    "docs/onboarding/source-of-truth-map.md",
    "docs/onboarding/codex-navigation-map.md",
    "docs/onboarding/deep-research-handoff-map.md",
    "docs/onboarding/contributor-module-map.md",
    "docs/onboarding/private-generated-data-map.md",
)

HISTORICAL_PATH_PARTS = ("docs/development-logs", "research-log")
HISTORICAL_LINE_MARKERS = (
    "historical",
    "implemented since",
    "completed in stage",
    "archive",
    "development log",
    "research log",
    "stage details",
)


@dataclass(frozen=True)
class StalePattern:
    check_id: str
    pattern: re.Pattern[str]
    message: str


STALE_CURRENT_STATE_PATTERNS = (
    StalePattern(
        "stale_current_stage_0a",
        re.compile(r"\bcurrent\s+stage(?:\s+is|:)?\s*stage\s+0a\b", re.IGNORECASE),
        "Stale current-stage claim points to Stage 0A.",
    ),
    StalePattern(
        "stale_current_stage_0d",
        re.compile(r"\bcurrent\s+stage(?:\s+is|:)?\s*stage\s+0d\b", re.IGNORECASE),
        "Stale current-stage claim points to Stage 0D.",
    ),
    StalePattern(
        "stale_stage0a_scaffold",
        re.compile(r"\bstage\s+0a\s+scaffold\b", re.IGNORECASE),
        "Stage 0A scaffold wording is stale in current operational context.",
    ),
    StalePattern(
        "stale_no_result_schema",
        re.compile(r"\bno\s+result\s+schema\b", re.IGNORECASE),
        "Result schema is no longer absent.",
    ),
    StalePattern(
        "stale_result_schema_planned_not_finalized",
        re.compile(r"\bplanned,\s+not\s+finalized\b", re.IGNORECASE),
        "Result schema should not be described as only planned.",
    ),
    StalePattern(
        "stale_no_corpus_loader",
        re.compile(r"\bno\s+corpus\s+loader\b", re.IGNORECASE),
        "Corpus/profile infrastructure now exists; avoid stale no-loader current-state claims.",
    ),
    StalePattern(
        "stale_stage3i_next",
        re.compile(r"\bstage\s+3i\b.*\bnext\b|\bnext\b.*\bstage\s+3i\b", re.IGNORECASE),
        "Stage 3I is not the next stage after Stage 3V.",
    ),
)


def check_state_drift_consistency(
    *,
    root: Path = repo_root(),
    files: tuple[str, ...] = DEFAULT_OPERATIONAL_FILES,
) -> list[ConsistencyCheckResult]:
    """Return consistency results for operational project-state drift."""

    results: list[ConsistencyCheckResult] = []
    texts: dict[str, str] = {}

    for relative in files:
        path = root / relative
        if not path.is_file():
            results.append(fail_result(GROUP, "file_present", f"{relative} is missing.", path=path))
            continue
        text = path.read_text(encoding="utf-8")
        texts[relative] = text
        stale = scan_stale_current_state(text, relative)
        if stale:
            for pattern_id, line_no, line in stale:
                results.append(
                    fail_result(
                        GROUP,
                        pattern_id,
                        f"Stale current-state wording on line {line_no}: {line.strip()}",
                        path=path,
                        data={"line": line_no},
                    )
                )
        else:
            results.append(
                pass_result(
                    GROUP,
                    "no_stale_current_state_claims",
                    f"{relative} has no stale current-state claims.",
                    path=path,
                )
            )

    combined = "\n".join(texts.values()).lower()
    status = texts.get("STATUS.md", "").lower()
    roadmap = texts.get("ROADMAP.md", "").lower()
    agents = texts.get("AGENTS.md", "").lower()
    staged_plan = texts.get("docs/roadmap/staged-plan.md", "").lower()
    private_map = texts.get("docs/onboarding/private-generated-data-map.md", "").lower()
    deep_research_map = texts.get("docs/onboarding/deep-research-handoff-map.md", "").lower()
    pyproject = texts.get("pyproject.toml", "").lower()

    _require_fact(
        results,
        "stage3v_complete",
        "stage 3v" in status and "complete" in status,
        "STATUS records Stage 3V complete.",
        root / "STATUS.md",
    )
    _require_fact(
        results,
        "stage3w_consolidation",
        all("stage 3w" in text for text in (status, roadmap, agents))
        and ("anti-drift" in combined or "state consolidation" in combined),
        "STATUS, ROADMAP, and AGENTS record Stage 3W consolidation.",
        root / "STATUS.md",
    )
    _require_fact(
        results,
        "stage3x_complete",
        "stage 3x" in staged_plan and "complete" in staged_plan,
        "Staged plan records Stage 3X complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage3y_complete",
        "stage 3y" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 3Y complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage3z_current_or_complete",
        "stage 3z" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan or "source-of-truth" in staged_plan),
        "Staged plan records Stage 3Z current/complete source-of-truth work.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4a_discord_research_bundle",
        "stage 4a" in staged_plan
        and "discord research-bundle" in staged_plan
        and "deep research" in staged_plan,
        "Staged plan records Stage 4A full Discord research-bundle extraction for Deep Research.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4a_current_or_complete",
        "stage 4a" in staged_plan and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4A as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4b_source_lock_visual_intake",
        "stage 4b" in staged_plan
        and "source-lock" in staged_plan
        and "visual observation" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4B source-lock triage and visual observation intake.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4c_cuneiform_dot_current_or_complete",
        "stage 4c" in staged_plan
        and "cuneiform" in staged_plan
        and "dot" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4C cuneiform/dot annotation as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4d_bounded_numeric_verifier_current_or_complete",
        "stage 4d" in staged_plan
        and "bounded numeric verifier" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4D bounded numeric verifier pack as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4e_cookie_exact_candidate_refresh_next",
        "stage 4e" in staged_plan
        and "cookie exact-candidate refresh" in staged_plan,
        "Staged plan records Stage 4E cookie exact-candidate refresh as next.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "canonical_corpus_inactive",
        "canonical corpus" in combined and "inactive" in combined,
        "Canonical corpus is documented as inactive.",
        root / "README.md",
    )
    _require_fact(
        results,
        "page_boundaries_reviewable",
        "page boundaries" in combined and "reviewable" in combined,
        "Page boundaries are documented as reviewable.",
        root / "README.md",
    )
    _require_fact(
        results,
        "cuda_deferred",
        "cuda" in combined and "deferred" in combined,
        "CUDA is documented as deferred.",
        root / "CUDA_NOTES.md",
    )
    _require_fact(
        results,
        "staged_plan_cuda_deferred",
        "cuda" in staged_plan and "deferred" in staged_plan,
        "Staged plan records CUDA as deferred.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "no_solve_claims",
        "no solve claim" in combined or "no solve claims" in combined,
        "No-solve-claim policy is documented.",
        root / "README.md",
    )
    _require_fact(
        results,
        "raw_generated_not_committed",
        _has_line_with_terms(combined, ("raw", "generated", "not committed")),
        "Raw/generated output non-commit policy is documented.",
        root / "README.md",
    )
    _require_fact(
        results,
        "discord_raw_logs_not_committed",
        _has_line_with_terms(combined, ("discord", "raw logs", "not committed")),
        "Discord raw-log non-commit policy is documented.",
        root / "AGENTS.md",
    )
    _require_fact(
        results,
        "local_page_images_not_committed",
        _has_line_with_terms(combined, ("page images", "not committed")),
        "Local page-image non-commit policy is documented.",
        root / "AGENTS.md",
    )
    _require_fact(
        results,
        "staged_plan_update_policy",
        "update policy" in staged_plan and "direction-change policy" in staged_plan,
        "Staged plan includes update and direction-change policy.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "discord_raw_logs_private_ignored",
        "discord raw logs" in staged_plan
        and "local" in staged_plan
        and "private" in staged_plan
        and "ignored" in staged_plan,
        "Staged plan records Discord raw logs as local/private/ignored.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "agents_docs_text_update_policy",
        ".md" in agents and ".txt" in agents and "staged-plan" in agents and "direction change" in agents,
        "AGENTS records staged-plan and markdown/text update policy for direction changes.",
        root / "AGENTS.md",
    )
    _require_fact(
        results,
        "private_generated_data_map_core_paths",
        all(
            term in private_map
            for term in (
                "discord",
                "page images",
                "experiments/results",
                "data/raw",
                "data/normalized",
            )
        ),
        "Private/generated data map records core raw and generated paths.",
        root / "docs/onboarding/private-generated-data-map.md",
    )
    _require_fact(
        results,
        "private_generated_data_map_stage4a_site",
        "discord-full-review" in private_map
        and "stage4a" in private_map
        and "static site" in private_map,
        "Private/generated data map records Stage 4A static-site output.",
        root / "docs/onboarding/private-generated-data-map.md",
    )
    _require_fact(
        results,
        "deep_research_handoff_stage4a_bundle",
        "stage 4a" in deep_research_map
        and "research-bundle" in deep_research_map
        and "redacted" in deep_research_map,
        "Deep Research handoff map records the Stage 4A redacted bundle.",
        root / "docs/onboarding/deep-research-handoff-map.md",
    )
    for relative in REQUIRED_ONBOARDING_FILES:
        _require_fact(
            results,
            f"onboarding_{Path(relative).stem.replace('-', '_')}_present",
            (root / relative).is_file(),
            f"{relative} exists.",
            root / relative,
        )
    _require_fact(
        results,
        "pyproject_not_stage0a_scaffold",
        "stage 0a scaffold" not in pyproject,
        "pyproject description is not a Stage 0A scaffold description.",
        root / "pyproject.toml",
    )
    return results


def scan_stale_current_state(text: str, relative_path: str | Path) -> list[tuple[str, int, str]]:
    """Return stale current-state pattern hits for one file."""

    path_text = str(relative_path).replace("\\", "/").lower()
    if any(part in path_text for part in HISTORICAL_PATH_PARTS):
        return []

    findings: list[tuple[str, int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if _is_historical_line(line):
            continue
        for stale in STALE_CURRENT_STATE_PATTERNS:
            if stale.pattern.search(line):
                findings.append((stale.check_id, line_no, line))
    return findings


def _is_historical_line(line: str) -> bool:
    lower = line.lower()
    return any(marker in lower for marker in HISTORICAL_LINE_MARKERS)


def _has_line_with_terms(text: str, terms: tuple[str, ...]) -> bool:
    return any(all(term in line for term in terms) for line in text.splitlines())


def _require_fact(
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
