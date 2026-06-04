---
title: "test_strategy required 实践"
slug: vol-03-02-tdd
series: chatbi-graph-harness-showcase
vol: "03"
chapter: "02"
status: compiled
---

# 02 · test_strategy: required

> **横切要点**：vol-01 / vol-02 均为 `required` · 但 **red-green 形态不同** — 本页统一口径，避免面试 overclaim「全员 strict TDD」。

---

## 1. 制度定义 vs 本仓实践

| 层 | 说法 |
| --- | --- |
| **制度**（`HARNESS_V2_PLAN` §5.1） | `required` = 先 **失败可复现** 的测试，再改实现；自检须附命令与通过证明 |
| **本仓实践**（2026-05-30 决策） | 以 **CI 回归 + 分层补测** 为主；**不全员** strict 先红后绿 |
| **OpenSpec 对齐** | task 须填 **行为变更 Delta** + **Scenario ID** · `harness_task_validate.py` 门禁 |

真值：[`HARNESS_V2_PLAN.md`](../../../harness/HARNESS_V2_PLAN.md) §5.1 · [`SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md`](../../../spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md)

**面试诚实句**：「required 在本仓是 **测试与验收不可省略**，P0 有专测 red-green；基线闸则是 **对齐 main 上已存在的 10 个失败测**，不是从零写 TDD。」

---

## 2. 两种 required 形态（本系列）

### A · 对齐既有失败（vol-01 基线闸）

| 项 | 内容 |
| --- | --- |
| **前提** | main 上 **10× v3 plan/clarify** 已 fail |
| **做法** | 修 **环境/配置/manifest 真值**（`conftest` · `agent` · contract） |
| **断言** | **未删测** · **未放宽** · **未**用 marker 排除 |
| **50 结论** | 修复后 10 passed；根因是 `.env` 阈值与 CI 不一致 |

```bash
pytest tests/test_unified_chat_backend_v2_agent.py \
  -k "v3 and (plan or low_confidence)" -q
# 期望：10 passed
```

### B · 新增专测（vol-02 P0）

| 项 | 内容 |
| --- | --- |
| **前提** | P0 Delta 定义五步 + Scenario |
| **做法** | **同 PR** 新增 `tests/test_chatbi_graph_p0_foundation.py` |
| **断言** | **10/10** · 覆盖边表 · stub 路由 · 共享层 import |
| **50 结论** | P0 专测 pass；全集 10 fail **仍属 main 基线**（非 P0 回归） |

```bash
pytest tests/test_chatbi_graph_p0_foundation.py -q
# 期望：10 passed
```

---

## 3. task 侧必填（开 30 前）

| 字段 | 用途 |
| --- | --- |
| `test_strategy: required` | 50 必落盘 · 关账前不可 skip |
| `## 行为变更（Delta）` | MODIFIED / ADDED · 与 diff 对照 |
| Scenario ID | 如 `graph-edge-table-smoke` · 专测或验收表映射 |
| `## 失败路径` | 触发 → 行为 → 可重试 · 缺则 **拒开工** |
| `## 验收标准` | 可勾选 · 含 pytest / contract 字面项 |

校验：

```bash
python tools/harness_task_validate.py \
  --task docs/tasks/active/task_<slug>.md
```

---

## 4. 合并前必绿（AGENTS §8）

两 task **共用**同一全集命令：

```bash
pytest tests -m "not intent_eval and not intent_benchmark" -q
# 2026-06-04 口径：287 passed, 1 skipped
```

**时间线差异**：

| 时点 | 全集 | 说明 |
| --- | --- | --- |
| P0 50（06-03） | 277 pass · **10 fail** | 与 main 同失败集 |
| #106 merge 后 | 277 pass · 0 fail（基线项已修） | vol-01 |
| #107 rebase 后 | **287 pass** | +P0 专测 10 条计入 |

---

## 5. 禁止项（50 / 审查会抓）

| 禁止 | 本系列反例 |
| --- | --- |
| 为绿 **删测** | 两 PR 均未删 v3 测 |
| 为绿 **改断言放水** | 基线闸修环境，未改 assert 文本 |
| `-m` / `@pytest.mark.skip` **排除** required 范围 | 未使用 |
| `not_applicable` 滥用 | 涉 `api/` 的 Graph P0 **必须** required |

---

## 6. 40 vs 50 的测试职责

| 帽 | 测什么 |
| --- | --- |
| **40** | 执行者 **独立复跑** task 验收表 · 回填 `### 自检结论` |
| **50** | **Fresh Context** 再跑 · 对照 diff · **不读** 30 invoke 全文 |

P0 40 曾记录「全集未绿」— 50 独立确认 **非 P0 回归** 后，维护者才选 B 开 vol-01。

---

## 指针

- vol-01-04 技术修复 · vol-02-02 五步专测
- OpenSpec Delta：task `## 行为变更（Delta）`
