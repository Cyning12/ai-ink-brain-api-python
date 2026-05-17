from __future__ import annotations

"""
graph_v2 等价检查（P2-0 草案）。

对照：自 *.ai.md 构建的参考 v2 vs 已提交 graph.json。
退出码：
- 0：通过
- 2：FP-1 输入/解析失败
- 3：FP-3 阈值未达或 schema 不符
- 5：FP-5 已提交图为 graph_v1（须先 P2-1 导出升版，禁止静默当 v2 用）
"""

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.tech_graph_graph_export import REPO_ROOT, TechGraphParseError
from tools.tech_graph_graph_v2_reference import build_reference_graph_v2
from tools.tech_graph_graph_v2_schema import (
    SCHEMA_VERSION_V2,
    GraphV2SchemaError,
    validate_graph_v2,
)

DEFAULT_INPUT = REPO_ROOT / "docs" / "_tech_graph"
DEFAULT_GRAPH = REPO_ROOT / "docs" / "_tech_graph" / "graph.json"

ANCHOR_COVERAGE_MIN = 0.95
EDGE_LABEL_COVERAGE_MIN = 0.90


@dataclass(frozen=True)
class EquivalenceMetrics:
    anchor_coverage: float
    edge_label_coverage: float
    topology_ok: bool
    missing_anchor_edges: list[str]
    missing_labels: list[str]


def _stderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def _edge_topology_key(e: dict[str, Any]) -> tuple[str, str, str]:
    return (e["from"], e["to"], e.get("mark", ""))


def _topology_edge_set(graph: dict[str, Any]) -> set[tuple[str, str, str]]:
    return {_edge_topology_key(e) for e in graph.get("edges") or []}


def _node_id_set(graph: dict[str, Any]) -> set[str]:
    nodes = graph.get("nodes") or []
    if nodes and isinstance(nodes[0], str):
        return set(nodes)
    return {n["id"] for n in nodes if isinstance(n, dict)}


def _anchor_keys(anchors: list[dict[str, Any]]) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for a in anchors:
        out.add((a.get("path", ""), a.get("symbol", "")))
    return out


def compute_equivalence_metrics(
    reference: dict[str, Any],
    exported: dict[str, Any],
) -> EquivalenceMetrics:
    ref_edges = reference.get("edges") or []
    exp_edges = exported.get("edges") or []

    ref_by_topo: dict[tuple[str, str, str], dict[str, Any]] = {}
    for e in ref_edges:
        ref_by_topo[_edge_topology_key(e)] = e

    exp_by_topo: dict[tuple[str, str, str], dict[str, Any]] = {}
    for e in exp_edges:
        exp_by_topo[_edge_topology_key(e)] = e

    topology_ok = _node_id_set(reference) == _node_id_set(exported) and set(
        ref_by_topo.keys()
    ) == set(exp_by_topo.keys())

    ref_with_anchor = [e for e in ref_edges if e.get("anchors")]
    matched_anchor = 0
    missing_anchor_edges: list[str] = []

    for re_ in ref_with_anchor:
        key = _edge_topology_key(re_)
        ee = exp_by_topo.get(key)
        if ee is None:
            missing_anchor_edges.append(f"{key[0]}->{key[1]} mark={key[2]!r}")
            continue
        ref_a = _anchor_keys(re_.get("anchors") or [])
        exp_a = _anchor_keys(ee.get("anchors") or [])
        if ref_a <= exp_a:
            matched_anchor += 1
        else:
            missing_anchor_edges.append(
                f"{key[0]}->{key[1]} missing={sorted(ref_a - exp_a)[:3]}"
            )

    anchor_coverage = (
        1.0 if not ref_with_anchor else matched_anchor / len(ref_with_anchor)
    )

    ref_semantic = [e for e in ref_edges if (e.get("label") or "").strip()]
    matched_label = 0
    missing_labels: list[str] = []

    for re_ in ref_semantic:
        key = _edge_topology_key(re_)
        ee = exp_by_topo.get(key)
        if ee is None:
            missing_labels.append(f"{key[0]}->{key[1]}")
            continue
        if (ee.get("label") or "").strip() == (re_.get("label") or "").strip():
            matched_label += 1
        else:
            missing_labels.append(f"{key[0]}->{key[1]} exp_label={ee.get('label')!r}")

    edge_label_coverage = (
        1.0 if not ref_semantic else matched_label / len(ref_semantic)
    )

    return EquivalenceMetrics(
        anchor_coverage=anchor_coverage,
        edge_label_coverage=edge_label_coverage,
        topology_ok=topology_ok,
        missing_anchor_edges=missing_anchor_edges[:20],
        missing_labels=missing_labels[:20],
    )


