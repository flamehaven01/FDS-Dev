# Changelog
All notable changes to this project will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and the project adheres to [Semantic Versioning](https://semver.org/).

## [0.0.2] - 2025-11-19
### Added
- MarkdownParser now extracts inline links (file, anchor, and external) so lint rules can reason about documentation references.
- `BrokenLinkCheckRule` verifies anchors, relative files, and (optionally) external URLs, with new `.fdsrc.yaml` toggles for `enabled`, `check_external`, and timeout.
- README (English/Korean) now documents the optional broken link audits, CLI commands (`fds lint`, `fds translate`), and the broader “code-level internationalization” positioning, plus a dual-language About section.

### Changed
- `LintRunner` supports `enabled: false` or `'off'` configurations so optional rules can be declared without running.
- `.fdsrc.yaml` now documents how to configure the broken link rule without enabling it by default.
- Internal reports (`DOCUMENTATION_COMPLETE.md`, `FIX_SUMMARY.md`, `PROJECT_COMPLETION_REPORT.md`, `README_UPDATE_SUMMARY.md`, `test_ko.md`) were removed from the repository and added to `.gitignore`.

### Testing
- Added parser coverage for link extraction and regression tests for the new BrokenLinkCheckRule (anchor, file, and external scenarios).
- Mocked network calls in unit tests to keep the suite deterministic even when external checking is enabled.

## [0.0.1] - 2025-11-19
### Added
- Initial `fds` CLI with the `lint` and `translate` commands, parallel lint execution, and persistent cache management via `.fds_cache.json`.
- Translation pipeline that detects the source language, enforces `.fdsrc.yaml` rules, and fans out to DeepL, LibreTranslate, MyMemory, or the google-free backend with consistent result objects.
- Language-aware Markdown parser, comment-preserving code parser, and translation quality tensor exported from `fds_dev.i18n`.
- Configuration bootstrap (`.fdsrc.yaml`) plus opinionated rule presets for structure-aware linting.
- Documentation set: `docs/ARCHITECTURE.md`, `docs/TRANSLATION_ALGORITHM.md`, `docs/TROUBLESHOOTING.md`, and the bilingual README pair.

### Fixed
- Corrected the `TranslationResult` import path and provided a guarded `GoogleTranslator` placeholder so unknown providers raise friendly errors instead of crashing.
- Added exponential backoff retries to all HTTP translators to smooth over transient API failures.
- Hardened output formatting and cache serialization so linting large documentation trees is deterministic.

### Testing
- Added 92 dedicated tests across `tests/test_i18n_language_detector.py`, `tests/test_i18n_translator.py`, `tests/test_i18n_metacognition.py`, and `tests/test_i18n_code_parser.py`, yielding 95% coverage with 100/105 tests green.
- Captured regression data and fixtures for language detection, translation quality scoring, and lint runner behaviors.

### Documentation
- Rebuilt `README.md` with deployment badges, a feature tour, translation provider matrix, and support channels.
- Authored Korean documentation (`README_KR.md`) to demonstrate the translation workflow.

### Infrastructure
- Set up `.github/workflows/ci.yml` for multi-version lint + pytest runs and `.github/workflows/release.yml` for trusted-publisher PyPI deployments and GitHub Releases.
- Added `PYPI_SETUP.md` to document how to provision tokens, environments, and release tags.
