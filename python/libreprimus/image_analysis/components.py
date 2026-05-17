"""Small deterministic connected-component summaries for thresholded images."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any

from PIL import Image

CONNECTIVITY = "4-connected"
DEFAULT_MAX_DIMENSION = 256


@dataclass(frozen=True)
class ComponentSummary:
    threshold: int
    component_count: int
    largest_components: list[dict[str, Any]]
    analysis_width: int
    analysis_height: int
    connectivity: str = CONNECTIVITY

    @property
    def largest_component_area_ratio(self) -> float:
        if not self.largest_components:
            return 0.0
        return float(self.largest_components[0]["area_ratio"])


def component_summary(
    gray: Image.Image,
    *,
    threshold: int,
    max_dimension: int = DEFAULT_MAX_DIMENSION,
    top_k: int = 5,
) -> ComponentSummary:
    """Return a 4-connected foreground component summary for pixels <= threshold."""
    analysis = _analysis_image(gray, max_dimension=max_dimension)
    width, height = analysis.size
    pixels = list(analysis.getdata())
    foreground = [pixel <= threshold for pixel in pixels]
    visited = bytearray(width * height)
    total_pixels = width * height
    components: list[tuple[int, tuple[int, int, int, int]]] = []

    for index, is_foreground in enumerate(foreground):
        if not is_foreground or visited[index]:
            continue
        area, bbox = _visit_component(index, width, height, foreground, visited)
        components.append((area, bbox))

    components.sort(key=lambda item: item[0], reverse=True)
    largest = [
        {
            "area": area,
            "area_ratio": round(area / total_pixels, 8),
            "bbox": list(bbox),
        }
        for area, bbox in components[:top_k]
    ]
    return ComponentSummary(
        threshold=threshold,
        component_count=len(components),
        largest_components=largest,
        analysis_width=width,
        analysis_height=height,
    )


def _analysis_image(gray: Image.Image, *, max_dimension: int) -> Image.Image:
    width, height = gray.size
    largest = max(width, height)
    if largest <= max_dimension:
        return gray.copy()
    scale = max_dimension / largest
    resized = (max(1, round(width * scale)), max(1, round(height * scale)))
    resample = getattr(Image, "Resampling", Image).NEAREST
    return gray.resize(resized, resample=resample)


def _visit_component(
    start_index: int,
    width: int,
    height: int,
    foreground: list[bool],
    visited: bytearray,
) -> tuple[int, tuple[int, int, int, int]]:
    queue: deque[int] = deque([start_index])
    visited[start_index] = 1
    area = 0
    min_x = width
    min_y = height
    max_x = -1
    max_y = -1

    while queue:
        index = queue.popleft()
        y, x = divmod(index, width)
        area += 1
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        for neighbor in _neighbors(x, y, width, height):
            if not visited[neighbor] and foreground[neighbor]:
                visited[neighbor] = 1
                queue.append(neighbor)
    return area, (min_x, min_y, max_x + 1, max_y + 1)


def _neighbors(x: int, y: int, width: int, height: int):
    if x > 0:
        yield y * width + x - 1
    if x + 1 < width:
        yield y * width + x + 1
    if y > 0:
        yield (y - 1) * width + x
    if y + 1 < height:
        yield (y + 1) * width + x
