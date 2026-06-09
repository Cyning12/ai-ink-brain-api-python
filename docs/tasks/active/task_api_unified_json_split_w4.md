> **epic**：`standards-engineering/api-modularization`
> **manifest_ref**：W4 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**：`required`
> **非范围**：SSE 路径（handle_unified_chat_stream · W5）、MANIFEST 表内未列出的 `api/*.py` 文件

---

# W4 · Unified JSON 路径下沉

> **状态**：active（执行中）
> **slug**：`api-unified-json-split`
> **git_branch**：`task/api-unified-json-w4`
> **风险**：High
> **freeze_id**：`CODING_BACKEND_L2@2026-06-09`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-unified-json-split` |
| **git_branch** | `task/api-unified-json-w4` |
| **orchestration** | Claude Code Harness 链 |
| **chain_prompt** | `PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md` |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `api/unified_chat.py` 中 JSON handler（`handle_unified_chat`）抽至 `api/unified/json_handler.py`；`unified_chat.py` 保留 SSE handler 和共享辅助函数。

### 下沉范围

| 函数 | 行数（HEAD） | 说明 |
|------|-------------|------|
| `handle_unified_chat` | ~1160 行（838–1997） | JSON 主 handler |

### 共享辅助函数策略

`handle_unified_chat` 依赖 `unified_chat.py` 中大量辅助函数（`_event`, `_now_ms`, `_safe_text_for_event`, `_build_rag_sources_event` 等）。策略：
- **留在 `unified_chat.py`**：被 JSON 和 SSE 共用的函数
- **随 JSON handler 下沉**：仅 JSON 路径使用的内部函数
- **循环依赖避免**：`json_handler.py` 从 `unified_chat` import 共享函数；`unified_chat.py` 从 `json_handler` import `handle_unified_chat`

### 契约对照

W4 须对照 `docs/_tech_graph/_contract_manifest.json`：
- `POST /api/py/unified/chat` 的 request/response 契约不变
- handler 名变更需在 manifest 中更新锚点

---

## 行为变更（Delta）

### ADDED
- `api/unified/json_handler.py` — 新模块，含 `handle_unified_chat`
- `api/unified/__init__.py` — 包入口

### MODIFIED
- `api/unified_chat.py` — 移除 `handle_unified_chat`，保留 import

### 不变
- `POST /api/py/unified/chat` 的 path/method/request/response
- SSE 路径（`handle_unified_chat_stream`）不动

---

## 先测后拆（D2）

| 测试文件 | 说明 |
|----------|------|
| `tests/test_unified_chat_backend_v1.py` | 已有，复用验证 JSON 路径 |
| `tests/test_unified_chat_backend_v2_agent.py` | 已有，复用 |

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-mega-refactor | 单 PR 触及 >8 个 `api/*.py` | **拒合并** |
| F2 | fp-contract-break | Unified JSON 契约变更 | **blocked** — 须对照 `_contract_manifest.json` |
| F3 | fp-sse-break | 拆分破坏 SSE 路径 | **40 阻塞** |
| F4 | fp-cycle-dep | `json_handler.py` ↔ `unified_chat.py` 循环导入 | **blocked** |

---

## 验收标准

- [ ] `api/unified/json_handler.py` 存在且 ruff 绿
- [ ] `api/unified_chat.py` 仍包含 `handle_unified_chat_stream`（SSE 不动）
- [ ] `unified_chat.py` 行数从 ~3236 降至 ~<2200
- [ ] `tests/test_unified_chat_backend_v1.py` 仍通过
- [ ] `tests/test_unified_chat_backend_v2_agent.py` 仍通过
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [ ] `ruff check api tests` 全绿
- [ ] `manifest_check` + `contract_check` 全绿
- [ ] 单 PR 触及 `api/*.py` 数量 ≤8

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W4 task 初稿 — unified JSON 路径下沉 |
