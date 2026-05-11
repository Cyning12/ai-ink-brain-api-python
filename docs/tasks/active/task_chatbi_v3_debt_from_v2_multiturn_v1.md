# Task：ChatBI V3 —— V2 多轮 / Text2SQL 值域相关**欠债**（承接自已完结子任务）

> **状态**：`backlog`（**仅在 V3 排期中考虑**；不阻塞 V2 主线）  
> **来源（已归档）**：`docs/tasks/done/task_chatbi_v2_text2sql_multiturn_grounding_v1.md`（V2 本子任务 **done**，A/B/C 与 PR1/PR2 已交付）  
> **统筹入口**：`docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md`  
> **V3 总规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md`（**§3** 任务归拢；**§2** 多轮技术债支柱）  
> **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Multiturn-Debt.md`  
> **关联规格**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md`（§4.3 澄清）、`docs/spec/SPEC-ChatBI-Enterprise-Gap.md`

---

## 0. 与 SPEC §2.1 批次对应（勿整单一次 PR）

| 本文件章节 | 总规批次 | 说明 |
|------------|----------|------|
| **§1**（澄清 §4.3、编排、SSE 形状） | **P1-4** | 与 **RBAC / 事件形状**（Overview **P1-3**）可能交叉，宜在 P1 内排期；**implementation 子任务**：[`task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`](./task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md)（`todo`）。 |
| **§1** 末行「集成抽检扩展」 | **P2-2** 协同 | 与 **评估 / 烟测集**（`SPEC-ChatBI-V3-Evaluation`）同批更省重复建设。 |
| **§2**（同义词、DISTINCT 节能、漂移 CI、图谱） | **P2-3** | 优化与非阻塞项；可多条小 PR，**不必**与 §1 同发布火车。 |

**结论**：本文件是 **欠债清单母单**，实施时按上表 **拆 PR / 拆子任务**；不要求「整单一次性 done」。

### 0.1 建议首包（P1-4 入口）

**§1 低置信澄清**：**P0 Text2SQL 可观测** 已归档（`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`）；排障与 E2E 留证复用 **`CHATBI_JSON_LOG`** + Timeline **`run_id`**。**implementation 子任务** 已登记：后端 [`task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`](./task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md)（`todo`）；前端 **Ink-Brain** `content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`（`pending`，**新 `chain.type` 须前后端同 PR + manifest**）。

---

## 1. 功能与产品语义（优先在 V3 拆解）

| 欠债项 | 说明 | 建议 V3 动作 |
|--------|------|----------------|
| **低置信指代澄清** | 规格 **§4.3**：表/列指代模糊或 Intent 置信不足时，向用户澄清而非硬猜。V2 仅 grounding + 值域提示，**无主动澄清轮**。 | 与 Intent / Agent 编排合单；定义触发阈值与 SSE 事件形状。 |
| **`commission_structure` 同义词与库内字面量** | YAML 同义词「提成结构→底薪加提成」与库内枚举字面量「提成结构」**同名**，易产生产品/解析歧义。 | 拆 `logical_key`、改措辞或 DISTINCT+字典分工说明。 |
| **集成抽检扩展** | V2 已抽检 `gender=保密` 等；「男性 / commission 口语」等仍可加抽。 | V3 建立固定烟测集或 CI 对真库 fixture（可选）。 |

---

## 2. 工程与运维（可选）

| 欠债项 | 说明 | 建议 V3 动作 |
|--------|------|----------------|
| **DISTINCT「节能短路」** | 任务 B.0-5：若将来要省 I/O，可增加「YAML 命中则跳过 DISTINCT」**可选 env，默认关**。 | 有成本压力时再开任务；默认保持防漂移并集。 |
| **YAML / DISTINCT 漂移 CI 告警** | 任务 B.4：可选对 fixture 做字典与库枚举差异告警。 | 与 ingest 或 nightly 对齐。 |
| **`_tech_graph` 与现网强一致** | 多轮 + Text2SQL 落库路径若产品要求图谱与代码逐边对齐。 | 按 `_tech_graph` 双轨协议补 `11_flow_text2sql` 等。 |

---

## 3. 验收与关键词

- **本文件**：不要求单独 CI；**被 V3 子任务引用时**再写验收 `- [ ]`。  
- **关键词**：V3、技术债、多轮澄清、§4.3、value_hints、DISTINCT、提成结构、`_tech_graph`
