# Task：Unified Chat（后端）— Router Evidence 可追溯日志（SSE + DB，v1）

> **状态**：done（2026-04-30 验收通过）  
范围：仅后端 `ai-ink-brain-api-python`  
前置：`docs/tasks/done/task_unified_chat_router_evidence_event_v1.md`（`router.evidence` 已验收通过）  
关联：
- 契约真值：`docs/_tech_graph/_contract_manifest.json`
- Manifest 真值：`docs/_tech_graph/_manifest.json`
- 门禁脚本：`tools/tech_graph_contract_check.py`、`tools/tech_graph_manifest_check.py`
- 事件输出：`api/unified_chat.py`
- 路由证据来源：`api/intent_router.py`（ddl/fts evidence 计算）
- 日志表：`public.rag_conversation_logs`（写入 `metadata`）

前端依赖策略（必须遵守）：
- 本任务只负责 **后端可追溯性**（事件 + 落库）。前端若要展示更详细的 candidates（如 Timeline 新节点/调试面板），必须在后端验收通过后再新建前端任务单；前端对未知事件 type 必须忽略不报错。

---

## 背景与目标

当前 `router.evidence` 已能展示 ddl/fts 的聚合统计（hits/score/阈值），但当出现 “可能命中但被阈值过滤导致 hits=0” 等情况时，缺少对 `top_k` 候选列表的可追溯记录，事后无法复盘：
- DDL 候选列表中是否出现了 `customer_info`？
- 每条候选的 score 是多少？是否因为 `< min_score` 被过滤？
- 是 top_k 太小、还是 tokenization/检索偏差导致候选排序异常？

目标：提供 **方案 1 + 方案 2** 的可追溯性闭环（均受 debug 开关控制）：
1. **SSE 新增事件**：`router.evidence.details`（用于 Timeline 实时回放）
2. **DB 落库**：将同样的 candidates 结构写入 `rag_conversation_logs.metadata.router_debug`，用于事后检索与对比

---

## 范围 / 非范围

### 范围

1. 新增事件：`router.evidence.details`（debug gated）
   - 仅当 `DEBUG_ROUTER_EVIDENCE=1` 时输出到 SSE（JSON 与 stream）
   - 放置位置：紧跟 `router.decision`/`router.evidence` 之后

2. DB 落库（debug gated）
   - 仅当 `DEBUG_ROUTER_EVIDENCE=1` 时写入 `public.rag_conversation_logs.metadata.router_debug`
   - 内容需截断（只保留候选摘要，避免存储完整 DDL/content）

3. 契约/manifest 同步
   - `_contract_manifest.json`：补齐 `router.evidence.details` 的 type 与 payload 最小键
   - `_manifest.json`：补齐新增 env：`DEBUG_ROUTER_EVIDENCE`

4. 测试与门禁
   - 更新/新增 pytest：断言 debug 开关开启时会输出 `router.evidence.details`
   - 必须通过：
     - `python tools/tech_graph_contract_check.py`
     - `python tools/tech_graph_manifest_check.py`

### 非范围

- 不改变路由决策逻辑（只做可观测性增强）
- 不要求默认开启（默认关闭，避免日志膨胀与信息泄露风险）

---

## 事件定义：router.evidence.details（建议）

### 事件 envelope

```json
{
  "type": "router.evidence.details",
  "ts": 130,
  "step_id": "red1",
  "payload": {
    "candidate_mode": "rag",
    "final_mode": "no_data",
    "fallback": "rag_without_fts→no_data",
    "thresholds": {
      "ddl_topk": 3,
      "ddl_min_score": 0.05,
      "fts_topk": 3
    },
    "ddl_candidates": [
      { "title": "DDL: customer_info", "score": 0.03 },
      { "title": "DDL: agent_info", "score": 0.01 }
    ],
    "fts_candidates": [
      { "id": "123", "path": "docs/xxx.md", "score": 0.1 }
    ]
  }
}
```

### 截断与安全约束（必须）
- `ddl_candidates[]` **不允许**写入完整 DDL content，只保留 `title/score`
- `fts_candidates[]` **不允许**写入 `content`，只保留 `id/path/score`
- candidates 数量最多保留 top_k（默认 3），字段字符串长度截断（例如 120 字符）

---

## DB 落库结构（建议）

写入 `public.rag_conversation_logs.metadata.router_debug`：

```json
{
  "router_debug": {
    "router_evidence_details": {
      "candidate_mode": "rag",
      "final_mode": "no_data",
      "fallback": "rag_without_fts→no_data",
      "thresholds": { "ddl_topk": 3, "ddl_min_score": 0.05, "fts_topk": 3 },
      "ddl_candidates": [{ "title": "DDL: customer_info", "score": 0.03 }],
      "fts_candidates": [{ "id": "123", "path": "docs/a.md", "score": 0.1 }]
    }
  }
}
```

写入要求：
- debug 开关开启才写
- 写入失败不得影响对外响应（best-effort）

---

## 验收标准（必须可操作）

### 1) 契约/manifest 门禁（阻断项）
- [x] `_contract_manifest.json` 已包含 `router.evidence.details` 的 `type_values` 与 payload 最小键
- [x] `_manifest.json` 已包含 `DEBUG_ROUTER_EVIDENCE`
- [x] `python tools/tech_graph_contract_check.py` 通过
- [x] `python tools/tech_graph_manifest_check.py` 通过

### 2) 行为验收（阻断项）
- [x] `DEBUG_ROUTER_EVIDENCE=0`（默认）时：不输出 `router.evidence.details`，且不落库
- [x] `DEBUG_ROUTER_EVIDENCE=1` 时：
  - [x] JSON：`/api/py/unified/chat` 返回的 `events[]` 包含 `router.evidence.details`
  - [x] SSE：`/api/py/unified/chat/stream` 的 `chain` 包含 `router.evidence.details`
  - [x] `rag_conversation_logs.metadata.router_debug.router_evidence_details` 可查到对应结构（仅候选摘要）

### 3) 测试验收（阻断项）
- [x] pytest 覆盖至少 1 条用例：开启 `DEBUG_ROUTER_EVIDENCE=1` 时断言 `router.evidence.details` 出现

---

## 实现备忘

- `ddl_candidates` 建议直接复用 `get_text2sql_store().search(query, top_k=ddl_topk)` 的返回列表（截断后落事件/落库）
- `fts_candidates` 建议复用 `keyword_documents` 的 top_k 结果（仅 id/path/score）
- 注意：`tools/tech_graph_contract_check.py` 只能从 `_event(... payload={...})` 的 **字面量 dict** 提取键名；实现时避免使用 `payload=some_function()` 这种写法，否则门禁无法通过。

