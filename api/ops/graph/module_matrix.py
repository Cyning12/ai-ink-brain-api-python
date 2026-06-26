"""Module 矩阵服务：从 graph snapshot 提取 distinct module_id，并关联 issue 扫描数据。

核心约束：
- 模块行来自 graph.json 中 kind=struct 或带 module_id 的节点，禁止遍历全部 flow 节点
- 行数上限 20
- Issue 映射优先级：labels 含 module:{module_id} > scan_tags 非空 + flow_map 回落
- Tier 计数来自 matched issues 的 scan_tags（C3-P0 / C3-P1 / C3-P2）
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from api.rag_env import supabase_execute_with_retry


def _default_flow_map_path() -> Path:
    raw = (os.getenv("OPS_GRAPH_MODULE_FLOW_MAP_PATH") or "").strip()
    if raw:
        return Path(raw)
    # 仓内只读路径（与 ingest 时写入 snapshot meta 的副本一致）
    return Path("workspace/kimi-code-meta/docs/_tech_graph/graph_module_flow_map.yaml")


def _load_flow_map(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """加载 graph_module_flow_map.yaml，返回 module_id -> rule 映射。"""
    p = path or _default_flow_map_path()
    if not p.exists():
        return {}
    try:
        import yaml

        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    rules = data.get("rules", [])
    if not isinstance(rules, list):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        module_id = rule.get("module_id")
        if not module_id:
            continue
        # 合并同 module_id 的多条 rule（取 path_globs / path_substrings 并集）
        existing = result.setdefault(module_id, {"path_globs": [], "path_substrings": []})
        for key in ("path_globs", "path_substrings"):
            vals = rule.get(key, [])
            if isinstance(vals, list):
                existing[key].extend(vals)
            elif isinstance(vals, str):
                existing[key].append(vals)
    return result


def _extract_module_ids(payload: dict[str, Any]) -> list[str]:
    """从 graph payload 提取 distinct module_id。

    策略：
    1. 优先取 node.module_id（post-Epic 结构）
    2. 次选 node.kind == 'struct' 的 node.id（struct 节点即 module）
    3. 去重、保持原序、上限 20
    """
    nodes = payload.get("nodes", [])
    if not isinstance(nodes, list):
        return []
    seen: set[str] = set()
    result: list[str] = []
    for node in nodes:
        if not isinstance(node, dict):
            continue
        module_id = node.get("module_id")
        if not module_id:
            # fallback：struct 节点用 node.id 作为 module_id
            if node.get("kind") == "struct":
                module_id = node.get("id")
        if not module_id or not isinstance(module_id, str):
            continue
        if module_id in seen:
            continue
        seen.add(module_id)
        result.append(module_id)
        if len(result) >= 20:
            break
    return result


def _match_issue_to_module(
    issue: dict[str, Any],
    module_id: str,
    flow_map: dict[str, dict[str, Any]],
) -> bool:
    """判断单个 issue 是否属于 module_id。

    优先级：
    1. labels 含 module:{module_id} → 直接命中
    2. scan_tags 非空 → 用 flow_map 的 path_substrings / title 关键词回落匹配
    """
    labels = issue.get("labels", [])
    if isinstance(labels, list) and f"module:{module_id}" in labels:
        return True

    scan_tags = issue.get("scan_tags", [])
    if not isinstance(scan_tags, list) or not scan_tags:
        return False

    rule = flow_map.get(module_id)
    if not rule:
        return False

    title = (issue.get("title") or "").lower()
    body = (issue.get("body") or "").lower()
    text = f"{title} {body}"

    # path_substrings 匹配 issue title/body
    substrings = rule.get("path_substrings", [])
    for sub in substrings:
        if sub and sub.lower() in text:
            return True

    # path_globs 转换为关键词（取最后一段）做宽松匹配
    globs = rule.get("path_globs", [])
    for glob in globs:
        if not glob:
            continue
        keyword = glob.strip("*/").lower()
        if keyword and keyword in text:
            return True

    return False


def _count_tiers(issues: list[dict[str, Any]]) -> dict[str, int]:
    """统计 issues 中 C3-P0 / C3-P1 / C3-P2 数量。"""
    counts = {"p0": 0, "p1": 0, "p2": 0}
    for issue in issues:
        tags = issue.get("scan_tags", [])
        if not isinstance(tags, list):
            continue
        for tag in tags:
            if tag == "C3-P0":
                counts["p0"] += 1
            elif tag == "C3-P1":
                counts["p1"] += 1
            elif tag == "C3-P2":
                counts["p2"] += 1
    return counts


class ModuleMatrixService:
    """共享模块矩阵服务：运行时 join graph snapshot + ops_issues。"""

    def __init__(
        self,
        repo_id: str,
        client: Any,
        flow_map: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self.repo_id = repo_id
        self.client = client
        self._flow_map = flow_map

    @property
    def flow_map(self) -> dict[str, dict[str, Any]]:
        if self._flow_map is None:
            self._flow_map = _load_flow_map()
        return self._flow_map

    def _sb(self) -> Any:
        return self.client

    def get_module_ids(self, payload: dict[str, Any]) -> list[str]:
        return _extract_module_ids(payload)

    def _fetch_open_issues(self) -> list[dict[str, Any]]:
        """拉取当前 repo 全部 open issues（内存内过滤，避免 N+1）。"""

        def _once() -> list[dict[str, Any]]:
            sb = self._sb()
            res = (
                sb.table("ops_issues")
                .select("number, title, state, labels, scan_tags, body, created_at, updated_at")
                .eq("repo_id", self.repo_id)
                .eq("state", "open")
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return [r for r in rows if isinstance(r, dict)]

        return supabase_execute_with_retry(_once)

    def build_matrix(
        self,
        payload: dict[str, Any],
        *,
        state: str = "open",
    ) -> list[dict[str, Any]]:
        """构建模块×Issue 矩阵。

        返回列表项：
        {
            "module_id": str,
            "label": str | None,
            "open_issue_count": int,
            "p0_count": int,
            "p1_count": int,
            "p2_count": int,
            "issue_numbers": list[int],
            "sample_issues": list[dict],
        }
        """
        module_ids = self.get_module_ids(payload)
        if not module_ids:
            return []

        # 获取节点元数据（label 等）
        nodes = payload.get("nodes", [])
        node_by_module: dict[str, dict[str, Any]] = {}
        for node in nodes if isinstance(nodes, list) else []:
            if not isinstance(node, dict):
                continue
            mid = node.get("module_id") or (node.get("id") if node.get("kind") == "struct" else None)
            if mid and isinstance(mid, str):
                node_by_module[mid] = node

        # 只查一次 open issues
        all_issues = self._fetch_open_issues() if state == "open" else []
        flow_map = self.flow_map

        matrix: list[dict[str, Any]] = []
        for module_id in module_ids:
            node = node_by_module.get(module_id, {})
            label = node.get("label") or module_id

            matched = [
                issue
                for issue in all_issues
                if _match_issue_to_module(issue, module_id, flow_map)
            ]

            tiers = _count_tiers(matched)
            sample = [
                {
                    "number": issue.get("number"),
                    "title": issue.get("title"),
                    "state": issue.get("state"),
                    "labels": issue.get("labels", []),
                }
                for issue in matched[:5]
            ]

            matrix.append(
                {
                    "module_id": module_id,
                    "label": label,
                    "open_issue_count": len(matched),
                    "p0_count": tiers["p0"],
                    "p1_count": tiers["p1"],
                    "p2_count": tiers["p2"],
                    "issue_numbers": [i.get("number") for i in matched],
                    "sample_issues": sample,
                }
            )

        return matrix

    def get_module_edges(
        self,
        payload: dict[str, Any],
        *,
        relation: str = "depends_on",
    ) -> list[dict[str, Any]]:
        """提取 module 级依赖边（端点均为 module/struct 节点）。

        返回：
        [{"from": module_id, "to": module_id, "relation": str, "label": str}]
        """
        nodes = payload.get("nodes", [])
        if not isinstance(nodes, list):
            return []

        module_id_set: set[str] = set()
        node_id_to_module: dict[str, str] = {}
        for node in nodes:
            if not isinstance(node, dict):
                continue
            mid = node.get("module_id")
            nid = node.get("id")
            if mid and isinstance(mid, str):
                module_id_set.add(mid)
                if nid and isinstance(nid, str):
                    node_id_to_module[nid] = mid
            elif node.get("kind") == "struct" and nid and isinstance(nid, str):
                module_id_set.add(nid)
                node_id_to_module[nid] = nid

        edges = payload.get("edges", [])
        if not isinstance(edges, list):
            return []

        result: list[dict[str, Any]] = []
        for edge in edges:
            if not isinstance(edge, dict):
                continue
            if edge.get("type") != relation:
                continue
            from_id = edge.get("from")
            to_id = edge.get("to")
            if not from_id or not to_id:
                continue
            from_module = node_id_to_module.get(from_id)
            to_module = node_id_to_module.get(to_id)
            if not from_module or not to_module:
                continue
            result.append(
                {
                    "from": from_module,
                    "to": to_module,
                    "relation": relation,
                    "label": edge.get("label", ""),
                }
            )
        return result
