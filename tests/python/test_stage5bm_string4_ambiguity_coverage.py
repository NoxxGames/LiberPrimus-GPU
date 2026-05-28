from test_stage5bm_common import load_yaml


def test_stage5bm_string4_ambiguity_coverage_counts_known_classes() -> None:
    record = load_yaml("data/token-block/stage5bm-string4-ambiguity-class-coverage.yaml")
    counts = record["ambiguity_class_counts"]

    assert record["coverage_assessment"] == "partially_supported"
    assert counts["I_l"] == 6
    assert counts["unsupported_external"] == 1
    assert record["majority_difference_class"] == "I_l"
    assert record["execution_allowed"] is False
