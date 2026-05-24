"""Build the Stage 5AN combined SFTP-ready webroot."""

from __future__ import annotations

import shutil
import zipfile
from pathlib import Path
from typing import Any

from libreprimus.website_render.loader import load_stage5al_inputs
from libreprimus.website_render.renderer import render_site

from .hashing import dir_size_bytes, file_count, sha256_file
from .inputs import ensure_clean_dir, repo_relative, resolve, write_yaml
from .models import COMBINED_WEBROOT, METADATA_SITE_ROOT, NOINDEX, PRIVATE_CONTENT_URL, STAGE_ID


def build_combined_webroot(
    *,
    metadata_site_root: Path = METADATA_SITE_ROOT,
    private_content_root: Path,
    out_root: Path = COMBINED_WEBROOT,
    summary_out: Path,
) -> dict[str, Any]:
    """Build the ignored SFTP-ready webroot."""

    root = ensure_clean_dir(out_root)
    metadata_root = resolve(metadata_site_root)
    if (metadata_root / "index.html").exists():
        _copy_tree_contents(metadata_root, root)
    else:
        inputs = load_stage5al_inputs(Path("data/website-ingest/stage5al"), Path("data/source-harvester/stage5al-summary.yaml"))
        render_site(inputs, root)
    private_target = root / "private-content"
    shutil.copytree(resolve(private_content_root), private_target, dirs_exist_ok=True)
    _inject_private_content_banner(root / "index.html")
    (root / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (root / "README.md").write_text(
        "\n".join(
            [
                "# Stage 5AN SFTP Webroot",
                "",
                "Copy the CONTENTS of this folder to the webserver root.",
                "Expected URLs:",
                "- http://liberprimus-gpu-data.info/index.html",
                "- http://liberprimus-gpu-data.info/private-content/index.html",
                "- http://liberprimus-gpu-data.info/private-content/data/content-pack-manifest.json",
                "",
                "This contains private/review-gated generated extracts. Use webserver access control if sensitive.",
                "robots.txt/noindex are not security.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    zip_path = _zip_dir(root, root.parent / "webserver-root.zip")
    summary = {
        "record_type": "stage5an_combined_webroot_summary",
        "schema": "schemas/deep-research-export/combined-webroot-summary-v0.schema.json",
        "stage_id": STAGE_ID,
        "source_stage_id": "stage-5am",
        "combined_webroot_generated": True,
        "combined_webroot_root": repo_relative(root),
        "combined_webroot_zip_created": zip_path.exists(),
        "combined_webroot_zip_path": repo_relative(zip_path),
        "combined_webroot_file_count": file_count(root),
        "combined_webroot_size_bytes": dir_size_bytes(root),
        "metadata_index_present": (root / "index.html").exists(),
        "private_content_present": (private_target / "index.html").exists(),
        "private_content_expected_url": PRIVATE_CONTENT_URL,
        "robots_noindex_present": True,
        "public_website_publication_performed": False,
        "solve_claim": False,
    }
    write_yaml(summary_out, summary)
    return summary


def _copy_tree_contents(source: Path, target: Path) -> None:
    for item in sorted(source.iterdir()):
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
        else:
            shutil.copyfile(item, destination)


def _inject_private_content_banner(index_path: Path) -> None:
    if not index_path.exists():
        return
    text = index_path.read_text(encoding="utf-8")
    banner = (
        "<section class='private-content-link'><h2>Private Deep Research Content Library</h2>"
        "<p>Review-gated hosted content is available at <a href='/private-content/'>/private-content/</a>. "
        "This is not public evidence and requires manual access control if sensitive.</p></section>"
    )
    if "/private-content/" in text:
        return
    if "</main>" in text:
        text = text.replace("</main>", banner + "\n</main>", 1)
    else:
        text += "\n" + banner + "\n"
    if NOINDEX not in text and "<head>" in text:
        text = text.replace("<head>", "<head>\n" + NOINDEX, 1)
    index_path.write_text(text, encoding="utf-8")


def _zip_dir(root: Path, zip_path: Path) -> Path:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(root).as_posix())
    sha256_file(zip_path)
    return zip_path
