"""Image-compression artifact backlog records for Stage 4E."""

from __future__ import annotations

from typing import Any


FUTURE_TESTS = [
    "source variant filename/count comparison",
    "sha256 and file-size comparison",
    "dimension and color-mode comparison",
    "DCT/blockiness estimate",
    "noise residual and edge residual views",
    "recompress-difference maps",
    "channel and bitplane views",
    "star-like symbol candidate review",
]

NEGATIVE_CONTROLS = [
    "known JPEG recompression controls",
    "PNG controls with no JPEG intermediate",
    "random crop controls",
    "mirror and rotation controls for star-like artefacts",
]


def build_image_artifact_observations() -> list[dict[str, Any]]:
    """Create future-preflight observations without interpreting images."""

    return [
        {
            "record_type": "image_compression_artifact_observation",
            "observation_id": "stage4e-lp-jpeg-like-artifact-preflight",
            "artifact_type": "jpeg_like_compression_or_source_variant",
            "source_basis": "community note and local LP image locks; no image transform run in Stage 4E",
            "possible_causes": [
                "source artwork had JPEG intermediates",
                "images were recompressed before later mirrors",
                "public mirrors have different compression histories",
                "ordinary compression or scanner noise",
                "less likely intentional visual artefacts",
            ],
            "future_tests": FUTURE_TESTS,
            "negative_controls": NEGATIVE_CONTROLS,
            "review_status": "future_preflight",
            "usable_as_experiment_seed": False,
            "trusted_as_canonical": False,
            "solve_claim": False,
            "notes": "Compression-like or star-like features remain review candidates only, not evidence.",
        }
    ]
