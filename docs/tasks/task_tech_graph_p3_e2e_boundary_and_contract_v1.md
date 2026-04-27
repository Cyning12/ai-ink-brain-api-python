# Task：Tech Graph P3 — 端到端边界图 + 契约视图（跨仓按需加载）

> **状态**：pending  
> **范围**：以 `ai-ink-brain-api-python` 为主仓，仅画“跨仓边界与契约”；不改业务代码  
> **关联图谱**：`docs/_tech_graph/00_main.ai.md`、`docs/_tech_graph/14_runtime_observability.ai.md`、`docs/_tech_graph/99_spec.md`  
> **前端依赖**：无（仅文档）；但需引用前端仓真实路径/协议（禁止脑补）

---

## 背景与目标

P0/P1/P2 已覆盖“后端内聚视角 + 可校验 + 排障视图”，但端到端协作仍缺少一张**系统边界图**，用于回答：

- 前端如何消费 SSE / JSON（事件类型与字段契约）
- content 语料如何进入后端 ingest（`CONTENT_ROOT` 边界）
- 后端如何与 Supabase（tables/RPC）交互（权限与失败模式）

P3 目标：新增一套**跨仓边界 + 契约**的按需加载图谱，使新 Agent 能在不读前端代码细节的前提下完成端到端改动评估。

---

## 范围

### 1) 新增端到端边界图（AI 协议版 + 人类版）

- [ ] 新增 `docs/_tech_graph/15_e2e_boundary.ai.md`
  - [ ] 节点必须覆盖 4 个域：
    - [ ] Frontend（SSE consumer / UI timeline renderer）
    - [ ] Content repo（语料来源：`content/`）
    - [ ] Backend API（本仓 endpoints：以 `_manifest.json` 为真值）
    - [ ] Supabase（tables/RPC：以 `_manifest.json` 为真值）
  - [ ] 边必须标注协议语义：`->` / `~>` / `?>` / `[ok]` / `[err]` / `::yields`
  - [ ] 所有跨仓边都必须有“契约锚点”（文件/端点/事件类型），禁止模糊描述

- [ ] 新增 `docs/_tech_graph/15_e2e_boundary.md`
  - [ ] 最小同步（≤ 12 节点），仅保留人类阅读主干

### 2) 将边界图接入主入口（按需加载）

- [ ] 更新 `docs/_tech_graph/00_main.ai.md`：新增 `加载 -> 15_e2e_boundary.md`
- [ ] 更新 `docs/_tech_graph/00_main.md`：新增链接条目（保持人类版一致）

### 3) 契约清单（事件 + HTTP）

- [ ] 在 `15_e2e_boundary.ai.md` 内以“payload keys 列表节点”表达：
  - [ ] `/api/py/unified/chat/stream` 的 SSE 包络（`chain` / `done`）
  - [ ] 核心事件类型集合（参考 `14_runtime_observability.ai.md`）
  - [ ] `rag.sources` 与 `sql.result` 的最小字段键（只列键名，不贴长 JSON）

---

## 非范围

- 不画前端内部组件树与状态管理（仅边界与契约）
- 不新增或修改后端接口（只做文档图谱）
- 不复制粘贴前端大段代码（只做锚点与契约键名）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 后端真值（端点/表/RPC/env） | `docs/_tech_graph/_manifest.json` |
| 运行/事件视图 | `docs/_tech_graph/14_runtime_observability.ai.md` |
| Mermaid 协议 | `docs/_tech_graph/99_mermaid_protocol.md` |
| 前端/内容仓锚点 | 必须引用真实文件路径（由执行 Agent 自行读取确认） |

---

## 验收标准

- [x] `15_e2e_boundary.ai.md` 与 `15_e2e_boundary.md` 同时存在（双轨）
- [x] 从 `00_main.ai.md` 可按需加载跳转到 `15_e2e_boundary.md`
- [x] 图中所有跨仓边均有锚点（前端/内容仓/后端/DB）且不编造
- [x] `python tools/tech_graph_manifest_check.py` 仍输出 `OK`（P3 不引入后端漂移）

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/15_e2e_boundary.ai.md`、`docs/_tech_graph/15_e2e_boundary.md`、`docs/_tech_graph/00_main(.ai).md` |
| 关键契约 | `<SSE 事件类型 + 最小字段键名>` |
| 锚点来源 | `<前端/内容仓引用的真实文件列表>` |

