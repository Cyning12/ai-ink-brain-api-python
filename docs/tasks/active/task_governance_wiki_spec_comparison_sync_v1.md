# Task：Governance A3 — SPEC §2 与对比表 Wiki 同步（v1）

> **状态**：`draft`  
> **母 Loop**：[`task_harness_wiki_loop_a1_a4_v1.md`](task_harness_wiki_loop_a1_a4_v1.md) · round **A3**  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)  
> **对比表**：[`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯治理文档小 diff；无行为变更。 |
| **freeze_id** | `GOV-WIKI-A3-SPEC-SYNC@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **task_slug** | `wiki-a3-spec-comparison` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 母 task [`HG-LOOP-BATCH`](task_harness_wiki_loop_a1_a4_v1.md) = `approved` 后方可 22 |

---

## 帽子顺序（**跳过 10** · Loop A3）

| 序 | 帽 | 启动 |
|----|-----|------|
| — | **10** | **跳过** |
| 1 | **22 R1** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md) · [`LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md) **round=A3** |
| 2–5 | **30→40→50→关账** | 同上 Loop 链 |

**说明**：A3 对 A1/A2 **无硬占位依赖**；可读 A1/A2 done 备忘核对措辞，建议在 A1/A2 done 后执行。

---

## 背景与目标

T1c 与 Multi slug AB 均已关账，但 **SPEC §2 时间线** 仍标 T1c 为 `planned`；对比表 **#12 concepts**、**#46 多 slug** 行需与 [`conclusion_multi_slug_zh.md`](../harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md) 及 §5.1 一致。

**完成态**（小 diff）：

1. SPEC §2：**T1c**、**Multi slug**（或等价行）标 **done**，与 §5.1 状态一致。  
2. 对比表：**#12** concepts 行反映 T1c 已交付 `test-strategy-ink-backend`；**#46** 多 slug 行与 Multi **部分外推** + A1/A2 Loop 意图一致（可注 test_strategy 缺口修复中/已修复，以关账时 A1/A2 为准）。

---

## 范围

- [ ] 更新 `SPEC-Governance-Wiki-Harness-Roadmap-v1.md` **§2** 时间线：T1c → **done**；增补或更新 Multi slug 行 → **done**（链 `task_wiki_ctx_ab_multi_slug_v1`）。  
- [ ] 更新 `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`：**#12** concepts 行（1 页 → T1c done + concept 页存在）。  
- [ ] 更新对比表 **#46** 多 slug 行：与 Multi 结论（slug B W 3/4、ingest 条件）一致；若 A1/A2 已 done 可改为「Loop A1/A2 已补 test_strategy 纪律」。  
- [ ] 两文件修订记录各追加一行。  
- [ ] 22/40/50 落盘；关账 `done/`。

## 非范围

- 不重写对比表全文或 SPEC 其他章节。  
- 不改 `docs/coding_wiki/` synthesis 正文（属 A1/A2）。  
- 不改 `RECENT_TASK_SCHEDULE`（属 A4）。  
- 不改 `api/`、`tests/`、CI、prompts。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| SPEC §2 / §5.1 | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` |
| 对比表 | `docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` #12、#46 |
| Multi done | `docs/tasks/done/task_wiki_ctx_ab_multi_slug_v1.md` |
| T1c done | `docs/tasks/done/task_coding_wiki_t1c_test_archive_v1.md` |
| 母 Loop | `LOOP_MANIFEST.md` round A3 |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | SPEC §2 T1c 仍为 `planned` 而 §5.1 已 done | 文档矛盾；22 **阻塞** | 是 | 对齐 §5.1 |
| F2 | #46 写「两 slug 均 4/4」与 Multi 结论不符 | 50 **fail** | 是 | 以 `conclusion_multi_slug_zh.md` 为准 |
| F3 | 大范围重写对比表（>20 行变更） | 越界；22 **阻塞** | 否 | 仅 #12、#46 + SPEC §2 |
| F4 | 与 A1/A2 未 done 时 #46 宣称「已修复」 | 22 应要求措辞为「进行中」或等 A1/A2 | 是 | 顺序见母 task |

---

## 验收标准

- [ ] `grep -n planned docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` 在 **§2 T1c 行** 无 `planned`（应为 done 或等价）。  
- [ ] SPEC §2 含 Multi slug **done** 引用（`task_wiki_ctx_ab_multi_slug_v1` 或结论文）。  
- [ ] 对比表 #12、#46 现状列与 2026-05-26 Multi + T1c 事实一致。  
- [ ] 22 R1 落盘 `reviews/by-task/wiki-a3-spec-comparison/`。  
- [ ] 50 复检 pass；本 task 在 `done/`。

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`。

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`、`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` |
| 图谱变更点 | 无 |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | — |
| 结论 | — |
| 要点 | — |

---

## 给 Cursor

`wiki-a3-spec-comparison`、`GOV-WIKI-A3-SPEC-SYNC@2026-05-26`、`WIKI_REQUIREMENTS_COMPARISON`、`SPEC` §2、`PROMPT_LOOP_22_to_CLOSE`、`round=A3`
