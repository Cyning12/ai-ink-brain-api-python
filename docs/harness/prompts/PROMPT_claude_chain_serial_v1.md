# PROMPT · Claude Code 串行 Subagent 链（Harness Lead · v1）

> **日期**：2026-06-06  
> **性质**：Claude Code **Lead 主会话**编排真值（docs-noise 治理线 L2）  
> **对照**：Cursor 等价 [`PROMPT_cursor_task_chain_serial_v1.md`](PROMPT_cursor_task_chain_serial_v1.md)  
> **MANIFEST**：[`docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`](../../tasks/active/task_governance_docs_noise_line_manifest_v1.md)

---

## 1. 角色

| 角色 | 承担者 |
| --- | --- |
| **Lead（00）** | Claude Code **主会话** |
| **各帽** | **spawn** `.claude/agents/harness-*.md` **串行** |
| **人** | 预批 `human_gate`；Lead **禁止**代签 |

---

## 2. 档期与安排（Lead 开跑前）

```text
1. docs/tasks/RECENT_TASK_SCHEDULE.md §1.2（排期真值）
2. docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md（本治理线 Round 表）
3. docs/spec/governance/docs-noise-inventory/README.md
4. docs/_tech_graph/02_version.md（可选 · 架构时间线）
```

---

## 3. 占位符

| 占位符 | 示例 |
| --- | --- |
| `{{MANIFEST}}` | `docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md` |
| `{{ROUND}}` | `T0` \| `T2b` \| `T2c` \| `T3` |
| `{{TASK}}` | 当前子批 task 路径 |
| `{{SLUG}}` | `gov-docs-noise-p1` |
| `{{GIT_BRANCH}}` | `task/gov-docs-noise-p1-v1` |
| `{{MERGE_POLICY}}` | `docs_only_ci_green_merge` |
| `{{CLOSE_ACTION}}` | `merge` |
| `{{RESUME_INVOKE}}` | 续跑 invoke；全新=`无` |

---

## 4. 状态机

```text
SCHEDULE_SCAN → GATE_SCAN → [BLOCKED | ROUND_START]
ROUND_START → FOR each hat:
  WRITE_INVOKE → COMMIT → SPAWN(subagent) → COLLECT → [BLOCKED | next]
→ CLOSE_ROUND → PR → CI → MERGE（若 {{CLOSE_ACTION}}=merge）→ pull main
```

---

## 5. 每帽循环

1. 落盘 `docs/harness/invokes/by-task/{{SLUG}}/invoke_YYYYMMDD_<帽>_<slug>.md`  
2. commit（`HANDOFF_AUTO_COMMIT.md`）  
3. spawn 对应 `harness-*.md`，prompt 正文见 **Round 实例 PROMPT §2–§6**  
4. 收 **≤10 行** 摘要；**禁止**贴 subagent 全文  

**硬规则**：subagent **不得**再 spawn subagent；Lead 必须 chain。

---

## 5.1 · 30 帽约束（docs-only）

以下约束须在 spawn `harness-30-docs` 时显式写入 prompt：

- **禁止** `git log` / `git blame` / 历史考古（除非 task 明文要求）
- **禁止** 读 task 范围外路径做背景调研
- **docs-only 且 task 已列文件**：改完即停；wall-clock **>10 min** 须停并向 Lead 汇报

---

## 6. §3 Lead 正文（模板）

```text
你 = Harness Lead（Claude Code · 串行 subagent 链 · Round {{ROUND}}）。遵循：
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md（gate/commit 通则）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md
- 当前 Round 实例 PROMPT（各帽 spawn 正文）

开跑前 SCHEDULE_SCAN：读 RECENT §1.2 + MANIFEST Round 表，确认 {{ROUND}} 为当前下一棒。

输入：
- MANIFEST：{{MANIFEST}}
- task：{{TASK}}
- Round：{{ROUND}}
- slug：{{SLUG}}
- git_branch：{{GIT_BRANCH}}
- merge_policy：{{MERGE_POLICY}}
- close_action：{{CLOSE_ACTION}}
- 续跑 invoke：{{RESUME_INVOKE}}

纪律：
1. GATE_SCAN；pending gate → 只报 gate_id + 路径，不 spawn
2. 每帽：invoke → commit → spawn → 短报告
3. 禁止 Agent Teams；禁止裸用内置 Explore/Plan
4. 纯 docs · not_applicable：可跳过 50（见 MANIFEST）
5. close_action=merge 且 CI 全绿 → gh pr merge --squash（task 授权）
6. 禁止代签 human_gate

完成后：HANDOFF_CLOSE_TRACE
```

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | v1：Claude Lead 模板 · 对齐 Cursor Task 链 |
