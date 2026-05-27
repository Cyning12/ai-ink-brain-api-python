#!/usr/bin/env python3
"""物化 Wiki-CTX-AB H-lean 臂 payload（README 摘录 + done task 全文 + RECENT 关键词行）。"""
from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HARNESS_README = REPO_ROOT / "docs/harness/README.md"
INVOKES_README = REPO_ROOT / "docs/harness/invokes/README.md"
RECENT = REPO_ROOT / "docs/tasks/RECENT_TASK_SCHEDULE.md"
DEFAULT_OUT = REPO_ROOT / "docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads"
DEFAULT_FREEZE = "WIKI-CTX-AB-REP@2026-05-27"

SLUG_DONE: dict[str, str] = {
    "harness-p1-docs-consolidation": "task_harness_p1_docs_consolidation_v1.md",
    "tech-graph-gate-d-v2-tasks": "task_engineering_tech_graph_gate_d_v2_tasks_v1.md",
    "chatbi-v3-p2-health-ready": "task_chatbi_v3_p2_resilience_health_ready_v1.md",
    "governance-l2-manifest-ci": "task_governance_l2_manifest_ci_v1.md",
    "wiki-ctx-ab-v1": "task_wiki_ctx_ab_v1.md",
    "harness-wiki-loop-t4-l2": "task_harness_wiki_loop_t4_l2_v1.md",
}

SLUG_RECENT_KEYWORDS: dict[str, list[str]] = {
    "harness-p1-docs-consolidation": ["P1-2", "P1-3", "harness-p1", "human_gate"],
    "tech-graph-gate-d-v2-tasks": ["tech-graph", "gate-d", "Gate D", "manifest"],
    "chatbi-v3-p2-health-ready": ["chatbi", "P2-1a", "health", "resilience"],
    "governance-l2-manifest-ci": ["L2", "manifest", "GOV-L2", "_test_manifest"],
    "wiki-ctx-ab-v1": ["Wiki-CTX-AB", "coding_wiki", "T2"],
    "harness-wiki-loop-t4-l2": ["Wiki Loop", "T4", "L2", "wiki-loop"],
}


def _extract_section(text: str, start: str, end_prefixes: tuple[str, ...]) -> str:
    lines = text.splitlines()
    out: list[str] = []
    inside = False
    for line in lines:
        if line.startswith(start):
            inside = True
            out.append(line)
            continue
        if inside and line.startswith("## ") and not line.startswith(start):
            if any(line.startswith(p) for p in end_prefixes):
                break
            if start == "## 1." and line.startswith("## 2."):
                break
        if inside:
            out.append(line)
    return "\n".join(out).strip() + "\n"


def harness_excerpt() -> str:
    text = HARNESS_README.read_text(encoding="utf-8")
    s1 = _extract_section(text, "## 1.", ("## 2.",))
    s21 = _extract_section(text, "### 2.1", ("### 2.2", "## 3."))
    return s1 + "\n" + s21


def invokes_excerpt() -> str:
    text = INVOKES_README.read_text(encoding="utf-8")
    lines = text.splitlines()
    keep: list[str] = []
    for i, line in enumerate(lines):
        if line.startswith("## 命名") or line.startswith("## 目录 taxonomy"):
            keep.extend(lines[i : min(i + 12, len(lines))])
    return "\n".join(keep).strip() + "\n"


def recent_excerpt(slug: str) -> str:
    keywords = SLUG_RECENT_KEYWORDS.get(slug, [slug])
    lines = RECENT.read_text(encoding="utf-8").splitlines()
    picked: list[str] = []
    for line in lines:
        if any(k.lower() in line.lower() for k in keywords):
            picked.append(line)
    if not picked:
        picked = lines[:8]
    return "\n".join(picked[:40]).strip() + "\n"


def materialize(
    slug: str,
    *,
    out_dir: Path = DEFAULT_OUT,
    freeze_id: str = DEFAULT_FREEZE,
) -> Path:
    if slug not in SLUG_DONE:
        raise KeyError(f"unknown slug: {slug}")

    done_path = REPO_ROOT / "docs/tasks/done" / SLUG_DONE[slug]
    if not done_path.is_file():
        raise FileNotFoundError(done_path)

    parts: list[str] = []
    parts.append(f"--- FILE: docs/harness/README.md ---\n{harness_excerpt()}")
    parts.append(f"--- FILE: docs/harness/invokes/README.md ---\n{invokes_excerpt()}")
    parts.append(
        f"--- FILE: docs/tasks/done/{SLUG_DONE[slug]} ---\n"
        f"{done_path.read_text(encoding='utf-8').rstrip()}\n"
    )
    parts.append(f"--- FILE: docs/tasks/RECENT_TASK_SCHEDULE.md ---\n{recent_excerpt(slug)}")

    body = "\n".join(parts)
    total = len(body)

    header = f"""# Payload · H-lean（Representative 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `H-lean` |
| **task_slug** | `{slug}` |
| **freeze_id** | `{freeze_id}` |
| **generated** | 2026-05-27 · `python tools/wiki_ctx_ab_materialize_h_lean.py` |

## Agent 约束

只能依据下文作答。禁止 invoke/review 全文。禁止 `docs/coding_wiki/*`。

---

## 载荷正文

"""
    footer = f"""
---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | {total} |
| `file_count` | 4 |
| `notes` | H-lean：README §1+§2.1 + invokes README 摘录 + done task 全文 + RECENT 关键词行 |
"""
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"H-lean_{slug}.md"
    out.write_text(header + body + footer, encoding="utf-8")
    print(f"{out.relative_to(REPO_ROOT)}  payload_char_count={total}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Wiki-CTX-AB H-lean payload")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--freeze-id", default=DEFAULT_FREEZE)
    args = parser.parse_args()
    materialize(args.slug, out_dir=args.out_dir, freeze_id=args.freeze_id)


if __name__ == "__main__":
    main()
