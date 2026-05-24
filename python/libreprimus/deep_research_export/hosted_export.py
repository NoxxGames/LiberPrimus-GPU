"""Render Stage 5AN hosted private content library."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Any

from .hashing import dir_size_bytes, file_count, sha256_file
from .inputs import ensure_clean_dir, read_json, repo_relative, resolve, write_json, write_yaml
from .models import (
    HOSTED_CONTENT_ROOT,
    METADATA_SITE_ROOT,
    NOINDEX,
    PRIVATE_BANNER,
    PRIVATE_CONTENT_MANIFEST_URL,
    PRIVATE_CONTENT_URL,
    PRIVATE_NOTICE,
    STAGE_ID,
)


def build_hosted_export(
    *,
    content_pack_root: Path,
    metadata_site_root: Path = METADATA_SITE_ROOT,
    out_root: Path = HOSTED_CONTENT_ROOT,
    summary_out: Path,
    upload_instructions_out: Path,
    consumption_guide_out: Path,
) -> dict[str, Any]:
    """Build ignored private-content static library and committed summaries."""

    root = ensure_clean_dir(out_root)
    (root / "assets").mkdir(parents=True, exist_ok=True)
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "files").mkdir(parents=True, exist_ok=True)
    pack_root = resolve(content_pack_root)
    manifest = read_json(pack_root / "deep-research-content-pack-stage5an-manifest.json")
    included_files = [dict(record) for record in manifest.get("included_files", []) if isinstance(record, dict)]
    for record in included_files:
        rel = Path(record["relative_path"])
        source = pack_root / rel
        destination = root / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)

    _write_assets(root)
    _write_data(root, pack_root, manifest, included_files)
    _write_pages(root, manifest, included_files)
    _write_readme(root)
    (root / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    zip_path = _zip_dir(root, root.parent / "private-content.zip")
    summary = {
        "record_type": "stage5an_hosted_content_export_summary",
        "schema": "schemas/deep-research-export/hosted-content-export-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "hosted_content_export_generated": True,
        "hosted_content_export_root": repo_relative(root),
        "hosted_content_export_zip_created": zip_path.exists(),
        "hosted_content_export_zip_path": repo_relative(zip_path),
        "hosted_content_file_count": file_count(root),
        "hosted_content_size_bytes": dir_size_bytes(root),
        "metadata_site_root": repo_relative(metadata_site_root),
        "content_pack_manifest": repo_relative(pack_root / "deep-research-content-pack-stage5an-manifest.json"),
        "included_file_count": len(included_files),
        "robots_noindex_present": True,
        "raw_bodies_included": True,
        "private_ids_published": False,
        "local_absolute_paths_published": False,
        "public_website_publication_performed": False,
        "solve_claim": False,
    }
    upload = build_upload_instructions()
    guide = build_consumption_guide()
    write_yaml(summary_out, summary)
    write_yaml(upload_instructions_out, upload)
    write_yaml(consumption_guide_out, guide)
    return {"summary": summary, "upload_instructions": upload, "consumption_guide": guide}


def build_upload_instructions() -> dict[str, Any]:
    """Return committed upload instructions."""

    return {
        "record_type": "stage5an_upload_instructions",
        "schema": "schemas/deep-research-export/upload-instructions-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "sftp_upload_directory": "website-export/stage5an/webserver-root/",
        "copy_contents_to_webserver_root": True,
        "expected_urls": [
            "http://liberprimus-gpu-data.info/index.html",
            "http://liberprimus-gpu-data.info/private-content/index.html",
            PRIVATE_CONTENT_MANIFEST_URL,
        ],
        "optional_zip": "website-export/stage5an/webserver-root.zip",
        "do_not_upload": [
            "third_party/",
            "raw archives/workbooks/images/PDFs/audio/video",
            "codex-output/",
            "experiments/results/",
            "source-harvester-output/",
            "harvest-output/",
            "raw local source roots",
        ],
        "access_control_required_if_sensitive": True,
        "robots_noindex_not_security": True,
        "warning": "This is no longer metadata-only. Use webserver access control if sensitive.",
        "public_website_publication_performed": False,
        "solve_claim": False,
    }


def build_consumption_guide() -> dict[str, Any]:
    """Return the Deep Research consumption guide."""

    return {
        "record_type": "stage5an_deep_research_consumption_guide",
        "schema": "schemas/deep-research-export/deep-research-consumption-guide-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "metadata_site_url": "http://liberprimus-gpu-data.info/index.html",
        "private_content_url": PRIVATE_CONTENT_URL,
        "private_content_manifest_url": PRIVATE_CONTENT_MANIFEST_URL,
        "recommended_sftp_upload_root": "website-export/stage5an/webserver-root/",
        "content_pack_zip": "deep-research-content-packs/stage5an/deep-research-content-pack-stage5an.zip",
        "hosted_export_root": "website-export/stage5an/private-content",
        "combined_webserver_root": "website-export/stage5an/webserver-root",
        "what_to_attach_if_upload_limits_allow": [
            "deep-research-content-packs/stage5an/deep-research-content-pack-stage5an-manifest.yaml",
            "data/deep-research-export/stage5an-deep-research-consumption-guide.yaml",
        ],
        "what_to_host_if_upload_limits_exceeded": [
            "website-export/stage5an/webserver-root/",
            "website-export/stage5an/webserver-root/private-content/",
        ],
        "first_deep_research_prompt_should_reference": [
            "metadata site URL",
            "private content URL",
            "content-pack manifest URL",
            "publication gates",
        ],
        "deep_research_performed": False,
        "public_website_publication_performed": False,
        "solve_claim": False,
    }


def _write_assets(root: Path) -> None:
    (root / "assets/site.css").write_text(
        "body{font-family:Segoe UI,Arial,sans-serif;margin:2rem;line-height:1.45;color:#1d2329;background:#fbfbf8}"
        "a{color:#22577a}.banner{border:2px solid #842029;background:#f8d7da;padding:1rem;margin-bottom:1rem}"
        "table{border-collapse:collapse;width:100%}td,th{border:1px solid #c8c8c8;padding:.4rem;text-align:left}"
        "code{background:#eee;padding:.1rem .2rem}",
        encoding="utf-8",
    )
    (root / "assets/site.js").write_text(
        "document.querySelectorAll('[data-filter]').forEach(i=>i.addEventListener('input',()=>{"
        "const q=i.value.toLowerCase();document.querySelectorAll('[data-row]').forEach(r=>{"
        "r.hidden=!r.textContent.toLowerCase().includes(q);});}));\n",
        encoding="utf-8",
    )


def _write_data(root: Path, pack_root: Path, manifest: dict[str, Any], included_files: list[dict[str, Any]]) -> None:
    write_json(root / "data/content-pack-manifest.json", manifest)
    for source_name, dest_name in [
        ("source-cards.json", "source-cards.json"),
        ("content-index.json", "content-index.json"),
        ("claim-index.json", "claim-index.json"),
        ("publication-gates.json", "publication-gates.json"),
    ]:
        source = pack_root / "metadata" / source_name
        write_json(root / "data" / dest_name, read_json(source))
    write_json(root / "data/file-index.json", {"record_type": "stage5an_file_index", "records": included_files})


def _write_pages(root: Path, manifest: dict[str, Any], included_files: list[dict[str, Any]]) -> None:
    nav = "<p><a href='./index.html'>Home</a> | <a href='files/index.html'>Files</a> | <a href='deep-research/index.html'>Deep Research</a></p>"
    file_rows = "\n".join(
        "<tr data-row><td><a href='../{url}'>{file_id}</a></td><td>{kind}</td><td>{status}</td><td><code>{sha}</code></td></tr>".format(
            url=record["relative_url"],
            file_id=record["file_id"],
            kind=record.get("content_kind", ""),
            status=record.get("publication_status", ""),
            sha=record.get("sha256", ""),
        )
        for record in included_files
    )
    index_body = [
        "<h1>Private Content Library</h1>",
        f"<p>Files: {len(included_files)}. Manifest: <a href='data/content-pack-manifest.json'>content-pack-manifest.json</a>.</p>",
        "<p><a href='files/index.html'>Browse included files</a></p>",
    ]
    _html(root / "index.html", "Private Content Library", nav + "\n".join(index_body))
    _html(root / "files/index.html", "Included Files", "<input data-filter placeholder='Filter files'>" f"<table><tr><th>File</th><th>Kind</th><th>Status</th><th>SHA-256</th></tr>{file_rows}</table>")
    _html(root / "bundles/index.html", "Bundles", _simple_list(manifest, "included_bundle_count"))
    _html(root / "sources/index.html", "Sources", _simple_list(manifest, "included_source_count"))
    _html(root / "claims/index.html", "Claims", _simple_list(manifest, "included_claim_count"))
    _html(
        root / "deep-research/index.html",
        "Deep Research",
        "<p>Use the metadata site, private content root, content manifest, and publication gates together.</p>"
        "<p>This stage did not run Deep Research.</p>",
    )


def _html(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "<!doctype html>",
                "<html lang='en'>",
                "<head>",
                "<meta charset='utf-8'>",
                NOINDEX,
                f"<title>{title}</title>",
                "<link rel='stylesheet' href='/private-content/assets/site.css'>",
                "</head>",
                "<body>",
                f"<div class='banner'><strong>{PRIVATE_BANNER}</strong><br>{PRIVATE_NOTICE}</div>",
                body,
                "<script src='/private-content/assets/site.js'></script>",
                "</body></html>",
            ]
        ),
        encoding="utf-8",
    )


def _simple_list(manifest: dict[str, Any], key: str) -> str:
    return f"<p>{key}: {manifest.get(key, 0)}</p>"


def _write_readme(root: Path) -> None:
    (root / "README.md").write_text(
        "# Stage 5AN Private Content\n\nReview-gated private content library. robots.txt/noindex are not security.\n",
        encoding="utf-8",
    )


def _zip_dir(root: Path, zip_path: Path) -> Path:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(root).as_posix())
    # Touch the digest during build to catch filesystem races.
    sha256_file(zip_path)
    return zip_path
