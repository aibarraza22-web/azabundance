"""Runtime configuration helpers."""

from __future__ import annotations

import os


def get_eia_api_key() -> str | None:
    """Return the optional EIA API key from the environment."""
    return os.getenv("EIA_API_KEY") or None
