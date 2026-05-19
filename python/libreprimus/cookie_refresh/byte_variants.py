"""Manifest-declared byte variants for Stage 4G cookie refresh."""

from __future__ import annotations

from pathlib import PurePosixPath
from urllib.parse import quote


def apply_byte_variant(text: str, variant: str) -> str:
    """Apply one declared variant to a source-backed string."""

    if variant == "raw":
        return text
    if variant == "lower":
        return text.lower()
    if variant == "upper":
        return text.upper()
    if variant == "trailing_lf":
        return f"{text}\n"
    if variant == "trailing_crlf":
        return f"{text}\r\n"
    if variant == "compact_no_spaces":
        return "".join(text.split())
    if variant == "compact_lower":
        return "".join(text.split()).lower()
    if variant == "compact_upper":
        return "".join(text.split()).upper()
    if variant == "quoted":
        return f'"{text}"'
    if variant == "url_encoded":
        return quote(text, safe="")
    if variant == "filename_only":
        return PurePosixPath(text.replace("\\", "/")).name
    if variant == "basename_no_extension":
        path = PurePosixPath(text.replace("\\", "/"))
        return path.stem
    if variant == "slash_wrapped":
        return f"/{text.strip('/')}/"
    if variant == "tmp_path_variant":
        cleaned = text.replace("\\", "/")
        return f"/tmp/{PurePosixPath(cleaned).name}"
    if variant == "leading_space":
        return f" {text}"
    if variant == "trailing_space":
        return f"{text} "
    if variant == "wrapped_space":
        return f" {text} "
    raise ValueError(f"unsupported byte variant: {variant}")
