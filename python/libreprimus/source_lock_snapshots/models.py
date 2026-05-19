"""Models and constants for Stage 4K source-lock snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_OUT_DIR = Path("experiments/results/source-lock-snapshots/stage4k")
DEFAULT_CACHE_DIR = Path("third_party/SourceSnapshots")
DEFAULT_SNAPSHOT_RECORDS_OUT = Path(
    "data/locks/third-party/source-snapshots/stage4k-source-lock-snapshot-records.yaml"
)
DEFAULT_FETCH_RECORDS_OUT = Path("data/locks/third-party/source-snapshots/stage4k-source-fetch-records.yaml")
DEFAULT_COPYRIGHT_RECORDS_OUT = Path(
    "data/locks/third-party/source-snapshots/stage4k-source-copyright-policy-records.yaml"
)
DEFAULT_SUMMARY_OUT = Path("data/locks/third-party/source-snapshots/stage4k-source-lock-summary.yaml")

SOURCE_RECORD_PATHS = {
    "stage4b_sources": Path("data/observations/archive/stage4b-promoted-source-records.yaml"),
    "stage4e_source_delta": Path("data/observations/archive/stage4e-cicada-solvers-iddqd-source-delta.yaml"),
    "stage4f_outguess": Path("data/observations/stego/stage4f-outguess-fixture-source-records.yaml"),
    "stage4f_audio": Path("data/observations/stego/stage4f-audio-fixture-source-records.yaml"),
    "stage4j_review_decisions": Path("data/observations/review/stage4j-observation-review-decisions.yaml"),
}

ALLOWLISTED_STAGE4K_IDS = (
    "stage4b-rtkd-iddqd",
    "stage4b-scream314-cicada3301",
    "stage4b-complete-cicada-archive",
    "stage4b-uncovering-liber-primus",
    "stage4b-uncovering-lp-unsolved-pages",
    "stage4b-uncovering-lp-transliteration",
    "stage4b-uncovering-frequency-analysis",
    "stage4b-uncovering-instar-emergence",
    "stage4b-uncovering-what-happened-2014",
    "stage4b-uncovering-outguess",
    "stage4e-cicada-solvers-iddqd",
    "stage4f-iddqd-lp-outguessed-tree",
    "stage4f-iddqd-2016-4gq25-image",
    "stage4f-iddqd-2013-02-assets",
    "stage4f-complete-archive-magicsquares-openpuff-context",
    "stage4f-iddqd-interconnectedness-mp3",
    "stage4f-iddqd-761-mp3-instar",
    "stage4f-charleswyt-mp3stego-reference",
)

SNAPSHOT_POLICIES = (
    "metadata_only",
    "ignored_local_snapshot",
    "committed_small_text_snapshot",
    "commit_addressed_reference",
    "archive_reference_only",
    "deferred_manual_review",
    "rejected_unsafe_or_noisy",
)

LOCK_STATUSES = (
    "source_locked",
    "metadata_locked",
    "snapshot_cached_ignored",
    "commit_address_locked",
    "deferred_requires_manual_review",
    "rejected_unsafe",
    "duplicate_existing_lock",
    "fetch_failed",
)


@dataclass(frozen=True)
class SourceCandidate:
    """One normalized public source candidate."""

    candidate_id: str
    source_url: str
    source_family: str
    title: str
    source_path: str | None = None
    artifact_type: str | None = None
    source_basis: str | None = None
    payload: dict[str, Any] | None = None


@dataclass(frozen=True)
class FetchResult:
    """A network or metadata fetch outcome."""

    retrieval_status: str
    http_status: int | None = None
    content_type: str | None = None
    content_length: int | None = None
    content_sha256: str | None = None
    ignored_cache_path: str | None = None
    error: str | None = None
    fetched: bool = False


def common_policy_flags() -> dict[str, bool]:
    """Return Stage 4K no-raw/no-solve flags."""

    return {
        "raw_private_data_committed": False,
        "binary_committed": False,
        "image_committed": False,
        "audio_committed": False,
        "font_committed": False,
        "archive_committed": False,
        "solve_claim": False,
        "trusted_as_canonical": False,
    }
