# Invoke · 30 执行编码 · R2 · wiki-t4-r2-l0-align

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |

---

## §1 角色与纪律

- 本帽为 **30 执行编码**（`docs/harness/prompts/hats/30-execute-code.md`）。
- 上一帽 22 已结束；本帽执行 task §范围。
- 仅 docs；不改 api/、tests/、prompts/、CI。

## §2 执行摘要

**已交付**：VERIFY 全量重跑 + 记录。

| 命令 | 结果 | 输出 |
|------|------|------|
| `rg 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md` | pass | line 42, exit 0 |
| `python tools/tech_graph_manifest_check.py` | pass | exit 0 |
| `python tools/tech_graph_drift_check.py` | **fail** | exit 1（已知历史债务，见下） |
| `python tools/tech_graph_contract_check.py` | pass | exit 0 |
| `python tools/tech_graph_graph_export.py --check` | pass | exit 0 |
| `graph_query neighbors C1/RAG/RAG_DOC/FTS` | pass | 4/4 exit 0 |

### drift_check 详情（已知历史债务）

```
FAIL: tech graph drift detected.

Endpoints missing in docs/_tech_graph:
  - /api/py/live      ← P2-1a health/ready
  - /api/py/ready

Supabase tables missing in docs/_tech_graph:
  - chatbi_access_tokens   ← P1-3 分级闸门

Key env vars missing in docs/_tech_graph:
  - SUPABASE_HTTP_RETRIES           ← P2-1a
  - SUPABASE_HTTP_RETRY_BASE_DELAY_S
  - SUPABASE_INSERT_RETRIES
  - SUPABASE_INSERT_RETRY_BASE_DELAY_S
  - TEXT2SQL_DISTINCT_COLUMNS       ← P0 Text2SQL
  - TEXT2SQL_DISTINCT_MAX
  - TEXT2SQL_DISTINCT_MAX_PROBES
  - TEXT2SQL_DISTINCT_STMT_TIMEOUT_MS
  - TEXT2SQL_RETRIEVE_QUERY_MAX_LEN
  - TEXT2SQL_VALUE_HINTS_PATH
```

**结论**：上述 drift 均为 **之前任务引入的历史债务**（P2-1a、P1-3、P0），非 R2 范围。task §非范围明确 "不改 `.ai.md` 拓扑（无业务变更时）"。

## §3 下一棒可复制 Prompt（40 自检）

```text
你正在执行 Wiki Loop T4+L2 **R2** 的 **40 自检帽**。上一帽（30 执行编码）已结束；本帽只按下文执行。

【元信息】
- round: R2
- hat: 40
- task: docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md
- task_slug: wiki-t4-r2-l0-align
- freeze_id: GOV-T4-R2-L0-ALIGN@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 40 帽职责
按 `docs/harness/prompts/hats/40-self-check.md`：
1. 逐条对照 task §验收标准，标记 pass/fail。
2. 运行 task 所列 VERIFY 命令，粘贴原始输出要点。
3. 将结论回填至 task 正文 `### 自检结论（执行者）` 小节。
4. drift_check exit 1 须标注为 "已知历史债务，非本 round 引入"。
5. 输出 50 独立复检 invoke。
6. 按 HANDOFF_AUTO_COMMIT 提交。

### 验收标准与 VERIFY

- [ ] `rg 'Wiki ↔ 图谱桥接' docs/_tech_graph/99_spec.md`
- [ ] `python tools/tech_graph_manifest_check.py` exit 0
- [ ] `python tools/tech_graph_drift_check.py`（记录输出，标注已知债务）
- [ ] `python tools/tech_graph_contract_check.py` exit 0
- [ ] `python tools/tech_graph_graph_export.py --check` exit 0
- [ ] Pilot `graph_nodes` lint pass

### 回填位置
task 文件末尾 `### 自检结论（执行者）` 空表（若不存在则新增于「实现备忘」之上）。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── task：task_governance_wiki_t4_r2_l0_align_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：VERIFY 全量重跑 + drift 记录
├── 下一棒：A=40 自检 · B=—
├── 推荐：A
└── 阻塞：无
```
