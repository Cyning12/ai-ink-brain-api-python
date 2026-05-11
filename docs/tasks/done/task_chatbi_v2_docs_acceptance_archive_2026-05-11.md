# Task：ChatBI V2 —— 规格与任务「验收 + 归档」（文档层收口）

状态：**done（2026-05-11 验收通过）** — 本文件已按 `docs/tasks/README.md` 迁入 **`docs/tasks/done/`**；**不修改**总规 `SPEC-ChatBI-V2-Agent-Overview.md` §7 正文勾选；本页为 **Runner + diary + CI** 的收口索引  
日期：**2026-05-11**  
范围：后端 `ai-ink-brain-api-python` 之 **`docs/spec/v2-agent/`**、**`docs/tasks/`**（ChatBI V2 相关；**已闭环子任务见 `docs/tasks/done/`** 下表）  
**执行真值**：`docs/tasks/active/task_chatbi_v2_acceptance_runner_v1.md` **§2.9**（L0–L7）  
**简历对齐**：`docs/diary/简历评估意见-2026-5-9.md` **§三 / §七**（V2 主线与「补强中」边界）

---

## 1. 验收结论（文档层）

| 维度 | 结论 |
|------|:----:|
| **SPEC 目录** `docs/spec/v2-agent/` | **已对齐实现**：总规 §7.4/§7.5、子规、vNext 分层可读；详见 **`README.md`** 阅读顺序 |
| **Runner** `task_chatbi_v2_acceptance_runner_v1.md` | **L0–L7 本机/生产证据已回填 §2.9**；L0 等价 **GitHub Actions** 跑绿即可 |
| **缺口快照** `SPEC-ChatBI-V2-Gap-Checklist.md` | **仍为主规互补**；总规 §7.1 未勾项以 Gap + 简历 §七 为准 |
| **企业级路线图** | **`docs/spec/SPEC-ChatBI-Enterprise-Gap.md`**（非 v2-agent 子路径；V3/P1 已链 `task_chatbi_v3_text2sql_tool_latency_obs_v1.md`） |

**仍标「补强 / 未在本文宣告 100%」**（与简历一致）：总规 **§7.1** 多步双工具 **产品级 E2E 黄金用例 + 压测**；纸面 **§7.2 P50/P95** 与真实延迟差距（见 L2 归档）。

---

## 2. `docs/spec/v2-agent/` 文件清单（归档索引）

| 文件 | 角色 |
|------|------|
| `README.md` | 目录、阅读顺序、**V2 归档入口** |
| `SPEC-ChatBI-V2-Agent-Overview.md` | **总规**：§7 验收、§7.4、§7.5 L0–L7 |
| `SPEC-ChatBI-V2-Gap-Checklist.md` | 缺口快照 |
| `SPEC-ChatBI-V2-Intent.md` | 意图子规 |
| `SPEC-ChatBI-V2-Tool-Design.md` | Tool 子规 |
| `SPEC-ChatBI-V2-ReAct-Loop.md` | ReAct 子规 |
| `SPEC-ChatBI-V2-Memory.md` | 记忆子规 |
| `SPEC-ChatBI-V2-Multiturn-Semantics.md` | 多轮语义子规 |
| `SPEC-ChatBI-V2-Events.md` | 事件子规 |
| `SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` | **vNext**（V2 里程碑暂结后排期） |
| `SPEC-ChatBI-V2-Incremental-SSE-Clarification-Brief-vNext.md` | **vNext** 吸收索引 |

---

## 3. `docs/tasks/` —— ChatBI V2 任务索引（**done/** 与 **active/**）

### 3.1 已迁入 **`docs/tasks/done/`**（本归档日收口）

| 文件 | 说明 |
|------|------|
| `docs/tasks/done/task_chatbi_v2_agent_p1_behavior.md` | P1 总览（已闭环） |
| `docs/tasks/done/task_chatbi_v2_agent_p1_eval_benchmark_v1.md` | P1-Eval |
| `docs/tasks/done/task_chatbi_v2_agent_p1c_intent_cache_observability_v1.md` | P1-C |
| `docs/tasks/done/task_chatbi_v2_agent_p1d_intent_prompt_and_thresholds_v1.md` | P1-D |
| `docs/tasks/done/task_chatbi_v2_rewrite_timeline_llm_prompt_capture_v1.md` | RAG 改写上链 + LLM Prompt 可观测（2026-05-11 归档） |
| `docs/tasks/done/task_chatbi_v2_incremental_sse_backend_v1.md` | 增量 SSE + `agent.llm.*` 后端 v1（2026-05-11 验收归档） |
| `docs/tasks/done/task_chatbi_v2_text2sql_multiturn_grounding_v1.md` | Text2SQL 多轮 + 值域 / DISTINCT（**2026-05-11 完结归档**；欠债见 `active/task_chatbi_v3_debt_from_v2_multiturn_v1.md`） |

### 3.2 仍位于 **`docs/tasks/active/`**（推进中 / 排期 / V3）

| 文件 | 说明 |
|------|------|
| `task_chatbi_v2_acceptance_runner_v1.md` | **L0–L7 执行引导 + §2.9 勾选** |
| `task_chatbi_v3_debt_from_v2_multiturn_v1.md` | **V3 欠债**：承接 multiturn 未纳入 V2 的项（澄清 §4.3 等） |
| `task_chatbi_v3_planning_after_resume_v1.md` | V3 规划入口 |
| `task_chatbi_v3_text2sql_tool_latency_obs_v1.md` | V3 Text2SQL 延迟与可观测 |

**说明**：任务单物理目录以 **`active/` vs `done/`** 为准；本页 §3.1 为 **2026-05-11** 快照。

---

## 4. 关联 diary（证据链）

| 文档 | 内容 |
|------|------|
| `docs/diary/2026-05-10-l4-sse-acceptance-archive.md` | L4 + §7.5.5.1 curl |
| `docs/diary/2026-05-10-l5-failure-matrix-acceptance.md` | L5 矩阵 |
| `docs/diary/2026-05-10-l6-multiturn-ui-acceptance.md` | L6 UI 多轮 |
| `docs/diary/2026-05-10-l7-prod-acceptance.md` | L7 生产 |
| `docs/diary/简历评估意见-2026-5-9.md` | **V3/V4 叙述边界与面试话术** |

---

## 5. 给 Cursor 的稳定关键词

`task_chatbi_v2_docs_acceptance_archive_2026-05-11`、V2 归档、§7.5、Runner §2.9、`task_chatbi_v3_planning_after_resume_v1`
