# Separator Grammar v0

## Status

Frozen tooling profile. `canonical_profile_active=true`; `canonical_corpus_active=false`.

## Grammar ID

`rtkd-separator-grammar-v0`

## File Path

`data/profiles/separators/rtkd-separator-grammar-v0.json`

## SHA-256

`e0a5f682ced4afcf25956d06b1b49d1356203fe8ed47c7dec41365e3bec7b8e7`

## Separator Classes

- `word_separator`: `-`
- `clause_separator`: `.`
- `paragraph_separator`: `&`
- `segment_separator`: `$`
- `chapter_separator`: `§`
- `line_separator`: `/`
- `page_separator_or_marker`: `%`
- `whitespace`: space and tab
- `physical_newline`
- `numeric_literal`
- `hex_literal_candidate`
- `unknown_symbol`

## Preservation Rules

Separators are preserved as tokens. They are not discarded during normalization, and token records preserve source positions.

## Page and Line Rules

`%` does not activate a canonical page boundary. `/` may support logical-line views but does not prove a page boundary.

## Unknown Symbol Policy

Unknown non-rune, non-separator symbols are preserved and produce warnings.

## Tokenization Implications

Stage 0E corpus candidates include separator tokens alongside rune tokens so later normalization can replay source text and grammar decisions.
