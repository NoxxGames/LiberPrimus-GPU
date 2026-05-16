from __future__ import annotations

from pathlib import Path

from libreprimus.experiment_execution.cpu_runner import run_cpu_execution_manifest

REPO = Path(__file__).resolve().parents[2]
MANIFEST_DIR = REPO / "experiments/manifests/cpu-execution"
OUT_DIR = REPO / "experiments/results/cpu-execution/stage2f"


def _run(name: str):
    return run_cpu_execution_manifest(MANIFEST_DIR / name, out_dir=OUT_DIR)


def test_direct_synthetic_execution_passes() -> None:
    _, results, _ = _run("stage2f-synthetic-direct-execution.yaml")

    assert results[0].match_status == "pass"
    assert results[0].output_normalized_text == "ABC"


def test_reverse_synthetic_execution_passes() -> None:
    _, results, _ = _run("stage2f-synthetic-reverse-gematria-execution.yaml")

    assert results[0].match_status == "pass"
    assert results[0].output_normalized_text == "ABC"


def test_rotated_reverse_synthetic_execution_passes() -> None:
    _, results, _ = _run("stage2f-synthetic-rotated-reverse-execution.yaml")

    assert results[0].match_status == "pass"
    assert results[0].output_normalized_text == "ABC"


def test_vigenere_synthetic_execution_passes() -> None:
    _, results, _ = _run("stage2f-synthetic-vigenere-execution.yaml")

    assert results[0].match_status == "pass"
    assert results[0].output_normalized_text == "ABC"


def test_prime_stream_synthetic_execution_passes() -> None:
    _, results, _ = _run("stage2f-synthetic-prime-stream-execution.yaml")

    assert results[0].match_status == "pass"
    assert results[0].output_normalized_text == "ABC"


def test_output_sha_and_safety_flags_are_deterministic() -> None:
    _, first, _ = _run("stage2f-synthetic-direct-execution.yaml")
    _, second, _ = _run("stage2f-synthetic-direct-execution.yaml")
    result = first[0]

    assert result.output_sha256 == second[0].output_sha256
    assert result.search_performed is False
    assert result.candidate_generation_performed is False
    assert result.scoring_used is False
    assert result.cuda_used is False
    assert not hasattr(result, "candidate_plaintexts")

