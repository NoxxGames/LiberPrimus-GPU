from collections import Counter

from test_stage5by_common import load_yaml


def test_stage5by_reviews_stage5bw_duplicate_source_digest_rows() -> None:
    review = load_yaml("data/project-state/stage5by-stage5bw-source-digest-duplicate-review.yaml")
    assert review["stage5bw_source_digest_row_count"] == 23
    assert review["stage5bw_source_digest_unique_path_count"] == 21
    assert review["stage5bw_source_digest_duplicate_path_count"] == 2
    assert review["duplicates_deduplicated_or_classified"] is True
    assert {item["path"] for item in review["duplicate_paths"]} == {
        "data/token-block/stage5bd-dry-run-plan-manifest.yaml",
        "data/token-block/stage5bd-run-plan-id-registry.yaml",
    }


def test_stage5by_source_digest_index_has_unique_paths() -> None:
    digest = load_yaml("data/project-state/stage5by-reviewable-source-digest-index.yaml")
    paths = [record["path"] for record in digest["source_digest_records"]]
    assert len(paths) == len(set(paths))
    assert Counter(paths).most_common(1)[0][1] == 1
    assert digest["source_paths_unique"] is True
