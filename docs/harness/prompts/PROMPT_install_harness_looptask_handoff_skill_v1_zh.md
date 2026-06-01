# Prompt · 安装 Harness LoopTask 交接 SKILL（后端 Agent · 若缺失则创建）

> **用途**：粘贴 **§3 全文** 到 **Open Folder = `ai-ink-brain-api-python`** 的对话；由 Agent **检测并补齐** `harness-looptask-handoff` 双轨 skill（与前端 Epic 对齐）。  
> **便携真值模板**：若本仓尚无正文，以 **`ai-ink-brain/docs/tasks/skills/` 不存在时** 复制前端 `.cursor/skills/harness-looptask-handoff/SKILL.md` 语义，并 **改路径** 为本仓 `docs/tasks/` · `docs/harness/` 约定（见 [`docs/harness/README.md`](../README.md) §2.1）。  
> **已存在时**：只做 diff 对齐 + 更新 README 索引，**禁止** 重复创建冲突目录。

---

## 1. 前置

| 项 | 说明 |
|----|------|
| Open Folder | **`ai-ink-brain-api-python`**（本子仓根） |
| 工作区只读 | 可 `@` `ai-ink-brain/.cursor/skills/harness-looptask-handoff/SKILL.md` 作前端对照 |
| 双轨约定 | [`.cursor/skills/README.md`](../../.cursor/skills/README.md) · [`docs/tasks/skills/README.md`](../../docs/tasks/skills/README.md) |

---

## 2. 检测清单（Agent 先跑）

```bash
# 在 ai-ink-brain-api-python 根执行
test -f .cursor/skills/harness-looptask-handoff/SKILL.md && echo CURSOR=ok || echo CURSOR=missing
test -f docs/tasks/skills/SKILL-harness-looptask-handoff.md && echo PORTABLE=ok || echo PORTABLE=missing
```

| 结果 | 动作 |
|------|------|
| 两者 **ok** | 读 portable 真值 · 对照前端 skill · 仅补 README 索引行（若缺）· 输出「已安装 · 无需改动」或 patch 摘要 |
| 任一 **missing** | 按 §3 创建 **缺失文件** + 更新 **两个 README** + `docs/harness/README.md` §1 表一行 |
| 仅 Cursor 缺 | 写 `.cursor/skills/.../SKILL.md`（frontmatter + 链 portable） |
| 仅 portable 缺 | 写 `docs/tasks/skills/SKILL-harness-looptask-handoff.md`（完整条文） |

---

## 3. 可复制 Prompt 正文（从下一行起）

```text
## 角色

你是 **ai-ink-brain-api-python 仓 Harness 文档 Agent**，任务：**若缺失则安装** `harness-looptask-handoff` skill，并与前端 Portfolio LoopTask 交接规则对齐。

Open Folder = ai-ink-brain-api-python
禁止：改业务代码（api/ · tests/）；改 human_gate；提交 .env

## 必读

- docs/harness/README.md §1 · §2.1（落盘 taxonomy）
- .cursor/skills/README.md（双轨说明）
- docs/tasks/skills/README.md（索引表）
- docs/tasks/skills/SKILL-harness-looptask-handoff.md（若已存在则 diff）
- 对照（只读）：ai-ink-brain/.cursor/skills/harness-looptask-handoff/SKILL.md

## 你必须完成

1. **检测** §2 两条 `test -f`；在回复开头写 CURSOR / PORTABLE 状态。
2. **若 missing**：
   a. 创建 `docs/tasks/skills/SKILL-harness-looptask-handoff.md`（完整）：含
      - 何时选用 · Agent 必须交付三件事（50 Prompt / 签收清单 / 人改 gate 表）
      - 本子仓路径：`docs/tasks/active/` · `docs/harness/reviews/by-task/` · `docs/harness/invokes/by-task/` · `docs/tasks/reinspect_results/`
      - CLOSE 四步 · 人改 gate 模板表（文件+位置+改什么）
      - **跨仓 Portfolio**：前端 W5 路径表 + 后端 `.env` 的 `CONTENT_ROOT` 可选行
   b. 创建 `.cursor/skills/harness-looptask-handoff/SKILL.md`：YAML frontmatter（name/description/disable-model-invocation）+ 摘要 + 链 portable 真值
   c. 更新 `.cursor/skills/README.md` 清单表增加一行
   d. 更新 `docs/tasks/skills/README.md` 六类一览表增加 `harness-looptask-handoff` 行 + 目录结构树
   e. 更新 `docs/harness/README.md` §1 日常读什么表增加一行：「LoopTask 止于 50 · 50 Prompt / 人改 gate」→ portable skill 路径
3. **若已存在**：核对 portable 与 Cursor 摘要一致；缺 README 索引则只补索引。
4. **输出给人**（无论新建或已存在）：
   - skill 路径两行（Cursor + portable）
   - **当前无 LoopTask 关账时**：给出「人改 HG-REINSPECT」**模板表**（相对 `docs/tasks/active/task_*.md`），不要写「需要人签」而不写文件
   - **Portfolio 跨仓**：列出前端 W5 签收文档路径（`ai-ink-brain/content/harness/reviews/...` 等）
5. **commit**（用户未说「不要 commit」时）：仅本轮 skill + README 路径；message 建议 `docs(harness): add harness-looptask-handoff skill (dual-track)`

## 禁止

- 复制工作区 `Projects/docs/harness/prompts/` 整包到本仓
- 用笼统语句代替「文件 | 位置 | 改什么」表
- 代填任何 task 的 human_gate

Judgment：
- hat_self: pass | pass-with-notes | blocked
- 若 blocked：列出缺哪条路径、需人提供什么
```

---

## 4. 安装后期望落盘

| 文件 | 作用 |
|------|------|
| `docs/tasks/skills/SKILL-harness-looptask-handoff.md` | Git 便携真值 |
| `.cursor/skills/harness-looptask-handoff/SKILL.md` | Cursor `@` 入口 |
| `.cursor/skills/README.md` | 清单 +1 行 |
| `docs/tasks/skills/README.md` | 一览 +1 行 |
| `docs/harness/README.md` | §1 +1 行 |

---

## 5. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-01 | v1：后端安装 Prompt · 对齐前端 Portfolio W5 LoopTask handoff |
