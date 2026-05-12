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
├── SPEC-ChatBI-V3-Evaluation.md                  # L1 评估 · 回归
└── text2sql/                                     # 场景留档（迭代稿 + 归档）
    ├── archive/README.md                         # 无权限等归档索引（验收真值见该目录）
    └── …                                         # 见目录内文件
```

---

## 阅读顺序（建议）

1. [`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§0、§2.1**（批次与支柱）  
2. 仅做 Text2SQL 可观测：**Observability-Text2SQL** → **Logging-Trace**  
3. 仅做多轮欠债：**Multiturn-Debt**（并与 V2 Multiturn SPEC 对照）  
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

新增 V3 任务时：**更新本 README 上表** + `SPEC-ChatBI-V3-Overview.md` **§3**；若新域无 L1 文件，**先补子规再挂任务**。

**Text2SQL 无权限场景（已验收）**：留档与真值索引见 [`text2sql/archive/README.md`](text2sql/archive/README.md)。

---

## 给 Cursor

`SPEC-ChatBI-V3-Overview`、`SPEC-ChatBI-V3-Observability-Text2SQL`、`SPEC-ChatBI-V3-Logging-Trace`、`SPEC-ChatBI-V3-Security`、`SPEC-ChatBI-V3-Identity-Access`、`SPEC-ChatBI-V3-Resilience-Ops`、`SPEC-ChatBI-V3-Multiturn-Debt`、`SPEC-ChatBI-V3-Evaluation`、`v3-agent`、`Enterprise Gap` §4.2、`task_chatbi_v3_*`
