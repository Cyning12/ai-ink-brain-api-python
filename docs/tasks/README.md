# docs/tasks/ 使用规则（v1）

> 目标：让新任务“落盘位置一致、状态可追踪、索引可直达”，并避免 `active/` 长期堆积。

---

## 最近任务安排（排期真值）

**近期执行顺序、Harness P0、active 清单与时间线** 以 **[`RECENT_TASK_SCHEDULE.md`](RECENT_TASK_SCHEDULE.md)** 为准；规划或 `@task` 前先读该表，再打开具体 `active/task_*.md`。

---

## 工作区 Harness 任务（不在本目录）

与 **跨子仓流程 / CI 门禁对齐** 相关的 Harness **任务单** 仍统一在工作区：

- **`../../../docs/harness/tasks/active/`**、**`../../../docs/harness/tasks/done/`**  
- 索引：**[`../../../docs/harness/tasks/README.md`](../../../docs/harness/tasks/README.md)**

**帽子 Prompt / TEMPLATE / 半自动通则** 已内嵌本仓，开发时读：

- **[`../harness/README.md`](../harness/README.md)** → **[`../harness/prompts/README.md`](../harness/prompts/README.md)**

本目录 **`docs/tasks/`** 仅承载 **本后端仓** 任务；invoke / review 落盘见 **`docs/harness/invokes/`**、**`docs/harness/reviews/`**。

---

## 目录结构（以当前仓为准）

```
docs/tasks/
  README.md                # 本文件：落盘规则
  RECENT_TASK_SCHEDULE.md  # 最近任务安排表（排期真值）
  _views/                  # 状态视图索引（聚合，不改原任务正文）
  active/                  # 设计中/待开始/进行中（task_*.md）
  done/                    # 已完成（task_*.md）；本仓任务的**归档目录**（相对 `active/`）
  specs/                   # 规格文档（SPEC-*.md）
  templates/               # 模板（TASK_TEMPLATE.md）
  legacy/                  # 历史命名/缺少状态/待补齐字段
  review_results/          # 审查帽输出归档（见该目录 README）；可交需求帽回填 task/SPEC
  reinspect_results/       # 独立复检帽输出归档（见该目录 README）；必要时交需求帽回填
```

### 工程纪律索引（防口头约定漂移）

- **ChatBI：新功能以 SSE 优先（团队纪律 task）**：[`done/task_engineering_chatbi_sse_first_v1.md`](done/task_engineering_chatbi_sse_first_v1.md) — 历史审查见 [`../diary/harness-archive/`](../diary/harness-archive/README.md)；**新 task** 22 帽落盘 [`../harness/reviews/`](../harness/reviews/README.md)。

### 审查与复检产出（非 task 单）

- **`review_results/`**：规格/任务 **审查帽**（`20`）结论归档；详见 [`review_results/README.md`](review_results/README.md)。  
- **`../harness/reviews/`**：**22 帽任务审核**（**仅本仓** `docs/tasks/` 绑定 task；勿混放总项目/他仓审查）。  
- **`reinspect_results/`**：**50 帽三方复检** — 关账必选。  
- **Harness**：[`../harness/README.md`](../harness/README.md)；10 结束输出 **下一棒 A（22）+ B（30）**，由人择一。

审查回填清单由 **需求帽**（[`../harness/prompts/10-requirements.md`](../harness/prompts/10-requirements.md)）更新本仓 `docs/tasks/`、`docs/spec/`。

---

## 新增任务如何落盘（必须遵守）

- **新建位置**：一律放在 `docs/tasks/active/`
- **命名规则**：`task_<domain>_<topic>_vN.md`（示例：`task_tech_graph_p8_xxx_v1.md`）
- **必须字段**：任务头部必须包含 `> **状态**：...`

允许状态集合（与现有模板兼容）：
- `draft`（等价 design）
- `pending`
- `in_progress`
- `done`

---

## 什么时候从 active 移到 done（归档目录）

