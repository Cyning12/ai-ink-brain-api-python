# 结论 · wiki-loop-unit-a · Claude Code · 2026-05-28

> **case**：[`scorecard.md`](./scorecard.md) · **量表**：[`rubric_v1.md`](../../rubric_v1.md) · **完成汇报**：[`REPORT_completion_wiki_loop_unit_a_v1.md`](../../../../invokes/by-task/wiki-loop-unit-a/REPORT_completion_wiki_loop_unit_a_v1.md)

---

## 1. 一句话

Claude Code 在 **`PROMPT_START` + `SKILL-harness-loop-batch`（第六轮）** 下 **首次完整跑通** docs-only **Loop 全链**（R1→R3→META）：**业务 96% · Harness 90% · 可开 PR-A 94%**；**ST0 过程债**（未人批即开工）已用人批 + 机器门禁收口，**不否定**关账后交付质量。

---

## 2. 做对了什么

| 项 | 说明 |
| --- | --- |
| **Loop 全链** | 3 round ×（22/30/40/50/CLOSE）+ META CLOSE + `REPORT_completion_*` |
| **cross-round** | R1·22 invoke 含 `cross_round_semi_auto: true` · 同会话续 R2/R3 |
| **业务交付** | hygiene 四文档 · T4 **20/20** `graph_nodes` · Batch-3 **25** syntheses |
| **C1–C7** | 与 `SKILL-harness-loop-batch` 合规自检一致（REPORT §5） |
| **关账 hygiene** | 母/子 task 头部 `done` · `_views` · 无「仅 git mv」债（对比 gov-l2-manifest-ci case） |
| **diff 纪律** | 无 `api/` / `tests/` / prompts 帽子 / CI workflow |

---

## 3. 偏差与根因

| 现象 | 根因 | 严重性 |
| --- | --- | --- |
| **未人批即开工**（过程） | cc **未**将「【授权】/ semi_auto」与 **`human_gate` 文件状态** 分离；贴 Prompt ≠ `approved` | **高**（已修门禁） |
| R2/R3·22 invoke §3 **摘要化** | 续跑 round 复用短模板，未每轮展开 `PROMPT_LOOP` 七步全文 | **低** · 仍过 C2 行数/体量 |
| review 目录在 `by-task/<slug>/` | 非 `wiki-loop-unit-a/` 聚合目录 · REPORT §3 计数路径笔误 | **低** · 可检索 |
| 依赖人批 commit `f30f8dd` 后才链式执行 | 符合设计；**不能**仅靠对话【授权】替代 | **信息** |

---

## 4. 已反哺的改进（本仓 · 2026-05-28）

| 工件 | 改动 |
| --- | --- |
| `SKILL-harness-loop-batch.md` | §执行铁律 · §机器门禁 · v1.9/v1.10 |
| `PROMPT_START_loop_unit_a_full_chain_v1.md` | 步骤 0 Gate · `grep approved` 自检 |
| `tools/harness_human_gate_check.py` | PR 执行产物 + `--task` 硬校验 |
| `rubric_v1.md` | **ST0** human_gate |
| **本 case** | `wiki-loop-unit-a_claude-code_20260528` 落盘 |

---

## 5. 裁决与后续

| 问题 | 答案 |
| --- | --- |
| cc 能否跑通 **harness-loop-batch** 全链？ | **能**（本 case 已证 · 优于单 task ST5 债个例） |
| 是否可签收 **PR-A**？ | **是**（docs-only · 建议 Required CI 绿后合并） |
| 是否推荐默认只贴【授权】不开工？ | **否** · 须 **人批 task + §1 grep + 步骤 0** |
| 单元 B（`gov-l2-phase-c-impl`）？ | **另 case** · `test_strategy: required` · 勿与 PR-A 混 PR |

---

## 6. 测评人备注

- 测评依据：Git 提交链、`invoke_*` 体量抽检、REPORT §5、母单 `done/` 状态。  
- **未**重跑业务 VERIFY（docs-only · 无 pytest 门禁）。  
- 若需 Cursor 对照：可对同一 `WIKI-LOOP-UNIT-A` 规格另开 `wiki-loop-unit-a_cursor_*` case。
