"""Pytest configuration and fixtures."""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent


@pytest.fixture
def data_dir(project_root):
    """Get data directory."""
    return project_root / "data"


@pytest.fixture
def docs_dir(project_root):
    """Get docs directory."""
    return project_root / "docs"
