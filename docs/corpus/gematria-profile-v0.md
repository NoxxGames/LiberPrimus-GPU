# Gematria Profile v0

## Status

Frozen tooling profile. `canonical_profile_active=true`; `canonical_corpus_active=false`.

## Profile ID

`gematria-primus-v0`

## File Path

`data/profiles/gematria/gematria-primus-v0.json`

## SHA-256

`80cb10863b1fd3de57b44000c6bd90c307f11b90cc9d864a3d493e3f069c3280`

## 29-Entry Table

| Index | Prime | Rune | Preferred | Labels |
|---:|---:|---|---|---|
| 0 | 2 | ᚠ | F | F |
| 1 | 3 | ᚢ | U | U, V |
| 2 | 5 | ᚦ | TH | TH |
| 3 | 7 | ᚩ | O | O |
| 4 | 11 | ᚱ | R | R |
| 5 | 13 | ᚳ | C | C, K |
| 6 | 17 | ᚷ | G | G |
| 7 | 19 | ᚹ | W | W |
| 8 | 23 | ᚻ | H | H |
| 9 | 29 | ᚾ | N | N |
| 10 | 31 | ᛁ | I | I |
| 11 | 37 | ᛄ | J | J |
| 12 | 41 | ᛇ | EO | EO |
| 13 | 43 | ᛈ | P | P |
| 14 | 47 | ᛉ | X | X |
| 15 | 53 | ᛋ | S | S, Z |
| 16 | 59 | ᛏ | T | T |
| 17 | 61 | ᛒ | B | B |
| 18 | 67 | ᛖ | E | E |
| 19 | 71 | ᛗ | M | M |
| 20 | 73 | ᛚ | L | L |
| 21 | 79 | ᛝ | ING | ING, NG |
| 22 | 83 | ᛟ | OE | OE |
| 23 | 89 | ᛞ | D | D |
| 24 | 97 | ᚪ | A | A |
| 25 | 101 | ᚫ | AE | AE |
| 26 | 103 | ᚣ | Y | Y |
| 27 | 107 | ᛡ | IA | IA, IO |
| 28 | 109 | ᛠ | EA | EA |

## Arithmetic Domain

Modulo operations use index order in `Z_29`. Prime values are profile metadata and validation values, not modulo-29 indices.

## Latin Labels

Latin labels are display aliases. Index order is the arithmetic source of truth.

## Variant Glyphs

`ᛂ` is not canonical in this profile. It is documented in the glyph variant profile only.

## Validation Rules

The profile must have exactly 29 entries, contiguous indices `0..28`, the first 29 primes, unique rune glyphs, unique prime values, non-empty labels, and bijective rune/prime inverse lookups.
