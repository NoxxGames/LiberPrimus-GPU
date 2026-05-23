"""Local fixture extraction helpers for static HTML and image metadata."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from .export import repo_relative, resolve, write_json
from .hashing import hash_file
from .models import STAGE_ID


class StaticPageParser(HTMLParser):
    """Small deterministic HTML extractor for local/static pages."""

    def __init__(self) -> None:
        super().__init__()
        self.text_chunks: list[str] = []
        self.links: list[str] = []
        self.images: list[str] = []
        self.tables: list[str] = []
        self.code_blocks: list[str] = []
        self._skip_depth = 0
        self._capture_table = False
        self._capture_code = False
        self._table_chunks: list[str] = []
        self._code_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag in {"script", "style", "nav", "header", "footer"}:
            self._skip_depth += 1
        if tag == "a" and attributes.get("href"):
            self.links.append(attributes["href"] or "")
        if tag == "img" and attributes.get("src"):
            self.images.append(attributes["src"] or "")
        if tag == "table":
            self._capture_table = True
            self._table_chunks = []
        if tag in {"pre", "code"}:
            self._capture_code = True
            self._code_chunks = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "nav", "header", "footer"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "table" and self._capture_table:
            self.tables.append(" ".join(self._table_chunks).strip())
            self._capture_table = False
        if tag in {"pre", "code"} and self._capture_code:
            self.code_blocks.append(" ".join(self._code_chunks).strip())
            self._capture_code = False

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text or self._skip_depth:
            return
        self.text_chunks.append(text)
        if self._capture_table:
            self._table_chunks.append(text)
        if self._capture_code:
            self._code_chunks.append(text)


def extract_html_file(path: Path, *, source_id: str | None = None, out: Path | None = None) -> dict[str, Any]:
    """Extract readable text, links, images, tables, and code blocks from a local HTML file."""

    target = resolve(path)
    parser = StaticPageParser()
    parser.feed(target.read_text(encoding="utf-8"))
    record = {
        "record_type": "extracted_page_record",
        "schema": "schemas/source-harvester/extracted-page-record-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_id": source_id,
        "source_path": repo_relative(target),
        "main_text": "\n".join(parser.text_chunks),
        "links": sorted(set(parser.links)),
        "image_links": sorted(set(parser.images)),
        "tables": [table for table in parser.tables if table],
        "code_blocks": [block for block in parser.code_blocks if block],
        "extraction_warnings": [],
        "image_interpretation_performed": False,
        "raw_body_committed": False,
        "generated_outputs_committed": False,
        "solve_claim": False,
    }
    if out is not None:
        write_json(out, record)
    return record


def image_metadata(path: Path, *, source_id: str | None = None) -> dict[str, Any]:
    """Read deterministic local image metadata and hash only."""

    target = resolve(path)
    hash_record = hash_file(target, source_id=source_id)
    try:
        from PIL import Image

        with Image.open(target) as image:
            width, height = image.size
            mode = image.mode
            image_format = image.format
    except Exception as exc:  # pragma: no cover - exercised only if Pillow is absent/broken.
        width = height = None
        mode = image_format = None
        warning = str(exc)
    else:
        warning = None
    return {
        "record_type": "image_metadata_record",
        "stage_id": STAGE_ID,
        "source_id": source_id,
        "path": repo_relative(target),
        "file_name": target.name,
        "width": width,
        "height": height,
        "mode": mode,
        "format": image_format,
        "size_bytes": hash_record["size_bytes"],
        "sha256": hash_record["sha256"],
        "mime_guess": hash_record["mime_guess"],
        "metadata_warning": warning,
        "image_interpretation_performed": False,
        "raw_file_committed": False,
        "solve_claim": False,
    }
