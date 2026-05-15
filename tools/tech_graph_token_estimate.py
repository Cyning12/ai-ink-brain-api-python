from __future__ import annotations

"""
闸口 A 附录：估算「代号 A」graph.json 与「代号 B」等价 Mermaid 源文的上下文体量对比。

规则（须与 gate_a_scheme1_backend.md §3「Agent/LM context」一致写进 PR/闸口表）：
- **bytes_utf8**：UTF-8 编码字节数（与传输/存储口径一致）。
- **chars**：Python 字符串长度（Unicode 码位计数）。
- **heuristic_tokens**：`max(1, chars // 4)`，**非** OpenAI 官方 cl100k_base；仅作 A/B **同规则**相对比较。

与 `tech_graph_graph_export.py` / `tech_graph_contract_check.py` **并行**，禁止合并契约逻辑。
"""

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_INPUT = REPO_ROOT / "docs" / "_tech_graph"
DEFAULT_GRAPH = REPO_ROOT / "docs" / "_tech_graph" / "graph.json"
MERMAID_FENCE = re.compile(r"```\s*mermaid\s*\n([\s\S]*?)```", re.IGNORECASE)


def _iter_ai_md_files(input_root: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(input_root.glob("*.ai.md")):
        if p.name.startswith("99_"):
            continue
        out.append(p)
    return out


def _repo_rel_posix(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def collect_mermaid_corpus(input_root: Path) -> str:
    """代号 B：与导出脚本同扫描范围，拼接所有 mermaid fence 正文（顺序：文件名排序）。"""
    parts: list[str] = []
    for path in _iter_ai_md_files(input_root):
        text = path.read_text(encoding="utf-8")
        for m in MERMAID_FENCE.finditer(text):
            body = m.group(1).strip()
            if body:
                parts.append(body)
    return "\n\n".join(parts)


def measure(label: str, s: str) -> dict[str, int | str]:
    raw = s.encode("utf-8")
    chars = len(s)
    heur = max(1, chars // 4)
    return {
        "label": label,
        "bytes_utf8": len(raw),
        "chars": chars,
        "heuristic_tokens": heur,
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="估算 graph.json（A）与 .ai.md 内 Mermaid 拼接（B）的 token 粗估对比。"
    )
    p.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="含 *.ai.md 的目录（默认 docs/_tech_graph）")
    p.add_argument(
        "--graph-json",
        type=Path,
        default=DEFAULT_GRAPH,
        help="graph.json 路径（默认 docs/_tech_graph/graph.json）",
    )
    p.add_argument("--json", action="store_true", help="打印一行 JSON（便于 CI 采集）")
    args = p.parse_args(argv)

    input_root = (REPO_ROOT / args.input).resolve() if not args.input.is_absolute() else args.input
    graph_path = (REPO_ROOT / args.graph_json).resolve() if not args.graph_json.is_absolute() else args.graph_json

    if not input_root.is_dir():
        print(f"输入目录不存在：{input_root}", file=sys.stderr)
        return 2
    if not graph_path.is_file():
        print(f"graph.json 不存在：{graph_path}", file=sys.stderr)
        return 2

    a_text = graph_path.read_text(encoding="utf-8")
    b_text = collect_mermaid_corpus(input_root)

    ma = measure("A_graph_json", a_text)
    mb = measure("B_mermaid_corpus", b_text)

    ratio_bytes = round(mb["bytes_utf8"] / max(1, int(ma["bytes_utf8"])), 4)
    ratio_heur = round(mb["heuristic_tokens"] / max(1, int(ma["heuristic_tokens"])), 4)

    out = {
        "schema": "tech_graph_token_estimate_v1",
        "input_root": _repo_rel_posix(input_root),
        "graph_json": _repo_rel_posix(graph_path),
        "A": {k: v for k, v in ma.items() if k != "label"},
        "B": {k: v for k, v in mb.items() if k != "label"},
        "ratio_B_per_A": {"bytes_utf8": ratio_bytes, "heuristic_tokens": ratio_heur},
        "rules": {
            "heuristic_tokens": "chars//4, min 1; not official tiktoken",
        },
    }

    if args.json:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print("| 代号 | bytes_utf8 | chars | heuristic_tokens (chars//4) |")
        print("| --- | ---:| ---:| ---:|")
        print(f"| A `graph.json` | {ma['bytes_utf8']} | {ma['chars']} | {ma['heuristic_tokens']} |")
        print(f"| B Mermaid 拼接 | {mb['bytes_utf8']} | {mb['chars']} | {mb['heuristic_tokens']} |")
        print(f"| B/A 比值 | {ratio_bytes} | — | {ratio_heur} |")
        print("\n规则：heuristic_tokens 仅为同口径相对比较，见脚本 docstring。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
