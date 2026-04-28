# Task：文档真值校准（PROJECT_CONFIG）+ 图谱 Backlog 状态对齐 + Legacy RAG 与 Unified 去重复用

> **状态**：done（2026-04-28 验收通过）  
> **归档路径**：`docs/tasks/done/task_docs_truth_and_rag_unify_v1.md`  
> **交付**：T1 PROJECT_CONFIG、T2 `99_spec` 表、T3 初批 `api/rag_shared`  
> **来源矛盾**：`docs/diary/test/result_AB_hybrid_v1.md` §漂移防线（PROJECT_CONFIG 过时、`99_spec.md` Backlog 完成度、`Legacy chat` vs `Unified` 重复实现）  
> **关联图谱**：`docs/_tech_graph/99_spec.md`（Next Steps Backlog）、`docs/_tech_graph/10_flow_rag*.md`  
> **关联真值表**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

---

## 背景与目标

### 矛盾点归纳（需在任务中逐项收口）

| # | 现象 | 期望 |
|---|------|------|
| 1 | `PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 与仓库现状不符（如 E 节仍写「未发现 `.github/workflows/`」；B 节仍以 `.cursorrules` / 「未发现 `.cursor/rules`」为主叙事） | **真值表与 AGENTS / 目录事实一致**，便于 Agent 接手不靠幻觉 |
| 2 | `docs/_tech_graph/99_spec.md` 内 **Next Steps Backlog** Mermaid 给人「路线图仍在推进」观感；Hybrid 核验表明 **P0/P1 相当一部分已落地**（manifest、manifest_check CI、drift_check 脚本等），**P2/P3/HOLD** 仍为未完成或搁置 | Backlog **显式标注完成度**，避免读者误判优先级 |
| 3 | `api/index.py::chat`（Legacy）与 `api/unified_chat.py`（RAG 分支）在 **threshold 解析、embedding 降级、keyword/融合** 等处 **重复实现**，长期漂移 | **以 Unified 侧可复用逻辑为单一实现源（SoT）**，Legacy 变薄壳或共用模块，降低双处修 bug |

---

## 范围 / 非范围

**范围**

- 修订 **`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`**（不删除整篇）。
- 在 **`docs/_tech_graph/99_spec.md`** 为 Backlog 增加 **可读的状态说明**（见子任务 T2）。
- 规划并（可选分 PR）实施 **RAG 共享层抽离与 Legacy 调用迁移**（见子任务 T3）。

**非范围**

- 不改变对外 HTTP 路径与默认行为语义（除非子任务 T3 验收明确允许极小行为对齐且测全）。
- 不删除 `POST /api/py/chat`（仅讨论「内部实现收缩」，下线路由若要做须单独任务）。

---

## 子任务与验收标准

### T1：`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` — **更新为主，不建议删除**

**结论（执行前先对齐）**

- **不建议删除**整份真值表：总仓 `AGENTS.md`、本子 Agent 流程仍依赖「PROJECT_CONFIG」作为人类可读边界说明。
- **建议**：**分段修订 + 文首或文末增加「最后校准日期」与「本节对照仓库路径」**；对已与事实矛盾的句子 **改写或删除該句**，而非删掉文档。

**必须修订的已知漂移（来自 Hybrid）**

- **§E 目录地图**：补充 `.github/workflows/` **已存在**，并列出与图谱相关的 workflow 文件名及用途（`tech-graph.yml`、`tech-graph-contract.yml`）；删除或改写「本仓当前未发现 workflows」类表述。
- **§B Cursor / Agent 规则**：与仓库现状对齐——`.cursor/rules/*.mdc` 为当前规则载体；`.cursorrules` 若仍存在则标注「兼容/遗留」而非「唯一真值」。
- **§A / §F**：若仍只列 Legacy 流式端点，需 **补充 Unified** 相关路径（`/api/py/unified/chat`、`/stream`）及「契约见 `_contract_manifest.json`」的交叉引用（简要即可）。

**验收**

- [x] 上述章节与 `ls .github/workflows`、`.cursor/rules`、`_manifest.json` 无矛盾；新 Agent 仅读 PROJECT_CONFIG + AGENTS 不会被带偏。
- [x] 文末或文首存在 **校准日期**（或 Git 提交说明中引用本 task id）。

---

### T2：`99_spec.md` — Next Steps Backlog **未完成部分显式化**

**结论**

- Backlog **整体并非「全部未完成」**：Hybrid 结论——**manifest / manifest CI / drift_check 脚本 / contract_check** 等已部分兑现；**P2/P3、Parking Lot（K1–K4）、Deferred HOLD** 仍可视为 **未完成或待重评**。
- **不建议只删图**：图仍是路线图语境；应 **增补文字状态表**，与图并存。

**实施建议**

- 在 `docs/_tech_graph/99_spec.md` 中 **Next Steps Backlog 图下方**增加一节 **「Backlog 状态快照（YYYY-MM）」** Markdown 表格，列：`条目 | 状态（done / in_progress / todo / deferred）| 证据（脚本/workflow/PR）| 备注`。
- 至少覆盖图中节点：P0、P0_1–P0_3、P1、P1_1–P1_3、P2、P3、HOLD、K1–K4（可合并行若内容过细）。
- 若改动 `99_spec.md` 中 Mermaid：**按工作区图谱规则**评估是否需同步 **其他 flowchart 的 `.ai.md` 双轨**；本文件 **无** `99_spec.ai.md`，仅需保证 **人类版**自洽（本项为 prose+表，一般不触双轨冲突）。

**验收**

- [x] 任意读者能区分「已落地机制」与「仍为规划/挂起」。
- [x] `python tools/tech_graph_drift_check.py` 仍通过（若表内引用了端点名，勿与 md 漂移规则冲突）。

---

### T3：Legacy RAG 与 Unified — **重复代码合并 / 迁移方向**

**原则**

- **行为与事件格式以 Unified 模块化实现为 SoT**（与 Hybrid 锚点一致：`api/unified_chat.py` 中 RAG 工具链、`parse_match_threshold`（见 `rag_shared`）、RPC 调用、降级策略）。
- Legacy `api/index.py::chat` 中长期目标：**尽可能调用同一套纯函数或 `api/rag_*` 共享模块**，避免两份 `MATCH_COUNT` / threshold / fallback 分叉。

**建议实施顺序（可分 PR）**

1. **盘点**：列出 Legacy vs Unified 重复符号（threshold、embedding 失败分支、keyword dual 路、RRF 入参等），附行号对照表写入本 task「实现备忘」或 `docs/_tech_graph/02_version.md` 一条记录。
2. **抽取**：新建或扩展 `api/rag_shared.py`（名称以实际代码风格为准），迁入无状态工具函数（如统一 `parse_match_threshold`、统一 `rpc_execute_with_retry` 包装调用点）。
3. **迁移**：`unified_chat` 与 `index.chat` 均从共享模块引用；Legacy 专有部分（StreamingResponse、`x-sources`、文末 marker）保留在 `index.py`。
4. **回归**：`pytest tests/` 全绿；重点 `test_unified_chat_*`、`rag` 相关用例；可选加一条「Legacy 与 Unified 同一 query 检索命中一致性」冒烟（允许极小差异时在断言中说明）。

**验收**

- [x] **初批**：`parse_match_threshold`、`strip_doc_context_prefix` 已迁入 `api/rag_shared.py`，Legacy / Unified / code_retrieval（注入）共用。**完整去重**（embedding 降级、RRF、keyword 双路等）留待后续迭代，见 **`docs/tasks/specs/SPEC-06-unified-rag-retrieve-reliability.md`**。
- [x] 无新增 manifest/drift 违规（跑 `tech_graph_manifest_check.py`、`tech_graph_drift_check.py`）。

---

## 关联任务与迁移说明（减少重复）

| 文档 | 迁移说明 |
|------|----------|
| `docs/tasks/active/task_unified_chat_backend_v1.md` | 初版需求含「不改动 `/api/py/chat`」。**T3 若涉及 Legacy 内部重构**，在本任务验收中单独列出兼容策略；原任务仍以 Unified API 为准。**请在原文件顶部增加迁移指向（已由本次提交附上）。** |
| `docs/tasks/active/task_unified_chat_streaming_backend_sse_v1.md` | SSE 契约与 `_contract_manifest.json` 仍以 Unified 为准；T3 抽取共享逻辑时 **勿破坏** SSE 与非流式 payload 一致性。**已在原文件顶部增加指向。** |
| `docs/tasks/specs/SPEC-06-unified-rag-retrieve-reliability.md` | T3 实施后回填 SPEC 或在本任务「实现备忘」中注明是否满足可靠性条目。 |
| `docs/tasks/done/task_tech_graph_p0_handoff_and_drift_check_v1.md` 等 | 已 done 的图谱任务不再改正文；本任务 **仅继承其机制**（manifest/drift），不重复验收 P0。 |

---

## 给执行 Agent 的可复制 Prompt（节选）

以下为分派子 Agent 时的 **最小约束**（可按需粘贴到会话）；**本任务已归档**，复制时请改用路径 **`docs/tasks/done/task_docs_truth_and_rag_unify_v1.md`** 作为历史参照。

```text
你在仓库 ai-ink-brain-api-python 执行 task：docs/tasks/done/task_docs_truth_and_rag_unify_v1.md。

优先级：T1（PROJECT_CONFIG 真值修订）→ T2（99_spec Backlog 状态表）→ T3（RAG 共享层，需单独 PR 时先开分支）。

硬性规则：
1. 不得删除 docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md 全文；只能修订段落并标注校准日期。
2. 99_spec.md 增补 Backlog 状态表；勿删除原有 Mermaid，除非同步评估图谱双轨。
3. T3 以 api/unified_chat.py 侧逻辑为合并基准；Legacy 保留路由与流式外壳。
4. 每次变更后运行：python tools/tech_graph_manifest_check.py && python tools/tech_graph_drift_check.py

产出：PR 描述写明对应子任务 T1/T2/T3；若仅完成 T1+T2，在 PR 中注明 T3 deferred。
```

---

## 实现备忘（回填区）

| 项目 | 回填 |
|------|------|
| PR / 分支 | 本地验收：`pytest` 32 passed；`manifest_check` / `drift_check` OK（2026-04-28）。若有远端 PR 请在此补链接。 |
| PROJECT_CONFIG 校准日期 | 2026-04-28 |
| 99_spec Backlog 表追加的日期 | 2026-04 |
| RAG 共享模块路径 | `api/rag_shared.py`（`parse_match_threshold`、`strip_doc_context_prefix`） |

---

## 给 Cursor / 人的一句话

**PROJECT_CONFIG：更新不要删；Backlog：用状态表说清「已做/未做」；RAG：合并以 Unified 为准、Legacy 变薄。**
