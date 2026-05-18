"""Shared constants for Stage 3Q Discord review bundles."""

from __future__ import annotations

TOPICS = [
    "source-links-and-datasets",
    "cuneiform-base60-and-babylonian",
    "page-art-dots-binary-braille-stars",
    "number-squares-and-onion7",
    "deep-web-hash-and-cookies",
    "prime-streams-totients-and-number-theory",
    "vigenere-keys-and-literature",
    "gematria-gp-sums-and-rune-counts",
    "image-artwork-symbols-and-visual-clues",
    "outguess-stego-audio-spectrograms",
    "solved-pages-and-method-history",
    "claimed-decodes-false-positives-debunks",
    "tools-code-and-repositories",
    "open-questions-and-strong-leads",
]

TOPIC_TITLES = {
    "source-links-and-datasets": "Source Links And Datasets",
    "cuneiform-base60-and-babylonian": "Cuneiform Base60 And Babylonian",
    "page-art-dots-binary-braille-stars": "Page Art Dots Binary Braille Stars",
    "number-squares-and-onion7": "Number Squares And Onion7",
    "deep-web-hash-and-cookies": "Deep Web Hash And Cookies",
    "prime-streams-totients-and-number-theory": "Prime Streams Totients And Number Theory",
    "vigenere-keys-and-literature": "Vigenere Keys And Literature",
    "gematria-gp-sums-and-rune-counts": "Gematria GP Sums And Rune Counts",
    "image-artwork-symbols-and-visual-clues": "Image Artwork Symbols And Visual Clues",
    "outguess-stego-audio-spectrograms": "OutGuess Stego Audio Spectrograms",
    "solved-pages-and-method-history": "Solved Pages And Method History",
    "claimed-decodes-false-positives-debunks": "Claimed Decodes False Positives Debunks",
    "tools-code-and-repositories": "Tools Code And Repositories",
    "open-questions-and-strong-leads": "Open Questions And Strong Leads",
}

SHARD_FILENAMES = {
    "source-links-and-datasets": "source-links-and-datasets.md",
    "cuneiform-base60-and-babylonian": "cuneiform-base60-and-babylonian.md",
    "page-art-dots-binary-braille-stars": "page-art-dots-binary-braille-stars.md",
    "number-squares-and-onion7": "number-squares-and-onion7.md",
    "deep-web-hash-and-cookies": "deep-web-hash-and-cookies.md",
    "prime-streams-totients-and-number-theory": "prime-streams-totients-and-number-theory.md",
    "vigenere-keys-and-literature": "vigenere-keys-and-literature.md",
    "gematria-gp-sums-and-rune-counts": "gematria-gp-sums-and-rune-counts.md",
    "image-artwork-symbols-and-visual-clues": "image-artwork-symbols-and-visual-clues.md",
    "outguess-stego-audio-spectrograms": "outguess-stego-audio-spectrograms.md",
    "solved-pages-and-method-history": "solved-pages-and-method-history.md",
    "claimed-decodes-false-positives-debunks": "claimed-decodes-false-positives-debunks.md",
    "tools-code-and-repositories": "tools-code-and-repositories.md",
    "open-questions-and-strong-leads": "open-questions-and-strong-leads.md",
}

KNOWN_NUMBERS = {3301, 1033, 761, 167, 509, 503, 563, 569, 29, 31, 13, 3722101}

REDACTED_STREAM_LIMITS = {
    "links": 500,
    "methods": 500,
    "numerics": 500,
    "attachments": 200,
}

DEFAULT_SHARD_MAX_BYTES = 100_000
