# Harness invoke snapshot — 10 帽 · B1 闸口 D（v2 题集扩域）

| 字段 | 值 |
| --- | --- |
| hat_id | 10 |
| template | `docs/harness/prompts/TEMPLATE-requirements-invoke.md` §3 |
| task_paths | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md`（由本帽 **新建**） |
| related_review_or_none | 无 |
| priority_roadmap | [`docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md`](../../../../docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md) §3 **B1** · INK-P5 |
| git_branch | **`task/engineering-tech-graph-gate-d-v2-tasks-v1`**（子 Agent **须自行创建**） |
| parallel_with | B3 · [`invoke_20260520_22_chatbi-v3-prompt-injection-closeout-audit.md`](invoke_20260520_22_chatbi-v3-prompt-injection-closeout-audit.md)（`task/chatbi-v3-prompt-injection-closeout-v1` · **禁止与本分支共用**） |
| created | 2026-05-20 |
| revised | 2026-05-20 |
| task_outcome | 2026-05-20：已产出 `docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md` v1.0；下一棒建议 **22 任务审核 R1** |

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-20 | 初版 invoke（INK-P5 / B1 闸口 D） |
| 2026-05-20 | 10 帽完成：task v1.0 落盘；freeze_id `TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0`；下一棒 **22** |

## 分支（子 Agent 必读）

1. **路线图**：开工前读 `docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md` §3 **B1**；关账后 **必须** 按 §0 更新 **INK-P5 / B1** 的 `路线图状态`。  
2. **仓库**：`ai-ink-brain-api-python`（勿改 `ai-ink-brain` 前端图谱）。  
3. **基线**：`git fetch` 后从 `main` 或维护者指定分支建线（若 C″ 规则 PR 未合并，可基于 `task/engineering-tech-graph-gate-c-double-prime-pr4-rules`）。  
4. `git checkout <基线> && git pull && git checkout -b task/engineering-tech-graph-gate-d-v2-tasks-v1`  
5. **禁止** 使用 `task/chatbi-v3-prompt-injection-closeout-v1`（B3 注入关账专用，见 parallel invoke）。

---

## 可复制 Prompt 正文（整段粘贴到新对话 user）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/10-requirements.md
- docs/harness/HARNESS_V2_PLAN.md §5
- docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md §0（关账后须回填路线图 INK-P5 / §3 B1）

【Git · 子 Agent 自行建分支】
- 仓库：ai-ink-brain-api-python
- git checkout -b task/engineering-tech-graph-gate-d-v2-tasks-v1
- 禁止共用分支 task/chatbi-v3-prompt-injection-closeout-v1（B3 · INK-P3）
- 禁止改 ai-ink-brain 前端仓；禁止重跑闸口 A/B/C 全量 batch（052803/083014/102810）
- 禁止共用分支 task/chatbi-v3-prompt-injection-closeout-v1（B3 · INK-P3 注入关账）

【目标与上下文】
PRIORITY_ROADMAP §3 B1 / INK-P5：将工作区草案「闸口 D — gate_ctx_ab_v2 题集扩域」立为正式 task，并细化可执行验收。
在维持 CTX_V2_QUERY 为 Agent machine 默认、沿用 C″ 物化策略前提下，金标题从 v1 三题扩为 v2（保留 v1 + 增量 T004 ChatBI/Text2SQL、T005 Intent/路由）。
产出：fixtures/tasks.json、物化与 batch 命令清单、freeze_id 命名、结论文路径约定；本帽不写 batch 跑分实现（交执行帽）。

【已有材料路径】
docs/tech_graph/tasks/PRIORITY_ROADMAP_v1_zh.md
ai_coding_governance/methodology/graph/drafts/draft_gate_ctx_ab_v2_expansion_v1.md
ai_coding_governance/methodology/graph/AGENT_GRAPH_CONSUMPTION_METHODOLOGY_v1_zh.md（§6.1、§7 T004/T005）
ai_coding_governance/methodology/graph/改进方向.md（闸口表 · 不修订 C/C′/C″ accepted）
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_double_prime_v1.md
ai-ink-brain-api-python/docs/tasks/done/task_engineering_tech_graph_gate_c_v2_dual_track_v1.md
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/
ai-ink-brain-api-python/docs/diary/jsonPKmermaid/reports/conclusion_gate_c_double_prime_v1_zh.md
docs/tech_graph/SPEC/query_graph/scheme_2_graph_query.md

【是否按任务审核文档回填】
无

你必须完成：
0. Invoke：落盘或更新 ai-ink-brain-api-python/docs/harness/invokes/invoke_20260520_10_tech-graph-gate-d-v2-tasks-requirements.md（含本 Prompt 快照）。
1. 在 task/engineering-tech-graph-gate-d-v2-tasks-v1 新建 docs/tasks/active/task_engineering_tech_graph_gate_d_v2_tasks_v1.md（从草案复制并补全：背景、范围/非范围、依赖、验收、failure_paths、test_strategy、gates_before_code、freeze_id 占位、给执行帽必读）。
2. 结构化输出：背景/范围/非范围/依赖/验收/failure_paths/给执行帽必读；矛盾单独小节。
3. test_strategy：required（pytest 门禁 + 实验可复现命令）。
4. 下一棒：输出 30 执行帽 或 22 审核帽 的可复制 Prompt 要点（含建议 run 目录、结论文文件名 conclusion_gate_d_ctx_v2_tasks_v1_zh.md）。
5. commit（invoke + task）；用户说不要 commit 则跳过。
6. 回复末尾给出 PRIORITY_ROADMAP §3 B1 行建议更新：planned → in_progress。

禁止：覆盖/改写 C/C′/C″ accepted 结论文；升 CTX_DUAL_MD 为默认；在本帽写 Neo4j/方案3；前端仓金标。
```
