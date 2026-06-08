# Diary · Harness 链式执行 · 下一棒 task 规划（2026-06-08）

> **日期**：2026-06-08（§7 增补 · 双轨废弃 `semi_auto`）  
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

- P0 diary：[`2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md`](2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md) · §5 **「Task 链定为改代码主力；semi_auto 计划废弃」**
- KC diary：[`2026-06-08-kimi-harness-pilot-recentsync_zh.md`](2026-06-08-kimi-harness-pilot-recentsync_zh.md)
- KC↔CC 对照：[`docs/harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md`](../harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md)

**结论（当日共识）**：

1. **三执行器**均可跑 docs-only 帽链（explore→22→30→40→CLOSE）。
2. **`semi_auto` 非链式真值字段**；链式靠 **`orchestration` + `PROMPT_*_chain_serial_*` + invoke 落盘**。
3. **KC 与 CC 最大差**：子 Agent 是否零上下文 → KC 须每帽内联读序/forbidden；CC 靠 `.claude/agents/` + 薄 spawn。
4. **P0 取向尚未在 api 面兑现**：docs 试点只证明 **编排**；P0 §5 的「改代码主力」须 **api 链式试点** 才能关账。
5. **P0 diary §7 待办仍未立项**：Harness V2 / governance SPEC 写「Task 链默认编排」条文。

---

## 2. 当前无 active「链式方法论」task

- `docs/tasks/active/` **无** `task_*chain*` / orchestration 推广单。
- 多数 active 为 ChatBI/RAG 业务 · `semi_auto: false` 或未绑链式 PROMPT。
- **旧模式残留**：[`task_chatbi_intent_llm_retry_u1_5_v1.md`](../tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md) 仍 `semi_auto: true` · `test_strategy: required` · 触 `api/intent_agent.py` — **方案 B 首选迁移对象**。

---

## 3. 新 task 可选方案（比选）

> 开干前须建 `docs/tasks/active/task_*.md` + 预批 `human_gate` + 对应 `PROMPT_*` 实例。

### 方案 A · 治理 SPEC：Task 链默认编排（**双轨之一 · docs**）

| 项 | 内容 |
| --- | --- |
| **动机** | 收口 P0 diary §7；把 `semi_auto` **过渡/废弃** 写入 governance 真值 |
| **交付** | `SPEC-Governance-Harness-Chain-Orchestration-v1` 或扩写 `HARNESS_V2_PLAN` §5；`TASK_TEMPLATE` 增 **`orchestration`** 字段 |
| **帽链** | 10→22→30 docs→40→CLOSE（`test_strategy: not_applicable`） |
| **执行器** | Cursor / CC · 可与 **E 合并** 同一 PR |
| **风险** | 低 |
| ** alone 不够** | 仅 A **不能**宣称全面废弃 `semi_auto`（缺 api 实证） |

### 方案 B · api 链式试点：ChatBI Intent Retry U1.5（**双轨之二 · required**）

