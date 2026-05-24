from __future__ import annotations

import re

import yaml

from libreprimus.paths import repo_root


ABSOLUTE_PATH_RE = re.compile(r"^[A-Za-z]:[\\/]|^\\\\")
FORBIDDEN_FIELDS = {"claim_text", "claim_formula", "claimed_values", "source_message_locator", "source_image_refs"}


def test_community_claim_metadata_excludes_private_body_fields() -> None:
    claims = yaml.safe_load((repo_root() / "data/website-ingest/stage5al/community-claims.yaml").read_text(encoding="utf-8"))
    for record in claims["records"]:
        assert not (FORBIDDEN_FIELDS & set(record))
        assert record["publication_status"] == "blocked_private_or_sensitive"
        assert record["website_publication_allowed"] is False
        assert record["execution_ready"] is False


def test_website_ingest_records_do_not_include_local_absolute_paths() -> None:
    for path in (repo_root() / "data/website-ingest/stage5al").glob("*.yaml"):
        text = path.read_text(encoding="utf-8")
        assert not ABSOLUTE_PATH_RE.search(text), path
