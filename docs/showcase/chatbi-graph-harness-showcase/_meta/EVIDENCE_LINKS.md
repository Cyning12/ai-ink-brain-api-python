# L1 证据指针一览

> 本系列 **不复制** 全文；续写时 `@` 下列路径。

## PR

| PR | 标题 | merge |
| --- | --- | --- |
| [#106](https://github.com/Cyning12/ai-ink-brain-api-python/pull/106) | 基线合并闸 | `26e1c45` |
| [#107](https://github.com/Cyning12/ai-ink-brain-api-python/pull/107) | P0 Graph 地基 | `f53327a` |

## Task

| slug | 路径 |
| --- | --- |
| `chatbi_baseline_merge_gate_v1` | `docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` |
| `chatbi_graph_p0_foundation_v1` | `docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` |

## 50 复检

| 文件 |
| --- |
| `docs/tasks/reinspect_results/reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md` |
| `docs/tasks/reinspect_results/reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md` |

## 22 审查

| 文件 |
| --- |
| `docs/harness/reviews/task_chatbi_baseline_merge_gate_v1_audit_R1_20260604.md` |
| `docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R1_20260603.md` |
| `docs/harness/reviews/task_chatbi_graph_p0_foundation_v1_audit_R2_20260603.md` |

## Invokes（按 task_slug）

| 目录 |
| --- |
| `docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/` |
| `docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/` |

## 路线图 SPEC

| 文件 |
| --- |
| `docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md` |
| `docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md` |

## 合并前必绿（本地）

```bash
pytest tests -m "not intent_eval and not intent_benchmark"
python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py
python tools/tech_graph_drift_check.py
```
