# W5 留证占位 · 待人执行（2026-06-02）

> **task**：`docs/tasks/active/task_portfolio_rag_demo_v1.md`  
> **RUNBOOK**：[`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../../../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md)  
> **状态**：Agent **未**执行生产/预发 sync · **未**跑五问

## 人须完成（按序）

1. **前置**：确认 `CONTENT_ROOT` 指向前端 `content/` 且三目录各有 ≥1 `.md`（W4 就绪）
2. **Sync**（RUNBOOK §2）：`POST /api/py/admin/sync` → 轮询 `succeeded` → 硬检查 §2.3 → 落盘 `sync-job-final.json`（脱敏）
3. **Visitor token**（RUNBOOK §1.4）：`local_chatbi_access_token_gen.py` → INSERT → `GET /api/py/chatbi/access/verify`
4. **五问**（RUNBOOK §4–§6）：逐字问句 · Q3 strict evidence · 单问 ≤3 重试
5. **留证**：`q1-sources-run{1,2}.json`、`q5-sources-run{1,2}.json`、`five-questions-results.md`
6. **人闸**：task 内 `HG-W5-SYNC`、`HG-W5-FIVE-Q` → `approved`

## 阻塞说明

| gate_id | 当前 | blocks |
|---------|------|--------|
| HG-W5-SYNC | pending | W5 关账 |
| HG-W5-FIVE-Q | pending | task → done |

## curl 索引（脱敏 · 勿写入真实密钥）

```bash
# Sync（人执行）
curl -sS -X POST "$PY_API_URL/api/py/admin/sync" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# 五问（ChatBI visitor Bearer · 非 ADMIN_TOKEN）
curl -sS -X POST "$PY_API_URL/api/py/unified/chat" \
  -H "Authorization: Bearer $VISITOR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"<五问问句>","session_id":"portfolio-five-q-smoke"}'
```
