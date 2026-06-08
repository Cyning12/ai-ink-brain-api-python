# PROMPT · Cursor 串行 Task 链（Harness 00 总调度 · v1）

> **日期**：2026-06-08  
> **性质**：工作区 Harness **链式常模** Prompt 真值（Open **`Projects/`**）  
> **用途**：Cursor **父 Agent** 串行 `Task(subagent_type=…)` · 单 task 或 Epic Round  
> **对照**：后端 Claude/Kimi 链见 `ai-ink-brain-api-python/docs/harness/prompts/PROMPT_*_chain_serial_*`  
> **编排指南**：[`../guides/GUIDANCE_epic_orchestration_task_chain_v1_zh.md`](../guides/GUIDANCE_epic_orchestration_task_chain_v1_zh.md)

---

## 1. 角色

| 角色 | 承担者 |
| --- | --- |
| **00 总调度** | Cursor **父 Agent**（主 Chat） |
| **各帽执行** | `Task(subagent_type=…)` **串行** |
| **人** | 预批 `human_gate`；00 **禁止**代签 |

---

## 2. 占位符

| 占位符 | 含义 | 示例 |
| --- | --- | --- |
| `{{TASK_PATH}}` | 主 task 路径（相对 `Projects/`） | `docs/harness/tasks/active/task_*.md` 或 `ai-ink-brain-api-python/docs/tasks/active/task_*.md` |
| `{{ROUND}}` | 轮次（Epic 可选） | `T1` \| `ALL` \| `—` |
| `{{SLUG}}` | invoke 目录 slug | `harness-frontend-p1-4-parity` |
| `{{GIT_BRANCH}}` | 任务分支 | `task/<slug>` |
| `{{PLANNED_HATS}}` | 本 round 帽序列 | `22,30,40,50,CLOSE` |
| `{{MERGE_POLICY}}` | 合并策略 | `ci_green_merge` \| `stop_before_merge` \| `docs_only_ci_green_merge` |
| `{{RESUME_INVOKE}}` | 续跑 invoke；全新=`无` | `docs/harness/invokes/by-task/<slug>/invoke_*.md` |

---

## 3. 状态机

```text
INIT → GATE_SCAN → [BLOCKED | ROUND_START]
ROUND_START → FOR each hat in PLANNED_HATS:
  WRITE_INVOKE → COMMIT → TASK → COLLECT → [BLOCKED | next hat]
→ CLOSE_ROUND → PR → CI → [BLOCKED | MERGE] → HANDOFF_CLOSE_TRACE → END
```

---

## 4. GATE_SCAN（每 round 开干前）

1. 读 `{{TASK_PATH}}` 的 `human_gate` 表 + `orchestration` 字段  
2. 任一 gate `pending` 且 `blocks_hats` 含本 round 计划帽 → **BLOCKED**（只报 gate_id + 路径）  
3. 全部相关 `approved` → 继续  
4. **`semi_auto: true` 不再作为开跑依据**（deprecated）；缺 `orchestration` / 链 PROMPT 路径 → BLOCKED

---

## 5. 每帽循环

### 5.1 WRITE_INVOKE

落盘路径（二选一，与 task 所属 git 根一致）：

- 工作区 task：`Projects/docs/harness/invokes/by-task/{{SLUG}}/invoke_YYYYMMDD_<帽号>_{{SLUG}}.md`
- 子仓 task：`<子仓>/docs/harness/invokes/by-task/{{SLUG}}/invoke_*.md`

元信息表：`round` · `hat` · `git_branch` · `worktree_root`（可选）· `read_paths` · `forbidden`

### 5.2 COMMIT

按 [`handoff/HANDOFF_AUTO_COMMIT.md`](handoff/HANDOFF_AUTO_COMMIT.md)；仅 add 本轮路径；**禁止** `git add -A`。

### 5.3 TASK（串行 · 禁止子 Task 再派 Task）

父 Agent 调用 `Task` 时，子 prompt **须**注入 canonical 读序 + forbidden + 回报格式。各帽 §3 正文见对应 `TEMPLATE-*-invoke.md` 或 task 绑定的实例 PROMPT。

