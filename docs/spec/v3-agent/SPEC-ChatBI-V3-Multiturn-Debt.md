# ChatBI V3 — 多轮与值域技术债（承接 V2）

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2** 支柱二、**§2.1** P1-4 / P2-3 / **P2 延伸（低置信方案确认）**  
> **任务单（母单）**：`docs/tasks/active/task_chatbi_v3_debt_from_v2_multiturn_v1.md`  
> **P1-4 implementation**：`docs/tasks/done/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`  
> **P2 延伸（需求）**：[`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`](SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md)（方案 B、预览、确认、门控升格）  
> **P1-4 前端（Ink-Brain）**：`ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`  
> **V2 规格交叉**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md`（尤其 **§4.3**）

---

## 0.1 与已交付 P0（Text2SQL 可观测）的衔接

**P0 单**（`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`）已提供：**SSE `text2sql.phase.*`**、**`tool.call.end.output.text2sql_phases_ms`**，以及可选 **`CHATBI_JSON_LOG`**（服务端单行 JSON，与 **`meta`/`done` 的 `run_id`** 同源）。  
落地 **§4.3 澄清轮**、编排与 SSE 新形状时，建议 **先**在 staging 打开 **`CHATBI_JSON_LOG`** 做 **E2E 留证**（grep 同 `run_id`）；生产默认可关，避免 stderr/采集量与序列化开销。Ink 侧 Timeline 已与 **`meta.payload.run_id`** 对齐（见 `P0/阶段B-验收-1.md` 文首说明）。

---

## 1. 背景

V2 已交付：`text2sql_grounding`、历史注入、`value_hints` YAML、DISTINCT 与字典并集（见已归档 multiturn 任务）。下列项 **刻意**留到 V3，避免与 V2 里程碑混验收。

---

## 2. 功能债（优先级建议）

| 主题 | 规格/产品要点 | V3 动作方向 |
|------|---------------|-------------|
| **低置信指代澄清** | `SPEC-ChatBI-V2-Multiturn-Semantics.md` **§4.3** | 触发阈值、澄清话术模板、**SSE `chain` 形状** 与 Intent/Agent 编排合单 |
| **低置信方案预览与确认（后 P1-4）** | P1-4 已能短路澄清，但缺少「将执行方案」可审阅性与 **编排 B** | 见 L1 [`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`](SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md)；任务 **`task_chatbi_v3_low_confidence_plan_preview_confirm_v1`**（`backlog`） |
| **`commission_structure` 同义与字面量** | YAML `logical_key` 与库枚举字面量易混 | 拆键名、改措辞或文档化「产品与解析」双真值 |
| **集成抽检扩展** | 性别口语、提成口语等 | 固定烟测集或可选 CI fixture |

---

## 3. 工程债（可选）

| 主题 | 说明 |
|------|------|
| **DISTINCT 节能短路** | 可选 env，**默认关**，保持防漂移并集（见 V2 任务 B.0-5） |
| **YAML / DISTINCT 漂移告警** | nightly 或 ingest 管线对比 |
| **`_tech_graph` 与现网** | 补 `11_flow_text2sql` 等与代码逐边对齐（双轨协议） |

---

## 4. 与 RBAC 的交叉

澄清轮若涉及 **敏感表名展示**，须在 [`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md) 中定义 **按角色脱敏** 规则后再合入产品。

---

## 5. 验收方向

- 澄清路径至少有 **1** 条 E2E（mock 或 staging）可演示。  
- 同义词 / 枚举边界有 **文档化** 决策记录（ADR 或任务单「实现备忘」）。  
- 不强制 DISTINCT 节能与漂移 CI **同 PR** —— 可按 P2-3 拆单。

---

## 6. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规（由总规拆分） |
| 2026-05-11 | **§0.1**：与 P0 Text2SQL 可观测单、`CHATBI_JSON_LOG`、Ink `run_id` 对齐留档衔接 |
| 2026-05-11 | 元信息：增加 **P1-4 前端** 任务路径（Ink `task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1`） |
| 2026-05-12 | **§2** 功能债表：登记 **低置信方案预览与确认**（交叉 **`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm`**）；元信息增加 **P2 延伸** 链接 |
