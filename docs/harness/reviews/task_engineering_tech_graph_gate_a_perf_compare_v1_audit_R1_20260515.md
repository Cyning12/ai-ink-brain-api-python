# 任务审核 · R1

## 元信息

| 字段 | 值 |
|------|-----|
| 关联 task | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_perf_compare_v1.md` |
| 审查轮次 | R1 |
| 落盘日期 | 2026-05-15 |
| 对照提交（非 `freeze_id`） | `ai-ink-brain-api-python`：`47a6f9e`（`docs(tech-graph,tasks): Gate A 性能对比专文单一真值与签收表`） |
| invoke_snapshot | `docs/harness/invokes/invoke_20260515_10_gate-a-scheme1-perf-compare-requirements.md`（需求帽） |
| invoke_snapshot（本帽） | `docs/harness/invokes/invoke_20260515_22_gate-a-scheme1-perf-compare-task-audit-r1.md` |
| 关联 SPEC / 总规（本轮已读摘要） | `docs/tech_graph/改进方向.md`；`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`；`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md`；`ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md` |

**给下一棒**：本 R1 审查全文真值在本文件；整单签收须待 §4.2 两项勾选后再开 **R2**；下一棒可复制 Prompt 见文末 **`text`** 围栏（与对话逐字一致）。

---

## 审查结论摘要

- **头部与 HARNESS_V2_PLAN §5**：`test_strategy: recommended` 与 `test_strategy_note` 一致，不要求闸口 A 主结论先以「失败即红」pytest 钉死，符合 §5.1 `recommended` 语义；`failure_paths` 表可操作化，含 FP-G / FP-H / FP-I 专条；头部 **`freeze_id`** 为 `TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`，**未**夹带 Actions run id，满足人工侧重与 task 自洽。
- **文档与口径（对照 commit 47a6f9e 及当前工作区文件）**：专文 `gate_a_scheme1_perf_compare_backend_detail.md` 含 **`#sec4-master-table`**、**`#sec9-perf-backend`**；§1 **CLI 真值**限定为 `tech_graph_graph_export.py` / `tech_graph_token_estimate.py`；§2 **§2 代号 A/B** 与 **计时 A/B** 分列，满足 **FP-G / FP-H / FP-I** 的反面约束。父文档 `gate_a_scheme1_backend.md` **「结论」** 将 **§3.2 浏览器**标为 **N/A** 于主结论，与 task §9 **T-1**、**FP-D/E/F** 一致；**未**把浏览器表当 Agent 主结论依据。
- **§8「已选」/ §10 自检 / 父文档 §6 / PR 一句**：task §8「总对比表主真值在专文」与 §10「PR 描述一句」及父文档 **「下一阶段」** 段「PR 描述须写一句：总对比表主真值在专文」、父文档 **§6** 四项 **`[x]`** 及 **§3.0** 链专文 **语义一致**；专文 §4 浏览器列 **N/A** 与父文档主口径一致。
- **§4.2 未勾项**：**「PR / CI」**与**「归档」**仍为 **`[ ]`**，与 task 状态 **`draft`**、实现备忘 **「PR / commit」** 行仍待回填 **一致**；属**计划内收尾门闸**，非「专文/父文档写错」类缺陷，但构成 **`22-task-audit` 意义上的整单未闭合**（故本 R1 **不写**终局「签收 / 关闭」）。

---

## 阻塞 / 非阻塞

| 类型 | 项 | 说明 |
|------|-----|------|
| **非阻塞（文档与证据链）** | FP-G / FP-H / FP-I、§3.2 N/A、`freeze_id` 行 | 专文锚点与术语表、CLI 真值、代号/计时分离、父文档结论与 §6 勾选与 task 口径对齐；满足本轮人工侧重。 |
| **阻塞（整单验收 / 闭环）** | §4.2「PR / CI」「归档」`[ ]` | **预期**：在 PR 描述留痕（复现命令、可选 Actions run id **仅**进 PR 描述/父文档快照区，**不**进 task `freeze_id` 行）、实现备忘回填 **commit/PR**、并按 `docs/tasks/README.md` 完成 **`git mv` + `_views`** 之前，**不得**将本 task 视为 Harness 终局签收对象。 |