```text
Task(
  description="<帽短名>",
  subagent_type="explore|generalPurpose|shell",
  prompt="""
  【角色】Harness <帽> · 上一帽已结束；只执行下文。

  【canonical 读序】
  <task 必读列表 · 相对 Projects/>
  {{TASK_PATH}}
  docs/harness/HARNESS_V2_PLAN.md §5

  【forbidden】
  未在 task 范围列出的子仓 · 静默扩 scope · 代签 human_gate

  【交付物】
  <本帽路径>

  【正文】
  <本帽 TEMPLATE-*-invoke.md §3 · 占位符已替换>

  【回报格式 · 硬】
  Status / Deliverables / Blockers / Judgment（各≤10行）
  """
)
```

### 5.4 COLLECT

- 校验交付物存在  
- **禁止**贴子 Task 全文  
- Blockers 非空 → BLOCKED  
- 记 KPI HatInstance 一行（若 task `kpi_aggregator: 00`）

---

## 6. 帽链常模

| test_strategy | 默认帽链 |
| --- | --- |
| `required` | explore（可选）→ 22 → 30 → 40 → 50 → CLOSE → PR → CI → merge |
| `not_applicable` | explore（可选）→ 22 → 30 → 40 → CLOSE → PR → CI → merge（跳过 50 · task 明示） |

---

## 7. PR 管道（仅父 Agent）

```text
CLOSE_ROUND:
  更新 task 状态 / _views（按 task README）
  invoke CLOSE + commit（子仓或工作区各自 git 根）

PR:
  git push -u origin HEAD
  gh pr create

CI:
  gh pr checks --watch（Required 全绿）

MERGE（须 {{MERGE_POLICY}} + task 授权）:
  gh pr merge --squash
  git checkout main && git pull origin main
```

---

## 8. §3 可复制 Prompt 正文（父 Agent · 模板）

```text
你 = Harness 00 总调度（Cursor · 串行 Task 链）。遵循：
- docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md（本文件 · 状态机）
- docs/harness/guides/GUIDANCE_epic_orchestration_task_chain_v1_zh.md
- docs/harness/prompts/00-orchestrator.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5.6（orchestration · human_gate）

输入：
- task：{{TASK_PATH}}
- Round：{{ROUND}}
- slug：{{SLUG}}
- planned_hats：{{PLANNED_HATS}}
- git_branch：{{GIT_BRANCH}}
- merge_policy：{{MERGE_POLICY}}
- 续跑 invoke：{{RESUME_INVOKE}}

纪律：
1. 开干 GATE_SCAN；pending → 只报 gate_id，不 Task
2. 每帽：invoke → commit → Task（串行）→ 收短报告
3. 禁止子 Task 再派 Task；禁止贴子 Task 全文
4. 建议每 task 一分支；禁止在 main 上链式连续提交
5. 遇 CI 红 BLOCKED
6. 禁止代签 human_gate；禁止以 semi_auto: true 代替本 Prompt

各帽 Task §3 正文：读 task 绑定的 PROMPT_*_T*_*.md，或 docs/harness/prompts/TEMPLATE-*-invoke.md §3。

若 {{RESUME_INVOKE}} 非「无」：读该 invoke §3，从标注阶段继续，不重复已完成帽。

完成后：HANDOFF_CLOSE_TRACE + Harness 状态栏 B（见 handoff/HANDOFF_CLOSE_TRACE.md）
```

---

## 9. 与 `semi_auto` 同会话换帽对比（历史）

| | `semi_auto`（**deprecated**） | 本 Prompt |
| --- | --- | --- |
| context | 历史叠加 | 子 Task 隔离 |
| 真值 | invoke | invoke（同） |
| 总闸 | task 字段 `semi_auto: true` | 本 PROMPT + `orchestration` |
| 父 context | 单会话涨 | 仍涨 → **建议每 round 新会话** |

---

## 10. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | v1：工作区迁入；替代 `semi_auto` 总闸；链 GUIDANCE + 00 |
