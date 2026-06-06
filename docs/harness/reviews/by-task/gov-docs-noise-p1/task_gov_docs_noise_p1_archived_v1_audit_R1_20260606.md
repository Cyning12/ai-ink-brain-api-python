# 22 帽 · R1 任务审核 — gov-docs-noise-p1

> **hat**: 22-task-audit · **round**: R1 · **date**: 2026-06-06
> **task**: `docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md`
> **freeze_id**: `GOV-DOCS-NOISE-INVENTORY@2026-06-06`
> **invoke_snapshot**: `docs/harness/invokes/by-task/gov-docs-noise-p1/explore_P1_diff_20260606.md`

---

## 元信息

| 字段 | 值 |
|------|-----|
| task_slug | `gov_docs_noise_p1_archived_v1` |
| human_gate (HG-TASK-DRAFT) | `approved` |
| human_gate (HG-GOV-P1-EXEC) | `approved` |
| validate CLI | `OK` |
| semi_auto | `true` |
| audit_profile | `post_close` |
| test_strategy | `not_applicable` |

---

## 审查结论摘要

- **P1-1 / P1-2 范围清晰、可验收**：两交付项均为纯 docs 指针标注，变更范围极小，验收标准逐条可检。
- **explore 差分确认**：变更仅 `docs/` 下两文件 —— `docs/delivery/v0.2.0-code-rag/README.md`（文首插入 archived 横幅）、`docs/flows/README.md`（新建 POINTER）。
- **零 api/tests/workflows 触及**：`git diff --stat` 预期仅 docs 目录两文件。
- **无阻塞项**。

---

## 理论对齐检查表（P0 · GOV-HARNESS-THEORY-ALIGN-P0@2026-05-29）

### §3.1 任务单最小字段

| # | 检查项 | 通过 |
|---|--------|:--:|
| 1 | 头部 Harness 元信息表：`test_strategy` 三选一 | ✅ `not_applicable` |
| 2 | `not_applicable` 时 `test_strategy_note` 非空 | ✅ "纯 docs 指针修正；无 `api/` / 契约 / CI workflow 变更" |
| 3 | `failure_paths` ≥1 行（触发→行为→可重试→用户可见） | ✅ 5 行（F1–F5） |
| 4 | **非范围** 独立小节非空 | ✅ 7 条非范围 |
| 5 | **验收标准** 含 **合并前必绿** 条 | ✅ "单 PR · docs-only · CI Required 全绿" + pytest 命令 |
| 6 | （P1 抽检）`semi_auto` + `audit_profile` 已填 | ✅ `true` / `post_close` |

### §3.2 合并前 CI 验收条

| # | 检查项 | 通过 |
|---|--------|:--:|
| 1 | 验收含：PR 上 pytest workflow 全绿 + 本地等价命令 | ✅ "`pytest tests -m \"not intent_eval and not intent_benchmark\"`" |
| 2 | 40 自检 / PR 链接可核对（终轮 22 不得无证明签收） | — 待 T2b 40 帽回填 |

### §Blocking · 高敏须人判断

| # | 检查项 | 通过 |
|---|--------|:--:|
| 1 | 若触达 Blocking 任一行 → 上表已核对，缺项阻塞 | ✅ 未触达 Blocking 项（纯 docs，无 api/ 契约/运行锚点/主依赖变更） |

### §3.3 独立复检（50）触发

| # | 检查项 | 通过 |
|---|--------|:--:|
| 1 | `test_strategy` 与变更类型匹配 | ✅ `not_applicable` ↔ 纯 docs |
| 2 | `required` 且涉 `api/`/契约 → 关账前 50 已落盘或显式阻塞 | N/A |

### OpenSpec × TDD 勾选项（P0 · Loop R2 · T1+T2）

| # | 检查项 | 通过 |
|---|--------|:--:|
| 1 | `test_strategy` 与变更类型一致（触达 `api/` 时非 `not_applicable`） | ✅ |
| 2 | §行为变更 Delta 已填 或 显式「无」 | ✅ Delta 含 ADDED 两条 Requirement + Scenario |
| 3 | `failure_paths` 含 **Scenario ID** 列且非空 | ✅ F1–F5 均含 `Scenario ID` |
| 4 | 验收含 **合并前 pytest** 条（或 task 模板等价表述） | ✅ |

---

## 范围审查：P1-1 / P1-2

### P1-1 — delivery README archived 横幅

| 维度 | 审查结论 |
|------|---------|
| 目标文件 | `docs/delivery/v0.2.0-code-rag/README.md`（已存在） |
| 变更动作 | 文首插入 archived 横幅 + supersede 指针 |
| 内容要求 | ✅ `ARCHIVED` 标记、链至 `docs/harness/README` + `docs/spec/`、不删改正文 —— 均已在 task 中明确 |
| 验收可检 | ✅ `rg -n 'ARCHIVED'` 行号 < 5；`rg` 命中 harness/spec 链接；正文行数未减 |

### P1-2 — flows README 新建

| 维度 | 审查结论 |
|------|---------|
| 目标文件 | `docs/flows/README.md`（须新建） |
| 变更动作 | 新建 POINTER README |
| 内容要求 | ✅ freeze 日期 `2026-04-16`、Legacy chat 性质、superseded by `_tech_graph`、链至具体入口文件、索引 / POINTER 定位 —— 均已在 task 中明确 |
| 验收可检 | ✅ `test -f docs/flows/README.md`；`rg` 命中 freeze 日期 / Legacy / `_tech_graph` |

---

## explore 差分确认

依据 `explore_P1_diff_20260606.md`：

- **变更文件数**：2（均位于 `docs/`）
- **修改**：`docs/delivery/v0.2.0-code-rag/README.md` — 文首插入横幅，保留全文 106 行
- **新建**：`docs/flows/README.md` — 索引 / POINTER，不替代子文件
- **未触及**：`api/`、`tests/`、`.github/workflows/`、现有历史文件无删除

---

## 阻塞项

**零阻塞，建议 30 开工。**

---

## 可选：validate 结果

```
$ python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md
=== docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md ===
OK
```

---

## 签收 / 关闭

- **R1 结论**：task 合同可执行，无阻塞。
- **下一棒**：30 执行帽（`harness-30-docs.md`）→ 40 自检帽（`harness-40-check.md`）→ CLOSE。
- **50 复检**：跳过（纯 docs · `not_applicable`）。

---

## 下一棒可复制 Prompt

```text
【角色】Harness 30 · 执行帽
【任务】执行 docs-noise 治理 P1 —— 两文件最小扰动：
1. `docs/delivery/v0.2.0-code-rag/README.md` 文首插入 ARCHIVED 横幅（链至 docs/harness/README.md + docs/spec/），不删改正文。
2. 新建 `docs/flows/README.md`，含 freeze 日期 2026-04-16、Legacy chat 说明、superseded by docs/_tech_graph/ 指针（链至 00_main.md 或 README.md），明确本 README 仅为索引 / POINTER。
【约束】仅改 docs/ 下两文件；不碰 api/tests/workflows；不删历史文件。
【自检】git diff --stat 须仅 docs/ 两文件；rg 验证横幅与链接存在。
【交付】执行后交 40 自检帽。
```
