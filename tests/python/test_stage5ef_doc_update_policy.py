from __future__ import annotations

from libreprimus.token_block import stage5ef
from test_stage5ef_common import ensure_stage5ef_built, load_yaml


def test_stage5ef_doc_update_policy_blocks_broad_doc_churn() -> None:
    ensure_stage5ef_built()

    result = stage5ef.validate_stage5ef_doc_update_policy()
    ledger = load_yaml("data/project-state/stage5ef-doc-update-policy-ledger.yaml")
    roles = {record["path"]: record for record in ledger["doc_roles"]}

    assert result.validation_error_count == 0
    for path in [
        "CIPHER_CATALOG.md",
        "EXPERIMENTS.md",
        "RESULTS_SCHEMA.md",
        "CUDA_NOTES.md",
        "BENCHMARKS.md",
        "tutorials/**",
        "docs/wiki-source/**",
    ]:
        assert roles[path]["stage5ef_default_update_allowed"] is False
    assert ledger["repo_wide_markdown_frontmatter_migration_performed"] is False
