# 任务审核报告：chatbi-v3-lowconf-rag-preview · R1

| 字段 | 值 |
|------|-----|
| task | `docs/tasks/active/task_chatbi_v3_lowconf_rag_preview_v1.md` |
| audit_round | R1 |
| freeze_id | `CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31` |
| audit_profile | `full` |
| test_strategy | `required` |
| kpi_aggregator | `00` |
| invoke_snapshot | `docs/harness/invokes/by-task/chatbi-v3-lowconf-rag-preview/invoke_20260531_22_chatbi-v3-lowconf-rag-preview.md` |
| paired_fe | `ai-ink-brain` · `72f8f0c` · C1 契约已拍板 |
| reviewer | Agent（22 帽） |
| date | 2026-05-31 |

---

## 审查结论摘要

**零阻塞 · 可进入执行帽**

§0 re-baseline 确认：`main` 仅有 **text2sql** 低置信预览链；本单 **5-3** 须对称扩展 **rag_search** + 契约键 `rewrite_query` 等。Ink FE（`72f8f0c`）已消费 C1；后端 30 与 Ink **同 PR 或紧耦合 PR** 合并。

---

## 理论对齐检查表（P0）

### §3.1 / §3.3

| # | 检查项 | 通过 |
|---|--------|------|
| 1 | `test_strategy: required` + api/契约 | ☑ |
| 2 | `failure_paths` + Delta | ☑ |
| 3 | 全栈 FE-5 关账阻塞已声明 | ☑ |
| 4 | `harness_task_validate.py` | ☑（执行 30 后复跑） |

`harness_human_gate_check.py`：HG-REINSPECT **pending**（**预期**，仅阻塞 `done`；不阻塞 30）。

---

## C1 拍板（与 Ink 一致）

| 分支 | 承诺键 |
|------|--------|
| 公共 | `plan_id`, `tool`, `warnings`, `plan_execution_token`, `expires_in_sec` |
| `text2sql_query` | + `sql_draft` |
| `rag_search` | + `rewrite_query`（`planned_top_k`, `preview_headlines` 可选） |

**token**：`clarify_plan_once` + payload `t` 工具名；兼容 legacy `clarify_text2sql_once`。

---

## human_gate

| gate_id | status | blocks_hats | 结论 |
|---------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 不阻塞 |
| HG-AUDIT-R1 | approved | 30 | 不阻塞 |
| HG-REINSPECT | pending | done | 50 后、merge 前人签 |

---

## 阻塞项

**无阻塞。**

---

## 签收 / 关闭

- **R1**：30 可开工；范围 G1–G7；**G5 SSE parity 强制**  
- **双仓**：契约 `_contract_manifest.json` 与 Ink 镜像须 merge 前一致  
- **50**：须 **Fresh Context** 新会话  

---

## 下一棒可复制 Prompt

见 `docs/harness/invokes/by-task/chatbi-v3-lowconf-rag-preview/invoke_20260531_30_chatbi-v3-lowconf-rag-preview.md` §3。
