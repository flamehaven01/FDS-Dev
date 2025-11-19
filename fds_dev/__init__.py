"""FDS-Dev package initializer."""

# Expose key modules at package level for convenience
from .parser import MarkdownParser, Document, Header  # noqa: F401
from .rules import BaseRule, LintError  # noqa: F401

__all__ = [
    "MarkdownParser",
    "Document",
    "Header",
    "BaseRule",
    "LintError",
]
