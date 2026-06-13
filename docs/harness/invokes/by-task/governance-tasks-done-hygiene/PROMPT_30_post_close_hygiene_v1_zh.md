# PROMPT · 30 关账后卫生修复 + 总结 + SKILL 研判

> **类型**：文档-only 跟进（** governance-tasks-done-hygiene 关账后**）  
> **前置**：PR #160 已合或分支已含 Hub 交付 · **禁止改 `api/**`**  
> **invoke 母目录**：`docs/harness/invokes/by-task/governance-tasks-done-hygiene/`

---

## 背景（审查缺口 · 须修复）

P0 索引治理 **已达标**，但留有小缺口，易误导后续 Agent：


| #   | 缺口                                                                         | 期望                                              |
| --- | -------------------------------------------------------------------------- | ----------------------------------------------- |
| G1  | `task_governance_tasks_done_index_hygiene_v1.md` §3「思考未闭合→30 拒开工」与已关账矛盾    | 删或改「已关账 · §5 豁免」                                |
| G2  | §5 R0–R5 仍「（待填）」                                                           | 增「关账豁免」注或极简一行回填                                 |
| G3  | §2 C1/C2 未勾 · §8 已有自检                                                      | 与 §8 对齐勾选                                       |
| G4  | `reinspect_governance_tasks_done_index_hygiene_20260613_v1.md` 链 `active/` | 改链 `done/task_governance_...`                   |
| G5  | `coding_wiki/index.md` §维护 未写 Hub / `source_task` 扁平路径                     | 补 2～3 bullet                                    |
| G6  | invoke `README.md` 仍链 `active/task_...`                                    | 改 `done/`                                       |
| G7  | （可选）`done/<domain>/` 空目录未建                                                 | `mkdir` 六域 + `epics`（对齐 cyning-harness install） |


**不做**：P1 批量 `git mv` 138 篇 · 不改 syntheses `source_task` 路径。

---

## 可复制块（整段复制 · Open `ai-ink-brain-api-python/`）