def run_equivalence_check(
    *,
    input_root: Path,
    graph_path: Path,
    freeze_id: str,
    require_v2: bool = True,
) -> int:
    if not graph_path.is_file():
        _stderr(f"FP-3: graph.json 缺失：{graph_path}")
        return 3

    try:
        exported = json.loads(graph_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _stderr(f"FP-3: graph.json 解析失败：{exc}")
        return 3

    if not isinstance(exported, dict):
        _stderr("FP-3: graph.json 根须为 object")
        return 3

    ver = exported.get("schema_version")
    if ver != SCHEMA_VERSION_V2:
        if require_v2:
            _stderr(
                f"FP-5: 已提交 schema_version={ver!r}，非 graph_v2；"
                "须 P2-1 导出升版后再跑等价检查（禁止静默整包 v1 作 v2）"
            )
            return 5
        _stderr(f"跳过等价：schema_version={ver!r}")

    try:
        validate_graph_v2(exported)
    except GraphV2SchemaError as exc:
        _stderr(f"FP-3: 导出图 schema 校验失败：{exc}")
        return 3

    gen = exported.get("generated_at")
    if not isinstance(gen, str):
        _stderr("FP-3: exported.generated_at 缺失")
        return 3

    try:
        reference = build_reference_graph_v2(
            input_root, generated_at=gen, freeze_id=freeze_id
        )
    except TechGraphParseError as exc:
        _stderr(f"FP-1: {exc.path}:{exc.line_no}: {exc.message}")
        return 2
    except FileNotFoundError as exc:
        _stderr(f"FP-1: 输入目录不存在：{exc}")
        return 2

    metrics = compute_equivalence_metrics(reference, exported)
    problems: list[str] = []

    if not metrics.topology_ok:
        problems.append("topology_mismatch")
    if metrics.anchor_coverage < ANCHOR_COVERAGE_MIN:
        problems.append(
            f"anchor_coverage={metrics.anchor_coverage:.3f} < {ANCHOR_COVERAGE_MIN}"
        )
    if metrics.edge_label_coverage < EDGE_LABEL_COVERAGE_MIN:
        problems.append(
            f"edge_label_coverage={metrics.edge_label_coverage:.3f} "
            f"< {EDGE_LABEL_COVERAGE_MIN}"
        )

    if problems:
        _stderr("FP-3: 等价检查未通过：\n- " + "\n- ".join(problems))
        if metrics.missing_anchor_edges:
            _stderr(
                "missing_anchors_sample: "
                + "; ".join(metrics.missing_anchor_edges[:5])
            )
        if metrics.missing_labels:
            _stderr(
                "missing_labels_sample: " + "; ".join(metrics.missing_labels[:5])
            )
        return 3

    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="graph_v2 参考图 vs 已提交 graph.json 等价检查（P2-0）"
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    parser.add_argument(
        "--freeze-id",
        default="TECH_GRAPH_S2_FREEZE_20260517_V2_0",
        help="参考图 freeze_id（与导出对齐）",
    )
    parser.add_argument(
        "--allow-v1",
        action="store_true",
        help="允许 graph_v1（仅 pytest；生产 CI 勿用）",
    )
    args = parser.parse_args(argv)

    input_root = (
        (REPO_ROOT / args.input).resolve()
        if not args.input.is_absolute()
        else args.input
    )
    graph_path = (
        (REPO_ROOT / args.graph).resolve()
        if not args.graph.is_absolute()
        else args.graph
    )

    return run_equivalence_check(
        input_root=input_root,
        graph_path=graph_path,
        freeze_id=args.freeze_id,
        require_v2=not args.allow_v1,
    )


if __name__ == "__main__":
    raise SystemExit(main())
