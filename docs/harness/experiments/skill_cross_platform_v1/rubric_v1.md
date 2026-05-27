# SKILL 跨平台测评 · 评分量表 v1

> **freeze_id**：`SKILL-CROSS-PLATFORM-RUBRIC@2026-05-27`  
> **适用**：`skill_cross_platform_v1/cases/*` 填表时对照；可与 [`SKILL-harness-task.md`](../../tasks/skills/SKILL-harness-task.md) §ST1–ST6 叠加。

---

## 1. 三维总评（0–100 · 可视化用百分比）

| 维度 | 测什么 | 90+ | 70–89 | &lt;70 |
| --- | --- | --- | --- | --- |
| **业务实现** | task 范围交付物是否齐全、VERIFY 是否真跑通 | 全交付 + 7/7 或 task 等价 VERIFY 绿 | 主交付齐全、 minor 缺口 | 缺核心文件 / 测试红 |
| **Harness 落盘** | invoke / review / reinspect / 帽链 commit / ST1–ST6 | 全帽 invoke §3≥15 · ST 全过 | 帽链走通但有 ST5/H5/§3 债 | 跳帽 / 无 reinspect / 无 review |
| **开 PR 就绪度** | 能否 **直接** 开可审 PR（含 docs hygiene） | 关账 checklist 全绿 | 业务可 PR、Harness 债另开 | 阻塞项未解 |

**填表格式**（scorecard 头部）：

```text
业务实现     ████████████████████  95%
Harness 落盘  ██████████████░░░░░░  70%
开 PR 就绪度   ████████████░░░░░░░░  60%
```

---

## 2. ST1–ST6 合规（单 task · 与 harness-task 对齐）

| # | 检查 | pass |
| --- | --- | --- |
| ST1 | 22 review + invoke_22 · §3 ≥15 行 | |
| ST2 | invoke_30 + 业务 commit 可对应 | |
| ST3 | invoke_40 + task §自检结论回填 | |
| ST4 | reinspect + invoke_50 | |
| ST5 | task 头部 done · 验收 `- [x]` · git mv · _views · CLOSE | |
| ST6 | RECENT §6.6/§8 · docs-governance H1–H5 | |

**注**：业务 PR 可先 merge，ST5 正文项可 **hygiene follow-up**（见 gov-l2-manifest-ci case）。

---

## 3. 平台偏差记录（每 case 必填）

| 字段 | 说明 |
| --- | --- |
| **rules 加载** | Cursor 自动 `.mdc` vs 他平台显式读 SKILL |
| **semi_auto 连续** | 是否同会话 22→关账 vs 中断/跳步 |
| **invoke §3 质量** | stub / &lt;15 行 / 达标 |
| **关账顺序** | git mv 先于 task done 正文等已知债 |
| **改进已落盘** | PROMPT_RETRO / SKILL 修订 · 链 commit/PR |

---

## 4. 与通用 SKILL 改进的映射

| 观测 | 建议反哺 |
| --- | --- |
| ST5 仅 git mv、不改 task 头部 | `SKILL-harness-task` 关账 checklist · `PROMPT_START` ST 勾选 |
| invoke §3 stub | invoke 质量硬约束 · 范例 invoke |
| active→done 引用残留 | `SKILL-docs-governance` H5 |
| 无 `.mdc` 漏读 HANDOFF | `PROMPT_START` 必读路径表 · Claude Code 范例 |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：三维 + ST1–ST6 + 平台偏差 · 源自 gov-l2-manifest-ci 审计 |
