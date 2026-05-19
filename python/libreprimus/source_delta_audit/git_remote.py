"""Git remote tree inspection for Stage 4E."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess
import tempfile


@dataclass(frozen=True)
class RemoteTree:
    repo_url: str
    reachable: bool
    head: str | None
    paths: list[str]
    warning: str | None = None


def inspect_remote_tree(repo_url: str, *, cache_dir: Path, allow_network: bool) -> RemoteTree:
    """Return a tree listing without storing repository blobs in the project."""

    local_path = Path(repo_url)
    if local_path.exists():
        return _inspect_local_repo(local_path, repo_url)
    if not allow_network:
        return RemoteTree(
            repo_url=repo_url,
            reachable=False,
            head=None,
            paths=[],
            warning="network_not_allowed",
        )
    cache_dir.mkdir(parents=True, exist_ok=True)
    temp_root = Path(tempfile.mkdtemp(prefix="stage4e-iddqd-", dir=str(cache_dir)))
    try:
        clone_dir = temp_root / "repo"
        _run_git(
            [
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "--depth",
                "1",
                repo_url,
                str(clone_dir),
            ]
        )
        head = _run_git(["-C", str(clone_dir), "rev-parse", "HEAD"]).strip()
        paths = _run_git(["-C", str(clone_dir), "ls-tree", "-r", "--name-only", "HEAD"]).splitlines()
        return RemoteTree(repo_url=repo_url, reachable=True, head=head, paths=sorted(paths))
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        return RemoteTree(
            repo_url=repo_url,
            reachable=False,
            head=None,
            paths=[],
            warning=f"git_remote_inspection_failed:{error}",
        )
    finally:
        shutil.rmtree(temp_root, ignore_errors=True)


def _inspect_local_repo(path: Path, repo_url: str) -> RemoteTree:
    try:
        head = _run_git(["-C", str(path), "rev-parse", "HEAD"]).strip()
        paths = _run_git(["-C", str(path), "ls-tree", "-r", "--name-only", "HEAD"]).splitlines()
        return RemoteTree(repo_url=repo_url, reachable=True, head=head, paths=sorted(paths))
    except (subprocess.CalledProcessError, FileNotFoundError) as error:
        return RemoteTree(
            repo_url=repo_url,
            reachable=False,
            head=None,
            paths=[],
            warning=f"local_git_inspection_failed:{error}",
        )


def _run_git(args: list[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return completed.stdout
