# SPEC — 治理：Harness 理论对齐 · P0（最高优先）

| 项 | 内容 |
| --- | --- |
| **状态** | `done`（P0 关账 · PR #90 · 2026-05-29） |
| **优先级** | **P0 · 全仓最高**（压过业务 feature 队列，直至 §6 验收勾选完成） |
| **freeze_id** | `GOV-HARNESS-THEORY-ALIGN-P0@2026-05-29` |
| **对照稿** | `ai_coding_governance/lib/COMPARISON_Harness-Ralph理论_vs_Ink落地_v1_zh.md` |
| **排期** | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) **§0.5** |
| **依赖** | 既有 Harness P0（2026-05-22 模板/22 落盘）**已完成**；本 SPEC 收口 **理论差距**，不重复造模板 |

---

## 0. 完成态（一句话）

**所有** 进入 `active/` 的业务与治理 task、子仓 `AGENTS.md`、**22 审查清单** 与讲义/卷三对齐：**地图化导航、Harness 最小字段不可缺、合并前 CI 可核对、高敏变更强制独立复检**。

---

## 1. 背景与目标

| 痛点 | 本 SPEC |
| --- | --- |
| 讲义强调背压与短 AGENTS，子仓 AGENTS **380～486 行** | 瘦身至 **≤120 行**（细则外链） |
| `TASK_TEMPLATE` 已有字段，**active 业务 task 未系统填写** | 22 **拒开工** + 存量 task 回填 |
| 验收条常缺「PR CI 绿」 | 模板与 22 检查 **强制一条** |
| Ralph **Critic** = 独立验证；Ink **50 常省略** | `api/`/契约类 **强制 50** |

**非范围**：实现 Ralph / Hermes 编排器；改动 ChatBI 业务逻辑（除为验收补测）。

---

## 2. 交付物清单

| # | 交付物 | 路径 / 动作 |
| --- | --- | --- |
| P0-1 | **22 审查增补清单**（字段 + CI + 50 触发） | `docs/harness/prompts/22-task-audit.md` + `reviews/README.md` 链入 |
| P0-2 | **TASK_TEMPLATE / README** 强化 | `docs/tasks/templates/TASK_TEMPLATE.md` · `docs/tasks/README.md`（`test_strategy` 默认表摘要） |
| P0-3 | **AGENTS 地图化**（后端仓） | `AGENTS.md` ≤120 行；长文迁 `PROJECT_CONFIG` / `docs/harness/README.md` |
| P0-4 | **active task 回填** | `docs/tasks/active/*.md`：Harness 元信息表 + `failure_paths` + 合并前 CI 验收条 |
| P0-5 | **关账验收 task** | `docs/tasks/active/task_harness_theory_align_p0_v1.md` → `done/` |

---

## 3. 应然规则（真值）

### 3.1 任务单最小字段（与卷三 §11 对齐）

凡 **新 task** 与 **进入 30 执行** 的存量 task，头部 **Harness 元信息表** 须完整：

| 字段 | 要求 |
| --- | --- |
| `test_strategy` | 三选一；`not_applicable` 须 `test_strategy_note` |
| `failure_paths` | ≥1 行表格式行（触发→行为→可重试→用户可见） |
| **非范围** | 独立小节，非空 |
| **验收标准** | 含 **合并前必绿** 一条（见 §3.2） |

**22 R1**：缺任一项 → **阻塞**，交 **10 帽** 回填后再 R+1。

### 3.2 合并前 CI 验收条（固定文案）

验收标准 **必须** 包含（可勾选）：

```markdown
- [ ] PR 上 `pytest` workflow 全绿（本地等价：`pytest tests -m "not intent_eval and not intent_benchmark"`）
```

纯前端跨仓 task 在 task 内写明对应 `quality` workflow，仍须 **可核对命令 + 日志要点**。

### 3.3 独立复检（50）强制场景

| 变更类型 | `test_strategy` | 50 |
| --- | --- | --- |
| `api/`、HTTP/SSE 契约、鉴权、并发/背压 | `required` | **必须** `reinspect_results/` 落盘 |
| 纯 `docs/`、索引、无行为 | `not_applicable` | 可选 |
| 一般功能 | `recommended` | 22 终轮签收可收口；task 可标 `reinspect: optional` |

与 [`RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) **§0.0** 一致；本 SPEC 将 **检查项写入 22 模板**。

### 3.4 AGENTS.md 地图化（后端）

| 保留在 AGENTS | 迁出 |
| --- | --- |
| 角色边界、必读顺序（≤7 条）、目录表、禁止项 | 图谱明细、Harness 长说明、Wiki 读序全文 → 链 `docs/harness/README.md`、`CODING_WIKI.md` |

**行数目标**：`AGENTS.md` **≤120 行**（不含空行注释块重复）。

---

## 4. `test_strategy` 默认表（写入 `docs/tasks/README.md`）

| 变更类型 | 默认 |
| --- | --- |
| 鉴权、计费、SSE/流式背压、核心算法回归 | `required` |
| 一般 API/功能 | `recommended` |
| 纯文档、图谱排版、无行为注释 | `not_applicable` + note |

task 头可覆盖默认值，**22 须核对合理性**。

---

## 5. 失败路径（SPEC 级）

| 触发 | 行为 |
| --- | --- |
| 22 发现 task 缺 §3.1 字段 | 阻塞清单；**禁止** 30 开工 |
| 40 无「合并前 CI」证明 | 22 不得终轮签收 |
| `required` 且无 50 落盘 | 不得 `git mv` 至 `done/` |

---

## 6. 验收标准（本 SPEC 关账）

- [x] `22-task-audit.md` 含 **§3.1～3.3** 检查表（或等效 checklist 节）
- [x] `AGENTS.md` 行数 ≤120（`wc -l` → **89** 行，2026-05-29）
- [x] `docs/tasks/active/` 内业务相关 task（§1.1 表 #1～#6）已回填 Harness 表 + CI 验收条，或显式标 `draft` 且 **blocks 30**
- [x] 至少 **1 份** 22 审查 md 样例引用新清单（`reviews/by-task/harness-theory-align-p0/`）
- [x] `RECENT_TASK_SCHEDULE.md` **§0.5** 标 **done**（PR #90 · 2026-05-29）

---

## 7. 与卷三公众稿

| 公众稿节 | 本 SPEC 提供 |
| --- | --- |
| §11 | 最少字段表（可转写，不写帽号） |
| §12 | 22 落盘 + 零阻塞留痕 |
| §13 | CI 验收条 + `test_strategy` |

**卷三备注**：需 **合并后实测** 的指标（如 active 回填率）在正文标 `【待后端 P0 验收后核对】`，见 narrative vol3 **§0.4**。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-29 | 关账：PR #90 合并 · 50 复检 · RECENT §0.5 done |
| 2026-05-29 | 初版：理论对齐 P0；最高优先 |
