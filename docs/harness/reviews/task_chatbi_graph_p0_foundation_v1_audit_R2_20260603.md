# 任务审核：ChatBI Graph P0 地基 — R2

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_path** | `ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |
| **audit_round** | R2（复审 · `post_close` 闸 1） |
| **关联上一轮** | [`task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md`](task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md) |
| **关联 SPEC** | `docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md` · `docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md` · `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` · `docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md` |
| **invoke_snapshot** | `ai-ink-brain-api-python/docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/invoke_20260603_22_chatbi-graph-p0-foundation-r2.md` |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **test_strategy** | `required` |
| **audit_profile** | `post_close` |
| **reviewer** | Agent（22 帽） |
| **date** | 2026-06-03 |
| **机械校验** | `python tools/harness_task_validate.py docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` → **OK** · `python tools/harness_human_gate_check.py --task …` → **exit 1**（`HG-TASK-DRAFT` · `HG-AUDIT-R1` 仍 `pending`） |

---

## 审查结论摘要

对照 **R1** 回填 diff（commit `ff41a46`）：**B-2～B-4 已闭合** — SDD §10 已冻结（Q-8 路由 · 项 3/4/5 · 确认行 `2026-06-03`）；`## 验收标准` / `## 失败路径`（F1～F4 + Scenario ID）/ `## 行为变更（Delta）` 齐全；`harness_task_validate.py` **OK**。task 与 Plan **§4A** / **D-1～D-5** 范围、非范围、P0 硬约束 **一致**；`test_strategy: required` + 边表单测/runner smoke 验收 **可观测**。

**结论：零阻塞（task 合同层）— 可进入执行帽**（**前提**：人签 `HG-TASK-DRAFT` 与 `HG-AUDIT-R1` → `approved`；30 开帽时若仍为 `pending` 须 **拒开工**）。

---

## R1 → R2 对照

| R1 ID | R2 状态 | 证据 |
|-------|---------|------|
| **B-1** | **人闸待签**（非 task 正文缺口） | `human_gate` 表仍 `pending`；`harness_human_gate_check` exit 1 |
| **B-2** | ☑ 已闭合 | §10 表 + 「均已人确认 · 2026-06-03」；Q-8 写入 §1 背景 |
| **B-3** | ☑ 已闭合 | `## 验收标准` 含 pytest + PR workflow；`## 失败路径` 表 + Scenario ID；validate OK |
| **B-4** | ☑ 已闭合 | `## 行为变更（Delta）` ADDED/MODIFIED + Scenario |
| 建议项 | ☑ | 验收含边表单测 + runner smoke（red-green 口径） |

---

## 理论对齐检查表（P0）

### §3.1 任务单最小字段

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `test_strategy` 三选一 | ☑ `required` |
| 2 | `not_applicable` + note | N/A |
| 3 | `failure_paths` ≥1 行 | ☑ F1～F4 |
| 4 | 非范围非空 | ☑ §3 |
| 5 | 验收含合并前必绿 pytest | ☑ 本地 + PR workflow 条 |
| 6 | `semi_auto` + `audit_profile` | ☑ |

### §3.2 合并前 CI

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | PR pytest + 本地等价命令 | ☑ |
| 2 | 40/50 可核对（终轮） | ☐ 待 30/40/50（预期） |

### §Blocking · 高敏

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `api/` 新路由 + manifest | ☑ Q-8 已冻 · 验收/manifest 已列 |
| 2 | 50 关账必须 | ☑ `test_strategy_note` 已声明 |

### §3.3 独立复检（50）

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `required` + 涉契约 | ☑ |
| 2 | 关账前 50 落盘 | ☐ 待 30 后 |

### OpenSpec × TDD

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | test_strategy 与变更一致 | ☑ |
| 2 | Delta 已填 | ☑ |
| 3 | Scenario ID 列 | ☑ |
| 4 | validate pytest 可扫 | ☑ |

---

## 阻塞项

**无 task 文档层阻塞。**

> **运行闸（非 22 拒签理由）**：`HG-TASK-DRAFT` · `HG-AUDIT-R1` = `pending` → 30 **不得**写代码直至 **人**改 `approved`（建议 **两闸各单独 commit**）。

---

## 非阻塞项

| ID | 说明 |
|----|------|
| NB-1 | `gates_before_code` 文案写「HG-* = approved」，与 `human_gate` 表 `pending` **不一致** — 以表为准；人签后对齐文案（可选 10 小修） |
| NB-2 | 小节编号跳号（§5 → 验收/失败路径 → §8）— 不影响 validate |
| NB-3 | `freeze_id` 仍引用 research SPEC 而非单行 ID — P0 可接受 |
| NB-4 | R2 落盘后 task §8 必读第 7 条可补 R2 链（30 可顺手补，非阻塞） |
| NB-5 | Q-7 defer P1 — 已注明 |

---

## 需任务帽回填清单

- [ ] **无**（R2 不强制 10 帽改 task）

---

## 是否建议执行帽开工

| 结论 |
|------|
| **是** — 分支 `task/chatbi-graph-p0-foundation-v1`；须 `test_strategy: required`（先红后绿：边表 + runner smoke + Graph 路由 pytest）；**前提**：人签 `HG-TASK-DRAFT` + `HG-AUDIT-R1`；**禁止**改 `unified_chat.py` 行为 · **禁止**夹带 P1 parity。 |

---

## 签收 / 关闭

