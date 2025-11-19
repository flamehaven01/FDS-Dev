"""Pytest configuration helpers."""

import sys
from pathlib import Path

# Ensure the project root is importable regardless of how pytest is invoked
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
