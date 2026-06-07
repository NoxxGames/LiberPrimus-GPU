"""Shared paths and constants for the Operator Console."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

APP_NAME = "Liber Primus Operator Console"
SOURCE_BROWSER_NAME = "Source Browser"

DATA_ROOT = Path("data/operator-console")
CONFIG_DIR = DATA_ROOT / "config"
SOURCE_BROWSER_ROOT = DATA_ROOT / "source-browser"
MANUAL_ENTRIES_DIR = SOURCE_BROWSER_ROOT / "manual-entries"
MANUAL_OVERRIDES_DIR = SOURCE_BROWSER_ROOT / "manual-overrides"
TOMBSTONES_DIR = SOURCE_BROWSER_ROOT / "tombstones"
COLUMN_PROFILES_DIR = SOURCE_BROWSER_ROOT / "column-profiles"
PATH_ALIASES_DIR = SOURCE_BROWSER_ROOT / "path-aliases"
SAVED_FILTERS_DIR = SOURCE_BROWSER_ROOT / "saved-filters"

DEFAULT_COLUMN_PROFILE = COLUMN_PROFILES_DIR / "default.yaml"
DEFAULT_PATH_ALIASES = PATH_ALIASES_DIR / "default.yaml"

CACHE_ROOT = Path(".cache/operator-console")
THUMBNAIL_CACHE_DIR = CACHE_ROOT / "thumbnails"
INDEX_CACHE_PATH = CACHE_ROOT / "index.json"
LOG_PATH = CACHE_ROOT / "operator-console.log"

CONTEXT_FILE = Path("ChatGPT-ContextFile.md")

SOURCE_RECORD_GLOBS = (
    "data/project-state/**/*.yaml",
    "data/historical-route/**/*.yaml",
    "data/source-harvester/**/*.yaml",
    "data/token-block/**/*.yaml",
    "data/research/**/*.yaml",
    "data/evidence-atlas/**/*.yaml",
)

MANUAL_RECORD_GLOBS = (
    "data/operator-console/source-browser/manual-entries/*.yaml",
    "data/operator-console/source-browser/manual-overrides/*.yaml",
    "data/operator-console/source-browser/tombstones/*.yaml",
)

REQUIRED_DATA_DIRS = (
    CONFIG_DIR,
    MANUAL_ENTRIES_DIR,
    MANUAL_OVERRIDES_DIR,
    TOMBSTONES_DIR,
    COLUMN_PROFILES_DIR,
    PATH_ALIASES_DIR,
    SAVED_FILTERS_DIR,
)

CATEGORY_NAMES = (
    "All",
    "Source-locks",
    "Candidate families",
    "Number facts",
    "Visual sources",
    "Images",
    "Documents",
    "References",
    "Solved precedents",
    "Warnings",
    "Hash contracts",
    "Quote / crib candidates",
    "DiskCipher",
    "Triangle",
    "Page32",
    "Blake",
    "Music",
    "Mayfly",
    "Dots",
    "Cover geometry",
    "Manual entries",
    "ChatGPT context",
)

DEFAULT_COLUMNS = (
    ("title", "Entry", 240),
    ("category", "Category", 130),
    ("candidate_family_id", "Candidate", 260),
    ("stage_id", "Stage", 90),
    ("status", "Status", 130),
    ("trust_tier", "Trust", 80),
    ("confidence", "Confidence", 120),
    ("images", "Images", 110),
    ("document_paths", "Docs", 100),
    ("urls", "URLs", 90),
    ("number_facts", "Number facts", 170),
    ("warnings", "Warnings", 110),
    ("modified_at", "Modified", 150),
    ("source_record_path", "Source record", 300),
)

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
DOCUMENT_EXTENSIONS = {".docx", ".xlsx", ".pdf", ".txt", ".md", ".yaml", ".yml", ".json", ".csv"}

HUGE_TEXT_CHAR_LIMIT = 20_000
HUGE_TEXT_LINE_LIMIT = 500

GUI_INSTALL_MESSAGE = "GUI dependencies are not installed. Install with: pip install -e .[gui]"
