# Wiki Loop 试点 · A1–A4（简化帽链）

> **目标**：单 PR、Cursor Agent；**只跑一轮 10**，之后每子 task **22 → 30 → 40 → 50 → 关账**（不再开 10）。

## 文件

| 文件 | 用途 |
|------|------|
| [`PROMPT_BATCH_10_four_tasks_v1.md`](./PROMPT_BATCH_10_four_tasks_v1.md) | **一次性**：生成母 task + A1～A4 四个 `active/task_*.md` 初稿 |
| [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) | **每轮执行**：替换 `LOOP_MANIFEST` 中当轮占位符后粘贴 §3 代码块 |
| [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) | 四轮路径 / slug / freeze_id / 回填关系（人改「当轮」行即可） |

## 流程

```text
[会话 1 · 仅一次]
  PROMPT_BATCH_10 → 落盘 5 个 task + invoke_10_batch snapshot → commit

[会话 2..N · 每子 task 一轮]
  若当轮 task 含 <!-- PLACEHOLDER:... --> 且上一子 task 已关账：
    → 先读上一子 done task §实现备忘 / CLOSE commit，回填占位 → commit（可标 chore(backfill)）
  PROMPT_LOOP_22_to_CLOSE（当轮 MANIFEST 行）→ 22→30→40→50→关账
  关账帽末尾：若有下一轮，回填下一轮占位（见 PROMPT §关账）；**禁止** 为下一轮新建 10

[全部四轮 done 后]
  母 task PROMPT_LOOP（round=META）→ 关账母 task → 开 PR
```

## 分支

`task/wiki-loop-a1-a4-v1` · **禁止在 `main` 连续提交**

## 人工闸

母 task `HG-LOOP-BATCH` = **approved** 后，子 task 文内写「继承母闸，不重复 pending」。
