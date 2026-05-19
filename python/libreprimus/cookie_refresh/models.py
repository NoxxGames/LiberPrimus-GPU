"""Models and defaults for Stage 4G cookie refresh."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


EXPERIMENT_ID = "exp_stage4b_cookie_pack_v2"
DEFAULT_MANIFEST = Path("experiments/manifests/stage4b-disabled/exp_stage4b_cookie_pack_v2.yaml")
DEFAULT_CANDIDATE_SOURCES = Path("data/observations/web/stage4b-cookie-candidate-source-records.yaml")
DEFAULT_COOKIE_TARGETS = Path("data/observations/web/cookie-hash-records-v0.yaml")
DEFAULT_OUTPUT_DIR = Path("experiments/results/cookie-refresh/stage4g")
DEFAULT_SUMMARY = Path("data/observations/web/stage4g-cookie-refresh-summary.yaml")
DEFAULT_STAGE3U_MANIFEST = Path("experiments/manifests/post-discord/EXP-3R-001-cookie-sha256-signed-variants-a.yaml")
DEFAULT_STAGE3L_PACK_DIR = Path("data/observations/web/hash-preimage-candidate-packs")

SUPPORTED_ALGORITHMS = {"sha256", "sha1", "sha512", "md5"}
DEFAULT_ALGORITHMS = ("sha256",)

SUPPORTED_BYTE_VARIANTS = {
    "raw",
    "lower",
    "upper",
    "trailing_lf",
    "trailing_crlf",
    "compact_no_spaces",
    "compact_lower",
    "compact_upper",
    "quoted",
    "url_encoded",
    "filename_only",
    "basename_no_extension",
    "slash_wrapped",
    "tmp_path_variant",
    "leading_space",
    "trailing_space",
    "wrapped_space",
}
DEFAULT_BYTE_VARIANTS = ("raw",)


@dataclass(frozen=True)
class CookieRefreshManifest:
    """Validated Stage 4G execution view over the Stage 4B disabled manifest."""

    manifest_id: str
    candidate_count_upper_bound: int
    source_basis: tuple[str, ...]
    byte_variants: tuple[str, ...]
    algorithms: tuple[str, ...]
    payload: dict


@dataclass(frozen=True)
class CandidateBaseString:
    """Source-backed base string before byte-variant expansion."""

    base_string_id: str
    source_record_id: str
    source_basis: str
    text: str


@dataclass(frozen=True)
class ExpandedCookieCandidate:
    """Deduplicated byte candidate for exact digest comparison."""

    candidate_id: str
    base_string_id: str
    source_record_id: str
    source_basis: str
    raw_string_redacted_if_needed: str
    byte_variant: str
    encoding: str
    candidate_text: str
    candidate_bytes: bytes
    candidate_bytes_sha256: str
    previous_pack_duplicate: bool = False
