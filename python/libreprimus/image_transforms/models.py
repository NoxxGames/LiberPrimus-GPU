"""Shared constants for Stage 3P image transforms."""

from __future__ import annotations

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png"}
THRESHOLDS = (32, 64, 96, 128, 160, 192, 224)
COMPONENT_OVERLAY_THRESHOLDS = (64, 128, 192)
CONTACT_TRANSFORMS = (
    "grayscale",
    "invert",
    "autocontrast",
    "threshold_128",
    "edge_difference",
    "bitplane_0",
    "bitplane_7",
    "left_right_mirror_difference",
    "top_bottom_mirror_difference",
    "rotation_180_difference",
)
REVIEW_STATUS = "human_review_required"
