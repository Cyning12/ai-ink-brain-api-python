# Task：Coding Wiki A2 — CODING_WIKI §8 ingest test_strategy 纪律（v1）

> **状态**：done（2026-05-26 验收通过 · CODING-WIKI-A2-SCHEMA-RULE@2026-05-26）  
> **母 Loop**：[`task_harness_wiki_loop_a1_a4_v1.md`](task_harness_wiki_loop_a1_a4_v1.md) · round **A2**  
> **关联 Schema**：[`docs/coding_wiki/CODING_WIKI.md`](../coding_wiki/CODING_WIKI.md) **§8**  
> **前置占位**：A1 关账回填（见下）

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Schema 文档增补；不新增 pytest、不改 synthesis 正文（除非 22 发现事实错误单列阻塞）。 |
| **freeze_id** | `CODING-WIKI-A2-SCHEMA-RULE@2026-05-26` |
| **gates_before_code** | `["human_gate", "A1_OUTCOME 已回填", "failure_paths"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **task_slug** | `wiki-a2-schema-test-strategy` |
| **wiki_delta** | `docs/coding_wiki` |
| **wiki_delta_note** | 存量迁移 · 本 task 触及 docs/coding_wiki（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 母 task [`HG-LOOP-BATCH`](task_harness_wiki_loop_a1_a4_v1.md) = `approved` 后方可 22 |

---

## 前置（A1 关账回填 · 勿删标记）

<!-- PLACEHOLDER:A1_OUTCOME -->
- **test_strategy**：`recommended`（与 L1 `task_05_query_rewrite_observability.md` 一致）
- **改动路径**：`docs/coding_wiki/syntheses/query-rewrite-observability.md`、`docs/coding_wiki/log.md`
- **30 commit**：`cbe181e`
- **摘要**：A1 在 synthesis frontmatter/摘要/§测试变更 蒸馏 `test_strategy`，修复 Wiki-CTX-AB Multi slug B-Q3 类缺口
<!-- /PLACEHOLDER:A1_OUTCOME -->

> **22 开工前**：若上块仍为「待回填」→ **先**完成 A1 关账回填，**再**开 22。

---

## 帽子顺序（**跳过 10** · Loop A2）

| 序 | 帽 | 启动 |
|----|-----|------|
| — | **10** | **跳过** |
| 1 | **22 R1** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md) · [`LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md) **round=A2** |
| 2–5 | **30→40→50→关账** | 同上 Loop 链 |

**纪律**：读 [`docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md`](task_coding_wiki_ingest_test_strategy_v1.md)（A1 done）确认占位已替换。

---

## 背景与目标

Multi 结论 §4 建议：**改 `api/` 的 done Epic**，synthesis ingest 时须含 **`test_strategy`**（或内联 pointer 至 `concepts/test-strategy-ink-backend` **正文**）。A1 已在实例页示范；A2 将纪律 **写入 Schema §8**，避免后续 ingest 再漏 B-Q3 类字段。

**完成态**：`CODING_WIKI.md` §8 增补 **ingest 规范** 小节（或表格行），明确 api/ 类 Epic 的 `test_strategy` 要求与 pointer 规则；与 A1 交付一致。

---

## 范围

- [x] 在 `docs/coding_wiki/CODING_WIKI.md` **§8** 增补 ingest 规范：`api/` 相关 done Epic → synthesis **须**含 `test_strategy`（frontmatter 或摘要）**或** 内联 pointer 至 `concepts/test-strategy-ink-backend` 正文。  
- [x] §8 修订记录追加一行（日期 + 摘要）。  
- [x] 22/40/50 落盘；关账 `git mv` 至 `done/`。

## 非范围

- **不**修改 A1 已改的 `query-rewrite-observability` synthesis 正文（除非 22 R1 发现与 L1 事实矛盾，须单列阻塞项）。  
- 不改 `api/`、`tests/`、CI、Harness prompts。  
- 不重写 `CODING_WIKI.md` 其他章节或对比表全文（对比表属 A3）。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| A1 done | `docs/tasks/done/task_coding_wiki_ingest_test_strategy_v1.md` |
| Schema | `docs/coding_wiki/CODING_WIKI.md` §8 |
| 概念页 | `docs/coding_wiki/concepts/test-strategy-ink-backend.md` |
| Multi 建议 | `conclusion_multi_slug_zh.md` §4 |
| 母 Loop | `LOOP_MANIFEST.md` round A2 · `PLACEHOLDER:A1_OUTCOME` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | `PLACEHOLDER:A1_OUTCOME` 未回填 | 22 **拒开工** | 是 | 先 A1 关账 |
| F2 | §8 仅写「见 concept」无 frontmatter/摘要要求 | 22 **阻塞**（不可答 B-Q3） | 是 | 须可操作 ingest 检查项 |
| F3 | 与 A1 实例 `test_strategy` 取值矛盾 | 22/50 **fail** | 是 | 以 L1 + A1 为准对齐 |
| F4 | 误改 A1 synthesis 正文 | 越界；50 **fail** | 否 | revert；单列 fix task |

---

## 验收标准

- [x] `CODING_WIKI.md` §8 含明确条文：`api/` 类 Epic synthesis 须 `test_strategy` 或合规 pointer。  
- [x] `grep -n test_strategy docs/coding_wiki/CODING_WIKI.md` 在 §8 区间有命中。  
- [x] 22 R1 落盘 `reviews/by-task/wiki-loop-a1-a4/`。  
- [x] 50 复检 pass；本 task 在 `done/`。  
- [x] 无 `api/`、`tests/` diff。

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`。

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/coding_wiki/CODING_WIKI.md` §8.1 |
| 30 commit | `3826cba` |
| 图谱变更点 | 无 |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `grep -n test_strategy docs/coding_wiki/CODING_WIKI.md` |
| 结论 | **pass** |
| 要点 | §8.1 含 ingest 纪律 + VERIFY；与 A1 示范一致 |

---

## 给 Cursor

`wiki-a2-schema-test-strategy`、`CODING-WIKI-A2-SCHEMA-RULE@2026-05-26`、`PLACEHOLDER:A1_OUTCOME`、`CODING_WIKI` §8、`PROMPT_LOOP_22_to_CLOSE`、`round=A2`
