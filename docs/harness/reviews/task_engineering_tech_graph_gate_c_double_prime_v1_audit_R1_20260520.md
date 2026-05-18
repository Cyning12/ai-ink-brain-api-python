# 任务审核 R1：闸口 C″ — 分题物化修补 T003 impact

## 元信息

| 字段 | 值 |
|------|-----|
| **轮次** | R1 |
| **日期** | 20260520 |
| **待审 task** | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md` |
| **关联 SPEC / 总规** | `Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md` · `Projects/docs/tech_graph/改进方向.md` |
| **上一轮审查** | 无 |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_51_tech-graph-gate-c-double-prime-task-audit-r1.md` |
| **10 帽 invoke** | `ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_50_tech-graph-gate-c-double-prime-requirements.md` |
| **freeze_id** | `TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0` |
| **audit_profile** | `post_close` |

---

## 审查结论摘要

**结论：零硬阻塞；书面审查通过 R1；建议在人签 `HG-TASK-DRAFT` 与 `HG-AUDIT-R1` 为 `approved` 后由执行帽（30）按 PR-1→PR-3 顺序开工。**

已核对：task 与闸口 C（`052803`）、C′（`083014`）accepted 结论及 `gold_f1.md` 数值一致；P0/P1/P-禁止 不推翻 `CTX_V2_QUERY` 默认；PR-1 T003 物化路径可落地（现有 `materialize_gate_c_payloads.py` 已具备 T002 三切片模式，可平移 T003）；§3.2 主 KPI（OR）与 T002 守卫阈值可量化；PR-4 与 NR-9 与 `HG-GATE-C-DOUBLE-PRIME-SIGNOFF` 阻塞链一致；`test_strategy: required` 与验收命令可观测；`failure_paths` FP-CDP1～8 具备拒开工/拒 scope 语义。

---

## 阻塞项

无（硬阻塞）。

---

## 非阻塞项（建议 · 可不阻断 30 开工）

| # | 项 | 说明 | 建议落点 |
|---|-----|------|----------|
| N1 | 结论状态机 | PR-3 未达 §3.2 时，`conclusion_gate_c_double_prime_v1_zh.md` 应标 `draft` 而非 `accepted`，避免与 PR-4/HG 冲突 | task §3.2 或 PR-3 验收末行 |
| N2 | T003 pytest 锚点 | 已有 `test_t002_subgraph_covers_gold_graph_ids` 范式；可增补 T003 对 `manifest_slice` / `impact_surface` 的 **示例 path**（如 `api/rag_env.py`、`supabase/sql`、`tools/tech_graph_manifest_check.py`） | task §3.1 或 PR-1 清单 |
| N3 | `freeze_id` 切换 | PR-1 写入 `gate_c_double_prime_freeze_id` 后，`query_seeds.json` / `materialize_report.freeze_id` 预期将切至 C″ freeze；须同步扩展 `test_protocol_freeze_ids_locked`（当前仅锁 canonical + C′） | task PR-1 或 §3.1 |
| N4 | T002 继承一句钉死 | 可增「**不修改** `materialize_gate_c_payloads.py` 中 `T002_unified_sse_chain_contract` 分支逻辑，仅新增 T003 分支」 | task §1.1 PR-1 |

---

## 需任务帽回填清单

无（均为上表非阻塞建议；执行帽可按 task 现有正文实施）。

---

## 是否建议执行帽开工

| 条件 | 状态 |
|------|------|
| 书面审查 R1 | **通过** |
| `human_gate` **HG-TASK-DRAFT** | `pending` → **须人** `approved`（建议与 R1 一并签） |
| `human_gate` **HG-AUDIT-R1** | `pending` → **须人** `approved`（本 R1 通过后） |
| `human_gate` **HG-GATE-C-DOUBLE-PRIME-SIGNOFF** | 保持 `pending`（**不**阻塞 30；**阻塞** PR-4 / 关账） |

**建议：30 帽在 `HG-AUDIT-R1` = `approved` 后开工；禁止在 HG 仍为 `pending` 时代填 `approved`。**

---

## 分项核对（重点审查）

### P0 / P1 / P-禁止 vs C / C′ accepted

| 检查点 | 结果 |
|--------|------|
| 维持 `CTX_V2_QUERY` / `graph_query` 默认 | §0.3 P0、§3.2 产品硬项与 `conclusion_gate_c_v2_dual_track_v1_zh.md` **accepted** 一致 |
| 不修订 C / C′ 结论文 | §3.2、NR-1～7 继承、P-禁止 明示 |
| 不升 `CTX_DUAL_MD` 默认 | P-禁止、NR-3 对齐 |
| 实验先行、rules 后置 | P1 + PR-4 条件 + NR-9 + `HG-GATE-C-DOUBLE-PRIME-SIGNOFF` 一致 |

### PR-1 T003 物化可执行性 · T002 继承

