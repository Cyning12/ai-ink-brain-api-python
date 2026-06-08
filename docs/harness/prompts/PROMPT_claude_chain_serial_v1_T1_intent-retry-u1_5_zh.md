# PROMPT · Claude T1 · Intent LLM Retry U1.5（B 轨 · api 链式关账）

> **Round**：T1  
> **MANIFEST**：[task_harness_semi_auto_retirement_manifest_v1.md](../../tasks/active/task_harness_semi_auto_retirement_manifest_v1.md)  
> **task**：[task_chatbi_intent_llm_retry_u1_5_v1.md](../../tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md)  
> **git_branch**：`task/chatbi-intent-llm-retry-u1.5-chain-v1`  
> **slug**：`chatbi-intent-retry-u1.5-chain`  
> **merge_policy**：`docs_only_ci_green_merge`（含 api/ · 须 pytest 全绿）  
> **通用模板**：[PROMPT_claude_chain_serial_v1.md](PROMPT_claude_chain_serial_v1.md)

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞帽 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22-R1, 30 |
| `HG-CHAIN-B-EXEC` | `approved` | explore, 22, 30, 40, 50, CLOSE |
| `HG-REINSPECT` | `approved` | done · merge 前 |

任一为 `pending` → Lead **只报 gate_id + task 路径**，不 spawn subagent。

**开分支（Lead）**：

```bash
git checkout main && git pull
git checkout -b task/chatbi-intent-llm-retry-u1.5-chain-v1
# 若实现已在 task/chatbi-intent-llm-retry-u1.5：cherry-pick 或 merge 该分支 commits
```

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T1 · B 轨 api 链式关账）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_intent-retry-u1_5_zh.md（本文件 §2–§7）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

输入：
- MANIFEST：docs/tasks/active/task_harness_semi_auto_retirement_manifest_v1.md
- task：docs/tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md
- slug：chatbi-intent-retry-u1.5-chain
- git_branch：task/chatbi-intent-llm-retry-u1.5-chain-v1
- test_strategy：required（不可 skip 50）

Round T1 帽链：
  explore → 22 → 30 → 40 → 50 → CLOSE → PR → CI → merge

纪律：
1. GATE_SCAN；pending → 只报 gate_id
2. 每帽 invoke → Lead commit → spawn → ≤10 行摘要
3. Git 仅 Lead · subagent 禁止 commit
4. 30 帽：先失败测试 tests/test_intent_llm_retry.py 再改 api/intent_agent.py（TDD）
5. 40 帽：pytest tests -m "not intent_eval and not intent_benchmark" 全绿证据
6. 50 帽：落盘 docs/tasks/reinspect_results/reinspect_chatbi_intent_llm_retry_u1_5_*.md
7. 禁止代签 human_gate

完成后：HANDOFF_CLOSE_TRACE · HG-REINSPECT 须人签后再 merge
```

---

## 2. §3 explore 帽

**invoke**：`docs/harness/invokes/by-task/chatbi-intent-retry-u1.5-chain/invoke_*_explore_*.md`  
**交付物**：`explore_intent_retry_u1_5_impl_gap.md`

```text
【角色】Harness explore · B 轨 · api 差分

【canonical 读序】
1. docs/tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md
2. api/intent_agent.py（重试/超时相关段落）
3. tests/ 下是否已有 test_intent_llm_retry.py
4. docs/spec/v3-agent/ 或 task §行为变更 · failure_paths F1–F4

【forbidden】改代码 · docs/diary/** glob

【交付】实现缺口 · 已有 pytest 状态 · 30 帽 TDD 顺序建议 · cherry-pick 来源分支说明
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. §3 22 帽

**交付物**：`docs/harness/reviews/by-task/chatbi-intent-retry-u1.5-chain/task_chatbi_intent_llm_retry_u1_5_v1_audit_R1_*.md`

```text
【角色】Harness 22 · R1

【审查】test_strategy required · 50 不可 skip · semi_auto→false 迁移 · failure_paths Scenario ID · api 范围 bounded
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. §3 30 帽（spawn harness-30-execute-code）

```text
【角色】Harness 30 · api 实现 · TDD 硬约束

【读序】task · R1 · explore · api/intent_agent.py

【TDD 顺序 · 硬】
1. 先写/补全 tests/test_intent_llm_retry.py（覆盖 F1–F4 Scenario）
2. 确认失败后再改 api/intent_agent.py
3. pytest 目标测试绿 → 再跑全集 marker 命令

【forbidden】git commit · 扩大 task 非范围 · 改 .github/

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 5. §3 40 帽

```text
【角色】Harness 40 · 自检

【必须】
pytest tests -m "not intent_eval and not intent_benchmark"（全绿 · 贴摘要）
python tools/harness_task_validate.py docs/tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md → OK
task 验收项勾选证据

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 6. §3 50 帽（spawn harness-50-independent-reinspect）

```text
【角色】Harness 50 · 独立复检 · required 不可 skip

【读序】task · 40 证据 · api/intent_agent.py · tests/test_intent_llm_retry.py · R1

【交付】docs/tasks/reinspect_results/reinspect_chatbi_intent_llm_retry_u1_5_YYYYMMDD_v1.md

【审查】重试阶梯 · 超时 · failure_paths 与测试映射 · 无 scope creep

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 7. CLOSE

Lead：PR · CI · **HG-REINSPECT approved 后** merge · task → done/ · MANIFEST B 轨更新。

---

## 8. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | T1 脚手架 · B 轨 api 链 · 含 50 |
