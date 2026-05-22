# Harness 评价与改进草案 — 回复与裁决（2026-05-22）

> **性质**：对流程评价修正版、改进设计草案的**正式回复**；供后续实现与闭环验收对照。  
> **时效**：强；实现落地后本节「待办」可能作废，真值以 `docs/harness/`、`docs/tasks/` 为准。  
> **来源文稿**：  
> - `docs/diary/tmp/2026-05-22-harness-flow-evaluation-corrected.md`  
> - `docs/diary/tmp/2026-05-22-harness-improvement-designs.md`  
> **仓库锚点**：提交 `d48845d`（`docs(harness): 内嵌最小 Harness，恢复 22/50 落盘约定`）

---

## 一、总裁决（一句话）

| 类别 | 裁决 |
|------|------|
| **评价修正版（诊断）** | **接受** — 初版「子仓零落地」为范围错误；核心矛盾改为「工作区已闭环、子仓有意重置后待新产出」。 |
| **评价修正版（六条建议）** | **部分接受** — 按子仓自治与 `06-harness-in-repo` 裁剪，不 bulk 迁入、不软链双真源。 |
| **改进设计草案（§一～§三）** | **接受为 P0/P1 规格** — 非一次性全做；与现有 `10`/`HANDOFF_*` 对齐。 |
| **三条最关键建议** | **均接受意图**；#1 改迁移手段，#2 先落 task 再验闭环，#3 与草案一致。 |

---

## 二、对《流程评价修正版》的回复

### 2.1 诊断与评分 — 接受及原因

| 评价结论 | 是否接受 | 原因 |
|----------|:--------:|------|
| 工作区根 `docs/harness/` 已有 reviews/invokes 闭环 | ✅ | 抽样 R2、invoke 30 与 `22-task-audit.md` 一致，证据充分。 |
| 初版「设计完美、落地为零」不成立 | ✅ | 审计范围仅限子仓导致误判。 |
| 核心矛盾：集中治理 vs 子仓自治；双份 prompts；pointer 悬空 | ✅ | 与 `d48845d` 后子仓 `reviews/` 仅 README、工作区 pointer 仍链子仓已删路径一致。 |
| Agent 成本已被 `05`/`06` 压低，人侧仍是瓶颈 | ✅ | 与 `human_gate` 仅人可 `approved`、`10` 双路径人择一一致。 |
| 子仓空壳可能含「组织习惯」因素 | ✅ | 技术路径（本仓 prompts + rules）已就绪，缺的是新 task 首份落盘与习惯切换。 |

**须补充的真值（评价稿未写清）**

- `d48845d` 后子仓 `docs/harness/reviews/` **有意清空**历史混放全文，invoke 已迁至 `docs/diary/harness-archive/`；**不是**单纯「迁移未完成」，而是 **为子仓专用 22 目录重建**。
- 历史 review 全文仍可从 **`d48845d` 父提交** 的 git 历史恢复，不必仅从工作区 pointer 复制。

### 2.2 评价稿六条建议 — 逐条裁决

| 建议 | 裁决 | 原因 |
|------|:----:|------|
| **1 子仓自治 + pointer 全文迁子仓** | **部分接受** | **接受**边界表（本仓 22→`docs/harness/reviews/`，50→`reinspect_results/`，跨仓不留正文）。**不接受**把工作区/前端/ChatBI 审查 bulk 进后端仓；**不接受**从已悬空 pointer 盲拷。恢复手段：`git show d48845d^:docs/harness/reviews/<file>` 或 worktree 真值，且仅 `docs/tasks/` 绑定本仓的条目。 |
| **2 文档单一真源（软链）** | **部分接受** | **接受**「每仓 Agent 只读本仓 prompts」— 已由 `d48845d` 内嵌实现。**不接受**子仓 prompts 软链工作区（Git/多机易碎）。`docs/harness/README.md` §4 `rsync` 保留为**维护者偶发同步**，非 Agent 日常路径。 |
| **3 总 Agent 不串行扛多子仓 Harness** | ✅ | 组织/会话策略，与文档无冲突，降低并行 worktree 认知负荷。 |
| **4 子仓跑通完整 Harness 闭环** | ✅ **P0** | 验证 `06`/`reviews/README` 是否真落地的**唯一硬验收**；优先于大规模历史迁移。 |
| **5 README 链工作区历史样例** | **部分接受** | **不接受** Agent 默认读 `Projects/docs/harness/`（违反 `06-harness-in-repo`）。**接受**在 `docs/diary/harness-archive/` 或 `reviews/README` 标注「历史样例（非必读）」；首份新 R1 落盘后以本仓产出为准。 |
| **6 降低人侧成本** | **部分接受** | 见 **第四节** 与改进草案；**不接受**用「默认推荐」替代人择 A/B 或代填 `human_gate`。 |

