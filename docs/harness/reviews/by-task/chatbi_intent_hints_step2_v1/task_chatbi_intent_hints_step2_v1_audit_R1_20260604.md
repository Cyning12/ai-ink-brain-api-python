# 任务审核报告：chatbi_intent_hints_step2_v1 · R1

| 字段 | 值 |
| --- | --- |
| **task_path** | `docs/tasks/active/task_chatbi_intent_hints_step2_v1.md` |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **audit_round** | R1 |
| **freeze_id** | `CHATBI-INTENT-HINTS@2026-06-09` |
| **audit_profile** | `post_close` |
| **test_strategy** | `required` |
| **git_branch** | `task/chatbi-intent-hints-step2-v1` |
| **invoke_snapshot** | `docs/harness/invokes/by-task/chatbi_intent_hints_step2_v1/invoke_20260604_22_task-audit-R1.md` |
| **关联 SPEC** | Step2-C-Mid · Schema §4.5 · Overview |
| **reviewer** | Agent（22 帽） |
| **date** | 2026-06-04 |

---

## 审查结论摘要

**零阻塞 · 建议进入执行帽（30）**

task 与 Step2 SPEC §2.1～§4、Schema §4.3/§4.5 **对齐**；Q-2（仲裁默认开 + `INTENT_HINTS_ARBITRATION` 可关）已在 task **resolved**；`failure_paths` F1～F6 含 Scenario ID；验收含 mock 仲裁、关 LLM router、负例与全集 pytest。

**前置**：main 已含 Step1 #109 + U1.5 #110；U1 五问 5/5 人验已通过（本 task 不重复 reinspect）。

**开 30 前**：人须将 **`HG-AUDIT-R1`** → `approved`（**单独 commit**，与 Step1 gate 纪律一致）。

---

## 理论对齐检查表（P0）

### §3.1 任务单最小字段

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 头部 Harness 元信息 · `test_strategy: required` | ☑ |
| 2 | `test_strategy_note` 非空 | ☑ |
| 3 | `failure_paths` ≥1 行（触发→行为→可重试→用户可见） | ☑（F1～F6） |
| 4 | **非范围** 独立小节非空 | ☑ §3 |
| 5 | **验收标准** 含合并前必绿 / pytest | ☑ |
| 6 | `semi_auto` + `audit_profile: post_close` | ☑ |

### §3.2 合并前 CI

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 验收含本地 pytest 等价命令 + CI 隐含（AGENTS §8） | ☑ |
| 2 | 40/50 关账留证路径已声明 | ☑（50 待关账） |

### §Blocking · 高敏（F8）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | 涉 `api/` · Delta 已填 · `test_strategy: required` → 关账须 50 | ☑ |

### §3.3 独立复检（50）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `required` + api/ 路由/仲裁 → **50 必须** `reinspect_results/` | ☑（task 已写） |
| 2 | 50 触发不阻塞 30 开工 | ☑ |

### OpenSpec × TDD（§4.2）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `harness_task_validate.py` | ☑ exit 0（R1 当日复跑） |
| 2 | Delta ADDED/MODIFIED 与 S2-1～S2-6 一致 | ☑ |
| 3 | failure_paths Scenario ID 非空 | ☑ |
| 4 | 验收含 pytest 表述 | ☑ |

`harness_human_gate_check.py --task`：**HG-AUDIT-R1 pending**（**预期** · 阻塞 30 直至人签；不阻塞本 R1 落盘）。

---

## SPEC / task 对齐抽检

| 项 | 结论 |
| --- | --- |
| Step2 SPEC S2-1～S2-6 | task §2 **一一覆盖** |
| 仲裁语义（强制 rag · 非降置信） | task § SPEC 决策与 Step2 §3 **一致** |
| V1 rule 合并公式 | task §2 S2-2 + Step2 §4 **一致** |
| RUNBOOK Q4 + Q-INTENT | 验收 § 逐字引用 **OK** |
| Q-1/Q-3/Q-4 | 引用 U1 · **不重复争论** ✓ |

---

## 阻塞项

**无阻塞。**

---

## 非阻塞项（30 实现时注意）

