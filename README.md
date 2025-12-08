# FDS-Dev (Flamehaven Doc Sanity for Developers)

<div align="center">

<p align="center">
  <img src="docs/Doc Sanity Logo.png" alt="FDS-Dev Logo" width="420">
</p>

**[English](README.md) | [한국어](README_KR.md)**

[![PyPI version](https://badge.fury.io/py/fds-dev.svg)](https://badge.fury.io/py/fds-dev)
[![Python Versions](https://img.shields.io/pypi/pyversions/fds-dev.svg)](https://pypi.org/project/fds-dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI/CD Pipeline](https://github.com/flamehaven01/FDS-Dev/actions/workflows/ci.yml/badge.svg)](https://github.com/flamehaven01/FDS-Dev/actions/workflows/ci.yml)
[![Test Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)](https://github.com/flamehaven01/FDS-Dev)
[![Code Quality](https://img.shields.io/badge/quality-A+-blue.svg)](https://github.com/flamehaven01/FDS-Dev)
[![SIDRCE Certified](https://img.shields.io/badge/SIDRCE-0.896%20Certified-green.svg)](https://github.com/flamehaven01/FDS-Dev)

<h3>
[>] Build once, speak every language.<br/>
[*] Enforce doc structure while AI translates without breaking code.<br/>
[=] Keep identifiers and code blocks pristine; localize only the prose.<br/>
[+] Ship production-ready English docs in seconds, not hours.
</h3>

<div align="center">[Features](#core-features)  [Quick Start](#quick-start)  [Documentation](docs/)  [Contributing](#contributing)  [Support](#support)</div>


---

## The Problem

You are a talented developer from Korea, Japan, China, Germany, or anywhere else in the world. Your code is brilliant, but writing documentation and comments in English is a chore. It slows you down and creates a barrier to sharing your work with the global open-source community.

Existing linters like `markdownlint` or `Vale` are great, but they are English-centric. They don't solve this core problem.

## The Solution: FDS-Dev

FDS-Dev is two tools in one:

1.  **A Blazing-Fast Linter:** Ensures your documentation has a clean, professional structure.
2.  **An AI-Powered Translator:** Automatically translates your native-language docs and comments into fluent, natural English.

**Stop worrying about English. Focus on your code.**

## Why FDS-Dev

### A New Category: Code-Level Internationalization

Traditional linters (markdownlint, Vale) only validate formatting, and conventional translators mangle code blocks or technical terms. FDS-Dev instead treats documentation, code comments, and docstrings as first-class data structures, so non-English-speaking developers can participate in global OSS without rewriting everything in English by hand.

### Problems We Actually Solve

- **Language barrier**: Converts README files, architecture notes, inline comments, and docstrings into production English while protecting the original code structure.
- **Documentation integrity**: Enforces section ordering, required headers, and other structure rules, so every README has the same professional baseline.

### Unique Advantages

1. **AI-driven code-aware translation**
   - Parses Markdown, Python docstrings, and inline comments via `CodeCommentParser`, so translations respect code layout and skip code blocks entirely.
   - Preserves CamelCase, snake_case, and other identifiers through `TechnicalTermDatabase`, keeping API names intact.
   - Scores every translation with an Omega (Ω) quality tensor; low-scoring translations can be retried or rejected automatically.

2. **Blazingly fast, structure-aware linting**
   - Runs lint jobs in parallel using a persistent cache (`.fds_cache.json`) so large doc trees finish quickly.
   - Validates structural requirements such as “License section must exist” or “Installation must precede Usage,” not just spelling.

3. **Flexible translation backends**
   - Default py-googletrans backend works with zero configuration for quick trials.
   - Switch to DeepL, MyMemory, or LibreTranslate in `.fdsrc.yaml` for higher quality or self-hosted control.

4. **Community impact**
   - Enables non-English-speaking developers to ship English documentation without losing intent, making it easier to get PRs accepted or run international product launches.
   - Actively-developed roadmap welcomes new contributors; stars, issues, and PRs help define the next wave of code-level localization tooling.

## Core Features

- **Structure-Aware Linting:** Go beyond simple style checks. Enforce section order, require specific headers, and validate the overall structure of your documents.
- **Broken Link Audits:** Optionally enable the `broken-link-check` rule to flag missing anchors, absent files, or unreachable URLs before publishing.
- **Automated Translation:** Translate Markdown files and source code comments from languages like Korean, Chinese, Japanese, and more into English.
- **Simple Configuration:** A single `.fdsrc.yaml` file to control everything.
- **Built for Speed:** Core components written for maximum performance.

## Quick Start

```bash
# Install
pip install --upgrade fds-dev

# Initialize configuration
fds init

# Run your first lint
fds lint README.md
```

### [>] 10-Minute Quickstart

**1. Lint your documentation** - Check for structural issues
```bash
fds lint README.ko.md
```

**2. Translate to English** - Global-ready documentation instantly
```bash
# Translates README.ko.md -> README.md
fds translate README.ko.md --output README.md

# Translate source code comments in-place
fds translate my_app/main.py --in-place
```

**3. See working examples**
```bash
# Clone repo and try examples
git clone https://github.com/flamehaven01/FDS-Dev.git
cd FDS-Dev
pip install -e .
python examples/basic_usage.py
```

[+] **Next Steps**: See [`examples/`](examples/) for production patterns and [`docs/ENTERPRISE.md`](docs/ENTERPRISE.md) for team deployments.

### Config and cache resolution
- `.fdsrc.yaml` is discovered starting from the path you pass to `fds lint` or `fds translate`, then walking upward. Each docs subtree can keep its own rules without changing your shell directory.
- The lint cache (`.fds_cache.json`) is stored alongside the target path (directory or file), keeping caches scoped to each docs tree.
- `translate` reports detected language with confidence and safely skips work when source and target languages already match.

## CLI Commands

- `fds lint <path>`: Runs the structure-aware lint checks configured in `.fdsrc.yaml`, including optional rules such as `broken-link-check`.
- `fds translate <path> [--output OUTPUT | --in-place]`: Converts Markdown or source files to English, preserving code blocks and identifiers.
- `fds translate --help` / `fds lint --help`: Show detailed usage and supported flags.

Broken link validation is controlled entirely via `.fdsrc.yaml`; once the rule is enabled, `fds lint` will report missing anchors, absent files, or unreachable URLs just like any other lint error.

## Translation Providers

FDS-Dev supports multiple translation providers. You can configure your preferred provider in the `.fdsrc.yaml` file.

| Provider                  | Default?        | API Key | Cost                  | Quality    | Stability      | Recommended Use Case                     |
| :------------------------ | :-------------- | :------ | :-------------------- | :--------- | :------------- | :--------------------------------------- |
| **Google Translate (Free)** | **✅ (Default)**  | None    | Free                  | High       | **Unstable**¹  | Personal projects, quick tests, general docs |
| **DeepL**                 | ❌              | **Required** | Limited Free Tier/Paid  | **Very High** | Very High      | Production, commercial, official docs      |
| **MyMemory**                | ❌              | None    | Free                  | Medium     | Medium         | Simple scripts, temporary use            |
| **LibreTranslate**          | ❌              | None    | Free (Self-hosted)    | Medium²    | **User-managed** | Private servers, offline, full control       |

> ¹ Uses an unofficial API, which may stop working without notice.
> ² Quality depends on the model you host yourself.

To use a provider other than the default, configure it in your `.fdsrc.yaml` file. For providers requiring an API key, it is highly recommended to use environment variables.

DeepL calls use a 5 second default timeout to avoid CLI hangs when the service is slow; override with `translator.providers.deepl.timeout`.

**Example for DeepL:**
```yaml
# .fdsrc.yaml
translator:
  provider: 'deepl'
  providers:
    deepl:
      # It's recommended to use the FDS_DEEPL_API_KEY environment variable instead.
      api_key: null
      timeout: 5   # seconds
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

See [CONTRIBUTING.md](CONTRIBUTING.md) for the detailed workflow, release checklist, and ASCII compatibility notes.

We welcome contributions from the community! Here's how you can help:

### How to Contribute

1. **Report Issues**: Found a bug? [Open an issue](https://github.com/flamehaven01/FDS-Dev/issues)
2. **Suggest Features**: Have an idea? Share it in [Discussions](https://github.com/flamehaven01/FDS-Dev/discussions)
3. **Submit Pull Requests**: Fix bugs or add features
4. **Improve Documentation**: Help make our docs even better

### Development Setup

```bash
# Clone repository
git clone https://github.com/flamehaven01/FDS-Dev.git
cd FDS-Dev

# Install in development mode
pip install -e .

# Run tests
pytest tests/ -v

# Run linter
flake8 fds_dev/
```

### Code Quality Standards

- Test coverage ≥ 90%
- All tests passing (100/105 expected)
- Follow PEP 8 style guide
- Add docstrings for public APIs
- Update documentation for new features

---

## For Teams & Enterprises

FDS-Dev scales from individual developers to enterprise deployments:

- [#] **Self-Hosted** - Full data control, air-gapped operation
- [#] **CI/CD Integration** - GitHub Actions, GitLab CI, Jenkins ready
- [&] **Custom Deployments** - Docker, Kubernetes, monorepo support
- [W] **SLA & Support** - Enterprise agreements available

[>] **Learn More**: See [`docs/ENTERPRISE.md`](docs/ENTERPRISE.md) for deployment architectures, security controls, and team workflows.

---

## Support

### Documentation

- **[Translation Algorithm](docs/TRANSLATION_ALGORITHM.md)** - Complete pipeline explanation
- **[Architecture Guide](docs/ARCHITECTURE.md)** - System design documentation
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### Get Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/flamehaven01/FDS-Dev/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/flamehaven01/FDS-Dev/discussions)
- **Email**: [info@flamehaven.space](mailto:info@flamehaven.space)

### Community

- **Website**: [flamehaven.space](https://flamehaven.space)
- **Repository**: [github.com/flamehaven01/FDS-Dev](https://github.com/flamehaven01/FDS-Dev)

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---


<div align="center">

**Made with ❤️ by [Flamehaven](https://flamehaven.space)**

[⬆ Back to top](#fds-dev-flamehaven-doc-sanity-for-developers)

</div>






