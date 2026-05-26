# Task：Coding Wiki A1 — synthesis 补全 test_strategy（v1）

> **状态**：done（2026-05-26 验收通过 · CODING-WIKI-A1-TEST-STRATEGY@2026-05-26）  
> **母 Loop**：[`task_harness_wiki_loop_a1_a4_v1.md`](task_harness_wiki_loop_a1_a4_v1.md) · round **A1**  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.1  
> **证据**：[`conclusion_multi_slug_zh.md`](../harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md) slug B B-Q3

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；关账须回填 A2 [`PLACEHOLDER:A1_OUTCOME`](task_coding_wiki_schema_test_strategy_rule_v1.md)。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 Wiki L2 元数据补洞；不新增 pytest、不改 `api/`。 |
| **freeze_id** | `CODING-WIKI-A1-TEST-STRATEGY@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "必读 L1 task"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **task_slug** | `wiki-a1-ingest-test-strategy` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 母 task [`HG-LOOP-BATCH`](task_harness_wiki_loop_a1_a4_v1.md) = `approved` 后方可 22 |

---

## 帽子顺序（**跳过 10** · Loop A1）

| 序 | 帽 | 启动 |
|----|-----|------|
| — | **10** | **跳过**（Batch-10 已起草） |
| 1 | **22 R1** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md) · [`LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md) **round=A1** |
| 2 | **30** | 同上 Loop 链（semi_auto 可连跑） |
| 3 | **40** | 同上 |
| 4 | **50** | 同上 · `reinspect_results/` |
| 5 | **关账** | 同上 · 回填 A2 `PLACEHOLDER:A1_OUTCOME` |

**纪律**：新对话 · 分支 `task/wiki-loop-a1-a4-v1` · **禁止** 再开 10。

---

## 背景与目标

Multi slug AB 表明：W 臂禁止回读 L1 done task 时，`query-rewrite-observability` synthesis **未蒸馏** L1 头字段 **`test_strategy: recommended`**，导致 B-Q3 无法作答。

**完成态**：在 [`docs/coding_wiki/syntheses/query-rewrite-observability.md`](../coding_wiki/syntheses/query-rewrite-observability.md) 的 **frontmatter 与/或摘要** 中明确 `test_strategy` 取值（与 [`task_05_query_rewrite_observability.md`](../tasks/done/task_05_query_rewrite_observability.md) 一致），使 Wiki-only 载荷可答 Multi B-Q3 类问题。

---

## 范围

- [x] 修改 `docs/coding_wiki/syntheses/query-rewrite-observability.md`：frontmatter 增 `test_strategy: recommended`（或等价 YAML + 摘要一句）。  
- [x] 摘要或 §测试变更 附近说明与 L1 / [`concepts/test-strategy-ink-backend.md`](../coding_wiki/concepts/test-strategy-ink-backend.md) 的 pointer 关系。  
- [x] 可选：`docs/coding_wiki/log.md` append 一行 ingest 记录。  
- [x] VERIFY：`rg -n test_strategy docs/coding_wiki/syntheses/query-rewrite-observability.md` 有命中且取值正确。  
- [x] 22/40/50 落盘；关账后回填 A2 占位 + `git mv` 本 task 至 `done/`。

## 非范围

- 不改 `api/`、`tests/`、CI、其他 synthesis 全文重写。  
- 不重跑 Multi slug 实验或改已冻结 scorecard。  
- 不在本 task 修改 `CODING_WIKI.md` §8（属 A2）。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| L1 真值 | `docs/tasks/done/task_05_query_rewrite_observability.md` · **`test_strategy: recommended`** |
| 目标页 | `docs/coding_wiki/syntheses/query-rewrite-observability.md` |
| 概念 pointer | `docs/coding_wiki/concepts/test-strategy-ink-backend.md` |
| Multi 证据 | `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md` §1 slug B |
| 母 Loop | `docs/harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md` round A1 |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | 母 `HG-LOOP-BATCH` = `pending` | 22 **拒开工** | 是 | 须人批母闸 |
| F2 | `test_strategy` 与 L1 不一致（如写成 `required`） | 22/50 **阻塞**；列矛盾点 | 是 | 以 L1 task 头为准 |
| F3 | 仅改 concept 页、未改目标 synthesis | VERIFY `rg` 无命中 → 40 **fail** | 是 | 改指定 synthesis |
| F4 | 复制 L1 done task 全文进 Wiki | 违反 ingest 纪律；22 **阻塞** | 否 | pointer + 摘要即可 |

---

## 验收标准

- [x] `rg -n test_strategy docs/coding_wiki/syntheses/query-rewrite-observability.md` 输出含 `recommended`（或与 L1 一致的其他合法取值 + 摘要说明）。  
- [x] frontmatter 仍符合 `CODING_WIKI.md` §3 最小集（不破坏既有 `slug` / `source_task`）。  
- [x] 22 R1 落盘 `docs/harness/reviews/by-task/wiki-loop-a1-a4/`（零阻塞亦须记录）。  
- [x] 50 复检 pass；关账已回填 A2 `<!-- PLACEHOLDER:A1_OUTCOME -->`。  
- [x] 无 `api/`、`tests/`、prompts、CI diff。

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（回归基线）。

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/coding_wiki/syntheses/query-rewrite-observability.md`、`docs/coding_wiki/log.md` |
| test_strategy 取值 | `recommended`（与 L1 `task_05_query_rewrite_observability.md` 一致） |
| 关键 env | 无 |
| 图谱变更点 | 无 |
| 30 commit | `cbe181e` |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `rg -n test_strategy docs/coding_wiki/syntheses/query-rewrite-observability.md`；`pytest tests -m "not intent_eval and not intent_benchmark" -q` |
| 结论 | **pass** |
| 要点 | synthesis 含 `test_strategy: recommended`（L9/L16/L36）；无 api/tests/prompts diff；pytest 221 passed |

---

## 给 Cursor

`wiki-a1-ingest-test-strategy`、`CODING-WIKI-A1-TEST-STRATEGY@2026-05-26`、`test_strategy`、`query-rewrite-observability`、`PROMPT_LOOP_22_to_CLOSE`、`round=A1`、`semi_auto`
