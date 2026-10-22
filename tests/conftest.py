from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def payload():
    """Fresh foundation config; contains no borrower records or empirical fixture."""
    return yaml.safe_load((ROOT / "configs/base.yaml").read_text())
