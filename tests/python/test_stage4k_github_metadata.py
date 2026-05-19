from __future__ import annotations

from libreprimus.source_lock_snapshots.github_metadata import (
    commit_addressed_url,
    parse_github_url,
)


def test_stage4k_github_parser_records_repo_blob_path_and_ref() -> None:
    reference = parse_github_url("https://github.com/cicada-solvers/iddqd/blob/master/2016/01/4gq25.jpg")
    assert reference is not None
    assert reference.owner == "cicada-solvers"
    assert reference.repo == "iddqd"
    assert reference.kind == "blob"
    assert reference.ref == "master"
    assert reference.path == "2016/01/4gq25.jpg"


def test_stage4k_github_commit_addressed_url() -> None:
    reference = parse_github_url("https://github.com/rtkd/iddqd")
    assert reference is not None
    url = commit_addressed_url(reference, "0123456789abcdef0123456789abcdef01234567")
    assert url == "https://github.com/rtkd/iddqd/tree/0123456789abcdef0123456789abcdef01234567"
