# SPEC: ChatBI V2 —— 事件流兼容设计

> **状态**：draft  
> **版本**：v2 + vNext §8（增量 LLM：`agent.llm.*`，chain-only）  
> **日期**：2026-04-27（vNext 终稿修订：2026-05-08）  
> **父文档**：`SPEC-ChatBI-V2-Agent-Overview.md`

---

## 1. 设计目标

V2 Agent 架构保留 V1 的 SSE 事件流格式，对外 mode 语义不变，前端无需修改即可接入。

新增 Agent 相关事件，透明化决策过程。

**策略 B**：允许新增 agent.* 类型，但必须同步更新契约真值（manifest），并明确"前端可忽略未知 type"的约束。

---

## 2. 事件类型总览

### 2.1 V1 保留事件（格式不变）

| 事件类型 | 说明 | 触发时机 | 前端处理 |
|---------|------|---------|---------|
| `router.decision` | 保留，内容变为 Agent 初始决策 | Agent 做出初始决策时 | 兼容 |
| `tool.call.start` | 工具调用开始 | 任何 Tool 执行前 | 兼容 |
| `tool.call.end` | 工具调用结束 | 任何 Tool 执行后 | 兼容 |
| `sql.result` | SQL 执行结果 | Text2SQL 工具执行后 | 兼容 |
| `rag.sources` | RAG 检索来源 | RAG 工具执行后 | 兼容 |
| `rag.query_expand` | 查询扩展 | RAG 工具执行时 | 兼容 |
| `assistant.message` | 最终回答 | Agent 完成时 | 兼容 |
| `latency` | 耗时统计 | 请求结束时 | 兼容 |
| `error` | 错误 | 任何阶段出错时 | 兼容 |

### 2.2 V2 新增事件（前端可安全忽略）

| 事件类型 | 说明 | 触发时机 | 前端处理 |
|---------|------|---------|---------|
| `agent.step.start` | Agent 步骤开始 | 每步 ReAct 循环开始时 | **可忽略** |
| `agent.think` | Agent 思考摘要（用户级） | LLM 决策后 | **可忽略** |
| `agent.intent` | 意图识别结果 | Intent Agent 决策后 | **可忽略** |
| `agent.step.end` | Agent 步骤结束 | 每步 ReAct 循环结束时 | **可忽略** |
| `agent.final` | Agent 最终决策 | Agent 决定直接回答时 | **可忽略** |
| `agent.llm.start` | LLM 子阶段开始（vNext） | 子步调用上游前 | Unified 增量客户端 **须处理**（右栏标题等） |
| `agent.llm.delta` | LLM 文本增量（vNext） | 上游流式 chunk | **须处理**（右栏拼接）；未知字段策略 B |
| `agent.llm.end` | LLM 子阶段结束（vNext） | 子步完成/失败 | **须处理** |
| `agent.llm.truncated` | 背压/截断信号（vNext） | 队列触顶 | **须处理**（可折叠展示） |

---

## 3. 事件详细定义

### 3.1 agent.step.start

```json
{
  "type": "agent.step.start",
  "ts": 120,
  "step_id": "a1",
  "payload": {
    "step_number": 1,
    "max_steps": 5
  }
}
```

### 3.2 agent.think（用户级摘要）

```json
{
  "type": "agent.think",
  "ts": 340,
  "step_id": "a1_think",
  "payload": {
    "step_number": 1,
    "thought": "用户问的是销售额统计，需要查询数据库",
    "selected_tool": "text2sql_query",
    "mode": "text2sql",
    "confidence": 0.92
  }
}
```

**注意**：`thought` 字段只包含用户级摘要（1-2 句话），不含系统提示或策略细节。

### 3.3 agent.intent

```json
{
  "type": "agent.intent",
  "ts": 120,
  "step_id": "intent_1",
  "payload": {
    "tool": "text2sql_query",
    "mode": "text2sql",
    "reasoning": "用户询问销售额，需要查询数据库获取结构化数据",
    "confidence": 0.92,
    "fallback": null
  }
}
```

### 3.4 agent.step.end

