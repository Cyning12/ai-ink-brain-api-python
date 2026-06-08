# COMPARISON · Kimi Code vs Claude Code · 串行 Harness Prompt 对照（v1）

> **日期**：2026-06-08  
> **性质**：执行器 Prompt **写法对照** · 非 L0 架构真值  
> **试点留证**：Kimi T1 [`PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md`](PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md) · PR [#134](https://github.com/Cyning12/ai-ink-brain-api-python/pull/134) · diary [`2026-06-08-kimi-harness-pilot-recentsync_zh.md`](../../diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md)  
> **Claude 基准**：[`PROMPT_claude_chain_serial_v1.md`](PROMPT_claude_chain_serial_v1.md) · T2b 实例 [`PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`](PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md)  
> **Plan Agent 背景**：[`docs/diary/2026-06-05-plan-agent-analysis/00_README.md`](../../diary/2026-06-05-plan-agent-analysis/00_README.md)

---

## 0. 一句话

| 执行器 | Prompt 形态 |
| --- | --- |
| **Kimi Code（KC）** | Lead 手册 + **每帽完整子 Prompt**（内联 canonical/forbidden · 防零上下文） |
| **Claude Code（CC）** | Lead 手册 + **spawn 指针** + **薄业务补充**（读序在 `.claude/agents/harness-*`） |

同一 T1 业务，CC 实例篇幅约为 KC 的 **1/3～1/2**；状态机、帽链、Git 仅 Lead、30 帽 §5.1 约束 **一致**。

---

## 1. 文件与角色对照

| KC（现有） | CC（等价形态） |
| --- | --- |
| [`PROMPT_kimi_task_chain_serial_v1.md`](PROMPT_kimi_task_chain_serial_v1.md) | [`PROMPT_claude_chain_serial_v1.md`](PROMPT_claude_chain_serial_v1.md) |
| [`PROMPT_kimi_*_T1_recentsync_zh.md`](PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md) | **待写** `PROMPT_claude_chain_serial_v1_T1_recentsync_zh.md`（业务同构 · 写法变薄） |
| Kimi `Agent(§3 全文)` | `spawn` [`.claude/agents/harness-*.md`](../../.claude/agents/README.md) |
| 每帽内联 canonical + forbidden（~35–50 行） | agent 文件 + 实例 **5～15 行**补充 |

---

## 2. 核心机制差异

| 维度 | Kimi Code | Claude Code |
| --- | --- | --- |
| 子 Agent 上下文 | **零注入** · 不自动读 `AGENTS.md` / rules | 较易沿 `CLAUDE.md` → `AGENTS.md` 导航 |
| spawn 语法 | `Agent(...)` | `spawn harness-explore-l0` 等 |
| 每帽 prompt 厚度 | **必须**重复读序/forbidden | 读序在 agent 定义 · 实例只写业务 delta |
| Git | **仅 Lead** commit/push/PR | **同约定** · [§5.2](PROMPT_claude_chain_serial_v1.md) + `.claude/settings.json` |
| 30 帽约束 | 内联 §5.1 全文 | spawn 时 **一句**引用 §5.1 或 agent 内已有 |

---

## 3. 通用模板层对照

| 章节 | KC `PROMPT_kimi_*` | CC `PROMPT_claude_*` |
| --- | --- | --- |
| §2 零上下文 / 档期 | KC 专节「与 Cursor/CC 差异」 | CC §2 档期（MANIFEST / RECENT） |
| §6 canonical 公共读序 | ✅ · **每帽须内联** | ❌ · 在 `.claude/agents/` |
| §7 forbidden 公共块 | ✅ · **每帽须内联** | ❌ · agent + task 非范围 |
| §5.2 Git 仅 Lead | 简表 | **详表**（settings 白名单 · subagent 可 rg/pytest） |
| Lead §3 模板 | `Agent(本帽§3全文)` | `spawn harness-*.md` + 实例 §3 |

---

## 4. Lead 开跑 Prompt 对照（T1 recentsync 同业务）

### 4.1 Kimi Code（现稿 §1 要点）

```text
你 = Harness Lead（Kimi Code · 串行 Agent 链 · Round T1）…

纪律：
1. GATE_SCAN …
2. 各帽 Agent prompt 必须使用本文件对应节 **全文**（含 canonical/forbidden）
3. 禁止 subagent 再 spawn · 禁止 subagent 任何 git 命令
4. test_strategy=not_applicable：40 不跑 pytest
5. CLOSE 后 gh pr create … stop_before_merge
```

### 4.2 Claude Code（等价写法）

```text
你 = Harness Lead（Claude Code · 串行 subagent 链 · Round T1）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_recentsync_zh.md（§2–§6）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/done/task_governance_kimi_harness_pilot_recentsync_v1.md

输入：
- task：docs/tasks/done/task_governance_kimi_harness_pilot_recentsync_v1.md
- slug：kimi-harness-recentsync
- git_branch：task/kimi-harness-pilot-recentsync-v1
- merge_policy：stop_before_merge

Round T1：explore → 22 → 30 → 40 → CLOSE → PR → CI

纪律：
1. GATE_SCAN；pending → 只报 gate_id
2. 每帽：invoke 落盘 → Lead commit → spawn `.claude/agents/harness-*.md`（正文见实例 §3）
3. subagent 禁止再 spawn · 禁止 subagent git commit（§5.2）
4. 禁止代签 human_gate
```

**差别**：CC Lead **不要求**每帽贴 KC §6/§7 公共块；读序由 agent + Lead 会话上下文承担。

---

## 5. 各帽 spawn 对照

### 5.1 explore

**KC**（[`T1_recentsync §2`](PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md) · ~35 行）：

```text
【canonical 读序 · 必须按序打开】
1. AGENTS.md §必读
2. docs/_tech_graph/00_main.md
3. docs/tasks/RECENT_TASK_SCHEDULE.md §1.2 全文
4. docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md §子批状态
5. docs/tasks/.../task_governance_kimi_harness_pilot_recentsync_v1.md §范围 A/B

【forbidden】
docs/spec/v3-agent/** · api/** · tests/** · git log · git blame …

【不要】 commit（Lead 负责）
```

**CC（等价 · ~8 行）**：

```text
spawn harness-explore-l0.md，prompt 追加：

【task】docs/tasks/done/task_governance_kimi_harness_pilot_recentsync_v1.md §A/B
【交付】docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md
【须核对】RECENT §1.2 vs MANIFEST；5 个 gov-docs-noise done 状态行；rg 扫描 done/ 候选 ≤15
【禁止】改 RECENT/done 正文 · git commit
【回报】≤10 行
```

canonical/forbidden 见 [`.claude/agents/harness-explore-l0.md`](../../.claude/agents/harness-explore-l0.md)。

---

### 5.2 22 · 30 · 40

| 帽 | KC | CC（等价） |
| --- | --- | --- |
| **22** | 内联 `22-task-audit` 读序 + explore 路径 + forbidden | `spawn harness-22-audit` + `【输入】task + explore 差分` + 可选 `harness_task_validate` |
| **30** | 内联 A/B 交付 + forbidden +「不要 commit」 | `spawn harness-30-docs` + `【交付】RECENT §1.2 + B-2 五文件` + §5.1 一句 |
| **40** | 内联 `rg` 验证 + 验收勾选 | `spawn harness-40-check` + 验证命令 + 建议 CLOSE |

**CC 30 帽示例（recentsync 同业务）**：

```text
spawn harness-30-docs.md：

【角色】Harness 30 · recentsync A+B
【交付】
- A：docs/tasks/RECENT_TASK_SCHEDULE.md §1.2（MANIFEST→done/、P0–P3、CLOSE）
- B-2：5 个 gov-docs-noise done task 状态行统一
【禁止】>10 个 done 文件 · api/ · git commit（Lead commit）
【回填】task ### 自检结论
【回报】≤10 行
```

参考现成 CC 薄写法：[`PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`](PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md) §2–§5。

---

## 6. 若把 KC 实例原样给 CC

| 做法 | 结果 |
| --- | --- |
| **原样粘贴 KC §2–§5 给 CC spawn** | 能跑 · **冗余**（与 agent 重复） |
| **推荐：CC 惯例改写** | 新建 `PROMPT_claude_chain_serial_v1_T1_*` · 每帽 5～15 行 |
| **Plan Agent 导航复验** | KC：[`PROMPT_kimi_plan_agent_nav_revalidation_zh.md`](PROMPT_kimi_plan_agent_nav_revalidation_zh.md) · CC 可 spawn 通用 agent + 同段 forbidden · 不必单独 Kimi 文件 |

---

## 7. 三执行器 Prompt 索引（本仓）

| 执行器 | 通用模板 | 试点实例 | 关账留证 |
| --- | --- | --- | --- |
| **Cursor** | [`PROMPT_cursor_task_chain_serial_v1.md`](PROMPT_cursor_task_chain_serial_v1.md) | T1 gov-docs-noise P0 | diary `2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md` |
| **Claude Code** | [`PROMPT_claude_chain_serial_v1.md`](PROMPT_claude_chain_serial_v1.md) | T0/T2b/c/d docs-noise | MANIFEST · PR #123–#129 |
| **Kimi Code** | [`PROMPT_kimi_task_chain_serial_v1.md`](PROMPT_kimi_task_chain_serial_v1.md) | [`T1_recentsync`](PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md) | diary [`2026-06-08-kimi-harness-pilot-recentsync_zh.md`](../../diary/2026-06-08-kimi-harness-pilot-recentsync_zh.md) |

---

## 8. 改写 checklist（KC task → CC 实例）

开写 `PROMPT_claude_chain_serial_v1_T{round}_*.md` 时：

- [ ] Lead §1：spawn 语法改 `.claude/agents/harness-*` · 删「Agent 全文内联」纪律
- [ ] explore：删 §6/§7 重复块 · 保留【task】【交付】【须核对】【回报】
- [ ] 22/30/40：对齐 T2b 薄格式 · 30 加「禁止 git commit · Lead commit」
- [ ] 保留：GATE_SCAN · human_gate · invoke 落盘路径 · merge_policy · CLOSE 管道
- [ ] 不复制：KC §2「零上下文」专节（CC 不需要）

---

## 9. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | v1 · KC/CC 串行 Harness Prompt 对照 · T1 recentsync 试点落盘 |
