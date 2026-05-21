from __future__ import annotations

from pathlib import Path


BANNED_TOKENS = (
    "<array>",
    "<vector>",
    "<string>",
    "<span>",
    "<optional>",
    "<variant>",
    "<sstream>",
    "<iomanip>",
    "<iostream>",
    "std::array",
    "std::vector",
    "std::string",
    "std::span",
    "std::optional",
    "std::variant",
    "std::ostringstream",
    "std::cout",
    "std::cerr",
    "throw",
)


def test_stage5j_cuda_facing_sources_use_conservative_subset() -> None:
    paths = [
        Path("cuda/include/libreprimus/gematria_shift_score_kernel.cuh"),
        Path("cuda/kernels/gematria_shift_score_kernel.cu"),
    ]
    findings: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for token in BANNED_TOKENS:
            if token in text:
                findings.append(f"{path}:{token}")
    assert findings == []


def test_stage5j_cxx_does_not_launch_python_workers() -> None:
    paths = [*Path("cuda").rglob("*.cu"), *Path("cuda").rglob("*.cuh"), *Path("src").rglob("*.cpp"), *Path("src").rglob("*.hpp")]
    worker_refs = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        if "python" in text and "worker" in text:
            worker_refs.append(str(path))
    assert worker_refs == []


def test_stage5f_uppercase_latin_kernel_remains_present() -> None:
    text = Path("cuda/kernels/shift_score_kernel.cu").read_text(encoding="utf-8")
    assert "stage5d-native-synthetic-shift-fixture-v0" in text
    assert "76a7d57c1da4d1ea39fc1d34f0e29ef4f732dab2f489b26d31758169ccd21a66" in text
    assert "LIBER PRIMUS STAGE FIVE D" in text
