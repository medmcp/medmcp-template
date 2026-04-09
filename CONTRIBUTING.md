# Contributing

Thanks for your interest in contributing to a medmcp ecosystem package.

This file lives in [medmcp-template](https://github.com/medmcp/medmcp-template) and is copied into every downstream repo. If you're reading it inside `medmcp-dicom`, `medmcp-neuro`, etc., the same workflow applies — only the repo name differs.

## Before you start

1. **Open an issue first** for non-trivial changes. It's cheap and avoids duplicated work or a direction that won't be merged.
2. **Check the scope.** Each medmcp package has a narrow scope (e.g. `medmcp-dicom` is *only* DICOM I/O, not neuro registration). If your idea spans multiple packages, say so in the issue so we can figure out where it belongs.

## Local setup

[uv](https://docs.astral.sh/uv/) is required; [just](https://just.systems/) is recommended but optional.

```bash
# 1. Fork and clone your fork
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. One-shot setup: installs uv if missing, syncs deps, installs pre-commit hooks
just setup
```

If you don't have `just`, the fallback is:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # if uv not installed
uv sync
uv run pre-commit install
```

## Running checks locally

Before pushing, run the same checks CI runs:

```bash
just check          # lint + format-check + typecheck + test
```

Or individually:

```bash
just lint           # ruff check
just format-check   # ruff format --check
just typecheck      # pyright (strict mode)
just test           # pytest
```

To auto-fix lint and formatting issues:

```bash
just fix
```

## Code style

- **Formatter / linter**: [Ruff](https://docs.astral.sh/ruff/). Line length 100, target Python 3.12.
- **Type checker**: [Pyright](https://github.com/microsoft/pyright) in **strict mode**. All code must be fully typed; no `Any` escapes without a comment explaining why.
- **Docstrings**: [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings). Public functions, classes, and modules are documented; trivial helpers can be skipped.
- **Pre-commit hooks** enforce formatting, trailing-whitespace, and YAML/TOML validity on every commit.

## Submitting a PR

1. Branch from `main` with a descriptive name: `feat/dicom-inspect`, `fix/anonymize-private-tags`.
2. Make small, focused commits with clear messages.
3. Push your branch and open a PR against `main`. Fill out the PR template.
4. CI runs on every PR — make sure all checks are green before requesting review.
5. Be responsive to review feedback; small PRs get merged fastest.

## Reporting issues

Use the issue templates: **Bug report** for defects, **Feature request** for proposals.

**Important for medical software:** *Never* attach real patient data (PHI) to issues, logs, or PRs. Use anonymized or synthetic DICOMs only. If a bug only reproduces on real data that you can't share, describe the file characteristics (modality, vendor, transfer syntax, dimensions) instead.

## Security

For security issues, please follow [SECURITY.md](SECURITY.md) — do **not** open a public issue for suspected vulnerabilities.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE).
