# SKILL 跨平台执行测评（v1）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `SKILL-CROSS-PLATFORM@2026-05-27` |
| **用途** | 记录 **通用 SKILL**（`docs/tasks/skills/SKILL-*.md`）在 **非 Cursor** 等 coding 平台上的实际执行与偏差，为后续通用性测评、Prompt 改进、ST 门禁强化提供 **可复现样本**。 |
| **与 Wiki-CTX-AB 实验的区别** | Wiki-CTX-AB 测 **上下文载荷**（H-full / H-lean / W）；本实验测 **Harness 帽链 + SKILL 可移植性**（平台是否自动加载 rules、semi_auto 是否连续、关账 hygiene 是否达标）。 |
| **真值 SKILL** | [`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../../../tasks/skills/SKILL-docs-governance.md) · [`SKILL-harness-loop-batch.md`](../../../tasks/skills/SKILL-harness-loop-batch.md) |

---

## 目录

| 路径 | 用途 |
| --- | --- |
| [`rubric_v1.md`](./rubric_v1.md) | **通用评分量表**（业务 / Harness 落盘 / PR 就绪 · 可叠加 ST1–ST6） |
| [`cases/`](./cases/) | 分 case 落盘：`scorecard.md` + `conclusion_zh.md` |
| `cases/<task_slug>_<platform>_<YYYYMMDD>/` | 命名：`gov-l2-manifest-ci_claude-code_20260527` |

---

## 支持平台（枚举 · 可扩展）

| platform_id | 说明 | 典型约束 |
| --- | --- | --- |
| `cursor` | Cursor Agent · 自动注入 `.mdc` rules | semi_auto、invoke 落盘较成熟 |
| `claude-code` | Claude Code CLI / 终端 Agent | **无** `.mdc` 自动加载 · 须显式 `@` 路径 |
| `kimi` | Kimi 等其它 Agent | 同 Claude Code · 显式读 SKILL |
| `third-party` | 三方复检 Agent | 通常只跑 50 / 测评臂 |

---

## 新增 case 流程

1. 选定 **task_slug** + **platform** + 使用的 **SKILL ID** 列表。
2. 在 `cases/` 下建目录，复制 [`cases/_TEMPLATE/scorecard.md`](./cases/_TEMPLATE/scorecard.md) 骨架。
3. 填 **三维评分**（见 `rubric_v1.md`）+ **ST1–ST6** 勾选 + 证据链（commit / PR / invoke 路径）。
4. 写 `conclusion_zh.md`：根因、对 SKILL/PROMPT 的改进建议（若已落盘则链 commit）。
5. （可选）在 [`docs/harness/README.md`](../README.md) §2 实验索引增一行。

**禁止**：将本目录结论覆盖 `docs/tasks/skills/` 或 `_tech_graph/` 实现真值；结论须 **人审** 后反哺 SKILL 正文。

---

## 已收录 case

| case | 平台 | SKILL | 业务 PR | hygiene PR | 摘要 |
| --- | --- | --- | --- | --- | --- |
| [`gov-l2-manifest-ci_claude-code_20260527`](./cases/gov-l2-manifest-ci_claude-code_20260527/) | Claude Code | harness-task · docs-governance | [#70](https://github.com/Cyning12/ai-ink-brain-api-python/pull/70) | [#71](https://github.com/Cyning12/ai-ink-brain-api-python/pull/71) | 单 task 22→关账 · ST5 关账正文债 · hygiene 后补 |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：实验目录 + rubric + 首 case（gov-l2-manifest-ci · Claude Code） |
