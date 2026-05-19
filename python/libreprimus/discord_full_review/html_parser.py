"""Streaming Discord HTML parser for Stage 4A."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
import re
from typing import Any

from libreprimus.discord_full_review.export import display_path, sha256_file, sha256_text
from libreprimus.discord_full_review.models import (
    DEBUNK_KEYWORDS,
    HTML_SUFFIXES,
    IMAGE_SUFFIXES,
    METHOD_KEYWORDS,
    VISUAL_KEYWORDS,
)
from libreprimus.discord_full_review.redaction import public_links_from_text, redact_text, sanitize_url


@dataclass
class ParsedMessage:
    text_parts: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    timestamp: str | None = None
    ordinal: int = 0


class DiscordFullReviewParser(HTMLParser):
    """Best-effort Discord HTML parser that never stores raw author identity fields."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.messages: list[ParsedMessage] = []
        self._current: ParsedMessage | None = None
        self._message_depth = 0
        self._skip_text_depth = 0
        self._timestamp_depth = 0
        self._ordinal = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key.lower(): value or "" for key, value in attrs}
        classes = set(attr.get("class", "").split())
        if tag.lower() in {"div", "li"} and "chatlog__message" in classes:
            self._start_message(attr)
        if self._current is not None:
            self._message_depth += 1
            if _is_identity_class(classes):
                self._skip_text_depth += 1
            if "chatlog__timestamp" in classes or "timestamp" in " ".join(classes).lower():
                self._timestamp_depth += 1
                title = attr.get("title")
                if title and not self._current.timestamp:
                    self._current.timestamp = redact_text(title)
            if not _is_identity_class(classes):
                for key in ("href", "src"):
                    value = attr.get(key)
                    if value and not _is_avatar_reference(value):
                        self._current.links.append(value)
                        if _is_image_reference(value):
                            self._current.images.append(value)

    def handle_endtag(self, tag: str) -> None:
        if self._current is None:
            return
        if self._skip_text_depth > 0:
            self._skip_text_depth -= 1
        if self._timestamp_depth > 0:
            self._timestamp_depth -= 1
        self._message_depth -= 1
        if self._message_depth <= 0:
            self._finish_message()

    def handle_data(self, data: str) -> None:
        if self._current is None:
            return
        text = " ".join(data.split())
        if not text:
            return
        if self._timestamp_depth and not self._current.timestamp:
            self._current.timestamp = redact_text(text)
            return
        if self._skip_text_depth:
            return
        self._current.text_parts.append(text)

    def close(self) -> None:
        super().close()
        if self._current is not None:
            self._finish_message()

    def _start_message(self, attrs: dict[str, str]) -> None:
        if self._current is not None:
            self._finish_message()
        self._ordinal += 1
        self._current = ParsedMessage(ordinal=self._ordinal)
        self._message_depth = 0
        self._skip_text_depth = 0
        self._timestamp_depth = 0
        title = attrs.get("title") or attrs.get("aria-label")
        if title:
            self._current.timestamp = redact_text(title)

    def _finish_message(self) -> None:
        if self._current is not None and (self._current.text_parts or self._current.links):
            self.messages.append(self._current)
        self._current = None
        self._message_depth = 0
        self._skip_text_depth = 0
        self._timestamp_depth = 0


def parse_discord_html_file(path: Path, *, channel_id: str, channel_name: str) -> list[dict[str, Any]]:
    parser = DiscordFullReviewParser()
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        while chunk := handle.read(1_048_576):
            parser.feed(chunk)
    parser.close()
    if not parser.messages:
        parser.messages = _fallback_messages(path)
    return [_message_record(message, channel_id=channel_id, channel_name=channel_name) for message in parser.messages]


def discover_html_files(source_dir: Path) -> list[Path]:
    if not source_dir.is_dir():
        return []
    return sorted(path for path in source_dir.rglob("*") if path.is_file() and path.suffix.lower() in HTML_SUFFIXES)


def channel_name_from_path(path: Path) -> str:
    name = re.sub(r"\s*\[[0-9]{8,24}\]\s*$", "", path.stem)
    parts = [part.strip() for part in name.split(" - ") if part.strip()]
    return parts[-1] if parts else name


