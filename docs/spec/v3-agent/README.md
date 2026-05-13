# ChatBI V3 —— SPEC 目录

> **状态**：**初版 + L1 子规**（2026-05-11）；子规为 `draft`，随首包实现收敛。  
> **总规（L0）**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) — **§0 规格层级**为权威索引  
> **企业级差距表**：[`../SPEC-ChatBI-Enterprise-Gap.md`](../SPEC-ChatBI-Enterprise-Gap.md) **§4.2**  
> **V2 冻结参考**：[`../v2-agent/README.md`](../v2-agent/README.md)

---

## 目录结构（L0 + L1）

```
docs/spec/v3-agent/
├── README.md                                    # 本文件
├── P0/                                          # 阶段 A/B 验收留档（见 P0/README.md）
│   ├── README.md
│   ├── 阶段A-中间验收.md
│   ├── 阶段A-中间验收-超时.md
│   ├── 阶段B-验收.md
│   └── 阶段B-验收-1.md
├── SPEC-ChatBI-V3-Overview.md                   # L0 总览
├── SPEC-ChatBI-V3-Observability-Text2SQL.md     # L1 可观测 · Text2SQL
├── SPEC-ChatBI-V3-Logging-Trace.md              # L1 日志 · Trace
├── SPEC-ChatBI-V3-Security.md                     # L1 安全（SQL + Prompt）
├── SPEC-ChatBI-V3-Identity-Access.md              # L1 RBAC · 数据域
├── SPEC-ChatBI-V3-Resilience-Ops.md               # L1 限流 · 熔断 · 健康检查
├── SPEC-ChatBI-V3-Multiturn-Debt.md              # L1 多轮 / 值域技术债
├── SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md # L1 低置信：方案预览 + 确认 + 编排 B（后 P1-4）
├── SPEC-ChatBI-V3-Evaluation.md                  # L1 评估 · 回归
└── text2sql/                                     # 场景留档（迭代稿 + 归档）
    ├── README.md                                 # 目录索引 + **有/无权限执行结果** 对照
    ├── archive/README.md                         # 无权限等归档索引（验收真值见该目录）
    └── …                                         # 见 `1.md` / `2.md` 等
```

---

## 阅读顺序（建议）

1. [`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§0、§2.1**（批次与支柱）  
2. 仅做 Text2SQL 可观测：**Observability-Text2SQL** → **Logging-Trace**  
3. 仅做多轮欠债：**Multiturn-Debt**（并与 V2 Multiturn SPEC 对照）→ 若做 **低置信方案预览 / 确认放行**：**LowConfidence-Plan-Confirm**  
4. 安全与权限：**Security** → **Identity-Access**  
5. 运维：**Resilience-Ops**（依赖日志可验证时与 Logging 联读）  
6. 评估：**Evaluation**

---

## `docs/tasks/active` 中已归拢的 V3 任务

| 任务文件 | 角色 | 主要 L1 子规 |
|----------|------|----------------|
| `task_chatbi_v3_planning_after_resume_v1.md` | 规划入口、迭代顺序 | Overview §2.1 |
| `task_chatbi_v3_text2sql_tool_latency_obs_v1.md`（**done · `docs/tasks/done/`**） | Text2SQL 延迟与可观测 | **Observability-Text2SQL**、Logging（协同）；执行/验收见 [`../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) |
| `task_chatbi_v3_debt_from_v2_multiturn_v1.md` | 多轮 / 值域欠债（母单） | **Multiturn-Debt** |
| `task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md` | P1-4：低置信指代澄清（§4.3 / V2 §4 第 3 点） | **Multiturn-Debt**、V2 Multiturn Semantics、**Identity-Access**（表名展示） |
| `task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md` | **P2 延伸（backlog）**：方案 B + 预览 + 用户确认 + 门控升格 | **LowConfidence-Plan-Confirm**、**Multiturn-Debt**、Security、Identity-Access |
| `task_chatbi_v3_sql_ast_text2sql_gate_v1.md` | **P1-1**：`chatbi_sql_gate` **SQL AST 硬化**、负例 pytest、`sql_gate_deny` | **Security** §2、**Logging**；前置 **P1-3 done** |
| `task_chatbi_v3_prompt_injection_guard_poc_v1.md` | **P1-2**：Prompt 注入 **PoC**（扫描、env、JSON 日志） | **Security** §3；与 **P1-1** 可并行不同文件 |
| `task_chatbi_level_gate_v1.md`（**done · `docs/tasks/done/`**） | **P1-3**：Bearer、`chatbi_access_tokens`、表策略、双闸、`CHATBI_JSON_LOG` | **Identity-Access**、**OpenItems**、**Security**；SQL `docs/text2sql/v1/sql/chatbi_0*.sql` |
| `task_chatbi_v3_intent_classification_debt_v1.md` | **backlog**：意图识别欠债（复合句、表结构 vs RAG/Text2SQL 边界）；预留 **Intent vNext** | 与 `api/intent_agent.py` 对齐；总规 **§3** 已登记 |

新增 V3 任务时：**更新本 README 上表** + `SPEC-ChatBI-V3-Overview.md` **§3**；若新域无 L1 文件，**先补子规再挂任务**。

**Text2SQL 无权限场景（已验收）**：留档与真值索引见 [`text2sql/archive/README.md`](text2sql/archive/README.md)；**有/无权限终态输出对照**见 [`text2sql/README.md`](text2sql/README.md)。

---

## 给 Cursor

`SPEC-ChatBI-V3-Overview`、`SPEC-ChatBI-V3-Observability-Text2SQL`、`SPEC-ChatBI-V3-Logging-Trace`、`SPEC-ChatBI-V3-Security`、`SPEC-ChatBI-V3-Identity-Access`、`SPEC-ChatBI-V3-Resilience-Ops`、`SPEC-ChatBI-V3-Multiturn-Debt`、`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm`、`SPEC-ChatBI-V3-Evaluation`、`v3-agent`、`Enterprise Gap` §4.2、`task_chatbi_v3_*`、`task_chatbi_v3_low_confidence_plan_preview_confirm_v1`
