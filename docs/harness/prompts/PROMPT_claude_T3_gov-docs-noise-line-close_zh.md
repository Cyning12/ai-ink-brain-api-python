# PROMPT · T3 · docs-noise 治理线母单关账（Claude Code Lead · META）

> **用途**：整文件 `@` 给 Claude Code Lead；**§0–§6 全部必做**。  
> **前置**：P0–P3 子批均已 merge（#121/#123/#126/#129 + 关账 #122/#127/#130）；#128 已合 main。  
> **Round**：**T3** · CLOSE + META（无 explore/30 业务实现）  
> **slug**：`gov-docs-noise-line`  
> **git_branch**：`task/gov-docs-noise-t3-manifest-close-v1`  
> **MANIFEST**：[`docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`](../../tasks/active/task_governance_docs_noise_line_manifest_v1.md)

---

## §0 · 开跑前

    git checkout main && git pull
    git checkout -b task/gov-docs-noise-t3-manifest-close-v1

| 纪律 | 说明 |
| --- | --- |
| **禁止** | 改 `api/`、`tests/`、`.github/workflows/` · 代签 gate · 重跑 P0–P3 业务 |
| **禁止** | 删 `docs/harness/invokes/`、`reviews/` 历史 |
| **必须** | invoke 落盘 → **Lead commit**（§5.2）· `HANDOFF_CLOSE_TRACE` |
| **invoke** | `docs/harness/invokes/by-task/gov-docs-noise-line/invoke_YYYYMMDD_T3_CLOSE_meta.md` |

**对照简报（只读）**：`tmp/diary/2026-06-06-gov-docs-noise-line-close_zh.md`（若本机有）

---

## §1 · 母单 MANIFEST 关账

### §1.1 `git mv` + 状态

- `git mv docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md docs/tasks/done/`
- 文首状态 → `done（2026-06-06 · 治理线 CLOSE · main @ 最新关账 commit）`
- Round 表 **T3** 行：链至 **本文件**；标注 **done**
- `git_branch（当前子批）` → `—`（母单已 CLOSE）
- 修订记录加 T3 关账一行

### §1.2 `_views/done.md`

追加 MANIFEST 条目（链至 `done/task_governance_docs_noise_line_manifest_v1.md`）

---

## §2 · 导图 / 索引收尾（小 diff）

### §2.1 `docs/spec/governance/docs-noise-inventory/README.md`

- **§0 一句话**：改为「C1–C6 已 close · P0–P3 已执行 · 禁止删 audit 链」（勿再写「需修 C1–C3」）
- **§6**：确认已写「治理线已 CLOSE」；补 P3 T0/T2d PROMPT 链（若缺）
- **§8 修订记录**：T3 母单关账一行

### §2.2 `docs/harness/prompts/README.md`

文件列表增：`PROMPT_claude_T3_gov-docs-noise-line-close_zh.md`（本文件）

---

## §3 · 子批 task 文书补全（可选但推荐 · 仅 done task）

对下列 **done** task **仅**补文书（不改业务正文）：

| task | 动作 |
| --- | --- |
| `task_gov_docs_noise_p2_readorder_v1.md` | 验收 `- [ ]` → `- [x]`；KPI 表回填（参考 30/40 节已有内容） |
| `task_gov_docs_noise_p3_index_v1.md` | 同上 |

**禁止**改 P0/P1 除非仅补 `#127`/`#130` 关账 commit 引用一行。

---

## §4 · 验收（Lead 自检 · 不 spawn 40）

- [ ] MANIFEST 在 `docs/tasks/done/`
- [ ] `python tools/harness_task_validate.py docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md` → OK
- [ ] 导图 §0 不再写「需修 C1–C3」
- [ ] `git diff --stat` 仅 `docs/` 路径
- [ ] `_views/done.md` 含 MANIFEST

---

## §5 · CLOSE + PR

- PR 标题：`docs(governance): docs-noise T3 — MANIFEST 母单关账 + 导图 §0 收束`
- docs-only · CI Required 全绿后 merge
- 回报：`HANDOFF_CLOSE_TRACE`（含 P0–P3 PR 表 · #128）

**禁止**：开 P4 / 新治理子批（本 Epic 已 CLOSE）

---

## §6 · HANDOFF_CLOSE_TRACE 必含表

| 批次 | 执行器 | 业务 PR | 关账 PR |
| --- | --- | --- | --- |
| P0 | Cursor | #121 | #122 |
| P1 | Claude | #123 | #124/#125 |
| P2 | Claude | #126 | #127 |
| P3 | Claude | #129 | #130 |
| 流程 | — | — | #128 settings |

冲突寄存器：**C1–C6 done**。

---

## §7 · 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1：T3 母单关账 · CC handoff |