def channel_slug(name: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return slug or "channel"


def channel_id_for_file(path: Path) -> str:
    return f"ch-{sha256_text(path.name)[:16]}"


def channel_source_record(path: Path, *, source_dir: Path, part_count: int, messages: list[dict[str, Any]]) -> dict[str, Any]:
    public_link_count = sum(len(record.get("public_links", [])) for record in messages)
    image_count = sum(len(record.get("image_refs", [])) for record in messages)
    method_count = sum(1 for record in messages if record.get("method_keywords"))
    numeric_count = sum(1 for record in messages if record.get("numeric_values"))
    visual_count = sum(1 for record in messages if record.get("visual_keywords"))
    debunk_count = sum(1 for record in messages if record.get("debunk_keywords"))
    channel_name = channel_name_from_path(path)
    slug = channel_slug(channel_name)
    return {
        "record_type": "discord_full_review_channel_record",
        "channel_id": channel_id_for_file(path),
        "channel_name": channel_name,
        "channel_slug": slug,
        "source_file_relative_path": display_path(path),
        "source_dir_relative_path": display_path(source_dir),
        "source_file_sha256": sha256_file(path),
        "file_size_bytes": path.stat().st_size,
        "estimated_message_count": len(messages),
        "part_count": part_count,
        "public_link_count": public_link_count,
        "image_reference_count": image_count,
        "method_claim_count": method_count,
        "numeric_claim_count": numeric_count,
        "visual_claim_count": visual_count,
        "debunk_count": debunk_count,
        "site_index_relative_path": f"site/channels/{slug}/index.html",
        "raw_message_committed": False,
        "username_committed": False,
        "user_id_committed": False,
        "message_id_committed": False,
        "private_url_committed": False,
        "solve_claim": False,
    }


def _message_record(message: ParsedMessage, *, channel_id: str, channel_name: str) -> dict[str, Any]:
    raw_text = " ".join(message.text_parts)
    redacted = redact_text(raw_text)
    public_links = _dedupe(public_links_from_text(raw_text) + [_safe for link in message.links if (_safe := sanitize_url(link)[0])])
    image_refs = [_image_ref(link, channel_id=channel_id, ordinal=index) for index, link in enumerate(message.images, start=1)]
    attachment_refs = [
        _attachment_ref(link, channel_id=channel_id, ordinal=index)
        for index, link in enumerate(message.links, start=1)
        if link not in message.images
        and not sanitize_url(link)[0]
        and (Path(link.split("?", 1)[0]).suffix.lower() or "discord" in link.lower())
    ]
    numbers = sorted({int(value) for value in re.findall(r"\b\d{1,12}\b", redacted)})
    lowered = redacted.lower()
    method_keywords = sorted({keyword for keyword in METHOD_KEYWORDS if keyword in lowered})
    visual_keywords = sorted({keyword for keyword in VISUAL_KEYWORDS if keyword in lowered})
    debunk_keywords = sorted({keyword for keyword in DEBUNK_KEYWORDS if keyword in lowered})
    message_ref = f"msg-{sha256_text(channel_id + ':' + str(message.ordinal) + ':' + redacted)[:24]}"
    for ref in image_refs + attachment_refs:
        ref["message_ref"] = message_ref
    return {
        "record_type": "discord_full_review_message_record",
        "message_ref": message_ref,
        "channel_id": channel_id,
        "channel_name": channel_name,
        "approximate_timestamp": message.timestamp,
        "redacted_text": redacted,
        "signal_class": "low_signal" if not (public_links or method_keywords or numbers or visual_keywords) else "review_signal",
        "public_links": public_links,
        "image_refs": image_refs,
        "attachment_refs": attachment_refs,
        "method_keywords": method_keywords,
        "numeric_values": numbers[:100],
        "visual_keywords": visual_keywords,
        "debunk_keywords": debunk_keywords,
        "raw_message_committed": False,
        "username_committed": False,
        "user_id_committed": False,
        "message_id_committed": False,
        "private_url_committed": False,
        "solve_claim": False,
    }


def _fallback_messages(path: Path) -> list[ParsedMessage]:
    collector = _TextCollector()
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        while chunk := handle.read(1_048_576):
            collector.feed(chunk)
    collector.close()
    text = " ".join(collector.parts)
    messages: list[ParsedMessage] = []
    for ordinal, start in enumerate(range(0, len(text), 1600), start=1):
        part = text[start : start + 1600].strip()
        if part:
            messages.append(ParsedMessage(text_parts=[part], links=re.findall(r"https?://\S+", part), ordinal=ordinal))
    return messages


class _TextCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if text:
            self.parts.append(text)


def _is_identity_class(classes: set[str]) -> bool:
    joined = " ".join(classes).lower()
    return "author" in joined or "avatar" in joined or "username" in joined


def _is_image_reference(value: str) -> bool:
    parsed = value.split("?", 1)[0].lower()
    return Path(parsed).suffix.lower() in IMAGE_SUFFIXES


def _is_avatar_reference(value: str) -> bool:
    lowered = value.lower()
    return "/avatars/" in lowered or "/embed/avatars/" in lowered


def _image_ref(url: str, *, channel_id: str, ordinal: int) -> dict[str, Any]:
    public, redacted = sanitize_url(url)
    file_name = Path(url.split("?", 1)[0]).name or "image"
    extension = Path(file_name).suffix.lower().lstrip(".")
    return {
        "record_type": "discord_image_reference",
        "image_reference_id": f"img-{sha256_text(channel_id + ':' + url + ':' + str(ordinal))[:18]}",
        "message_ref": "",
        "channel_id": channel_id,
        "file_name": file_name,
        "extension": extension,
        "media_kind": "image",
        "url_public": public,
        "url_redacted": redacted,
        "private_url_committed": False,
        "raw_message_committed": False,
        "username_committed": False,
        "solve_claim": False,
        "usable_as_experiment_seed": False,
    }


def _attachment_ref(url: str, *, channel_id: str, ordinal: int) -> dict[str, Any]:
    _, redacted = sanitize_url(url)
    file_name = Path(url.split("?", 1)[0]).name or "attachment"
    return {
        "record_type": "discord_attachment_reference",
        "attachment_reference_id": f"att-{sha256_text(channel_id + ':' + url + ':' + str(ordinal))[:18]}",
        "message_ref": "",
        "channel_id": channel_id,
        "file_name": file_name,
        "extension": Path(file_name).suffix.lower().lstrip("."),
        "url_redacted": redacted,
        "private_url_committed": False,
        "raw_message_committed": False,
        "username_committed": False,
        "solve_claim": False,
    }


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value not in seen:
            output.append(value)
            seen.add(value)
    return output


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
