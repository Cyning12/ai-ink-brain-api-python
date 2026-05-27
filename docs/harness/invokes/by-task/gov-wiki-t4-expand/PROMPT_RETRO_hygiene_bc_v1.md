# Hygiene + 复盘 Prompt · gov-wiki-t4-expand（Part A / B / C 合一）

> **与 `PROMPT_START_full_chain_v1.md` 的区别**
>
> | 文件 | 何时用 |
> |------|--------|
> | **PROMPT_START** | **首次**全链执行 22→关账（业务交付） |
> | **本文件（PROMPT_RETRO）** | 已执行后 **补 Harness 债** + **根因复盘** + **SKILL 改进** + **对话 Part C** |
>
> **禁止** 只贴 PROMPT_START 时期望自动包含本文件的 Part B/C。

| 项 | 值 |
|----|-----|
| **task_slug** | `gov-wiki-t4-expand` |
| **freeze_id** | `GOV-T4-EXPAND@2026-05-27` |
| **分支** | `task/gov-t4-l2-followup-v1`（或从该分支拉出的执行分支） |
| **SKILL** | [`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../../../tasks/skills/SKILL-docs-governance.md) |

---

## 执行顺序（硬）

```text
若 Part A 已完成（5 invoke + review + done 头部 + RECENT）→ 跳过 Part A，只做 Part B + Part C
否则 → Part A → Part B → Part C（同一对话，分 commit）
```

---

## Part A · Hygiene 修复（N1–N5）

> **若已存在 commit** `4c9cc8f` / `6797f05` / `27f6cee` → **跳过 Part A**，在 Part C 注明「A 已由前序完成」。

### A1 · Harness 帽链（N1）

- [ ] `docs/harness/reviews/by-task/gov-wiki-t4-expand/task_governance_wiki_t4_expand_audit_R1_20260527.md`
- [ ] `invoke_20260527_22_gov-wiki-t4-expand-v1.md` · §3 ≥15 行 · **无** `round: R1`
- [ ] `invoke_20260527_30_gov-wiki-t4-expand-v1.md`（追溯 · 对应 baf86bc）
- [ ] 更新 40/50/CLOSE：元信息统一；CLOSE commit 表含 22→30→40→50→关账

### A2 · task done 正文（N2）

- [ ] `docs/tasks/done/task_governance_wiki_t4_expand_v2.md`：`done（日期 · freeze_id）` · 验收 `- [x]`

### A3 · RECENT（N3–N4）

- [ ] §6.6 **T4 expand** → **done**
- [ ] §8 增关账修订行

### A4 · invoke 元信息（N5）

- [ ] 单 task：**禁止** Loop 字段 `round: R1`

**VERIFY（A）**：

```bash
ls docs/harness/invokes/by-task/gov-wiki-t4-expand/invoke_*_{22,30,40,50,CLOSE}_*.md
test -f docs/harness/reviews/by-task/gov-wiki-t4-expand/task_governance_wiki_t4_expand_audit_R1_20260527.md
rg 'done（' docs/tasks/done/task_governance_wiki_t4_expand_v2.md
```

---

## Part B · 根因落盘 + SKILL 改进（必须）

### B1 · 新建复盘报告

路径：**[`REPORT_retro_gap_analysis_20260527_v1.md`](./REPORT_retro_gap_analysis_20260527_v1.md)**（≥40 行）

须含：现象表 · 5 条根因（.mdc / 无 ST / 跳帽 / hygiene 顺序 / Loop 字段污染）· 与 loop-batch C2 对比 · 改进已实施文件列表

### B2 · 实施 SKILL / PROMPT 改进（本仓应已含 ST1–ST6，若无则补）

| 文件 | 改动 |
|------|------|
| `docs/tasks/skills/SKILL-harness-task.md` | §单 task 合规自检 ST1–ST6 |
| `docs/tasks/skills/SKILL-docs-governance.md` | H3/H4 与 git mv 同批说明 |
| `PROMPT_START_full_chain_v1.md`（本目录 + `gov-l2-manifest-ci`） | 禁止跳帽 + 关账前 ST 勾选 |
| `PROMPT_TASK_22_to_CLOSE_v1.md` | 步骤 0：ST 门禁 |

**commit 建议**：`docs(skills): 单 task ST1–ST6 + PROMPT 禁止跳帽（gov-wiki-t4-expand 复盘）`

---

## Part C · 对话输出（必须 · 勿只写进文件）

在回复 **末尾** 原样输出以下四节（填真实 pass/fail）：

```markdown
### 修复核对表
| ID | 结果 | 备注 |
|----|------|------|
| N1 | pass/fail | … |
| N2 | pass/fail | … |
| N3 | pass/fail | … |
| N4 | pass/fail | … |
| N5 | pass/fail | … |

### 根因结论（3 条）
1. …
2. …
3. …

### SKILL/PROMPT 已改文件
- …

### 下一棒
- L2：`docs/harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_START_full_chain_v1.md`
- 执行前勾选 ST1–ST6 · 禁止跳帽
```

---

## 可复制 Prompt（全文粘贴 Claude Code）

```text
你正在 ai-ink-brain-api-python 执行 gov-wiki-t4-expand 的 **PROMPT_RETRO**（Part A/B/C 合一）。

【必读】
- docs/harness/invokes/by-task/gov-wiki-t4-expand/PROMPT_RETRO_hygiene_bc_v1.md（本文件）
- docs/harness/invokes/by-task/gov-wiki-t4-expand/REPORT_retro_gap_analysis_20260527_v1.md（Part B 产出或更新）
- docs/tasks/skills/SKILL-harness-task.md（§ST1–ST6）
- 分支：task/gov-t4-l2-followup-v1

【硬】
1. 先读 PROMPT_RETRO §执行顺序：Part A 若已完成则跳过
2. 必须完成 Part B（REPORT + 核对 SKILL/PROMPT 已有 ST）
3. 必须在回复末尾输出 Part C 四节（见上文模板）

禁止：开 L2 manifest CI 业务交付（仅可同步 PROMPT 防再犯）

开始。
```

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：Part A/B/C 合一落盘 · 区分 PROMPT_START |
