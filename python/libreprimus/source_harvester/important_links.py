"""Stage 5AJ important-links parsing and manifest extension generation."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from .export import read_records, repo_relative, resolve, write_json, write_records, write_yaml
from .hashing import hash_file
from .models import (
    SOURCE_MANIFEST_PATH,
    STAGE5AJ_ID,
    STAGE5AJ_IMPORTANT_LINKS_PATH,
    STAGE5AJ_MANIFEST_EXTENSION_PATH,
    STAGE5AJ_OUTPUT_DIR,
    STAGE5AJ_REPORTS,
    STAGE5AJ_SOURCE_ROOT,
    STAGE5AJ_SOURCE_STAGE_ID,
)
from .usefulfiles import LOCAL_SOURCE_SPECS

URL_PATTERN = re.compile(r"https?://[^\s)>\]]+")


def _url(
    source_id: str,
    title: str,
    url: str,
    source_type: str,
    priority: str,
    related_leads: list[str],
    bundle_ids: list[str],
) -> dict[str, Any]:
    return {
        "source_id": source_id,
        "title": title,
        "url": url,
        "source_type": source_type,
        "priority": priority,
        "source_tier": _tier(source_type),
        "recommended_capture_modes": _capture_modes(source_type),
        "related_leads": related_leads,
        "bundle_ids": bundle_ids,
    }


def _tier(source_type: str) -> str:
    if source_type in {"github_repo", "github_org"}:
        return "tier1_committed_repo_record"
    if source_type == "fandom_page":
        return "tier2_archived_community_page_with_references"
    if source_type.startswith("reddit"):
        return "tier4_social_claim_or_screenshot"
    return "tier3_reproducible_community_data"


def _capture_modes(source_type: str) -> list[str]:
    if source_type == "fandom_page":
        return ["html", "markdown", "text", "tables", "images", "links"]
    if source_type.startswith("reddit"):
        return ["targeted_post_capture", "listing_metadata", "links"]
    if source_type.startswith("github"):
        return ["commit_sha", "file_inventory", "hash_inventory"]
    return ["metadata", "text", "links"]


MINIMUM_URL_RECORDS: list[dict[str, Any]] = [
    _url("fandom_symbols_drawing_art_liber_primus", "Symbols/Drawing/Art of Liber Primus", "https://uncovering-cicada.fandom.com/wiki/Symbols/Drawing/Art_of_Liber_Primus", "fandom_page", "A1", ["depictions_tree_cicada_mayfly_wing_spiral_cuneiform", "cuneiform_base60_base59", "red_runes_dots_punctuation"], ["04-cuneiform-base60-base59", "05-red-markers-and-visual-numerics"]),
    _url("fandom_frequency_analysis_unsolved_pages", "Frequency Analysis Unsolved Pages", "https://uncovering-cicada.fandom.com/wiki/Frequency_Analysis_Unsolved_Pages", "fandom_page", "A1", ["same_rune_bigram_statistic", "low_doublet_statistical_texture"], ["03-page-49-51-token-block", "09-community-hypotheses"]),
    _url("fandom_page_56", "PAGE 56", "https://uncovering-cicada.fandom.com/wiki/PAGE_56", "fandom_page", "A1", ["dwh_target_and_algorithms", "p56_prime_minus_one"], ["03-page-49-51-token-block", "08-tools-gpprime-dwh-gematria"]),
    _url("fandom_page_57", "PAGE 57", "https://uncovering-cicada.fandom.com/wiki/PAGE_57", "fandom_page", "A1", ["p57_parable_gp_product", "p56_p57_gp_sum_3301_1033"], ["03-page-49-51-token-block", "08-tools-gpprime-dwh-gematria"]),
    _url("fandom_list_of_missing_information", "List of missing information", "https://uncovering-cicada.fandom.com/wiki/List_of_missing_information", "fandom_page", "A1", ["source_gap_closure", "negative_or_retired_ideas"], ["09-community-hypotheses"]),
    _url("fandom_outguess", "OutGuess", "https://uncovering-cicada.fandom.com/wiki/OutGuess", "fandom_page", "A1", ["outguess_all_pages_claim", "stego_tool_provenance"], ["06-outguess-stego-hidden-formatting"]),
    _url("fandom_2016_message", "2016 Message", "https://uncovering-cicada.fandom.com/wiki/2016_Message", "fandom_page", "A1", ["2016_liber_primus_is_the_way_quote", "2016_prime_layering"], ["06-outguess-stego-hidden-formatting", "09-community-hypotheses"]),
    _url("fandom_other_twitter_accounts", "Other Twitter Accounts Associated With 3301's Emails", "https://uncovering-cicada.fandom.com/wiki/Other_Twitter_Accounts_Associated_With_3301%27s_Emails", "fandom_page", "A2", ["twitter_1033_3301_fibonacci_prime_context"], ["09-community-hypotheses"]),
    _url("fandom_harmonic_key_proposal", "PROPOSAL: THE 16-DIGIT HARMONIC KEY", "https://uncovering-cicada.fandom.com/wiki/PROPOSAL%3A_THE_16-DIGIT_HARMONIC_KEY_%282422826321411203%29", "fandom_page", "C", ["ai_generated_or_overfit_claims", "negative_or_retired_ideas"], ["10-known-negative-retired-ideas"]),
    _url("reddit_cicada_subreddit", "r/cicada subreddit", "https://www.reddit.com/r/cicada/", "reddit_subreddit", "A2", ["reddit_claims_targeted_capture"], ["09-community-hypotheses"]),
    _url("reddit_page32_path_lies_empty", "Next step is page 32 in Liber Primus / path lies empty", "https://www.reddit.com/r/cicada/comments/9zb42i/next_step_is_page_32_in_liber_primus_the/", "reddit_post", "A2", ["page32_tree_path_lies_empty", "2016_liber_primus_is_the_way_quote"], ["09-community-hypotheses"]),
    _url("reddit_56_57_gp_sums_3301_1033", "56/57.jpg GP sums of 3301 and 1033", "https://www.reddit.com/r/cicada/comments/1m9lm2a/5657jpg_gp_sums_of_3301_and_1033_found_next_to/", "reddit_post", "A1", ["p56_p57_gp_sum_3301_1033", "fehu_skip_policy"], ["08-tools-gpprime-dwh-gematria", "09-community-hypotheses"]),
    _url("reddit_magic_square_diagonals", "Hidden magic diagonals found in magic squares", "https://www.reddit.com/r/cicada/comments/1lrwmb9/hidden_magic_diagonals_found_in_the_magic_squares/", "reddit_post", "A1", ["magic_square_diagonal_3301_1033", "know_this_magic_square_claims"], ["09-community-hypotheses"]),
    _url("reddit_frequency_analysis_lp_notes", "Frequency analysis on LP and notes", "https://www.reddit.com/r/cicada/comments/rxo4vg/frequency_analysis_on_lp_and_some_notes_and/", "reddit_post", "A2", ["frequency_analysis_unsolved", "low_doublet_statistical_texture"], ["09-community-hypotheses"]),
    _url("reddit_layered_primes_2016_message", "Layered primes in the 2016 message", "https://www.reddit.com/r/cicada/comments/12j1evm/layered_primes_in_the_2016_message/", "reddit_post", "A2", ["2016_prime_layering"], ["09-community-hypotheses"]),
    _url("brown_corpus_reference", "Brown Corpus", "https://en.wikipedia.org/wiki/Brown_Corpus", "static_webpage", "A2", ["brown_corpus_word_length_controls"], ["09-community-hypotheses"]),
]


def parse_important_links(
    *,
    source_root: Path = STAGE5AJ_SOURCE_ROOT,
    existing_manifest_path: Path = SOURCE_MANIFEST_PATH,
    results_dir: Path = STAGE5AJ_OUTPUT_DIR,
    out: Path = STAGE5AJ_IMPORTANT_LINKS_PATH,
    out_manifest_extension: Path = STAGE5AJ_MANIFEST_EXTENSION_PATH,
) -> dict[str, Any]:
    """Parse UsefulFiles important_links and write manifest-extension records."""

    root = resolve(source_root)
    existing_manifest_records = read_records(existing_manifest_path)
    existing_urls = {canonical_url(str(record.get("url", ""))): record for record in existing_manifest_records if record.get("url")}
    link_path = _find_first(root, ["important_links.txt", "important_link.txt"])
    ideas_path = _find_first(root, ["ideas.txt"])
    parsed = _parse_url_file(link_path) if link_path else []
    if ideas_path:
        parsed.extend(_parse_url_file(ideas_path))
    by_url: dict[str, dict[str, Any]] = {}
    for record in parsed:
        by_url.setdefault(canonical_url(record["url"]), record)
    index_records = []
    for url_key, parsed_record in sorted(by_url.items()):
        matched = existing_urls.get(url_key)
        source_record = _source_record_for_url(parsed_record["url"], parsed_record.get("title") or parsed_record["url"])
        index_records.append(
            {
                "record_type": "stage5aj_important_links_url_record",
                "schema": "schemas/source-harvester/important-links-source-index-v0.schema.json",
                "stage_id": STAGE5AJ_ID,
                "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
                "url": parsed_record["url"],
                "canonical_url": url_key,
                "line_number": parsed_record["line_number"],
                "nearby_title": parsed_record.get("title"),
                "source_type": source_record["source_type"],
                "duplicate_status": "duplicate_existing_manifest" if matched else "new_or_planned_source",
                "already_known_source_id": matched.get("source_id") if matched else None,
                "new_source_id": None if matched else source_record["source_id"],
                "recommended_priority": source_record["priority"],
                "recommended_bundle_id": source_record["bundle_ids"][0] if source_record["bundle_ids"] else None,
                "network_fetch_performed": False,
                "solve_claim": False,
            }
        )
    extension_records = _local_source_records(root)
    url_extension_records = []
    minimum_canonicals = {canonical_url(record["url"]) for record in MINIMUM_URL_RECORDS}
    for canonical, parsed_record in sorted(by_url.items()):
        if canonical in existing_urls or canonical in minimum_canonicals:
            continue
        source_record = _source_record_for_url(
            parsed_record["url"],
            parsed_record.get("title") or parsed_record["url"],
        )
        url_extension_records.append(
            {
                **source_record,
                "record_type": "stage5aj_source_manifest_extension_record",
                "schema": "schemas/source-harvester/usefulfiles-source-manifest-extension-v0.schema.json",
                "stage_id": STAGE5AJ_ID,
                "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
                "collection_status": "new_online_source_added",
                "present_in_important_links": True,
                "manual_collection_required": True,
                "allow_network_fetch": False,
                "allow_dynamic_browser": False,
                "raw_commit_allowed": False,
                "google_drive_storage_allowed": False,
                "network_fetch_performed": False,
                "solve_claim": False,
            }
        )
    for minimum in MINIMUM_URL_RECORDS:
        canonical = canonical_url(minimum["url"])
        parsed_present = canonical in by_url
        duplicate = canonical in existing_urls
        if duplicate:
            continue
        url_extension_records.append(
            {
                **minimum,
                "record_type": "stage5aj_source_manifest_extension_record",
                "schema": "schemas/source-harvester/usefulfiles-source-manifest-extension-v0.schema.json",
                "stage_id": STAGE5AJ_ID,
                "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
                "collection_status": "new_online_source_added" if parsed_present else "planned_source_record_absent_from_local_links",
                "present_in_important_links": parsed_present,
                "manual_collection_required": True,
                "allow_network_fetch": False,
                "allow_dynamic_browser": False,
                "raw_commit_allowed": False,
                "google_drive_storage_allowed": False,
                "network_fetch_performed": False,
                "solve_claim": False,
            }
        )
    extension_records.extend(sorted(url_extension_records, key=lambda item: item["source_id"]))
    summary = {
        "record_type": "stage5aj_important_links_source_index",
        "schema": "schemas/source-harvester/important-links-source-index-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "source_path": repo_relative(link_path) if link_path else None,
        "important_links_detected": link_path is not None,
        "important_links_urls_found": len(index_records),
        "important_links_new_urls": sum(1 for record in index_records if record["duplicate_status"] == "new_or_planned_source"),
        "duplicate_url_count": sum(1 for record in index_records if record["duplicate_status"] == "duplicate_existing_manifest"),
        "fandom_url_count": sum(1 for record in index_records if record["source_type"] == "fandom_page"),
        "reddit_url_count": sum(1 for record in index_records if str(record["source_type"]).startswith("reddit")),
        "github_url_count": sum(1 for record in index_records if str(record["source_type"]).startswith("github")),
        "static_url_count": sum(1 for record in index_records if record["source_type"] == "static_webpage"),
        "network_fetch_performed": False,
        "solve_claim": False,
    }
    manifest_summary = {
        "record_type": "stage5aj_usefulfiles_source_manifest_extension",
        "schema": "schemas/source-harvester/usefulfiles-source-manifest-extension-v0.schema.json",
        "stage_id": STAGE5AJ_ID,
        "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
        "local_source_records": sum(1 for record in extension_records if record["source_type"] == "local_user_upload"),
        "new_url_source_records": sum(1 for record in extension_records if record["source_type"] != "local_user_upload"),
        "network_fetch_performed": False,
        "online_repo_clone_performed": False,
        "google_drive_storage_used": False,
        "solve_claim": False,
    }
    write_records(out, index_records, **summary)
    write_records(out_manifest_extension, extension_records, **manifest_summary)
    write_json(results_dir / STAGE5AJ_REPORTS["important_links"], {**summary, "records": index_records})
    write_yaml(results_dir / STAGE5AJ_REPORTS["manifest_preview"], {**manifest_summary, "records": extension_records})
    return {**summary, "manifest_extension_records": len(extension_records)}


def canonical_url(url: str) -> str:
    return url.strip().rstrip("/").replace("http://uncovering-cicada.wikia.com", "https://uncovering-cicada.fandom.com")


def _parse_url_file(path: Path) -> list[dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        for match in URL_PATTERN.finditer(line):
            url = match.group(0).rstrip(".,")
            title = line[: match.start()].strip(" :*-") or None
            records.append({"url": url, "title": title, "line_number": line_number})
    return records


def _find_first(root: Path, names: list[str]) -> Path | None:
    for name in names:
        path = root / name
        if path.exists():
            return path
    return None


def _source_record_for_url(url: str, title: str) -> dict[str, Any]:
    canonical = canonical_url(url)
    for record in MINIMUM_URL_RECORDS:
        if canonical_url(record["url"]) == canonical:
            return record
    host = urlparse(url).netloc.lower()
    source_type = _source_type(host, url)
    source_id = _source_id_from_url(title, host)
    return _url(source_id, title, url, source_type, "A2" if source_type in {"fandom_page", "reddit_post", "reddit_subreddit"} else "B", [_lead_from_title(title)], [_bundle_for_source_type(source_type)])


def _source_type(host: str, url: str) -> str:
    if "uncovering-cicada" in host:
        return "fandom_page"
    if "reddit.com" in host and "/comments/" in url:
        return "reddit_post"
    if "reddit.com" in host:
        return "reddit_subreddit"
    if host == "github.com":
        return "github_repo" if len(urlparse(url).path.strip("/").split("/")) >= 2 else "github_org"
    if "pastebin.com" in host:
        return "pastebin"
    if "youtube.com" in host or "youtu.be" in host:
        return "youtube_video"
    if "docs.google.com" in host:
        return "google_sheet"
    if "colab.research.google.com" in host:
        return "google_colab"
    if "dropbox.com" in host:
        return "dropbox_folder"
    if "shinyapps.io" in host:
        return "shiny_app"
    return "static_webpage"


def _source_id_from_url(title: str, host: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_") or re.sub(r"[^a-z0-9]+", "_", host.lower()).strip("_")
    prefix = "stage5aj"
    if "uncovering-cicada" in host:
        prefix = "fandom"
    elif "reddit.com" in host:
        prefix = "reddit"
    elif host == "github.com":
        prefix = "github"
    return f"{prefix}_{base}"[:96]


def _lead_from_title(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")[:80] or "source_gap_closure"


def _bundle_for_source_type(source_type: str) -> str:
    if source_type == "fandom_page":
        return "09-community-hypotheses"
    if source_type.startswith("reddit"):
        return "09-community-hypotheses"
    if source_type.startswith("github"):
        return "08-tools-gpprime-dwh-gematria"
    return "09-community-hypotheses"


def _local_source_records(root: Path) -> list[dict[str, Any]]:
    records = []
    for source_id, spec in LOCAL_SOURCE_SPECS.items():
        matched = _find_source_file(root, spec["filenames"])
        if matched is None:
            continue
        hashed = hash_file(matched)
        records.append(
            {
                "record_type": "stage5aj_source_manifest_extension_record",
                "schema": "schemas/source-harvester/usefulfiles-source-manifest-extension-v0.schema.json",
                "stage_id": STAGE5AJ_ID,
                "source_stage_id": STAGE5AJ_SOURCE_STAGE_ID,
                "source_id": source_id,
                "title": spec["title"],
                "source_type": "local_user_upload",
                "priority": spec["priority"],
                "source_tier": spec["source_tier"],
                "collection_status": "local_ready",
                "local_path_hint": repo_relative(matched),
                "sha256": hashed["sha256"],
                "size_bytes": hashed["size_bytes"],
                "recommended_capture_modes": spec["recommended_capture_modes"],
                "related_leads": spec["clue_categories"],
                "bundle_ids": spec["bundle_ids"],
                "manual_collection_required": False,
                "allow_network_fetch": False,
                "allow_dynamic_browser": False,
                "raw_commit_allowed": False,
                "google_drive_storage_allowed": False,
                "network_fetch_performed": False,
                "solve_claim": False,
            }
        )
    return records


def _find_source_file(root: Path, filenames: set[str]) -> Path | None:
    for path in sorted(root.glob("*"), key=lambda item: item.name.lower()):
        normalized = path.name.lower().replace("_", " ").replace("-", " ")
        normalized = " ".join(normalized.split())
        if normalized in filenames:
            return path
    return None
