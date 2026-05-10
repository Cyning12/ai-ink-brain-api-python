# V3 待办：Text2SQL 工具链延迟与可观测性（多轮场景）

## 元信息

- **状态**：backlog（V3 开工时纳入迭代）
- **背景会话**：多轮追问下 `text2sql_query` 的 `tool.call.start` → `tool.call.end` 间隔可达百秒级，期间无 SSE，体感「卡在 step5→step6」
- **关联代码**：`api/agent.py`（工具事件边界）、`api/tools.py::text2sql_execute`、`api/text2sql_core.py`、`api/text2sql_api.py`（聚合快路径参考）
- **图谱**：`_tech_graph/11_flow_text2sql.md`（确定性总结分支与 Agent 路径对齐）

## 背景与目标

当前 V2 Agent 路径下，`tool.call.start/end` 包住 **整段** `text2sql_execute`（DDL 检索 → 生成 SQL → 执行 → 总结），`ToolResult.latency_ms` 为整段墙时；**同一工具内串行两次** `chat.completions.create`（`llm_generate_sql` + `llm_summarize`），多轮时 prompt 随 `history_to_rewrite_block` 变长，上游排队时延迟叠加。V3 目标：**可观测、可预算、低冗余调用**，避免用户误以为挂死。

## 范围 / 非范围

- **范围**：Agent 路径 Text2SQL 工具、SSE 契约扩展（若需新版本头，与 `SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` 对齐）、可选配置项。
- **非范围**：替换 SiliconFlow、重写 Text2SQL 算法；本单仅列改进点与验收方向。

## 改进点（V3 实施清单）

1. **子阶段 SSE 或结构化耗时**
   - 在 `text2sql_execute` 内分段计时（retrieve / llm_sql / validate / db / llm_summary），写入 `ToolResult.data` 或专用 debug 事件；或在 `emit` 路径增加 `tool.subphase.*`（需评估契约版本 `X-ChatBI-Sse-Contract`）。
   - **验收**：多轮场景下前端可区分「在等模型」还是「在查库」，P95 可归因。

2. **Agent 路径复用确定性总结（跳第二次 LLM）**
   - `text2sql_api.py` 已有 `_try_summarize_aggregate`；`tools.text2sql_execute` 在「单行/单值数值」等条件下应走同一逻辑，避免简单 COUNT 仍调 `llm_summarize`。
   - **验收**：典型「多少条 / 几个」类查询仅 **一次** 生成 SQL 的 LLM 调用（或明确文档例外）。

3. **多轮上下文预算**
   - 对注入 `build_sql_prompt` 的 `dialogue_context`、`_text2sql_retrieve_query` 合并串设硬上限或摘要（已有 `TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`，可复核 grounding 行膨胀）。
   - **验收**：第 N 轮 prompt token 有上界或监控指标，延迟不随轮次线性失控。

4. **LLM 调用超时与降级**
   - `OpenAI` 客户端为 `llm_generate_sql` / `llm_summarize` 配置合理 `timeout`；超时返回结构化 `error_code`（与现有 `LLM_API_TIMEOUT` 语义一致），避免无限挂起。
   - **验收**：下游慢时用户在 T 秒内收到失败/降级事件，而非仅长等待。

5. **（可选）模型分级**
   - 总结阶段使用更小/更快模型（与 `SPEC-ChatBI-V2-Intent.md` 中「Intent 用 Turbo」思路一致），由 env 开关控制。
   - **验收**：配置项文档化；默认行为与 V2 兼容。

## 依赖与引用

- `docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md` — 事件枚举扩展时同步
- `docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §4.2 V3 — 可与结构化日志 / Trace ID 一并落地

## 验收标准（V3 开工时勾选）

- [ ] 多轮 Text2SQL 至少具备 **分阶段耗时** 或 **子阶段事件** 之一（可观测）
- [ ] `text2sql_execute` 对可判定聚合结果走 **确定性总结**，减少无谓 `llm_summarize`
- [ ] LLM 调用具备 **timeout** 与结构化错误码
- [ ] `_tech_graph/11_flow_text2sql.md` / `.ai.md` 与实现一致

## 实现备忘（回填）

- 由 V3 负责 Agent 回填：涉及文件列表、SSE manifest、环境变量表（`PROJECT_CONFIG`）

---

**给 Cursor**：关键词：`V3`、`backlog`、`text2sql_execute`、`tool.call`、`latency`、`_try_summarize_aggregate`、`_tech_graph`
