"""Source module scaffold.

Implement fetch(), parse(), and validate() only after fetching and inspecting the
current live source files and documenting them in SOURCES.md.
"""

from pathlib import Path


def fetch(raw_dir: Path) -> Path:
    """Download and snapshot raw source files."""
    raise NotImplementedError("Inspect the live source and document SOURCES.md before implementing fetch().")


def parse(raw_path: Path, tidy_dir: Path) -> Path:
    """Transform raw snapshots into tidy data."""
    raise NotImplementedError("Parser not implemented for this source yet.")


def validate(tidy_path: Path) -> None:
    """Run schema and sanity checks."""
    raise NotImplementedError("Validation not implemented for this source yet.")
