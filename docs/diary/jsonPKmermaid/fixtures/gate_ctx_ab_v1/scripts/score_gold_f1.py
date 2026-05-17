#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对 gate_ctx_ab S0 raw jsonl 按 tasks.json gold 计算 entrypoints / impacts 的 P/R/F1。

用法：
  python …/score_gold_f1.py --batch-dir docs/diary/jsonPKmermaid/runs/gate_ctx_ab_v1_batch_20260516_111037
  python …/score_gold_f1.py --runs-root docs/diary/jsonPKmermaid/runs   # 扫描所有 *batch* 目录
  python …/score_gold_f1.py --jsonl path/to/raw/*.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve()
FIXTURE_ROOT = _REPO.parents[1]
REPO_ROOT = _REPO.parents[6]
DEFAULT_TASKS = FIXTURE_ROOT / "tasks.json"
DEFAULT_RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"
REPORTS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "reports"


def _norm_path(p: str) -> str:
    return (p or "").strip().replace("\\", "/").rstrip("/")


def _text_blob(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        parts: list[str] = []
        for k, v in obj.items():
            parts.append(str(k))
            parts.append(_text_blob(v))
        return " ".join(parts)
    if isinstance(obj, list):
        return " ".join(_text_blob(x) for x in obj)
    return str(obj)


@dataclass
class ScoreCounts:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    @property
    def precision(self) -> float | None:
        if self.tp + self.fp == 0:
            return None
        return self.tp / (self.tp + self.fp)

    @property
    def recall(self) -> float | None:
        if self.tp + self.fn == 0:
            return None
        return self.tp / (self.tp + self.fn)

    @property
    def f1(self) -> float | None:
        p, r = self.precision, self.recall
        if p is None or r is None or (p + r) == 0:
            return None
        return 2 * p * r / (p + r)


@dataclass
class RecordScore:
    file: str
    task_id: str
    arm: str
    status: str
    parse_ok: bool
    entrypoints: ScoreCounts = field(default_factory=ScoreCounts)
    impacts: ScoreCounts = field(default_factory=ScoreCounts)
    gold_entry_hits: list[str] = field(default_factory=list)
    gold_entry_misses: list[str] = field(default_factory=list)


def _load_tasks(path: Path) -> dict[str, dict[str, Any]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    return {t["task_id"]: t for t in doc.get("tasks", [])}


def _collect_graph_refs(response: dict[str, Any]) -> set[str]:
    refs: set[str] = set()
    for ev in response.get("evidence") or []:
        if not isinstance(ev, dict):
            continue
        ref = str(ev.get("ref") or ev.get("graph_id") or "").strip()
        if ref:
            refs.add(ref.upper())
    for key in ("entrypoints", "impacts"):
        for item in response.get(key) or []:
            if isinstance(item, dict):
                gid = item.get("graph_id")
                if gid:
                    refs.add(str(gid).strip().upper())
    return refs


def _entrypoint_pred_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    items = [x for x in (response.get("entrypoints") or []) if isinstance(x, dict)]
    return items


def _impact_pred_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    items = [x for x in (response.get("impacts") or []) if isinstance(x, dict)]
    return items


def _gold_entry_label(g: dict[str, Any]) -> str:
    parts = [_norm_path(g.get("path") or "")]
    if g.get("symbol"):
        parts.append(str(g["symbol"]))
    if g.get("graph_id"):
        parts.append(f"#{g['graph_id']}")
    return " ".join(p for p in parts if p)


def _match_entrypoint_gold(gold: dict[str, Any], response: dict[str, Any]) -> bool:
    g_path = _norm_path(gold.get("path") or "")
    g_sym = (gold.get("symbol") or "").strip()
    g_gid = (gold.get("graph_id") or "")
    g_gid_u = g_gid.strip().upper() if g_gid else ""

    graph_refs = _collect_graph_refs(response)
    if g_gid_u and g_gid_u in graph_refs:
        return True

    blob = _text_blob(response)
    if g_path and g_path in blob:
        return True

    for pred in _entrypoint_pred_items(response):
        p_path = _norm_path(pred.get("path") or "")
        p_sym = (pred.get("symbol") or "").strip()
        if g_path and p_path == g_path:
            return True
        if g_sym and p_sym and g_sym == p_sym:
            return True
        if g_path and g_path in p_path:
            return True

    return False


def _match_impact_gold(gold: dict[str, Any], response: dict[str, Any]) -> bool:
    g_path = _norm_path(gold.get("path") or "")
    g_kind = (gold.get("kind") or "").strip().lower()
    g_gid = (gold.get("graph_id") or "")
    g_gid_u = g_gid.strip().upper() if g_gid else ""

    graph_refs = _collect_graph_refs(response)
    if g_gid_u and g_gid_u in graph_refs:
        return True

    for pred in _impact_pred_items(response):
        p_path = _norm_path(pred.get("path") or "")
        p_kind = (pred.get("kind") or "").strip().lower()
        desc = _text_blob(pred)
        path_ok = bool(g_path) and (p_path == g_path or g_path in p_path or g_path in desc)
        kind_ok = bool(g_kind) and g_kind == p_kind
        if path_ok and (not g_kind or kind_ok):
            return True
        if kind_ok and not g_path:
            return True

    blob = _text_blob(response)
    if g_path and g_path in blob:
        if not g_kind or g_kind in blob.lower():
            return True
    return False


def _pred_entry_matches_gold(pred: dict[str, Any], gold_list: list[dict[str, Any]], response: dict[str, Any]) -> bool:
    """预测 entrypoint 是否命中任一 gold（用于 precision）。"""
    p_path = _norm_path(pred.get("path") or "")
    p_sym = (pred.get("symbol") or "").strip()
    for g in gold_list:
        g_path = _norm_path(g.get("path") or "")
        g_sym = (g.get("symbol") or "").strip()
        if p_path and g_path and (p_path == g_path or g_path in p_path or p_path in g_path):
            return True
        if p_sym and g_sym and p_sym == g_sym:
            return True
    # symbol/path 在 evidence 里指向 gold path
    blob = _text_blob(response)
    if p_path and any(_norm_path(g.get("path") or "") in p_path for g in gold_list):
        return True
    if p_sym and p_sym in blob and any((g.get("symbol") or "") == p_sym for g in gold_list):
        return True
    return False


def _pred_impact_matches_gold(pred: dict[str, Any], gold_list: list[dict[str, Any]]) -> bool:
    p_path = _norm_path(pred.get("path") or "")
    p_kind = (pred.get("kind") or "").strip().lower()
    desc = _text_blob(pred)
    for g in gold_list:
        g_path = _norm_path(g.get("path") or "")
        g_kind = (g.get("kind") or "").strip().lower()
        path_ok = bool(g_path) and (p_path == g_path or g_path in p_path or g_path in desc)
        kind_ok = bool(g_kind) and g_kind == p_kind
        if path_ok and (not g_kind or kind_ok):
            return True
        if kind_ok and not g_path:
            return True
    return False


def score_record(record: dict[str, Any], task: dict[str, Any]) -> RecordScore:
    gold = task.get("gold") or {}
    gold_eps = list(gold.get("entrypoints") or [])
    gold_imps = list(gold.get("impacts") or [])
    response = record.get("response") if isinstance(record.get("response"), dict) else {}

    rs = RecordScore(
        file=str(record.get("file") or ""),
        task_id=str(record.get("task_id") or task.get("task_id") or ""),
        arm=str(record.get("arm") or ""),
        status=str(record.get("status") or ""),
        parse_ok=bool(record.get("parse_ok")),
    )

    if not record.get("parse_ok") or record.get("status") != "ok":
        rs.entrypoints.fn = len(gold_eps)
        rs.impacts.fn = len(gold_imps)
        for g in gold_eps:
            rs.gold_entry_misses.append(_gold_entry_label(g))
        return rs

    # entrypoints: recall on gold
    for g in gold_eps:
        label = _gold_entry_label(g)
        if _match_entrypoint_gold(g, response):
            rs.entrypoints.tp += 1
            rs.gold_entry_hits.append(label)
        else:
            rs.entrypoints.fn += 1
            rs.gold_entry_misses.append(label)

    preds_ep = _entrypoint_pred_items(response)
    for pred in preds_ep:
        if _pred_entry_matches_gold(pred, gold_eps, response):
            continue
        rs.entrypoints.fp += 1

    # impacts: recall on gold
    for g in gold_imps:
        if _match_impact_gold(g, response):
            rs.impacts.tp += 1
        else:
            rs.impacts.fn += 1

    for pred in _impact_pred_items(response):
        if _pred_impact_matches_gold(pred, gold_imps):
            continue
        rs.impacts.fp += 1

    return rs


def _load_jsonl(path: Path) -> dict[str, Any]:
    line = path.read_text(encoding="utf-8").strip().splitlines()[0]
    return json.loads(line)


def _iter_jsonl_paths(
    *,
    batch_dir: Path | None,
    runs_root: Path | None,
    jsonl_paths: list[Path],
) -> list[Path]:
    out: list[Path] = list(jsonl_paths)
    if batch_dir:
        out.extend(sorted(batch_dir.glob("round_*/raw/*_S0.jsonl")))
    if runs_root:
        for d in sorted(runs_root.iterdir()):
            if d.is_dir() and "batch" in d.name:
                out.extend(sorted(d.glob("round_*/raw/*_S0.jsonl")))
    # 去重
    seen: set[str] = set()
    unique: list[Path] = []
    for p in out:
        key = str(p.resolve())
        if key not in seen:
            seen.add(key)
            unique.append(p)
    return unique


def _f1_fmt(x: float | None) -> str:
    return "—" if x is None else f"{x:.3f}"


def _aggregate_by_arm_task(scores: list[RecordScore]) -> dict[str, Any]:
    """按 task_id + arm 聚合 macro F1（对各条记录 F1 取平均）。"""
    from collections import defaultdict

    buckets: dict[tuple[str, str], list[RecordScore]] = defaultdict(list)
    for s in scores:
        buckets[(s.task_id, s.arm)].append(s)

    agg: dict[str, Any] = {}
    for (task_id, arm), rows in sorted(buckets.items()):
        ep_f1s: list[float] = []
        im_f1s: list[float] = []
        for r in rows:
            if r.entrypoints.f1 is not None:
                ep_f1s.append(r.entrypoints.f1)
            if r.impacts.f1 is not None:
                im_f1s.append(r.impacts.f1)
        agg[f"{task_id}|{arm}"] = {
            "task_id": task_id,
            "arm": arm,
            "n_records": len(rows),
            "entrypoints_f1_mean": sum(ep_f1s) / len(ep_f1s) if ep_f1s else None,
            "impacts_f1_mean": sum(im_f1s) / len(im_f1s) if im_f1s else None,
            "entrypoints_recall_mean": sum(r.entrypoints.recall or 0 for r in rows) / len(rows),
            "impacts_recall_mean": sum(r.impacts.recall or 0 for r in rows) / len(rows),
        }
    return agg


def _render_markdown(
    scores: list[RecordScore],
    agg: dict[str, Any],
    *,
    source_label: str,
) -> str:
    lines = [
        f"# gate_ctx_ab gold F1 — {source_label}",
        "",
        "> entrypoints：path / symbol / graph_id（evidence）任一命中 gold 即 TP。",
        "> impacts：path（含 description）+ kind 与 graph_id（evidence）启发式匹配。",
        "",
        "## 逐条记录",
        "",
        "| jsonl | task | arm | ep P/R/F1 | imp P/R/F1 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for s in scores:
        ep, im = s.entrypoints, s.impacts
        ep_cell = f"{_f1_fmt(ep.precision)}/{_f1_fmt(ep.recall)}/{_f1_fmt(ep.f1)}"
        im_cell = f"{_f1_fmt(im.precision)}/{_f1_fmt(im.recall)}/{_f1_fmt(im.f1)}"
        rel = Path(s.file).name if s.file else "—"
        lines.append(f"| `{rel}` | `{s.task_id}` | `{s.arm}` | {ep_cell} | {im_cell} |")

    lines.extend(["", "## 按 task × arm 均值（F1）", "", "| task | arm | n | entrypoints F1 | impacts F1 |", "| --- | --- | ---:| ---:| ---:|"])
    for _k, v in sorted(agg.items()):
        lines.append(
            f"| `{v['task_id']}` | `{v['arm']}` | {v['n_records']} | "
            f"{_f1_fmt(v.get('entrypoints_f1_mean'))} | {_f1_fmt(v.get('impacts_f1_mean'))} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="gate_ctx_ab gold F1 计分")
    p.add_argument("--tasks", type=Path, default=DEFAULT_TASKS)
    p.add_argument("--batch-dir", type=Path, default=None, help="单个 batch 目录")
    p.add_argument("--runs-root", type=Path, default=None, help="扫描其下所有 *batch* 目录")
    p.add_argument("--jsonl", type=Path, action="append", default=[], help="可多次指定 jsonl")
    p.add_argument("--out-json", type=Path, default=None)
    p.add_argument("--out-md", type=Path, default=None)
    args = p.parse_args()

    tasks = _load_tasks(args.tasks)
    paths = _iter_jsonl_paths(
        batch_dir=args.batch_dir,
        runs_root=args.runs_root or (DEFAULT_RUNS_ROOT if not args.batch_dir and not args.jsonl else None),
        jsonl_paths=args.jsonl,
    )
    if not paths:
        print("未找到 jsonl；请指定 --batch-dir / --runs-root / --jsonl", file=sys.stderr)
        return 2

    scores: list[RecordScore] = []
    for jp in paths:
        rec = _load_jsonl(jp)
        try:
            rec.setdefault("file", str(jp.resolve().relative_to(REPO_ROOT.resolve())))
        except ValueError:
            rec.setdefault("file", str(jp))
        task_id = rec.get("task_id") or rec.get("primary_task_id")
        if task_id not in tasks:
            print(f"跳过未知 task_id={task_id} @ {jp}", file=sys.stderr)
            continue
        scores.append(score_record(rec, tasks[task_id]))

    if not scores:
        print("无有效记录", file=sys.stderr)
        return 2

    agg = _aggregate_by_arm_task(scores)
    source = str(args.batch_dir or args.runs_root or "jsonl")
    md = _render_markdown(scores, agg, source_label=source)

    out_json = args.out_json
    out_md = args.out_md
    if args.batch_dir and not out_json:
        out_json = args.batch_dir / "gold_f1.json"
    if args.batch_dir and not out_md:
        out_md = args.batch_dir / "gold_f1.md"
    if args.runs_root and not out_json:
        out_json = REPORTS_ROOT / "gold_f1_all_batches.json"
        out_md = REPORTS_ROOT / "gold_f1_all_batches.md"

    payload = {
        "schema": "gate_ctx_ab_gold_f1_v1",
        "source": source,
        "records": [
            {
                "file": s.file,
                "task_id": s.task_id,
                "arm": s.arm,
                "status": s.status,
                "parse_ok": s.parse_ok,
                "entrypoints": {
                    "tp": s.entrypoints.tp,
                    "fp": s.entrypoints.fp,
                    "fn": s.entrypoints.fn,
                    "precision": s.entrypoints.precision,
                    "recall": s.entrypoints.recall,
                    "f1": s.entrypoints.f1,
                    "gold_hits": s.gold_entry_hits,
                    "gold_misses": s.gold_entry_misses,
                },
                "impacts": {
                    "tp": s.impacts.tp,
                    "fp": s.impacts.fp,
                    "fn": s.impacts.fn,
                    "precision": s.impacts.precision,
                    "recall": s.impacts.recall,
                    "f1": s.impacts.f1,
                },
            }
            for s in scores
        ],
        "aggregate": agg,
    }

    print(md)
    if out_json:
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\nOK json -> {out_json}", flush=True)
    if out_md:
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(md, encoding="utf-8")
        print(f"OK md   -> {out_md}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
