#!/usr/bin/env python3
"""Harness task 状态 JSON（human_gate · 元信息 · validate 摘要）。

真值：docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §5（O5）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# 同目录 tools 模块（复用 R1 validate · human_gate 解析）
_TOOLS = Path(__file__).resolve().parent
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import harness_human_gate_check as hhg  # noqa: E402
import harness_task_validate as htv  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
HAT_FLOW = ("22", "30", "40", "50", "CLOSE")

GATE_ROW = re.compile(
    r"^\|\s*(HG-[A-Z0-9-]+)\s*\|\s*(pending|approved)\s*\|\s*([^|]+)\|",
    re.I | re.M,
)


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def parse_gate_rows(text: str) -> list[dict[str, object]]:
    gates: list[dict[str, object]] = []
    for m in GATE_ROW.finditer(text):
        blocks = [b.strip() for b in m.group(3).split(",") if b.strip()]
        gates.append(
            {
                "gate_id": m.group(1),
                "status": m.group(2).lower(),
                "blocks_hats": blocks,
            }
        )
    return gates


def _hat_blocked(hat: str, gates: list[dict[str, object]]) -> bool:
    for gate in gates:
        if gate["status"] != "pending":
            continue
        for block in gate["blocks_hats"]:
            token = str(block)
            if token == hat or token.startswith(f"{hat}-") or token.startswith(hat):
                return True
    return False


def suggested_next_hat(gates: list[dict[str, object]]) -> str | None:
    for hat in HAT_FLOW:
        if not _hat_blocked(hat, gates):
            return hat
    return None


def build_status(task_path: Path) -> dict[str, object]:
    text = htv._read(task_path)
    meta = htv._meta_fields(text)
    gates = parse_gate_rows(text)
    pending = [g for g in gates if g["status"] == "pending"]

    # 继承母闸：合并母单 gate 行（与 harness_human_gate_check 一致）
    for mother in hhg.mother_task_paths(task_path, text):
        if mother.is_file():
            for mg in parse_gate_rows(htv._read(mother)):
                if mg["gate_id"] not in {g["gate_id"] for g in gates}:
                    gates.append(mg)
                elif mg["status"] == "pending":
                    pending.append(mg)

    validation = htv.validate_file(task_path)
    blocked_hats = sorted(
        {
            block
            for gate in pending
            for block in gate["blocks_hats"]
        }
    )

    return {
        "task_path": _rel(task_path),
        "task_slug": meta.get("task_slug", ""),
        "freeze_id": meta.get("freeze_id", ""),
        "meta": {
            "test_strategy": meta.get("test_strategy", ""),
            "test_strategy_note": meta.get("test_strategy_note", ""),
            "semi_auto": meta.get("semi_auto", "").lower() == "true",
            "audit_profile": meta.get("audit_profile", ""),
            "git_branch": meta.get("git_branch", ""),
        },
        "human_gates": gates,
        "pending_gates": pending,
        "blocked_hats": blocked_hats,
        "suggested_next_hat": suggested_next_hat(gates),
        "validate": {
            "ok": validation.ok,
            "error_count": len(validation.errors),
            "warning_count": len(validation.warnings),
            "errors": [htv.asdict(f) for f in validation.errors],
            "warnings": [htv.asdict(f) for f in validation.warnings],
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Harness task 状态 JSON")
    parser.add_argument(
        "--task",
        required=True,
        help="task 文件路径",
    )
    parser.add_argument("--json", action="store_true", help="JSON 输出（默认即 JSON）")
    args = parser.parse_args(argv)

    task_path = (REPO_ROOT / args.task).resolve() if not Path(args.task).is_absolute() else Path(args.task)
    if not task_path.is_file():
        print(f"harness_change_status: file not found: {task_path}", file=sys.stderr)
        return 1

    payload = build_status(task_path)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
