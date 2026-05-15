from libreprimus.paths import package_root, project_path, repo_root


def test_repo_root_contains_readme() -> None:
    assert repo_root().joinpath("README.md").is_file()


def test_package_root_name() -> None:
    assert package_root().name == "libreprimus"


def test_project_path_joins_under_root() -> None:
    assert project_path("README.md") == repo_root().joinpath("README.md")
