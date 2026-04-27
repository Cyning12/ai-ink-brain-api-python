# Task：Tech Graph P6 — 跨仓契约 Manifest + Cross-Repo 门禁脚本（SSE/Events）

> **状态**：done  
> **关联图谱**：`docs/_tech_graph/14_runtime_observability.ai.md`、`docs/_tech_graph/15_e2e_boundary.ai.md`  
> **前端依赖**：无（不要求改前端代码，但需要读取前端仓文件做校验）

---

## 背景与目标

P4 解决的是**后端仓内部**的漂移门禁（端点/RPC/表/env/anchors）。  
但 Unified Chat 的真实风险点是“**前端消费字段** 与 **后端产出字段** 的隐式耦合”：

- 后端改了 SSE events 的字段/结构，前端解析崩
- 前端开始依赖某个字段，但后端并未承诺稳定

P6 目标：引入一个**跨仓契约真值**（contract manifest），并提供一个脚本做 Cross-Repo 校验：

- 后端输出（truth）必须覆盖契约（manifest）
- 前端读取（expect）不得超出契约（manifest）
- 校验失败即返回非 0（可被 CI/本地门禁调用）

> 约束：只做“可机械验证的键名/枚举集合”，不做语义理解；不贴长 JSON。

---

## 范围

### 1) 新增跨仓契约 manifest（真值来源）

- [x] 新增 `docs/_tech_graph/_contract_manifest.json`
  - [x] SSE envelope：
    - [x] `event` 允许值：`chain` / `done`
    - [x] `data` 最小键（按 event 分类）
  - [x] `chain.data` 最小键：`type`、`ts`、`step_id`、`payload`
  - [x] `done.data` 最小键：`ok`、`mode`、`run_id`、`session_id`
  - [x] 关键事件 payload（只列键名）：
    - [x] `rag.sources.payload.sources[*]` keys（参考 `14_runtime_observability.ai.md`）
    - [x] `sql.result.payload` keys（参考 `14_runtime_observability.ai.md`）
  - [x] 前端锚点（只做定位，不强耦合校验）：
    - [x] SSE 消费点（TSX 文件路径）
    - [x] Next BFF 透传点（route.ts 文件路径）

### 2) 新增 cross-repo 校验脚本

- [x] 新增 `tools/tech_graph_contract_check.py`
  - [x] 输入：`docs/_tech_graph/_contract_manifest.json`
  - [x] 后端抽取（backend truth）：
    - [x] 从 `api/unified_chat.py` 抽取 `_event()` 产出的 `type` 集合（或显式常量表）
    - [x] 从 `_build_rag_sources_event` / `sql.result` 构造处抽取 payload keys（只抽 dict 顶层键）
  - [x] 前端抽取（frontend expect）：
    - [x] 从 manifest 给定的 TSX/route.ts 锚点文件中，抽取对 `event/data/type/payload` 的访问键名
      - [x] 采用静态提取（regex/轻量解析），只校验键名/枚举集合
  - [x] 对比规则（最小但有效）：
    - [x] `backend_truth ⊇ contract_manifest`（后端至少产出承诺键）
    - [x] `frontend_expect ⊆ contract_manifest`（前端不得读取未承诺键）
    - [x] `frontend_expect.event_values ⊆ allowed_events`
  - [x] 输出：可读 diff（缺失/越界/枚举不一致）
  - [x] 返回码：0=OK，1=drift，2=运行错误/文件缺失

### 3) 图谱对接（按需加载）

- [x] 在 `docs/_tech_graph/15_e2e_boundary.ai.md` 的备注区补充：
  - [x] `contract_manifest` 作为跨仓契约真值
  - [x] `tools/tech_graph_contract_check.py` 作为跨端门禁入口

---

## 非范围

- 不要求前端改为强类型 SDK（不做生成 TypeScript types）
- 不做全量 AST 解析（除非 regex 不足以稳定抽取）
- 不接入 CI（可在后续任务中把该脚本加入前端/后端 CI；P6 先把脚本跑通）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 后端真值（端点等） | `docs/_tech_graph/_manifest.json`（不直接校验跨端字段，但可用于定位） |
| 运行事件视图 | `docs/_tech_graph/14_runtime_observability.ai.md` |
| 跨仓边界与锚点 | `docs/_tech_graph/15_e2e_boundary.ai.md` |

---

## 验收标准

- [x] `docs/_tech_graph/_contract_manifest.json` 存在，且键名集合覆盖 `14_runtime_observability.ai.md` 的最小字段
- [x] `python tools/tech_graph_contract_check.py` 在本机可运行并输出 `OK`
- [x] 负向用例：手工在 `_contract_manifest.json` 删除一个必需键时，脚本必须失败并指出缺失
- [x] 负向用例：手工在前端消费点（或用临时 patch）增加对未承诺字段的访问时，脚本必须失败并指出越界键

---

## 开发流程（SOP｜避免“先改哪边”导致返工）

### A) 端点变更（HTTP 路由层）
- 顺序：
  1) 改后端实现（`api/index.py` 新增/修改 `@app.get/post`）
  2) 同步更新 `docs/_tech_graph/_manifest.json`（method/path/handler/anchor）
  3) 运行 `python tools/tech_graph_manifest_check.py` 必须 `OK`
  4) （如启用 P5）运行 render，同步 `00_main.ai.md` 的 auto 区块

> 端点变更通常不涉及 `_contract_manifest.json`（那是跨端 events/字段契约）。

### B) SSE/Events 契约变更（跨端字段层）
- 顺序（契约优先）：
  1) 先更新 `docs/_tech_graph/_contract_manifest.json`（只改键名/枚举集合）
  2) 改后端产出（`api/unified_chat.py` 的 `_event/_sse/rag.sources/sql.result`）
  3) 跑 `python tools/tech_graph_contract_check.py`（backend_truth ⊇ contract）
  4) 改前端消费（P3 锚点 TSX/route.ts）
  5) 再跑 `python tools/tech_graph_contract_check.py`（frontend_expect ⊆ contract）

---

## 手动测试用例（必须执行）

> ✅ 已执行：用例 1-3 全部通过（2026-04-27）。

### 用例 1：正向（全一致）
- 操作：运行 `python tools/tech_graph_contract_check.py`
- 期望：输出 `OK`

### 用例 1.1：本地体验（推荐，一键演示负向→恢复）
- 操作：运行 `python tools/tech_graph_contract_demo.py`
- 期望：
  - baseline 为 OK
  - 删除必需键后失败
  - restore 后恢复 OK

### 用例 2：负向（契约缺失 → 报缺失）
- 操作：从 `_contract_manifest.json` 删除 `done.data.session_id`（或任一必需键），再运行脚本
- 期望：失败，提示 `missing` 键名
- 回滚：恢复文件后再次运行应为 `OK`

### 用例 3：负向（前端越界读取 → 报越界）
- 操作：在前端 SSE 消费点临时加入一次对不存在键的读取（例如 `data.payload.nonexistent_key`），再运行脚本
- 期望：失败，提示 `extra/forbidden` 键名
- 回滚：撤销该读取后再次运行应为 `OK`

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/_contract_manifest.json`、`tools/tech_graph_contract_check.py`、（可选）`docs/_tech_graph/15_e2e_boundary.ai.md` |
| 关键限制 | 静态抽取仅校验键名/枚举，不做语义推断 |
| 前端锚点 | `../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx`、`../ai-ink-brain/app/api/py/unified/chat/stream/route.ts` |

