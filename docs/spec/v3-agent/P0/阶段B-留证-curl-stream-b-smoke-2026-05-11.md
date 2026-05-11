# 阶段 B 手工留证 — curl SSE（`b-smoke`）

> **用途**：**RUNBOOK §3.4**「带鉴权 stream + 取 `run_id`」的 **SSE 原文落盘**；与 **`text2sql_tool_call_end`** 的 stderr 对读仍须在 **API 进程侧** grep（本节 **§stderr 对齐** 可补贴脱敏 JSON 一行）。  
> **关联**：[`阶段B-验收-1.md`](阶段B-验收-1.md)（R / `meta` / `done` 口径）、[`../../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](../../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) **§3.4**

---

## 元信息

| 项 | 值 |
|----|-----|
| **日期** | 2026-05-11 |
| **端点** | `POST http://127.0.0.1:8000/api/py/unified/chat/stream` |
| **鉴权** | `Authorization: Bearer` 已脱敏为 **`XXXX`**（真值仅本地 `.env`） |
| **`run_id`（`meta` / `done` 同源）** | `0e1ba483-72e3-45b9-9a69-43538c9055a6` |
| **`request_id`（`done`）** | 与上相同（v1 策略） |
| **`session_id`** | `b-smoke` |
| **`prefer`** | `text2sql` |
| **业务结果摘要** | `tool.call.end` → 回答「共有 12 条。」；`sql.result` → `select count(*) from agent_info`，`count`: 12 |

---

## 命令（Bearer 脱敏）

```bash
curl -sS -N --max-time 300 -H "Authorization: Bearer XXXX" -H "Content-Type: application/json" \
  -d '{"query":"agent_info 表有多少行","session_id":"b-smoke","prefer":"text2sql"}' \
  http://127.0.0.1:8000/api/py/unified/chat/stream
```

---

## stderr JSON 对齐（执行人可补）

在同一次请求、**`CHATBI_JSON_LOG=true`** 的前提下，于 **运行 FastAPI/uvicorn 的进程** 的 **stderr** 或其 **tee 出来的日志文件** 里 grep。

**勿对本 Markdown 文件 grep**：本文表格与下文 SSE 摘录里 **写死了同一 `run_id`**，对 `阶段B-留证-curl-stream-b-smoke-2026-05-11.md` 执行 `grep` 只会命中这些字面量，**不会出现** `"message":"text2sql_tool_call_end"` 的 **服务端 JSON 行**（与终端里你看到的「grep md 只有 meta/done」现象一致）。

```bash
# 占位符须换成真实路径：例如启动 API 时 `2>&1 | tee /tmp/chatbi-api.log`
grep '0e1ba483-72e3-45b9-9a69-43538c9055a6' /tmp/chatbi-api.log | grep text2sql_tool_call_end
```

将 **脱敏后** 的匹配行（单行 JSON）粘贴至本节下方即可与 RUNBOOK **B3** 闭环。

### B3 闭环节录（tee：`/tmp/chatbi-api.log`）

> 与 **§元信息** 表内第一次 curl 摘录的 `run_id`（`0e1ba483-…`）为 **另一次请求**；下列为 **`CHATBI_JSON_LOG=true`** + **`2>&1 | tee /tmp/chatbi-api.log`** 后，对 **当次** SSE `meta`/`done` 同源 id 的 grep 原文。

**命令**：

```bash
grep '554e5b2f-f984-4cbd-9db8-1b3d3847dc7f' /tmp/chatbi-api.log | grep text2sql_tool_call_end
```

**匹配行（单行 JSON）**：

```json
{"timestamp": "2026-05-11T08:49:55.049085+00:00", "level": "INFO", "message": "text2sql_tool_call_end", "service": "chatbi-api", "request_id": "554e5b2f-f984-4cbd-9db8-1b3d3847dc7f", "run_id": "554e5b2f-f984-4cbd-9db8-1b3d3847dc7f", "session_id": "b-smoke", "route": "agent", "mode": "text2sql", "tool": "text2sql_query", "latency_ms": 16191, "text2sql_phases_ms": {"retrieve": 3550, "llm_sql": 11025, "validate": 0, "db": 1614}, "step_number": 1}
```

---

## SSE 原始输出

下列与执行时终端一致；其中 **`agent.debug.llm_prompts`** 内 `messages` 正文过长，留档中 **折叠为占位**，完整原文以执行人本机抄屏为准。

```text
event: chain
data: {"type":"meta","ts":3,"step_id":"m1","payload":{"run_id":"0e1ba483-72e3-45b9-9a69-43538c9055a6","mode":"text2sql","session_id":"b-smoke"}}

: sse-keepalive

event: chain
data: {"type":"router.decision","ts":26256,"step_id":"r1","payload":{"prefer":"text2sql","candidate_mode":"text2sql","final_mode":"text2sql","rule_hits":[],"evidence":{"agent_reasoning":"用户指定 prefer=text2sql，选择对应工具开始处理。"},"fallback":null}}

event: chain
data: {"type":"agent.step.start","ts":26256,"step_id":"a1","payload":{"step_number":1,"max_steps":5}}

event: chain
data: {"type":"agent.intent","ts":26256,"step_id":"intent_1","payload":{"tool":"text2sql_query","mode":"text2sql","reasoning":"用户指定 prefer=text2sql，选择对应工具开始处理。","confidence":1.0,"fallback":null,"cache":null,"cache_key_hash":null,"latency_ms":null}}

event: chain
data: {"type":"agent.think","ts":26256,"step_id":"a1_think","payload":{"step_number":1,"thought":"用户指定 prefer=text2sql，选择对应工具开始处理。","selected_tool":"text2sql_query","mode":"text2sql","confidence":1.0}}

event: chain
data: {"type":"tool.call.start","ts":26256,"step_id":"t_step1","payload":{"tool":"text2sql_query","input":{"query":"agent_info 表有多少行"}}}

event: chain
data: {"type":"tool.call.end","ts":26256,"step_id":"t_step1","payload":{"output":{"answer":"共有 12 条。"},"error":null,"latency_ms":20531}}

event: chain
data: {"type":"agent.debug.llm_prompts","ts":26256,"step_id":"tool_llm_replay_1","payload":{"scope":"tool","tool":"text2sql_query","step_number":1,"items":[{"phase":"text2sql_sql","model":"deepseek-ai/DeepSeek-V4-Flash","messages":"…[折叠：完整 messages 见执行人本机 SSE 原文；含 DDL/值域提示等]…"}]}}

event: chain
data: {"type":"sql.result","ts":26256,"step_id":"q_step1","payload":{"sql":"select count(*) from agent_info","columns":["count"],"rows":[{"count":12}],"truncated":false}}

event: chain
data: {"type":"agent.step.end","ts":26256,"step_id":"a1_end","payload":{"step_number":1,"tool_used":"text2sql_query","mode":"text2sql","success":true,"next_action":"final_answer"}}

event: chain
data: {"type":"agent.final","ts":26256,"step_id":"a_final","payload":{"total_steps":1,"tools_used":["text2sql_query"],"modes":["text2sql"],"fallback_used":false}}

event: chain
data: {"type":"assistant.message","ts":26256,"step_id":"s_answer","payload":{"role":"assistant","content":"共有 12 条。"}}

event: chain
data: {"type":"latency","ts":26256,"step_id":"l1","payload":{"total_ms":26256,"stages_ms":{}}}

event: done
data: {"ok":true,"mode":"text2sql","run_id":"0e1ba483-72e3-45b9-9a69-43538c9055a6","request_id":"0e1ba483-72e3-45b9-9a69-43538c9055a6","session_id":"b-smoke","persist":{"ok":true,"path":"full"}}
```

---

## 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版：手工 curl SSE 落盘；`agent.debug.llm_prompts` 长正文折叠 |
| 2026-05-11 | **§stderr**：注明勿 grep 本 md；示例改为具体日志路径占位 |
| 2026-05-11 | **§B3 闭环**：补 `554e5b2f-…` + `text2sql_tool_call_end` tee 留证一行（与当次 SSE `run_id` 同源） |