| 检查点 | 结果 |
|--------|------|
| T003 变量 | `manifest_slice` + `impact_surface` + 现有 `downstream(A2,2)`；gold 来自 `fixtures/gate_ctx_ab_v1/tasks.json` T003 `impacts[]` — **路径/kind 可枚举** |
| 实现锚点 | `materialize_gate_c_payloads.py` 已对 T002 实现 `_manifest_slice_sse_unified`、`_t002_impact_surface`（实为读 gold impacts）；T003 可增 **Admin ingest** manifest 过滤 + 同型 `impact_surface` — **可执行** |
| T002 继承 C′ | §0.2「C″ 不重斗 T002」、§1.1「继承 C′…不重做争论性切片」、§3.2 守卫 **≥ 0.873** — **避免重复争论** |
| 可选 `query_seeds` | 标注可选且禁止整图 — 不阻塞 |

### §3.2 主 KPI（OR）· 基线 052803 + 083014

| 指标 | task 阈值 | 对照 `gold_f1.md`（D 臂 impact F1） | 一致 |
|------|-----------|-------------------------------------|------|
| T003 主 KPI | ≥ **0.45** **或** Δ≥ **+0.15** vs C′ | 052803 **0.400**；083014 **0.222**（Δ+0.15 → **≥ 0.372**） | 是 |
| T002 守卫 | ≥ **0.873** | C′ **0.923** − 0.05 | 是 |
| entry 守卫 | 无单题降 >0.05；中位数 ≥ **0.80** | C′ entry 0.857/0.923/1.000，中位数 **0.923** | 是 |
| token | 中位数 ≤ **≈599**；单题 < **8192** | §2.2 表 canonical/C′ 与中位数 **479/481** | 是 |
| 双基线引用 | §2.1、§5.6、PR-3 结论表 | 路径 `…_052803` / `…_083014` | 是 |

### PR-4 / NR-9 / HG-GATE-C-DOUBLE-PRIME-SIGNOFF

| 关系 | 结果 |
|------|------|
| NR-9 | batch 前 / 结论未签收前 **禁止** 改 `10-tech-graph.mdc` |
| PR-4 | 合并前提 = §3.2 + 结论 `accepted` + **HG** `approved` |
| HG 表 | `blocks_hats`: `PR-4`, `50`, 关账 — 与 NR-9/§3.3 **一致** |

### HARNESS §5 · test_strategy · failure_paths

| 字段 | 结果 |
|------|------|
| `test_strategy: required` | 有 `test_strategy_note`（物化/batch/双基线）— 合规 |
| 可失败测试 | §3.1：`pytest tests/test_gate_ctx_c_v1_materialize.py`；§3.2：全量 pytest + batch 评分 — **可观测** |
| `gates_before_code` | `failure_paths`, `freeze_id`, `deps_installed` — task §4 已齐 |
| FP-CDP1～8 | 覆盖覆盖历史 run、物化顺序、token、改默认轨、scope、偷改 rules、空子图、batch 失败 — **可操作** |

---

## 签收 / 关闭

| 项 | 声明 |
|----|------|
| **R1 轮次** | **通过**；task 仍为 `draft`，**非** task 终局关闭 |
| **下一棒** | **执行帽（30）** — 待 `HG-AUDIT-R1` 人签 |
| **终轮** | 关账须 R? + `HG-GATE-C-DOUBLE-PRIME-SIGNOFF` + `HANDOFF_CLOSE_TRACE`（本 R1 不产出） |

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/30-execute-code.md
- docs/harness/prompts/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/harness/prompts/HANDOFF_SEMI_AUTO.md（执行前扫描 human_gate）

输入：
- 主 task（相对 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_c_double_prime_v1.md
- 子仓根：
ai-ink-brain-api-python
- 合并前验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 任务审核书面结论（R1）：
ai-ink-brain-api-python/docs/harness/reviews/task_engineering_tech_graph_gate_c_double_prime_v1_audit_R1_20260520.md
- 本帽 invoke 快照：
ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_51_tech-graph-gate-c-double-prime-task-audit-r1.md
- 关联 SPEC：
Projects/docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

开帽前硬检查：
1. task 内 HG-TASK-DRAFT、HG-AUDIT-R1 须为 approved；若仍为 pending → 仅输出 gate_id，拒开工。
2. HG-GATE-C-DOUBLE-PRIME-SIGNOFF 仍为 pending 正常；禁止在 PR-3 签收前改 .cursor/rules/10-tech-graph.mdc（NR-9 / FP-CDP6）。
3. test_strategy: required → PR-1 先扩 test_gate_ctx_c_v1_materialize（T003 manifest_slice + impact_surface）再改 materialize_gate_c_payloads.py。

执行顺序（task §5）：
PR-1（T003 物化 + protocol gate_c_double_prime_freeze_id + pytest 绿）
→ PR-2（仅 token 超限）
→ PR-3（新 batch 目录，禁止覆盖 052803/083014；结论 conclusion_gate_c_double_prime_v1_zh.md 含对双基线 Δ 表）
→ PR-4（仅 HG-GATE-C-DOUBLE-PRIME-SIGNOFF approved 且 §3.2 + 结论 accepted）

必读只读基线：
docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_052803/gold_f1.md
docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_20260518_083014/gold_f1.md

分支建议：task/engineering-tech-graph-gate-c-double-prime-v1（自 main）

完成：回填 task「### 自检结论（执行者）」；按 HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python 提交本轮路径。
```
