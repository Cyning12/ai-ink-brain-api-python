# Invoke · 10 需求帽 · chatbi_graph_p0_foundation_v1 · 2026-06-03

| 字段 | 值 |
| --- | --- |
| **hat_code** | 10 |
| **task_slug** | `chatbi_graph_p0_foundation_v1` |
| **git_branch** | `task/chatbi-graph-p0-foundation-v1` |
| **semi_auto** | `true` |
| **test_strategy** | `required` |
| **SDD 状态** | 轮 0+1 骨架完成，待轮 2 |
| **NEW_OR_MAJOR_SPEC** | 否 |
| **audit_review** | 无 |
| **交付** | `docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` 草案 |

## §3 快照（开帽 Prompt 全文）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md（SDD 三轮 · §4 待确认清单 · §5 完成后下一棒）

输入（占位符已替换）：

【目标与上下文】
为 ChatBI 自研 StateGraph 编排开 **P0 单 Loop 单 task**（Task-P0）：在一个 PR 内完成共享层抽取 + Graph 骨架路由，**不**做 P1 完整 Agent parity。

完成态（一句话）：旧 Unified/Agent 行为不变的前提下，抽出 chatbi_events/models/failure、落地 ChatBIState 与边表草案、注册 `/api/py/unified/chat/graph(.stream)` 骨架路由（stub 可调用），pytest 必绿集全绿。

约束（已冻结，勿再辩论）：
- D-1 自研，不引 langgraph/langchain
- D-2 新 Graph 路由并行，**不改** unified_chat.py 行为
- D-3 Graph 边表 Intent 超时走方案 A；legacy FailureTypeHandler 保留 v1 fallback
- D-4 前端 **否**；后端 Graph 常开，入口曝光由前端后续控制
- D-5 P0 可不新增 graph.* SSE type；若新增须过 contract CI

建议 task_slug：`chatbi_graph_p0_foundation_v1`
建议 git_branch：`task/chatbi-graph-p0-foundation-v1`
Open Folder：本仓 `ai-ink-brain-api-python`

【已有材料路径或粘贴说明】
- docs/spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md（§4A P0 单 Loop · Done 清单 · §10 Task-P0）
- docs/spec/research/SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md（§4.3 D-1～D-5 已冻结）
- docs/spec/research/SPEC-Research-SelfChain-vs-LangChain-v1_zh.md（背景参考）
- docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md（§2.4 fallback 对照）
- api/agent.py（~1342 行，P0 抽模块目标）
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

【是否按任务审核文档回填】（无则写「无」）
无

【SDD 三轮状态】
轮0+1 骨架完成，待轮2

【是否新建或重大修订 SPEC】
否

你必须完成：

0. **Invoke 快照**：将本用户消息全文落盘到 `docs/harness/invokes/by-task/chatbi_graph_p0_foundation_v1/invoke_YYYYMMDD_10_requirements.md`（元数据表 + §3 快照 fenced code）。

1. **SDD 纪律**：
   - 不新建 L1 SPEC；task 引用既有 research/plan SPEC。
   - task 末附 **「SPEC 待确认清单」**（至少冻结 **Q-8 Graph 路由 path**；Q-7 Intent 超时 ok 字段 **defer 至 P1/Task-B** 须在表中写明）。
   - 待确认清零或人明示「方向对」后，再推荐下一棒。

2. **产出** `docs/tasks/active/task_chatbi_graph_p0_foundation_v1.md` 完整草案，须含：
   - Harness 元信息：`task_slug`、`semi_auto: true`、`test_strategy: required`、`git_branch`、`Open Folder`
   - 背景 / 范围 / 非范围（对齐 §4A.4）
   - 依赖链接（相对路径）
   - 验收 `- [ ]`（复制 §4A.3 Done 清单）
   - **failure_paths**（至少：旧 Agent 回归失败、contract check 失败、Graph stub 路由 4xx/5xx）
   - **gates_before_code** 与 **human_gate** 草案（HG-TASK-DRAFT pending）
   - 给 30 帽必读列表（§4A.2 五步顺序）
   - P0 单 Loop 执行顺序与 **禁止夹带 P1** 的硬约束

3. **test_strategy**：`required`；注明涉 `api/` + 新 HTTP 路由，关账前须 50。

4. 禁止：写 api/ 实现代码；改 unified_chat.py 行为；改 CI；绝对本机路径。

5. **下一棒 A/B（两条 Prompt 全文，人择一）**：
   - 本 task 为 `test_strategy: required` + 新路由 → **推荐路径 A（22 任务审核 R1）**
   - 路径 A：`TEMPLATE-task-audit-invoke.md` §3 全文（task 指向上述 active 路径）
   - 路径 B：`TEMPLATE-execute-invoke.md` §3 全文（须注明跳过 22 的风险，默认不推荐）

6. 回复末尾：**Harness 状态栏（版本 B）**（不得代填 human_gate approved）。

7. **Commit**：落盘 invoke + task 草案后，在分支 `task/chatbi-graph-p0-foundation-v1` commit（用户未说「不要 commit」则执行）。
```
