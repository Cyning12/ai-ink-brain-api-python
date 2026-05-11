# 阶段 B · 前端验收留档（Unified Chat 导出）

## 此次验收结果（2026-05-11）

| 项 | 结论 |
|----|------|
| **留证类型** | Ink **Unified Chat** 导出 **Timeline（JSON）** + **执行链路**（RUNBOOK **§3.6 / C** 口径） |
| **业务路径** | `prefer=auto` → `text2sql`；`tool.call.end` / `sql.result` / 答复一致，**12 条** |
| **`meta.payload.run_id`（R，服务端 canonical）** | `34c3c7ef-bff6-4a38-beea-5912b4ae1ace` |
| **`user.message` 及后续链事件顶层 `run_id`（文首至 `latency`）** | `9c17c696-95ae-411e-b954-360ca5b70c38` |
| **与 [`阶段B-验收-1.md`](阶段B-验收-1.md) 目标** | **未对齐**：文首 **R** 与 **顶层 `run_id`** **不一致**；验收-1 要求 **`meta` 到达后回填**，**全表与 `payload.run_id` 同源**（可与该文件内样例对照）。**建议**：确认已部署含 **`UnifiedChatPageClient.tsx`** `meta` **`payload.run_id` 回填** 的构建；若为 **增量 SSE** 路径，核对是否遗漏同一逻辑后 **重新导出** 再签收 **C**。 |
| **与 B（stderr）对读** | [`阶段B-留证-curl-stream-b-smoke-2026-05-11.md`](阶段B-留证-curl-stream-b-smoke-2026-05-11.md) 中 `554e5b2f-…` 等为 **另一次 curl/tee 会话**，UUID **不必**与本导出相同；若要做 **同一会话** C+B 对读，须以 **当轮 SSE** 的 **`meta.payload.run_id`** 去 grep `text2sql_tool_call_end`。 |

---

## 原始导出（应用内复制，结构未改）

=== Timeline（共 23 条，JSON）===
[
  {
    "type": "user.message",
    "ts": 1778489721976,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "user",
    "payload": {
      "text": "统计 agent_info 表里有多少条数据"
    }
  },
  {
    "type": "meta",
    "ts": 0,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "m1",
    "payload": {
      "run_id": "34c3c7ef-bff6-4a38-beea-5912b4ae1ace",
      "mode": "auto",
      "session_id": "11b42400-5117-49a7-ac3d-e90d7c25a9bd"
    }
  },
  {
    "type": "agent.step.start",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "a1",
    "payload": {
      "step_number": 1,
      "max_steps": 5
    }
  },
  {
    "type": "agent.llm.start",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_intent",
    "payload": {
      "phase": "intent",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_intent",
    "payload": {
      "text": "用户要求统计 agent_inf",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_intent",
    "payload": {
      "text": "o 表的数据条数，属于结构化数据",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_intent",
    "payload": {
      "text": "查询，需要执行数据库查询获取结果",
      "part_index": 2
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_intent",
    "payload": {
      "text": "。",
      "part_index": 3
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_intent",
    "payload": {
      "ok": true,
      "phase": "intent",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "agent.intent",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "intent_1",
    "payload": {
      "tool": "text2sql_query",
      "mode": "text2sql",
      "reasoning": "用户要求统计 agent_info 表的数据条数，属于结构化数据查询，需要执行数据库查询获取结果。",
      "confidence": 0.95,
      "fallback": null,
      "cache": "miss",
      "cache_key_hash": "be4e0213aca3da8d",
      "latency_ms": 2323
    }
  },
  {
    "type": "router.decision",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "r1",
    "payload": {
      "prefer": "auto",
      "candidate_mode": "text2sql",
      "final_mode": "text2sql",
      "rule_hits": [],
      "evidence": {
        "agent_reasoning": "用户要求统计 agent_info 表的数据条数，属于结构化数据查询，需要执行数据库查询获取结果。"
      },
      "fallback": null
    }
  },
  {
    "type": "agent.think",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "a1_think",
    "payload": {
      "step_number": 1,
      "thought": "用户要求统计 agent_info 表的数据条数，属于结构化数据查询，需要执行数据库查询获取结果。",
      "selected_tool": "text2sql_query",
      "mode": "text2sql",
      "confidence": 0.95
    }
  },
  {
    "type": "tool.call.start",
    "ts": 3526,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "t_step1",
    "payload": {
      "tool": "text2sql_query",
      "input": {
        "query": "统计 agent_info 表里有多少条数据"
      }
    }
  },
  {
    "type": "tool.call.end",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "t_step1",
    "payload": {
      "output": {
        "answer": "agent_info 表中共有 12 条数据。"
      },
      "error": null,
      "latency_ms": 45432
    }
  },
  {
    "type": "sql.result",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "q_step1",
    "payload": {
      "sql": "select count(*) as total_count from agent_info",
      "columns": [
        "total_count"
      ],
      "rows": [
        {
          "total_count": 12
        }
      ],
      "truncated": false
    }
  },
  {
    "type": "agent.llm.start",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_text2sql_summary",
    "payload": {
      "phase": "text2sql_summary",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_text2sql_summary",
    "payload": {
      "text": "agent_info 表中共有 ",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_text2sql_summary",
    "payload": {
      "text": "12 条数据。",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "34c3c7efbff6_s1_text2sql_summary",
    "payload": {
      "ok": true,
      "phase": "text2sql_summary",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "agent.step.end",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "a1_end",
    "payload": {
      "step_number": 1,
      "tool_used": "text2sql_query",
      "mode": "text2sql",
      "success": true,
      "next_action": "final_answer"
    }
  },
  {
    "type": "agent.final",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "a_final",
    "payload": {
      "total_steps": 1,
      "tools_used": [
        "text2sql_query"
      ],
      "modes": [
        "text2sql"
      ],
      "fallback_used": false
    }
  },
  {
    "type": "assistant.message",
    "ts": 48958,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "s_answer",
    "payload": {
      "role": "assistant",
      "content": "agent_info 表中共有 12 条数据。"
    }
  },
  {
    "type": "latency",
    "ts": 48959,
    "run_id": "9c17c696-95ae-411e-b954-360ca5b70c38",
    "step_id": "l1",
    "payload": {
      "total_ms": 48959,
      "stages_ms": {}
    }
  }
]
=== 执行链路 ===

Query:
统计 agent_info 表里有多少条数据

--- step-1 ---
agent.llm.start · intent（使用 LLM 意图识别）
用户要求统计 agent_info 表的数据条数，属于结构化数据查询，需要执行数据库查询获取结果。
agent.llm.end · intent · ok

--- step-2 ---
agent.intent · text2sql_query · mode text2sql

--- step-3 ---
router.decision → text2sql

--- step-4 ---
agent.think
用户要求统计 agent_info 表的数据条数，属于结构化数据查询，需要执行数据库查询获取结果。
tool text2sql_query · mode text2sql

--- step-5 ---
tool.call.start · text2sql_query

--- step-6 ---
tool.call.end · text2sql_query
45432 ms
（无 error 字段）
output 摘要:
agent_info 表中共有 12 条数据。

--- step-7 ---
agent.llm.start · text2sql_summary（Text2SQL 总结）
agent_info 表中共有 12 条数据。
agent.llm.end · text2sql_summary · ok
