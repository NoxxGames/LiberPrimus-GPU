# Split Mirror And Symmetry Analysis

Stage 3P adds deterministic split/mirror previews for visual review:

- left half
- right half
- mirrored left and right halves
- left-vs-right mirror difference
- top half
- bottom half
- mirrored top and bottom halves
- top-vs-bottom mirror difference
- 180-degree rotation difference

The metrics are normalized mean absolute grayscale differences. Low or high values are not interpreted as meaning. They only help reviewers find pages or regions worth inspecting later.

Future stages may promote a reviewed visual observation into a source registry record, but transform candidates are not experiment seeds by default.
