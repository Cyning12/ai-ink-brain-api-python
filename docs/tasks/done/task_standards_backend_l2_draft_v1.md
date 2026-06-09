# 起草后端编码规范 L2（P2 · 对称前端 active）

> **状态**：**done** — L2 **active** v1.1 · PR [#143](https://github.com/Cyning12/ai-ink-brain-api-python/pull/143) · 2026-06-09
> **schedule_ref**：编码规范 Epic · P2 后端  
> **epic**：`standards-engineering`（工作区 [`00_OUTLINE`](../../../docs/standards/00_OUTLINE_工程编码规范改进_v1_zh.md) §5 P2）  
> **关联图谱**：`docs/_tech_graph/99_spec.md`（规约层 · 无业务流程变更）  
> **前端对称**：[`ai-ink-brain/docs/standards/CODING_FRONTEND_L2_v1_zh.md`](../../../ai-ink-brain/docs/standards/CODING_FRONTEND_L2_v1_zh.md)（**active** v1.2 · R1 2026-06-09）  
> **后端依赖**：无  
> **前端依赖**：无（文档 task；L2 正文完成后前端可读对称条文）

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **task_slug** | `standards-backend-l2-draft` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯文档 + 可选 L3 `.mdc` 短链；无 `api/` 行为变更 |
| **code_quality_bar** | `baseline` |
| **freeze_id** | `CODING_BASELINE_L1@2026-06-09` |
| **orchestration** | `Cursor Task 链` |
| **chain_prompt** | `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_standards-backend-l2-draft_zh.md`（**30 帽起草**；实例由 22/10 回填占位符） |
| **semi_auto** | `false` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/standards-backend-l2-draft` |
| **experience_capture** | `recommended` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | 总设初稿人扫 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 落盘 `docs/harness/reviews/` 后人签 |
| HG-L2-ACTIVE | signed | done | L2 升 **active** v1.1（2026-06-09 · R1 无阻塞项） |

---

## 背景与目标

工作区 L1 已 **active**；前端 L2 已 **active**（F-01～F-14 · P3/P4）。本 task 交付 **后端栈 L2 初稿**，供后端 Agent **补全条文、工具映射、PR 自检与 R1 验收 Prompt**，对称进入 P3（`.mdc` 短链）与 P4（Ruff/pytest 升严）。

**完成态**：`docs/standards/CODING_BACKEND_L2_v1_zh.md`（`draft`）+ `docs/standards/README.md` 索引；条文 ID `P-01～P-xx`，每条 `遵循 B-xx`。

---

## 范围

- [x] 新建 `docs/standards/CODING_BACKEND_L2_v1_zh.md`（参照前端 L2 结构）
- [x] 新建 `docs/standards/README.md`（链 L1 · 本 L2 · 私仓 pointer）
- [x] 条文覆盖：后端服务层（路由、ingest、RAG、Unified Chat、错误 registry、结构化日志 · 见 L2 §1）
- [x] 映射 L1 B-01～B-12；REF：REF-PEP8、REF-GOOG-PY、REF-MS-REST、REF-OWASP-API（见工作区 [`SOURCES`](../../../docs/standards/SOURCES_编码规范外部参考_v1_zh.md)）
- [x] §4 PR 自检（叠加 L1 §4）；`code_quality_bar: strict` 链 Harness [`§5.9`](../../../docs/harness/HARNESS_V2_PLAN.md)
- [x] 反模式节选 `AP-01～`（对齐前端 AF 风格；可引用工作区 `ANTI_PATTERNS` 规划）
- [x] `AGENTS.md` / `docs/tasks/README.md` 增 L2 入口链
- [x] **给后端 Agent 回填**：P-条文编号、Ruff 规则 ID、`pytest` 门禁、失败路径与 FastAPI 错误形状示例

## 非范围

- **不** 在本 task 内改 Python 服务实现（属后续 tech-debt task）
- **不** 复制 L1 全文进后端仓
- **不** 前端 L2 条文修改
- P3 `.mdc`、P4 Ruff 升严可 **另 task** 或本 task 子阶段（由 22 帽拆分建议）

---

## 行为变更（Delta）

无

（文档真值 · 无对外 HTTP 行为变更。）

### ADDED

- `docs/standards/CODING_BACKEND_L2_v1_zh.md`（**active** v1.1）
- `docs/standards/README.md`、三方验收 Prompt、R1 评审报告

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| L1 真值 | 工作区 [`docs/standards/CODING_BASELINE_L1_v1_zh.md`](../../../docs/standards/CODING_BASELINE_L1_v1_zh.md) |
| OUTLINE | [`docs/standards/00_OUTLINE_工程编码规范改进_v1_zh.md`](../../../docs/standards/00_OUTLINE_工程编码规范改进_v1_zh.md) |
| PROJECT_CONFIG | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) |
| 前端 L2 对称 | [`ai-ink-brain/docs/standards/CODING_FRONTEND_L2_v1_zh.md`](../../../ai-ink-brain/docs/standards/CODING_FRONTEND_L2_v1_zh.md) |
| CI 真值 | `.github/workflows/pytest.yml`；`AGENTS.md` §8 |
| 错误形状 | `docs/spec/` 错误 registry / unified chat 错误约定（以图谱为准） |
| 图谱 | `docs/_tech_graph/11_flow_api.md` · `99_spec.md` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| — | 本 task 无运行时失败路径 | — | — | — |

---

## 验收标准

- [x] `docs/standards/CODING_BACKEND_L2_v1_zh.md` 存在且状态 **active** v1.1
- [x] 每条 `P-xx` 标注 `遵循 B-xx`；B-01～B-12 无遗漏
- [x] §4 PR 自检可勾选；链 Harness §5.9 `code_quality_bar`
- [x] `docs/standards/README.md` 可链达 L2 与 L1
- [x] `AGENTS.md` 或 `docs/tasks/README.md` 可发现 L2 入口
- [x] 工作区 `docs/standards/README.md` 后端行更新（由 CLOSE 或工作区 task 同步）
- [x] （可选）`PROMPT_third_party_review_BACKEND_L2_v1_zh.md` 初稿

**合并前必绿（本仓 · 文档 task）**：无 pytest 要求；若改动触发 CI，须 `pytest tests -m "not intent_eval and not intent_benchmark"` 绿。

---

## 规划摘要（给后端 Agent 扩展）

### 建议条文骨架（待补编号与细节）

| 主题 | 遵循 B-xx | 落地指向（初稿） |
|------|-----------|------------------|
| 路由/Handler 薄 | B-01 | `api/index.py` 注册；业务在 `api/*.py` 模块 |
| 早返回 / 嵌套 | B-02 | 校验前置；避免深层 try 套 try |
| `rag_env` / env | B-03 | `api/rag_env.py`；禁止散落 magic URL |
| 命名与类型 | B-04, B-08 | typed 边界；禁止裸 `dict` 对外 |
| 结构化错误 | B-05 | HTTPException / registry；对齐 BFF 转发 |
| 策略表驱动 | B-06 | intent / tier 映射表 |
| 最小 diff | B-07 | 禁止无关格式化 |
| 重复逻辑 | B-09 | 抽 `api/` 子模块 |
| pytest | B-10 | `tests/`；`test_strategy` 对齐 |
| 密钥 / SQL | B-11 | `SYNC_ADMIN_SECRET`；Text2SQL 路径 |
| 日志字段 | B-12 | `rag_conversation_logs`；request id |

### P3/P4 后续（本 task 可只留 §6 占位）

- P3：`.cursor/rules/07-coding-standards-l2.mdc`（或 `07-` 后端命名）短链
- P4：Ruff / 类型检查升严（对照 OUTLINE §1.4 P1 渐进）

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/standards/CODING_BACKEND_L2_v1_zh.md`、`docs/standards/README.md`、`docs/standards/PROMPT_third_party_review_BACKEND_L2_v1_zh.md`；`AGENTS.md`、`docs/tasks/README.md`、`docs/README.md`；工作区 `docs/standards/README.md` |
| 图谱变更点 | 无 |
| 工作区同步 | `docs/standards/README.md` 后端行 → **active**（本仓已签收；工作区待同步） |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | Read：前端 L2、L1、task、PROJECT_CONFIG、structured_error_registry、pytest.yml；L2 落地指向抽样 |
| 结论 | pass（文档交付；未改 Python 服务实现） |
| 要点 | P-01～P-15 覆盖 B-01～B-12；§4 PR 自检链 Harness §5.9；Ruff P4 标待办 |

---

## 给 Cursor / 后端 Agent

- Open Folder：**本仓根** `ai-ink-brain-api-python/`；读 L1 须 Open **`Projects/`** 或 `@` 工作区 `docs/standards/`。
- 对称参考：前端 L2 **勿复制**；按 Python/FastAPI 栈重写落地。
- 完成后建议：三方 R1 Prompt → `active`；再 P3/P4 task。
- 关键词：`CODING_BACKEND_L2`、`P-xx`、`遵循 B-xx`、`rag_env`、`pytest`、`code_quality_bar`、`Harness`、`RECENT_TASK_SCHEDULE`
