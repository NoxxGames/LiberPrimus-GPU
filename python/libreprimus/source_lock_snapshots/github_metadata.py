"""GitHub metadata parsing and commit-address locking for Stage 4K."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from urllib.parse import unquote, urlparse


@dataclass(frozen=True)
class GitHubReference:
    """Parsed GitHub URL reference."""

    owner: str
    repo: str
    kind: str
    ref: str | None = None
    path: str | None = None

    @property
    def repo_url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}"

    @property
    def clone_url(self) -> str:
        return f"{self.repo_url}.git"


def parse_github_url(url: str) -> GitHubReference | None:
    """Parse a supported github.com URL."""

    parsed = urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return None
    parts = [unquote(part) for part in parsed.path.strip("/").split("/") if part]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1].removesuffix(".git")
    if len(parts) >= 4 and parts[2] in {"blob", "tree"}:
        return GitHubReference(owner=owner, repo=repo, kind=parts[2], ref=parts[3], path="/".join(parts[4:]) or None)
    return GitHubReference(owner=owner, repo=repo, kind="repository")


def resolve_commit_sha(reference: GitHubReference, *, allow_network: bool, cwd: Path | None = None) -> str | None:
    """Resolve a GitHub ref to a commit SHA via git ls-remote when network is allowed."""

    if not allow_network:
        return None
    ref = reference.ref or "HEAD"
    candidates = [ref]
    if ref != "HEAD":
        candidates.extend([f"refs/heads/{ref}", f"refs/tags/{ref}"])
    for candidate in candidates:
        try:
            result = subprocess.run(
                ["git", "ls-remote", reference.clone_url, candidate],
                cwd=cwd,
                check=False,
                capture_output=True,
                text=True,
                timeout=30,
            )
        except (OSError, subprocess.SubprocessError):
            continue
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            sha = line.split(maxsplit=1)[0] if line.strip() else ""
            if len(sha) == 40 and all(char in "0123456789abcdefABCDEF" for char in sha):
                return sha.lower()
    return None


def commit_addressed_url(reference: GitHubReference, commit_sha: str | None = None) -> str:
    """Return a commit-addressed GitHub URL when a commit SHA is available."""

    if commit_sha is None:
        return reference.repo_url
    if reference.kind in {"blob", "tree"} and reference.path:
        return f"{reference.repo_url}/{reference.kind}/{commit_sha}/{reference.path}"
    if reference.kind == "tree" and not reference.path:
        return f"{reference.repo_url}/tree/{commit_sha}"
    return f"{reference.repo_url}/tree/{commit_sha}"


def github_lock_metadata(url: str, *, allow_network: bool, cwd: Path | None = None) -> dict:
    """Return GitHub commit-address metadata for a URL."""

    reference = parse_github_url(url)
    if reference is None:
        return {}
    commit_sha = resolve_commit_sha(reference, allow_network=allow_network, cwd=cwd)
    return {
        "github_owner": reference.owner,
        "github_repo": reference.repo,
        "github_ref": reference.ref,
        "github_path": reference.path,
        "github_reference_kind": reference.kind,
        "github_commit_sha": commit_sha,
        "canonical_url": commit_addressed_url(reference, commit_sha),
        "commit_address_locked": commit_sha is not None,
    }
