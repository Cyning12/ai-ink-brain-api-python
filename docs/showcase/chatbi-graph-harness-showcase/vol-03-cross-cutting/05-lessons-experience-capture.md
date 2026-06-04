---
title: "经验沉淀"
slug: vol-03-05-lessons
series: chatbi-graph-harness-showcase
vol: "03"
chapter: "05"
status: compiled
---

# 05 · 经验沉淀（experience_capture）

> **横切要点**：从 vol-01/02 **抽象可复用教训**；P1 / 下一条 Loop 开工前 **必读**。  
> 非 L0 真值 — 细节以 reinspect / task 为准。

---

## 1. 分两 PR · 基线债 vs 架构增量

| 教训 | 本系列表现 | P1 复用 |
| --- | --- | --- |
| **Delta 可审计** | P0 50 发现 main 10 fail ≠ P0 引入 → **选 B** 独立 #106 | P1 勿在 Graph MVP PR 里修无关红项 |
| **task `blocks` 落盘** | P0 task 阻塞于基线闸 | 新 task 显式写 merge 顺序 |
| **rebase 顺序** | #106 → rebase P0 → #107 | 任何「先合 feature 再修 CI」须书面决策 |

**50 Judgment 句**：pass-with-notes **不是**「可以无视 CI」— 是「**本 task 增量 OK**，Strict 阻塞来自 **仓内基线**，须 **另 task** 或豁免策略」。

---

## 2. `.env` vs `conftest` · 本地与 CI 真值

| 教训 | 证据 |
| --- | --- |
| 开发者 `.env` 常见 `INTENT_MIN_CONFIDENCE=0.3` · 规格/CI 用 **0.6** | 10× v3 clarify 本地 mysteriously fail |
| **fix** | `tests/conftest.py` 在 dotenv 前固定 `0.6` |
| **面试** | 「不是删测，是对齐 **测试环境真值**」 |

勿 overclaim：「修了 Agent 大编排」— 实际是 **阈值 + clarify 合法值 `on`** + manifest。

---

## 3. manifest · contract · drift 三门

| 教训 | #106 / #107 |
| --- | --- |
| contract 红 | `label` 未登记 → `_contract_manifest.json` |
| manifest 绿但 drift 红 | Q-8 path 已进 `_manifest.json` · **`99_spec.md` 未写** |
| **习惯** | 新端点 checklist（vol-03-03 §5） |

---

## 4. Harness 治理

| 教训 | 说明 |
| --- | --- |
| **22 两回合** | 复杂 task：R1 列阻塞 → 10 回填 → R2，比 30 中途改 task 便宜 |
| **human_gate 人签** | 单独 commit · `git blame` 指向人 · 50 追溯 |
| **Fresh Context 50** | 不读 30 invoke · 防「自证循环」 |
| **semi_auto** | invoke 落盘 + commit 再换帽 |

---

## 5. test_strategy 诚实口径

| 误区 | 纠正 |
| --- | --- |
| 「我们全员 TDD」 | 本仓 **required = 不可省略测试** · strict red-green **分场景** |
| 「287 绿 = P0 修好了 10 测」 | **#106** 修基线 · P0 专测 +10 |
| 「50 fail = 实现烂」 | 须对照 **origin/main** 同失败集 |

---

## 6. 展示 vs 真值

| 层 | 用途 |
| --- | --- |
| L1 task/reinspect | 验收 fail 真值 |
| L2 showcase（本系列） | 叙事 · 面试 · 演示脚本 |
| L0 图谱/代码 | 拓扑与 runtime |

**禁止**：用 vol-90 电梯稿替代 reinspect · 用 diary 覆盖 `_tech_graph`。

关账后可选摘要：`docs/diary/`（非必读 · 易过时）。

---

## 7. vol-04 P1 开工检查（摘自上列）

- [ ] 新 task · Delta · Scenario · `required` 专测计划  
- [ ] Q-8 路由 **行为**升级时三门 CI checklist  
- [ ] D-2：`unified_chat.py` 仍零 diff？（或单独 task 说明）  
- [ ] 50 Fresh Context · reinspect 路径预留  
- [ ] 更新本卷 vol-03（若 Harness/CI 规则有变）+ `_meta/TIMELINE`

---

## 8. experience_capture 字段（50 回填）

两案例 50 均建议 **维持 `required`** — P0 专测有效；基线红项不应降为 `not_applicable`。

下一条 task 的 50 可引用本页作为 **Judgment · 可复用模式** 指针。

---

## 指针

- vol-01 · vol-02 案例书  
- vol-90 投递短稿（L2 压缩版）  
- Roadmap P1：[`vol-04-p1/`](../vol-04-p1/)
