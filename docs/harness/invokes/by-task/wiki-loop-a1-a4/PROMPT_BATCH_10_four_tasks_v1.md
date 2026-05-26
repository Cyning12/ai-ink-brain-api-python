# 启动 Prompt · 一次性 Batch-10 · Wiki Loop A1–A4（v1）

> **只运行一次**。生成母 task + 四个子 task 初稿后，后续每轮 **仅** 使用 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md)（见 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md)）。  
> **分支**：`task/wiki-loop-a1-a4-v1` · Open **`ai-ink-brain-api-python/`**

---

```text
你正在扮演 Harness「需求与任务分析帽（10）· Batch 模式」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（输出形状；本批 **禁止** 写业务代码）
- docs/tasks/templates/TASK_TEMPLATE.md
- docs/tasks/skills/SKILL-docs-governance.md（预填片段）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、07-git-workflow.mdc

【背景】
Wiki-CTX-AB Multi slug 已结论「部分外推」：slug B W 臂 B-Q3 因 synthesis 缺 test_strategy。
本轮 **单 PR** 试点 **简化 loop**：本 Prompt 只生成 5 份 task 初稿；执行阶段 **不再开 10**，每子 task 走 22→30→40→50→关账。
证据：docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md §4

【开帽 · Invoke 快照】将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/wiki-loop-a1-a4/invoke_20260526_10_batch_four_tasks_v1.md

【SDD】不涉及新 SPEC · 状态 = 不涉及新 SPEC（§3 省略）

【你必须落盘以下 5 个文件（相对子仓根）】

---

## 0. 母 task · task_harness_wiki_loop_a1_a4_v1.md

路径：docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md

| 字段 | 值 |
|------|-----|
| test_strategy | not_applicable |
| test_strategy_note | Loop 编排；子 task 交付 docs；母 task 不直接改 synthesis |
| freeze_id | WIKI-LOOP-A1-A4@2026-05-26 |
| semi_auto | true |
| audit_profile | post_close |
| git_branch | task/wiki-loop-a1-a4-v1 |
| task_slug | wiki-loop-a1-a4 |

人工闸（仅母 task）：
| HG-LOOP-BATCH | approved | — | 人批后子 task 写「继承母闸」 |

正文须含：
- 子 task 顺序表 A1→A2→A3→A4→母关账
- 每子 task 路径链到 active 文件
- 执行纪律：子 task **禁止** 再开 10；用 PROMPT_LOOP_22_to_CLOSE + LOOP_MANIFEST
- 单 PR、不改 api/tests/prompts/CI
- §验收：四轮均 done/ 后母 task 关账

---

## 1. 子 task A1 · task_coding_wiki_ingest_test_strategy_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | CODING-WIKI-A1-TEST-STRATEGY@2026-05-26 |
| task_slug | wiki-a1-ingest-test-strategy |
| human_gate | 继承 HG-LOOP-BATCH |

**目标**：在 docs/coding_wiki/syntheses/query-rewrite-observability.md 的 frontmatter 与/或摘要中明确 **test_strategy**（与 L1 done task 一致，须可答 Multi B-Q3）。

**范围**：
- 改上述 synthesis；可选 log.md 一行 ingest
- VERIFY：rg -n test_strategy docs/coding_wiki/syntheses/query-rewrite-observability.md

**非范围**：不改 api/、tests/、其他 synthesis 全文重写

**帽子顺序表**：22→30→40→50→关账 · 启动稿路径 wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md + LOOP_MANIFEST round=A1

---

## 2. 子 task A2 · task_coding_wiki_schema_test_strategy_rule_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | CODING-WIKI-A2-SCHEMA-RULE@2026-05-26 |
| task_slug | wiki-a2-schema-test-strategy |

**目标**：CODING_WIKI.md §8 增补 **ingest 规范**：改 api/ 的 done Epic，synthesis 须含 test_strategy 或内联 pointer（链 concepts/test-strategy-ink-backend）。

**前置（占位 · 由 A1 关账回填，执行 A2 的 22 之前必须已替换）**：

```markdown
## 前置（A1 关账回填 · 勿删标记）

<!-- PLACEHOLDER:A1_OUTCOME -->
（待回填：A1 写入的 test_strategy 取值、修改的文件路径、commit 短哈希、一句摘要）
<!-- /PLACEHOLDER:A1_OUTCOME -->
```

**非范围**：不修改 A1 已改的 synthesis 正文（除非 22 发现事实错误单列阻塞）

---

## 3. 子 task A3 · task_governance_wiki_spec_comparison_sync_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | GOV-WIKI-A3-SPEC-SYNC@2026-05-26 |
| task_slug | wiki-a3-spec-comparison |

**目标**（小 diff）：
- SPEC-Governance-Wiki-Harness-Roadmap-v1.md §2 时间线：T1c、Multi slug 标 done（与 §5.1 一致）
- WIKI_REQUIREMENTS_COMPARISON_v1_zh.md：#12 concepts 行、#46 多 slug 行与 Multi 结论文一致

**非范围**：不重写对比表全文

---

## 4. 子 task A4 · task_governance_recent_schedule_wiki_sync_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | GOV-WIKI-A4-SCHEDULE@2026-05-26 |
| task_slug | wiki-a4-recent-schedule |

**目标**：RECENT_TASK_SCHEDULE.md §1 现状快照（active 数量、近期当前棒）与 §6.6 Wiki 行同步（Multi done、Loop 进行中/完成后更新）

**建议**：A4 在 A1–A3 均 done 后执行，排期表才准确

---

## 5. 每个 task 文内统一块（五份都要有）

- Harness 元信息表（上表字段）
- 背景与目标 / 范围 / 非范围 / 依赖与必读 / 验收标准（`- [ ]`）/ failure_paths（2–4 条）
- **帽子顺序**：写清 **跳过 10**；链 `PROMPT_LOOP_22_to_CLOSE_v1.md` + `LOOP_MANIFEST.md` 当轮 round
- ### 自检结论（执行者）（空表待 40 填）
- 给 Cursor 关键词行

---

## 6. Commit

git add docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md \
        docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md \
        docs/tasks/active/task_coding_wiki_schema_test_strategy_rule_v1.md \
        docs/tasks/active/task_governance_wiki_spec_comparison_sync_v1.md \
        docs/tasks/active/task_governance_recent_schedule_wiki_sync_v1.md \
        docs/harness/invokes/by-task/wiki-loop-a1-a4/invoke_20260526_10_batch_four_tasks_v1.md

message: docs(task): Wiki loop A1–A4 五份 task 初稿 · WIKI-LOOP-A1-A4@2026-05-26

---

## 7. 对话末尾

- 📋 Harness 状态栏
- **下一棒**：人批 HG-LOOP-BATCH（若未 approved）→ 新对话 · [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) · MANIFEST **round=A1**
- **禁止**：在本会话执行 A1 的 22 或改 synthesis（属下一轮）

关键词：Batch-10、Wiki loop、A1 A2 A3 A4、test_strategy、PLACEHOLDER、单 PR
```
