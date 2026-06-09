> **epic**：`standards-engineering/api-modularization`
> **manifest_ref**：W3 · task_standards_backend_api_modularization_manifest_v1.md
> **test_strategy**：`required`
> **非范围**：MANIFEST 表内未列出的 `api/*.py` 文件

---

# W3 · Admin Ingest 路由下沉

> **状态**：done（PR 待创建 · 2026-06-09）
> **slug**：`api-routes-admin-ingest-split`
> **git_branch**：`task/api-routes-admin-w3`
> **风险**：Medium
> **freeze_id**：`CODING_BACKEND_L2@2026-06-09`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `api-routes-admin-ingest-split` |
| **git_branch** | `task/api-routes-admin-w3` |
| **orchestration** | Claude Code Harness 链 |
| **chain_prompt** | `PROMPT_claude_chain_serial_v1_T1_standards-backend-api-modularization-w2-w8_zh.md` |
| **test_strategy** | `required` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |

---

## 目标

将 `api/index.py` 中 admin/sync/ingest 路由抽至 `api/routes/admin_ingest.py`；`index.py` 仅保留路由注册薄层。

### 下沉范围

| 路由 | 方法 | 行数（HEAD） |
|------|------|-------------|
| `/api/py/admin/sync` | POST | ~25 行 |
| `/api/py/admin/sync` | GET | ~15 行 |
| `/api/py/admin/ingest` | POST | ~27 行 |

### 共享处理

`_require_auth` 被 admin 路由和 legacy_chat.py（延迟 import）共用。W3 将其提取至 `api/auth_utils.py`，避免循环依赖：
- `api/auth_utils.py`：新建，含 `_require_auth`
- `api/index.py`：从 `auth_utils` import，移除本地定义
- `api/routes/admin_ingest.py`：从 `auth_utils` import `_require_auth`
- `legacy_chat.py` 不改动：其内部 `from ..index import _require_auth` 仍有效（index.py 仍暴露该名）

### 死代码清理

`_require_rag_history_auth` 已在 `legacy_chat.py` 中定义，index.py 中的版本不再使用，W3 一并移除。

---

## 行为变更（Delta）

### ADDED
- `api/routes/admin_ingest.py` — 新模块，含 3 个 admin 路由 handler
- `api/auth_utils.py` — 新模块，含 `_require_auth`

### MODIFIED
- `api/index.py` — 移除 admin handler body 和 `_require_auth`/`_require_rag_history_auth`

### 不变
- 所有对外 HTTP path / method / request body / response shape
- `_contract_manifest.json` 无变更

---

## 先测后拆（D2）

| 路由 | 测试文件 | 覆盖 |
|------|----------|------|
| `/api/py/admin/ingest` POST | 已有 `tests/test_admin_ingest_route.py` | 复用，验证 mock 后仍通过 |
| `/api/py/admin/sync` POST/GET | `tests/test_admin_sync_route.py` | auth 401、missing jobId 400、job not found 404、mock sync 202/200 |

---

## 失败路径

| # | Scenario ID | 触发 | 行为 |
|---|-------------|------|------|
| F1 | fp-mega-refactor | 单 PR 触及 >8 个 `api/*.py` | **拒合并** |
| F2 | fp-contract-break | 路由 path/method 变更 | **blocked** |
| F3 | fp-cycle-dep | `admin_ingest.py` 与 `index.py` 循环导入 | **blocked** — 用 `auth_utils.py` 隔离 |
| F4 | fp-legacy-break | 改动破坏 legacy_chat.py 的延迟 import | **40 阻塞** |

---

## 验收标准

- [x] `api/routes/admin_ingest.py` 存在且 ruff 绿
- [x] `api/auth_utils.py` 存在且 ruff 绿
- [x] `api/index.py` 仍包含 admin 路由注册（@app.post/get），但 handler body 已下沉
- [x] `index.py` 行数从 ~446 降至 ~345
- [x] `tests/test_admin_ingest_route.py` 仍通过
- [x] `tests/test_admin_sync_route.py` 通过
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [x] `ruff check api tests` 全绿
- [x] 单 PR 触及 `api/*.py` 数量 ≤8（实际 4 个）

---

---

## 自检结论（40）

| # | 验收项 | 结果 |
|---|--------|------|
| 1 | `api/routes/admin_ingest.py` 存在且 ruff 绿 | PASS |
| 2 | `api/auth_utils.py` 存在且 ruff 绿 | PASS |
| 3 | `index.py` 路由注册保留，handler body 已下沉 | PASS |
| 4 | `index.py` 行数 345（目标 <380） | PASS |
| 5 | `test_admin_ingest_route.py` 仍通过 | PASS |
| 6 | `test_admin_sync_route.py` 通过（5 例） | PASS |
| 7 | pytest 352 passed, 1 skipped | PASS |
| 8 | ruff 全绿 | PASS |
| 9 | 单 PR 触及 4 个 `api/*.py` | PASS |
| 10 | manifest + contract 全绿 | PASS |

**总体结论**：通过，无阻塞。

---

## 关闭回溯（CLOSE · 2026-06-09）

### 执行路线

| 阶段 | 关键动作 | Commit |
|------|----------|--------|
| DRAFT | task 文件创建 | `@a7473b7` |
| 30 | 代码实现 + 测试 | `@b2f77b0` |
| CLOSE | manifest 修复 + task 状态 done | — |

### 分仓 Commit 索引

- `b2f77b0` refactor(api): W3 admin ingest 路由下沉 + auth_utils 提取
- `a7473b7` docs(harness): W3 task draft

---

## 修订记录

| 日期 | 说明 |
|------|------|
| 2026-06-09 | v1：W3 task 初稿 — admin ingest 路由下沉 |
