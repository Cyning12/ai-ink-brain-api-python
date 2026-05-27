# 结论 · gov-l2-manifest-ci · Claude Code · 2026-05-27

> **case**：[`scorecard.md`](./scorecard.md) · **量表**：[`rubric_v1.md`](../../rubric_v1.md)

---

## 1. 一句话

Claude Code 在 **`PROMPT_START` + `SKILL-harness-task`** 驱动下，**业务交付优秀（95%）**，**Harness 帽链走通但关账正文 hygiene 薄弱（70%）**；经 **Part A 补债（PR #71）** 后可作为「单 task + 非 Cursor」的 **正面范例**，同时暴露与 `gov-wiki-t4-expand` **同根** 的 ST5 缺口。

---

## 2. 做对了什么

| 项 | 说明 |
| --- | --- |
| 帽链完整 | 22→30→40→50→CLOSE · 每帽 commit · 无跳帽 |
| 业务 VERIFY | 7/7 全绿 · CI workflow step 正确 |
| 人工闸 | HG-TASK-DRAFT / HG-AUDIT-R1 / HG-CI-WORKFLOW 均 approved 后改 workflow |
| 50 复检 | 独立 reinspect · 范围纪律 pass |
| semi_auto | 同会话连续执行（Claude Code 可做到，前提是 Prompt 写死） |

---

## 3. 偏差与根因

| 现象 | 根因 | 通用性 |
| --- | --- | --- |
| task 头部仍 `draft`、验收未 `- [x]` | 关账 commit 只做 `git mv`，未执行 ST5 正文项 | **高** · 非 Cursor 常见 |
| invoke §3 stub / &lt;15 行 | Prompt 虽写硬约束，**无自动校验** | **高** |
| invoke/review 链 `active/` | git mv 后未批量改元信息 | **高** · H5 |
| PROMPT_START 已含 ST1–ST6 仍漏执行 | **无关账前勾选 enforcement**（依赖 Agent 自觉） | **中** · 需 RETRO 或 CI lint |

**与 Cursor 差异**：Cursor 注入 `05-harness-semi-auto.mdc`，Claude Code **完全依赖** `PROMPT_START` 粘贴；漏读 HANDOFF = 漏 discipline。

---

## 4. 已反哺的改进（本仓）

| 工件 | 改动 |
| --- | --- |
| `SKILL-harness-task.md` | §ST1–ST6 单 task 合规自检 |
| `gov-l2-manifest-ci/PROMPT_START` | 关账前 ST 勾选 · 禁止跳帽 |
| `gov-l2-manifest-ci/PROMPT_RETRO` | PR #70 后 Part A hygiene |
| `gov-wiki-t4-expand/REPORT_retro_gap_analysis` | 同根因先例 |
| **本实验** | `skill_cross_platform_v1` · 可复用量表 + case 库 |

---

## 5. 后续测评建议

1. **同 task · Cursor 对照**：同一 `gov-l2-manifest-ci` 规格在 Cursor 跑一轮，比 ST5/§3 是否更好（预期略好，未必 100%）。
2. **Loop Batch · Claude Code**：`wiki-loop-*` 类母单 · 测 C1–C7 与 cross-round。
3. **自动化（远期）**：对 invoke §3 行数、task done 头部、active 链做 **pre-commit 或 CI lint**（docs-only）。

---

## 6. 裁决

| 问题 | 答案 |
| --- | --- |
| Claude Code 能否跑通 harness-task 单 task？ | **能**（本 case 已证） |
| 能否无 hygiene 直接「完美关账」？ | **不能**（须 Part A 或加强 Prompt/CI） |
| 是否推荐他平台默认用 PROMPT_START？ | **是** · 必须显式 SKILL + ST 勾选 + 可选 RETRO |