| 项 | 内容 |
| --- | --- |
| **动机** | P0 §5「改代码主力」；[`task_chatbi_intent_llm_retry_u1_5_v1`](../tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md) 已 active · **`semi_auto: true` → 链式迁移** |
| **交付** | `api/intent_agent.py` 重试/超时 + **`tests/test_intent_llm_retry.py`** · 链式 invoke/review/**50** |
| **帽链** | explore→22→30→40→**50**→CLOSE（`test_strategy: required`） |
| **执行器** | **CC 或 Cursor 首棒**（改码 + spawn）；KC 可后续对照 · 不宜 api 首棒 |
| **风险** | 中高 · 须 TDD + reinspect |
| ** alone 不够** | 仅 B 无 A → RECENT/TEMPLATE 仍写 `semi_auto`，会继续漂移 |

### 方案 C · docs：RECENT §6.3 done/ 扩面

| 项 | 内容 |
| --- | --- |
| **动机** | KC explore 曾列 11 候选未修 |
| **备注** | 与 #134 重叠 · 优先级低于 A+B · 按需 |

### 方案 D · Kimi Plan Agent 导航复验（零 PR）

| 项 | 内容 |
| --- | --- |
| **动机** | [`PROMPT_kimi_plan_agent_nav_revalidation_zh.md`](../harness/prompts/PROMPT_kimi_plan_agent_nav_revalidation_zh.md) 未执行 |
| **备注** | 非 Harness T1 · 可与 A/B **筹备并行** · 不阻塞废弃 `semi_auto` |

### 方案 E · docs-noise §6 + prompts README 补丁

| 项 | 内容 |
| --- | --- |
| **动机** | §6 缺 KC/#134/COMPARISON · 链仍指 `active/` MANIFEST |
| **备注** | **建议并入方案 A** |

### 方案 F · CC 薄 Prompt 工程回归

| 项 | 内容 |
| --- | --- |
| **备注** | 验证 COMPARISON 可跑 · 业务增量≈0 · 低于 A/B |

---

## 4. 推荐排期（**人择：同意 · 2026-06-08**）

> **全面废弃 `semi_auto`** = **A（±E）+ B 双轨 CLOSE**，非「仅 docs 链式常模」。

```text
Epic：Harness 链式常模 + semi_auto 退场

并行筹备（可两 PR / 两 task 分支）：
  ① 方案 A（±E）  →  governance 真值 · orchestration 字段 · semi_auto 过渡说明
  ② 方案 B        →  api/ 链式首棒 U1.5 · required + 50 · 迁移 off semi_auto

可选并行（不阻塞）：
  ③ 方案 D        →  Kimi Plan Agent 复验 · 零业务 PR

延后 / 按需：
  ④ 方案 C / F
```

**硬门禁（宣称 semi_auto 全面废弃前）**：

| 门禁 | 方案 | 证明什么 |
| --- | --- | --- |
| G1 文档常模 | A（±E） | SPEC/TEMPLATE/RECENT 不再以 `semi_auto: true` 为默认 |
| G2 改码关账 | B | 链式 + TDD + pytest CI + **50 reinspect** 可闭环 |
| G3 执行器 | 已有 #121/#123–134 | Cursor / CC / KC 至少各 1 次 docs；B 补 **api** |

---

## 5. 开下一棒 checklist（通用）

- [x] 人择 **A+B 双轨**（2026-06-08 同意）
- [x] A：`docs/tasks/done/task_harness_chain_orchestration_spec_v1.md` · `semi_auto: false` · `orchestration` · PR #135 · T1 CLOSE
- [ ] B：改 [`task_chatbi_intent_llm_retry_u1_5_v1`](../tasks/active/task_chatbi_intent_llm_retry_u1_5_v1.md) · **`semi_auto: false`** · 绑 `PROMPT_{claude|cursor}_chain_serial_v1_T1_intent-retry-u1.5`
- [ ] B 追加：`PROMPT_*` 内 **30 先测后实现 · 40 pytest · 50 落盘** 硬约束
- [ ] `human_gate` 预批 · 分支 `task/harness-chain-orchestration-spec-v1` / `task/chatbi-intent-llm-retry-u1.5-chain-v1`
- [ ] invoke slug：`harness-chain-orchestration-spec` / `chatbi-intent-retry-u1.5-chain`

---

## 6. 方案 B 链式相对 docs 试点增量（备忘）

| 维度 | docs 试点（#121–#134） | api 试点 B（U1.5） |
| --- | --- | --- |
| `test_strategy` | `not_applicable` | **`required`** |
| 50 帽 | 可 skip | **必须** `reinspect_results/` |
| 30 帽 | 改 Markdown | 改 **`api/`** + 先写失败测试 |
| 40 帽 | rg / 验收勾选 | **pytest** 全绿证据 |
| `semi_auto` | 已是 `false` | 从 **`true` 迁移** off |

---

## 7. 双轨废弃 `semi_auto`（决策摘要）

**问题**：P0 已写「Task 链 = 改代码主力 · semi_auto 计划废弃」，但后续仅完成 **docs** 链式试点；[`HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5.6 仍把 `semi_auto` 列为可选常模。

**决策（2026-06-08）**：

1. **全面废弃 `semi_auto`** 须 **治理文档（A）+ api 实证（B）** 同时 CLOSE，缺一不可。
2. **A 与 B 可并行筹备**（不必等 A merge 再开 B task 草案）；关账叙事上 **G1+G2 齐** 再对外宣称废弃。
3. **B 首选** U1.5 micro-PR：范围 bounded · 已有 active task · 与 Intent Epic 一致。
4. **D/C/F** 不纳入 semi_auto 退场硬门禁。

**下一文档动作（待执行）**：在本分支或子分支起草 A/B 的 `active/task_*.md` + PROMPT 实例（**本文仅更新规划 diary**）。

---

## 8. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | 初稿：KC #134 收口后 · 六方案比选 |
| 2026-06-08 | §7 增补：双轨废弃 semi_auto · A+B 并行 · B=U1.5 api 试点 · 修订 §4/§5 checklist |
