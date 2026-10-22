# Contributing

Start with the [quickstart](README.md#quickstart) and [roadmap](docs/roadmap.md).
Keep each change focused, describe its assumptions, and update the relevant docs.
Use a topic branch and open a pull request against `main`.

Before submitting, run from the repository root:

```bash
uv sync --locked
uv run credit-risk validate-config configs/base.yaml
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

Add meaningful tests for new behavior and failure modes. Tests must not download data,
train models, or require network access. Keep any future fixtures tiny, synthetic,
and explicitly labeled. No borrower data is present today.

Do not commit data extracts, credentials, environments, generated reports, or model
binaries. Inspect the staged diff and tracked file list before committing; ignore
rules are a safeguard, not a privacy review. Notebooks must have outputs cleared
and contain no private information. Cite dataset licenses and upstream sources.

When changing dependencies, regenerate `uv.lock` with `uv lock`, verify `uv sync
--locked`, and state which optional environments were actually tested. A resolved
optional dependency is not evidence that a model runs. Run formatting before the
format check when editing Python. Document split, target, and metric changes before
using new empirical results to make a claim.
