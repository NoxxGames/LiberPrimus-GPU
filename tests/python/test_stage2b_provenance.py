from pathlib import Path

from libreprimus.result_store.provenance import (
    git_branch,
    git_commit,
    host_metadata,
    profile_metadata,
    sha256_file,
    tool_versions,
)


def test_git_commit_and_branch_detected() -> None:
    assert git_commit()
    assert git_branch()


def test_python_and_platform_metadata_captured_without_environment_dump() -> None:
    host = host_metadata()
    tools = tool_versions()

    assert host["python_version"]
    assert host["platform"]
    assert "PATH" not in host
    assert "TOKEN" not in str(host).upper()
    assert tools["python"]


def test_manifest_sha256_and_profiles_are_captured() -> None:
    manifest = Path("experiments/manifests/solved-baselines/stage2a-all-known-solved-baselines.yaml")

    assert len(sha256_file(manifest)) == 64
    profiles = profile_metadata()
    assert {profile["profile_id"] for profile in profiles} >= {
        "gematria-primus-v0",
        "rtkd-separator-grammar-v0",
        "glyph-variants-v0",
    }
