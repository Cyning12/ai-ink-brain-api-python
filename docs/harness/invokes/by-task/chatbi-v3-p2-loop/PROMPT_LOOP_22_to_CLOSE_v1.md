# Loop 单 round 模板 · 22 → 关账（`chatbi-v3-p2-loop`）

> **用法**：断点续跑时替换下表占位符后粘贴 §3。  
> **全链首次**：优先 [`PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md`](./PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md)（含【授权】）。

| 占位符 | 示例 R1 | 示例 R2 |
|--------|---------|---------|
| `{round}` | R1 | R2 |
| `{task_path}` | `.../task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` | `.../task_chatbi_v3_p2_resilience_circuit_breaker_v1.md` |
| `{task_slug}` | `chatbi-v3-p2-loop-r1-closeout` | `chatbi-v3-p2-loop-r2-circuit-breaker` |
| `{freeze_id}` | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| `{50_required}` | 可选 | **必做** |

---

## §3 可复制 Prompt

```text
你正在执行 ChatBI P2 Loop **{round}** 帽链，严格遵循 HANDOFF_SEMI_AUTO、SKILL-harness-loop-batch、LOOP_MANIFEST。

开帽前：
python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
python tools/harness_human_gate_check.py --task {task_path}

【元信息】
- round: {round}
- task: {task_path}
- task_slug: {task_slug}
- freeze_id: {freeze_id}
- git_branch: task/chatbi-v3-p2-loop-v1
- 母 task: docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
- invoke: docs/harness/invokes/by-task/chatbi-v3-p2-loop/

【帽链】
- R1: 22 → 30 → 40（50 可选）
- R2: 22 → 30 → 40 → 50（required · 必落盘 reinspect）
- META: 22 → 30 → 40 → 50 → 关账 + REPORT_completion_chatbi_v3_p2_loop_v1.md

每帽：invoke §3 落盘 + commit。关账输出 Harness 状态栏（版本 B）。
```
