# SPEC — SDD 起草：多轮意图对齐（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `active` |
| **日期** | 2026-05-25 |
| **freeze_id** | `SPEC-SDD-INTENT-ROUNDS@2026-05-25` |
| **适用范围** | 本仓 `docs/spec/` 新建或重大修订；**不**替代 [`HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5 字段真值 |
| **Harness 映射** | **10** 需求 · **20** 规格短评（可选）· **22** 任务审核 · **30** 实现 |

> **一句话**：SPEC 不应「一轮生成定稿」；意图在 **写 SPEC 之前/之中** 多轮收敛，再 `freeze_id` 进 task。

---

## 0. 为何需要多轮

| 问题 | 单轮写满 SPEC 的后果 |
| --- | --- |
| 范围漂移 | 30 帽实现与最初口头目标不一致 |
| 验收不可测 | 22/40 才发现缺 `failure_paths`、命令未写清 |
| 与图谱/契约冲突 | 未对照 `_tech_graph` / `PROJECT_CONFIG` |
| 过度规格 | 小改也写一篇 SPEC，维护负担爆炸 |

**原则**：多轮对齐的是 **决策点**，不是 **页数**。

---

## 1. 三轮模型（默认 · 可按 Epic 裁剪）

### 轮 0 · 意图卡（Intent Card）

| 项 | 内容 |
| --- | --- |
| **产出** | 短文档或 **task 背景节**（可不进 `docs/spec/`） |
| **必含** | 完成态一句话 · **非范围** · 依赖（图谱路径 / API / 他 SPEC）· 验收口径草案 |
| **Harness** | **10 需求帽** 对话；人确认前 **不** 创建 L1 子规正文 |
| **停止** | 人/agent 勾选「方向对」或列出 **≤5 条待确认决策** |

### 轮 1 · SPEC 骨架（L0 / Overview）

| 项 | 内容 |
| --- | --- |
| **产出** | `SPEC-*-Overview.md` 或 governance 级 SPEC 的 §0～§2 |
| **必含** | 批次/模块边界 · 与现有 SPEC 引用 · 不重复造规的声明 |
| **Harness** | 10 帽可输出 **task 草案** + 指向骨架路径；**20 短评** 适合审骨架缺口 |
| **停止** | 无「与 xxx 矛盾」未决项 |

### 轮 2 · L1 子规 + 冻结（按需展开）

| 项 | 内容 |
| --- | --- |
| **产出** | `v3-agent/SPEC-*-<主题>.md` 等 **本 Epic 会动到的域** |
| **必含** | 行为 · **失败语义** · 与 `test_strategy` 建议（`required` / …）· `freeze_id` 候选 |
| **Harness** | **20** 查可测性；**22** 审 **task 与 SPEC 章节对齐**（非重写 SPEC） |
| **停止** | task 可填 `freeze_id`、执行帽 **gates_before_code** 可自检 |

```text
轮 0 意图卡 ──► 轮 1 L0 骨架 ──► 轮 2 L1+冻结 ──► task ──► 22? ──► 30
     ▲              │                │
     └──── 人确认决策点（每轮 ≤5 条）──┘
```

---

## 2. 与 Harness 帽子分工

| 帽子 | 对 SPEC 的职责 | 禁止 |
| --- | --- | --- |
| **10** | 澄清意图；输出 **SPEC 待确认清单**（见 §4）；写 task 草案 | 默认 **不** 一次生成整本 L1 |
| **20** | 对照 SPEC/task：**缺口、歧义、failure_paths、test_strategy** | 不替人拍板优先级 |
| **22** | 审 task 是否 **引用正确 SPEC 节**、验收是否可操作 | 不替代 20 做全文规格评审（除非人要求） |
| **30** | **只实现已冻结** 的 SPEC+task；发现 spec 缺口 **停工列清单** | 不顺手改 SPEC 冒充已审 |

**SDD 链**（与 [`SDD_HAT_FLOW.md`](../harness/SDD_HAT_FLOW.md) 一致）：

```text
SPEC（真值）→ task → [20] → [22 A] → 30 → 40 → [50] → 关账
```

**TDD**：由 task **`test_strategy`** 分级；`required` 将 SPEC 行为语义钉入测试（见 `HARNESS_V2_PLAN` §5.1）。**不是**每个 SPEC 都必须 `required`。

---

## 3. 何时可省略完整 SPEC

| 场景 | 做法 |
| --- | --- |
| 纯文档 / 目录 / 实验填表 | **无新 SPEC**；`task` + `test_strategy: not_applicable` + 一行理由 |
| 仅落实已有 L1 | task **引用** 既有 SPEC 章节 + `freeze_id`；最多 **轮 2 补一句** 修订记录 |
| 治理/实验（如 Wiki-CTX-AB） | [`governance/SPEC-Governance-*.md`](./governance/) 作 L0；细节在 `task` + `experiments/` |

**禁止**：用 **Coding Wiki** 或 **invoke 全文** 代替 SPEC 前的意图对齐（Wiki 是关账后编译层，见 [`governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)）。

---

## 4. 10 帽交付物：`SPEC 待确认清单`（推荐）

10 帽结束 task 草案时，若涉及 **新 SPEC 或重大增节**，须附下表（**3～5 行即可**）：

| # | 决策点 | 建议选项 | 待谁确认 |
| --- | --- | --- | --- |
| 1 | （例：是否改对外 API 契约） | A / B | 人 |
| 2 | … | … | 人 |

- **未确认前**：30 帽 **拒开工**（仅输出缺口）。  
- **已确认后**：写入 SPEC 或 task **修订记录**，并定 `freeze_id`。

---

## 5. 反模式

| 反模式 | 纠正 |
| --- | --- |
| Agent 自问自答完成「多轮」 | 每轮须 **显式待确认清单** 或人勾选 |
| 每轮重写 20 页 SPEC | 每轮只改 **范围/验收/失败语义** |
| 30 边写代码边发明 SPEC | 回到轮 2 或开 20/22 |
| 小 task 也新建 L0+L1 全套 | 用 §3 省略规则 |

---

## 6. 关联引用

| 用途 | 路径 |
| --- | --- |
| Harness 字段 | [`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) §5 |
| 帽子流程 | [`docs/harness/SDD_HAT_FLOW.md`](../harness/SDD_HAT_FLOW.md) |
| 10 帽正文 | [`docs/harness/prompts/hats/10-requirements.md`](../harness/prompts/hats/10-requirements.md) |
| 20 帽正文 | [`docs/harness/prompts/hats/20-review-spec-task.md`](../harness/prompts/hats/20-review-spec-task.md) |
| spec 目录索引 | [`docs/spec/README.md`](./README.md) |
| ChatBI L0 示例 | [`v3-agent/SPEC-ChatBI-V3-Overview.md`](./v3-agent/SPEC-ChatBI-V3-Overview.md) |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | v1：三轮意图对齐 + Harness 映射 + 10 帽待确认清单 |

---

## 给 Cursor

`SPEC-SDD-Intent-Rounds`、`意图卡`、`L0 骨架`、`freeze_id`、`10`、`20`、`SPEC 待确认清单`
