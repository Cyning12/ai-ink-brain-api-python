# 独立复检（50 帽）：技术图谱 — 方案2 补全

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `docs/tasks/active/task_engineering_tech_graph_scheme2_completion_v1.md`（**v0.2**） |
| **关联 R1** | `docs/harness/reviews/task_engineering_tech_graph_scheme2_completion_v1_audit_R1_20260518.md` |
| **invoke_snapshot** | `docs/harness/invokes/invoke_20260518_50_tech-graph-scheme2-completion-reinspect.md` |
| **模式** | 独立复检（§一） |
| **复检日期** | 2026-05-18 |
| **git_branch** | `task/engineering-tech-graph-scheme2-completion-v1` |
| **diff 范围** | 子仓 `origin/main...HEAD` |
| **freeze_id** | `TECH_GRAPH_S2_FREEZE_20260517_V2_2`（继承；本 PR 无 schema 语义变更） |

---

## 复检结论摘要

**建议合并**（子仓 feature → `main`）。**零硬阻塞**；40 帽命令表经 50 独立复跑 **一致**。S2-B 工作区文档已在 **Projects `main@820f087`**，子仓 PR 须 **显式链** 该 commit（非阻塞 N-WS）。

**不**代签 `HG-AUDIT-CLOSE` / `HG-GLOBAL-SIGNOFF`（task 表已为 `approved`，本报告仅核对工程证据）。

---

## diff 摘要（子仓 `origin/main...HEAD`）

| 指标 | 值 |
|------|-----|
| 变更文件 | 10 |
| 行数 | +664 / −88 |
| commits | 6（`7873a37` … `dbe1183`） |
| 核心实现 | `tools/tech_graph_graph_query.py`（`has_path` / `describe_impact` + CLI） |
| 单测 | `tests/test_tech_graph_graph_query.py`（+8 用例级） |
| S2-B（子仓） | `docs/_tech_graph/graph_v2_schema.md` §9 |
| S2-C | `.cursor/mcp.json.example`；Harness 模板可选步骤（工作区 `main`） |

**未在子仓 diff**：`Projects/docs/tech_graph/`（`scheme_2_graph_query.md`、`改进方向.md` §2.3～2.7）→ **`main@820f087`**。

**禁止项抽检**：无 `.github/workflows/`；无 `run_gate_b_batch`；无 `graph_query.py` 重命名。

---

## 命令复跑（对照 task「### 自检结论」）

| 命令 | 40 帽 | 50 复检 |
|------|-------|---------|
| `pytest tests/test_tech_graph_graph_query.py -q` | 0 · 16 passed | **0 · 16 passed** |
| `python tools/tech_graph_graph_export.py --check` | 0 | **0** |
| `python tools/tech_graph_graph_equivalence_check.py` | 0 | **0** |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 · 184 passed, 1 skipped | **0 · 184 passed, 1 skipped** |

---

## 验收表

| 验收项 | 结论 | 证据 |
|--------|------|------|
| §3.1 `has_path` 路径/非路径/同节点 | pass | `test_has_path_reachable` / `not_reachable` / `same_node` |
| §3.1 未知节点 → FP-4 | pass | `test_has_path_fp4_unknown` → `EXIT_FP4` |
| §3.1 `describe_impact` 子串语义 | pass | `test_describe_impact_contains_labels` |
| §3.1 CLI `has-path` / `describe-impact` | pass | `test_cli_has_path_auth_rag`、`test_cli_describe_impact_pool` |
| §3.1 原有用例仍绿 | pass | 16 passed |
| §3.2 SPEC / 改进方向 | pass | `Projects/docs/tech_graph/` @ `820f087` |
| §3.2 `graph_v2_schema.md` §9 | pass | `has-path` / `describe-impact` 行 |
| §3.2 闸口 B 引用不重跑 | pass | 无 batch；文档链结论报告 |
| §3.3 export / equivalence / 全量 pytest | pass | 见上表 |
| §3.4 S2-C C1+C2 | pass | `.cursor/mcp.json.example`；`TEMPLATE-task-audit-invoke.md` 可选节 |
| §1.2 NR（workflow/schema/重命名/Neo4j） | pass | diff 抽检 |
| §4 FP-S2-5/6 | pass | `_require_node` + 现 loader |
| test_strategy: required | pass（弱注） | 同 PR 含测+实现；未从 git 证先红后绿 |
| 40 已知未测 | 非阻塞 | 生产图 AUTH→RAG；MCP 无 IDE e2e |

---

## 阻塞合并项

**无硬阻塞。**

| ID | 类型 | 说明 |
|----|------|------|
| N-WS | 非阻塞 | PR 须链 `Projects@820f087`（S2-B 工作区文档） |
| N-MCP | 非阻塞 | C1 为 CLI 示例，非完整 MCP 协议 |
| N-PROD | 非阻塞 | 生产 `graph.json` 与 golden fixture 可能不一致 |

---

## R1 执行后对照

| R1 项 | 判定 |
|-------|------|
| 零硬阻塞 | **仍成立** |
| §0.4 / §0.5 / NR | **一致** |
| S2-B 悬空项 | **已闭合**（工作区 + 子仓 schema） |
| R1 时 HG 待签 | task 现三闸均为 `approved` |

---

## 执行路线与 Commit 回溯

| 阶段 | commit | 摘要 |
|------|--------|------|
| 10 | `7873a37` | task v0.2 + invoke |
| 22 R1 | `d09a13f` | R1 review + 30 invoke |
| 30 | `e8b934c` | feat: has_path / describe_impact |
| 40 | `16f6db6` / `dbe1183` | 自检 invoke + task 结论 |
| S2-B 工作区 | `820f087`（Projects `main`） | SPEC + 改进方向 |
| 50 | （本轮） | 本报告 + invoke |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-18 | 50 独立复检：建议合并；零硬阻塞 |
