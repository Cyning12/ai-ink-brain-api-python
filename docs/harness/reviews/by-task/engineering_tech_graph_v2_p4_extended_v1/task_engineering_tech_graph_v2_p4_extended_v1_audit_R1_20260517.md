# 任务审核：技术图谱 graph_v2 P2-4 扩展 + 闸口 B follow-up（R1）

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md`（**v0.2** · 10 帽结构化） |
| **上一轮审查** | 无（首轮 R1） |
| **关联 SPEC / 材料** | `docs/tech_graph/改进方向.md`（v1.1.3）；`docs/_tech_graph/graph_v2_schema.md`；`docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md` |
| **前置关账** | `docs/harness/reviews/by-task/engineering_tech_graph_v2_graph_query_v1/task_engineering_tech_graph_v2_graph_query_v1_audit_CLOSE_20260517.md` |
| **轮次** | R1 |
| **审查日期** | 2026-05-17 |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260517_22_tech-graph-v2-p4-task-audit-r1.md` |
| **对照规约** | `docs/harness/prompts/hats/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5、`handoff/HANDOFF_SEMI_AUTO.md` |
| **人工闸（审查时）** | `HG-TASK-DRAFT: approved`；`HG-AUDIT-R1: pending`（**须人签后** 执行帽方可开工） |

---

## 审查结论摘要

task **v0.2** 与前置 **CLOSE** 延后项（P2-4 + follow-up）、P2-0 schema 基线、闸口 B 产品决议 **方向一致**。Harness §5（`test_strategy: required`、`failure_paths` FP-4-x + FP-5、分期 §2.2）**可支撑执行拒开工门闸**。

**相对前置 R1（B-D1）**：本 task 已把 P2-4 从「延后幻想字段」收敛为 **4a 必做 / 4b·4c 可选**，**无**「P2-0 误塞 graphs/ref」类硬阻塞。

**结论（零硬阻塞）**：**建议执行帽从 P2-4a 开工**；**首 PR 宜拆子阶段**（见焦点 1 · **N-1**，非阻塞）。**30 开工前** 人须将 **`HG-AUDIT-R1`** 置 `approved`。

---

## R1 审查焦点 — 逐项结论

| # | 焦点 | 结论 |
|---|------|------|
| 1 | P2-4a 是否过重、首 PR 能否再砍 | **范围合理**（CLOSE 已整包延后 P2-4）。**首 PR 建议再砍**：**4a-1** 仅 `nodes[].kind` + `validate_graph_v2` 条件分支（P2-0 无 kind 仍绿 · FP-4-4）；**4a-2** 再上 `graphs[]` + `edges[].ref` + 导出/等价。三字段同 PR 风险可控但 **FP-4-3** 面更大 → **N-1** |
| 2 | §2.2 与 `post_close` | **一致**：4a **阻塞关账**；4b/4c **不阻塞**；执行期 30→40 + CI，关账人审 `HG-AUDIT-CLOSE` ✓ |
| 3 | `test_strategy: required` + note | **可失败自动化已具备基线**：`tests/test_tech_graph_graph_v2_equivalence.py`、`test_tech_graph_graph_export.py`、`test_tech_graph_graph_query.py`；`tools/tech_graph_graph_v2_schema.py` 现 **禁止** P2-4 字段（须升级为条件校验）。执行帽 **须** 增 P2-4 正反用例（非法 `ref`/未知 `graph_id` 非 0）方满足 note ✓ |
| 4 | FP-4-1～FP-4-4 ↔ §3 | **映射完整**；§3.1 第 3 条（无 P2-4 时 P2-0 等价）↔ **FP-4-4** ✓；§3.1 非法组合非 0 ↔ **FP-4-2** + schema 测试 ✓ |
| 5 | NR-1 / FP-5 / FP-4-3 | **足以拦住**：NR-1 + §1.2 禁主实验重跑；FP-5 + G-END-5 + 非范围整包 v2；FP-4-3 + §1.2「query 默认不多读分图」+ query pytest ✓ |
| 6 | `freeze_id` TBD | **已标注** merge 前 bump；**非阻塞**（**N-2**） |
| 7 | P2-4c vs 闸口 B follow-up | **语义一致**（T002 · `upstream`/`neighbors` · 无全 batch 重跑）。**文案**：报告为 **§5 项 4**，task 多处写 **「§5.4」**（无该小节号）→ **N-3** 建议统一为「§5 项 4」 |

---

## Harness §5 核对

| 字段 / 小节 | 状态 | 备注 |
|-------------|------|------|
| `semi_auto` + `audit_profile: post_close` | ✓ | 与 §2.2、human_gate 表一致 |
| `test_strategy: required` + note | ✓ | 执行期须补 P2-4 专用 pytest |
| `failure_paths` | ✓ | FP-4-1～4-4 + FP-5；含 CI 可见列 |
| `freeze_id` | TBD | N-2 |
| 验收 §3.1～3.3 | ✓ | 4a 必达 / 4b·4c 可选分层清晰 |
| 必读 §5 | ✓ | NR-1、schema 升级顺序、freeze 对齐 |
| `human_gate` | ✓ | HG-TASK-DRAFT 已 approved；**HG-AUDIT-R1 仍 pending → 阻塞 30** |

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **硬阻塞** | — | **无** |
| **流程阻塞（非 task 正文）** | G-30 | **`HG-AUDIT-R1: pending`** → 执行帽 **30** 在 `blocks_hats` 内；R1 落盘后 **须人改 approved** |
| **非阻塞（执行策略）** | N-1 | 首 PR 建议 **4a-1（kind）→ 4a-2（graphs+ref）**；task 允许整包 4a，执行帽自选拆分须保持单 PR 内 pytest 绿 |
| **非阻塞（merge 前）** | N-2 | `TECH_GRAPH_S2_FREEZE_TBD` → 与 `protocol_version.yaml` · `graph_v2_freeze_id` bump |
| **非阻塞（文案）** | N-3 | 「§5.4」→ 建议改为「`conclusion_gate_b` §5 项 4」 |
| **非阻塞（schema 澄清）** | N-4 | §2.1 须执行期在 `graph_v2_schema.md` 定稿：`ref` 与 `from`/`to` **互斥或共存**规则；`graph_id` 在 node/edge 上的落点 |

---

## 需任务帽回填清单

**无硬阻塞回填。** 可选（**N-3**）：修订 task 头与 §5 中「§5.4」为「§5 项 4」——**不阻执行**。

---

## 是否建议执行帽开工

**建议**（在 **`HG-AUDIT-R1: approved`** 之后）。从 **P2-4a** 开工：

1. 升级 `tech_graph_graph_v2_schema.py`：**有则校验、无则 P2-0 兼容**（现 FORBIDDEN_* 须重构）。  
2. 更新 `graph_v2_schema.md` § P2-4。  
3. `test_strategy: required` — **先** 增失败测试（含 FP-4-4 回归：无 P2-4 字段图仍 PASS）。  
4. **禁止** 本阶段改 `graph_query` 默认多分图行为；**禁止** `run_gate_b_batch` 全 arms（NR-1）。  
5. 合并前：`pytest tests -m "not intent_eval and not intent_benchmark"` + `export --check` + 等价 CI。

---

## 签收 / 关闭

- **本轮（R1）**：**不声明 task 实现完成**；**声明任务文档层可进入执行**（零硬阻塞）。  
- **任务正式关闭条件（供终轮）**：§3.1 P2-4a 全勾 + CI 绿 + `freeze_id` 已 bump + §9/CLOSE_TRACE；可选 4b/4c 不阻关账（与 task §2.2 一致）。

---

## 下一棒可复制 Prompt

以下与 **对话回复** 中「下一棒」块 **逐字一致**。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md

【人工闸 — 开帽前必读】
task 文首 HG-AUDIT-R1 须为 approved 且 blocks_hats 含 30；若为 pending → 仅输出阻塞说明，禁止改业务代码。

输入（占位符已替换）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_v2_p4_extended_v1.md
- 子仓根（相对 Projects/）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/by-task/engineering_tech_graph_v2_p4_extended_v1/task_engineering_tech_graph_v2_p4_extended_v1_audit_R1_20260517.md
- 关联 SPEC / 总规：
docs/tech_graph/改进方向.md（v1.1.3）；docs/_tech_graph/graph_v2_schema.md；docs/diary/jsonPKmermaid/reports/conclusion_gate_b_ctx_query_v1_zh.md

你必须完成：
0. Invoke 快照：按 docs/harness/invokes/README.md 将本消息全文落盘后再开工。
0b. 确认 HG-AUDIT-R1: approved；否则拒开工。
1. 通读 task v0.2 与 R1 审查 N-1：从 P2-4a 开工；建议首 PR 仅 kind + schema 条件分支（4a-1），次 PR graphs[]+ref（4a-2）；禁止单 PR 塞 4b/4c/多分图 query。
2. 升级 tech_graph_graph_v2_schema.py（现 FORBIDDEN 须改为有则校验）；更新 graph_v2_schema.md。
3. test_strategy: required — 先增失败 pytest（含无 P2-4 字段时 FP-4-4 回归、非法 ref 非 0），再改导出/等价。
4. 禁止：graph_query 默认多读分图；run_gate_b_batch 全 arms 重跑（NR-1）；默认整包 v2 进 prompt（FP-5）。
5. P2-4a 首 merge 前 bump freeze_id 与 fixtures/gate_ctx_ab_v1/protocol_version.yaml 对齐。
6. 子仓根执行 VERIFY；回填 task「### 自检结论（执行者）」。
7. semi_auto：完成后再落盘 40 自检 invoke 并 commit（若 HG 无阻塞）。
8. 按 HANDOFF_AUTO_COMMIT 提交本轮代码/测试/task 变更。

禁止：扩 scope 至 Neo4j/退役 .ai.md；无测试静默放开 graphs[]/ref/kind。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-17 | R1：零硬阻塞；建议 P2-4a 开工；HG-AUDIT-R1 仍须人签；首 PR 宜 4a-1→4a-2 |
