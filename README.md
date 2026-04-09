# medmcp-template

Scaffolding template for packages in the [medmcp](https://github.com/medmcp) ecosystem — foundations (e.g. `medmcp-dicom`), stacks (e.g. `medmcp-neuro`), and supporting tools.

Click **Use this template** on GitHub to scaffold a new package with our standard layout, tooling, issue/PR templates, and contributor docs.

> [!WARNING]
> medmcp and its ecosystem packages are research software under active development and are **not licensed for clinical use**.

---

## What's in the box

| Area | Files | Notes |
|---|---|---|
| Build / deps | `pyproject.toml`, `.python-version` | uv-managed, Python ≥3.12, strict `ruff` + `pyright` + `pytest` config |
| Dev workflow | `justfile`, `.pre-commit-config.yaml` | `just setup`, `just check`, `just fix` |
| Editor hygiene | `.editorconfig`, `.gitignore` | |
| CI | `.github/workflows/ci.yml` | Lint, format-check, pyright (strict), pytest on py3.12 / 3.13 |
| Contributor docs | `README.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `CHANGELOG.md` | |
| Issue management | `.github/ISSUE_TEMPLATE/*`, `PULL_REQUEST_TEMPLATE.md`, `CODEOWNERS`, `dependabot.yml` | Medical-context-aware bug report form with PHI warnings |
| Package stub | `src/medmcp_template/`, `tests/test_smoke.py` | Minimal package that passes CI; rename after copy |
| Helper | `scripts/rename.sh` | One-shot rename of the placeholder package name |

---

## Using this template

### Option A: GitHub "Use this template" (recommended)

1. On GitHub, click **Use this template → Create a new repository**.
2. Choose a name (e.g. `medmcp-dicom`).
3. Clone your new repo locally.
4. Run the rename helper to replace the `medmcp_template` placeholder:

   ```bash
   ./scripts/rename.sh medmcp-dicom
   rm scripts/rename.sh
   ```

5. Edit `pyproject.toml` — update `description`, `keywords`, `authors`, and the `Homepage`/`Issues` URLs.
6. Edit `README.md` — replace this file with your project's own README.
7. `just setup` and `just check` — both should pass out of the box on an empty package.
8. Commit and push.

### Option B: Copy by hand

Clone, delete `.git/`, rename the package dir, find-replace `medmcp_template` → `your_package`, `git init` a new repo.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: fork, `just setup`, `just check`, open a PR against `main`.

## License

[Apache 2.0](LICENSE)
