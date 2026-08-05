# 后端编码规范 P3+P4（L3 `.mdc` 短链 + Ruff CI）

> **状态**：done（PR [#145](https://github.com/Cyning12/ai-ink-brain-api-python/pull/145) · 2026-06-09）
> **schedule_ref**：编码规范 Epic · §1.5 P3/P4  
> **epic**：`standards-engineering`（工作区 [`00_OUTLINE`](../../../docs/standards/00_OUTLINE_工程编码规范改进_v1_zh.md) §5 P3/P4）  
> **前置**：[`done/task_standards_backend_l2_draft_v1.md`](../done/task_standards_backend_l2_draft_v1.md) · PR [#143](https://github.com/Cyning12/ai-ink-brain-api-python/pull/143) · L2 **active** v1.1  
> **前端对称**：[`ai-ink-brain`](../../../ai-ink-brain/) · `07-coding-standards-l2.mdc` + ESLint `no-explicit-any: error`（2026-06-09）  
> **关联图谱**：`docs/_tech_graph/99_spec.md`（规约层 · 无业务流程变更）  
> **前端依赖**：无  
> **后端依赖**：无

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **task_slug** | `standards-backend-p3-p4-l3-ruff` |
| **test_strategy** | `recommended` |
| **test_strategy_note** | 以 CI `ruff check` 绿 + 既有 pytest 绿为主；不新增业务行为测试 |
| **code_quality_bar** | `baseline` |
| **freeze_id** | `CODING_BACKEND_L2@2026-06-09` |
| **orchestration** | `Cursor Task 链` |
| **chain_prompt** | （30 帽执行时新建 `PROMPT_*_chain_serial_*_standards-backend-p3-p4_*`） |
| **semi_auto** | `false` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/standards-backend-p3-p4-l3-ruff` |
| **experience_capture** | `recommended` |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `CLOSE` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | 总设 / 执行前人扫 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 后人签 |
| HG-RUFF-BASELINE | pending | done | 首版 Ruff CI 绿后人签（避免 silent 全仓 ignore） |

---

## 背景与目标

L2 后端 **active**（P-01～P-15）已签收；§6 标 **P3 待办**（Cursor 短链）、§5 标 **Ruff 未入 CI**。本 task **小步**交付 L3 + P4，对称前端 P3/P4，**不**顺带做 Python 服务模块拆分（见 [`task_standards_backend_api_modularization_manifest_v1.md`](task_standards_backend_api_modularization_manifest_v1.md)）。

**完成态**：

1. **P3**：`.cursor/rules/31-coding-standards-l2.mdc`（≤15 行 · 链 L2；**勿**用 `07-` — 本仓 `07-git-workflow.mdc` 已占用）
2. **P4**：`ruff.toml` + `requirements.txt`（或 dev 依赖文档化）+ CI Required 步骤 + `scripts/verify-pr-local.sh` 可选同步
3. L2 [`CODING_BACKEND_L2_v1_zh.md`](../../standards/CODING_BACKEND_L2_v1_zh.md) §5/§6 状态更新（v1.2）

---

## 范围

- [x] 新建 `.cursor/rules/31-coding-standards-l2.mdc`（`globs: api/**/*.py,tests/**/*.py` · 短链至 L2 + L1 pointer）
- [x] 更新 `AGENTS.md` 规则索引（或 `python tools/gen_agents_md.py` 若需再生成）
- [x] 新建 `ruff.toml`：`select` 首批 `E,F,I,UP,B`；`ANN` **warn 或 extend-ignore**（P4 渐进 · 对齐 OUTLINE §1.4 P1）
- [x] `requirements.txt` 增加 `ruff` 版本 pin（与 CI Python 3.11 一致）
- [x] CI：在 `verify-fast.yml` 或新 `ruff.yml` 增加 **Required** job/step：`ruff check api tests`
- [x] 首绿策略：仅修 **ruff 新报且易修** 项；历史债大块 ignore 须 **task 内表格列文件+理由**（禁止空 `ignore` 全仓）
- [x] 更新 L2 §5 工具表、§6 L3 路径、§7 修订记录 → v1.2
- [x] 更新 [`docs/standards/README.md`](../../standards/README.md) P3/P4 行

## 非范围

- **不** 在本 task 内拆分 `index.py` / `unified_chat.py` 等上帝模块（Epic 子 task）
- **不** 全仓 `ruff format` 重格式化
- **不** 关闭或削弱既有 pytest / tech-graph Required checks
- **不** 修改 Unified Chat / RAG **运行时行为**（仅 lint/规则/文档）

---

## 行为变更（Delta）

无

（工具链与 Agent 可读规则；无对外 HTTP 行为变更。）

### ADDED

- CI：`ruff check` Required（路径见上）
- Cursor：L3 短链规则 `31-coding-standards-l2.mdc`

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| L2 真值 | [`docs/standards/CODING_BACKEND_L2_v1_zh.md`](../../standards/CODING_BACKEND_L2_v1_zh.md) |
| L1 | 工作区 [`CODING_BASELINE_L1_v1_zh.md`](../../../docs/standards/CODING_BASELINE_L1_v1_zh.md) |
| SOURCES REF-PEP8 | 工作区 [`SOURCES_编码规范外部参考_v1_zh.md`](../../../docs/standards/SOURCES_编码规范外部参考_v1_zh.md) |
| 本地验收 | `bash scripts/verify-pr-local.sh` · 合并前须 pytest 绿 |
| 前端对照 | `ai-ink-brain/.cursor/rules/07-coding-standards-l2.mdc` · `eslint.config.mjs` |

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | fp-ruff-ci-red | PR 引入 ruff 违规 | CI fail · 阻塞 merge | 是（修代码或收窄规则） | GitHub checks 红 |
| F2 | fp-ruff-ignore-sweep | 为绿而全仓 `# noqa` / 空 ignore | 22 审查拒签 | — | — |

---

## 验收标准

- [x] `31-coding-standards-l2.mdc` 存在且 ≤15 行、无 P-01～P-15 全文复制
- [x] `ruff check api tests` 本地与 CI **绿**
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` 仍绿
- [x] L2 升 **v1.2**；§6 指向实际 `.mdc` 路径
- [x] PR Test plan 含 ruff + pytest 命令
- [ ] （可选）工作区 `00_OUTLINE` §5 后端 P3/P4 行更新为 ✅

**合并前必绿**：tech-graph + contract + pytest + **ruff**（本 task 新增）

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| ruff 版本 | `0.9.10`（`requirements.txt`） |
| CI workflow | `.github/workflows/verify-fast.yml` · step `Ruff check` |
| 首版 ignore 表 | `ruff.toml`：`E501` 行宽 · `E402` env 加载 · `B008` FastAPI Depends · `UP017/UP038/UP041` 渐进 |
| 代码 touch | import 排序/清理（`ruff --fix`）· 5 处 lint 小修（`B904`/`F841`/`B012`）· **无** 行为变更 |

---

## 给 Cursor

- Open Folder：**本仓根**
- 先读 L2 §5/§6 · 前端 `07-coding-standards-l2.mdc` **仅结构对照**
- 模块拆分 **禁止** 本 task 展开 → 见 Epic MANIFEST
