# Prompt · Portfolio 后端 W5 关账 Loop（00 开帽 → CLOSE · KPI）

> **用途**：**新对话**粘贴 **§3 全文**；由 **00 总调度** 编排帽链，**关账至 CLOSE**（含 **`### KPI（00）`** 打分）。  
> **Open Folder**：`ai-ink-brain-api-python`（W5 预跑读前端 content / 生产 URL 时 `@` 双仓）  
> **配对前端**：前端并行 **W3 visitor-auth**（`ai-ink-brain` · `task_portfolio_visitor_auth_v1` 或等价 LoopTask）；**本 Prompt 不改前端 / 不改 `api/`**  
> **task 真值**：[`docs/tasks/active/task_portfolio_rag_demo_v1.md`](../tasks/active/task_portfolio_rag_demo_v1.md)（W2/W3 文档已 done · **W5 待人**）

---

## 1. 帽链（关账 · 非止于 50）

```text
00 → 10 → 22(R1′) ⇄ 10 → 30 → 40 → 22(R2) → Task·50 → CLOSE（KPI + 关账回溯）
```

| 帽 | 执行者 | 要点 |
|----|--------|------|
| **00** | 主 Chat | 扫 task / gates / `audit_profile: post_close`；派 10；**关账轮**填 `### KPI（00）` |
| **10** | 主 Chat semi_auto | **W5 专项**细化验收·failure_paths·与前端 W3 边界；更新 task §2.3 / 人工闸说明 |
| **22 R1′** | 主 Chat | W5 增量审查落盘（若 R1 已存在则 **R1′ 增量** 或 **R2 前复核**）；阻塞 → 仅回 10 |
| **30** | 主 Chat semi_auto | 文档/RUNBOOK/留证目录；**禁止** `api/`/`tests/`；**禁止**代跑生产 sync |
| **40** | 主 Chat | 回填 `### 自检结论`；W5 证据 **有人提供则落盘**，无则标 **blocked_by 人闸** |
| **22 R2** | 主 Chat | 签收/关闭节 → 派 Task 50 |
| **50** | **Task 子代理** | Fresh Context · W5 验收矩阵 · reinspect 落盘 |
| **CLOSE** | 主 Chat（00） | `### KPI（00）` · `HANDOFF_CLOSE_TRACE` · **人签后** `git mv` → `done/` |

> **与前端 W2 LoopTask 差异**：本链 **不停在 50**；`kpi_aggregator: CLOSE` · `audit_profile: post_close`。

---

## 2. 前置（开跑前人工 1 分钟）

| # | 动作 |
|---|------|
| 1 | Open Folder = **`ai-ink-brain-api-python`** |
| 2 | `git checkout main && git pull` → `git checkout -b task/portfolio-rag-w5-v1`（**勿在 main 提交**） |
| 3 | 确认前端 W5 语料存在：`ai-ink-brain/content/{methodology,resume,evidence}/` 各 ≥1 `.md` |
| 4 | 确认 `.env` / Vercel：`CONTENT_ROOT`、`SYNC_ADMIN_SECRET`、Supabase、Embedding 已配（见 `.env.example` § Portfolio） |
| 5 | **若已 sync**：准备 job 终态 JSON 摘要；**若未 sync**：Agent 须在 HG-W5-SYNC 前 **STOP** 并输出 RUNBOOK §2 curl |
| 6 | 新 Chat 粘贴 **§3 全文** |

---

## 3. 可复制 Prompt 正文（从下一行起 · 00 开帽）

