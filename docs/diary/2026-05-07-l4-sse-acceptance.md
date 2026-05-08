# L4 — SSE 实链与前端 Timeline 验收归档（2026-05-07）

> 口径：`SPEC-ChatBI-V2-Agent-Overview.md` **§7.5.3**（L4）。  
> **L4 验什么**：流式 **SSE / `chain` 事件** 是否按契约产出、**前端能否稳定渲染**（未知 type 可忽略策略）；**不**将「Intent 是否超时 / 是否 v1_fallback」记为 L4 失败（属 **Intent 质量与超时策略**，见 P1 / `CHATBI_V2_INTENT_TIMEOUT_S`）。

---

## 1. 验收结论

| 路径 | 结论 | 说明 |
|------|:----:|------|
| **curl + 本机 API** | **通过** | `POST /api/py/unified/chat/stream`，响应落 **`/private/tmp/l4_sse_sample.txt`**：`meta` → `router.decision` → `agent.*` → `tool.*` → `sql.result` → `assistant.message` → `latency` → **`done`**（`ok: true`，`mode: text2sql`）；Intent 走 **text2sql_query**，业务侧为「未查到数据」属数据域，**非 L4 失败**。 |
| **前端（`ai-ink-brain` 流式）** | **通过** | Timeline 可见 **`meta` → `router.decision` → `agent.step.start` → `agent.intent` → `agent.think` → `tool.call.*` → `agent.step.end` → `agent.final` → `assistant.message` / `latency`**；**无白屏、无未捕获异常**即可视为 L4 通过。 |

---

## 2. 前端本轮可观测行为（摘要）

- **`router.decision`**：`candidate_mode` / `final_mode` 为 **`no_data`**，`evidence.agent_reasoning` 含 **「意图识别超时，降级到 V1 规则路由。」** — 对应 **`v1_fallback`** / Intent 上游超时后的 **V1 规则路由**，**允许**在 L4 中出现（验收关注「链路仍闭合、事件仍齐」）。  
- **`agent.intent`**：`direct_answer`，**`cache: miss`**，`latency_ms` 量级 **~61s**（与超时顶满一致）；随后 **`agent.think`** 与 **`tool.call.*`** 走 **`direct_answer`**，`tool.call.end` 有正常 **`output.answer`**。  
- **`latency.total_ms`**：**~64409 ms**（整轮 wall）。  
- **UI 提示**：「本轮 events 未发现 **router.evidence**」与 **`debug_router` 未开** 或路由证据未落事件一致，**不**影响 L4 通过。  
- **run 标识**：若 Timeline 顶栏 **`run=`** 与 **`meta.payload.run_id`** 不一致，多为 **多标签 / 多会话 / 复制混贴**；以 **当前条 `payload.run_id`** 为准排查。

---

## 3. 与 curl 样本的对照

| 维度 | curl 样本（`/private/tmp/l4_sse_sample.txt`） | 前端本轮 |
|------|-----------------------------------------------|----------|
| Intent 路径 | LLM **text2sql**，无超时降级 | **超时 → V1 → direct_answer** |
| 最终 `mode` | **text2sql** | **no_data** |
| L4 是否通过 | **是**（事件链完整） | **是**（事件链完整 + UI 正常） |

**结论**：**不必**依赖 curl；**前端调用同一 SSE 契约**即完成 L4 的「跨端」侧；两条路径差异体现 **环境与超时**，归档时分开描述即可。

---

## 4. 后续（非 L4）

- **降低 `v1_fallback` / 对齐查数意图**：调 **`CHATBI_V2_INTENT_TIMEOUT_S`**、上游模型与网络，见 **`docs/diary/2026-05-06-p1-intent-eval-session-result.md`** 与 `PROJECT_CONFIG`。  
- **L5–L7**：仍按 Overview **§7.5.4–§7.5.6**。

---

## 5. 关联

- `docs/diary/2026-05-07-l0-l3-regression-acceptance.md`（L0–L3）  
- `SPEC-ChatBI-V2-Agent-Overview.md` §7.5.3  
- `docs/_tech_graph/_contract_manifest.json`
