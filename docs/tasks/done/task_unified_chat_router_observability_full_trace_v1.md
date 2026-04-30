# Task：Unified Chat（后端）— Router Observability Full Trace 落库（v1）

> **状态**：done（2026-04-30 验收通过）  
> **关联图谱**：无（仅补齐可追溯日志，不改业务流程）  
> **关联 Issue/PR**：无  
> **前端依赖**：无（本任务仅落库；前端展示/查询另起任务）  
>
> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done（YYYY-MM-DD 验收通过）` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/done.md` 索引。

---

## 背景与目标

当前系统已具备：
- `router.evidence`（聚合统计）
- `router.evidence.details`（候选摘要 + 阈值 + fallback）
- `rag_conversation_logs.metadata.router_debug.router_evidence_details`（候选摘要落库）

但排障时仍存在“追溯断点”：
- 只知道最终 `fallback` 与候选摘要，不知道 **检索时的输入参数**、**每一步耗时**、以及“当时到底执行了哪些路由/检索动作”
- 仅靠事件回放不稳定（SSE 客户端中断/网络波动）；仅靠结果快照又缺少过程细节

目标：在不引入新表/不阻塞响应的前提下，补齐 **Router 全过程可追溯（Full Trace）** 的 DB 落库结构，做到：
- 事后可以按 `session_id` 定位到单次请求的 trace
- 能复盘“为什么降级、降级前看过什么证据、阈值/参数是什么、耗时是否异常”

---

## 范围

- [x] **新增落库结构**：写入 `public.rag_conversation_logs.metadata.router_debug.router_trace_v1`
- [x] **覆盖路径**：`/api/py/unified/chat`（JSON）与 `/api/py/unified/chat/stream`（SSE）两条路径均写（best-effort）
- [x] **开关策略**：
  - [x] 默认开启 DB trace（便于事后追溯），支持通过 env 关闭
  - [x] 支持请求级 `debug_router: true` 强制开启（即使 env 关闭）
- [x] **安全与体积约束**：严禁落库敏感/大字段，必须截断与限量
- [x] **测试与门禁**：新增最小 pytest 覆盖 + tech_graph manifest 同步

---

## 非范围

- 不改变路由决策逻辑（`api/intent_router.py` 的 candidate/fallback 逻辑不动）
- 不新增前端 UI（如需面板展示/查询能力，另起前端任务单）
- 不引入新数据库表/索引（仅复用 `rag_conversation_logs.metadata` JSONB）

---

## 落库位置（真值）

- **表**：`public.rag_conversation_logs`
- **列**：`metadata`（JSONB）
- **路径**：`metadata.router_debug.router_trace_v1`

> 说明：`router_evidence_details` 继续保留；`router_trace_v1` 属于更“过程化”的补充，二者并存。

---

## 数据结构：`metadata.router_debug.router_trace_v1`

### 顶层结构（建议）

```json
{
  "router_trace_v1": {
    "ts_ms": 1714460000000,
    "run_id": "uuid",
    "mode": "no_data",
    "prefer": "auto",
    "debug_router": false,
    "timing_ms": {
      "router_decide": 4,
      "ddl_search": 12,
      "fts_search": 36,
      "total": 120
    },
    "ddl_search": {
      "query_text": "原始 query（截断）",
      "topk": 3,
      "min_score": 0.05,
      "returned": 3,
      "candidates": [
        { "title": "DDL: customer_info", "score": 0.0 }
      ]
    },
    "fts_search": {
      "query_text": "原始 query（截断）",
      "match_count": 3,
      "returned": 0,
      "candidates": [
        { "id": "123", "path": "docs/a.md", "score": 0.12 }
      ]
    },
    "decision": {
      "candidate_mode": "text2sql",
      "final_mode": "no_data",
      "fallback": "text2sql_without_ddl→no_data"
    },
    "events_digest": [
      { "type": "router.decision", "step_id": "r1", "ts": 12 },
      { "type": "router.evidence", "step_id": "re1", "ts": 13 }
    ],
    "errors": [
      { "stage": "ddl_search", "message": "..." }
    ],
    "v": "router_trace_v1"
  }
}
```

### 字段说明（约束）

- **`query_text`**：必须截断（建议 200 字符），禁止写入任何“文档 content/DDL content”
- **`candidates`**：
  - DDL：仅 `{title, score}`（title 截断 120）
  - FTS：仅 `{id, path, score}`（path 截断 180）
- **`events_digest`**：仅保存极简摘要（type/step_id/ts），不保存 payload（避免膨胀/泄露）
- **`errors[]`**：仅保存 stage 与 message（message 截断 300）
- **`timing_ms`**：用整数毫秒

---

## 开关与默认策略（建议）

新增 env（需要加入 `docs/_tech_graph/_manifest.json`）：
- `DEBUG_ROUTER_TRACE_DB`：默认 `"1"`，控制是否写入 `router_trace_v1`

请求级覆盖：
- body 传 `debug_router: true` 时，**强制写入**（并保持对前端输出 `router.evidence.details` 的既有逻辑不变）

> 说明：现有 `DEBUG_ROUTER_EVIDENCE_DB` 负责 `router_evidence_details`；本任务新增 `DEBUG_ROUTER_TRACE_DB` 用于 full trace，避免语义混淆。

---

## 性能与可靠性约束

- 写入必须 **best-effort 异步**（不得阻塞对外返回）
- 单条 trace 体积控制：建议上限 **≤ 8KB**（超过则进一步截断/丢弃非关键字段）
- 任意写库失败不得影响 `ok/mode/answer` 返回

---

## 验收标准

### 门禁与真值同步（阻断项）
- [x] `docs/_tech_graph/_manifest.json` 增加 `DEBUG_ROUTER_TRACE_DB`
- [x] `python tools/tech_graph_manifest_check.py` 通过

### 行为验收（阻断项）
- [x] 默认（`DEBUG_ROUTER_TRACE_DB=1`）时：每次 unified_chat 请求都会在 `metadata.router_debug.router_trace_v1` 写入一份 trace（best-effort）
- [x] `DEBUG_ROUTER_TRACE_DB=0` 时：不写入 `router_trace_v1`
- [x] 请求体 `debug_router: true` 时：即使 `DEBUG_ROUTER_TRACE_DB=0` 也会写入 `router_trace_v1`
- [x] trace 中不包含 `content/ddl` 等大字段；符合截断/限量约束

### 测试验收（阻断项）
- [x] pytest 至少 1 条用例：模拟一次请求，断言写入 payload 结构包含 `router_trace_v1.v` / `decision` / `timing_ms`

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/unified_chat.py`（落库点）、可能需要 `api/intent_router.py` 暴露 timing hooks（如需） |
| 关键 env | `DEBUG_ROUTER_TRACE_DB` |
| 数据库表 | `public.rag_conversation_logs`（无需迁移） |
| 图谱变更点 | `docs/_tech_graph/_manifest.json` |

