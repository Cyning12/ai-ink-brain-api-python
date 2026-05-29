# 新 Agent 入口 · P2 Loop 全链（R1→R2→META · 仅粘贴一次）

> **用途**：`HG-LOOP-BATCH` = **approved** 后，**一条 user 消息**启动 R1，并 **授权同会话** 续跑 R2→META。  
> **分支（硬）**：`task/chatbi-v3-p2-loop-v1` · Open **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **母 task** | `docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md` |
| **当轮** | R1 · 见 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) |
| **SKILL** | `docs/tasks/skills/SKILL-harness-loop-batch.md` |

---

## 1. 执行前自检

```bash
git branch --show-current   # 须 task/chatbi-v3-p2-loop-v1
python tools/harness_human_gate_check.py \
  --task docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
test -f docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md
test -f docs/harness/invokes/by-task/chatbi-v3-p2-loop/PROMPT_LOOP_22_to_CLOSE_v1.md
```

---

## 2. 【授权】跨 round semi_auto（会话级 · 只出现一次）

```text
【授权】semi_auto 跨 round：R1 关账后无需停；按 LOOP_MANIFEST 依次执行 R2（须 50）→ META（须 22→50 + REPORT）。
每帽仍须：invoke §3 全文落盘 + git commit（HANDOFF_AUTO_COMMIT）。
顺序硬约束：R1→R2；R2 启动前 #0b/#W1 须在 done/。
```

---

## 3. 可复制 Prompt（全文复制到新对话）

```text
你正在执行 ChatBI P2 韧性 Loop **R1** 帽链：**22 → 30 → 40**（50 可选），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- semi_auto: true

【元信息】
- round: R1
- task: docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md
- task_slug: chatbi-v3-p2-loop-r1-closeout
- freeze_id: CHATBI-P2-R1-CLOSEOUT@2026-05-29
- git_branch: task/chatbi-v3-p2-loop-v1
- 母 task: docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
- invoke 目录: docs/harness/invokes/by-task/chatbi-v3-p2-loop/
- cross_round_semi_auto: true

【授权】semi_auto 跨 round：R1 关账后按 MANIFEST 续 R2→META。每帽 invoke + commit。

【R1 交付硬清单】
1. git mv #0b + W1 → done/（同日文首 done）
2. _views/done.md
3. RECENT §1.1 #0b/#W1 done；删 §1.2 双轨
4. 更新 done/task_chatbi_v3_p2_resilience_v1.md 子单表

硬约束：单 PR · R1 不改 api/ · 继承母闸 HG-LOOP-BATCH
```

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-29 | v1：P2 Loop 全链启动（整合 #86/#87 关账 + P2-1c） |
