# 任务审核 R1 · chatbi_intent_hints_step1_v1

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_path** | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_intent_hints_step1_v1.md` |
| **task_slug** | `chatbi_intent_hints_step1_v1` |
| **audit_round** | `R1` |
| **audit_date** | `20260604` |
| **prev_review** | 无（首轮） |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/chatbi_intent_hints_step1_v1/invoke_20260604_22_audit-r1.md` |
| **关联 SPEC** | `docs/spec/intent-hints/` Step1 · Schema · Overview |
| **审查帽** | `22-task-audit` |
| **git_branch** | `task/chatbi-intent-hints-step1-v1` |

---

## 审查结论摘要

**task 文档层：零阻塞，R1 通过。** U1 Step1（C-lite）目标清晰：外置 `intent_hints.yaml` + loader + `_llm_decide_v2` Prompt 注入，修复 Portfolio Q4 / 人名误路由；**不**改 router / Graph / `unified_chat.py` 主路径。`test_strategy: required` 与涉 `api/intent_agent.py` 匹配；`harness_task_validate.py` **OK**；Overview §7 四项已在 task **§ SPEC 决策** resolved/deferred。

**流程层：暂不可进 30。** `HG-TASK-DRAFT` = **approved**（2026-06-04 人签）。**`HG-AUDIT-R1` = `pending`**（预期：人阅读本 R1 后改 `approved`），**阻塞 30**。

---

## 理论对齐检查表（P0 · 已核对项）

### §3.1 任务单最小字段

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 头部 Harness 元信息表：`test_strategy` 三选一 | ✅ `required` |
| 2 | `not_applicable` 时 `test_strategy_note` 非空 | N/A |
| 3 | `failure_paths` ≥1 行（触发→行为→可重试→用户可见） | ✅ F1–F5，含 Scenario ID |
| 4 | **非范围** 独立小节非空 | ✅ §3（router/Graph/Step2–3/sync/前端） |
| 5 | **验收标准** 含 **合并前必绿** 条 | ✅ pytest + PR workflow |
| 6 | `semi_auto` + `audit_profile` 已填 | ✅ `true` + `post_close` |

### §3.2 合并前 CI 验收条

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 验收含 PR pytest workflow 全绿 + 本地等价命令 | ✅ §验收 + `AGENTS.md` §8 |
| 2 | 40 自检 / PR 链接可核对 | ⏳ 执行阶段（30→40） |

### §Blocking · 高敏须人判断

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 触达 `api/intent_agent.py` · Intent Prompt 注入 | ✅ Delta ADDED/MODIFIED 已填；`freeze_id` 已锚；关账须 **50**（`test_strategy_note`） |

### §3.3 独立复检（50）触发

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | `test_strategy` 与变更类型匹配 | ✅ `required` + 涉 `api/` |
| 2 | `required` 且涉 `api/` → 关账前 50 落盘 | ✅ 已声明；**不阻塞 30 开工** |

### OpenSpec × TDD（`harness_task_validate.py`）

| # | 检查项 | 结果 |
|---|--------|------|
| 1 | 触达 `api/` 时非 `not_applicable` | ✅ |
| 2 | §行为变更 Delta 已填或显式「无」 | ✅ ADDED/MODIFIED |
| 3 | `failure_paths` 含 **Scenario ID** 列且非空 | ✅ |
| 4 | 验收含合并前 pytest 条 | ✅ |

**机械校验**：`python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_hints_step1_v1.md` → **OK**

---

## 阻塞

| ID | 类型 | 说明 | 修复 |
| --- | --- | --- | --- |
| **B1** | **human_gate** | `HG-AUDIT-R1` = `pending`，`blocks_hats`: `30` | 人阅读 **本 R1** 后在 task `### 人工闸` 改 `approved`（**建议单独 commit**） |

---

## 非阻塞

| 项 | 说明 |
| --- | --- |
| Overview §7 checkbox | SPEC 正文 `[ ]` 未勾；task **§ SPEC 决策** 已 resolved/deferred — 30 前可选同步勾选 Overview |
| intent-hints SPEC `draft` | Step1/Schema 行为真值已齐；合 main 前人审是否标 `accepted` 非本 task 交付 |
| F2 `fp-step1-llm-still-direct` | Prompt-only 不 100% 保证；task 已诚实标注 · U2 仲裁 defer |
| F3 集成验收 | Q4/人名集成探针依赖 ingest/sync；RUNBOOK §2 硬检查 · 非 Step1 代码债 |
| `git_branch` | 30 须在 `task/chatbi-intent-hints-step1-v1` 从 `origin/main` 开干（task 已声明） |
| scope creep | F4 + §3 非范围 + diff 不含 `api/graph/*` 可操作 |

---

## 需任务帽回填清单

（无 — task 文档层无需 10 帽回填。）

---

## 是否建议执行帽开工

**否（当前）。** 须先 **B1**：`HG-AUDIT-R1` → `approved`。

闸口通过后：**建议进入 30**（`test_strategy: required` · 先 loader/Intent stub 红绿再实现 · 参照 `text2sql_value_hints.py`）。

---

## 签收 / 关闭

| 项 | 结论 |
| --- | --- |
| **R1 文档审查** | **通过** — task 合同可执行，验收可观测，失败路径与 Delta 齐备 |
| **30 开工** | **未签收** — 待 `HG-AUDIT-R1` = `approved` |
| **关账** | 不在本轮；`audit_profile: post_close` · 关账前须 **50** 落盘 + KPI（00） |

---

## 人工闸通过后 · 下一棒可复制 Prompt（30 执行）

> **须在** task 内 `HG-AUDIT-R1` = **`approved`** 后再粘贴；30 开帽前 `harness_human_gate_check.py --task …` 须 **exit 0**。

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」

输入：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_intent_hints_step1_v1.md
- 逻辑子仓：
ai-ink-brain-api-python
- Worktree 研发目录：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_intent_hints_step1_v1_audit_R1_20260604.md
- 关联 SPEC：
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md

你必须完成：
0. Invoke 快照落盘 docs/harness/invokes/by-task/chatbi_intent_hints_step1_v1/invoke_*_30_*.md
0b. human_gate：HG-AUDIT-R1 须 approved，否则拒开工
1. 确认 git 分支 task/chatbi-intent-hints-step1-v1（从 origin/main 拉）
2. test_strategy required：先 loader + Intent stub 可失败测试，再实现
3. 范围：intent_hints.yaml · api/intent_hints.py · api/intent_agent.py · 测试 · .env.example 注释
4. 禁止：api/graph/* · intent_router 仲裁 · Step2/3 逻辑
5. 跑 pytest 全绿；回填 task ### 自检结论（执行者）
6. semi_auto：落盘 40 invoke 并链 40（无 gate 阻塞时）

禁止：未 approved 代填 gate；夹带 U2/U3 scope。
```

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 22 R1 首轮：文档零阻塞；HG-AUDIT-R1 阻塞 30 |
