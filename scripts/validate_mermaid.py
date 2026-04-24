#!/usr/bin/env python3
"""
Mermaid 拓扑协议验证脚本
检查 .ai.md 文件是否符合拓扑协议规范

用法:
    python scripts/validate_mermaid.py [文件路径...]
    无参数时默认检查 docs/_tech_graph/*.ai.md
"""

import re
import sys
from pathlib import Path


def extract_mermaid_blocks(filepath: str) -> list[str]:
    """从 markdown 文件提取 mermaid 代码块"""
    with open(filepath) as f:
        content = f.read()

    blocks = []
    in_mermaid = False
    current = []

    for line in content.split("\n"):
        if line.strip() == "```mermaid":
            in_mermaid = True
            current = []
        elif line.strip() == "```" and in_mermaid:
            in_mermaid = False
            blocks.append("\n".join(current))
            current = []
        elif in_mermaid:
            current.append(line)

    return blocks


def validate_mermaid(text: str, filename: str) -> tuple[list[str], list[str]]:
    """验证拓扑协议合规性，返回 (errors, warnings)"""
    errors = []
    warnings = []
    lines = text.split("\n")

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        if not stripped or stripped.startswith("%%"):
            continue
        if stripped.startswith("classDef") or stripped.startswith("class "):
            continue
        if stripped.startswith("subgraph") or stripped == "end":
            continue

        # 检查裸边（没有引号的 -->）
        if "-->" in stripped and not ('--"' in stripped or "-.->" in stripped):
            errors.append(f"  行{i}: 裸边（无引号标记）-> {stripped[:60]}")

        # 检查锚点格式
        if "// →" in stripped:
            if not re.match(r"\s*// → [\w/]+\.(py|sql|md)(#[L\d]+|::[\w_]+)?", stripped):
                warnings.append(f"  行{i}: 锚点格式非标准 -> {stripped[:60]}")

    # 检查是否有锚点
    has_anchor = any("// →" in l for l in lines)
    if not has_anchor:
        warnings.append("  无锚点注释（建议添加代码位置链接）")

    # 检查异步节点：[[async def ...]] 且作为边的起点时，应该用 ~>
    # 但 ::yields / ::branches / ::merges 等元关系边除外
    for line in lines:
        match = re.search(r"(\w+)\[\[async def", line)
        if match:
            node_id = match.group(1)
            for edge_line in lines:
                edge_match = re.search(rf"{node_id}\s+--\"([^\"]+)\"-->", edge_line)
                if edge_match:
                    marker = edge_match.group(1)
                    if marker.startswith("::"):
                        continue
                    if marker == "->":
                        errors.append(
                            f"  异步节点 {node_id} 用了同步边 '->'，应改为 '~>'"
                        )

    return errors, warnings


def main() -> int:
    project_root = Path(__file__).parent.parent
    default_files = list((project_root / "docs" / "_tech_graph").glob("*.ai.md"))

    files = sys.argv[1:] if len(sys.argv) > 1 else [str(f) for f in default_files]

    total_errors = 0
    total_warnings = 0

    for filepath in files:
        path = Path(filepath)
        print(f"\n{'='*60}")
        print(f"📄 {path.name}")
        print("=" * 60)

        if not path.exists():
            print(f"  ❌ 文件不存在")
            total_errors += 1
            continue

        blocks = extract_mermaid_blocks(str(path))

        if not blocks:
            print("  ⚠️ 未找到 mermaid 代码块")
            continue

        for idx, block in enumerate(blocks, 1):
            print(f"\n  📊 图 {idx} ({len(block.split(chr(10)))} 行):")

            errors, warnings = validate_mermaid(block, str(path))

            if errors:
                print(f"    ❌ 错误 ({len(errors)}):")
                for e in errors:
                    print(f"      {e}")
                total_errors += len(errors)
            else:
                print(f"    ✅ 无错误")

            if warnings:
                print(f"    ⚠️ 警告 ({len(warnings)}):")
                for w in warnings:
                    print(f"      {w}")
                total_warnings += len(warnings)
            else:
                print(f"    ✅ 无警告")

    print(f"\n{'='*60}")
    print(f"总计: {len(files)} 个文件, {total_errors} 错误, {total_warnings} 警告")
    print("=" * 60)

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
