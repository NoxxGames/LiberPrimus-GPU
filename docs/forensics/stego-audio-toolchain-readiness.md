# Stego/Audio Toolchain Readiness

Stage 4N records toolchain readiness by path detection only. It does not execute stego/audio tools or run extraction commands.

Toolchain states include:

- `outguess_missing`
- `outguess_available_unverified`
- `outguess_available_version_recorded`
- `openpuff_manual_required`
- `mp3stego_manual_required`
- `hexdump_strings_available`
- `audio_tools_not_required`
- `not_applicable`

Tool paths in committed records are sanitised to avoid absolute local machine paths. The readiness records are blockers and planning metadata, not permission to execute historical tools.