---

## 需任务帽 / 维护者回填清单（可选；非改 task 正文则不必经任务帽）

- [ ] PR 合入后：task **§4.2**「PR / CI」勾选；**`### 实现备忘`**「PR / commit」填入短 hash 或 PR 号（**勿**将 run id 写入头部 `freeze_id` 行）。
- [ ] 验收完成后：`git mv` 至 `docs/tasks/done/` 并更新 **`docs/tasks/_views/done.md`**（及曾列入的 **`design.md` / `in_progress.md`**），勾选 §4.2「归档」。
- [ ] （可选）task 头部 **`invoke_snapshot`** 第二行链至本帽 `invoke_20260515_22_…`（与 task 第 7 行「审核帽首轮可追加第二行」一致）。

---

## 是否建议执行帽开工

**否。** 依据 `docs/harness/prompts/22-task-audit.md`：**仍有未勾选的原子验收（§4.2 两项）**，且主文档与专文交付已在子仓提交 **`47a6f9e`** 体现，**不宜**再以「新业务实现」名义指示执行帽开工；收尾以 **PR 文案、CI 留痕、仓库移动与 task 勾选** 为主，完成后请发起 **R2** 任务审核（见下一棒 Prompt）。

---

## 签收 / 关闭

本 R1 **不对**本 task 作 Harness **终局签收**；**签收 / 关闭** 延至 **§4.2 全勾**且 **R2（或后续）审查文档** 明确可关闭时落盘。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/22-task-audit.md（身份、禁止项、输出形状、交接物）
- docs/harness/reviews/README.md（文件命名、R1/R2 闭环）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths 等与 task 字段对齐）

输入（已由人工替换占位符；若你仍看到 {{…}} 或本段「待填」字样，须先追问用户，不得开工）：
- 待审 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_perf_compare_v1.md
- 关联 SPEC / 总规路径（无则写「无」）：
docs/tech_graph/改进方向.md
docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md
ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md
ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md
- 上一轮审查文档路径（首轮写「无」；复审必填）：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R1_20260515.md

落盘文件建议名（须与文内元信息一致；若与用户输入冲突以用户为准并追问）：
- 待审 task 在 **`ai-ink-brain-api-python/docs/tasks/`** 下：`ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md`（全文真值）；工作区 `docs/harness/reviews/` 可仅存指针链至此路径。  
- 否则：`docs/harness/reviews/task_engineering_tech_graph_gate_a_perf_compare_v1_audit_R2_20260515.md`

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 `docs/harness/invokes/README.md` 落盘到 `Projects/docs/harness/invokes/`（含元数据表 + 快照 fenced code）。你在步骤 3 落盘审查 md 时，须在文首元信息表增加 **`invoke_snapshot`** 指向该 invoke 文件（相对 `Projects/`）。同一会话内追问 **不** 再新增快照文件。
1. 通读待审 task 全文及头部元信息（状态、freeze_id、gates_before_code、test_strategy、failure_paths、验收、必读链接）。
2. 对照 HARNESS_V2_PLAN.md §5 检查验收可观测性、required 与可失败自动化测试说明。
3. 落盘一篇审查文档至 **上表路径**（与 `reviews/README.md`、`22-task-audit.md` 子仓规则一致）。
4. 文内结构：元信息 → 审查结论摘要 → 阻塞 / 非阻塞 → 需任务帽回填清单（若有）→ 是否建议执行帽开工 → 「签收 / 关闭」仅在终轮或明确不可关闭时写死 → **「下一棒可复制 Prompt」**（`text` 代码围栏，内为已替换占位符的下一棒 §3 全文；与 `22-task-audit.md` **交接物**（1）（2）逐字一致）。
5. 禁止仅在对话里说「过了」而不写 reviews；禁止在仍有阻塞时指示执行帽开工。
6. 不要写业务实现代码；不要擅自改写 task 正文。
7. **对话与归档**：① **对话回复** 中输出与步骤 4 审查 md 末节 **完全相同** 的下一棒可复制 Prompt 全文；② **禁止**仅用「见落盘审查」等语省略对话中的 Prompt 正文。
```
