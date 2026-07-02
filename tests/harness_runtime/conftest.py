"""harness_runtime 单测夹具。"""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sessions_tmp(tmp_path: Path) -> Path:
    root = tmp_path / "sessions"
    root.mkdir()
    return root
