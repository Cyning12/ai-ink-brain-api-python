# ChatBI V2 Agent 架构 —— SPEC 文档目录

> **状态**：总规 **§7.4 / §7.5** 已与实现对齐（2026-05-07）；子规仍可能各自标 `draft`  
> **日期**：2026-04-27（目录修订：2026-05-07；**vNext 交互 SPEC** 见 `SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md`）

---

## 文档结构

```
docs/spec/v2-agent/
├── README.md                              # 本文件：目录说明
├── SPEC-ChatBI-V2-Agent-Overview.md       # 总规：目标、§7 验收、§7.4 全量对照、§7.5 深度回归
├── SPEC-ChatBI-V2-Gap-Checklist.md        # 缺口快照（与 §7.4 互补；下文含历史审计原文）
├── SPEC-ChatBI-V2-Intent.md               # 意图：测试集、缓存
├── SPEC-ChatBI-V2-Tool-Design.md          # 子规：Tool 接口与封装
├── SPEC-ChatBI-V2-ReAct-Loop.md           # 子规：ReAct 循环详细设计
├── SPEC-ChatBI-V2-Memory.md               # 子规：记忆管理设计
├── SPEC-ChatBI-V2-Events.md               # 子规：事件流兼容设计
└── SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md  # 下一版：执行期增量 SSE + LLM 流式 + Timeline/双栏
```

---

## 阅读顺序

1. **SPEC-ChatBI-V2-Agent-Overview.md** — 先读总规，理解架构目标和模块关系
2. **SPEC-ChatBI-V2-Tool-Design.md** — 再读 Tool 设计，理解如何复用 V1
3. **SPEC-ChatBI-V2-ReAct-Loop.md** — 再读 ReAct 循环，理解 Agent 核心逻辑
4. **SPEC-ChatBI-V2-Memory.md** — 再读记忆管理，理解多轮对话
5. **SPEC-ChatBI-V2-Events.md** — 最后读事件流，理解前后端兼容  
6. **SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md** — 下一版：执行期增量 SSE 与 Timeline/双栏（**在 V2 里程碑暂结之后**排期）

---

## 关联文档

| 文档 | 位置 | 说明 |
|------|------|------|
| P0 归档 | `docs/tasks/done/task_chatbi_v2_agent_p0_backend.md` | 骨架与契约 |
| P1 总览 | `docs/tasks/active/task_chatbi_v2_agent_p1_behavior.md` | Eval / 缓存 / P1-D 等子链入口 |
| 技术图谱 | `docs/_tech_graph/10_flow_rag.md` | RAG 流程 |
| 技术图谱 | `docs/_tech_graph/11_flow_text2sql.md` | Text2SQL 流程 |
| 项目配置 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 环境变量真值表 |
| 前端仓 | `ai-ink-brain/`（`PY_API_URL`、`components/chain-chat`） | 全量对照 §7.4「前端」列 |

---

## 快速导航

- [总规：架构目标与模块设计](SPEC-ChatBI-V2-Agent-Overview.md)
- [意图识别升级设计](SPEC-ChatBI-V2-Intent.md) ⬅️ 新增
- [Tool 设计与封装](SPEC-ChatBI-V2-Tool-Design.md)
- [ReAct 循环详细设计](SPEC-ChatBI-V2-ReAct-Loop.md)
- [记忆管理设计](SPEC-ChatBI-V2-Memory.md)
- [事件流兼容设计](SPEC-ChatBI-V2-Events.md)
- [下一版：增量 SSE 与 Timeline 实时感知](SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md)
