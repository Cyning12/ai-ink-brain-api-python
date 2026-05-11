> **阶段 A · 中间验收（超时抽检路径留档）**  
> **环境与依赖说明**：Text2SQL 的 **`retrieve`** 阶段依赖 **Supabase / 向量检索等托管与外网链路**，网络抖动、冷启动或配额压力下 **墙时钟易明显拉长**；再叠加 **`llm_sql` 分阶段 LLM 超时（本例配置为 120s 档）** 时，**更容易出现**「检索偏慢 + SQL 生成阶段打满超时」的组合。解读下方 **`text2sql_phases_ms`** 与 step 耗时：**不宜单独归因于应用代码回归**；与成功路径留档对读见同目录 [`阶段A-中间验收.md`](阶段A-中间验收.md)。

---

=== Timeline（共 34 条，JSON）===
[
  {
    "type": "user.message",
    "ts": 1778484563336,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "user",
    "payload": {
      "text": "其中有多少男人"
    }
  },
  {
    "type": "meta",
    "ts": 0,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "m1",
    "payload": {
      "run_id": "78264245-0586-4a8b-bfcf-877076ca88e3",
      "mode": "auto",
      "session_id": "a94214a5-dd77-4356-ae58-9cdbede186b2"
    }
  },
  {
    "type": "agent.step.start",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a1",
    "payload": {
      "step_number": 1,
      "max_steps": 5
    }
  },
  {
    "type": "agent.llm.start",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s1_intent",
    "payload": {
      "phase": "intent",
      "step_id": "s1"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s1_intent",
    "payload": {
      "text": "用户要求统计 agent_inf",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s1_intent",
    "payload": {
      "text": "o 表中男性人数，需要数据库查询",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s1_intent",
    "payload": {
      "text": "获取具体数值",
      "part_index": 2
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s1_intent",
    "payload": {
      "ok": true,
      "phase": "intent",
      "step_id": "s1",
      "simulated_stream": true
    }
  },
  {
    "type": "router.decision",
    "ts": 1793,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "r1",
    "payload": {
      "prefer": "auto",
      "candidate_mode": "text2sql",
      "final_mode": "text2sql",
      "rule_hits": [],
      "evidence": {
        "agent_reasoning": "用户要求统计 agent_info 表中男性人数，需要数据库查询获取具体数值"
      },
      "fallback": null
    }
  },
  {
    "type": "agent.think",
    "ts": 1794,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a1_think",
    "payload": {
      "step_number": 1,
      "thought": "用户要求统计 agent_info 表中男性人数，需要数据库查询获取具体数值",
      "selected_tool": "text2sql_query",
      "mode": "text2sql",
      "confidence": 0.95
    }
  },
  {
    "type": "tool.call.start",
    "ts": 1794,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "t_step1",
    "payload": {
      "tool": "text2sql_query",
      "input": {
        "query": "其中有多少男人"
      }
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 1794,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "text2sql.phase.retrieve",
    "payload": {
      "subphase_id": "text2sql.phase.retrieve",
      "phase_id": "retrieve",
      "phase_kind": "io"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 24434,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "text2sql.phase.retrieve",
    "payload": {
      "subphase_id": "text2sql.phase.retrieve",
      "phase_id": "retrieve",
      "latency_ms": 22640
    }
  },
  {
    "type": "text2sql.phase.start",
    "ts": 24434,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "text2sql.phase.llm_sql",
    "payload": {
      "subphase_id": "text2sql.phase.llm_sql",
      "phase_id": "llm_sql",
      "phase_kind": "llm"
    }
  },
  {
    "type": "text2sql.phase.end",
    "ts": 144435,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "text2sql.phase.llm_sql",
    "payload": {
      "subphase_id": "text2sql.phase.llm_sql",
      "phase_id": "llm_sql",
      "latency_ms": 120000
    }
  },
  {
    "type": "tool.call.end",
    "ts": 144435,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "t_step1",
    "payload": {
      "output": {
        "text2sql_phases_ms": {
          "retrieve": 22640,
          "llm_sql": 120000
        }
      },
      "error": "Text2SQL SQL 生成 LLM 超时",
      "latency_ms": 142641
    }
  },
  {
    "type": "agent.step.end",
    "ts": 145167,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a1_end",
    "payload": {
      "step_number": 1,
      "tool_used": "text2sql_query",
      "mode": "text2sql",
      "success": false,
      "next_action": "continue"
    }
  },
  {
    "type": "agent.step.start",
    "ts": 145167,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a2",
    "payload": {
      "step_number": 2,
      "max_steps": 5
    }
  },
  {
    "type": "agent.think",
    "ts": 145167,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a2_think",
    "payload": {
      "step_number": 2,
      "thought": "意图/模型调用超时，降级到 V1 规则路由。（code=LLM_API_TIMEOUT stage=text2sql.generate msg=Text2SQL SQL 生成 LLM 超时）",
      "selected_tool": "direct_answer",
      "mode": "no_data",
      "confidence": 1
    }
  },
  {
    "type": "tool.call.start",
    "ts": 145167,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "t_step2",
    "payload": {
      "tool": "direct_answer",
      "input": {
        "query": "其中有多少男人"
      }
    }
  },
  {
    "type": "tool.call.end",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "t_step2",
    "payload": {
      "output": {
        "answer": "您好！您的问题“其中有多少男人”缺少具体的上下文，我无法直接给出数字。请问您指的是某个特定群体、场景或数据吗？例如：一个班级、一场活动、一家公司，或者某个统计报告？请提供更多信息，我会尽力帮您解答。"
      },
      "error": null,
      "latency_ms": 136151
    }
  },
  {
    "type": "agent.llm.start",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "phase": "direct",
      "step_id": "s2"
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "您好！您的问题“其中有多少男人”",
      "part_index": 0
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "缺少具体的上下文，我无法直接给出",
      "part_index": 1
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "数字。请问您指的是某个特定群体、",
      "part_index": 2
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "场景或数据吗？例如：一个班级、一",
      "part_index": 3
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "场活动、一家公司，或者某个统计报",
      "part_index": 4
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "告？请提供更多信息，我会尽力帮您",
      "part_index": 5
    }
  },
  {
    "type": "agent.llm.delta",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "text": "解答。",
      "part_index": 6
    }
  },
  {
    "type": "agent.llm.end",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "782642450586_s2_direct",
    "payload": {
      "ok": true,
      "phase": "direct",
      "step_id": "s2",
      "simulated_stream": true
    }
  },
  {
    "type": "agent.step.end",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a2_end",
    "payload": {
      "step_number": 2,
      "tool_used": "direct_answer",
      "mode": "no_data",
      "success": true,
      "next_action": "final_answer"
    }
  },
  {
    "type": "agent.final",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "a_final",
    "payload": {
      "total_steps": 2,
      "tools_used": [
        "text2sql_query",
        "direct_answer"
      ],
      "modes": [
        "text2sql",
        "no_data"
      ],
      "fallback_used": true
    }
  },
  {
    "type": "assistant.message",
    "ts": 281318,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "s_answer",
    "payload": {
      "role": "assistant",
      "content": "您好！您的问题“其中有多少男人”缺少具体的上下文，我无法直接给出数字。请问您指的是某个特定群体、场景或数据吗？例如：一个班级、一场活动、一家公司，或者某个统计报告？请提供更多信息，我会尽力帮您解答。"
    }
  },
  {
    "type": "latency",
    "ts": 281324,
    "run_id": "3556138d-424c-43a2-b735-aefb5ea15be5",
    "step_id": "l1",
    "payload": {
      "total_ms": 281324,
      "stages_ms": {}
    }
  }
]
=== 执行链路 ===

Query:
其中有多少男人

--- step-1 ---
agent.llm.start · intent（使用 LLM 意图识别）
用户要求统计 agent_info 表中男性人数，需要数据库查询获取具体数值
agent.llm.end · intent · ok

--- step-2 ---
agent.intent · text2sql_query · mode text2sql

--- step-3 ---
router.decision → text2sql

--- step-4 ---
agent.think
用户要求统计 agent_info 表中男性人数，需要数据库查询获取具体数值
tool text2sql_query · mode text2sql

--- step-5 ---
tool.call.start · text2sql_query

--- step-6 ---
text2sql.phase.start · retrieve · kind=io

--- step-7 ---
text2sql.phase.end · retrieve · 22640 ms

--- step-8 ---
text2sql.phase.start · llm_sql · kind=llm

--- step-9 ---
text2sql.phase.end · llm_sql · 120000 ms

--- step-10 ---
tool.call.end · text2sql_query
142641 ms
工具 error: Text2SQL SQL 生成 LLM 超时
Text2SQL 分段耗时（终态 text2sql_phases_ms）:
{
  "retrieve": 22640,
  "llm_sql": 120000
}
（无 output 摘要）

--- step-11 ---
agent.think
意图/模型调用超时，降级到 V1 规则路由。（code=LLM_API_TIMEOUT stage=text2sql.generate msg=Text2SQL SQL 生成 LLM 超时）
tool direct_answer · mode no_data

--- step-12 ---
tool.call.start · direct_answer

--- step-13 ---
tool.call.end · direct_answer
136151 ms
（无 error 字段）
output 摘要:
您好！您的问题“其中有多少男人”缺少具体的上下文，我无法直接给出数字。请问您指的是某个特定群体、场景或数据吗？例如：一个班级、一场活动、一家公司，或者某个统计报告？请提供更多信息，我会尽力帮您解答。

--- step-14 ---
agent.llm.start · direct（直接生成）
您好！您的问题“其中有多少男人”缺少具体的上下文，我无法直接给出数字。请问您指的是某个特定群体、场景或数据吗？例如：一个班级、一场活动、一家公司，或者某个统计报告？请提供更多信息，我会尽力帮您解答。
agent.llm.end · direct · ok
