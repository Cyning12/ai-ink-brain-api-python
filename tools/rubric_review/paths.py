# -*- coding: utf-8 -*-
"""Rubric 产出路径（与任务审核 `docs/harness/reviews` 分离）。"""

from __future__ import annotations

from pathlib import Path

# 与 `tools/rubric_review/__init__.py` 同级上溯两级 = 本仓根
REPO_ROOT = Path(__file__).resolve().parents[2]


def default_rubric_runs_dir() -> Path:
    """默认落盘：`docs/_staging/jsonPKmermaid-rubric-demo/rubric_runs/`（暂存区，与 JSON/Mermaid 主实验目录分离）。"""
    return REPO_ROOT / "docs" / "_staging" / "jsonPKmermaid-rubric-demo" / "rubric_runs"
