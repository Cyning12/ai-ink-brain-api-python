# R1 审核 · task_gov_docs_noise_p2_readorder_v1

> **日期**：2026-06-06  
> **审核帽**：22（Cursor 预审 · 供 Claude Code 改稿前真值）  
> **task**：[`docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md`](../../../../tasks/active/task_gov_docs_noise_p2_readorder_v1.md)  
> **CLI**：`python tools/harness_task_validate.py` → **OK**（改稿后须重跑）  
> **总判**：**条件通过** — 改稿 + 脚手架齐后再签 `HG-TASK-DRAFT` / 开 T2c

---

## 1. 通过项

| 维度 | 结论 |
| --- | --- |
| Harness 字段 | `task_slug` / `failure_paths` F1–F7 + Scenario ID / gates / `git_branch` 齐全 |
| SPEC §8.3 | P2-1～P2-4 与正文 §8.3 表一致 |
| 非范围 | 不碰 api/tests/ci · 不删审计链 |
| legacy 清单 | 6 文件与 `docs/tasks/legacy/` 一致 |
| P2-1 依据 | `.cursorrules` 仓库内**不存在**；PROJECT_CONFIG §B 仍写「仍常保留」 |
| P2-3 依据 | 根 `README.md` 无 Unified Chat / `CHATBI_*` |
| P1 继承 | `blocked_by` P1 done；30 帽 §5.1 已在 main（#125） |

---

## 2. 必改（B1–B3）

### B1 · P2-2「读序完全一致」过严

**问题**：`docs/README.md` §1 是 **docs 分类导航**（10+ 条）；`AGENTS.md` 是 **Agent 最小地图**（7 步）。SPEC §7 canonical 为 **5 步**。要求两文件「读序完全一致」会导致 30 帽删导航或越 scope。

**改法**：验收改为 **canonical 子集对齐 + 双向互链 + 扩展导航保留**（见 [`PROMPT_claude_P2_pre_exec_amendments_zh.md`](../../../prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md) §2.1）。

### B2 · 冲突寄存器编号错误

**问题**：task 背景写「C5/C6 = AGENTS vs docs/README」；SPEC 导图 §3 真值为：

| ID | 真值 | P2 对应 |
| --- | --- | --- |
| **C4** | PROJECT_CONFIG `.cursorrules` | P2-1 |
| **C5** | 根 README 端点/env 不完整 | P2-3 |
| **C6** | `HARNESS_V2_PLAN` vs `AGENTS` 权威链 | **P2 未覆盖** |
| （C2） | docs/README flows vs `_tech_graph` | P0 **done**；P2-2 做互链/子集复核 |

**改法**：背景 bullets、非范围、关账验收补 C6 说明（见改稿 Prompt §2.2–§2.3）。

### B3 · 执行脚手架缺失

| 项 | 状态 |
| --- | --- |
| `PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md` | 须新建 |
| `PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md` | 须新建 |
| MANIFEST P2 行 | 仍「未建」 |
| `docs-noise-inventory/README.md` §6 | 仍「下一棒 P1」 |

**改法**：见改稿 Prompt §3（CC 执行）。

---

## 3. 警告（T2c 执行注意 · 写入 T2c PROMPT）

| ID | 说明 |
| --- | --- |
| W1 | `task_rag_b2_v2_*`：**explore 须查** `supabase/` / `rag_fts_alias` 再定 done vs archived；禁止凭表直接 `git mv` |
| W2 | P2-1：除 §B 外 **§A L17** 也提 `.cursorrules`，须一并改 |
| W3 | 实际 diff >「四文件」：含 6×legacy + `_views/done.md` + 可能 `tasks/README.md` |
| W4 | CLOSE 时更新导图 **C4/C5** 冲突寄存器为 `done`（task 验收须加一条） |
| W5 | CLOSE 一次填 KPI/40，**禁止**留第二处「待回填」空节（P1 教训） |
| W6 | 30 帽遵守 `harness-30-docs` + PROMPT **§5.1**（禁止 git log 考古 · >10min 停） |

---

## 4. 现网差分（explore 用 · 禁止全库考古）

| ID | 现网 | 期望 |
| --- | --- | --- |
| P2-1 | PROJECT_CONFIG §A/B：`.cursorrules` 仍「兼容/仍常保留」 | 「已移除」；真值 `.mdc` |
| P2-2 | AGENTS ↔ docs/README **无互链** | 双向 pointer；§1 前 3–5 条与 AGENTS canonical 子集一致 |
| P2-3 | 根 README 仅 Legacy 端点 | Unified pointer 或 PROJECT_CONFIG §F |
| P2-4 | legacy 6 份未入 `_views/done.md` | mv/archived + 索引 |

---

## 5. Gate 建议

| gate_id | 建议 |
| --- | --- |
| `HG-TASK-DRAFT` | **改稿 Prompt 执行完成** + validate OK 后再 `approved` |
| `HG-GOV-P2-EXEC` | T0/T2c PROMPT + MANIFEST 就绪后再签 |

---

## 6. CC 下一棒

```text
@docs/harness/prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md
按全文执行 §1–§4；完成后回报 gate_id + 改动的文件列表。
```

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | R1 预审 · 条件通过 · 链改稿 Prompt |
