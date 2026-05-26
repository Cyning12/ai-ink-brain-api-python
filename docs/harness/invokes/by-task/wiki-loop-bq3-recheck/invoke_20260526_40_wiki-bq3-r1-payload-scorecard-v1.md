# Invoke · 40 自检 · R1 · wiki-bq3-r1-payload-scorecard

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_wiki_ctx_ab_multi_bq3_recheck_v1.md` |
| **task_slug** | `wiki-bq3-r1-payload-scorecard` |
| **freeze_id** | `WIKI-BQ3-R1-PAYLOAD@2026-05-26` |

---

## §3 可复制 Prompt 正文

```text
R1 · 40 自检帽：重跑 VERIFY；填 ### 自检结论（执行者）；落盘 invoke；commit。
VERIFY: rg -n test_strategy payloads/W_query-rewrite-observability.md
下一棒：50 独立复检
```

## VERIFY 输出

```
78:test_strategy: recommended
85:... L1 **`test_strategy: recommended`** ...
105:**Harness `test_strategy`**：`recommended` ...
```

**结论**：自检 pass → 准许 50。
