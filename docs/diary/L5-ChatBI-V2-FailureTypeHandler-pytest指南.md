# L5（Fallback / `error_code` 矩阵）— pytest 完整示例与操作指南

> **总规入口**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` **§7.5.4 L5**  
> **实现入口**：`api/agent.py` → `FailureTypeHandler.decide_next`、`_allow_sql_fallback`  
> **示例用例**：`tests/test_unified_chat_backend_v2_agent.py`（文件头 **①②③④** 注释 + 下文两则「canonical」用例）

---

## 1. L5 到底在验什么（一句话）

证明：**工具返回的 `ToolResult.error_code`** 与 **`IntentDecision`（含 gating 信号）** 组合后，**下一步工具名 / 是否立即结束（`stop_now`）** 与总规 **§2.4 / §2.4.1** 一致；**尤其** `RAG_RETRIEVE_EMPTY` 时 **不得**在无 gating 时盲启 `text2sql_query`。

L5 **不是**「固定 UI 必须 rag→text2sql」，而是 **矩阵里每一行** 的可重复断言（pytest 为主，集成手测为辅）。

---

## 2. `RAG_RETRIEVE_EMPTY` 的 gating（无独立 env 开关）

`_allow_sql_fallback(intent)` 为真，当且仅当 **以下任一** 成立：

| 代号 | 条件 | 典型来源 |
|------|------|----------|
| **A** | `intent.tool == "text2sql_query"` 或 `intent.fallback == "text2sql_query"` | `decide_intent_v2` 主工具 / 低置信度 fallback |
| **B** | `intent.structured_signals.llm_prefers_sql` | `intent_agent` 内对 query 调 `is_text2sql_intent(query)` |
| **C** | `intent.structured_signals.has_aggregation_signals` | `intent_agent` 内对 query 调 `_has_aggregation_keywords(query)` |

**无** `GATING_ON=1` 这类环境变量；单测里通过 **③ patch `decide_intent_v2`** 返回带合适 `StructuredSignals` 的 `IntentDecision`，即可稳定覆盖开/关。

---

## 3. 为什么用 mock（而不是只打真实 API）

| 原因 | 说明 |
|------|------|
| **稳定** | 真实向量库未必「空命中」；真实 SQL 失败不可控。 |
| **CI 零外呼** | `CHATBI_V2_INTENT_LLM=false` + 桩意图，或 ③ 完全替换 `decide_intent_v2`。 |
| **只测 handler** | 在 **dummy `execute`** 里返回指定 `error_code`，不依赖 `unified_chat` 整条链外设。 |

**禁止**：在 `FailureTypeHandler.decide_next` 里硬改 `code`、或对 **`IntentDecision`（frozen）** 原地赋值 `intent.tool = ...`（会抛 `FrozenInstanceError`）。调整意图请 **`dataclasses.replace(...)`** 或重新构造 `IntentDecision`。

---

## 4. pytest 注入点约定（①②③④）

与 `tests/test_unified_chat_backend_v2_agent.py` 文件头一致：

| 标记 | 做什么 | `monkeypatch` 典型目标 |
|------|--------|-------------------------|
| **①** | 控制 **`ToolResult.error_code`** | 在 **dummy 工具** 的 `execute` 里 `return ToolResult(..., error_code="RAG_RETRIEVE_EMPTY", ...)` |
| **②** | 替换整表工具 | `unified_chat.get_tool_registry` → 返回只含 dummy 的 `_DummyRegistry(dummy_tools)` |
| **③** | 固定 **意图 + gating** | `api.agent.decide_intent_v2` → `_fake_...` 返回 `IntentDecision(..., structured_signals=StructuredSignals(...))` |
| **④** | **不** patch 意图，只靠 query + 启发式 | `CHATBI_V2_INTENT_LLM=false` + ①②；query 避开 text2sql 关键词 |

**reload**：该测试文件惯例是先 `_reload_api_index(monkeypatch)` 再 `import api.unified_chat` / `api.agent`，避免旧模块缓存。

---

## 5. 完整示例 A —— gating **开**：`rag_search` → `RAG_RETRIEVE_EMPTY` → **`text2sql_query`**

**目标**：验证 `FailureTypeHandler` 在 **C 或 B 或 A 为真** 时，RAG 空后第二步是 SQL。

**步骤概要**：

1. `monkeypatch.setenv("CHATBI_USE_AGENT", "true")`；意图可 `CHATBI_V2_INTENT_LLM=false`（与 CI 一致）。  
2. **`[mock ②]`** `rag_search` / `text2sql_query` / `direct_answer` 均为 dummy；`rag_search` 的 execute 固定返回 `success=False`, `error_code="RAG_RETRIEVE_EMPTY"`；`text2sql_query` 返回成功 `ToolResult`。  
3. **`[mock ③]`** `decide_intent_v2` 返回 `IntentDecision(tool="rag_search", ..., structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=True))`（**C 为真**即可放行 SQL）。  
4. `POST /api/py/unified/chat`（非 stream 亦可），从 `events` 里取 `agent.final`。  
5. **断言**：`tools_used[0] == "rag_search"` 且 **`text2sql_query` in `tools_used`**，`total_steps == 2`。

**仓库内对应函数名**：`test_v2_rag_empty_gated_fallback`。

---

## 6. 完整示例 B —— gating **关**：`rag_search` → `RAG_RETRIEVE_EMPTY` → **`direct_answer`**

**目标**：验证 **无 A/B/C** 时 **不得**调用 `text2sql_query`。

**步骤概要**：

1. 同上 env + **`[mock ②]`**：`rag_search` 仍返回 `RAG_RETRIEVE_EMPTY`；`direct_answer` 成功桩；`text2sql_query` 的 execute 内 **`raise AssertionError`**（若被调用则测试失败）。  
2. **不**使用 **③**：删除对 `decide_intent_v2` 的 patch，调用 **`clear_intent_cache()`** 避免意图缓存串线。  
3. query 使用纯日记类文案（如 **`2026-04-28日记的大致内容`**），不含 `is_text2sql_intent` / `_has_aggregation_keywords` 命中词。  
4. **断言**：`tools_used == ["rag_search", "direct_answer"]`，且 **`text2sql_query` not in tools_used**。

**仓库内对应函数名**：`test_v2_natural_diary_query_rag_empty_fallback_to_direct`。

---

## 7. 本地如何跑、与 CI 的关系

```bash
cd ai-ink-brain-api-python
python -m pytest tests/test_unified_chat_backend_v2_agent.py -q --tb=short
```

- **全文件通过** ≈ 该文件内与 Agent / 失败路径相关的回归通过。  
- L5 **全矩阵**（所有 `error_code`）是否都已覆盖，需再对照 `FailureTypeHandler.decide_next` **逐分支**核对；本指南只把 **`RAG_RETRIEVE_EMPTY` 两侧**讲透。

---

## 8. 暂时关闭 L5 mock 用例、之后如何再开

两则 canonical 用例可能带有 **`@pytest.mark.skip(...)`**（若仓库已加上）：

- **恢复**：删除对应函数上的 **`@pytest.mark.skip`** 装饰器即可。  
- **原因**：便于本地先不跑 mock、或排期后再开；**不要**把大段 `monkeypatch` 用 `#` 注释掉（易残留语法错误）。