- **R2 结论**：**22-R2 approved（零阻塞）** — task 合同层 **可执行**；**不等同** task `done`。
- **须继续的条件**：30 → 40 自检 → CI 绿 → **50**（`reinspect_results/`）→ `post_close` 终轮 22 签收 → 归档 `done/`。
- **人须在本轮或开 30 前**：`HG-TASK-DRAFT` → `approved`；R2 签收后 **`HG-AUDIT-R1`** → `approved`。

---

## 下一棒可复制 Prompt

```text
你正在扮演工作区 Harness「执行编码帽」，严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（身份、只做什么、禁止什么、拒开工、输出形状、交接物）
- docs/harness/prompts/hats/40-self-check.md（验证命令、回填 task「### 自检结论（执行者）」）
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy、failure_paths、gates_before_code）
- 子仓 AGENTS.md、task 内「给执行帽的必读列表」、根 AGENTS.md §8（合并前必绿命令真值，若与本条 VERIFY 冲突以 task + 子仓 workflow 为准）

输入（已由人工替换占位符；若你仍看到 {{…}} 或「待填」，须先追问用户，不得开工写业务代码）：
- 主 task 路径（相对工作区根 Projects/）：
ai-ink-brain-api-python/docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md
- 逻辑子仓（task 路径前缀；相对 Projects/）：
ai-ink-brain-api-python
- Worktree 研发目录（所有 git/pytest/pnpm 默认 cwd；并行时须与 invoke 元信息 worktree_root 一致，见 docs/harness/README.md「并行分支与 Git worktree」）：
ai-ink-brain-api-python
- 合并前须跑通的验证命令（与 CI / task 一致）：
pytest tests -m "not intent_eval and not intent_benchmark"
- 关联任务审核书面结论路径（无则「无」）：
ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md
- 关联 SPEC / 总规（无则「无」）：
ai-ink-brain-api-python/docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md
ai-ink-brain-api-python/docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md
ai-ink-brain-api-python/docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 docs/harness/invokes/README.md 落盘到 docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
0b. **人工闸**：扫描 task / 关联 reviews 的 human_gate（见 docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md）。若任一对 **本帽（30）** 为 pending → 仅输出须人改的 gate_id 与路径，**拒开工**；禁止代填 approved。**例外**：若 invoke 声明 gate 已「人 kickoff 预批」但文件仍为 pending，Agent 须向用户二次确认（见 HANDOFF_SEMI_AUTO.md §2.3 预批与二次确认），获得明确文字授权后方可代填，且须在 commit message 注明 human_gate 由 Agent 按人授权代填。
1. 通读 task 全文：头部 gates_before_code、audit_profile、semi_auto、test_strategy / test_strategy_note、freeze_id、failure_paths、拒开工条件、验收标准、必读列表、非范围。
2. 若 task 明示拒开工条件未满足（缺 failure_paths 可操作性、缺验收命令、必读未覆盖等）→ **仅输出 Markdown 阻塞清单**（缺什么、建议回填的小节标题、推荐下一棒角色），**不写**业务实现代码。
3. test_strategy: required 时：先增加或调整 **可失败** 的自动化测试（或与实现同 PR 且满足 task 所述 red-green / 可复现失败语义），再改实现；禁止「只写实现、后补测」绕过 task 约定。
4. 在 ai-ink-brain-api-python 内按 task 范围改代码/配置（**禁止**在并行另一 worktree/checkout 改同一子仓）；禁止静默扩大 scope；SPEC/task 矛盾走变更请求或交回需求帽，不擅自调和为代码假设。
5. 在 ai-ink-brain-api-python 执行 pytest tests -m "not intent_eval and not intent_benchmark"（及 task 另行要求的命令），保留可核对输出要点；修复直至通过或记录环境阻塞并停止扩写。
6. 按 hats/40-self-check.md 将结论与命令摘要 **回填** 至 task 正文 ### 自检结论（执行者）（无则新增该小节）。
7. 对话回复：生成可以完整复制的 Prompt，用于直接交给下一棒执行；须兼顾打回、二次审查等情形，下一棒也可能是上一棒（由其修复问题）。
8. **自动 commit**：在输出下一棒 Prompt 且本轮代码/测试/task 自检回填已落盘后，按 docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md 在 ai-ink-brain-api-python 对应 git 根 commit（仅本轮路径；禁止 git add -A；对话报 short-hash）。用户写明「不要 commit」则跳过。
9. **半自动下一棒（可选）**：若 task semi_auto: true 且下一棒（如 40）无 human_gate 阻塞：先将 **下一棒 §3 全文** 落盘新 invoke 并 commit，再切换角色执行；规则见 HANDOFF_SEMI_AUTO.md §3。否则仅输出下一棒 Prompt 供人开新会话。

禁止：在未读完必读与 failure_paths 的情况下改路由/契约；删除与 task 无关的大段重构；口头宣称「已测过」而无命令输出。

【22-R2 审查约束（须一并遵守）】
- 五步顺序：① 抽 chatbi_events/models/failure ② ChatBIState + 边表（api/graph/state.py）③ api/graph/runner stub ④ Q-8 路由注册 + _manifest ⑤ 边表单测 + runner smoke。
- Q-8 冻结：POST /api/py/unified/chat/graph · POST /api/py/unified/chat/graph/stream；stub = HTTP 200 + 最小 JSON/SSE 心跳（项 5 选项 A）。
- D-2/D-5：unified_chat.py 行为零变更；不新增 graph.* SSE type。
- 关账前须 50 帽（test_strategy_note）；本 PR 仅实现 + 40 自检。
- 审查全文：ai-ink-brain-api-python/docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md
```
