> **epic**: `standards-engineering/api-modularization`
> **manifest_ref**: W7 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**: `required`
> **非范围**: MANIFEST 表内未列出的 `api/*.py` 文件

---

# W7 · Tool 注册表拆分

> **状态**: active（PR 待 merge）
> **slug**: `api-tools-registry-split`
> **git_branch**: `task/api-tools-w7`
> **风险**: Medium
> **freeze_id**: `CODING_BACKEND_L2@2026-06-09`

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

无对外 HTTP 变更；`from api.tools import …` 入口不变。

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