```json
{
  "type": "agent.step.end",
  "ts": 1250,
  "step_id": "a1_end",
  "payload": {
    "step_number": 1,
    "tool_used": "text2sql_query",
    "mode": "text2sql",
    "success": true,
    "next_action": "continue | final_answer"
  }
}
```

### 3.5 agent.final

```json
{
  "type": "agent.final",
  "ts": 2800,
  "step_id": "a_final",
  "payload": {
    "total_steps": 2,
    "tools_used": ["text2sql_query", "rag_search"],
    "modes": ["text2sql", "rag"],
    "fallback_used": false
  }
}
```

---

## 4. 完整事件流示例

### 4.1 单工具场景（Text2SQL）

```
chain: meta              # 首包：run_id, mode
chain: router.decision   # Agent 决策：选 text2sql_query，mode=text2sql
chain: agent.step.start  # Step 1 开始
chain: agent.think       # LLM 思考：需要查数据库
chain: agent.intent      # 意图识别：text2sql，confidence=0.92
chain: tool.call.start   # 调用 text2sql_query
chain: tool.call.end     # 返回 SQL 结果
chain: sql.result        # SQL 执行结果
chain: agent.step.end    # Step 1 结束
chain: agent.final       # Agent 完成
done: ok=true, mode=text2sql
```

### 4.2 多工具场景（Text2SQL + RAG）

```
chain: meta
chain: router.decision   # Agent 决策：先 text2sql_query，mode=text2sql
chain: agent.step.start  # Step 1
chain: agent.think       # 先查数据
chain: agent.intent      # 意图：text2sql
chain: tool.call.start   # text2sql_query
chain: tool.call.end     # 发现异常
chain: sql.result
chain: agent.step.end    # Step 1 完成，需要更多信息

chain: agent.step.start  # Step 2
chain: agent.think       # 数据异常，查文档看原因
chain: agent.intent      # 意图：rag_search
chain: tool.call.start   # rag_search
chain: rag.sources       # 检索来源
chain: tool.call.end     # 找到原因
chain: agent.step.end    # Step 2 完成

chain: agent.final       # 综合两步结果
done: ok=true, mode=text2sql
```

### 4.3 Fallback 场景（SQL 失败 → RAG）

```
chain: meta
chain: router.decision   # Agent 决策：text2sql_query
chain: agent.step.start  # Step 1
chain: agent.think       # 查数据
chain: agent.intent      # 意图：text2sql，fallback=rag_search
chain: tool.call.start   # text2sql_query
chain: tool.call.end     # 失败：表不存在
chain: error             # SQL 执行错误
chain: agent.step.end    # Step 1 失败

chain: agent.step.start  # Step 2（fallback）
chain: agent.think       # 表不存在，查文档看正确表名
chain: agent.intent      # 意图：rag_search（fallback）
chain: tool.call.start   # rag_search
chain: rag.sources       # 检索到文档
chain: tool.call.end     # 找到正确表名
chain: agent.step.end    # Step 2 完成

chain: agent.final       # 完成（带 fallback 标记）
done: ok=true, mode=text2sql, fallback_used=true
```

---

## 5. 与 V1 的兼容策略

### 5.1 前端兼容

**约束**：前端收到未知 type 时**忽略，不报错**。

```typescript
// 前端示例（TypeScript）
function handleEvent(event: SSEEvent) {
  switch (event.type) {
    case 'tool.call.start':
      // V1 已知事件，正常处理
      showToolStart(event);
      break;
    case 'agent.think':
      // V2 新增事件，可选处理（如显示"思考中..."）
      showThinking(event.payload.thought);
      break;
    default:
      // 未知事件：安全忽略
      if (DEBUG) console.log('Unknown event type:', event.type);
      break;
  }
}
```

### 5.2 后端兼容

```python
# unified_chat.py 中判断模式
USE_AGENT = os.getenv("CHATBI_USE_AGENT", "true").lower() == "true"

if USE_AGENT:
    # V2 路径：Agent 决策
    result = await agent.run(query, session_id)
    mode = result.mode  # 对外仍输出 V1 mode
else:
    # V1 路径：规则路由（降级）
    decision = decide_intent(query=query, prefer=prefer)
    mode = decision.final_mode
    # ... V1 逻辑
```

