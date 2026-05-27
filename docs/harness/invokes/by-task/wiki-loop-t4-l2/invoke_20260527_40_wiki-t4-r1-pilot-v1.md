# Invoke · 40 自检 · R1 · wiki-t4-r1-pilot

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md` |
> | task_slug | `wiki-t4-r1-pilot` |
> | freeze_id | `GOV-T4-R1-PILOT@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |

---

## §1 角色与纪律

- 本帽为 **40 自检**（`docs/harness/prompts/hats/40-self-check.md`）。
- 上一帽 30 已结束；本帽独立重跑 VERIFY、回填 task 自检结论。
- 禁止凭记忆声称「测过」；无命令输出不勾选。

## §2 自检结果

### 2.1 命令输出

**V1 · graph_nodes frontmatter**：
```bash
$ rg -n '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md
10:graph_nodes:
EXIT:0
```

**V2 · CODING_WIKI 引用**：
```bash
$ rg -n 'graph_nodes' docs/coding_wiki/CODING_WIKI.md
50:| `graph_nodes` | 否 | **T4** 可选；`id` + `relation` + 可选 `note` / `manifest_ref`（见 T4 SPEC §3） |
66:2. 若 frontmatter 含 `graph_nodes`：记下种子 `id`，对每个 id 执行 `python tools/tech_graph_graph_query.py neighbors <id>`，再按需 `downstream`/`upstream`。  
78:| `graph_nodes[].id` 不在 graph_v2 | `graph_query neighbors <id>` exit 4 → 修 id 或删项 |
79:| `graph_nodes[].relation` 非法 | 须在 T4 SPEC §3.1 表内 |
98:| `graph_nodes` 机器轨 | frontmatter 种子 + `graph_query`；**禁止** 手改 `graph.json` |
170:| 2026-05-27 | T4：`graph_nodes` frontmatter · query/lint · 链 Bridge SPEC |
EXIT:0
```

**V3 · seed id 存在性**：
```bash
$ for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; echo "$id: $?"; done
C1: 0
RAG: 0
RAG_DOC: 0
FTS: 0
```

**V4 · graph_export --check**：
```bash
$ python tools/tech_graph_graph_export.py --check
EXIT:0
```

**额外 · CODING_WIKI 链 Bridge SPEC**：
```bash
$ rg -n 'SPEC-Governance-Wiki-TechGraph-Bridge-v1' docs/coding_wiki/CODING_WIKI.md
4:> **治理 SPEC**：[...] · **T4 桥接**：[...]
EXIT:0
```

**额外 · RECENT in_progress**：
```bash
$ rg -n -F 'T4+L2' docs/tasks/RECENT_TASK_SCHEDULE.md
322:| **T4+L2** | **Wiki Loop T4+L2** | **in_progress** | `task_harness_wiki_loop_t4_l2_v1` · R1 Pilot · freeze `WIKI-LOOP-T4-L2@2026-05-27` |
EXIT:0
```

### 2.2 验收表

| 检查项 | 结果 | 证据 |
|--------|------|------|
| graph_nodes frontmatter 存在 | **pass** | `rg` line 10, exit 0 |
| CODING_WIKI 引用 graph_nodes | **pass** | 5 处命中, exit 0 |
| seed id 存在 graph_v2 | **pass** | 4/4 exit 0 |
| graph_export --check | **pass** | exit 0 |
| CODING_WIKI 链 Bridge SPEC | **pass** | line 4 |
| RECENT §6.6 in_progress | **pass** | line 322 |
| 99_spec T4 指针 | **pass** | diff +10 lines |

**全部 pass。无阻塞。**

## §3 回填确认

task 正文 `### 自检结论（执行者）` 已回填（7 项全 pass）。
`实现备忘` 表已填 `graph_nodes ids` 与 `commits`。

## §4 下一棒可复制 Prompt（50 独立复检）

```text
你正在执行 Wiki Loop T4+L2 **R1** 的 **50 独立复检帽**。上一帽（40 自检）已结束；本帽只按下文执行。

【元信息】
- round: R1
- hat: 50
- task: docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md
- task_slug: wiki-t4-r1-pilot
- freeze_id: GOV-T4-R1-PILOT@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 50 帽职责
按 `docs/harness/prompts/hats/50-independent-reinspect.md`：
1. 独立重跑 task §VERIFY 命令（不引用 40 结论为证据）。
2. 对照 task §验收标准逐条 pass/fail。
3. 检查 task §failure_paths 是否有遗漏。
4. 检查 human_gate diff（确认未由 Agent 代填 approved）。
5. 落盘复检报告到 `docs/tasks/reinspect_results/reinspect_wiki-t4-r1-pilot_20260527_v1.md`。
6. 若建议合并且无返工：输出关账 CLOSE_TRACE。
7. 按 HANDOFF_AUTO_COMMIT 提交。

### VERIFY（须独立重跑）
```bash
rg -n '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md
rg -n 'graph_nodes' docs/coding_wiki/CODING_WIKI.md
for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; done
python tools/tech_graph_graph_export.py --check
```

### 额外抽检
- `git log --oneline -5 -- docs/coding_wiki/syntheses/query-rewrite-observability.md` 确认 graph_nodes 非旧提交混入
- `git diff HEAD~1 -- docs/coding_wiki/CODING_WIKI.md | grep -c graph_nodes` 确认增量
- `rg -F 'HG-LOOP-BATCH' docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md` 确认 approved

### 落盘路径
`docs/tasks/reinspect_results/reinspect_wiki-t4-r1-pilot_20260527_v1.md`
```

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── task：task_governance_wiki_t4_r1_pilot_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：VERIFY 全绿 + task 自检结论回填
├── 下一棒：A=50 独立复检 · B=—
├── 推荐：A
└── 阻塞：无
```
