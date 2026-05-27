#!/usr/bin/env python3
"""物化 Wiki-CTX-AB P2 · W 臂 payload（index + syntheses/{slug}.md）。"""
from __future__ import annotations

import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SLUG = "harness-p1-docs-consolidation"
DEFAULT_OUT_DIR = REPO_ROOT / "docs/harness/experiments/wiki_ctx_ab_v1/payloads"
DEFAULT_FREEZE_ID = "WIKI-CTX-AB@2026-05-25"


def materialize(
    slug: str,
    *,
    out_dir: Path = DEFAULT_OUT_DIR,
    freeze_id: str = DEFAULT_FREEZE_ID,
) -> Path:
    files = [
        REPO_ROOT / "docs/coding_wiki/index.md",
        REPO_ROOT / f"docs/coding_wiki/syntheses/{slug}.md",
    ]
    for p in files:
        if not p.is_file():
            raise FileNotFoundError(p)

    parts: list[str] = []
    total = 0
    for p in files:
        rel = p.relative_to(REPO_ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        block = f"--- FILE: {rel} ---\n{text.rstrip()}\n"
        parts.append(block)
        total += len(block)

    body = "\n".join(parts)
    header = f"""# Payload · W（P2 物化实例 · 自动生成）

| 元信息 | 值 |
| --- | --- |
| **arm** | `W` |
| **task_slug** | `{slug}` |
| **freeze_id** | `{freeze_id}` |
| **generated** | 见运行日 · `python tools/wiki_ctx_ab_materialize_w.py` |

## Agent 约束

只能依据下文作答；**禁止** `docs/harness/`、`docs/tasks/done/` 全文、invoke/review。

---

## 载荷正文

"""
    footer = f"""
---

## 物化后统计

| 字段 | 值 |
| --- | --- |
| `payload_char_count` | {total} |
| `file_count` | {len(files)} |
| `notes` | P2 仅 Wiki：`index.md` + `syntheses/{slug}.md` |
"""
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"W_{slug}.md"
    out.write_text(header + body + footer, encoding="utf-8")
    print(f"{out.relative_to(REPO_ROOT)}  payload_char_count={total}")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Materialize Wiki-CTX-AB W arm payload")
    parser.add_argument("--slug", default=DEFAULT_SLUG)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help="Output directory for W_<slug>.md",
    )
    parser.add_argument(
        "--freeze-id",
        default=DEFAULT_FREEZE_ID,
        help="freeze_id in payload header",
    )
    args = parser.parse_args()
    materialize(args.slug, out_dir=args.out_dir, freeze_id=args.freeze_id)


if __name__ == "__main__":
    main()