当任务验收通过（满足任务文档里的“验收标准”）后，**必须**完成归档：`done/` 为本仓任务单的归档目录，与仍在推进的 `active/` 分离，避免 Agent 误判「仍在进行」。

### 任务归档流程（维护检查清单）

按顺序执行（可随同一提交完成）：

1. **核对验收**：任务正文「验收标准」已全部勾选为完成，或等价说明已写明例外与签核人/日期。  
2. **更新头部状态**：将 `> **状态**：...` 改为 `done（YYYY-MM-DD 验收通过）`（日期为实际验收日）。  
3. **移动文件**：在仓库根执行 `git mv docs/tasks/active/<文件名>.md docs/tasks/done/`，**禁止**仅复制内容而遗留 `active/` 同名文件。  
   - **硬规则**：**禁止**只把头部改成 `done` 而文件仍留在 `active/`（会误导 Agent）；**`done` 状态与 `git mv` 须在同一提交内完成**，真值以 **目录位置 + 头部状态** 双一致为准。  
4. **更新已完成索引**：在 `docs/tasks/_views/done.md` 追加一行指向 `../done/<文件名>.md` 的相对链接（可附简短验收说明，与现有条目风格一致）。  
5. **若任务曾列入进行中视图**：检查 `docs/tasks/_views/in_progress.md`，移除或更新对该任务的引用（避免双轨）。  
6. **配对前端 / 跨仓任务**：若头部或正文引用了 `ai-ink-brain/content/tasks/active/task_*.md`，须在 `ai-ink-brain` 仓按 **`content/tasks/README.md`** 执行归档：**`git mv`** 至 **`content/tasks/done/`**，更新 **`content/tasks/_views/done.md`**，头部 **`状态`** 改为 `done（YYYY-MM-DD 验收通过）`。（**不**移动 `docs/spec/` 下规格文件，规格持续维护、不因任务归档而搬迁。）

> 说明：`_views/*.md` 只做链接聚合，不作为真值；真值以任务文件头部 `状态` + 文件所在目录（`active/` 或 `done/`）为准。

---

## specs / legacy 的边界

- **`specs/`**：只放规格（`SPEC-*.md`），可被多个 task 引用。
- **`legacy/`**：只放历史遗留（命名不规范/缺少状态/待补齐字段）。后续“修复命名与状态”应通过独立 task 执行，避免一次性大改造成漂移。

---

## 视图索引维护规则（最小集）

- `docs/tasks/_views/design.md`：列出 `draft/design` 的任务 + “缺少状态字段”清单（统一维护在此）
- `docs/tasks/_views/backlog.md`：列出 `backlog`（**需求池**，排期前一览）
- `docs/tasks/_views/in_progress.md`：列出 `in_progress`
- `docs/tasks/_views/done.md`：列出 `done`

---

## Harness V2 · 任务单扩展字段

**模板真值**：[`templates/TASK_TEMPLATE.md`](templates/TASK_TEMPLATE.md)（含 `test_strategy`、`failure_paths`、`semi_auto`、`human_gate`、`audit_profile`、`git_branch` 等）；与 **`docs/harness/HARNESS_V2_PLAN.md` §5** 对齐。

新建 task 时 **复制模板** 再改占位符；细则与半自动通则见 [`../harness/prompts/HANDOFF_SEMI_AUTO.md`](../harness/prompts/HANDOFF_SEMI_AUTO.md)。

## 常见坑（强制避免）

- 不要把已完成任务留在 `active/`（会误导新 Agent 判断“还在做”）
- 不要在任务文件里写“已完成但状态还是 pending”（状态必须与事实一致）
- 不要在 `docs/tasks/` **顶层**混放零散 `task_*.md` / `SPEC-*.md` / 模板（须进 `active/`、`done/`、`specs/`、`templates/`）；**`review_results/`、`reinspect_results/`** 为帽子产出专用子目录，见上节
