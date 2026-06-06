# PROMPT · Cursor 串行 Task 链（Harness 00 总调度 · v1）

> **日期**：2026-06-06  
> **性质**：本仓 Harness **试点** Prompt 真值（docs-noise 治理线 L1）  
> **用途**：Cursor **父 Agent** 串行 `Task(subagent_type=…)` · Round T0–T3  
> **实例（已填占位符）**：[`PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md`](PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md)  
> **分析背景（非 L0）**：`tmp/diary/2026-06-06-agent-orchestration-analysis/`

---

## 1. 角色

| 角色 | 承担者 |
| --- | --- |
| **00 总调度** | Cursor **父 Agent**（主 Chat） |
| **各帽执行** | `Task(subagent_type=…)` **串行** |
| **人** | 预批 `HG-GOV-*` / `HG-TASK-DRAFT`；00 **禁止**代签 |

---

## 2. 占位符

| 占位符 | 含义 | 示例 |
| --- | --- | --- |
| `{{MOTHER_TASK}}` | 母 task 或本轮 task 路径 | `docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md` |
| `{{ROUND}}` | 轮次 | `T0` \| `T1` \| `T2b` \| `T2c` \| `T3` \| `ALL` |
| `{{SLUG}}` | invoke 目录 slug | `gov-docs-noise-p0` |
| `{{GIT_BRANCH}}` | 任务分支 | `task/gov-docs-noise-p0-v1` |
| `{{MERGE_POLICY}}` | 合并策略 | `docs_only_ci_green_merge` \| `stop_before_merge` |
| `{{RESUME_INVOKE}}` | 续跑 invoke；全新=`无` | `docs/harness/invokes/by-task/gov-docs-noise-p0/invoke_…` |

---

## 3. 状态机

```text
INIT → GATE_SCAN → [BLOCKED | ROUND_START]
ROUND_START → FOR each hat:
  WRITE_INVOKE → COMMIT → TASK → COLLECT → [BLOCKED | next hat]
→ CLOSE_ROUND → PR → CI → [BLOCKED | MERGE] → pull main → NEXT_ROUND
→ META_CLOSE → CLOSE_TRACE → END
```

---

## 4. GATE_SCAN（每 round 开干前）

1. 读 `{{MOTHER_TASK}}` + 本子 task 的 `human_gate` 表  
2. 任一 gate `pending` 且 `blocks_hats` 含本 round 计划帽 → **BLOCKED**（只报 gate_id + 路径）  
3. 预批全部 `approved` → 继续  

---

## 5. 每帽循环

### 5.1 WRITE_INVOKE

落盘：`docs/harness/invokes/by-task/{{SLUG}}/invoke_YYYYMMDD_<帽号>_{{SLUG}}.md`

元信息表：`round` · `hat` · `git_branch` · `read_paths` · `forbidden`

### 5.2 COMMIT

按 [`handoff/HANDOFF_AUTO_COMMIT.md`](handoff/HANDOFF_AUTO_COMMIT.md)；仅 add 本轮路径。

### 5.3 TASK（串行 · 禁止子 Task 再派 Task）

父 Agent 调用 `Task` 时，子 prompt **须**注入 canonical 读序 + forbidden + 回报格式。各帽 §3 正文见 **实例文件** 或对应 `TEMPLATE-*-invoke.md`。

```text
Task(
  description="<帽短名>",
  subagent_type="explore|generalPurpose|shell",
  prompt="""
  【角色】Harness <帽> · 上一帽已结束；只执行下文。

  【canonical 读序】
  docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md
  docs/_tech_graph/00_main.md
  docs/spec/governance/docs-noise-inventory/README.md
  {{当前 task 路径}}

  【forbidden】
  docs/diary/** · docs/harness/invokes/** glob · docs/showcase/**
  docs/delivery/** · docs/flows/** · docs/spec/v3-agent/**
  api/ 巨型源码全文（除非 task 指向）

  【交付物】
  <本帽路径>

  【正文】
  <本帽 §3 已替换占位符 · 见实例 PROMPT_*_T1_*.md>

  【回报格式 · 硬】
  Status / Deliverables / Blockers / Judgment（各≤10行）
  """
)
```

### 5.4 COLLECT

- 校验交付物存在  
- **禁止**贴子 Task 全文  
- Blockers 非空 → BLOCKED  
- 记 KPI HatInstance 一行（若 task 要求）

---

## 6. Round 示例（docs-noise）

| Round | hats 链 | PR |
| --- | --- | --- |
| T0 | 10（父会话或 Task） | 母+子 task 草案 |
| T1 | explore→22→30→40→CLOSE | P0 C1–C3 |
| T2b | 22→30→40→CLOSE | P1 archived |
| T2c | 22→30→40→CLOSE | P2 读序 |
| T3 | CLOSE + META | 母单 done |

---

## 7. PR 管道（仅父 Agent）

```text
CLOSE_ROUND:
  git mv · _views/done.md · 冲突寄存器 C* → done
  invoke CLOSE + commit

PR:
  git push -u origin HEAD
  gh pr create

CI:
  gh pr checks --watch（Required 全绿）

MERGE（须 {{MERGE_POLICY}} + task 授权）:
  gh pr merge --squash
  git checkout main && git pull origin main

NEXT:
  若 ROUND=ALL 且还有 round → ROUND_START
  否则 META + HANDOFF_CLOSE_TRACE
```

---

## 8. §3 可复制 Prompt 正文（父 Agent · 模板）

```text
你 = Harness 00 总调度（Cursor · 串行 Task 链）。遵循：
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/spec/governance/docs-noise-inventory/README.md
- docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md（本文件 · 状态机）

输入：
- task：{{MOTHER_TASK}}
- Round：{{ROUND}}
- slug：{{SLUG}}
- git_branch：{{GIT_BRANCH}}
- merge_policy：{{MERGE_POLICY}}
- 续跑 invoke：{{RESUME_INVOKE}}

纪律：
1. 开干 GATE_SCAN；pending → 只报 gate_id，不 Task
2. 每帽：invoke → commit → Task（串行）→ 收短报告
3. 禁止子 Task 再派 Task；禁止贴子 Task 全文
4. 每 round 单分支单 PR；merge 后 pull main 再下一 round
5. ROUND=ALL 时串行 T0→T3；遇 CI 红 BLOCKED
6. 禁止代签 human_gate

各帽 Task §3 正文：读实例 PROMPT_*_T{{N}}_*.md 对应节，或 TEMPLATE-*-invoke.md。

若 {{RESUME_INVOKE}} 非「无」：读该 invoke §3，从标注阶段继续，不重复已完成帽。

完成后：HANDOFF_CLOSE_TRACE + Harness 状态栏 B
```

---

## 9. 与 semi_auto 换帽对比

| | semi_auto 同会话换帽 | 本 Prompt |
| --- | --- | --- |
| context | 历史叠加 | 子 Task 隔离 |
| 真值 | invoke | invoke（同） |
| 父 context | 单会话涨 | 仍涨 → **建议每 round 新会话** |

---

## 10. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1 草案（tmp/diary） |
| 2026-06-06 | v1 冻结迁入 `docs/harness/prompts/`；增 T1 实例指针 |
