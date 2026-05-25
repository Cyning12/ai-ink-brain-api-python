# 任务审核 · R2

## 元信息

| 字段 | 值 |
|------|-----|
| 关联 task | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_perf_compare_v1.md` |
| 审查轮次 | R2 |
| 落盘日期 | 2026-05-15 |
| 上一轮审查 | `ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R1_20260515.md` |
| invoke_snapshot | `docs/harness/invokes/invoke_20260515_22_gate-a-scheme1-perf-compare-task-audit-r2.md` |
| invoke_snapshot（需求帽 · 可选追溯） | `docs/harness/invokes/invoke_20260515_10_gate-a-scheme1-perf-compare-requirements.md` |
| 关联 SPEC / 总规（本轮对照 task 元信息） | `docs/tech_graph/改进方向.md`；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md`；`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md` |

**给下一棒**：本 R2 审查全文真值在本文件；与 R1 相比 **收尾门闸仍未闭合**；下一棒可复制 Prompt 见文末 **`text`** 围栏（与对话逐字一致）。

---

## 审查结论摘要

- **与 R1 的差异**：对照当前 task 正文，**§4.2** 中 **「PR / CI」**、**「归档」** 仍为 **`[ ]`**；头部 **`状态`** 仍为 **`draft`**；**`### 实现备忘`** 中 **「PR / commit」** 仍为待回填占位。与 R1 审查中列出的 **阻塞项** 一致，**未见**任务帽或维护者在本轮复审前完成约定回填。
- **HARNESS_V2_PLAN §5**：`test_strategy: recommended` 与 `test_strategy_note` 成对出现，**未**滥用 `not_applicable`；**未**声明 `required`，故 **不**要求闸口 A 主结论必须先有「失败即红」的 pytest 断言；与 §5.1 表及 task §6 自述一致。
- **`failure_paths`**：FP-A～I 表结构完整（触发 / 行为 / 可重试 / 用户可见类型），与验收 §4.1、§9 文档张力及 §7 必读可对照执行。
- **头部元信息**：`freeze_id`、`test_strategy` / `test_strategy_note`、`invoke_snapshot`（需求帽）齐全；**未**见显式 **`gates_before_code`** 字段，按规划 §5.4 视为隐式门闸（失败路径 + 验收 + 必读已由 task 覆盖），**不**构成本轮阻塞。
- **验收可观测性**：§4.2 未勾两项为 **可机械核对**（PR 描述留痕、`git mv` + `_views`）；§4.2 已勾项与专文 / 自检结论在 task 内自洽，**不因**收尾未做而推翻既有文档交付结论。

---

## 阻塞 / 非阻塞

| 类型 | 项 | 说明 |
|------|-----|------|
| **阻塞（整单 Harness 签收）** | §4.2「PR / CI」「归档」未勾；`状态: draft`；实现备忘 PR/commit 未填 | 与 R1 **同一组**计划内收尾门闸；未完成前 **不得**在终轮审查中声明本 task 可签收关闭。 |
| **非阻塞（相对 R1 的文档与 §5 对齐）** | `test_strategy`、`failure_paths`、`freeze_id`、已勾验收项、§10 自检要点 | 本轮复审 **未**发现相对 R1 的 **新增**文档矛盾或 §5 违规。 |

---

## 需任务帽 / 维护者回填清单

- [ ] PR 合入后：勾选 task **§4.2**「PR / CI」；在 **`### 实现备忘`**「PR / commit」填入短 hash 或 PR 号（**勿**将 Actions run id 写入头部 **`freeze_id`** 行）。
- [ ] 验收完成后：按 `docs/tasks/README.md` 执行 **`git mv`** 至 `docs/tasks/done/` 并更新 **`docs/tasks/_views/done.md`**（及曾列入的 **`design.md` / `in_progress.md`**），勾选 §4.2「归档」。
- [ ] （可选）task 头部 **`invoke_snapshot`** 增链本帽 R2 invoke：`docs/harness/invokes/invoke_20260515_22_gate-a-scheme1-perf-compare-task-audit-r2.md`（与 R1 建议的第二行审核快照一致）。
- [ ] 上述完成后：发起 **R3** 任务审核（见文末下一棒 Prompt 中的 **任务审核** 变体，或先走需求帽整理再 R3）。

---

## 是否建议执行帽开工

**否。** 依据 `docs/harness/prompts/hats/22-task-audit.md`：**仍有 R1 已标明的原子验收未闭合**；且当前阻塞为 **PR 文案 / CI 留痕 / 仓库归档与 task 勾选**，**不属于**再开一轮业务代码实现的范围。

---

## 签收 / 关闭

本 R2 **不对**本 task 作 Harness **终局签收**。**签收 / 关闭** 延至 **§4.2 全勾**、实现备忘与头部状态与仓库事实一致，且 **R3（或后续）审查文档** 明确可关闭时落盘。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
依据 `ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_gate_a_perf_compare_v1/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md` 的回填清单：在 PR 已合入并完成 `docs/tasks/README.md` 规定的 `git mv` 至 `done/` 与 `_views` 更新后，指导或起草对 `task_engineering_tech_graph_gate_a_perf_compare_v1.md` 的更新——勾选 §4.2「PR / CI」「归档」、填写 §10 实现备忘 PR/commit、按实更新头部 `状态`；不得将 Actions run id 写入头部 `freeze_id` 行；可选为头部 `invoke_snapshot` 增加 R2 审核 invoke 链接。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_perf_compare_v1.md
ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_gate_a_perf_compare_v1/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_gate_a_perf_compare_v1/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
3. 若 AUDIT 路径非「无」：按该审查文档的回填清单逐条映射到 task 小节建议，并在建议文末注明「按审查 R2 回填」应指向的文件名。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值。
5. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。

不强制落盘；若用户要求写入某 task 文件，须由用户明确路径后再编辑（本模板不预置写文件占位符）。
```
