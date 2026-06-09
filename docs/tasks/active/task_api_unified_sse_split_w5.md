> **epic**：`standards-engineering/api-modularization`
> **manifest_ref**：W5 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**：`required`
> **非范围**：JSON 路径（已 W4 完成）、MANIFEST 表内未列出的 `api/*.py` 文件

---

# W5 · Unified SSE 路径下沉

> **状态**：active（执行中）
> **slug**：`api-unified-sse-split`
> **git_branch**：`task/api-unified-sse-w5`
> **风险**：High
> **freeze_id**：`CODING_BACKEND_L2@2026-06-09`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-unified-sse-split` |
| **git_branch** | `task/api-unified-sse-w5` |
| **orchestration** | Claude Code Harness 链 |
| **chain_prompt** | `PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md` |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `api/unified_chat.py` 中 SSE handler（`handle_unified_chat_stream` + `_sse`）抽至 `api/unified/sse_handler.py`；`unified_chat.py` 保留共享辅助函数和 JSON 薄层 wrapper。

### 下沉范围

| 函数 | 行数（HEAD） | 说明 |
|------|-------------|------|
| `handle_unified_chat_stream` | ~1220 行（862–2084） | SSE 主 handler |
| `_sse` | ~12 行（848–861） | SSE 格式化辅助 |

### 共享辅助函数策略

- **留在 `unified_chat.py`**：被 JSON 和 SSE 共用的函数（`_event`, `_now_ms`, `_safe_text_for_event` 等）
- **随 SSE 下沉**：仅 SSE 路径使用的内部函数
- **循环依赖避免**：`sse_handler.py` 从 `unified_chat` import 共享函数；`unified_chat.py` 用延迟 import wrapper

### 契约对照

W5 须对照 `docs/_tech_graph/_contract_manifest.json`：
- `POST /api/py/unified/chat/stream` 的 SSE 契约不变

---

## 行为变更（Delta）

### ADDED
- `api/unified/sse_handler.py` — 新模块

### MODIFIED
- `api/unified_chat.py` — 移除 `handle_unified_chat_stream` + `_sse`，保留薄层 wrapper

### 不变
- `POST /api/py/unified/chat/stream` 的 path/method/SSE 事件格式
- JSON 路径不动

---

## 先测后拆（D2）

| 测试文件 | 说明 |
|----------|------|
| `tests/test_unified_chat_streaming_sse.py` | 已有，复用 |
| `tests/test_unified_chat_sse_incremental_vnext.py` | 已有，复用 |

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-mega-refactor | 单 PR 触及 >8 个 `api/*.py` | **拒合并** |
| F2 | fp-contract-break | Unified SSE 契约变更 | **blocked** |
| F3 | fp-json-break | 拆分破坏 JSON 路径 | **40 阻塞** |

---

## 验收标准

- [ ] `api/unified/sse_handler.py` 存在且 ruff 绿
- [ ] `unified_chat.py` 仍包含 `handle_unified_chat`（JSON 不动）
- [ ] `unified_chat.py` 行数从 ~2084 降至 ~<900
- [ ] `test_unified_chat_streaming_sse.py` 仍通过
- [ ] `test_unified_chat_sse_incremental_vnext.py` 仍通过
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [ ] `ruff check api tests` 全绿
- [ ] `manifest_check` + `contract_check` 全绿
- [ ] 单 PR 触及 `api/*.py` 数量 ≤8

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W5 task 初稿 — unified SSE 路径下沉 |
