# ChatBI V2 Agent 架构 —— SPEC 文档目录

> **状态**：draft  
> **日期**：2026-04-27

---

## 文档结构

```
docs/spec/v2-agent/
├── README.md                              # 本文件：目录说明
├── SPEC-ChatBI-V2-Agent-Overview.md       # 总规：架构目标、模块设计、验收标准
├── SPEC-ChatBI-V2-Tool-Design.md          # 子规：Tool 接口与封装
├── SPEC-ChatBI-V2-ReAct-Loop.md           # 子规：ReAct 循环详细设计
├── SPEC-ChatBI-V2-Memory.md               # 子规：记忆管理设计
└── SPEC-ChatBI-V2-Events.md               # 子规：事件流兼容设计
```

---

## 阅读顺序

1. **SPEC-ChatBI-V2-Agent-Overview.md** — 先读总规，理解架构目标和模块关系
2. **SPEC-ChatBI-V2-Tool-Design.md** — 再读 Tool 设计，理解如何复用 V1
3. **SPEC-ChatBI-V2-ReAct-Loop.md** — 再读 ReAct 循环，理解 Agent 核心逻辑
4. **SPEC-ChatBI-V2-Memory.md** — 再读记忆管理，理解多轮对话
5. **SPEC-ChatBI-V2-Events.md** — 最后读事件流，理解前后端兼容

---

## 关联文档

| 文档 | 位置 | 说明 |
|------|------|------|
| 任务单 | `docs/tasks/active/task_chatbi_v2_agent_v1.md` | 开发任务追踪（待创建） |
| 技术图谱 | `docs/_tech_graph/10_flow_rag.md` | RAG 流程 |
| 技术图谱 | `docs/_tech_graph/11_flow_text2sql.md` | Text2SQL 流程 |
| 项目配置 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 环境变量真值表 |

---

## 快速导航

- [总规：架构目标与模块设计](SPEC-ChatBI-V2-Agent-Overview.md)
- [意图识别升级设计](SPEC-ChatBI-V2-Intent.md) ⬅️ 新增
- [Tool 设计与封装](SPEC-ChatBI-V2-Tool-Design.md)
- [ReAct 循环详细设计](SPEC-ChatBI-V2-ReAct-Loop.md)
- [记忆管理设计](SPEC-ChatBI-V2-Memory.md)
- [事件流兼容设计](SPEC-ChatBI-V2-Events.md)
