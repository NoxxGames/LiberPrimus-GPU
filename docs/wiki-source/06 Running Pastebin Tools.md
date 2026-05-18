> This Wiki page mirrors $sourceRel. The repository tutorial file is the source of truth.

# Running Pastebin Tools

## Source

The local file `58-Pages-In-Runes-With-Prime-Values-Pastebin.txt` is a non-canonical legacy LP2 rune/prime-value source.

Numeric rows are Gematria prime values, not decimal modulo-29 indices.

## Commands

```powershell
libreprimus legacy-pastebin summary --input <path-to-local-txt>
libreprimus legacy-pastebin validate --input <path-to-local-txt> --allow-warnings
libreprimus legacy-pastebin extract --input <path-to-local-txt> --out-dir <repo-root>\data\normalized\legacy-pastebin
libreprimus legacy-pastebin anchors --input <path-to-local-txt>
```

## Outputs

Generated line-pair, anchor, summary, and warning files are ignored. They are parser outputs, not source truth.

## Troubleshooting

If validation reports unknown glyph `á›‚`, see `docs/research/glyph-variant-policy.md`. The raw glyph must be preserved.
