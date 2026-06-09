> **epic**: `standards-engineering/api-modularization`
> **manifest_ref**: W8 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**: `required`
> **非范围**: MANIFEST 表内未列出的 `api/*.py` 文件

---

# W8 · Intent 栈拆分

> **状态**: done（PR [#157](https://github.com/Cyning12/ai-ink-brain-api-python/pull/157) · 2026-06-09）
> **slug**: `api-intent-stack-split`
> **git_branch**: `task/api-intent-w8`
> **风险**: Medium
> **freeze_id**: `CODING_BACKEND_L2@2026-06-09`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-intent-stack-split` |
| **git_branch** | `task/api-intent-w8` |
| **orchestration** | Cursor Task 链 |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `intent_agent.py` / `intent_router.py` 中表驱动规则与 LLM 路径分文件；公开 import 不变。

### 下沉范围

| 模块 | 说明 |
|------|------|
| `api/intent_router_rules.py` | V1 表驱动规则（rag/sql/no_data keyword 命中） |
| `api/intent_llm.py` | LRU 缓存、LLM 外呼/重试、`decide_intent_v2` |

---

## 行为变更（Delta）

### ADDED
- `api/intent_router_rules.py` · `api/intent_llm.py`

### MODIFIED
- `api/intent_agent.py` — 模型 + hints 仲裁 + re-export
- `api/intent_router.py` — 保留 `decide_intent()` 入口，规则下沉

### 不变
- `from api.intent_agent import decide_intent_v2, IntentDecision, ...`
- `from api.intent_router import decide_intent`
- `api/agent.py` 须保留 `decide_intent_v1` import 绑定

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-intent-split-break | 拆分破坏 intent 路由/缓存/重试 | pytest 阻塞 merge |

---

## 验收标准

- [x] 子模块存在且 ruff 绿
- [x] `decide_intent()` 仍在 `api/intent_router.py`
- [x] `decide_intent_v2()` 仍可从 `api/intent_agent` import
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [x] 单 PR 触及 `api/*.py` ≤8（本 PR：**4**）

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W8 实现 |
