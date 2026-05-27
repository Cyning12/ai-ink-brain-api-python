# Retro Gap Analysis · gov-wiki-t4-expand · 2026-05-27

> **task_slug**: gov-wiki-t4-expand
> **freeze_id**: GOV-T4-EXPAND@2026-05-27
> **性质**: 关账后 hygiene 复盘 · **非**重新做 30 业务交付
> **触发**: 第三方复查发现 Harness / 索引缺口（N1–N5）

---

## §1 现象表（N1–N5）

| # | 缺口 | 严重程度 | 发现方式 | 修复 commit |
|---|------|----------|----------|-------------|
| **N1** | **22 review + 22 invoke + 30 invoke 缺失**；仅有 40/50/CLOSE | 高（Harness 链断裂） | 目录遍历发现 invoke 目录只有 3 个文件 | 4c9cc8f（追溯补全） |
| **N2** | **task 头部 `draft` 未改 `done`**；§范围/§验收 checkbox 未勾选 | 中（关账不完整） | 读 task 文件头部 | 6797f05（回填） |
| **N3** | **RECENT §6.6 T4 expand 行仍为 `draft`**；§8 缺 "done" 语义 | 中（索引未同步） | rg 'T4 expand' RECENT | 27f6cee（hygiene） |
| **N4** | **`_views/design.md` 仍链 `../active/task_*.md`**（已 git mv 到 done/） | 低（索引漂移） | 读 design.md | 27f6cee（hygiene） |
| **N5** | **40/50/CLOSE invoke 含 `round: R1`**（Loop 字段污染单 task） | 中（元信息错误） | 读 invoke 元信息表 | 4c9cc8f（去 round） |

**附加**：CLOSE invoke 写 `reinspec_*`（缺 `t`），与 N1 同批次修复。

---

## §2 根因（5 条假设 + 证据）

### R1 · .mdc 规则未加载（Claude Code 无自动加载）

**假设**：执行 Agent（Claude Code）未自动读取 `.cursor/rules/05-harness-semi-auto.mdc` 与 `06-harness-in-repo.mdc`，导致"单 task 无 round""每帽 invoke + commit"等约束未被感知。

**证据**：
- 40/50/CLOSE invoke 均含 `round: R1`（.mdc 中若加载应被拦截）。
- PROMPT_START §3 已写"Claude Code 无 .mdc 自动加载"，但执行时 Agent 未显式打开规则文件。

### R2 · 无 ST（单 task 合规自检）门禁

**假设**：关账前无逐项勾选清单（ST1–ST6），导致 22/30 invoke 和 22 review 的缺失未被拦截。

**证据**：
- 原始 CLOSE invoke 的 commit 表从 30 起跳，无 22 行。
- task 头部 `draft` 在关账 commit 中未改。

### R3 · Prompt 可跳帽（semi_auto 连续执行时易跳过）

**假设**：用户消息"阅读文档后开始任务"未明确说"从 22 开始"，Agent 直接进 30 编码。

**证据**：
- 最早 commit 是 `baf86bc`（30 执行编码），前面无 22 review/invoke 的 commit。
- dc67ec6 是"人签 approved + 单 task 全链 Prompt"，属于准备阶段而非 22 审核落盘。

### R4 · hygiene 与 git mv 顺序问题

**假设**：关账 commit（7bb878b）只做了 `git mv` + `_views/done.md` + CLOSE invoke，但未同步更新 RECENT §6.6/§8 和 design.md。

**证据**：
- RECENT §6.6 T4 expand 行在关账后仍为 `draft`。
- design.md 仍链 `../active/...`。

### R5 · Loop round 字段污染（元信息模板复用）

**假设**：Agent 复用了 Loop 的 invoke 模板（含 `round: R1`），未根据"单 task"场景删除该字段。

**证据**：
- 40/50/CLOSE 三文件元信息表结构一致，均含 `round: R1`。
- 单 task 的 PROMPT_START 中未明确写"invoke 元信息表禁止 round 字段"。

---

## §3 改进建议与实施状态

| # | 建议 | 目标文件 | 实施状态 |
|---|------|----------|----------|
| 1 | **单 task invoke 元信息去 round**：元信息表模板改为 hat / task_slug / freeze_id / git_branch / note；显式禁止 `round` 字段 | `SKILL-harness-task.md` | **已实施**（v1.2 §ST6 含"invoke 无 round 字段"） |
| 2 | **ST1–ST6 关账前自检**：缺任一项 = 不得关账；Claude Code 须显式勾选 | `SKILL-harness-task.md` | **已实施**（v1.2 新增 §ST1–ST6） |
| 3 | **禁止跳帽**：未落盘当前帽 invoke + commit → 禁止下一帽 | `PROMPT_START_full_chain_v1.md`（expand + l2） | **已实施**（expand v1.1 / l2 已增"禁止跳帽"） |
| 4 | **关账前 ST1–ST6 勾选**：写入 PROMPT_START §2 | `PROMPT_START_full_chain_v1.md`（expand + l2） | **已实施**（expand v1.1 已增） |
| 5 | **reinspect 拼写白名单**：`reinspec_` → `reinspect_` 常见 typo 拦截 | `SKILL-docs-governance.md` H1 | **已实施**（H1 已写"禁止 reinspec_"） |
| 6 | **H3/H4 与 git mv 同批提醒**：RECENT §8 / §6.6 建议与 ST5 同批或下一 commit | `SKILL-docs-governance.md` H3/H4 | **已实施**（H3 已写"建议与 ST5/git mv 同批或下一 commit"） |

---

## §4 与相关文件的关系

| 文件 | 角色 |
|------|------|
| `SKILL-harness-task.md` v1.2 | **真值源**：ST1–ST6 + 单 task 元信息规范 |
| `PROMPT_START_full_chain_v1.md`（expand · v1.1） | **入口**：禁止跳帽 + ST1–ST6 勾选 |
| `PROMPT_START_full_chain_v1.md`（l2 · 已同步） | **入口**：同上，防再犯 |
| `PROMPT_RETRO_hygiene_bc_v1.md` | **复盘入口**：本 REPORT 的快捷链 |
| `SKILL-docs-governance.md` v1 | **hygiene 真值**：H1–H6（含 git mv 同步提醒） |

---

## §5 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-27 | v1：N1–N5 现象表 + R1–R5 根因 + 6 条改进建议及实施状态 |

---

## 给 Cursor

`gov-wiki-t4-expand`、复盘、retro、gap analysis、ST1–ST6、禁止跳帽、单 task 合规、hygiene、关账后审计
