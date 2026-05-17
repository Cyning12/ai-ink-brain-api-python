# -*- coding: utf-8 -*-
"""Markdown / JSON 报告写入 `docs/harness/reviews/`。"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tools.rubric_review.paths import REPO_ROOT
from tools.rubric_review.reviewer import FullReviewState


def _json_rel_for_meta(json_path: Path) -> str:
    try:
        return json_path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return json_path.name


def state_to_json_dict(state: FullReviewState, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    base = {
        "rubric_name": state.rubric.get("rubric_name"),
        "rubric_version": state.rubric.get("version"),
        "review_a": {
            "dimension_scores": state.review_a.dimension_scores,
            "justification": state.review_a.justification,
            "model_used": state.review_a.model_used,
        },
        "review_b": {
            "dimension_scores": state.review_b.dimension_scores,
            "justification": state.review_b.justification,
            "model_used": state.review_b.model_used,
        },
        "final_scores": state.final_scores,
        "arbitration_needed": state.arbitration_needed,
        "arbitration_mode": state.arbitration_mode,
        "arbitration_justification": state.arbitration_justification,
        "disputed_dimensions": state.disputed_dimensions,
        "meta": state.meta,
    }
    if extra:
        base["run"] = extra
    return base


def render_markdown(
    state: FullReviewState,
    *,
    artifact_path: str,
    rubric_path: str,
    backend: str,
    json_rel_path: str,
) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    m1 = state.meta.get("reviewer_r1_model", "")
    m2 = state.meta.get("reviewer_r2_model", "")
    marb = state.meta.get("arbitration_model", "")
    seed = state.meta.get("random_seed")
    seed_s = "" if seed is None else str(seed)

    lines: list[str] = [
        "# Rubric 双人评审报告（自动化）",
        "",
        "## 元信息",
        "",
        "| 字段 | 值 |",
        "|------|-----|",
        f"| 落盘时间（UTC） | {now} |",
        f"| LLM 后端 | `{backend}` |",
        f"| R1 模型 | `{m1}` |",
        f"| R2 模型 | `{m2}` |",
        f"| 仲裁模型 | `{marb}` |",
        f"| 随机种子 | `{seed_s or '（未固定，每次不同）'}` |",
        f"| 工件路径 | `{artifact_path}` |",
        f"| Rubric 路径 | `{rubric_path}` |",
        f"| 机器可读结果 | `{json_rel_path}` |",
        "",
        "## Rubric",
        "",
        f"- **名称**：{state.rubric.get('rubric_name', '')}",
        f"- **版本**：{state.rubric.get('version', '')}",
        "",
        "## 分数汇总",
        "",
        "| dimension_id | R1 | R2 | 终分 |",
        "|--------------|----|----|------|",
    ]
    for dim in state.rubric["dimensions"]:
        did = dim["id"]
        s1 = state.review_a.dimension_scores.get(did, "")
        s2 = state.review_b.dimension_scores.get(did, "")
        fin = state.final_scores.get(did)
        fin_s = "" if fin is None else str(fin)
        lines.append(f"| `{did}` | {s1} | {s2} | {fin_s} |")

    lines.extend(
        [
            "",
            "## 评审理由",
            "",
            f"### R1（`{m1}`）",
            "",
            state.review_a.justification or "（空）",
            "",
            f"### R2（`{m2}`）",
            "",
            state.review_b.justification or "（空）",
            "",
        ]
    )
    if state.arbitration_needed:
        lines.extend(
            [
                "## 仲裁",
                "",
                f"- **需要仲裁**：是",
                f"- **模式**：`{state.arbitration_mode}`",
                f"- **争议维度**：{', '.join(state.disputed_dimensions) or '（无）'}",
                f"- **仲裁所用模型**：`{marb}`",
                "",
            ]
        )
        if state.arbitration_justification:
            lines.extend(["### 仲裁说明", "", state.arbitration_justification, ""])
        if state.arbitration_mode == "human_pending":
            lines.extend(
                [
                    "> **待人工**：`fallback` 为 `human_webhook` 时，终分中 `null` 表示未自动仲裁；请在 webhook 侧闭环后回填本 JSON 或另开审查文档。",
                    "",
                ]
            )
    else:
        lines.extend(["## 仲裁", "", "- **需要仲裁**：否", ""])

    lines.extend(
        [
            "## 给下一棒",
            "",
            "- 本文件由 `python -m tools.rubric_review` 生成，**不**等价于任务审核帽 `task_*_audit_R*.md`；默认与任务审核分目录存放（`docs/diary/jsonPKmermaid/rubric_runs/`）。",
            "",
            "## 给 Cursor",
            "",
            "`rubric_review`、`SILICONFLOW_API_KEY`、双人盲审、仲裁、webhook",
            "",
        ]
    )
    return "\n".join(lines)


def write_reports(
    state: FullReviewState,
    *,
    output_dir: Path,
    stem: str,
    artifact_path: str,
    rubric_path: str,
    backend: str,
    extra: dict[str, Any] | None = None,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"
    rel_json = _json_rel_for_meta(json_path)
    payload = state_to_json_dict(state, extra=extra)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    md = render_markdown(
        state,
        artifact_path=artifact_path,
        rubric_path=rubric_path,
        backend=backend,
        json_rel_path=rel_json,
    )
    md_path.write_text(md, encoding="utf-8")
    return json_path, md_path