---

## 三、对《改进设计草案》的回复

### 3.1 §一 Task 生成（模板骨架 + SKILL 蒸馏）

| 设计点 | 裁决 | 原因 |
|--------|:----:|------|
| 分层：模板骨架 + SKILL 预填 | ✅ P0/P1 | 解决 `HARNESS_V2` §5 字段填写率低；与现有 `docs/tasks/templates/TASK_TEMPLATE.md` 扩展一致。 |
| `docs/tasks/templates/` + `docs/tasks/skills/` 落点 | ✅ | `docs/tasks/README.md` 已有 `templates/`，skills 为增量目录。 |
| 6 类 SKILL 初版 | ✅ P1 | 类型与后端仓任务匹配；`harness-task` 应对齐 `audit_profile: full`。 |
| CLI 生成脚本 | ⏳ P1 | 非阻塞；可先 `cp` 模板 + 手工改字段。 |
| 关账后蒸馏 + **人审后合并** | ✅ | 避免过拟合历史 task；符合 Harness 人闸精神。 |

### 3.2 §二 Harness 状态栏

| 设计点 | 裁决 | 原因 |
|--------|:----:|------|
| 版本 **B**（结构化多行）为对话默认 | ✅ P0 | 与 Execution Report 习惯一致，可读性优于单行 A。 |
| 版本 C 表格写入 invoke/review | ✅ P0 | 利于跨会话锚点，与 invoke 快照职能一致。 |
| 与 `HANDOFF_CLOSE_TRACE` 分工 | ✅ | 状态栏=会话内「现在在哪」；CLOSE_TRACE=关账全链路，互补不替代。 |
| 落盘位置 | ✅ P0 | 建议写入 `HANDOFF_SEMI_AUTO.md` §3.2 后「每棒结束须输出状态栏」；规则层可选同步 `05-harness-semi-auto.mdc` 一句。 |

### 3.3 §三 A/B 路径默认推荐

| 设计点 | 裁决 | 原因 |
|--------|:----:|------|
| 仍输出 A、B **全文**两条 Prompt | ✅ **硬** | 与 `10-requirements.md`、`TEMPLATE-requirements-invoke` §3 一致。 |
| 标题加 `（推荐）` + 推荐理由 | ✅ P0 | 降低人认知，不剥夺决策权。 |
| 推荐规则表 + 冲突处理 | ✅ | `audit_profile` 显式声明优先于启发式；`test_strategy: required` 次优先，合理。 |
| 「紧急 bug → B」 | ⚠️ 附条件 | 接受速度优先，但 task 须写明 **事后补 22** 或 **post_close 闸 2**，避免永久跳过审查。 |
| Agent 因推荐自动走路径 | ❌ | 与 `human_gate`、人择一冲突；仅标注，不自动执行下一帽。 |

---

## 四、三条「最关键建议」— 专项 QA（含原因）

### 4.1 立即迁移：工作区 pointer 全文 → 子仓 `docs/harness/reviews/`

| 项 | 内容 |
|----|------|
| **意图** | ✅ 接受 — 消除悬空 pointer，子仓 Agent 有可读历史样例。 |
| **手段** | ❌ 不接受「从工作区 pointer 一键 bulk 迁」 — 大量链已断（`d48845d` 删树）；部分链 **worktree** 路径（如 `ai-ink-brain-api-python-wt-gate-d-v2`）。 |
| **定稿做法** | ① 仅 **绑定** `docs/tasks/**` 本仓的 `task_*_audit_*.md`；② 优先 `git show d48845d^:docs/harness/reviews/<file>` 恢复；③ 工作区改 **索引一行** 或删悬空 pointer，**不**保留双份正文；④ P1 按需恢复 1～2 份样例即可，**不阻塞** P0 闭环。 |

