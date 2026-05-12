=== Timeline（共 32 条，JSON）===
[
  {
    "type": "user.message",
    "ts": 1778485469518,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "user",
    "payload": {
      "text": "统计 agent_info 表里有多少条数据"
    }
  },
  {
    "type": "meta",
    "ts": 3,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "m1",
    "payload": {
      "run_id": "4a68e80b-412e-4bb4-9a31-b108e9e57826",
      "mode": "auto",
      "session_id": "a94214a5-dd77-4356-ae58-9cdbede186b2"
    }
  },
  {
    "type": "agent.step.start",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "a1",
    "payload": {
      "step_number": 1,
      "max_steps": 5
    }
  },
  {
    "type": "agent.llm.start",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_intent",
    "payload": {
      "phase": "intent",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_intent",
    "payload": {
      "text": "用户要求统计 agent_inf",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_intent",
    "payload": {
      "text": "o 表的数据条数，属于结构化数据",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_intent",
    "payload": {
      "text": "查询，应由数据库执行 count",
      "part_index": 2
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_intent",
    "payload": {
      "text": " 操作。",
      "part_index": 3
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_intent",
    "payload": {
      "ok": true,
      "phase": "intent",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "router.decision",
    "ts": 23983,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "r1",
    "payload": {
      "prefer": "auto",
      "candidate_mode": "text2sql",
      "final_mode": "text2sql",
      "rule_hits": [],
      "evidence": {
        "agent_reasoning": "用户要求统计 agent_info 表的数据条数，属于结构化数据查询，应由数据库执行 count 操作。"
      },
      "fallback": null
    }
  },
  {
    "type": "agent.think",
    "ts": 24636,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "a1_think",
    "payload": {
      "step_number": 1,
      "thought": "Agent 超时，降级到 V1 规则路由。",
      "selected_tool": "text2sql_query",
      "mode": "text2sql",
      "confidence": 0.95
    }
  },
  {
    "type": "tool.call.start",
    "ts": 24636,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "t_step1",
    "payload": {
      "tool": "text2sql_query",
      "input": {
        "query": "统计 agent_info 表里有多少条数据"
      }
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 24636,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.retrieve",
    "payload": {
      "subphase_id": "text2sql.phase.retrieve",
      "phase_id": "retrieve",
      "phase_kind": "io"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 28400,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.retrieve",
    "payload": {
      "subphase_id": "text2sql.phase.retrieve",
      "phase_id": "retrieve",
      "latency_ms": 3763
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 28400,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.llm_sql",
    "payload": {
      "subphase_id": "text2sql.phase.llm_sql",
      "phase_id": "llm_sql",
      "phase_kind": "llm"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 31733,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.llm_sql",
    "payload": {
      "subphase_id": "text2sql.phase.llm_sql",
      "phase_id": "llm_sql",
      "latency_ms": 3332
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 31733,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.validate",
    "payload": {
      "subphase_id": "text2sql.phase.validate",
      "phase_id": "validate",
      "phase_kind": "io"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 31733,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.validate",
    "payload": {
      "subphase_id": "text2sql.phase.validate",
      "phase_id": "validate",
      "latency_ms": 0
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 31733,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.db",
    "payload": {
      "subphase_id": "text2sql.phase.db",
      "phase_id": "db",
      "phase_kind": "db"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 41532,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.db",
    "payload": {
      "subphase_id": "text2sql.phase.db",
      "phase_id": "db",
      "latency_ms": 9798
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 41532,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.llm_summary",
    "payload": {
      "subphase_id": "text2sql.phase.llm_summary",
      "phase_id": "llm_summary",
      "phase_kind": "llm"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "text2sql.phase.llm_summary",
    "payload": {
      "subphase_id": "text2sql.phase.llm_summary",
      "phase_id": "llm_summary",
      "latency_ms": 51744
    }
  },
  {
    "type": "tool.call.end",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "t_step1",
    "payload": {
      "output": {
        "answer": "agent_info 表中共有 12 条数据。",
        "text2sql_phases_ms": {
          "retrieve": 3763,
          "llm_sql": 3332,
          "validate": 0,
          "db": 9798,
          "llm_summary": 51744
        }
      },
      "error": null,
      "latency_ms": 68639
    }
  },
  {
    "type": "sql.result",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
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
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_text2sql_summary",
    "payload": {
      "phase": "text2sql_summary",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_text2sql_summary",
    "payload": {
      "text": "agent_info 表中共有 ",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_text2sql_summary",
    "payload": {
      "text": "12 条数据。",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "4a68e80b412e_s1_text2sql_summary",
    "payload": {
      "ok": true,
      "phase": "text2sql_summary",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "agent.step.end",
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
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
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
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
    "ts": 93276,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "s_answer",
    "payload": {
      "role": "assistant",
      "content": "agent_info 表中共有 12 条数据。"
    }
  },
  {
    "type": "latency",
    "ts": 93278,
    "run_id": "7aedf681-149d-4b73-b618-78391ac30332",
    "step_id": "l1",
    "payload": {
      "total_ms": 93278,
      "stages_ms": {}
    }
  }
]

=== 执行链路 ===

Query:
统计 agent_info 表里有多少条数据

--- step-1 ---
agent.llm.start · intent（使用 LLM 意图识别）
用户要求统计 agent_info 表的数据条数，属于结构化数据查询，应由数据库执行 count 操作。
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
text2sql.phase.start · retrieve · kind=io

--- step-7 ---
text2sql.phase.end · retrieve · 3763 ms

--- step-8 ---
text2sql.phase.start · llm_sql · kind=llm

--- step-9 ---
text2sql.phase.end · llm_sql · 3332 ms

--- step-10 ---
text2sql.phase.start · validate · kind=io

--- step-11 ---
text2sql.phase.end · validate · 0 ms

--- step-12 ---
text2sql.phase.start · db · kind=db

--- step-13 ---
text2sql.phase.end · db · 9798 ms

--- step-14 ---
text2sql.phase.start · llm_summary · kind=llm

--- step-15 ---
text2sql.phase.end · llm_summary · 51744 ms

--- step-16 ---
tool.call.end · text2sql_query
68639 ms
（无 error 字段）
Text2SQL 分段耗时（终态 text2sql_phases_ms）:
{
  "retrieve": 3763,
  "llm_sql": 3332,
  "validate": 0,
  "db": 9798,
  "llm_summary": 51744
}
output 摘要:
agent_info 表中共有 12 条数据。

--- step-17 ---
agent.llm.start · text2sql_summary（Text2SQL 总结）
agent_info 表中共有 12 条数据。
agent.llm.end · text2sql_summary · ok
