# Invoke · 40 自检 · R2 · wiki-t4-r2-l0-align

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |

---

## §1 角色与纪律

- 本帽为 **40 自检**（`docs/harness/prompts/hats/40-self-check.md`）。
- 上一帽 30 已结束；本帽独立重跑 VERIFY、回填 task 自检结论。

## §2 自检结果

### 2.1 命令输出

**99_spec T4 小节**：
```bash
$ rg -n 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md
42:### Wiki ↔ 图谱桥接（T4 · 叙事指针）
EXIT:0
```

**manifest_check**：
```bash
$ python tools/tech_graph_manifest_check.py
OK: manifest matches code/SQL truth
EXIT:0
```

**drift_check**：
```bash
$ python tools/tech_graph_drift_check.py
FAIL: tech graph drift detected.
Endpoints missing: /api/py/live, /api/py/ready
Tables missing: chatbi_access_tokens
Env missing: SUPABASE_HTTP_RETRIES, SUPABASE_HTTP_RETRY_BASE_DELAY_S, ...
EXIT:1
```

**contract_check**：
```bash
$ python tools/tech_graph_contract_check.py
OK: cross-repo contract check passed
EXIT:0
```

**graph_export --check**：
```bash
$ python tools/tech_graph_graph_export.py --check
EXIT:0
```

**Pilot graph_nodes lint**：
```bash
$ for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" > /dev/null; echo "$id: $?"; done
C1: 0
RAG: 0
RAG_DOC: 0
FTS: 0
```

### 2.2 验收表

| 检查项 | 结果 | 证据 |
|--------|------|------|
| 99_spec T4 小节存在 | **pass** | line 42, exit 0 |
| manifest_check | **pass** | exit 0 |
| drift_check | **fail** | exit 1；已知历史债务，非 R2 引入 |
| contract_check | **pass** | exit 0 |
| graph_export --check | **pass** | exit 0 |
| Pilot graph_nodes lint | **pass** | 4/4 exit 0 |

**结论**：5/6 直接通过；drift_check fail 为已知历史债务（P2-1a/P1-3/P0），task §非范围明确不修复。无阻塞。

## §3 回填确认

task 正文 `### 自检结论（执行者）` 已回填（6 项 + drift 债务标注）。
`实现备忘` 表已填 `commits`。

## §4 下一棒可复制 Prompt（50 独立复检）

```text
你正在执行 Wiki Loop T4+L2 **R2** 的 **50 独立复检帽**。上一帽（40 自检）已结束；本帽只按下文执行。

【元信息】
- round: R2
- hat: 50
- task: docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md
- task_slug: wiki-t4-r2-l0-align
- freeze_id: GOV-T4-R2-L0-ALIGN@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 50 帽职责
按 `docs/harness/prompts/hats/50-independent-reinspect.md`：
1. 独立重跑 task §VERIFY 命令（不引用 40 结论为证据）。
2. 对照 task §验收标准逐条 pass/fail。
3. drift_check exit 1 须确认为 "已知历史债务"（非 R2 引入的端点/表/env drift）。
4. 检查 human_gate diff（确认未由 Agent 代填 approved）。
5. 落盘复检报告到 `docs/tasks/reinspect_results/reinspect_wiki-t4-r2-l0-align_20260527_v1.md`。
6. 若建议合并且无返工：输出关账 CLOSE_TRACE。
7. 按 HANDOFF_AUTO_COMMIT 提交。

### VERIFY（须独立重跑）
```bash
rg -n 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" > /dev/null; done
```

### 落盘路径
`docs/tasks/reinspect_results/reinspect_wiki-t4-r2-l0-align_20260527_v1.md`
```

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── task：task_governance_wiki_t4_r2_l0_align_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：VERIFY 5/6 pass + task 回填 + drift 债务标注
├── 下一棒：A=50 独立复检 · B=—
├── 推荐：A
└── 阻塞：无
```
