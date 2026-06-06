# PROMPT · Claude T2d · gov-docs-noise P3（执行 · SPEC §8.4）

> **Round**：T2d
> **MANIFEST**：[task_governance_docs_noise_line_manifest_v1.md](../../tasks/active/task_governance_docs_noise_line_manifest_v1.md)
> **git_branch**：`task/gov-docs-noise-p3-v1`
> **slug**：`gov-docs-noise-p3`
> **task**：[docs/tasks/active/task_gov_docs_noise_p3_index_v1.md](../../tasks/active/task_gov_docs_noise_p3_index_v1.md)

---

## 0. 开跑前

| 项 | 说明 |
| --- | --- |
| **档期** | 读 RECENT §1.2 + MANIFEST · 确认 P3 为当前棒 |
| **gate** | `HG-GOV-P3-EXEC` 须 `approved`；否则阻塞 |

---

## 1. 强制注入（§5.1）

```text
【PROMPT §5.1 · 30-docs spawn 强制注入】

你执行 P3 SPEC §8.4 交付时：
1. 禁止 git log/blame/考古
2. 禁止读 task 范围外路径
3. docs-only 任务若单文件修改 >10min 须停并向 Lead 汇报
4. 优先 edit 现有文件而非新建；确需新建时先确认 Lead
```

---

## 2. §3 Lead 正文

```text
你 = Harness Lead（Claude Code · Round T2d · P3 执行）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2d_gov-docs-noise-p3_zh.md（本文件）
- docs/tasks/active/task_gov_docs_noise_p3_index_v1.md
- docs/spec/governance/docs-noise-inventory/README.md
- docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.4

开跑 SCHEDULE_SCAN：RECENT §1.2 → MANIFEST 确认 P3/T2d。

Round T2d 帽链：
  explore → 22 → 30 → 40 → CLOSE（跳过 50 · not_applicable）

各帽 spawn 须传入 §5.1 强制注入。

30 帽交付：
- P3-1a：docs/spec/governance/README.md 按 batch 聚合视图
- P3-1b：子目录 docs-noise-inventory/ 显式链入
- P3-2：docs/showcase/README.md 新建
- C6-optional：HARNESS_V2_PLAN.md 文首 superseded 标注（若成本低）

40 帽验证：
- rg 'docs-noise-inventory' docs/spec/governance/README.md
- rg 'showcase' docs/showcase/README.md
- rg 'L2|展示轨|非实现真值' docs/showcase/README.md
- git diff --stat HEAD -- api/ tests/ .github/workflows/（须无输出）
- 若执行 C6：rg 'superseded|archived' docs/harness/HARNESS_V2_PLAN.md

禁止：
- 删 invoke/review 历史
- 改正文全文（仅索引/标注）
- 改 api/ tests/ workflows

关账后：
- 更新 docs/spec/governance/docs-noise-inventory/README.md 冲突寄存器 C6（若解决）
- git mv task → done/ + _views/done.md + MANIFEST
```

---

## 3. §3 Subagent spawn 正文

### explore

```text
【角色】explore · P3 现状速览 · 只读
【目标】确认 governance/README 当前结构、showcase 目录内容、HARNESS_V2_PLAN 长度
【禁止】改任何文件
【交付】≤20 行摘要： governance/README 当前行数/分组状态；showcase 子目录清单；HARNESS_V2_PLAN 行数
```

### 22-audit

```text
【角色】22 审核帽 · P3 task 审阅
【读】task_gov_docs_noise_p3_index_v1.md + explore 摘要
【核】failure_paths 含 F#+Scenario ID；验收标准覆盖 P3-1/P3-2/C6-optional；范围/非范围清晰
【交付】audit_R2 文件 + 零阻塞建议开工 / 阻塞清单
```

### 30-docs

```text
【角色】30 docs 执行帽 · P3 SPEC §8.4 交付
【强制注入】§5.1（禁止考古、禁止范围外路径、>10min 停）
【读】task + governance/README + showcase/chatbi-graph-harness-showcase/README + HARNESS_V2_PLAN（仅文首）
【交付】
  1. docs/spec/governance/README.md：保留平面列表，新增按 batch 分组表
  2. docs/showcase/README.md：新建
  3.（optional）docs/harness/HARNESS_V2_PLAN.md：文首补 superseded
【回填】task ### 自检结论（执行者）
【禁止】改正文全文、改 api/tests/workflows
```

### 40-check

```text
【角色】40 自检帽 · P3 交付验证
【执行】task 中列出的 5 项 rg + git diff --stat
【回填】task ### 自检结论（40 帽回填 · T2d 后）
【结论】全绿 → 建议 CLOSE；红 → 列出阻塞
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T2d 实例 · P3 执行 PROMPT |
