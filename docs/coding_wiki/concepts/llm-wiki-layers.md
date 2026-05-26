---
title: LLM Wiki 三层与本仓 L0/L1/L2
slug: llm-wiki-layers
layer: L2
status: compiled
freeze_id: CODING-WIKI-PILOT@2026-05-25
---

# LLM Wiki 三层与本仓 L0/L1/L2

## 要点

- **Karpathy LLM Wiki**：Raw → Wiki（互链 Markdown）→ Schema（ingest/query/lint）。  
- **本仓映射**：L0 = 图谱与契约；L1 = task + Harness 落盘；L2 = **本目录**（关账后编译）。  
- **流水线**：需求/SDD → Harness（10→22→30→40→50→关账）→ **可选** Wiki ingest → 下一任务。

## 何时读 Wiki vs 图谱

| 问题类型 | 优先 |
|----------|------|
| 影响面、依赖、RPC/表 | `graph_query` + `_tech_graph`（L0） |
| 单 task 验收与闸口 | L1 task / review |
| 跨 Epic 决策、Harness 口径、历史 why | L2 `index.md` + syntheses |
| 测试增删改查的 **过程档案**（非 coverage 真值） | L2 `decisions/`、`syntheses` §测试变更；真值仍在 `tests/` + L0 |

Schema 细则：[[../CODING_WIKI]] §7–§9。

## 链接

- Schema：[[../CODING_WIKI]]  
- 治理 SPEC：→ `docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`  
- Harness taxonomy：→ `docs/harness/README.md` §2.1