```text
你是后端 Harness 执行 Agent（文档-only · 禁止 api/**）。

【任务】
governance-tasks-done-hygiene · 关账后卫生修复 + 总结 + SKILL 研判

【必读】
@docs/tasks/done/task_governance_tasks_done_index_hygiene_v1.md
@docs/tasks/done/README.md
@docs/tasks/_views/done.md
@docs/tasks/README.md
@docs/coding_wiki/index.md
@docs/tasks/reinspect_results/reinspect_governance_tasks_done_index_hygiene_20260613_v1.md
@docs/harness/invokes/by-task/governance-tasks-done-hygiene/README.md
@docs/tasks/skills/SKILL-docs-governance.md
@docs/tasks/skills/SKILL-harness-task.md
@../../../cyning-harness/harness/templates/TASK_done_README.md

【执行清单】

1) 修复 G1–G6（见上文表）
   - task §3：移除或替换「§5 待填→30 拒开工」为「本单 docs-only · §5 未走 10 长思考 · 已人签关账」
   - task §2：C1/C2 勾选并与 §8 一致
   - task §9 或 §11：追加一行「关账后卫生修复 YYYY-MM-DD」
   - reinspect：Task 链指向 docs/tasks/done/...
   - coding_wiki/index.md §维护：增
     · 关账更新 docs/tasks/done/README.md Hub 一行 + done_by_domain
     · syntheses source_task 仍指向 L1 扁平 done/*.md（P0）；浏览用 Hub
   - invoke README：task 真值路径改 done/

2) （可选 G7）创建空目录（若不存在）：
   docs/tasks/done/{harness,governance,chatbi,engineering,standards,epics}/

3) 链接复检（同关账时方法或简化 rg）
   - 至少扫：task · reinspect · index.md · invoke README
   - 结论写入 SUMMARY

4) 落盘总结（新建）：
   docs/harness/invokes/by-task/governance-tasks-done-hygiene/SUMMARY_post_close_hygiene_20260613.md

   SUMMARY 须含：
   · 修复项列表（G1–G7 逐项 pass/skip）
   · P0 与 cyning-harness 模板符合度（Hub/薄_views/FRAGMENT/Wiki · 物理域化=P1）
   · 与工作区 Harness 试点差异一句话
   · SKILL 研判结论（下节模板）
   · 是否建议开 follow-up PR（小 docs commit）

5) SKILL 研判（必须写入 SUMMARY §SKILL）

   阅读并对比：
   - docs/tasks/skills/SKILL-docs-governance.md §关账 hygiene H2（仍写「_views/done 增一行」）
   - docs/tasks/skills/SKILL-harness-task.md §关账 checklist 第 3 项（同上）

   判定规则：
   · 若 H2/checklist 与「Hub + done_by_domain · _views/done 薄指针」冲突 → **须更新 SKILL**
   · 若仅措辞过时、无行为冲突 → 更新并标修订记录
   · harness-loop-batch / 其他 SKILL：仅在 SUMMARY 写明「无需改」或「原因」

   若更新 SKILL：
   - 改 H2 为：更新 done/README.md Hub 一行 + done_by_domain；**禁止**向 _views/done.md 追加长列表
   - 改 harness-task checklist 第 3 项对齐
   - skills/README.md 一览表无需改 ID，可在 SKILL 修订记录写来源 task
   - **不**自动标 SKILL 为 active；保持 draft 或原 status，附「须人审」

【验收】
- [ ] G1–G6 已修 · 无矛盾句误导 Agent
- [ ] SUMMARY 已落盘
- [ ] SKILL 研判有明确结论（更新 / 不更新 + 理由）
- [ ] 若改了 SKILL：修订记录 + 来源 task 一行
- [ ] 零 api/** diff

【输出形状】
```text
阶段：关账后卫生 · pass
交付：{文件列表}
SKILL：{更新 SKILL-docs-governance + harness-task | 无需更新 · 理由}
建议：{是否单独 commit/PR}
```

本回复末尾附 SUMMARY 路径 + SKILL 结论摘要。你是后端 Harness 执行 Agent（文档-only · 禁止 api/**）。

【任务】
governance-tasks-done-hygiene · 关账后卫生修复 + 总结 + SKILL 研判

【必读】
@docs/tasks/done/task_governance_tasks_done_index_hygiene_v1.md
@docs/tasks/done/README.md
@docs/tasks/_views/done.md
@docs/tasks/README.md
@docs/coding_wiki/index.md
@docs/tasks/reinspect_results/reinspect_governance_tasks_done_index_hygiene_20260613_v1.md
@docs/harness/invokes/by-task/governance-tasks-done-hygiene/README.md
@docs/tasks/skills/SKILL-docs-governance.md
@docs/tasks/skills/SKILL-harness-task.md
@../../../cyning-harness/harness/templates/TASK_done_README.md

【执行清单】

1) 修复 G1–G6（见上文表）
   - task §3：移除或替换「§5 待填→30 拒开工」为「本单 docs-only · §5 未走 10 长思考 · 已人签关账」
   - task §2：C1/C2 勾选并与 §8 一致
   - task §9 或 §11：追加一行「关账后卫生修复 YYYY-MM-DD」
   - reinspect：Task 链指向 docs/tasks/done/...
   - coding_wiki/index.md §维护：增
     · 关账更新 docs/tasks/done/README.md Hub 一行 + done_by_domain
     · syntheses source_task 仍指向 L1 扁平 done/*.md（P0）；浏览用 Hub
   - invoke README：task 真值路径改 done/

2) （可选 G7）创建空目录（若不存在）：
   docs/tasks/done/{harness,governance,chatbi,engineering,standards,epics}/

3) 链接复检（同关账时方法或简化 rg）
   - 至少扫：task · reinspect · index.md · invoke README
   - 结论写入 SUMMARY

4) 落盘总结（新建）：
   docs/harness/invokes/by-task/governance-tasks-done-hygiene/SUMMARY_post_close_hygiene_20260613.md

   SUMMARY 须含：
   · 修复项列表（G1–G7 逐项 pass/skip）
   · P0 与 cyning-harness 模板符合度（Hub/薄_views/FRAGMENT/Wiki · 物理域化=P1）
   · 与工作区 Harness 试点差异一句话
   · SKILL 研判结论（下节模板）
   · 是否建议开 follow-up PR（小 docs commit）

5) SKILL 研判（必须写入 SUMMARY §SKILL）

   阅读并对比：
   - docs/tasks/skills/SKILL-docs-governance.md §关账 hygiene H2（仍写「_views/done 增一行」）
   - docs/tasks/skills/SKILL-harness-task.md §关账 checklist 第 3 项（同上）

   判定规则：
   · 若 H2/checklist 与「Hub + done_by_domain · _views/done 薄指针」冲突 → **须更新 SKILL**
   · 若仅措辞过时、无行为冲突 → 更新并标修订记录
   · harness-loop-batch / 其他 SKILL：仅在 SUMMARY 写明「无需改」或「原因」

   若更新 SKILL：
   - 改 H2 为：更新 done/README.md Hub 一行 + done_by_domain；**禁止**向 _views/done.md 追加长列表
   - 改 harness-task checklist 第 3 项对齐
   - skills/README.md 一览表无需改 ID，可在 SKILL 修订记录写来源 task
   - **不**自动标 SKILL 为 active；保持 draft 或原 status，附「须人审」

【验收】
- [ ] G1–G6 已修 · 无矛盾句误导 Agent
- [ ] SUMMARY 已落盘
- [ ] SKILL 研判有明确结论（更新 / 不更新 + 理由）
- [ ] 若改了 SKILL：修订记录 + 来源 task 一行
- [ ] 零 api/** diff

【输出形状】
```text
阶段：关账后卫生 · pass
交付：{文件列表}
SKILL：{更新 SKILL-docs-governance + harness-task | 无需更新 · 理由}
建议：{是否单独 commit/PR}

本回复末尾附 SUMMARY 路径 + SKILL 结论摘要。

```

---

## 给维护者

`post-close`、`SKILL-docs-governance`、`Hub`、卫生修复、关账后

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-13 | v1：关账后 G1–G7 修复 + SUMMARY + SKILL 研判 Prompt |
```

