# Source Browser Path Aliases

Path aliases help the Source Browser resolve local review paths that may be rooted differently on different machines. They are local navigation aids only and do not change committed source-lock records.

Default aliases live at:

```text
data/operator-console/source-browser/path-aliases/default.yaml
```

The default record keeps project-relative paths stable:

```yaml
record_type: source_browser_path_aliases
schema: schemas/operator-console/source-browser-path-aliases-v0.schema.json
path_aliases:
  - from: third_party
    to: third_party
  - from: data
    to: data
```

## Policy

- Aliases may make local browsing more convenient, but raw third-party files remain ignored.
- Aliases must not rewrite committed source records.
- Missing paths are warnings, not validation failures.
- The Source Browser must not automatically follow URLs or execute files after resolving an alias.
