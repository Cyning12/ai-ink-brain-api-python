# PROMPT · Claude T2b · gov-docs-noise P1（archived / flows）

> **Round**：T2b  
> **task**（T0 产出）：`docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md`  
> **git_branch**：`task/gov-docs-noise-p1-v1`  
> **slug**：`gov-docs-noise-p1`  
> **merge_policy**：`docs_only_ci_green_merge` · **close_action**：`merge`

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22, 30 |
| `HG-GOV-P1-EXEC` | `approved` | explore, 22, 30, 40, CLOSE |

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T2b · 执行 P1）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- 本文件 §2–§5（各 spawn 正文）
- docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md
- docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md

GATE_SCAN 通过后串行 spawn（禁止 Agent Teams · 禁止 subagent 再 spawn）：
  harness-explore-l0 → harness-22-audit → harness-30-docs → harness-40-check → Lead CLOSE

跳过：harness-50-reinspect（纯 docs · not_applicable · MANIFEST 明示）

每帽：invoke 落盘 → commit → spawn → ≤10 行摘要

close_action=merge：CI Required 全绿后 gh pr merge --squash

禁止：代签 gate · 删 audit 链 · 改 api/tests/workflows
```

---

## 2. §3 explore spawn（harness-explore-l0）

**交付**：`docs/harness/invokes/by-task/gov-docs-noise-p1/explore_P1_diff_YYYYMMDD.md`

```text
【角色】Harness explore · P1 只读差分

【本 task 允许读】（T2b 例外）
docs/delivery/v0.2.0-code-rag/README.md
docs/flows/ 目录列表 + 现有 rag-chat 快照文件名

【canonical + SPEC §8.2 + task 路径】

【交付】P1-1/P1-2 现状 vs 期望 · archived 横幅建议文案 · flows README 大纲

【回报】≤10 行
```

---

## 3. §3 22 spawn（harness-22-audit）

**交付**：`docs/harness/reviews/by-task/gov-docs-noise-p1/task_gov_docs_noise_p1_archived_v1_audit_R1_YYYYMMDD.md`

```text
【角色】Harness 22 · R1 · 零阻塞则建议 30 开工
【输入】task + explore 差分 + SPEC §8.2
【可选】python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md
【回报】≤10 行
```

---

## 4. §3 30 spawn（harness-30-docs）

```text
【角色】Harness 30 · P1 实现
【交付】
- P1-1：docs/delivery/v0.2.0-code-rag/README.md 文首 archived 横幅 + 链 harness/spec
- P1-2：新建 docs/flows/README.md（freeze 日期 · Legacy chat · superseded by _tech_graph）
【禁止】删 invoke/review 历史
【回填】task ### 自检结论（执行者）
【回报】≤10 行
```

---

## 5. §3 40 spawn（harness-40-check）

```text
【角色】Harness 40 · 对照 task 验收 · 不跑 pytest
【验证】test -f docs/flows/README.md · rg archived docs/delivery/v0.2.0-code-rag/README.md
【回报】≤10 行 · 建议 CLOSE + PR
```

---

## 6. §3 CLOSE（Lead）

```text
invoke CLOSE · gh pr create · CI watch · merge（close_action）· HANDOFF_CLOSE_TRACE
```

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T2b 实例 · P1 执行链 |
