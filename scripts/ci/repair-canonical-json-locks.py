"""Normalize committed canonical JSON locks and verify SHA-256 metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]

LOCKED_JSON_FILES = [
    Path("data/profiles/gematria/gematria-primus-v0.json"),
    Path("data/profiles/separators/rtkd-separator-grammar-v0.json"),
    Path("data/profiles/glyph-variants/glyph-variants-v0.json"),
    Path("data/transform-registry/cpu-reference-transforms-v0.json"),
]


def canonical_json_bytes(payload: Any) -> bytes:
    text = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)
    return (text + "\n").encode("utf-8")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def metadata_path_for(json_path: Path) -> Path:
    return json_path.with_suffix(".metadata.json")


def sha_path_for(json_path: Path) -> Path:
    return json_path.with_suffix(".sha256")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_bytes_if_changed(path: Path, payload: bytes, *, check: bool) -> bool:
    current = path.read_bytes() if path.exists() else b""
    if current == payload:
        return False
    if check:
        raise SystemExit(f"{path} is not normalized or has stale content.")
    path.write_bytes(payload)
    return True


def update_metadata(metadata_path: Path, sha256: str, *, check: bool) -> bool:
    metadata = load_json(metadata_path)
    if not isinstance(metadata, dict):
        raise SystemExit(f"{metadata_path} must contain a JSON object.")
    metadata["sha256"] = sha256
    return write_bytes_if_changed(metadata_path, canonical_json_bytes(metadata), check=check)


def update_sha_lock(json_path: Path, sha256: str, *, check: bool) -> bool:
    lock_path = sha_path_for(json_path)
    payload = f"{sha256}  {json_path.name}\n".encode("utf-8")
    return write_bytes_if_changed(lock_path, payload, check=check)


def verify_no_crlf(path: Path) -> None:
    if b"\r\n" in path.read_bytes():
        raise SystemExit(f"{path} contains CRLF line endings.")


def repair_file(json_path: Path, *, check: bool) -> tuple[str, str, bool, bool, bool]:
    payload = load_json(json_path)
    before = sha256_bytes(json_path.read_bytes())
    canonical = canonical_json_bytes(payload)
    after = sha256_bytes(canonical)
    json_changed = write_bytes_if_changed(json_path, canonical, check=check)
    lock_changed = update_sha_lock(json_path, after, check=check)
    metadata_changed = update_metadata(metadata_path_for(json_path), after, check=check)
    verify_no_crlf(json_path)
    verify_no_crlf(sha_path_for(json_path))
    verify_no_crlf(metadata_path_for(json_path))
    actual_lock = sha_path_for(json_path).read_text(encoding="utf-8").split()[0]
    actual_metadata = load_json(metadata_path_for(json_path))["sha256"]
    if actual_lock != after:
        raise SystemExit(f"{sha_path_for(json_path)} does not match {json_path}.")
    if actual_metadata != after:
        raise SystemExit(f"{metadata_path_for(json_path)} sha256 does not match {json_path}.")
    return before, after, json_changed, lock_changed, metadata_changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    changed_json = 0
    changed_locks = 0
    changed_metadata = 0
    for relative in LOCKED_JSON_FILES:
        path = REPO_ROOT / relative
        before, after, json_changed, lock_changed, metadata_changed = repair_file(
            path,
            check=bool(args.check),
        )
        changed_json += int(json_changed)
        changed_locks += int(lock_changed)
        changed_metadata += int(metadata_changed)
        status = "ok" if before == after else "updated"
        print(f"{relative}: {status} {before} -> {after}")
    mode = "check" if args.check else "repair"
    print(
        f"canonical_json_lock_{mode}: json_changed={changed_json} "
        f"locks_changed={changed_locks} metadata_changed={changed_metadata}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
