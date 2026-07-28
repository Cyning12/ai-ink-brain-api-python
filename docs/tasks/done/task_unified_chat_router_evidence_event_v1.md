# Task：Unified Chat（后端）— 新增 `router.evidence` 事件（降级前证据可视化）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


状态：done（2026-04-30 验收通过）  
范围：仅后端 `ai-ink-brain-api-python`  
关联：
- `docs/_tech_graph/_contract_manifest.json`（SSE 契约真值）
- `tools/tech_graph_contract_check.py`（契约门禁）
- `api/intent_router.py`（V1 路由与 evidence 采集）
- `api/unified_chat.py`（事件输出端点：JSON + SSE）

前端依赖策略（必须遵守）：
- 本任务只负责**后端事件与契约**。若需要前端展示（Timeline 新节点/面板），要求：**后端验收通过后**，由后端创建并编写对应前端任务单（包含 UI 交互与渲染方案），再进入前端实现。

---

## 背景与目标

当前 Unified Chat 的降级信息主要集中在 `router.decision.payload.evidence` 与 `fallback` 字段中，前端 Timeline 展开查看不够直观。

目标：新增一条独立事件 `router.evidence`，用于在 Timeline 中明确展示：
- “候选模式（candidate）→ 证据（ddl/fts）→ 最终模式（final）→ 降级原因（fallback）”的判定链路
- 以及关键阈值（topk/min_score）与命中统计，便于排查误降级/误路由

---

## 范围 / 非范围

### 范围

- 在 `POST /api/py/unified/chat` 的 `events[]` 中新增 `router.evidence`
- 在 `POST /api/py/unified/chat/stream` 的 SSE `chain` 中新增 `router.evidence`
- 同步更新 `_contract_manifest.json`：
  - `sse.chain.type_values` 增加 `router.evidence`
  - `payload_min_keys_by_type` 增加 `router.evidence` 的最小键集合
- 新增/更新 pytest 用例，确保 `router.evidence` 在路由阶段出现且 payload 满足契约

### 非范围

- 不改变路由逻辑（`candidate_mode/final_mode` 判定逻辑仍由 `api/intent_router.py` 决定）
- 不要求前端马上消费（前端收到未知 type 可忽略；但后续若要展示，另开前端任务）

---

## 事件定义（建议）

### 事件 envelope（保持与现有一致）

```json
{
  "type": "router.evidence",
  "ts": 120,
  "step_id": "re1",
  "payload": {
    "candidate_mode": "text2sql",
    "final_mode": "no_data",
    "fallback": "text2sql_without_ddl→no_data",
    "ddl": {
      "hits": 0,
      "top_score": null,
      "topk": 3,
      "min_score": 0.05
    },
    "fts": {
      "hits": 0,
      "top1_score": null,
      "topk": 3
    }
  }
}
```

### payload 最小键（用于 `_contract_manifest.json`）

- `candidate_mode`
- `final_mode`
- `fallback`
- `ddl`
- `fts`

其中 `ddl` 最小键：
- `hits`
- `top_score`
- `topk`
- `min_score`

`fts` 最小键：
- `hits`
- `top1_score`
- `topk`

---

## 验收标准（必须可操作）

### 1) 契约门禁（阻断项）
- [x] 更新 `docs/_tech_graph/_contract_manifest.json` 后，`python tools/tech_graph_contract_check.py` 通过

### 2) 行为验收（阻断项）
- [x] `prefer=auto` 时，`router.decision` 后紧跟输出 `router.evidence`
- [x] `router.evidence.payload` 与 `router.decision.payload` 对齐（至少 `candidate_mode/final_mode/fallback` 一致）
- [x] JSON（非流式）与 SSE（流式）两条路径都能输出该事件

### 3) 测试验收（阻断项）
- [x] pytest 覆盖：至少断言 `router.evidence` 出现，且包含契约最小键（建议复用/扩展现有 unified_chat 测试）

---

## 验收记录

### 契约门禁

```bash
python tools/tech_graph_contract_check.py
```

关键输出（节选）：

```text
OK: cross-repo contract check passed (backend truth covers contract; frontend reads within contract).
```

### 测试

```bash
pytest -q
```

关键输出（节选）：

```text
39 passed, 3 warnings in 0.87s
```

---

## 实现备忘

- `router.evidence` 的 payload 可以由 `api/intent_router.py::decide_intent()` 的 `evidence` 字段与相关 env 组合构造，避免重复计算：
  - ddl：`ddl_hits/ddl_top_score/INTENT_DDL_EVIDENCE_TOPK/INTENT_DDL_EVIDENCE_MIN_SCORE`
  - fts：`fts_hits/fts_top1_score/INTENT_FTS_EVIDENCE_TOPK`
- 事件位置建议紧跟 `router.decision` 之后，以便 Timeline 直观看到“决策 → 证据”。

