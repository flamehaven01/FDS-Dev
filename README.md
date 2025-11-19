# FDS-Dev

**A blazingly fast, structure-aware linter for your documentation, supercharged with AI-powered translation.**

Built for the global developer community. Write documentation and code comments in your native language, and let FDS-Dev instantly translate it to production-ready English.

---

## The Problem

You are a talented developer from Korea, Japan, China, Germany, or anywhere else in the world. Your code is brilliant, but writing documentation and comments in English is a chore. It slows you down and creates a barrier to sharing your work with the global open-source community.

Existing linters like `markdownlint` or `Vale` are great, but they are English-centric. They don't solve this core problem.

## The Solution: FDS-Dev

FDS-Dev is two tools in one:

1.  **A Blazing-Fast Linter:** Ensures your documentation has a clean, professional structure.
2.  **An AI-Powered Translator:** Automatically translates your native-language docs and comments into fluent, natural English.

**Stop worrying about English. Focus on your code.**

## Core Features

- **Structure-Aware Linting:** Go beyond simple style checks. Enforce section order, require specific headers, and validate the overall structure of your documents.
- **Automated Translation:** Translate Markdown files and source code comments from languages like Korean, Chinese, Japanese, and more into English.
- **Simple Configuration:** A single `.fdsrc.yaml` file to control everything.
- **Built for Speed:** Core components written for maximum performance.

## Quick Start

### 1. Lint your documentation

Check for structural issues in your documentation.

```bash
fds lint README.ko.md
```

### 2. Translate to English

Translate your Korean README and its comments into a new, global-ready English file.

```bash
# Translates README.ko.md -> README.md
fds translate README.ko.md --output README.md
```

```bash
# Translate a source code file's comments in-place
fds translate my_app/main.py --in-place
```

## Deployment & Automation

### Continuous Integration

GitHub Actions automatically runs the test suite across Python 3.9–3.11 and builds release artifacts for every push and pull request targeting `main`. You can find the workflow definition in `.github/workflows/ci.yml`.

### Automated PyPI Releases

Tagging a commit with the `v*` pattern (for example, `v0.2.0`) triggers `.github/workflows/release.yml`, which builds the project with `python -m build` and publishes the result to PyPI using the `PYPI_API_TOKEN` secret.

### Official Docker Image

Ship the CLI as a container image by using the provided `Dockerfile`:

```bash
docker build -t fds-dev .
docker run --rm fds-dev lint README.md
```

The image installs the package globally and exposes the `fds` entrypoint, so any CLI command can be run directly.

## Contributing

FDS-Dev is in early development. Contributions are welcome!
