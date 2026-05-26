# Task：治理 — invoke README / _views 索引同步（R2 · 烟雾）

> **状态**：draft  
> **母 Loop**：[`task_harness_wiki_loop_c2_verify_v1.md`](task_harness_wiki_loop_c2_verify_v1.md) · round **R2**  
> **依赖**：R1 须在 `done/` 且 RECENT §6.6 含 Loop C2 Verify draft 行

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；**本 round 负责** RECENT §6.6 行标 **done** + `_views/done.md`。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | invoke README 验收说明 + 索引同步；纯 docs。 |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |
| **task_slug** | `wiki-c2-r2-index-sync` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 继承 [`HG-LOOP-BATCH`](task_harness_wiki_loop_c2_verify_v1.md) |

---

## 帽子顺序（**跳过 10** · Loop R2）

| 序 | 帽 | 启动 |
|----|-----|------|
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-c2-verify/PROMPT_LOOP_22_to_CLOSE_v1.md) · **round=R2** |

---

## 背景与目标

R1 已在 RECENT §6.6 写入 Loop C2 Verify draft 行。本 round 补全 invoke 目录 **验收说明**，并在关账时将 RECENT 行与 `_views/done.md` 同步为 done。

**完成态**：

- [`docs/harness/invokes/by-task/wiki-loop-c2-verify/README.md`](../../harness/invokes/by-task/wiki-loop-c2-verify/README.md) **验收说明** 段落含 C2 verify 主目标一句（链 meta-reinspect 结论）。  
- 关账时 RECENT §6.6 本 Loop 行 **→ done**；`_views/done.md` 更新 R1/R2 索引。

---

## 范围

- [ ] 22 前确认 R1 在 `docs/tasks/done/`。  
- [ ] 更新 invoke README 验收说明（若 R1 Batch 已写骨架则 **补全/确认** 一行结论位）。  
- [ ] 关账：RECENT §6.6 done + `_views/done.md`。  
- [ ] 22/30/40/50 invoke **C2 全绿**（§3 ≥15 行 · **R2 各帽禁止 stub**）。

## 非范围

- Harness prompts / api / tests / CI。  
- 重跑 B-Q3；代 SKILL 标 accepted。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | R1 未 done | 22 阻塞 |
| F2 | R2 30/40/50 invoke stub | **C2 fail** · 50 fail（本 Loop 主验收） |
| F3 | RECENT done 但 R1 未 done | 关账阻塞 |

---

## 验收标准

- [ ] invoke README 含 C2 verify 验收说明。  
- [ ] RECENT §6.6 本 Loop 行状态 **done**。  
- [ ] `_views/done.md` 含 R1/R2 条目。  
- [ ] **R2 全链 invoke C2 pass**（对比 B-Q3 R2/R3 stub 债）。

**VERIFY**：

```bash
rg 'C2 verify|C2 Verify' docs/harness/invokes/by-task/wiki-loop-c2-verify/README.md
rg 'Loop C2 Verify.*done' docs/tasks/RECENT_TASK_SCHEDULE.md
```

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `wiki-loop-c2-verify/README.md` · 关账时 `RECENT_TASK_SCHEDULE.md` §6.6 · `_views/done.md` |
| README | §验收说明已回填 · 链 meta-reinspect C2 FAIL · R1/R2 invoke C2 目标 |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| README 验收说明 | | |
| RECENT done | | |
| R2 invoke C2 | | |

---

## 给 Cursor

`wiki-c2-r2-index-sync`、`PROMPT_LOOP`、`round=R2`、`_views/done`、`invoke C2`
