# Task Badger Docs

Mkdocs-material documentation site for Task Badger. Published to https://docs.taskbadger.net.

## Commands

```bash
uv sync                                # Install deps (use uv, not pip — README is stale)
inv serve                              # Dev server on http://localhost:8082
uv run mkdocs serve -a localhost:8082  # Equivalent without invoke
uv run mkdocs build                    # Build static site to ./site/
```

## Architecture

- Content: Markdown files in `docs/`
- Config: `mkdocs.yml` (theme, nav, plugins, markdown extensions)
- Tasks: `tasks.py` (invoke tasks)

## Sibling repo dependency

The Python SDK reference pages use `mkdocstrings` to pull docstrings from a sibling
checkout of `taskbadger-python`. Path is set via `TB_PYTHON_SRC` (defaults to
`../taskbadger-python`). Without it sitting next to this repo, SDK pages won't render
properly. mkdocs also `watch:`es that path during `mkdocs serve`.

## Navigation

The site nav is controlled by the `nav:` block in `mkdocs.yml`, **not** by the
filesystem. Adding a new `.md` file under `docs/` doesn't make it appear in the
sidebar — add it to `nav:` too.

## Deployment

Push to `main` triggers `.github/workflows/deploy.yml`, which runs
`uv run mkdocs gh-deploy --force`. There is no staging — main goes live.
