# 任务审核：闸口 C′ — graph_v2 查询轨 impact F1 提升与对照重跑

## 元信息

| 项 | 内容 |
|----|------|
| **关联 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md`（**v0.1**） |
| **关联 SPEC / 总规** | `Projects/docs/tech_graph/改进方向.md`（**R4** 闸口 C **accepted**、C′ 为深化不重跑 A/B）；`Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` |
| **轮次** | **R1**（首轮） |
| **审查日期** | 2026-05-20 |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_40_tech-graph-gate-c-prime-f1-audit-r1.md` |
| **对照规约** | `docs/harness/prompts/22-task-audit.md`、`docs/harness/HARNESS_V2_PLAN.md` §5、`HANDOFF_SEMI_AUTO.md` |
| **git_branch** | `task/engineering-tech-graph-gate-c-prime-f1-v1` |
| **audit_profile** | `post_close` |
| **前置（只读）** | canonical run `gate_ctx_c_v1_batch_20260518_052803`；`conclusion_gate_c_v2_dual_track_v1_zh.md`（**accepted**）；`task_engineering_tech_graph_v2_query_coverage_v1.md`（done） |

---

## 审查结论摘要

task **v0.1** 与闸口 C **accepted** 结论、方案2 SPEC、Harness §5 字段 **整体对齐**。**§0.2** 强制优先级（impact F1 → token 约束 → C′ batch）与 **§1.3** 分期一致；**PR-2** 明确为 **PR-1 超 token 限时** 才触发，不与 F1 主 KPI 倒置。**NR-1～NR-7** 与 **FP-CP1～CP5** 可映射到拒开工 / materialize exit / 变更请求语义；**`test_strategy: required`** 在 `test_strategy_note`、§3.1（materialize + `test_gate_ctx_c_v1_materialize.py`）、§3.2（`score_gold_f1` + pytest 主链）上可执行。

**§2.1** 基线表与 canonical **`052803`** 中 **D 臂（`CTX_V2_QUERY`）** 的 `gold_f1.md` **逐题一致**（entry / impact F1 与中位数可复算）。**§3.2** 阈值（impact 中位数 ≥0.45 或 T002 D ≥0.55；entry 单题 Δ≤0.05、中位数 ≥0.80；token 中位数 ≤ canonical D×1.25）均可由 **`score_gold_f1.py`** 产出 + 与 §2.1 对照完成验收。

**本轮结论**：**零硬阻塞**（无需任务帽 R2）。**不**代填 **`HG-GATE-C-PRIME-SIGNOFF`**（关账闸，不阻 **30**）。**建议执行帽开工**（见下表）。

---

## 阻塞 / 非阻塞

| 类型 | ID | 说明 |
|------|-----|------|
| **已核对通过** | ✓-1 | **`HG-TASK-DRAFT: approved`** — 满足 `blocks_hats: 22-R1, 30`；R1 可落盘、**30 可开** |
| **已核对通过** | ✓-2 | **PR-3 新 run** vs **NR-1**：新目录 `gate_ctx_c_v1_batch_<YYYYMMDD>_*`；**FP-CP1** 禁止改 canonical jsonl — 与「不覆盖 052803」一致 |
| **已核对通过** | ✓-3 | **F1 优先 vs PR-2**：§0.2、§1.1 PR-2「仅 PR-1 超限时」、收缩顺序含 **须记录 F1 变化** — 不先砍切片再测 F1 |
| **已核对通过** | ✓-4 | **不推翻闸口 C**：§0.1、NR-6、§3.2 产品结论（维持 `CTX_V2_QUERY` 默认；E 仅 T002 impact 更高不构成改默认）— 与 `改进方向.md` 闸口 C 行一致 |
| **已核对通过** | ✓-5 | **NR-3**：不升 `CTX_DUAL_MD` 为 machine 默认；C′ 仅 D vs E 对照 |
| **已核对通过** | ✓-6 | **`failure_paths`** FP-CP1～CP5 触发/行为可操作 |
| **已核对通过** | ✓-7 | **`freeze_id`** / **`graph_v2_freeze_id`（输入 V2_3）** 与 query coverage 任务链一致；本 task bump `TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0` 不覆盖 canonical `TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0` |
| **已核对通过** | ✓-8 | **`test_strategy: required`** — 现有 `tests/test_gate_ctx_c_v1_materialize.py` 含 T002 `contract_slice`/gold/token 断言，可扩展 PR-1 |
| **非阻塞** | N-1 | task 头部 **`状态: draft`** 与 **`HG-TASK-DRAFT: approved`** 并存；建议任务帽将状态改为 `active` 或加注「draft=文稿态、闸已开」避免误读 |
| **非阻塞** | N-2 | §3.1 **PR-1 出口**「相对 post-coverage 物化」为 **定性**（载荷 diff / 说明），无数值 F1；量化验收在 **§3.2 PR-3** — 执行帽须在 PR-3 前完成物化并保留 diff 证据 |
| **非阻塞** | N-3 | §3.2 token「约 **600**」为启发式量级；执行时以 **052803** run 内 D 臂 `heuristic_tokens` **实测中位数 ×1.25** 为准，写入 C′ 结论表 |
| **非阻塞** | N-4 | 子仓分支 **`task/engineering-tech-graph-gate-c-prime-f1-v1`** 已存在（invoke 注「待 30 创建」可视为已提前检出）；**30** 仍须确认基于 **main** 且无未提交漂移 |
| **非阻塞** | N-5 | **`HG-GATE-C-PRIME-SIGNOFF`** `pending` — 仅阻 **50 / 关账**，符合 `post_close`；**30→40** 不受影响 |