```text
## 角色

你是 **Harness 00 总调度 + 关账编排 Agent（Portfolio 后端 · W5 sync + 五问留证 + task 关账）**，严格遵循：
- docs/harness/prompts/hats/00-orchestrator.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md（换帽 invoke + commit）
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md（关账回溯）
- docs/harness/guides/KPI_RUBRIC_v1_2.md（HatInstance + Task_KPI%）
- docs/tasks/active/task_portfolio_rag_demo_v1.md
- docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md（§6 · §7 W5）
- docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md
- docs/spec/governance/投递冲刺_20260609_v1_zh.md §2 五问 · §7 Checklist
- ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md（§4.3 访客秘钥 · **只读** · 与 W3 对齐表述）
- AGENTS.md · .cursor/rules/07-git-workflow.mdc

Open Folder = ai-ink-brain-api-python
git_branch = task/portfolio-rag-w5-v1
task_slug = portfolio-rag-demo
task_path = docs/tasks/active/task_portfolio_rag_demo_v1.md
freeze_id = PORTFOLIO-RAG-DEMO@2026-06-01
semi_auto = true
audit_profile = post_close
kpi_rubric = KPI_RUBRIC_v1_2
kpi_aggregator = CLOSE
experience_capture = recommended
test_strategy = recommended

## 关账 Loop 硬规则

1. **帽序**：00 → 10 → 22(R1′) → [10↔22 直至放行] → 30 → 40 → 22(R2) → **Task 50** → **CLOSE**
2. **跳过 20**；**禁止**无 22 书面进 30
3. **禁止**修改 `api/`、`tests/`、CI workflow（本 Epic 文档 + 留证；既有 pytest 仅回归确认）
4. **禁止**对生产/预发执行 `POST /api/py/admin/sync`（RUNBOOK §2 仅 **人** 执行；Agent 可写 curl、可落盘 **脱敏** JSON）
5. **禁止**代填 `human_gate` 为 `approved`；遇 `HG-W5-SYNC` / `HG-W5-FIVE-Q` **pending** 须 STOP 并输出 **gate_id + 文件路径 + 人须动作**
6. 换帽前：下一棒 §3 invoke 全文 → `docs/harness/invokes/by-task/portfolio-rag-demo/` → **commit**（任务分支）
7. **50 必须 Task 子代理**（Fresh Context）；主会话只收短报告
8. **CLOSE 轮**：按 KPI_RUBRIC_v1_2 填 task **`### KPI（00）`**（HatInstance 表 + Task_KPI% + blocked 说明）
9. **git mv → done/** 与更新 `docs/tasks/_views/done.md`：**仅当** HG-W5-* 与 HG-REINSPECT 均已 **人签 approved** 且 50 pass；否则 CLOSE 输出 **待人工清单**，**不**关账移动 task

## 人工闸（读 task 当前 status · 勿代填）

| human_gate_id | 典型 blocks | 人须完成 |
|---------------|-------------|----------|
| HG-W5-SYNC | 40 W5 留证 | 预发/生产等价环境 sync **succeeded** + 硬检查（§2.3 G-W5-1） |
| HG-W5-FIVE-Q | done | 五问 5/5 + diary 留证 + Q1/Q5 sources×2（§2.3 G-W5-2～4） |
| HG-REINSPECT | done | 50 落盘后人签（已 approved 则 50 后复核即可） |

**访客秘钥（前端 W3）**：Unified Chat 五问 Bearer 走 **`chatbi_access_tokens`**（见 `api/chatbi_principal.py` · `docs/diary/local_chatbi_access_token_gen.py`）。本 task **可**在 RUNBOOK §1.3 增补 **运维签发 token** 指针；**不**实现前端 unlock。

## W5 业务真值（不得弱化）

| 项 | 标准 |
|----|------|
| Sync | 仅 `POST /api/py/admin/sync`；`succeeded`；`filesScanned>0`；`chunksUpserted>0`；三目录各 ≥1 `.md` |
| 五问 | 问句与投递冲刺 §2 **逐字**；Q3 sources **仅** `evidence`；单问重试 ≤3 |
| 留证 | **本地默认** `tmp/portfolio-rag-demo/`（`PORTFOLIO_RAG_EVIDENCE_DIR`）：`sync-job-final.json`、`q1/q5-sources-run{1,2}.json`、`five-questions-results.md`；**人签后**脱敏复制至 `docs/diary/samples/portfolio-rag-demo/` |
| 鉴权分工 | admin/sync → **`SYNC_ADMIN_SECRET`**（shell：`export ADMIN_TOKEN="$SYNC_ADMIN_SECRET"`）；五问 → visitor ChatBI Bearer（**非** admin secret） |

## 00 本轮立即动作

1. 读 task + 最新 `docs/harness/invokes/by-task/portfolio-rag-demo/` invoke
2. 落盘本 Prompt 快照 → `docs/harness/invokes/by-task/portfolio-rag-demo/invoke_YYYYMMDD_00_portfolio-rag-w5-close.md`
3. commit invoke
4. **自动进入 10 帽**（semi_auto；若 HG-TASK-DRAFT 类闸阻塞则报 gate_id）

---

### 【帽 10 · W5 需求细化】

真值：docs/harness/prompts/hats/10-requirements.md · TEMPLATE-requirements-invoke.md §3

**目标**：在 **不改 api** 前提下，把 task §2.3 W5 验收写清；补 **与前端 W3 分工** 一节；确认 failure_paths 覆盖 F5/F6。

**输出**：
- 更新 `docs/tasks/active/task_portfolio_rag_demo_v1.md`（§2.3 / §6.2 / 实现备忘 W5 行）
- 下一棒 **22 R1′** Prompt 全文落盘 invoke
- SDD：`不涉及新 SPEC` · `轮0+1+2 已完成，清单已人确认`

**禁止**：扩 scope 到 ChatBI handoff · 前端 unlock 实现

---

### 【帽 22 R1′ · W5 增量审查】

落盘：`docs/harness/reviews/by-task/portfolio-rag-demo/task_portfolio_rag_demo_v1_audit_R1_W5_YYYYMMDD.md`

- 阻塞 → **仅回 10**
- 放行 → 30（W5 文档/留证 tranche）

---

### 【帽 30 · 执行 · 文档/留证】

**在范围**
1. RUNBOOK §1.3：增补 **ChatBI visitor token** 签发指针（`local_chatbi_access_token_gen.py` · `GET /api/py/chatbi/access/verify` · 与前端 W3 unlock **分工**）
2. `docs/diary/samples/portfolio-rag-demo/README.md`：W5 留证清单（**本地 tmp → 冻结 diary**）与 **blocked** 占位说明
3. 若维护者 **已提供** sync/五问脱敏 JSON → 落盘 diary；**未提供** → 写 `NOTES-w5-pending_YYYYMMDD.md` 待人执行
4. `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §C.1：**仅**若 W5 发现 env 缺口则最小增补（无密钥）
5. pytest 回归：`pytest tests -m "not intent_eval and not intent_benchmark" -q`（应仍绿）

**禁止**：`api/` · 生产 sync · 真实密钥入 Git

---

### 【帽 40 · 自检】

回填 task `### 自检结论（执行者）`：含 W5 验收表 pass/fail/defer · pytest 行 · **人工闸状态**

若 HG-W5-SYNC / HG-W5-FIVE-Q 仍 pending：**不得**宣称 W5 pass；须列 **待人 RUNBOOK 步骤**

---

### 【帽 22 R2 · 签收】

落盘 `docs/harness/reviews/by-task/portfolio-rag-demo/task_portfolio_rag_demo_v1_audit_R2_W5_YYYYMMDD.md` → 派 **Task 50**

---

### 【帽 50 · Task 子代理】

Fresh Context · 模板参考 `docs/tasks/reinspect_results/reinspect_portfolio_rag_demo_v1_20260601_v1.md`

落盘：`docs/tasks/reinspect_results/reinspect_portfolio_rag_demo_v1_W5_YYYYMMDD_v1.md`

**defer 非 fail**：前端 W3 unlock · W4 chip · 卷四/卷五 release 后再 sync（RUNBOOK §7）

---

### 【帽 CLOSE · 00 · KPI + 关账】

1. 汇总各帽 **HatInstance** → task **`### KPI（00）`**（rubric `KPI_RUBRIC_v1_2`）
2. 输出 **执行路线与 Commit 回溯**（HANDOFF_CLOSE_TRACE §2）
3. **若人闸全 approved + 50 建议合并**：
   - `git mv docs/tasks/active/task_portfolio_rag_demo_v1.md docs/tasks/done/`
   - 更新 `docs/tasks/_views/done.md`
   - commit：`docs(task): 关账 portfolio-rag-demo W5`
4. **若人闸 pending**：输出 **待人工表**（gate_id · 文件 · 动作）；**不** git mv

**experience_capture**：若本轮有 CI/测试教训，可追加 `docs/diary/samples/portfolio-rag-demo/NOTES-*.md`（可选）

## 给 Cursor

00、CLOSE、KPI、portfolio-rag-demo、W5、五问、RUNBOOK、HG-W5-SYNC、HG-W5-FIVE-Q、chatbi_access_tokens、semi_auto
```

---

## 4. 与前端 W3 并行说明

| 维度 | 前端 W3 | 本后端 Prompt |
|------|---------|---------------|
| 秘钥形态 | `PORTFOLIO_VISITOR_*` → unlock Cookie | `chatbi_access_tokens` Bearer（DB） |
| 代码仓 | `ai-ink-brain` · unlock/session | **本仓仅文档** + 五问 RUNBOOK |
| 汇合点 | W6 生产 URL 五问 + 录屏 | W5 留证 + task 关账 |

---

## 5. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-02 | 初版：前端 W3 并行 · 后端 W5 关账 Loop · 00→CLOSE + KPI |
