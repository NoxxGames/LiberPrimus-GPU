"""State-drift checks for long-lived project context."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from libreprimus.consistency.models import ConsistencyCheckResult, fail_result, pass_result
from libreprimus.observation_review.path_sanitisation import check_paths_summary
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
    StalePattern(
        "stale_next_stage4i",
        re.compile(r"\bnext:\s*stage\s+4i\b", re.IGNORECASE),
        "Stage 4I is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4k",
        re.compile(r"\bnext:\s*stage\s+4k\b", re.IGNORECASE),
        "Stage 4K is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4l",
        re.compile(r"\bnext:\s*stage\s+4l\b", re.IGNORECASE),
        "Stage 4L is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4m",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+4m\b", re.IGNORECASE),
        "Stage 4M is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4n",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+4n\b", re.IGNORECASE),
        "Stage 4N is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4o",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+4o\b", re.IGNORECASE),
        "Stage 4O is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4p",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+4p\b", re.IGNORECASE),
        "Stage 4P is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage4q",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+4q\b", re.IGNORECASE),
        "Stage 4Q is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5a",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5a\b", re.IGNORECASE),
        "Stage 5A is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5b",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5b\b", re.IGNORECASE),
        "Stage 5B is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5c",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5c\b", re.IGNORECASE),
        "Stage 5C is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5d",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5d\b", re.IGNORECASE),
        "Stage 5D is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5e",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5e\b", re.IGNORECASE),
        "Stage 5E is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5f",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5f\b", re.IGNORECASE),
        "Stage 5F is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5g",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5g\b", re.IGNORECASE),
        "Stage 5G is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5h",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5h\b", re.IGNORECASE),
        "Stage 5H is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5i",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5i\b", re.IGNORECASE),
        "Stage 5I is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5j",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5j\b", re.IGNORECASE),
        "Stage 5J is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5k",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5k\b", re.IGNORECASE),
        "Stage 5K is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5l",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5l\b", re.IGNORECASE),
        "Stage 5L is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5m",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5m\b", re.IGNORECASE),
        "Stage 5M is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5n",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5n\b", re.IGNORECASE),
        "Stage 5N is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_next_stage5o",
        re.compile(r"\bnext(?:\s+planned\s+stage)?\s*:\s*stage\s+5o\b", re.IGNORECASE),
        "Stage 5O is complete and should not be described as the next stage.",
    ),
    StalePattern(
        "stale_stage3z_current",
        re.compile(r"\bstage\s+3z\s+current\b", re.IGNORECASE),
        "Stage 3Z is no longer the current stage.",
    ),
    StalePattern(
        "stale_stage3y_latest_completed",
        re.compile(r"\bstage\s+3y\s+is\s+the\s+latest\s+completed\b", re.IGNORECASE),
        "Stage 3Y is no longer the latest completed stage.",
    ),
    StalePattern(
        "stale_deferred_after_stage4d",
        re.compile(r"\bdeferred\s+work\s+after\s+stage\s+4d\b", re.IGNORECASE),
        "Stage 4D deferred-work wording is stale in current operational context.",
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
        duplicate_entries = scan_duplicate_stage_list_entries(text, relative)
        if duplicate_entries:
            for line_no, line in duplicate_entries:
                results.append(
                    fail_result(
                        GROUP,
                        "duplicate_stage_list_entry",
                        f"Duplicate adjacent stage-list entry on line {line_no}: {line.strip()}",
                        path=path,
                        data={"line": line_no},
                    )
                )
        else:
            results.append(
                pass_result(
                    GROUP,
                    "no_duplicate_stage_list_entries",
                    f"{relative} has no duplicate adjacent stage-list entries.",
                    path=path,
                )
            )
        redundant_current_status = scan_redundant_current_status_label(text, relative)
        if redundant_current_status:
            for line_no, line in redundant_current_status:
                results.append(
                    fail_result(
                        GROUP,
                        "redundant_current_status_label",
                        f"Redundant Current status label on line {line_no}: {line.strip()}",
                        path=path,
                        data={"line": line_no},
                    )
                )
        else:
            results.append(
                pass_result(
                    GROUP,
                    "no_redundant_current_status_label",
                    f"{relative} has no redundant Current status label.",
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
        "stage4e_source_delta_audit_current_or_complete",
        "stage 4e" in staged_plan
        and "source-lock delta audit" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4E source-lock delta audit as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4f_outguess_audio_source_lock_current_or_complete",
        "stage 4f" in staged_plan
        and "outguess" in staged_plan
        and "audio" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4F OutGuess/audio source-locking as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4g_cookie_exact_candidate_current_or_complete",
        "stage 4g" in staged_plan
        and "cookie" in staged_plan
        and "exact" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4G cookie exact-candidate refresh as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4h_cpu_batch_transform_current_or_complete",
        "stage 4h" in staged_plan
        and "cpu batch" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4H CPU batch transform API extraction as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4i_scorer_consolidation_current_or_complete",
        "stage 4i" in staged_plan
        and "scorer" in staged_plan
        and "calibration" in staged_plan,
        "Staged plan records Stage 4I scorer consolidation and calibration report as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4j_observation_review_current_or_complete",
        "stage 4j" in staged_plan
        and "observation review" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4J observation review workflow hardening as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4k_source_lock_snapshots_current_or_complete",
        "stage 4k" in staged_plan
        and "source-lock" in staged_plan
        and "snapshot" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4K allowlisted public source-lock snapshots as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4l_reviewed_observation_promotion_current_or_complete",
        "stage 4l" in staged_plan
        and "reviewed observation promotion ledger" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4L reviewed observation promotion ledger as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4m_image_source_variant_compression_current_or_complete",
        "stage 4m" in staged_plan
        and "image source-variant" in staged_plan
        and "compression preflight" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4M image source-variant and compression preflight as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4n_outguess_audio_positive_control_current_or_complete",
        "stage 4n" in staged_plan
        and "outguess" in staged_plan
        and "audio" in staged_plan
        and "positive-control" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4N OutGuess/audio positive-control completion as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4o_cpu_batch_adapter_current_or_complete",
        "stage 4o" in staged_plan
        and "cpu batch" in staged_plan
        and "adapter expansion" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4O CPU batch adapter expansion as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4p_result_store_score_summary_current_or_complete",
        "stage 4p" in staged_plan and "result-store" in staged_plan and "score-summary" in staged_plan,
        "Staged plan records Stage 4P result-store and score-summary unification as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage4q_cpu_benchmark_parity_current_or_complete",
        "stage 4q" in staged_plan
        and "cpu benchmark" in staged_plan
        and "parity planning" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 4Q CPU benchmark and parity planning as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5a_cuda_planning_next",
        "stage 5a" in staged_plan
        and "cuda planning" in staged_plan
        and "parity scaffolding" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5A CUDA planning and parity scaffolding as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5b_cuda_parity_harness_current_or_complete",
        "stage 5b" in staged_plan
        and "cuda parity harness skeleton" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 5B CUDA parity harness skeleton as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5c_cuda_build_device_detection_current_or_complete",
        "stage 5c" in staged_plan
        and "cuda build" in staged_plan
        and "device-detection scaffold" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 5C CUDA build and device-detection scaffold as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5d_native_cpp_cpu_backend_current_or_complete",
        "stage 5d" in staged_plan
        and "native c++ cpu batch backend" in staged_plan
        and "deterministic threading baseline" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 5D native C++ CPU batch backend as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5e_first_cuda_kernel_contract_current_or_complete",
        "stage 5e" in staged_plan
        and "first cuda kernel contract" in staged_plan
        and "cpu/native parity adapter selection" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 5E first CUDA kernel contract and CPU/native parity adapter selection as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5f_synthetic_cuda_parity_kernel_current_or_complete",
        "stage 5f" in staged_plan
        and "first synthetic-only cuda parity kernel implementation" in staged_plan
        and ("current" in staged_plan or "complete" in staged_plan),
        "Staged plan records Stage 5F first synthetic-only CUDA parity kernel implementation as current or complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5g_shift_score_reporting_complete",
        "stage 5g" in staged_plan
        and "shift_score cuda parity reporting" in staged_plan
        and "solved-fixture-safe adapter preflight" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5G shift_score CUDA parity reporting and solved-fixture-safe adapter preflight as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5h_gematria_shift_score_contract_complete",
        "stage 5h" in staged_plan
        and "gematria mod-29" in staged_plan
        and "shift_score contract" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5H Gematria mod-29 shift_score contract preparation as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5i_gematria_synthetic_cuda_parity_complete",
        "stage 5i" in staged_plan
        and "gematria mod-29" in staged_plan
        and "synthetic cuda parity" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5I Gematria mod-29 synthetic CUDA parity preparation as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5j_gematria_synthetic_cuda_kernel_complete",
        "stage 5j" in staged_plan
        and "gematria mod-29" in staged_plan
        and "synthetic cuda parity" in staged_plan
        and "kernel implementation" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5J Gematria mod-29 synthetic CUDA parity kernel implementation as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5k_gematria_parity_reporting_complete",
        "stage 5k" in staged_plan
        and "gematria" in staged_plan
        and "parity reporting" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5K Gematria parity reporting as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5l_gematria_token_mapping_complete",
        "stage 5l" in staged_plan
        and "gematria" in staged_plan
        and "token mapping" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5L Gematria token mapping as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5m_gematria_solved_fixture_cuda_parity_complete",
        "stage 5m" in staged_plan
        and "solved-fixture-safe" in staged_plan
        and "cuda parity" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5M solved-fixture-safe CUDA parity as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5n_gematria_solved_fixture_cuda_reporting_complete",
        "stage 5n" in staged_plan
        and "solved-fixture-safe" in staged_plan
        and "controlled expansion gate" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5N solved-fixture-safe CUDA reporting as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5o_gematria_solved_fixture_repeat_complete",
        "stage 5o" in staged_plan
        and "solved-fixture-safe" in staged_plan
        and "repeat verification" in staged_plan
        and "result-store preflight" in staged_plan
        and "complete" in staged_plan,
        "Staged plan records Stage 5O solved-fixture-safe repeat verification and result-store preflight as complete.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stage5p_controlled_result_store_next",
        "stage 5p" in staged_plan
        and "controlled" in staged_plan
        and "result-store" in staged_plan,
        "Staged plan records Stage 5P controlled result-store integration as next.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "source_lock_snapshot_policy_present",
        "source-lock snapshot" in combined and "allowlisted" in combined and "snapshot policy" in combined,
        "Allowlisted public source-lock snapshot policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "observation_review_workflow_present",
        "observation review" in combined and "promotion" in combined and "experiment seed" in combined,
        "Observation review and promotion gates are documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "observation_promotion_ledger_present",
        "promotion ledger" in combined and "ready_for_manifest" in combined and "control-only" in combined,
        "Reviewed observation promotion ledger policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "image_preflight_policy_present",
        "image preflight" in combined and "compression" in combined and "source variants" in combined,
        "Image source-variant and compression preflight policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "stego_positive_control_readiness_policy_present",
        "positive-control readiness" in combined
        and "expected output" in combined
        and "stego/audio" in combined,
        "Stego/audio positive-control readiness policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cpu_batch_adapter_expansion_policy_present",
        "cpu batch adapter expansion" in combined
        and "parity expectations" in combined
        and "transform semantics" in combined,
        "CPU batch adapter expansion and future CUDA parity expectations are documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "result_store_score_summary_unification_policy_present",
        "result-store" in combined
        and "score-summary" in combined
        and "unified result" in combined
        and "triage" in combined,
        "Result-store and score-summary unification policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cpu_benchmark_parity_planning_policy_present",
        "cpu benchmark" in combined
        and "parity planning" in combined
        and "gpu benchmark" in combined
        and "stage 5a" in combined,
        "CPU benchmark and future CUDA parity planning policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cuda_planning_parity_scaffolding_policy_present",
        "cuda planning" in combined
        and "parity scaffolding" in combined
        and "stage 5b" in combined
        and "speedup claim" in combined,
        "CUDA planning and parity scaffolding policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cuda_parity_harness_skeleton_policy_present",
        "cuda parity harness skeleton" in combined
        and "future kernel" in combined
        and "backend capability" in combined
        and "speedup claim" in combined,
        "CUDA parity harness skeleton and backend capability policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cuda_build_device_detection_policy_present",
        "cuda build" in combined
        and "device detection" in combined
        and "no-gpu" in combined
        and "local 16gb" in combined
        and "speedup claim" in combined,
        "CUDA build/device detection and no-GPU policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "native_cpu_backend_policy_present",
        "native c++ cpu" in combined
        and "deterministic threading" in combined
        and "python" in combined
        and "orchestration" in combined
        and "speedup claim" in combined,
        "Native C++ CPU backend and deterministic threading policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cuda_kernel_contract_policy_present",
        "first cuda kernel contract" in combined
        and "contract only" in combined
        and "stage 5f" in combined
        and "synthetic-only" in combined,
        "First CUDA kernel contract selection policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "synthetic_cuda_kernel_policy_present",
        "synthetic-only cuda parity kernel" in combined
        and "shift_score_kernel" in combined
        and "no-gpu" in combined
        and "speedup claim" in combined,
        "Stage 5F synthetic-only CUDA kernel and no-GPU policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "cuda_parity_reporting_device_subset_policy_present",
        "shift_score cuda parity reporting" in combined
        and "conservative cuda-c" in combined
        and "solved-fixture-safe" in combined
        and "stage 5h" in combined,
        "Stage 5G CUDA parity reporting, device-code subset, and solved-fixture-safe preflight policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_shift_contract_policy_present",
        "gematria mod-29" in combined
        and "shift_score contract" in combined
        and "stage 5i" in combined
        and "native parity fixture" in combined,
        "Stage 5H Gematria mod-29 shift_score contract and native parity fixture policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_cuda_preparation_policy_present",
        "gematria cuda preparation" in combined
        and "cuda-c abi" in combined
        and "stage 5j" in combined
        and "stage 5h" in combined,
        "Stage 5I Gematria CUDA preparation and Stage 5J implementation boundary is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_cuda_kernel_policy_present",
        "gematria cuda kernel" in combined
        and "gematria_mod29_shift_score_kernel" in combined
        and "stage 5k" in combined
        and "speedup claim" in combined,
        "Stage 5J Gematria CUDA kernel and Stage 5K reporting boundary is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_cuda_parity_reporting_policy_present",
        "gematria cuda parity reporting" in combined
        and "solved-fixture-safe" in combined
        and "stage 5l" in combined
        and "no-gpu" in combined,
        "Stage 5K Gematria CUDA parity reporting and Stage 5L token-mapping boundary is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_solved_fixture_mapping_policy_present",
        "solved-fixture-safe gematria token mapping" in combined
        and "native parity" in combined
        and "stage 5m" in combined
        and "explicit future-stage approval" in combined,
        "Stage 5L solved-fixture-safe Gematria token mapping and native parity boundary is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_solved_fixture_cuda_parity_policy_present",
        "solved-fixture-safe gematria cuda parity" in combined
        and "gematria_mod29_shift_score_kernel" in combined
        and "stage 5n" in combined
        and "no new cuda kernels" in combined,
        "Stage 5M solved-fixture-safe Gematria CUDA parity boundary is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_solved_fixture_cuda_reporting_gate_policy_present",
        "solved-fixture-safe gematria cuda parity reporting" in combined
        and "controlled expansion gate" in combined
        and "no-unsolved" in combined
        and "stage 5o" in combined,
        "Stage 5N solved-fixture-safe Gematria CUDA reporting and no-unsolved expansion gate is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "gematria_solved_fixture_cuda_repeat_policy_present",
        "solved-fixture-safe gematria cuda repeat" in combined
        and "result-store preflight" in combined
        and "stage 5p" in combined
        and "no new cuda kernels" in combined,
        "Stage 5O solved-fixture-safe Gematria CUDA repeat and result-store preflight policy is documented.",
        root / "docs/roadmap/staged-plan.md",
    )
    _require_fact(
        results,
        "scoring_contract_present",
        "scoring contract" in combined and "triage" in combined,
        "Scoring contract is documented as triage-only infrastructure.",
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
    path_summary = check_paths_summary(root)
    if path_summary["path_sanitisation_passed"]:
        results.append(
            pass_result(
                GROUP,
                "no_absolute_local_paths",
                "Operational docs and records contain no unsafe absolute local paths.",
                path=root,
            )
        )
    else:
        results.append(
            fail_result(
                GROUP,
                "no_absolute_local_paths",
                "Operational docs or records contain unsafe local paths or stale current-state text.",
                path=root,
                data=path_summary,
            )
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


def scan_duplicate_stage_list_entries(text: str, relative_path: str | Path) -> list[tuple[int, str]]:
    """Return duplicate Stage bullet entries inside contiguous stage-list blocks."""

    path_text = str(relative_path).replace("\\", "/").lower()
    if any(part in path_text for part in HISTORICAL_PATH_PARTS):
        return []

    findings: list[tuple[int, str]] = []
    seen_in_block: set[str] = set()
    for line_no, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith(("-", "*")):
            seen_in_block.clear()
            continue
        match = re.match(r"^[-*]\s+stage\s+\d+[a-z]?\b", stripped, re.IGNORECASE)
        if not match:
            continue
        key = re.sub(r"\s+", " ", stripped.lower())
        if key in seen_in_block and not _is_historical_line(line):
            findings.append((line_no, line))
        seen_in_block.add(key)
    return findings


def scan_redundant_current_status_label(text: str, relative_path: str | Path) -> list[tuple[int, str]]:
    """Return headings where `## Current status` is followed by `Current status:`."""

    path_text = str(relative_path).replace("\\", "/").lower()
    if any(part in path_text for part in HISTORICAL_PATH_PARTS):
        return []

    findings: list[tuple[int, str]] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower() != "## current status":
            continue
        for next_index in range(index + 1, len(lines)):
            next_line = lines[next_index].strip()
            if not next_line:
                continue
            if next_line.lower().startswith("current status:"):
                findings.append((next_index + 1, lines[next_index]))
            break
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
