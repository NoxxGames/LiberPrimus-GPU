from __future__ import annotations

import json
from pathlib import Path

from libreprimus.discord_promotion.export import read_yaml
from libreprimus.discord_promotion.promoter import promote_discord_sources


def _write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(record) for record in records) + "\n", encoding="utf-8")


def test_stage3o_promotes_public_source_links(tmp_path: Path) -> None:
    ingestion_dir = tmp_path / "ingestion"
    out_dir = tmp_path / "out"
    links_out = tmp_path / "promoted-links.yaml"
    methods_out = tmp_path / "promoted-methods.yaml"
    numerics_out = tmp_path / "promoted-numerics.yaml"
    _write_jsonl(
        ingestion_dir / "discord_extracted_links.jsonl",
        [
            {"link_id": "l1", "normalized_url": "https://github.com/example/repo?utm_source=x", "domain": "github.com", "url_kind": "github"},
            {"link_id": "l2", "normalized_url": "https://uncovering-cicada.fandom.com/wiki/Liber_Primus", "domain": "uncovering-cicada.fandom.com", "url_kind": "fandom"},
            {"link_id": "l3", "normalized_url": "https://archive.org/details/cicada", "domain": "archive.org", "url_kind": "internet_archive"},
            {"link_id": "l4", "normalized_url": "https://reddit.com/r/cicada/comments/abc", "domain": "reddit.com", "url_kind": "reddit"},
            {"link_id": "l5", "normalized_url": "https://cdn.discordapp.com/attachments/1/2/file.png?ex=private", "domain": "cdn.discordapp.com", "url_kind": "discord_attachment"},
        ],
    )
    _write_jsonl(
        ingestion_dir / "discord_method_claim_candidates.jsonl",
        [{"claim_type": "transform_method", "extracted_keywords": ["prime", "totient"], "redacted_summary": "method keyword cluster: prime/totient"}],
    )
    _write_jsonl(
        ingestion_dir / "discord_numeric_observation_candidates.jsonl",
        [{"candidate_kind": "prime", "numbers": [3301, 1033], "context_keywords": ["prime"], "redacted_summary": "numeric keyword cluster"}],
    )

    summary = promote_discord_sources(
        ingestion_dir=ingestion_dir,
        out_dir=out_dir,
        promoted_links_out=links_out,
        promoted_methods_out=methods_out,
        promoted_numerics_out=numerics_out,
        allow_warnings=True,
    )

    promoted = read_yaml(links_out)["records"]
    domains = {record["domain"] for record in promoted}
    assert {"github.com", "uncovering-cicada.fandom.com", "archive.org", "reddit.com"} <= domains
    assert all("discordapp.com" not in record["url"] for record in promoted)
    assert summary["private_or_unsafe_links_rejected_count"] == 1


def test_stage3o_promoted_records_are_reviewable() -> None:
    repo = Path(__file__).resolve().parents[2]
    payload = read_yaml(repo / "data/observations/discord/promoted-public-source-links-stage3o.yaml")
    assert payload["records"]
    for record in payload["records"][:20]:
        assert record["trusted_as_canonical"] is False
        assert record["review_status"]
        assert record["raw_message_committed"] is False
        assert record["usernames_committed"] is False
