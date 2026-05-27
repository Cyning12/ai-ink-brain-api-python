# Invoke · 30 执行编码 · R1 · wiki-t4-r1-pilot

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md` |
> | task_slug | `wiki-t4-r1-pilot` |
> | freeze_id | `GOV-T4-R1-PILOT@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |

---

## §1 角色与纪律

- 本帽为 **30 执行编码**（`docs/harness/prompts/hats/30-execute-code.md`）。
- 上一帽 22 已结束；本帽只执行 task §范围。
- 仅 docs；不改 api/、tests/、prompts/、CI。

## §2 执行摘要

**已交付**（4 文件，+34/-4）：

| 文件 | 动作 | 说明 |
|------|------|------|
| `docs/coding_wiki/syntheses/query-rewrite-observability.md` | 增 frontmatter | `graph_nodes` 4 项（C1/RAG/RAG_DOC/FTS）+ 正文 T4 pointer |
| `docs/coding_wiki/CODING_WIKI.md` | 增字段/lint/链 | `graph_nodes` 可选字段、§4.2 query 读序、§4.3 lint 规则、链 Bridge SPEC |
| `docs/_tech_graph/99_spec.md` | 增小节 | Wiki↔图谱桥接（T4·叙事指针）pointer |
| `docs/tasks/RECENT_TASK_SCHEDULE.md` | 增行 | §6.6 Wiki Loop T4+L2 **in_progress** |

**预验证**：4 个 graph_nodes id 经 `graph_query neighbors` 全部 exit 0；relation 均在 Bridge SPEC §3.1 表内；`graph_export --check` exit 0。

## §3 下一棒可复制 Prompt（40 自检）

```text
你正在执行 Wiki Loop T4+L2 **R1** 的 **40 自检帽**。上一帽（30 执行编码）已结束；本帽只按下文执行。

【元信息】
- round: R1
- hat: 40
- task: docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md
- task_slug: wiki-t4-r1-pilot
- freeze_id: GOV-T4-R1-PILOT@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 40 帽职责
按 `docs/harness/prompts/hats/40-self-check.md`：
1. 逐条对照 task §验收标准，标记 pass/fail。
2. 运行 task 所列 VERIFY 命令，粘贴原始输出要点。
3. 将结论回填至 task 正文 `### 自检结论（执行者）` 小节。
4. 输出 50 独立复检 invoke。
5. 按 HANDOFF_AUTO_COMMIT 提交。

### 验收标准与 VERIFY

- [ ] `rg '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md`
- [ ] `rg 'graph_nodes' docs/coding_wiki/CODING_WIKI.md`
- [ ] 每个 seed id：`python tools/tech_graph_graph_query.py neighbors <id>` exit 0
- [ ] `python tools/tech_graph_graph_export.py --check` exit 0

**完整 VERIFY**：
```bash
rg -n '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md
rg -n 'graph_nodes' docs/coding_wiki/CODING_WIKI.md
for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; done
python tools/tech_graph_graph_export.py --check
```

### 额外检查
- CODING_WIKI.md 头部是否链 Bridge SPEC
- 99_spec.md 是否含 Wiki 桥接 pointer
- RECENT §6.6 是否有 T4+L2 in_progress 行

### 回填位置
task 文件末尾 `### 自检结论（执行者）` 空表（若不存在则新增于「实现备忘」之上）。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── task：task_governance_wiki_t4_r1_pilot_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：4 文件修改已 commit（f2f7505）
├── 下一棒：A=40 自检 · B=—
├── 推荐：A
└── 阻塞：无
```
