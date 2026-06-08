# PROMPT · Kimi Code 串行 Agent 链（Harness Lead · v1）

> **日期**：2026-06-06  
> **性质**：Kimi Code **Lead 主会话**编排真值（Harness 执行器试点 L2）  
> **对照**：Cursor [`PROMPT_cursor_task_chain_serial_v1.md`](PROMPT_cursor_task_chain_serial_v1.md) · Claude [`PROMPT_claude_chain_serial_v1.md`](PROMPT_claude_chain_serial_v1.md)  
> **背景（非 L0）**：[`docs/diary/2026-06-05-plan-agent-analysis/00_README.md`](../../diary/2026-06-05-plan-agent-analysis/00_README.md)

---

## 1. 角色

| 角色 | 承担者 |
| --- | --- |
| **Lead（00）** | Kimi Code **主会话** |
| **各帽** | Kimi `Agent(...)` **串行 spawn** · prompt **内联**帽正文 |
| **人** | 预批 `human_gate`；Lead **禁止**代签 |
| **Git** | **仅 Lead** commit / push / PR（subagent **禁止** git） |

---

## 2. Kimi 与 Cursor/CC 差异（硬）

| 项 | Kimi Code | Cursor / Claude |
| --- | --- | --- |
| 子 Agent 上下文 | **零注入** · 不自动读 `AGENTS.md` / rules | Cursor/CC 较易继承导航 |
| spawn 方式 | `Agent(...)` | `Task(...)` / `.claude/agents/` |
| 每帽 prompt | **必须**重复 canonical + forbidden 全文 | 可较短 |
| git | **Lead 独占** | CC 同约定 · Cursor 父 Agent |

**因此**：实例 PROMPT 各帽 §3 **不可省略**读序/forbidden；禁止假设子 Agent「已知道项目结构」。

---

## 3. 占位符

| 占位符 | 示例 |
| --- | --- |
| `{{TASK}}` | `docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md` |
| `{{ROUND}}` | `T1` |
| `{{SLUG}}` | `kimi-harness-recentsync` |
| `{{GIT_BRANCH}}` | `task/kimi-harness-pilot-recentsync-v1` |
| `{{MERGE_POLICY}}` | `stop_before_merge` |
| `{{RESUME_INVOKE}}` | 续跑 invoke；全新=`无` |

---

## 4. 状态机

```text
SCHEDULE_SCAN → GATE_SCAN → [BLOCKED | ROUND_START]
ROUND_START → FOR each hat:
  WRITE_INVOKE → COMMIT(Lead) → Agent(subagent) → COLLECT → [BLOCKED | next]
→ CLOSE_ROUND → PR → CI → stop（或 merge 若授权）
```

---

## 5. 每帽循环

1. Lead 落盘 `docs/harness/invokes/by-task/{{SLUG}}/invoke_YYYYMMDD_<帽>_{{SLUG}}.md`  
2. **Lead** commit（[`handoff/HANDOFF_AUTO_COMMIT.md`](handoff/HANDOFF_AUTO_COMMIT.md)）  
3. Lead spawn `Agent(...)`，prompt = **本帽 §3 全文**（含 canonical/forbidden/回报格式）  
4. 收 **≤10 行**摘要；**禁止**贴 subagent 全文  

**硬规则**：subagent **不得**再 spawn subagent；subagent **不得** `git commit` / `git push`。

### 5.1 · 30 帽约束（docs-only）

spawn 30 帽时 **须**写入 prompt：

- **禁止** `git log` / `git blame` / 历史考古  
- **禁止** 读 task 范围外路径做背景调研  
- **禁止** `docs/spec/v3-agent/**`、`api/**` 深读  
- docs-only 且 task 已列文件：改完即停；**>10 min** 须停并向 Lead 汇报  

### 5.2 · Git 仅 Lead

- subagent 产出文件由 Lead 审阅后 **Lead** `git add` + `commit`  
- 与 Claude Code [`PROMPT_claude_chain_serial_v1.md`](PROMPT_claude_chain_serial_v1.md) §5.2 同约定  

---

## 6. canonical 读序（所有帽公共前缀 · spawn 时须内联）

```text
1. AGENTS.md（仅 §必读地图 · 不全文考古）
2. docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md（边界段）
3. docs/_tech_graph/00_main.md（架构一览 · 禁止 graph.json 整包）
4. docs/tasks/RECENT_TASK_SCHEDULE.md §1.2
5. {{TASK}}
6. docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md（A 段真值对照）
```

## 7. forbidden（所有帽公共 · spawn 时须内联）

```text
docs/diary/** glob（除非 task 指向）
docs/harness/invokes/by-task/** glob（Lead 写 invoke 除外）
docs/showcase/** · docs/delivery/** · docs/flows/** 全文
docs/spec/v3-agent/** · api/** · tests/** · .github/workflows/**
git log / git blame（30 帽）
```

---

## 8. Round 示例（本试点）

| Round | hats 链 | 实例 PROMPT |
| --- | --- | --- |
| T1 | explore→22→30→40→CLOSE | [`PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md`](PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md) |

---

## 9. §3 Lead 开跑正文（模板）

```text
你 = Harness Lead（Kimi Code · 串行 Agent 链 · Round {{ROUND}}）。遵循：
- docs/harness/prompts/PROMPT_kimi_task_chain_serial_v1.md（本文件）
- docs/harness/prompts/PROMPT_kimi_task_chain_serial_v1_T{{N}}_*.md（实例 · 各帽 §3）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

输入：
- task：{{TASK}}
- slug：{{SLUG}}
- git_branch：{{GIT_BRANCH}}
- merge_policy：{{MERGE_POLICY}}

纪律：
1. GATE_SCAN；pending human_gate → 只报 gate_id，不 spawn
2. 每帽：invoke 落盘 → Lead commit → Agent(本帽§3全文) → 收短报告
3. 禁止 subagent 再 spawn · 禁止 subagent git
4. 禁止代签 human_gate
5. CLOSE 后 PR + CI；stop_before_merge → 报告 PR URL，不 merge

完成后：HANDOFF_CLOSE_TRACE + 建议 diary 落盘路径
```

---

## 10. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1 · Kimi Harness 试点通用模板 · A+B recentsync 实例 |
