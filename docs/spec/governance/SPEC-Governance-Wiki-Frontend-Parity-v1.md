# SPEC — 治理：前端 Harness / Coding Wiki Parity（P1-4 · v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **freeze_id** | `GOV-WIKI-FRONTEND-PARITY@2026-05-27` |
| **Roadmap** | [`SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.2 · **当前推广主棒** |
| **实验依据** | [`docs/harness/experiments/wiki_ctx_ab_representative_v1/conclusion_representative_zh.md`](../../harness/experiments/wiki_ctx_ab_representative_v1/conclusion_representative_zh.md) §4 · [`scorecard.md`](../../harness/experiments/wiki_ctx_ab_representative_v1/scorecard.md) |
| **后端读序（done）** | [`SPEC-Governance-Wiki-Agent-Readorder-v1.md`](./SPEC-Governance-Wiki-Agent-Readorder-v1.md) · **本 Epic 镜像，不重复 ingest** |
| **执行 task（工作区）** | [`Projects/docs/harness/tasks/active/task_harness_frontend_p1_4_wiki_parity_v1.md`](../../../../docs/harness/tasks/active/task_harness_frontend_p1_4_wiki_parity_v1.md) |
| **Agent 入口 Prompt** | [`Projects/docs/harness/invokes/by-task/harness-frontend-p1-4-parity/PROMPT_START_full_chain_v1.md`](../../../../docs/harness/invokes/by-task/harness-frontend-p1-4-parity/PROMPT_START_full_chain_v1.md) |

---

## 0. 完成态（一句话）

在 **`ai-ink-brain/`** 落地与后端 **Wiki-CTX-AB 代表性结论** 对齐的 **Harness + Agent 读序 parity**：前端 Agent 默认先走 **配对后端 `docs/coding_wiki/` 指针**（或前端自有 index 若已镜像），**不** 回读全量 `content/harness/invokes/`；Harness 目录 / rules 与后端 taxonomy **可对照、可验收**。

---

## 1. 背景与立项条件

| 项 | 结论 |
| --- | --- |
| **立项条件** | AB-REP **accepted（部分外推）** · 6 slug · 5/6 W **4/4** · T7/T8 pass — **已满足**（2026-05-27） |
| **定量附件** | 载荷降幅 **60.8%–77.3%**（见 scorecard 聚合） |
| **为何工作区 task** | 主交付在 **`ai-ink-brain/`**；Open Folder 须 **`Projects/`**（见工作区 `05-harness-workspace.mdc`） |
| **为何后端 SPEC** | 跨仓契约真值；其他 Agent **读本 SPEC** 即知当前推广安排，**不必**依赖会话窗口 |

---

## 2. 范围

| 在范围 | 说明 |
| --- | --- |
| **`ai-ink-brain/AGENTS.md`** | 插入 **Coding Wiki / 关账回顾读序**（链后端 `docs/coding_wiki/` 或等价 pointer） |
| **`.cursor/rules/`** | 可选短规则：禁止默认 glob 全量 harness invokes；改 UI/BFF 仍 L0 前端 `_tech_graph` |
| **`content/harness/` 或 `docs/harness/`** | 与后端 taxonomy §2.1 **对照表** + 缺口清单（模板 / invokes 路径 / review 落盘） |
| **前端 gold slug 集** | **≥3** 个 **前端 done task** slug（**非**后端 ingest 重复）；写入 task 正文锁定 |
| **工作区 invoke** | `docs/harness/invokes/by-task/harness-frontend-p1-4-parity/` 全链落盘 |

| 非范围 | 说明 |
| --- | --- |
| 后端 **`docs/coding_wiki/syntheses/`** 增删 | 属 Ingest Batch / P2 Loop |
| 改 **`api/`** / Python RAG | 后端仓 |
| 将 Wiki 升为 L0 架构真值 | 与 Roadmap §5 禁止项一致 |

---

## 3. 执行编排（单 task · 非 Loop）

| 字段 | 值 |
| --- | --- |
| **Open Folder** | **`Projects/`**（工作区根） |
| **代码仓** | `ai-ink-brain/` |
| **git_branch** | `task/harness-frontend-p1-4-parity-v1` |
| **Harness** | 单 task 全链 **22→关账** · [`SKILL-harness-task`](../../tasks/skills/SKILL-harness-task.md) |
| **test_strategy** | `not_applicable`（docs + rules；`pnpm lint` 若改 TS 配置则 task 内写明） |

**子 Agent 分工**：后端仓 Agent **仅** 维护本 SPEC + Roadmap + RECENT 指针；**执行** 由工作区 Agent 粘贴 `PROMPT_START_full_chain_v1.md` §3。

---

## 4. 验收标准（SPEC 级）

- [ ] 工作区 task **`done/`** 且 `_views/done.md` 已链
- [ ] `ai-ink-brain/AGENTS.md` 含 **Coding Wiki 读序** 一条（与后端 §2.1 语义等价）
- [ ] 前端 harness 与后端 taxonomy **对照表** 落盘（task 或 `content/harness/README.md`）
- [ ] **≥3** 前端 gold slug 锁定且 **不** 与后端 Batch-1 10 slug 重复
- [ ] PR 描述引用 AB-REP scorecard 降幅与 5/6 W 4/4

---

## 5. 关联引用

| 用途 | 路径 |
| --- | --- |
| 需求逐项对比 | [`docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) |
| 后端 ingest | [`SPEC-Governance-Wiki-Ingest-Batch-v1.md`](./SPEC-Governance-Wiki-Ingest-Batch-v1.md) |
| 工作区 Harness task 目录 | `Projects/docs/harness/tasks/README.md` |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：AB-REP 签收后冻结 P1-4；链工作区 task + PROMPT |

---

## 给 Cursor

`P1-4`、`Frontend Parity`、`Open Projects`、`harness-frontend-p1-4-parity`、`GOV-WIKI-FRONTEND-PARITY`
