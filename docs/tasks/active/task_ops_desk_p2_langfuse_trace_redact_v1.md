# Task · Ops Desk P2-5b-hotfix · Langfuse Trace Input 脱敏

> **状态**：`active` · **P0** · 2026-06-25
> **触发**：P2-5b 人验 A4 Langfuse trace · GENERATION `input` 序列化 `store` · 含 Supabase `service_role` JWT
> **父任务**：P2-5b [`task_ops_desk_p2_langfuse_eval_v1.md`](../done/task_ops_desk_p2_langfuse_eval_v1.md)（human CLOSE pass）
> **关联**：P2-5a-ext-2 hotfix 曾将「Langfuse input 脱敏」列为**非范围** · 本 task 单独立项

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-langfuse-trace-redact` |
| **priority** | **P0** · 密钥已进 Cloud trace 时须先轮换 key 再开 trace |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-LANGFUSE-TRACE-REDACT` |
| **orchestration** | 00 @ `Projects/` · **单泳道** `ai-ink-brain-api-python/` |
| **git_branch** | `fix/ops-desk-p2-langfuse-trace-redact` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **human_gate** | 开 `LANGFUSE_TRACING=true` 跑 A4 · Cloud GENERATION input **无** JWT / `supabase_key` |

---

## 背景与目标

`@traceable` / Langfuse `@observe` 默认采集函数入参。`chat_completion(..., kwargs={step, run_id, store})` 将完整 `OpsStore`（含 Supabase client、`service_role`）写入 GENERATION `input`。

**完成态**

- [x] `chat_completion` / 其他 `@traceable` deep 路径：**不上报** `store` 或等价脱敏
- [x] 保留可调试字段：`messages`（或摘要）、`step`、`run_id`、`ops_run_id`（metadata）
- [x] pytest：断言 trace 调用参数 / mock observe 不含 `supabase_key` / `Bearer`
- [x] 文档：`LANGFUSE_QUICKSTART_zh.md` 或 `tracing.py` 模块注释一行纪律
- [ ] 维护者：**轮换**已泄露的 Supabase `service_role`（本 task 不代操作）

---

## 范围 / 非范围

| 范围 | 非范围 |
| --- | --- |
| `api/ops/tracing.py` · `capture_input` 策略 | Langfuse Dataset 导入（另 optional follow-up） |
| `api/ops/llm.py` 或 orchestrator 上 `@traceable` 签名 | 删 Langfuse 历史 trace（管理台手工可选） |
| `tests/ops_desk/test_*tracing*` 或扩展现有 llm 测试 | 改 Demo D1–D4 语义 |
| Harness task + invoke 指针 | 前端 / BFF |

---

## 实现方案

**方案 A（已落地）**

`api/ops/llm/__init__.py:69` 的 `chat_completion` 装饰器改为：

```python
@traceable(run_type="llm", capture_input=False)
def chat_completion(..., store: Any = None, ...) -> LlmCompletionResult:
    ...
```

- `capture_input=False` 阻止 `store` / `messages` 被 `@observe` 序列化写入 GENERATION `input`。
- 函数内部仍正常接收 `store`，`_write_usage_event` / `append_event` 双写不变。
- 其余三处 `@traceable`（`issue_analyst.py:32`、`orchestrator/core.py:100`、`orchestrator/core.py:145`）已带 `capture_input=False, capture_output=False`，**未改动**。

---

## 验收标准

- [x] `pytest tests/ops_desk/ -q` 绿
- [x] 新增或扩展测试：mock `observe` / patch tracing · input 无密钥模式
- [ ] 人验：A4 deep 一条 trace · GENERATION input 可展开检查 · **无** `eyJ` JWT · **无** `service_role`
- [x] `ops_run_events` / 内部 `llm.usage` **不变**（仅 Langfuse 观测面）

---

## 失败路径

| 触发 | 行为 |
| --- | --- |
| `LANGFUSE_TRACING=false` | no-op · 与现网一致 |
| observe 抛错 | 不阻塞 chat 主路径（保持现有静默/降级纪律） |

---

## 运维 · 密钥轮换（维护者 · 与代码 PR 并行）

| 步骤 | 动作 |
| --- | --- |
| 1 | Supabase Dashboard → Settings → API → **Rotate service_role key** |
| 2 | 更新本机 / 部署环境 `.env` 中 `SUPABASE_SERVICE_ROLE_KEY`（或项目等价变量名） |
| 3 | 可选：Langfuse Cloud 删除含泄露内容的 A4 trace（**不能**替代轮换） |
| 4 | 脱敏 PR merge 后，再对共享 Project 开 `LANGFUSE_TRACING=true` |

> **仅废弃/轮换 key 不够**：未改代码前，新 trace 仍会再次泄露新 key。

---

## 依赖与引用

| 项 | 路径 |
| --- | --- |
| tracing shim | `ai-ink-brain-api-python/api/ops/tracing.py` |
| GUIDE Phase A | [`GUIDE_ops_desk_langfuse_eval_v1_zh.md`](../../guides/GUIDE_ops_desk_langfuse_eval_v1_zh.md) §1 |
| P2-5b CLOSE | [`task_ops_desk_p2_langfuse_eval_CLOSE_R1_20260625.md`](../../reviews/task_ops_desk_p2_langfuse_eval_CLOSE_R1_20260625.md) |
| 前人验证据 | A4 run `4d4662ff-1b1e-4035-a25a-58cf08beca48` |

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-25 | v1 · P0 hotfix 草案 · P2-5b 人验 follow-up |
| 2026-06-25 | v2 · 方案 A 落地 · 新增 `test_tracing_redact.py` · 文档补充 §5.1 安全纪律 |
