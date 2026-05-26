# Wiki Loop 试点 · A1–A4（简化帽链）

> **目标**：单 PR、Cursor Agent；**只跑一轮 10**，之后每子 task **22 → 30 → 40 → 50 → 关账**（不再开 10）。

## 文件

| 文件 | 用途 |
|------|------|
| [`PROMPT_BATCH_10_four_tasks_v1.md`](./PROMPT_BATCH_10_four_tasks_v1.md) | **一次性**：生成母 task + A1～A4 四个 `active/task_*.md` 初稿 |
| [`PROMPT_START_loop_a1_full_chain_v1.md`](./PROMPT_START_loop_a1_full_chain_v1.md) | **全链启动（推荐）**：A1 粘贴 **一次** + 【授权】cross-round；含 commit 硬纪律 |
| [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) | **单 round 模板**（无【授权】）；断点续跑时按 MANIFEST 替换 §3 |
| [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) | 四轮路径 / slug / freeze_id / 回填关系 |

## 流程

```text
[会话 1 · 仅一次]
  PROMPT_BATCH_10 → 5 task + invoke_10_batch → commit

[会话 2 · 全链 · 推荐]
  人批 HG-LOOP-BATCH → PROMPT_START_loop_a1_full_chain §3（含【授权】一次）
  → A1..A4 各 22→30→40→50→关账 → META 关账 → 开 PR
  每帽：invoke 落盘 + commit（HANDOFF_AUTO_COMMIT）

[断点续跑 · 可选]
  读最新 invoke + MANIFEST 当 round → PROMPT_LOOP §3（不必再贴【授权】，若首 invoke 含 cross_round_semi_auto）
```

## 分支

`task/wiki-loop-a1-a4-v1` · **禁止在 `main` 连续提交**

## 人工闸

母 task `HG-LOOP-BATCH` = **approved** 后，子 task 文内写「继承母闸，不重复 pending」。

## cross-round【授权】放哪

| 放 | 不放 |
|----|------|
| `PROMPT_START_loop_a1_full_chain_v1.md` §2（会话级，一次） | `PROMPT_LOOP_22_to_CLOSE_v1.md` §3 模板正文 |

断点凭据：首份 A1·22 invoke 元信息 `cross_round_semi_auto: true`。

## invoke C2（第三批）

换帽前自检见 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) 步骤 1–5 · [`SKILL-harness-loop-batch`](../../../tasks/skills/SKILL-harness-loop-batch.md) §invoke 质量门禁。
