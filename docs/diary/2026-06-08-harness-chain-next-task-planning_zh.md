# Diary · Harness 链式执行 · 下一棒 task 规划（2026-06-08）

> **日期**：2026-06-08  
> **分支**：`task/harness-chain-orchestration-next-v1`（自 `main` 拉出 · **规划态** · 尚未开 active task）  
> **性质**：链式编排 **试点收口回顾** + **新 task 方案比选** · 非 L0 真值  
> **触发**：KC 试点 PR [#134](https://github.com/Cyning12/ai-ink-brain-api-python/pull/134) 已 merge · Cursor 终验关账完成

---

## 1. 链式试点现状（已 CLOSE）

| 批次 | 执行器 | task（done） | PR | Prompt 真值 |
| --- | --- | --- | --- | --- |
| docs-noise P0 | **Cursor Task 链** | `task_gov_docs_noise_p0_readme_v1` | #121 | `PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0` |
| docs-noise P1–P3 | **Claude Code spawn 链** | `task_gov_docs_noise_p1~p3_*` | #123/#126/#129 | `PROMPT_claude_chain_serial_v1_T0/T2*` |
| docs-noise MANIFEST | CC Lead | `task_governance_docs_noise_line_manifest_v1` | #132 等 | `PROMPT_claude_T3_*` |
| **KC 试点 T1** | **Kimi Code Agent 链** | `task_governance_kimi_harness_pilot_recentsync_v1` | **#134** | `PROMPT_kimi_task_chain_serial_v1_T1_recentsync` |

**留证**：

- P0 diary：[`2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md`](2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md)
- KC diary：[`2026-06-08-kimi-harness-pilot-recentsync_zh.md`](2026-06-08-kimi-harness-pilot-recentsync_zh.md)
- KC↔CC 对照：[`docs/harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md`](../harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md)

**结论（当日共识）**：

1. **三执行器**均可跑 docs-only 帽链（explore→22→30→40→CLOSE）。
2. **`semi_auto` 非链式真值字段**；链式靠 **`orchestration` + `PROMPT_*_chain_serial_*` + invoke 落盘**。
3. **KC 与 CC 最大差**：子 Agent 是否零上下文 → KC 须每帽内联读序/forbidden；CC 靠 `.claude/agents/` + 薄 spawn。
4. **P0 diary 可选待办仍未立项**：Harness V2 / governance SPEC 写「Task 链默认编排」条文。

---

## 2. 当前无 active「链式方法论」task

- `docs/tasks/active/` **无** `task_*chain*` / orchestration 推广单。
- 多数 active 为 ChatBI/RAG 业务 · `semi_auto: false` 或未绑链式 PROMPT。
- 例外：`task_chatbi_intent_llm_retry_u1_5_v1` 仍 `semi_auto: true`（**旧半自动**，非 Task 链）。

---

## 3. 新 task 可选方案（比选 · 待人择一）

> 下列为 **2026-06-08** 规划候选；开干前须建 `docs/tasks/active/task_*.md` + 预批 `human_gate` + 对应 `PROMPT_*` 实例。

### 方案 A · 治理 SPEC：Task 链默认编排（**推荐优先**）

| 项 | 内容 |
| --- | --- |
| **动机** | 收口 P0 diary 待办；把 `semi_auto` 过渡态写入 governance 真值 |
| **交付** | `SPEC-Governance-Harness-Chain-Orchestration-v1` 或扩写 `HARNESS_V2_PLAN` §5；`TASK_TEMPLATE` 增 **`orchestration`** 字段说明 |
| **帽链** | 10→22 定稿→30 docs→40→CLOSE（`test_strategy: not_applicable`） |
| **执行器** | Cursor / CC / Kimi 均可 · 建议 **CC 或 Cursor**（改 docs 为主） |
| **风险** | 低 · 纯 docs |
| **unblocks** | 后续业务 task 默认知道用哪套 PROMPT |

### 方案 B · 业务链式首棒：ChatBI Intent Retry（U1.5）

| 项 | 内容 |
| --- | --- |
| **动机** | `task_chatbi_intent_llm_retry_u1_5_v1` 已 active 且 `semi_auto: true` · 适合 **迁移** 到链式 |
| **交付** | 实现 + 链式 invoke/review · 可能触 `api/` |
| **执行器** | CC（有 `.claude/agents`）或 Cursor |
| **风险** | **中高** · `test_strategy: required` · 须 50 |
| **备注** | 首个 **改代码** 链式 task · 建议 A 完成后再开 |

### 方案 C · 业务链式 docs：RECENT §6.3 done/ 状态卫生（扩面）

| 项 | 内容 |
| --- | --- |
| **动机** | KC 试点 B 段仅修 gov-docs-noise 5 文件；explore 曾列 **11** 个 legacy/早期候选未修 |
| **交付** | 再选 ≤10 个 `done/` 状态行回填 · 更新 RECENT §6.3 |
| **执行器** | 任一 · KC 可 **A/B 对照** 耗时 |
| **风险** | 低 · docs-only |
| **备注** | 与 #134 部分重叠 · 需写清 **非重复** 范围 |

### 方案 D · Kimi Plan Agent 导航复验（零 PR）

| 项 | 内容 |
| --- | --- |
| **动机** | [`PROMPT_kimi_plan_agent_nav_revalidation_zh.md`](../harness/prompts/PROMPT_kimi_plan_agent_nav_revalidation_zh.md) 已落盘 · 未执行 |
| **交付** | `tmp/diary/` 或 diary 对比稿 · **不改** task/RECENT/api |
| **执行器** | Kimi Code 主会话 |
| **风险** | 极低 · 非 Harness 关账 task |
| **备注** | **不是**链式 T1 · 可与 A 并行 |

### 方案 E · 导图/索引补丁：docs-noise §6 + prompts README

| 项 | 内容 |
| --- | --- |
| **动机** | `docs-noise-inventory/README.md` §6 仍偏 CC · 缺 KC/#134/COMPARISON；部分链仍指 `active/` MANIFEST |
| **交付** | §6 执行编排表 + Kimi 行 · 链路径修正 |
| **执行器** | CC/Cursor · 小 diff |
| **风险** | 低 |
| **备注** | 可与 **A 合并** 为同一 PR |

### 方案 F · CC 薄 Prompt 回归：T1 recentsync 同业务 CC 实例

| 项 | 内容 |
| --- | --- |
| **动机** | 验证 [`COMPARISON`](../harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md) 中「CC 实例 ≈ KC 1/3 篇幅」可跑通 |
| **交付** | 新建 `PROMPT_claude_chain_serial_v1_T1_recentsync_zh.md` · **不重复** 改 RECENT（已 #134 合入） |
| **执行器** | Claude Code |
| **风险** | 低 · 偏 **工程实验** · 业务增量几乎为 0 |
| **备注** | 优先级低于 A |

---

## 4. 推荐排期（建议）

```text
① 方案 A（±E 合并）  →  governance 真值 · 链式常模冻结
② 方案 D（可选并行）  →  Kimi 产品向 · 零 PR
③ 方案 B              →  首个 api/ 链式业务 · 须 A 后
④ 方案 C / F          →  按需 · 避免与 #134 重复
```

---

## 5. 开下一棒 checklist（通用）

- [ ] 人择方案 A–F 之一（或组合 A+E）
- [ ] `docs/tasks/active/task_harness_chain_*_v1.md` · `orchestration` · `semi_auto: false`
- [ ] `PROMPT_{cursor|claude|kimi}_chain_serial_v1_T*` 实例
- [ ] `human_gate` 预批
- [ ] `git_branch` = `task/harness-chain-*-v1`
- [ ] invoke slug 落 `docs/harness/invokes/by-task/<slug>/`

---

## 6. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | 初稿：KC #134 收口后 · 下一棒链式 task 六方案比选 |