### 5.3 配置切换

```bash
# .env
CHATBI_USE_AGENT=true   # 启用 V2 Agent
CHATBI_USE_AGENT=false  # 降级到 V1
```

---

## 6. 契约更新（两层清单 + 唯一真值入口）

> **⚠️ 重要**：V2 Agent 新增事件涉及**两层契约**，职责分明，必须同时更新，否则会导致 CI/前端读取字段时漂移。

### 6.1 两层清单职责

| 文件 | 职责 | 校验脚本 |
|------|------|---------|
| `docs/_tech_graph/_manifest.json` | 机器可读清单：端点 / RPC / 表 / env / anchors 等**基础设施元数据** | `tools/tech_graph_manifest_check.py` |
| `docs/_tech_graph/_contract_manifest.json` | **SSE 事件契约真值**：`type_values`（允许的事件类型）、`payload_min_keys_by_type`（每个 type 的 payload 最小必需键集合）、`envelope_keys`（信封键）、`done.data_keys`（结束事件键） | `tools/tech_graph_contract_check.py` |

### 6.2 唯一真值入口

**所有 V2 Agent 新增事件，必须同时写入 `_contract_manifest.json`**（不是只写 `_manifest.json`）。

`_contract_manifest.json` 是前端消费与后端产出的**唯一 SSE 契约真值入口**。

更新示例（在 `_contract_manifest.json` 的 `sse.chain` 下追加）：

```json
{
  "sse": {
    "chain": {
      "type_values": [
        "meta",
        "router.decision",
        "tool.call.start",
        "tool.call.end",
        "rag.query_expand",
        "rag.sources",
        "sql.result",
        "assistant.message",
        "latency",
        "error",
        "agent.step.start",
        "agent.think",
        "agent.intent",
        "agent.step.end",
        "agent.final"
      ],
      "payload_min_keys_by_type": {
        "meta": ["run_id", "mode", "session_id"],
        "router.decision": ["prefer", "candidate_mode", "final_mode", "rule_hits", "evidence", "fallback"],
        "tool.call.start": ["tool", "input"],
        "tool.call.end": ["output", "error", "latency_ms"],
        "rag.query_expand": ["raw", "rewrite"],
        "rag.sources": {
          "payload_keys": ["sources", "retrieval"],
          "source_item_keys": ["id", "content", "filename", "score", "path", "url"],
          "retrieval_keys": ["top_k", "rrf_k"]
        },
        "sql.result": ["sql", "columns", "rows", "truncated"],
        "assistant.message": ["role", "content"],
        "latency": ["total_ms", "stages_ms"],
        "error": ["stage", "message"],
        "agent.step.start": ["step_number", "max_steps"],
        "agent.think": ["step_number", "thought", "selected_tool", "mode", "confidence"],
        "agent.intent": ["tool", "mode", "reasoning", "confidence", "fallback"],
        "agent.step.end": ["step_number", "tool_used", "mode", "success", "next_action"],
        "agent.final": ["total_steps", "tools_used", "modes", "fallback_used"]
      }
    }
  }
}
```

### 6.3 CI 校验

| 校验项 | 脚本 | 失败后果 |
|--------|------|---------|
| 新增事件 type 是否在 `type_values` 中 | `tools/tech_graph_contract_check.py` | PR 阻断 |
| 新增 type 的 payload 是否补了 `payload_min_keys_by_type` | `tools/tech_graph_contract_check.py` | PR 阻断 |
| 端点/RPC/表/env 是否同步到 `_manifest.json` | `tools/tech_graph_manifest_check.py` | PR 阻断 |
| 文档是否覆盖新增变更 | `tools/tech_graph_drift_check.py` | 告警（P0_3） |

> **规则**：新增事件 → **实现代码与** `_contract_manifest.json`（补 type + payload 键）**须同一 PR**；再改 `_manifest.json`（如有新端点/env），最后改 spec 文档。CI 全通过后方可合并。**vNext `agent.llm.*`** 见 **§8**；禁止 manifest 先于 `unified_chat.py` 空转。

---

## 7. 验收标准