| # | 项 | 建议 |
| --- | --- | --- |
| NB-1 | **F3 over-rag** | 仲裁条件须 **person+trigger 或 career_span regex** 命中；单独 keyword（如泛「经历」）**不**触发仲裁 · 与 task F3 一致 |
| NB-2 | **仲裁 hook 落点** | task 允许 `intent_agent` 和/或 `agent`；30 优先 **`decide_intent_v2` 成功路径末尾**（缓存写入前）· 避免 double-apply |
| NB-3 | **`hints_arbitration` 契约** | task 已 defer cross-repo contract；**本 PR** 仅 `raw_response` 内观测 · 30 勿改 SSE 契约除非登记 manifest |
| NB-4 | **`intent_hints.yaml`** | 随 PR 增 `arbitration:` 段（Schema §4.5 默认 enabled） |
| NB-5 | Overview §7 checkbox | 文档同步 · **非**本 task 代码交付 · 可选 follow-up docs PR |

---

## 需任务帽回填清单

**无。**（零阻塞 R1 · 不必 R2 除非 30 前 scope 变更。）

---

## 是否建议执行帽开工

| 项 | 结论 |
| --- | --- |
| **30 编码** | **建议开工** — 待 **`HG-AUDIT-R1` approved** |
| **50 复检** | 关账前必须 · Fresh Context 新会话 |
| **PR** | 标题可用 task 建议 · diff 禁止 `api/graph/*` |

---

## human_gate（R1 核对 · 不代填）

| human_gate_id | status | blocks_hats | R1 结论 |
| ------------- | ------ | ----------- | ------- |
| HG-TASK-DRAFT | approved | 22-R1, 30 | ☑ 已人签 |
| HG-AUDIT-R1 | **pending** | 30 | **人签后** 30 可开工 |
| HG-REINSPECT | pending | done, 合并 PR | 50 后人签 |

---

## 签收 / 关闭

- **R1 结论**：task **可执行** · 零阻塞  
- **本 task 未关闭**：须 30→40→50→PR→`HG-REINSPECT`  
- **下一棒**：30 执行编码（见下 §3 全文）

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- ai-ink-brain-api-python/docs/harness/prompts/hats/30-execute-code.md
- ai-ink-brain-api-python/docs/harness/prompts/hats/40-self-check.md
- ai-ink-brain-api-python/docs/harness/HARNESS_V2_PLAN.md §5
- ai-ink-brain-api-python/AGENTS.md · task 内「给执行帽的必读列表」

输入（占位符已替换）：
- 主 task 路径：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_intent_hints_step2_v1.md
- 逻辑子仓：
ai-ink-brain-api-python
- Worktree 研发目录：
ai-ink-brain-api-python
- 合并前须跑通的验证命令：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径：
ai-ink-brain-api-python/docs/harness/reviews/by-task/chatbi_intent_hints_step2_v1/task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md
- 关联 SPEC / 总规：
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md
ai-ink-brain-api-python/docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md

你必须完成：
0. Invoke 快照落盘 docs/harness/invokes/by-task/chatbi_intent_hints_step2_v1/invoke_20260604_30_execute-step2-u2.md
0b. 人工闸：HG-AUDIT-R1 须 approved，否则拒开工并输出 gate_id + 路径。
1. 通读 task gates_before_code、failure_paths F1～F6、验收、必读列表、§ SPEC 决策 Q-2。
2. test_strategy required：先写 tests/test_intent_hints_arbitration.py + 扩展 test_intent_router_backend_v1.py（可失败），再改 api/。
3. 实现 S2-1～S2-6：intent_hints 规则函数 · router 合并 · apply_hints_arbitration · yaml arbitration 段 · env · PROJECT_CONFIG。
4. 禁止 api/graph/* · Step3 范围 · 批量改 60 金标。
5. 跑 task VERIFY 三节命令 + 全集 pytest 至绿。
6. 回填 task ### 自检结论（执行者）。
7. semi_auto：无阻塞则落盘 40 自检 invoke 并 commit；输出下一棒 40 Prompt。
8. 按 HANDOFF_AUTO_COMMIT 分 commit（实现 vs harness 文档分离）。
```
