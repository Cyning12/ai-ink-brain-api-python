# Task：Tech Graph P1 — 方案A最小落地（manifest + 自动校验）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：done  
> **关联图谱**：`docs/_tech_graph/00_main.ai.md`、`docs/_tech_graph/10_flow_*.ai.md`、`docs/_tech_graph/99_spec.md`  
> **前端依赖**：无

---

## 背景与目标

P0 已补齐可接手性与最小漂移检测，但仍缺少“机器可读真值”，导致：

- 只能做粗粒度覆盖检查，无法精确定位差异与归因
- 无法对“新增/改名”做强约束（容易漏改图谱）

P1 目标：落地 **方案A最小闭环**：

- 引入 manifest（机器可读真值）
- 自动校验 manifest 与源码/SQL 一致性（不一致即失败）
- （可选）由 manifest 渲染/更新部分 `.ai.md`（先校验，后生成）

---

## 范围

### 1) manifest（真值来源）

- [x] 新增 `docs/_tech_graph/_manifest.json`（或 `.yaml`，优先 json）包含：
  - [x] endpoints：从 `api/index.py` 抽取的 `/api/py/*` 路由
  - [x] supabase：
    - [x] tables：`documents` / `code_chunks` / `rag_conversation_logs` 等
    - [x] rpc：`match_documents` / `keyword_documents` / refresh 等
  - [x] env：关键环境变量（见 `99_spec.md` Env Truth Table）
  - [x] anchors：关键 handler/函数锚点（path + line 或 symbol）

### 2) validator（强校验）

- [x] 新增 `tools/tech_graph_manifest_check.py`：
  - [x] 从源码/SQL 抽取真值（端点/RPC/表/env）
  - [x] 对比 manifest（缺失/多余/不一致）并给出可读 diff
  - [x] 返回码：0=OK，1=drift，2=运行错误

### 3)（可选）renderer（增量生成）

- [ ] 新增 `tools/tech_graph_render_ai.py`（可选，若时间足够）：
  - [ ] 以 manifest 为输入，增量更新 `00_main.ai.md` 的端点与锚点段落
  - [ ] 不重绘业务子流程（保持增量）

---

## 非范围

- 不做 P2/P3（分层视角 / 端到端边界）——P1 完成后重评
- 不把所有 env 都拉进 manifest（仅关键子集）
- 不引入完整 CI workflow（但保留可被 CI 调用的脚本接口）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| Mermaid 协议 | `docs/_tech_graph/99_mermaid_protocol.md` |
| 路由真值 | `api/index.py` |
| RPC/表调用点 | `api/*.py` |
| SQL 真值 | `supabase/sql/*.sql` |
| P0 漂移检测 | `tools/tech_graph_drift_check.py`（保留为 quick check） |

---

## 验收标准

- [x] `docs/_tech_graph/_manifest.json` 存在且字段齐全（endpoints/rpc/tables/env/anchors）
- [x] `python tools/tech_graph_manifest_check.py` 输出 `OK`
- [x] 当手动制造漂移（例如改一个端点字符串或 rpc 名称）时，校验脚本能失败并指出差异
- [ ] （可选）`python tools/tech_graph_render_ai.py` 可根据 manifest 增量更新 `00_main.ai.md`

---

## 检查发现问题与修复记录

- **问题**：在负向测试（手动制造漂移）后，`_manifest.json` 未恢复，导致校验持续失败（缺失 `POST /api/py/unified/chat/stream`）。
- **修复**：将该 endpoint 条目补回 `docs/_tech_graph/_manifest.json`，并重新运行校验脚本确认恢复 `OK`。

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/_manifest.json`、`tools/tech_graph_manifest_check.py`、（可选）`tools/tech_graph_render_ai.py`、相关 `.ai.md` |
| 关键 env | manifest 覆盖的 env 子集（与 `99_spec.md` 一致） |
| 接口变更 | 无（文档/工具链变更） |
| 图谱变更点 | manifest 成为真值来源；`.ai.md` 可被增量渲染 |

