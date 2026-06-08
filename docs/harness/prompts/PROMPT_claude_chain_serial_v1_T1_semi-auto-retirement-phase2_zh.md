# PROMPT · Claude T1 · semi_auto 物理退场（Phase 2 · G3）

> **Round**：T1  
> **MANIFEST**：[task_harness_semi_auto_retirement_manifest_v1.md](../../tasks/done/task_harness_semi_auto_retirement_manifest_v1.md)  
> **task**：[task_harness_semi_auto_retirement_phase2_v1.md](../../tasks/active/task_harness_semi_auto_retirement_phase2_v1.md)  
> **git_branch**：`task/harness-semi-auto-retirement-phase2-v1`  
> **slug**：`harness-semi-auto-retirement-phase2`  
> **merge_policy**：`docs_only_ci_green_merge`  
> **通用模板**：[PROMPT_claude_chain_serial_v1.md](PROMPT_claude_chain_serial_v1.md)

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞帽 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22-R1, 30 |
| `HG-CHAIN-P2-EXEC` | `approved` | explore, 22, 30, 40, CLOSE |

任一为 `pending` → Lead **只报 gate_id + task 路径**，不 spawn subagent。

**开分支（Lead）**：

```bash
git checkout main && git pull
git checkout -b task/harness-semi-auto-retirement-phase2-v1
```

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T1 · Phase 2 semi_auto 物理退场）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_semi-auto-retirement-phase2_zh.md（本文件 §2–§6）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

输入：
- MANIFEST：docs/tasks/done/task_harness_semi_auto_retirement_manifest_v1.md
- task：docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md
- slug：harness-semi-auto-retirement-phase2
- git_branch：task/harness-semi-auto-retirement-phase2-v1
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
6. 禁止删 HANDOFF_SEMI_AUTO / 05 规则全文；须 DEPRECATED 横幅 + 链式 pointer

完成后：HANDOFF_CLOSE_TRACE · 更新 RECENT §1.4 · MANIFEST Phase 2 行
```

---

## 2. §3 explore 帽（spawn harness-explore-l0 或等价）

**invoke**：`docs/harness/invokes/by-task/harness-semi-auto-retirement-phase2/invoke_*_explore_*.md`  
**交付物**：`explore_semi_auto_retirement_phase2_gap.md`

```text
【角色】Harness explore · Phase 2 · 只读差分

【canonical 读序】
1. docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md
2. docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md
3. docs/harness/HARNESS_V2_PLAN.md §0.0 · §5.6
4. docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
5. .cursor/rules/05-harness-semi-auto.mdc · 06-harness-in-repo.mdc
6. docs/tasks/RECENT_TASK_SCHEDULE.md §0.0 · §1.3

【forbidden】api/** · tests/** · .github/** · 删历史 invoke/review

【交付】P2-1～P2-8 缺口表 · SPEC 是否仍写「待 B 轨」· §0.0 semi_auto 常模残留
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. §3 22 帽（spawn harness-22-audit）

**交付物**：`docs/harness/reviews/by-task/harness-semi-auto-retirement-phase2/task_harness_semi_auto_retirement_phase2_v1_audit_R1_*.md`

```text
【角色】Harness 22 · R1 审查

【读序】task · explore 报告 · A 轨 SPEC · MANIFEST

【审查】P2-1～P2-8 范围 · failure_paths F1–F4 · deprecated 策略是否可执行
【禁止】改 api/ · 代签 gate
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. §3 30 帽（spawn harness-30-docs）

```text
【角色】Harness 30 · 纯 docs · 执行 task §范围 P2-1～P2-8

【读序】task · R1（无阻塞）· explore

【forbidden】api/** · tests/** · .github/** · git log/blame · 删 invokes/reviews/done 历史

【必须完成】
- SPEC 全面生效 · §0/§1 完成态
- HARNESS_V2_PLAN §0.0 + §5.6 deprecated 表述
- HANDOFF_SEMI_AUTO DEPRECATED 横幅
- 05/06 .mdc deprecated + 链式 pointer
- TASK_TEMPLATE · README · AGENTS · RECENT §0.0/§1.4
- governance/prompts README · MANIFEST Phase 2 行
- harness_task_validate task → OK

【禁止 git commit · Lead 负责】
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 5. §3 40 帽（spawn harness-40-check）

```text
【角色】Harness 40 · docs-only 自检

【验证】
- rg -n 'DEPRECATED|deprecated|全面生效' docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md .cursor/rules/05-harness-semi-auto.mdc
- rg -n '待 B 轨' docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md  # 应无匹配
- python tools/harness_task_validate.py docs/tasks/active/task_harness_semi_auto_retirement_phase2_v1.md

【跳过】pytest · 50（not_applicable · task 明示）

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 6. CLOSE

Lead：`gh pr create` · CI Required 全绿 · `gh pr merge --squash`（task 授权）· `git mv` task → `done/` · 更新 MANIFEST Phase 2 → done · RECENT §1.4 CLOSE。

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | T1 脚手架 · Phase 2 G3 CC spawn 链 |
