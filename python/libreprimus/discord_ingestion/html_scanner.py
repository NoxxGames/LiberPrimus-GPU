"""Privacy-preserving local Discord HTML archive scanner for Stage 3N."""

from __future__ import annotations

from collections import Counter
from datetime import UTC, datetime
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import re
from typing import Any

from libreprimus.discord_ingestion.attachment_extractor import attachment_candidates_from_links
from libreprimus.discord_ingestion.claim_extractor import extract_claim_candidates
from libreprimus.discord_ingestion.export import write_json, write_jsonl
from libreprimus.discord_ingestion.link_extractor import extract_plaintext_urls, link_record
from libreprimus.discord_ingestion.models import (
    ARCHIVE_ID,
    FAILURE_KEYWORDS,
    KNOWN_NUMBERS,
    METHOD_KEYWORDS,
    SOURCE_KEYWORDS,
)
from libreprimus.discord_ingestion.numeric_extractor import extract_numeric_candidates
from libreprimus.paths import repo_root

HTML_SUFFIXES = {".html", ".htm"}
HASH_LIKE_RE = re.compile(r"\b[0-9a-fA-F]{32,128}\b")
MAX_INTERESTING_FRAGMENTS_PER_FILE = 20_000


class DiscordArchiveParser(HTMLParser):
    """Small HTML parser that keeps URLs and review keywords, not raw bodies."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.urls: list[str] = []
        self.interesting_fragments: list[str] = []
        self.hash_like_count = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name.lower() in {"href", "src"} and value:
                self.urls.append(value)

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text:
            return
        self.urls.extend(extract_plaintext_urls(text))
        self.hash_like_count += len(HASH_LIKE_RE.findall(text))
        if len(self.interesting_fragments) >= MAX_INTERESTING_FRAGMENTS_PER_FILE:
            return
        if _interesting_text(text):
            self.interesting_fragments.append(text[:4000])


def scan_discord_archive(
    *,
    source_dir: Path,
    out_dir: Path,
    allow_missing: bool = False,
    allow_warnings: bool = False,
) -> dict[str, Any]:
    """Scan a local Discord HTML export and write ignored review outputs."""
    resolved_source = _resolve(source_dir)
    resolved_out = _resolve(out_dir)
    warnings: list[str] = []
    html_paths: list[Path] = []
    if resolved_source.is_dir():
        html_paths = sorted(
            path
            for path in resolved_source.rglob("*")
            if path.is_file() and path.suffix.lower() in HTML_SUFFIXES
        )
    elif allow_missing:
        warnings.append("source_dir_missing_scan_skipped")
    else:
        raise FileNotFoundError(resolved_source)

    file_locks: list[dict[str, Any]] = []
    link_records: list[dict[str, Any]] = []
    method_claims: list[dict[str, Any]] = []
    numeric_candidates: list[dict[str, Any]] = []
    seen_links: set[tuple[str, str]] = set()
    hash_like_count = 0

    for html_path in html_paths:
        file_lock, parser = _scan_one_file(html_path, resolved_source)
        file_locks.append(file_lock)
        source_sha = str(file_lock["sha256"])
        hash_like_count += parser.hash_like_count

        file_link_count = 0
        for raw_url in parser.urls:
            candidate = link_record(
                raw_url,
                source_file_sha256=source_sha,
                ordinal=len(link_records) + 1,
            )
            dedupe_key = (source_sha, str(candidate["normalized_url"]))
            if dedupe_key in seen_links:
                continue
            seen_links.add(dedupe_key)
            link_records.append(candidate)
            file_link_count += 1

        for fragment in parser.interesting_fragments:
            method_claims.extend(
                extract_claim_candidates(
                    fragment,
                    source_file_sha256=source_sha,
                    ordinal=len(method_claims) + 1,
                )
            )
            numeric_candidates.extend(
                extract_numeric_candidates(
                    fragment,
                    source_file_sha256=source_sha,
                    ordinal=len(numeric_candidates) + 1,
                )
            )

        if len(parser.interesting_fragments) >= MAX_INTERESTING_FRAGMENTS_PER_FILE:
            warnings.append(f"{file_lock['relative_path']}: interesting_fragment_limit_reached")
        if file_link_count == 0 and parser.hash_like_count == 0 and not parser.interesting_fragments:
            warnings.append(f"{file_lock['relative_path']}: no_source_discovery_candidates_found")

    attachment_candidates = attachment_candidates_from_links(link_records)
    source_candidates = _build_source_candidates(link_records)
    summary = _build_summary(
        source_dir=resolved_source,
        out_dir=resolved_out,
        file_locks=file_locks,
        link_records=link_records,
        attachment_candidates=attachment_candidates,
        method_claims=method_claims,
        numeric_candidates=numeric_candidates,
        source_candidates=source_candidates,
        hash_like_count=hash_like_count,
        warnings=warnings,
    )
    resolved_out.mkdir(parents=True, exist_ok=True)
    write_jsonl(resolved_out / "discord_html_file_locks.jsonl", file_locks)
    write_jsonl(resolved_out / "discord_extracted_links.jsonl", link_records)
    write_jsonl(resolved_out / "discord_attachment_candidates.jsonl", attachment_candidates)
    write_jsonl(resolved_out / "discord_method_claim_candidates.jsonl", method_claims)
    write_jsonl(resolved_out / "discord_numeric_observation_candidates.jsonl", numeric_candidates)
    write_jsonl(resolved_out / "discord_source_candidates.jsonl", source_candidates)
    write_jsonl(resolved_out / "warnings.jsonl", [{"warning": warning} for warning in warnings])
    write_json(resolved_out / "discord_ingestion_summary.json", summary)
    _write_review_index(resolved_out / "local_review_index.html", summary, source_candidates)

    if warnings and not allow_warnings:
        raise RuntimeError("; ".join(warnings))
    return summary


def _scan_one_file(html_path: Path, source_dir: Path) -> tuple[dict[str, Any], DiscordArchiveParser]:
    parser = DiscordArchiveParser()
    with html_path.open("r", encoding="utf-8", errors="replace") as handle:
        while chunk := handle.read(1_048_576):
            parser.feed(chunk)
    parser.close()
    sha256 = _sha256_file(html_path)
    relative_path = _relative_to_repo(html_path)
    return (
        {
            "record_type": "discord_html_file_lock",
            "archive_id": ARCHIVE_ID,
            "relative_path": relative_path,
            "file_name": html_path.name,
            "file_size_bytes": html_path.stat().st_size,
            "sha256": sha256,
            "estimated_message_count": _estimate_message_count(html_path),
            "extracted_at_utc": _utc_now(),
            "raw_content_committed": False,
            "notes": f"Local file under {source_dir.name}; raw Discord HTML remains ignored.",
        },
        parser,
    )


def _estimate_message_count(path: Path) -> int | None:
    patterns = [b"chatlog__message", b"data-message-id", b"class=\"message", b"class='message"]
    counts = Counter({pattern: 0 for pattern in patterns})
    with path.open("rb") as handle:
        while chunk := handle.read(1_048_576):
            for pattern in patterns:
                counts[pattern] += chunk.count(pattern)
    best = max(counts.values(), default=0)
    return best or None


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1_048_576), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _interesting_text(text: str) -> bool:
    lowered = text.lower()
    if any(keyword in lowered for keyword in METHOD_KEYWORDS | FAILURE_KEYWORDS | SOURCE_KEYWORDS):
        return True
    if any(str(number) in lowered for number in KNOWN_NUMBERS):
        return True
    return bool(HASH_LIKE_RE.search(text))


def _build_source_candidates(link_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: Counter[tuple[str, str, str]] = Counter()
    for record in link_records:
        url_kind = str(record["url_kind"])
        if url_kind == "discord_attachment":
            continue
        counts[(str(record["normalized_url"]), str(record["domain"]), url_kind)] += 1
    candidates: list[dict[str, Any]] = []
    for index, ((normalized_url, domain, url_kind), count) in enumerate(sorted(counts.items()), start=1):
        candidates.append(
            {
                "record_type": "discord_source_candidate",
                "source_candidate_id": f"discord-source-candidate-{index:06d}",
                "archive_id": ARCHIVE_ID,
                "normalized_url": normalized_url,
                "domain": domain,
                "url_kind": url_kind,
                "link_count": count,
                "message_body_committed": False,
                "usernames_committed": False,
                "review_status": "unreviewed",
                "notes": "Generated local review candidate; Discord claim is not canonical evidence.",
            }
        )
    return candidates


def _build_summary(
    *,
    source_dir: Path,
    out_dir: Path,
    file_locks: list[dict[str, Any]],
    link_records: list[dict[str, Any]],
    attachment_candidates: list[dict[str, Any]],
    method_claims: list[dict[str, Any]],
    numeric_candidates: list[dict[str, Any]],
    source_candidates: list[dict[str, Any]],
    hash_like_count: int,
    warnings: list[str],
) -> dict[str, Any]:
    domain_counts = Counter(str(record["domain"]) for record in link_records)
    url_kind_counts = Counter(str(record["url_kind"]) for record in link_records)
    known_bogus_count = sum(
        1
        for record in method_claims
        if record.get("claim_type") in {"false_positive_warning", "tried_and_failed"}
    )
    output_paths = {
        "file_locks": _relative_to_repo(out_dir / "discord_html_file_locks.jsonl"),
        "links": _relative_to_repo(out_dir / "discord_extracted_links.jsonl"),
        "attachments": _relative_to_repo(out_dir / "discord_attachment_candidates.jsonl"),
        "method_claims": _relative_to_repo(out_dir / "discord_method_claim_candidates.jsonl"),
        "numeric_observations": _relative_to_repo(
            out_dir / "discord_numeric_observation_candidates.jsonl"
        ),
        "source_candidates": _relative_to_repo(out_dir / "discord_source_candidates.jsonl"),
        "summary": _relative_to_repo(out_dir / "discord_ingestion_summary.json"),
        "local_review_index": _relative_to_repo(out_dir / "local_review_index.html"),
        "warnings": _relative_to_repo(out_dir / "warnings.jsonl"),
    }
    return {
        "record_type": "discord_ingestion_summary",
        "archive_id": ARCHIVE_ID,
        "generated_at_utc": _utc_now(),
        "source_dir": _relative_to_repo(source_dir),
        "html_file_count": len(file_locks),
        "total_bytes": sum(int(record["file_size_bytes"]) for record in file_locks),
        "link_count": len(link_records),
        "unique_domain_count": len(domain_counts),
        "attachment_candidate_count": len(attachment_candidates),
        "method_claim_candidate_count": len(method_claims),
        "numeric_observation_candidate_count": len(numeric_candidates),
        "known_bogus_or_debunked_claim_candidate_count": known_bogus_count,
        "source_candidate_count": len(source_candidates),
        "hash_like_candidate_count": hash_like_count,
        "warning_count": len(warnings),
        "domain_counts": dict(sorted(domain_counts.items())),
        "url_kind_counts": dict(sorted(url_kind_counts.items())),
        "raw_logs_committed": False,
        "message_bodies_committed": False,
        "usernames_committed": False,
        "ai_upload_used": False,
        "live_api_used": False,
        "scrape_used": False,
        "output_paths": output_paths,
        "warnings": warnings,
        "notes": "Admin-provided Discord HTML scanned locally for reviewable source discovery only.",
    }


def _write_review_index(
    path: Path,
    summary: dict[str, Any],
    source_candidates: list[dict[str, Any]],
) -> Path:
    rows = "\n".join(
        "<tr>"
        f"<td>{candidate['url_kind']}</td>"
        f"<td>{candidate['domain']}</td>"
        f"<td>{candidate['link_count']}</td>"
        f"<td><a href=\"{candidate['normalized_url']}\">public link</a></td>"
        "</tr>"
        for candidate in source_candidates[:500]
    )
    html = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Stage 3N Discord Source Review</title></head>
<body>
<h1>Stage 3N Discord Source Review</h1>
<p>Generated local review aid. No message bodies, usernames, or raw logs are included.</p>
<dl>
<dt>HTML files</dt><dd>{summary['html_file_count']}</dd>
<dt>Links</dt><dd>{summary['link_count']}</dd>
<dt>Unique domains</dt><dd>{summary['unique_domain_count']}</dd>
<dt>Method claim candidates</dt><dd>{summary['method_claim_candidate_count']}</dd>
<dt>Numeric observation candidates</dt><dd>{summary['numeric_observation_candidate_count']}</dd>
</dl>
<table>
<thead><tr><th>Kind</th><th>Domain</th><th>Count</th><th>Link</th></tr></thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>
"""
    path.write_text(html, encoding="utf-8", newline="\n")
    return path


def _utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _resolve(path: Path) -> Path:
    return path if path.is_absolute() else repo_root() / path


def _relative_to_repo(path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root()).as_posix()
    except ValueError:
        return path.as_posix()
