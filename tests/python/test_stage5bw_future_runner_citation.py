from test_stage5bw_common import load_yaml


def test_stage5bw_future_runner_citation_fails_closed() -> None:
    citation = load_yaml("data/token-block/stage5bw-future-runner-citation-requirements.yaml")

    assert citation["future_runner_citation_status"] == "citation_required_fail_closed"
    assert "data/token-block/stage5bw-inactive-sidecar-planning-ingestion-proposal.yaml" in citation["future_runner_must_cite"]
    assert "citation_missing" in citation["fail_closed_if"]
    assert "generate_string4_bytes" in citation["runner_must_not"]
