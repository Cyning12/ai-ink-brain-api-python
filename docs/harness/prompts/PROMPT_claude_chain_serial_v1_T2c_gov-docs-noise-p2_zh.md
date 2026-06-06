# PROMPT · Claude T2c · gov-docs-noise P2（读序对齐 / legacy 消化）

> **Round**：T2c  
> **task**（T0 产出）：`docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md`  
> **git_branch**：`task/gov-docs-noise-p2-v1`  
> **slug**：`gov-docs-noise-p2`  
> **merge_policy**：`docs_only_ci_green_merge` · **close_action**：`merge`

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22, 30 |
| `HG-GOV-P2-EXEC` | `approved` | explore, 22, 30, 40, CLOSE |

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T2c · 执行 P2）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- 本文件 §2–§6（各 spawn 正文）
- docs/harness/prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md（R1 改稿真值）
- docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md
- docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md

GATE_SCAN 通过后串行 spawn（禁止 Agent Teams · 禁止 subagent 再 spawn）：
  harness-explore-l0 → harness-22-audit → harness-30-docs → harness-40-check → Lead CLOSE

跳过：harness-50-reinspect（纯 docs · not_applicable · MANIFEST 明示）

每帽：invoke 落盘 → **Lead commit** → spawn → ≤10 行摘要

（§5.2：subagent **禁止** git commit；30/40 只改文件 + 跑验证，由 Lead 在每帽后 commit）

close_action=merge：CI Required 全绿后 gh pr merge --squash

禁止：代签 gate · 删 audit 链 · 改 api/tests/workflows
```

---

## 2. §3 explore spawn（harness-explore-l0）

**交付**：`docs/harness/invokes/by-task/gov-docs-noise-p2/explore_P2_diff_YYYYMMDD.md`

```text
【角色】Harness explore · P2 只读差分

【本 task 允许读】
- docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md §A/B 前 30 行
- AGENTS.md「必读」节
- docs/README.md §1
- README.md Endpoints / env 段落
- docs/tasks/legacy/ 目录列表
- rg rag_fts_alias supabase/（判定 b2_v2 状态）

【canonical + SPEC §8.3 + task 路径】

【交付】P2-1~P2-4 现状 vs 期望 · canonical 子集对齐建议 · legacy 6 文件 done/archived 判定证据

【回报】≤10 行
```

---

## 3. §3 22 spawn（harness-22-audit）

**交付**：`docs/harness/reviews/by-task/gov-docs-noise-p2/task_gov_docs_noise_p2_readorder_v1_audit_R1_YYYYMMDD.md`

```text
【角色】Harness 22 · R1 · 零阻塞则建议 30 开工
【输入】task + explore 差分 + SPEC §8.3
【可选】python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md
【回报】≤10 行
```

---

## 4. §3 30 spawn（harness-30-docs）

```text
【角色】Harness 30 · P2 实现

【强制注入】
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md §5.1：禁止 git log/blame/考古 · 禁止读 task 范围外路径 · docs-only >10min 须停并向 Lead 汇报
- §5.2：**禁止** git add/commit/mv/push；改完回报文件清单，由 **Lead** commit

【交付】
- P2-1：PROJECT_CONFIG §A/B `.cursorrules` → 已移除；真值 `.cursor/rules/*.mdc`
- P2-2：AGENTS.md 与 docs/README.md §1 canonical 子集对齐 + 双向互链；保留扩展导航条
- P2-3：根 README.md Unified Chat 端点 pointer（或 PROJECT_CONFIG §F pointer）
- P2-4：legacy 6 文件消化（git mv done/ 或补 archived + pointer）+ _views/done.md 更新

【禁止】删 invoke/review 历史 · 改 legacy 正文全文 · 无证据判定 b2_v2 为 done
【回填】task ### 自检结论（执行者）
【回报】≤10 行
```

---

## 5. §3 40 spawn（harness-40-check）

```text
【角色】Harness 40 · 对照 task 验收 · 不跑 pytest
【验证】使用 task 内 40 表命令：
  - rg -n '\.cursorrules.*当前\|仍.*保留\|仍常保留' docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
  - rg -n 'AGENTS\.md\|docs/README\.md' AGENTS.md docs/README.md
  - rg -n 'unified/chat\|PROJECT_CONFIG.*§F' README.md
  - git diff --stat HEAD~1 -- api/ tests/ .github/workflows/
  - ls docs/tasks/legacy/
  - rg -n 'task_rag_b\|task_03\|Task 04' docs/tasks/_views/done.md
【回报】≤10 行 · 建议 CLOSE + PR
```

---

## 6. §3 CLOSE（Lead）

```text
invoke CLOSE → gh pr create → CI watch → merge（close_action）
→ 更新 docs/spec/governance/docs-noise-inventory/README.md 冲突寄存器 C4/C5 为 done（C6 不改）
→ HANDOFF_CLOSE_TRACE
```

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T2c 实例 · P2 执行链 |
| 2026-06-06 | v1.1：§5.2 Git 仅 Lead · 30 spawn 禁止 commit |