- [ ] V1 事件格式保持不变（mode 语义不变）
- [ ] 新增 agent.* 事件可被前端安全忽略
- [ ] 单工具场景事件流与 V1 基本一致（只多 agent.*）
- [ ] 多工具场景事件流清晰展示决策过程
- [ ] Fallback 场景事件流完整记录降级路径
- [ ] 可通过环境变量切换 V1/V2 模式
- [ ] `_contract_manifest.json` 已包含新增 `agent.*` type 与对应的 `payload_min_keys_by_type`
- [ ] `_manifest.json` 如有新增端点 / env / anchors 已同步

---

## 8. vNext：Unified Chat LLM 流式（`chain-only`）

> **父 SPEC**：`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` §0 / §5 / §7 / §9。本节为 **语义真值**；**枚举与最小键**以合并日 `docs/_tech_graph/_contract_manifest.json` 为准。

### 8.1 与 Legacy `event: token` 的硬区分

| 路径 | `event: token` |
|------|----------------|
| **Legacy RAG**（非 `/api/py/unified/chat/stream` 的既有流式页） | **允许**沿用历史语义。 |
| **Unified Chat + `CHATBI_USE_AGENT` + 增量路径** | **禁止**用顶层 `token` 承载 **子步 LLM** 增量；子步 **必须**为 **`event: chain`** 且 `type ∈ { agent.llm.start, agent.llm.delta, agent.llm.end, agent.llm.truncated }`。 |

区分依据：**HTTP 路径** +（Unified 侧）**`X-ChatBI-Sse-Contract: 2`**，**不**靠 `scope` 推断 Legacy。

### 8.2 新增 `chain.type`（vNext 落地时写入 manifest）

| `type` | 说明 |
|--------|------|
| `agent.llm.start` | 某 LLM 子阶段开始；`payload.phase` 见 §8.4。 |
| `agent.llm.delta` | 文本增量；**多条兄弟 `chain`**，`payload.text` + `part_index`。 |
| `agent.llm.end` | 子阶段结束；`payload.ok`。 |
| `agent.llm.truncated` | 背压 / 截断可观测信号。 |

### 8.3 「首条有意义 chain」白名单（验收用）

用于 **`meta` 之后**首条有效 `chain.data` 的 CI 断言：`router.decision`、`agent.step.start`、`agent.intent`、`agent.llm.start`、`tool.call.start`。  
**排除**：SSE **注释行**、**坏 JSON**（前端策略 B 跳过）。

### 8.4 `phase` 枚举（`agent.llm.start` / `agent.llm.end`）

`intent` | `rag_generate` | `text2sql_sql` | `text2sql_summary` | `direct`（扩展须同步 manifest + 本表）。

### 8.5 好例与坏例（最小）

**好例**（顺序）：见 vNext SPEC **§5.4** JSON 行序列。

**坏例**：一条 `agent.llm.delta` **缺少** `payload.text` → 前端 **丢弃该帧**，`parse_error_count++`，**不抛异常**、**不白屏**。

### 8.6 与 `agent.think` / `assistant.message` 的关系

- **`agent.think`**：**仅摘要**；出现在 **`agent.llm.end` 之后**（同一步内）。  
- **`assistant.message`**：**最终答案唯一真相源**（成功路径全文）；右栏 **执行链路** 中各 **`agent.llm.*` 段内** delta 为过程展示，**同一 phase（如最终作答段）内宜可对齐** `assistant.message.content`（归一化规则由实现 + 单测固定）；**跨 phase** 右栏全文 **不要求** 与最终答案逐字一致 — 见 **`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` §8.4**。

### 8.7 流式失败与 `done`

- 子步失败：**`agent.llm.end`** `ok: false` → 可接 **`error`** `chain` → **`done` 仍到达**。  
- `assistant.message` 内容策略三选一（空 / 部分 / 错误全文）须在 **实现 PR** 固定并在 pytest 覆盖一种默认策略。

---

## 9. 关联文档

- 父文档：`SPEC-ChatBI-V2-Agent-Overview.md`
- 意图识别：`SPEC-ChatBI-V2-Intent.md`
- ReAct 循环：`SPEC-ChatBI-V2-ReAct-Loop.md`
- Manifest 规范：`docs/_tech_graph/99_spec.md`
