# 独立复检 — T4 L0 对齐与 VERIFY（R2）

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | task | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | round | R2 |
> | invoke | `docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_20260527_50_wiki-t4-r2-l0-align-v1.md` |

---

## 复检结论

**建议合并。无阻塞项。**

drift_check exit 1 为 **已知历史债务**（P2-1a/P1-3/P0 引入），非 R2 范围。task §非范围明确 "不改 `.ai.md` 拓扑（无业务变更时）"。

---

## 验收项逐项判定

| # | 验收项 | 结果 | 证据 | 备注 |
|---|--------|------|------|------|
| A1 | `rg 'Wiki ↔ 图谱桥接' 99_spec.md` | **pass** | line 42, exit 0 | R1 f2f7505 已交付 |
| A2 | `manifest_check` exit 0 | **pass** | exit 0 | — |
| A3 | `drift_check` | **fail** | exit 1 | 已知历史债务，见下 |
| A4 | `contract_check` exit 0 | **pass** | exit 0 | — |
| A5 | `graph_export --check` exit 0 | **pass** | exit 0 | — |
| A6 | Pilot `graph_nodes` lint | **pass** | 4/4 exit 0 | C1/RAG/RAG_DOC/FTS |
| A7 | 未改 api/tests/prompts/CI | **pass** | diff 无相关路径 | — |
| A8 | human_gate 未由 Agent 代填 | **pass** | 母 task HG-LOOP-BATCH approved | — |

### drift_check 债务明细（非 R2 引入）

| 缺失项 | 来源 | 引入时间 |
|--------|------|----------|
| `/api/py/live`, `/api/py/ready` | P2-1a health/ready | 2026-05-25 |
| `chatbi_access_tokens` | P1-3 分级闸门 RBAC | 2026-05-13 |
| `SUPABASE_HTTP_RETRIES` 等 | P2-1a 韧性 | 2026-05-25 |
| `TEXT2SQL_DISTINCT_*` | P0 Text2SQL 可观测 | 2026-05-11 |

---

## 阻塞合并项

**无。**

---

## 是否建议合并

**是。** 全部 T4 相关验收通过；drift 为已有技术债务，不在 R2 范围。
