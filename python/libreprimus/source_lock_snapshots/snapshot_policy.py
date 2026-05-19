"""Snapshot policy classification for Stage 4K sources."""

from __future__ import annotations

from urllib.parse import urlparse

BINARY_EXTENSIONS = {
    ".bin",
    ".dat",
    ".exe",
    ".iso",
}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".tif", ".tiff"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
FONT_EXTENSIONS = {".ttf", ".otf", ".woff", ".woff2"}
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".gz", ".tgz", ".7z", ".rar"}
PDF_EXTENSIONS = {".pdf"}
TEXT_EXTENSIONS = {".txt", ".md", ".rst", ".csv", ".json", ".yaml", ".yml"}


def classify_source_class(url: str, artifact_type: str | None = None) -> str:
    """Map URL and source metadata to a compact source class."""

    host = urlparse(url).netloc.lower()
    path = urlparse(url).path
    artifact = (artifact_type or "").lower()
    if "github.com" in host:
        if "/tree/" in path:
            return "github_tree"
        if "/blob/" in path:
            return "github_blob"
        return "github_repository"
    if "uncovering-cicada.fandom.com" in host:
        return "uncovering_cicada_page"
    if "archive.org" in host or "web.archive.org" in host:
        return "archive_reference"
    if "tool" in artifact or "outguess" in artifact or "mp3stego" in artifact:
        return "tool_reference"
    if "fixture" in artifact or "image" in artifact or "audio" in artifact or "font" in artifact:
        return "artifact_metadata"
    return "historical_reference"


def file_extension(url: str) -> str:
    """Return lowercase file extension from URL path."""

    path = urlparse(url).path.lower()
    name = path.rsplit("/", maxsplit=1)[-1]
    if "." not in name:
        return ""
    return "." + name.rsplit(".", maxsplit=1)[-1]


def artifact_kind(url: str, artifact_type: str | None = None) -> str:
    """Return broad content kind for policy decisions."""

    ext = file_extension(url)
    artifact = (artifact_type or "").lower()
    if ext in FONT_EXTENSIONS or "font" in artifact:
        return "font"
    if ext in IMAGE_EXTENSIONS or "image" in artifact:
        return "image"
    if ext in AUDIO_EXTENSIONS or "audio" in artifact or "mp3" in artifact:
        return "audio"
    if ext in ARCHIVE_EXTENSIONS or ext in PDF_EXTENSIONS:
        return "archive"
    if ext in BINARY_EXTENSIONS:
        return "binary"
    if ext in TEXT_EXTENSIONS:
        return "text"
    return "page_or_repo"


def choose_snapshot_policy(url: str, source_class: str, artifact_type: str | None = None) -> str:
    """Choose the default Stage 4K snapshot policy."""

    kind = artifact_kind(url, artifact_type)
    if kind == "font":
        return "metadata_only"
    if kind in {"binary", "image", "audio", "archive"}:
        return "metadata_only"
    if source_class in {"github_repository", "github_tree", "github_blob"}:
        return "commit_addressed_reference"
    if source_class == "archive_reference":
        return "archive_reference_only"
    if source_class == "uncovering_cicada_page":
        return "ignored_local_snapshot"
    if kind == "text":
        return "ignored_local_snapshot"
    return "metadata_only"


def committed_snapshot_allowed(url: str, policy: str, artifact_type: str | None = None) -> bool:
    """Return true only for safe small text snapshot policy."""

    return policy == "committed_small_text_snapshot" and artifact_kind(url, artifact_type) == "text"