---

## 9. 总规要求的「矩阵归档」（可选但建议）

在 **`docs/diary/`**（本文件同目录）另建一页表格，例如：

| `error_code` | 输入意图摘要 | 预期 `next_tool` | 预期 `stop_now` | pytest 用例 / 待补 |
|--------------|--------------|------------------|-------------------|---------------------|
| `RAG_RETRIEVE_EMPTY` | gating 开 | `text2sql_query` | false | `test_v2_rag_empty_gated_fallback` |
| `RAG_RETRIEVE_EMPTY` | gating 关 | `direct_answer` | false | `test_v2_natural_diary_query_rag_empty_fallback_to_direct` |
| `SQL_GEN_SYNTAX` | … | `rag_search` | … | 见同文件其它用例 / 待补 |
| … | … | … | … | … |

表末注明 **日期、commit**，即满足 §7.5.4 **「归档」** 的字面要求。

---

## 10. 与前端「执行链路」样例的关系

`ai-ink-brain/content/diary/UnifiedChat-执行链路-参考样例-日记查询.md` 中的 **§B** 可作为 **示例 B** 的 UI 侧对照；**不能**单独替代本节 pytest + 矩阵表。

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-06 | 初稿：L5 目标、gating、①②③④、示例 A/B、运行与归档 |
