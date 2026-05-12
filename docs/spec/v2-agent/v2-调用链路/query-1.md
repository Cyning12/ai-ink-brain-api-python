=== Timeline（共 20 条，JSON）===
[
  {
    "type": "user.message",
    "ts": 1778469373168,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "user",
    "payload": {
      "text": "统计 agent_info 表里有多少条数据"
    }
  },
  {
    "type": "meta",
    "ts": 3,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "m1",
    "payload": {
      "run_id": "4359402b-a2ef-4418-a2c0-64db7a21d89a",
      "mode": "auto",
      "session_id": "f6ad3b47-c6ab-418d-9291-6a70dc09c11d"
    }
  },
  {
    "type": "agent.step.start",
    "ts": 61017,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "a1",
    "payload": {
      "step_number": 1,
      "max_steps": 5
    }
  },
  {
    "type": "agent.llm.start",
    "ts": 61017,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_intent",
    "payload": {
      "phase": "intent",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 61017,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_intent",
    "payload": {
      "text": "意图识别超时，降级到 V1 规则",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 61017,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_intent",
    "payload": {
      "text": "路由。",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 61017,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_intent",
    "payload": {
      "ok": true,
      "phase": "intent",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "router.decision",
    "ts": 61017,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "r1",
    "payload": {
      "prefer": "auto",
      "candidate_mode": "text2sql",
      "final_mode": "text2sql",
      "rule_hits": [],
      "evidence": {
        "agent_reasoning": "意图识别超时，降级到 V1 规则路由。"
      },
      "fallback": null
    }
  },
  {
    "type": "agent.think",
    "ts": 61541,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "a1_think",
    "payload": {
      "step_number": 1,
      "thought": "Agent 超时，降级到 V1 规则路由。",
      "selected_tool": "text2sql_query",
      "mode": "text2sql",
      "confidence": 0.6
    }
  },
  {
    "type": "tool.call.start",
    "ts": 61541,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
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
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "t_step1",
    "payload": {
      "output": {
        "answer": "agent_info 表中共有 12 条数据。"
      },
      "error": null,
      "latency_ms": 505667
    }
  },
  {
    "type": "sql.result",
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "q_step1",
    "payload": {
      "sql": "select count(*) as total_count\nfrom agent_info",
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
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_text2sql_summary",
    "payload": {
      "phase": "text2sql_summary",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_text2sql_summary",
    "payload": {
      "text": "agent_info 表中共有 ",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_text2sql_summary",
    "payload": {
      "text": "12 条数据。",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "4359402ba2ef_s1_text2sql_summary",
    "payload": {
      "ok": true,
      "phase": "text2sql_summary",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "agent.step.end",
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
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
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
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
    "ts": 567208,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "s_answer",
    "payload": {
      "role": "assistant",
      "content": "agent_info 表中共有 12 条数据。"
    }
  },
  {
    "type": "latency",
    "ts": 567214,
    "run_id": "e736b90b-6652-4faf-87ee-cb4571b6f019",
    "step_id": "l1",
    "payload": {
      "total_ms": 567214,
      "stages_ms": {}
    }
  }
]

=== 执行链路 ===

Query:
统计 agent_info 表里有多少条数据

--- step-1 ---
agent.llm.start · intent（使用 LLM 意图识别）
意图识别超时，降级到 V1 规则路由。
agent.llm.end · intent · ok

--- step-2 ---
agent.intent · text2sql_query · mode text2sql

--- step-3 ---
router.decision → text2sql

--- step-4 ---
agent.think
Agent 超时，降级到 V1 规则路由。
tool text2sql_query · mode text2sql

--- step-5 ---
tool.call.start · text2sql_query

--- step-6 ---
tool.call.end · text2sql_query
505667 ms
（无 error 字段）
output 摘要:
agent_info 表中共有 12 条数据。

--- step-7 ---
agent.llm.start · text2sql_summary（Text2SQL 总结）
agent_info 表中共有 12 条数据。
agent.llm.end · text2sql_summary · ok

=== 历史消息 ===
历史消息
已完成轮次摘要（来自 rag_conversation_logs）；当前轮 Timeline 与下方「消息」区仅展示本轮
user
统计 agent_info 表里有多少条数据
assistant
agent_info 表中共有 12 条数据。