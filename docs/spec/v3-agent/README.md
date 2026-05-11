# ChatBI V3 —— SPEC 目录

> **状态**：**初版**（2026-05-11）；子主题随任务落地可拆独立子规。  
> **总规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md)  
> **企业级差距表**（P0/P1 优先级语汇）：[`../SPEC-ChatBI-Enterprise-Gap.md`](../SPEC-ChatBI-Enterprise-Gap.md) **§4.2**  
> **V2 冻结参考**：[`../v2-agent/README.md`](../v2-agent/README.md)

---

## 目录结构（当前）

```
docs/spec/v3-agent/
├── README.md                      # 本文件
└── SPEC-ChatBI-V3-Overview.md     # V3 总览：目标、范围、任务归拢、与 V2/vNext 关系
```

---

## `docs/tasks/active` 中已归拢的 V3 任务

| 任务文件 | 角色 |
|----------|------|
| `task_chatbi_v3_planning_after_resume_v1.md` | 规划入口、迭代顺序 |
| `task_chatbi_v3_text2sql_tool_latency_obs_v1.md` | Text2SQL 工具链延迟与可观测 |
| `task_chatbi_v3_debt_from_v2_multiturn_v1.md` | V2 多轮 / 值域相关技术债 |

新增 V3 子任务时：**在本 README 上表追加一行**，并在 `SPEC-ChatBI-V3-Overview.md` **§3** 同步。

---

## 给 Cursor

`SPEC-ChatBI-V3-Overview`、`v3-agent`、`Enterprise Gap` §4.2、`task_chatbi_v3_*`
