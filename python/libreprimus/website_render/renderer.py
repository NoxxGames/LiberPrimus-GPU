"""Render the Stage 5AM static research index."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .loader import repo_relative, resolve, write_json
from .models import REQUIRED_ASSETS, REQUIRED_DATA_FILES, REQUIRED_PAGES, SAFE_DATASETS
from .privacy import sanitize_payload
from .search_index import build_search_index
from .templates import cards, page, summary_grid, table, warning_panel


def render_site(inputs: dict[str, Any], site_root: Path, *, create_zip: bool = True) -> dict[str, Any]:
    """Render the static metadata-only website export."""

    root = resolve(site_root)
    if root.exists():
        shutil.rmtree(root)
    (root / "assets").mkdir(parents=True, exist_ok=True)
    (root / "data").mkdir(parents=True, exist_ok=True)
    for subdir in ["bundles", "sources", "content", "claims", "publication-gates", "missing-sources", "deep-research", "about"]:
        (root / subdir).mkdir(parents=True, exist_ok=True)

    datasets = {name: sanitize_payload(payload) for name, payload in inputs["datasets"].items()}
    for name, filename in SAFE_DATASETS.items():
        write_json(root / "data" / filename, datasets[name])

    search_index = build_search_index(datasets)
    write_json(root / "assets" / "search-index.json", search_index)
    _write_assets(root)
    _write_pages(root, inputs, datasets)

    zip_path: Path | None = None
    if create_zip:
        zip_base = root.parent / root.name
        zip_name = shutil.make_archive(str(zip_base), "zip", root)
        zip_path = Path(zip_name)

    files = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    return {
        "record_type": "stage5am_render_output_manifest",
        "schema": "schemas/website-render/render-output-manifest-v0.schema.json",
        "stage_id": "stage-5am",
        "source_stage_id": "stage-5al",
        "metadata_only": True,
        "website_export_generated": True,
        "website_export_root": repo_relative(site_root),
        "upload_directory": repo_relative(site_root),
        "zip_package_generated": zip_path is not None,
        "zip_package_path": repo_relative(zip_path) if zip_path else None,
        "static_pages_generated": len(REQUIRED_PAGES),
        "data_json_files_generated": len(REQUIRED_DATA_FILES),
        "asset_files_generated": len(REQUIRED_ASSETS),
        "required_pages": REQUIRED_PAGES,
        "required_data_files": REQUIRED_DATA_FILES,
        "required_assets": REQUIRED_ASSETS,
        "generated_file_count": len(files),
        "generated_files": files,
        "raw_bodies_included": False,
        "private_ids_published": False,
        "public_website_publication_performed": False,
        "solve_claim": False,
    }


def _write_assets(root: Path) -> None:
    (root / "assets" / "site.css").write_text(
        """body{margin:0;font-family:Arial,Helvetica,sans-serif;background:#f6f7f9;color:#18202a;line-height:1.5}
.site-header{background:#1b2633;color:#fff;padding:24px 32px}.site-header p{max-width:920px}
.eyebrow{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#ffd166;font-weight:700}
nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}nav a{color:#fff;text-decoration:none;border:1px solid #738091;padding:6px 9px;border-radius:4px}
main{padding:24px 32px;max-width:1280px;margin:0 auto}.warning{background:#fff3cd;border:1px solid #e0b94f;padding:16px;margin-bottom:20px}
.summary-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:16px 0}
.summary-grid div,.card{background:#fff;border:1px solid #d9dee6;border-radius:6px;padding:14px}.summary-grid strong{display:block;color:#4d5968}.summary-grid span{font-size:20px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}.card h2{font-size:18px;margin:0 0 10px}
dl{display:grid;grid-template-columns:minmax(120px,36%) 1fr;gap:6px 10px}dt{font-weight:700;color:#46515f}dd{margin:0;word-break:break-word}
.labels span{display:inline-block;background:#e8eef6;color:#1e334d;border:1px solid #c8d4e3;border-radius:4px;padding:2px 6px;margin:2px;font-size:12px}
.table-wrap{overflow:auto;background:#fff;border:1px solid #d9dee6}table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:8px 10px;border-bottom:1px solid #e6eaf0;text-align:left;vertical-align:top}
footer{padding:20px 32px;color:#536170;border-top:1px solid #d9dee6}input.search{padding:8px;width:min(480px,100%);margin:12px 0}
""",
        encoding="utf-8",
    )
    (root / "assets" / "site.js").write_text(
        """document.addEventListener("DOMContentLoaded",()=>{const input=document.querySelector("[data-search]");
if(!input)return;const cards=[...document.querySelectorAll(".card, tbody tr")];input.addEventListener("input",()=>{
const q=input.value.toLowerCase();for(const card of cards){card.style.display=card.textContent.toLowerCase().includes(q)?"":"none";}});});
""",
        encoding="utf-8",
    )
    (root / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (root / "README.md").write_text(
        "# Stage 5AM static research index\n\n"
        "Upload this directory as a private, review-gated metadata-only research index. "
        "Do not upload raw `third_party/`, `data/raw/`, `research-inputs/`, or generated experiment outputs.\n",
        encoding="utf-8",
    )


def _write_pages(root: Path, inputs: dict[str, Any], datasets: dict[str, Any]) -> None:
    summary = inputs["stage5al_summary"]
    deep = datasets["deep-research-export"]
    bundles = datasets["research-bundles"]["records"]
    sources = datasets["source-cards"]["records"]
    content = datasets["content-index"]["records"]
    claims = datasets["community-claims"]["records"]
    gates = datasets["publication-gates"]["records"]
    missing = datasets["missing-sources"]["records"]

    home_items = {
        "stage": "Stage 5AM static research index",
        "current_data_source": inputs["website_ingest_dir"],
        "bundle_count": summary.get("bundle_count", 0),
        "source_card_count": summary.get("source_card_count", 0),
        "content_record_count": summary.get("content_index_count", 0),
        "community_claim_count": summary.get("claim_record_count", 0),
        "publication_gate_count": summary.get("publication_gate_count", 0),
        "deep_research_export_ready": summary.get("deep_research_export_ready", False),
        "recommended_next_stage": "Stage 5AN - Deep Research source inventory and reliability prompt",
        "public_website_ready_count": summary.get("public_website_ready_count", 0),
    }
    (root / "index.html").write_text(
        page("Liber Primus Research Index", warning_panel() + summary_grid(home_items)),
        encoding="utf-8",
    )
    (root / "bundles" / "index.html").write_text(
        page(
            "Research Bundles",
            '<input class="search" data-search placeholder="Filter bundles">'
            + cards(
                bundles,
                [
                    "bundle_id",
                    "readiness",
                    "priority",
                    "publication_status",
                    "review_status",
                    "source_ids",
                    "missing_source_refs",
                    "do_not_assume_tags",
                    "known_questions_refs",
                ],
                id_field="bundle_id",
            ),
            depth=1,
        ),
        encoding="utf-8",
    )
    (root / "sources" / "index.html").write_text(
        page(
            "Sources",
            '<input class="search" data-search placeholder="Filter sources">'
            + table(
                sources,
                [
                    "source_id",
                    "title",
                    "source_type",
                    "source_tier",
                    "priority",
                    "publication_status",
                    "review_status",
                    "path_kind",
                    "risk_level",
                ],
            ),
            depth=1,
        ),
        encoding="utf-8",
    )
    (root / "content" / "index.html").write_text(
        page(
            "Content Metadata",
            '<input class="search" data-search placeholder="Filter content">'
            + table(
                content,
                [
                    "content_id",
                    "bundle_id",
                    "source_id",
                    "content_kind",
                    "title",
                    "publication_status",
                    "review_status",
                    "path_kind",
                ],
            ),
            depth=1,
        ),
        encoding="utf-8",
    )
    (root / "claims" / "index.html").write_text(
        page(
            "Community Claims",
            '<input class="search" data-search placeholder="Filter claims">'
            + cards(
                claims,
                [
                    "claim_id",
                    "claim_family",
                    "verification_status",
                    "risk_level",
                    "requires_null_controls",
                    "requires_transcript_policy",
                    "requires_image_coordinate_policy",
                    "publication_status",
                    "review_status",
                ],
                id_field="claim_id",
            ),
            depth=1,
        ),
        encoding="utf-8",
    )
    (root / "publication-gates" / "index.html").write_text(
        page(
            "Publication Gates",
            warning_panel()
            + table(
                gates,
                [
                    "status",
                    "description",
                    "blocks_publication_by_default",
                    "metadata_may_be_public_after_review",
                    "private_deep_research_allowed",
                    "website_publication_allowed",
                    "raw_content_publication_allowed",
                ],
            ),
            depth=1,
        ),
        encoding="utf-8",
    )
    (root / "missing-sources" / "index.html").write_text(
        page(
            "Missing Sources",
            '<input class="search" data-search placeholder="Filter missing sources">'
            + table(missing, ["source_id", "title", "priority", "source_type", "status", "publication_status", "path_kind"]),
            depth=1,
        ),
        encoding="utf-8",
    )
    deep_items = {
        "recommended_first_report": deep.get(
            "recommended_first_report_prompt_title",
            "Stage 5AN - Deep Research source inventory and reliability prompt",
        ),
        "bundle_order": ", ".join(str(item) for item in deep.get("bundle_order", [])),
        "source_count": deep.get("source_card_count", summary.get("source_card_count", 0)),
        "claim_count": deep.get("claim_record_count", summary.get("claim_record_count", 0)),
        "citation_policy": deep.get("recommended_citation_policy", ""),
        "what_not_to_analyze_yet": ", ".join(str(item) for item in deep.get("what_not_to_analyze_yet", [])),
    }
    (root / "deep-research" / "index.html").write_text(
        page("Deep Research Handoff", warning_panel() + summary_grid(deep_items), depth=1),
        encoding="utf-8",
    )
    about_body = warning_panel() + summary_grid(
        {
            "upload_directory": "website-export/stage5am/research-index",
            "do_not_upload": "third_party, data/raw, research-inputs, experiments/results, codex-output",
            "metadata_only": True,
            "publication_gates_override": False,
            "deep_research_executed": False,
            "solve_claim": False,
        }
    )
    (root / "about" / "index.html").write_text(page("About This Export", about_body, depth=1), encoding="utf-8")
