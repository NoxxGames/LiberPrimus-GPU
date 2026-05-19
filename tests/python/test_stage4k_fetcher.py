from __future__ import annotations

from libreprimus.source_lock_snapshots.fetcher import fetch_to_ignored_cache, hash_bytes


def test_stage4k_network_disabled_fetch_produces_deferred_record(tmp_path) -> None:
    result = fetch_to_ignored_cache(
        url="https://uncovering-cicada.fandom.com/wiki/OutGuess",
        cache_dir=tmp_path,
        record_id="test",
        allow_network=False,
    )
    assert result.retrieval_status == "network_disabled"
    assert result.content_sha256 is None


def test_stage4k_synthetic_fetch_hash_is_deterministic() -> None:
    assert hash_bytes(b"stage4k") == hash_bytes(b"stage4k")
    assert hash_bytes(b"stage4k") != hash_bytes(b"stage4K")
