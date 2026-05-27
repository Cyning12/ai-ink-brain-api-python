# 复盘报告 · gov-wiki-t4-expand · Harness 缺口与 SKILL 改进

> **task_slug**: gov-wiki-t4-expand  
> **freeze_id**: GOV-T4-EXPAND@2026-05-27  
> **日期**: 2026-05-27  
> **性质**: 业务已交付后的流程债追溯 + 规范蒸馏（非 Loop）

---

## §1 现象表

| ID | 现象 | 应然（真值） |
|----|------|----------------|
| N1 | 缺 22/30 invoke；无 22 review | `SKILL-harness-task` §落盘路径 |
| N2 | `done/` 内 task 头部仍为 `draft` | §关账 checklist #1 |
| N3 | RECENT §6.6 T4 expand 仍为 draft | `SKILL-docs-governance` H4 |
| N4 | RECENT §8 无关账单行 | H3 |
| N5 | invoke 元信息含 `round: R1` | 单 task **无 round** |

**业务侧**：3 篇 `graph_nodes`、reinspect 建议合并 — **无阻塞**。

---

## §2 根因分析（5 条 · 证据）

| # | 假设 | 成立？ | 证据 |
|---|------|--------|------|
| 1 | Claude Code **不加载** `.cursor/rules/*.mdc` | **是** | 无 semi_auto / 每帽 commit 硬约束除非 Prompt 写明 |
| 2 | 执行入口误用 **PROMPT_START only**，无 **PROMPT_RETRO** | **是** | START 无 Part B/C；Agent 从 30 交付直跳 40/50 |
| 3 | `harness-task` **无** loop-batch 同级 **C2/ST 门禁** | **是** | loop-batch 有 C1–C7；单 task 仅 checklist 分散 |
| 4 | **关账 hygiene** 与 `git mv` 未绑定同一 mental 步骤 | **是** | `git mv` 做了；RECENT/done 头部滞后 |
| 5 | **Loop 字段**（`round: R1`）渗入单 task Prompt/invoke | **是** | 拷贝 Loop 模板未改元信息表 |

---

## §3 与 Loop SKILL 对比

| 项 | `harness-loop-batch` | `harness-task`（改进前） |
|----|----------------------|-------------------------|
| 合规表 | C1–C7 + invoke C2 | 仅关账 checklist 5 条 |
| 入口 | PROMPT_START + PROMPT_LOOP | PROMPT_START only |
| 复盘 | REPORT_completion | **无** 强制 REPORT |

**结论**：单 task 须 **镜像精简版 ST1–ST6**（非 C1–C7 全表），并 **拆分 PROMPT_RETRO** 与 PROMPT_START。

---

## §4 已实施改进（本复盘 commit）

| 文件 | 改动 |
|------|------|
| `SKILL-harness-task.md` | §ST1–ST6 |
| `SKILL-docs-governance.md` | H3/H4 与 git mv 批次 |
| `gov-wiki-t4-expand/PROMPT_START_full_chain_v1.md` | 禁止跳帽 + ST |
| `gov-l2-manifest-ci/PROMPT_START_full_chain_v1.md` | 同上（防 L2 再犯） |
| `PROMPT_TASK_22_to_CLOSE_v1.md` | 步骤 0 ST |
| `PROMPT_RETRO_hygiene_bc_v1.md` | 本系列 Part A/B/C 合一 |

---

## §5 下一棒

- **L2** `gov-l2-manifest-ci`：用 **PROMPT_START** + 关账前 **ST1–ST6** 勾选  
- **勿** 再混用 START 承担复盘职责
