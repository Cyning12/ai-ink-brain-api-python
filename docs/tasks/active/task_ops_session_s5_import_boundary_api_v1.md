# Task · Ops Session S5.0 Import Boundary API（harness_runtime 无 RAG 硬依赖）

> **状态**：`draft` · 00 统筹起草 · 2026-07-03  
> **epic**：Session Orchestrator · S5 `ops-session-s5-extract`  
> **schedule_ref**：SPEC §11 · §12.1 S5 · BLOCKERS B5/B7 · PLAN §5  
> **关联 SPEC**：[`SPEC_ops_session_orchestrator_v1_zh.md`](../../../ai-ink-brain/docs/tasks/specs/SPEC_ops_session_orchestrator_v1_zh.md) §11.2 Import 边界 · §11.3 抽包路线  
> **前置**：`[task_ops_session_s4_verify_api_v1.md](../done/task_ops_session_s4_verify_api_v1.md)` · HG-S4-LOCAL-ACCEPTANCE · PR #229 merged（或本地验收后可开工）  
> **配对前端**：无（纯后端 Runtime 边界）  
> **依赖**：无外部 probe；Runtime 内 **禁止 import harness_probe**  
> **人拍板**：D3 = **等 v0.10.1 可用** · 本 task **不**改 probe 集成，仅 import 边界 pytest（PLAN §9）

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-session-s5-import-boundary-api` |
| **module_id** | `OPS-SESSION-ORCH` |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **test_strategy** | `required` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **git_branch** | `task/ops-session-s5-import-boundary-api` |
| **blocks** | S5.1 `ops-session-s5-extract-adr` |
| **blocked_by** | S4 `ops-session-s4-verify-api` |

### 行为变更 Delta

| 变更 | 类型 | 触达 api/ | 说明 |
| --- | --- | --- | --- |
| 新增 import 边界 pytest | ADDED | `tests/harness_runtime/test_import_boundary_*.py` | 静态/动态 import 黑名单校验 |
| 新增 `harness_runtime` 包隔离显式声明 | ADDED | `api/harness_runtime/__init__.py` · `pyproject.toml` 可选 | 边界契约文档化 |
| 修正 S0–S4 潜在越界 import | MODIFIED | `api/harness_runtime/**`（若边界测试失败） | 仅当 pytest 暴露违规时 |

---

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | `approved` | 20-task-audit, 30 | 人签 · 2026-07-03 · 派工执行 |
| HG-AUDIT-R1 | `approved` | 30 | 人签 · 2026-07-03 · 20-task-audit 关注点由 30/50 复核 |

---

## 背景与目标

SPEC §11.2 强制：`harness_runtime` 内 **禁止 import** `api.ingest_*` · `api.rag_*` · `api.index` chat 路径 · `public.documents` 等业务 ORM，以保证 Runtime 可剥离为独立 Agent 产品（BLOCKERS B5 monorepo 子包 → S5 评估抽包）。

**完成态一句话**：`pytest tests/harness_runtime/test_import_boundary*.py` 绿，证明 `harness_runtime` 在静态与动态层面均无 RAG/ingest/业务 DB 硬依赖；若测试失败则修复越界 import。

### 拍板（00 统筹 · SPEC/BLOCKERS）

| # | 决策 |
| --- | --- |
| D1 | **禁止 import 黑名单**（SPEC §11.2）：`api.ingest_*` · `api.rag_*` · `api.index` · `public.documents` · 任何 RAG/ingest/业务 ORM |
| D2 | 允许标准库 · pydantic · langgraph · langchain_core · `api.ops` Protocol/DTO（注入） |
| D3 | `harness_runtime` 内 **禁止 import harness_probe**（B7 · subprocess 非 import） |
| D4 | 边界测试：静态 AST + 动态 import 双保险 |

---

## 范围

- [ ] 新建 `tests/harness_runtime/test_import_boundary_static.py`：AST 扫描 `api/harness_runtime/` 内所有 Python 文件，断言无黑名单 import / `from` import
- [ ] 新建 `tests/harness_runtime/test_import_boundary_dynamic.py`：在隔离 Python 进程中 import `api.harness_runtime` 及关键子模块，断言成功且不触发黑名单模块加载
- [ ] 提供违规模块列表（Scenario ID 化）到 pytest 失败信息，便于定位
- [ ] 若 S0–S4 代码存在越界 import，则重构为 adapters 注入 / Protocol / 延迟 import
- [ ] 更新 `api/harness_runtime/__init__.py`（或新增 `BOUNDARY.md`）显式列出允许依赖
- [ ] ruff + pytest 全量绿：`pytest tests/harness_runtime -q`

---

## 非范围

- 不改 RAG/ingest/业务 ORM 本身逻辑
- 不实现抽包（仅做边界 · 抽包评估见 S5.1）
- 不引入 harness-probe import
- 不新增对外接口契约
- 不处理 graph_delta promote（S5.2 可选）

---

## 失败路径

| # | Scenario ID | 触发 | 行为 | 可重试 |
| --- | --- | --- | --- | --- |
| F1 | fp-import-rag-static | AST 发现 `api.rag_*` 或 `public.documents` import | pytest fail，输出违规文件与行号 | 否（须改代码） |
| F2 | fp-import-ingest-static | AST 发现 `api.ingest_*` import | pytest fail，输出违规文件与行号 | 否（须改代码） |
| F3 | fp-import-chat-dynamic | 动态 import `api.harness_runtime` 时加载 `api.index` chat 路径 | pytest fail，输出 sys.modules 意外加载项 | 否（须改代码） |
| F4 | fp-import-probe | Runtime 内出现 `import harness_probe` | pytest fail，违反 B7 subprocess 约定 | 否（须改代码） |
| F5 | fp-adapter-cycle | 拆分时引入循环 import | pytest fail / ruff fail | 否（须重构） |

---

## 20-task-audit 关注点

- [ ] S5.0 与 S5.1 是否应合并为单一 task？（人要求 20-task-audit 再次确认拆分合理性）
- [ ] import 边界黑名单是否完整（SPEC §11.2）
- [ ] failure_paths 是否覆盖 AST 与动态 import 两种失败模式
- [ ] 是否有遗漏的 RAG/ingest/业务 ORM 越界调用

---

## 验收标准

- [ ] `pytest tests/harness_runtime/test_import_boundary_static.py -q` 绿
- [ ] `pytest tests/harness_runtime/test_import_boundary_dynamic.py -q` 绿
- [ ] `pytest tests/harness_runtime -q` 全量绿（S1–S4 回归）
- [ ] `ruff check api/harness_runtime tests/harness_runtime` 0 error
- [ ] 无新增 `import harness_probe`
- [ ] 新增/修改文件均有边界说明注释

**合并前必绿**：`pytest tests/harness_runtime -q` · `ruff check api/harness_runtime`

---

### 自检结论（执行者，30 回填）

| 项 | 结果 |
| --- | --- |
| **日期** | 2026-07-03 |
| **分支** | `task/ops-session-s5-import-boundary-api` |

```text
# 30 完成后回填：ruff → pass（S5 文件 0 error；S4.2 untracked 文件有 1 F841 未修）
# import_boundary_static → 19 passed
# import_boundary_dynamic → 1 passed
# harness 全量 → 54 passed, 2 failed（均来自未关联的 S4.2 test_session_promote_conflict_s4_2.py；排除后 48 passed）
```

---

## 给 Cursor

`ops-session-s5-import-boundary-api` · **HG-AUDIT-R1 pending** · 30 不可开工直至人签。