### 4.2 验证闭环：`task_05_query_rewrite_observability` 子仓 10→关账

| 项 | 内容 |
|----|------|
| **意图** | ✅ 接受 — 里程碑验收，产出子仓 **第一份新** `reviews/task_*_audit_R1_*.md`。 |
| **阻塞** | 本仓 **尚无** 该 task 文件（评价稿为排期名，非现成 `active/` 任务）。 |
| **定稿做法** | ① 先在 `docs/tasks/active/` 落盘 task（可扩 `TASK_TEMPLATE` + 可选 `SKILL-api-endpoint`）；② 分支 `task/<slug>`，禁止在 `main` 链式 commit；③ 试跑 §三推荐 + §二状态栏；④ 关账须含 `reinspect_results/` + `human_gate` approved + CI。 |
| **备选** | 若 `task_05` 范围过大，可先用更小 `docs-governance` task 验流程，再大 task。 |

### 4.3 降低人侧成本：模板脚本、A/B 推荐、状态栏

| 项 | 内容 |
|----|------|
| **意图** | ✅ 接受 — 瓶颈在人，非 Agent。 |
| **定稿** | P0：扩展 `TASK_TEMPLATE` Harness 字段 + §三推荐标注 + §二状态栏写入 HANDOFF；P1：CLI、`skills/`、关账蒸馏。 |
| **不做** | 推荐替代人择；脚本自动生成 `approved`。 |

---

## 五、推荐执行顺序（P0 / P1）

```text
P0（闭环优先）
  1. 扩展 docs/tasks/templates/TASK_TEMPLATE.md（semi_auto、human_gate、audit_profile、test_strategy、failure_paths）
  2. 新建/确认 task_05（或等价小 task）+ 分支 task/<slug>
  3. HANDOFF_SEMI_AUTO：增补「每棒状态栏（版本 B）」；10 帽试跑双 Prompt +（推荐）+ 理由
  4. 跑通 10 → 22(R1) → 30 → 40 → 50 → CLOSE_TRACE → 子仓 reviews/ 首份新产出

P1（闭环通过后）
  5. git 恢复 d48845d^ 中后端绑定 review → docs/harness/reviews/（按需，非 bulk）
  6. 工作区 Projects/docs/harness/reviews/：pointer 改索引或删悬空
  7. docs/tasks/skills/ + 关账蒸馏流程（人审合并）
  8. 可选：task 生成 CLI
```

---

## 六、明确不做项（原因摘要）

| 不做 | 原因 |
|------|------|
| 前端/工作区 harness task 审查全文进后端 `reviews/` | 违反子仓边界；`reviews/README.md` 已禁止混放。 |
| 子仓 prompts 软链工作区 | 易碎；Agent 已以本仓为真源（`06`）。 |
| 评价稿「全部接受」六条建议字面执行 | #1/#2/#5/#6 需裁剪；与 `d48845d` 策略冲突。 |
| Agent 按推荐自动走 A 或 B | 破坏人择一与 `human_gate` 硬规则。 |
| 在 `main` 上 semi_auto 多帽链式提交 | `HANDOFF_SEMI_AUTO` §5 强烈建议 task 分支。 |

---

## 七、后续落盘真值（实现后应更新处）

| 位置 | 更新时机 |
|------|----------|
| `docs/harness/prompts/HANDOFF_SEMI_AUTO.md` | P0：状态栏 + 与改进草案交叉引用 |
| `docs/tasks/templates/TASK_TEMPLATE.md` | P0：Harness 元信息块 |
| `docs/harness/reviews/README.md` | 首份新 R1 后：增加「本仓已产出示例」链接 |
| `docs/harness/README.md` §4 | 标明 rsync 为维护者可选，非 Agent 路径 |
| `docs/tasks/README.md` | P1：`human_gate` 场景速查表 |

---

## 八、修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：评价修正版 + 改进草案 + 三关键建议 QA 合并回复 |

---

## 给 Cursor

`Harness`、`评价回复`、`改进草案`、`d48845d`、`子仓 reviews`、`task_05`、`pointer 迁移`、`A/B 推荐`、`状态栏`、`P0 P1`
