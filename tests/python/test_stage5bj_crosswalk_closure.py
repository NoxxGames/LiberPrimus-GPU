import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: str):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_every_stage5bi_crosswalk_candidate_has_stage5bj_closure() -> None:
    stage5bi = load_yaml("data/historical-route/stage5bi-original-archive-crosswalk-candidates.yaml")
    stage5bj = load_yaml("data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml")

    source_ids = {record["candidate_id"] for record in stage5bi["records"]}
    closure_ids = {record["candidate_id"] for record in stage5bj["records"]}

    assert stage5bj["source_stage5bi_crosswalk_candidate_count"] == len(source_ids) == 12
    assert stage5bj["crosswalk_closure_record_count"] == len(stage5bj["records"])
    assert closure_ids == source_ids
    assert stage5bj["raw_archive_files_committed"] is False
    assert stage5bj["execution_allowed"] is False
    assert stage5bj["solve_claim"] is False


def test_closure_status_counts_match_summary() -> None:
    stage5bj = load_yaml("data/historical-route/stage5bj-original-archive-crosswalk-closure.yaml")
    summary = load_yaml("data/project-state/stage5bj-summary.yaml")

    counts = stage5bj["crosswalk_closure_status_counts"]
    assert counts["closed_exact_original_archive_equivalent"] == summary["closed_exact_original_archive_equivalent_count"]
    assert (
        counts["closed_archive_equivalent_but_not_exact_surface"]
        == summary["closed_archive_equivalent_but_not_exact_surface_count"]
    )
    assert counts["local_archive_search_no_match"] == summary["local_archive_search_no_match_count"]
