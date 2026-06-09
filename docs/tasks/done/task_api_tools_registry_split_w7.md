> **epic**: `standards-engineering/api-modularization`
> **manifest_ref**: W7 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**: `required`
> **非范围**: MANIFEST 表内未列出的 `api/*.py` 文件

---

# W7 · Tool 注册表拆分

> **状态**: done（PR [#155](https://github.com/Cyning12/ai-ink-brain-api-python/pull/155) · 2026-06-09）
> **slug**: `api-tools-registry-split`
> **git_branch**: `task/api-tools-w7`
> **风险**: Medium
> **freeze_id**: `CODING_BACKEND_L2@2026-06-09`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-tools-registry-split` |
| **git_branch** | `task/api-tools-w7` |
| **orchestration** | Cursor Task 链 |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `api/tools.py` 中 RAG / Text2SQL 工具实现分文件；`tools.py` 保留 `get_tool_registry()` 入口与 `direct_answer`。

### 下沉范围

| 模块 | 说明 |
|------|------|
| `api/tool_models.py` | `ToolResult` / `Tool` / `ToolRegistry` / `ToolName` |
| `api/tools_shared.py` | 共享 helper（elapsed、chat model、sql error 映射等） |
| `api/tools_rag.py` | `rag_search_execute` + `_rag_retrieve` |
| `api/tools_text2sql.py` | `text2sql_execute` 及子阶段 helper |

---

## 行为变更（Delta）

### ADDED
- `api/tool_models.py` · `api/tools_shared.py` · `api/tools_rag.py` · `api/tools_text2sql.py`

### MODIFIED
- `api/tools.py` — 瘦身为 registry 入口
- `tools/tech_graph_contract_check.py` — `BACKEND_CONTRACT_SOURCES` 纳入 `tools_text2sql.py`

### 不变
- `get_tool_registry()` / `from api.tools import Tool` 等对外 import

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-tools-split-break | 拆分破坏 tool execute 行为 | pytest 阻塞 merge |

---

## 验收标准

- [x] 子模块存在且 ruff 绿
- [x] `get_tool_registry()` 仍在 `api/tools.py`
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [x] 单 PR 触及 `api/*.py` ≤8（本 PR：**5**）

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W7 实现 · PR 待 merge |
