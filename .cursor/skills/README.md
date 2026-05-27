# 本仓 Cursor Skills（项目级）

> **与 `docs/tasks/skills/` 双轨**：内容语义一致；**跨 Agent 真值以 Git 内 `docs/tasks/skills/` 为准**（Claude Code、Kimi、Codex CLI 等通常读 `AGENTS.md` / `CLAUDE.md`，**不会**自动加载 `.cursor/skills/`）。

## 各平台能否读到？

| 落盘位置 | Cursor Agent | Claude Code | Kimi Code / 其它 |
|----------|--------------|-------------|------------------|
| **`.cursor/skills/<id>/SKILL.md`** | ✅ 项目 skill（用户 `@` 或描述匹配时） | ❌ 默认不读 | ❌ 默认不读 |
| **`docs/tasks/skills/SKILL-*.md`** | ✅ 可读（建议 `@` 路径） | ✅ 读 `AGENTS.md` 链入后 `@` 路径 | ✅ 人 `@` 或复制 Prompt |
| **`~/.cursor/skills/`**（用户级） | ✅ 全项目 | ❌ | ❌ |

**推荐**：关账蒸馏、Harness 流程类 skill **两处同步维护**；改一处时检查另一处 frontmatter / 索引是否一致。

## 本目录清单

| skill 目录 | 便携正文（Git 真值） |
|------------|----------------------|
| [`harness-meta-reinspect/`](harness-meta-reinspect/SKILL.md) | [`docs/tasks/skills/SKILL-harness-meta-reinspect.md`](../../docs/tasks/skills/SKILL-harness-meta-reinspect.md) |
| [`harness-loop-batch/`](harness-loop-batch/SKILL.md) | [`docs/tasks/skills/SKILL-harness-loop-batch.md`](../../docs/tasks/skills/SKILL-harness-loop-batch.md) |
| [`docs-governance/`](docs-governance/SKILL.md) | [`docs/tasks/skills/SKILL-docs-governance.md`](../../docs/tasks/skills/SKILL-docs-governance.md) |
| [`harness-task/`](harness-task/SKILL.md) | [`docs/tasks/skills/SKILL-harness-task.md`](../../docs/tasks/skills/SKILL-harness-task.md) |

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-24 | 初版：双轨说明 + `harness-meta-reinspect`（来源 P2-1 元复检） |
| 2026-05-26 | 新增 `harness-loop-batch`（Wiki Loop A1–A4 蒸馏） |
| 2026-05-27 | 新增 `docs-governance`、`harness-task`；`harness-loop-batch` 同步 v1.8 |