### R1 重点核对清单（本 task 特有）

| # | 核对项 | 结论 |
|---|--------|------|
| 1 | PR-3 新 run vs NR-1 不覆盖 052803 | **通过**（NR-1 + FP-CP1 + §1.1 PR-3 新目录） |
| 2 | F1 优先序 vs PR-2 触发条件 | **通过**（§0.2、§1.3、PR-2 条件节） |
| 3 | 不推翻闸口 C accepted、不升 CTX_DUAL_MD 默认 | **通过**（§0.1、NR-3/6、§3.2 产品段） |
| 4 | §2.1 与 canonical `gold_f1.md` 可复现 | **通过**（已对照 `052803/gold_f1.md` D 臂） |
| 5 | §3.2 阈值可观测 | **通过**（`score_gold_f1` + 基线表） |

### §2.1 与 canonical 052803（D 臂 · 抽样核对）

| task | §2.1 entry | §2.1 impact | gold_f1 D 臂 entry | gold_f1 D 臂 impact |
|------|------------|-------------|--------------------|---------------------|
| T001 | 0.857 | 0.200 | 0.857 | 0.200 |
| T002 | 0.667 | 0.429 | 0.667 | 0.429 |
| T003 | 1.000 | 0.400 | 1.000 | 0.400 |
| **中位数** | **0.857** | **0.400** | **0.857** | **0.400** |

---

## 需任务帽回填清单

**无**（零硬阻塞，不要求 R2 才能执行）。

可选（非阻塞）：**N-1** 统一 task 头部 `状态` 与 `HG-TASK-DRAFT: approved` 表述。

---

## 是否建议执行帽开工

| 条件 | 建议 |
|------|------|
| **文档层（R1）** | **是 — 建议 30 开工** |
| **人工闸** | **`HG-TASK-DRAFT`** 已 `approved`；**勿**代填 **`HG-GATE-C-PRIME-SIGNOFF`** |
| **执行顺序** | **PR-1 →（条件 PR-2）→ PR-3**；遵守 **FP-CP2**（禁止跳过物化直接 batch） |
| **分支** | `task/engineering-tech-graph-gate-c-prime-f1-v1`（子仓 `ai-ink-brain-api-python`） |

---

## 签收 / 关闭

- **本轮（R1）**：**不声明 task 可 `done`**；**`HG-GATE-C-PRIME-SIGNOFF`** 仍为关账闸。  
- **R1 书面审查**：**通过（零硬阻塞）**；**签收：可进入执行帽（30）**。  
- **任务正式关闭条件（供终轮引用）**：§3 全勾选 + C′ 结论 md + **`HG-GATE-C-PRIME-SIGNOFF: approved`** + 40/50 与 `HANDOFF_CLOSE_TRACE`（若适用）。

---

## 下一棒可复制 Prompt

以下与 **对话回复** 中「下一棒」块 **语义一致**；执行前可读已落盘 invoke：

`ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md`

```text
你正在扮演工作区 Harness「执行编码帽（30）」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（开帽前扫描 human_gate；不得代填 approved）

【Git 前提】
- 子仓 ai-ink-brain-api-python：分支 task/engineering-tech-graph-gate-c-prime-f1-v1（自 main；确认无未提交漂移）
- 工作区根 Projects/：本 task 默认不改 docs/tech_graph/ 除非 C′ 结论需索引一行且人签

【输入】
- 主 task：
@ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_prime_f1_v1.md
- 任务审核（R1）：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_prime_f1_audit_R1_20260520.md
- invoke_snapshot：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md
- 闸口 C canonical（只读 · 基线 F1）：
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_v2_dual_track_v1_zh.md
- query coverage（已合 main · 物化起点）：
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_v2_query_coverage_v1.md
- 方案2 SPEC：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md
- 物化 / batch / 评分：
fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py
fixtures/gate_ctx_c_v1/query_seeds.json
fixtures/gate_ctx_c_v1/protocol_version.yaml
fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py
fixtures/gate_ctx_ab_v1/tasks.json
- 合并前验证：
pytest tests -m "not intent_eval and not intent_benchmark"

【开帽前硬检查】
0. 落盘 invoke（若尚未提交）：invoke_20260520_41_tech-graph-gate-c-prime-f1-execute.md
0b. human_gate：HG-TASK-DRAFT 须 approved；HG-GATE-C-PRIME-SIGNOFF 仍 pending（不阻塞 30）
1. 通读 task §0.2：**先 F1 物化，再 token，再 C′ batch**
2. 禁止覆盖 runs/gate_ctx_c_v1_batch_20260518_052803（NR-1 / FP-CP1）

【范围 · PR-1 → PR-2（条件）→ PR-3】
见 task §1.1～§1.3 与 invoke_41 全文；结论建议路径：
docs/diary/jsonPKmermaid/reports/conclusion_gate_c_prime_f1_v1_zh.md

【禁止】
NR-1～7；不代填 HG-GATE-C-PRIME-SIGNOFF approved；git add 勿扫无关 WIP

【交付】
1. 回填 task §6 +「### 自检结论（执行者）」
2. 输出下一棒 40 自检 Prompt（链 invoke_20260520_42）
3. HANDOFF_AUTO_COMMIT：仅本轮路径；报 short-hash
```
