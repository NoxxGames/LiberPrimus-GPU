# Source-Lock Snapshot Policy

Source-locking preserves enough immutable public-source metadata to make later claims reproducible.
It is not a content mirror and does not make a source canonical.

Snapshot policy values:

- `metadata_only`: commit URL, source class, copyright note, and retrieval status only.
- `ignored_local_snapshot`: fetch small public text/HTML to an ignored cache and commit hash metadata.
- `committed_small_text_snapshot`: reserved for explicitly safe small text snapshots.
- `commit_addressed_reference`: prefer GitHub commit/tree/blob references over branch URLs.
- `archive_reference_only`: lock archive/Wayback URL metadata without committing content.
- `deferred_manual_review`: preserve candidate metadata until retrieval or copyright status is clearer.
- `rejected_unsafe_or_noisy`: record why a URL is not suitable for source-locking.

Default restrictions:

- Network retrieval requires `--allow-network`.
- Full repositories are not mirrored.
- Raw Discord/private URLs are rejected.
- Binary, image, audio, font, PDF, and archive artefacts are metadata-only by default.
- Fetched bytes go under `third_party/SourceSnapshots/` and remain ignored.
- Source locks do not imply solved plaintext, canonical corpus activation, or page-boundary finality.
