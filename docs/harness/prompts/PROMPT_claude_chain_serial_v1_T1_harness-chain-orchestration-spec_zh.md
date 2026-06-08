# PROMPT · Claude T1 · Harness 链式编排 SPEC（A 轨 · semi_auto 退场）

> **Round**：T1  
> **MANIFEST**：[task_harness_semi_auto_retirement_manifest_v1.md](../../tasks/active/task_harness_semi_auto_retirement_manifest_v1.md)  
> **task**：[task_harness_chain_orchestration_spec_v1.md](../../tasks/active/task_harness_chain_orchestration_spec_v1.md)  
> **git_branch**：`task/harness-chain-orchestration-spec-v1`  
> **slug**：`harness-chain-orchestration-spec`  
> **merge_policy**：`docs_only_ci_green_merge`  
> **通用模板**：[PROMPT_claude_chain_serial_v1.md](PROMPT_claude_chain_serial_v1.md)

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞帽 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22-R1, 30 |
| `HG-CHAIN-A-EXEC` | `approved` | explore, 22, 30, 40, CLOSE |

任一为 `pending` → Lead **只报 gate_id + task 路径**，不 spawn subagent。

**开分支（Lead）**：

```bash
git checkout main && git pull
git checkout -b task/harness-chain-orchestration-spec-v1
```

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T1 · A 轨治理 SPEC）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_harness-chain-orchestration-spec_zh.md（本文件 §2–§6）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

输入：
- MANIFEST：docs/tasks/active/task_harness_semi_auto_retirement_manifest_v1.md
- task：docs/tasks/active/task_harness_chain_orchestration_spec_v1.md
- slug：harness-chain-orchestration-spec
- git_branch：task/harness-chain-orchestration-spec-v1
- merge_policy：docs_only_ci_green_merge
- close_action：merge

Round T1 帽链（串行 · 跳过 50 · not_applicable）：
  explore → 22 → 30 → 40 → CLOSE → PR → CI → merge

纪律：
1. GATE_SCAN 通过后按 §2–§6：每帽 invoke 落盘 → Lead commit → spawn harness-* → 收 ≤10 行
2. Git 仅 Lead（§5.2）；subagent 禁止 commit
3. test_strategy=not_applicable：40 不跑 pytest
4. 禁止改 api/ tests/ .github/
5. 禁止代签 human_gate

完成后：HANDOFF_CLOSE_TRACE · 更新 planning diary §5 checklist
```

---

## 2. §3 explore 帽（spawn harness-explore 或等价）

**invoke**：`docs/harness/invokes/by-task/harness-chain-orchestration-spec/invoke_*_explore_*.md`  
**交付物**：`explore_chain_orchestration_spec_gap.md`

```text
【角色】Harness explore · A 轨 · 只读差分

【canonical 读序】
1. docs/tasks/active/task_harness_chain_orchestration_spec_v1.md
2. docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md（草案）
3. docs/tasks/templates/TASK_TEMPLATE.md
4. docs/harness/HARNESS_V2_PLAN.md §5.6
5. docs/diary/2026-06-08-harness-chain-next-task-planning_zh.md §7

【forbidden】api/** · tests/** · .github/** · 改业务交付文件

【交付】A-1～A-7 缺口表 · TASK_TEMPLATE 是否缺 orchestration · §5.6 semi_auto 表述对照
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. §3 22 帽（spawn harness-22-task-audit）

**交付物**：`docs/harness/reviews/by-task/harness-chain-orchestration-spec/task_harness_chain_orchestration_spec_v1_audit_R1_*.md`

```text
【角色】Harness 22 · R1 审查

【读序】task · explore 报告 · SPEC 草案 · MANIFEST

【审查】A-1～A-7 范围 · failure_paths F1–F3 · orchestration/semi_auto 关系是否清晰
【禁止】改 api/ · 代签 gate
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. §3 30 帽（spawn harness-30-docs）

```text
【角色】Harness 30 · 纯 docs · 执行 task §范围 A-1～A-7

【读序】task · R1（无阻塞）· explore · SPEC 草案

【forbidden】api/** · tests/** · .github/** · git log/blame · 删 invokes/reviews 历史

【必须完成】
- 定稿 SPEC-Governance-Harness-Chain-Orchestration-v1.md
- TASK_TEMPLATE 增 orchestration 行
- HARNESS_V2_PLAN §5.6 链式常模 + semi_auto 过渡/废弃
- governance README · prompts README · docs-noise §6 · RECENT §1.3 一行表
- harness_task_validate task → OK

【禁止 git commit · Lead 负责】
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 5. §3 40 帽（spawn harness-40-self-check）

```text
【角色】Harness 40 · docs-only 自检

【验证】
- rg orchestration docs/tasks/templates/TASK_TEMPLATE.md
- test -f docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md
- python tools/harness_task_validate.py docs/tasks/active/task_harness_chain_orchestration_spec_v1.md

【跳过】pytest · 50（not_applicable · task 明示）

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 6. CLOSE

Lead：`gh pr create` · CI Required 全绿 · `gh pr merge --squash`（task 授权）· `git mv` task → done/ · 更新 MANIFEST A 轨状态。

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | T1 脚手架 · A 轨 CC spawn 链 |
