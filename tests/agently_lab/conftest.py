"""agently_lab 测试级 marker 与公共夹具。"""

from __future__ import annotations

import pytest


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line(
        "markers",
        "agently_lab_online: 调用真实 LLM / GitHub API 的测试，默认 -m 'not agently_lab_online' 跳过",
    )
