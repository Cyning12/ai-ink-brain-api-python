# SPEC — 治理：Harness 理论对齐 · P1

| 项 | 内容 |
| --- | --- |
| **状态** | `done`（P1 关账 · PR #92 · 2026-05-29） |
| **优先级** | **P1**（**依赖 P0 关账** 后启动；见 [`SPEC-Governance-Harness-Theory-Align-P0-v1.md`](./SPEC-Governance-Harness-Theory-Align-P0-v1.md)） |
| **freeze_id** | `GOV-HARNESS-THEORY-ALIGN-P1@2026-05-29` |
| **对照稿** | `ai_coding_governance/lib/COMPARISON_Harness-Ralph理论_vs_Ink落地_v1_zh.md` |
| **排期** | [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../tasks/RECENT_TASK_SCHEDULE.md) **§0.5** |
| **姊妹** | [`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](./SPEC-Governance-L2-Anchor-Test-Manifest-v1.md)（测试 manifest · 可并行草案，本 SPEC 先 **一条** 业务 Linter） |

---

## 0. 完成态（一句话）

讲义 **「修 Harness 一次」** 在 Ink 落地为：**半自动闸可观测、22/50 Fresh Context 纪律、首条领域结构 CI、test_strategy 默认表运维化**——在 **不引入 Ralph 编排器** 前提下拉近 **Sensors + Constrain**。

---

## 1. 背景与目标

| 讲义要点 | P1 动作 |
| --- | --- |
| 领域 `check_report_structure` | 选 **1 条** 高频路径做结构检查脚本 + CI（非全盘研报 Linter） |
| Ralph Fresh Context | 22/50 **新对话** + 40 交接三件 |
| 半自动 vs 全自动 | `semi_auto` / `human_gate` 在 active task **显式填写** |
| Guides+Sensors 闭环 | 与既有 `tech-graph` CI **并列**，不替代 |

**非范围**：`ralph_demo` 产品化；Hermes 全量 Skill 自进化；`verify-fast` 升为 Required（另议）。

---

## 2. 交付物清单

| # | 交付物 | 说明 |
| --- | --- | --- |
| P1-1 | **Fresh Context 纪律** | `22-task-audit.md`、`50-independent-reinspect.md`、`40-self-check.md`、`TEMPLATE-*-invoke` 增补禁止附带 30 长文 |
| P1-2 | **半自动推广** | `docs/tasks/README.md`：`human_gate` 场景 + `semi_auto` 决策表；active task 填 `audit_profile` |
| P1-3 | **领域结构 Linter（首条）** | 见 §3；建议首靶：**ChatBI v3 SSE/事件名** 或 **统一错误响应 shape**（与 `tech_graph_contract_check` 互补） |
| P1-4 | **test_strategy 默认表运维** | README 表 + 22 抽检季度说明（一行即可） |
| P1-5 | **关账 task** | `task_harness_theory_align_p1_v1.md` → `done/` |

---

## 3. 领域结构 Linter（首条 · 草案）

### 3.1 原则

- **机械可失败**：CI 或 pre-commit 可跑；输出非零即红。  
- **单一路径**：先覆盖 **1 个** 高频回归面（建议 `tests/` 中已有 marker 的 ChatBI 路径）。  
- **不重复**：已有 `tech_graph_contract_check` 的 SSE 事件名 **扩展字段** 优先于新脚本。

### 3.2 完成标准

- [ ] `tools/` 或 `linters/` 下脚本 + `pytest.yml` 或独立 job **至少跑通一次**  
- [ ] `PROJECT_CONFIG` 或 `docs/harness/README.md` **链入命令**  
- [ ] 文档说明：**失败时改 Harness（测/契约/manifest）而非手改绕过**

### 3.3 候选（实现 task 时三选一）

| 候选 | 价值 |
| --- | --- |
| A. ChatBI 响应 JSON 必填字段 | 对齐讲义 report structure 思想 |
| B. SSE `event:` 白名单 vs `_contract` | 与跨端契约一致 |
| C. 统一 `ErrorResponse` 必填键 | 对齐 `failure_paths` 可测 |

---

## 4. Fresh Context（Ralph 信条 1 的 Ink 版）

| 帽子 | 规则 |
| --- | --- |
| **22 / 50** | **新对话**；输入仅 task、reviews、diff 摘要、40 自检三件 |
| **40 → 50** | 必交：`diff` 要点、验收表、`### 自检结论`；**禁止**粘贴 30 思考链 |
| **30 → 22** | 22 复审时 **不** 读 invoke 全文，读 **40 + diff** |

写入各帽 md 的 **禁止什么** 小节（P1-1）。

---

## 5. 半自动与人工闸（卷三 §14）

| `semi_auto` | 适用 | 仍须人做 |
| --- | --- | --- |
| `true` | 小改动：`10→30→40→22` 链（无 pending 闸） | 终轮 **22 签收**、合并 PR、`human_gate: approved` |
| `false` | 契约/跨仓/架构 | 各 `HG-*` 按表 |

**active task** 须显式 `semi_auto` + `audit_profile`（P0 回填时一并完成；P1 抽检）。

---

## 6. 验收标准（本 SPEC 关账）

- [x] P0 已 **done**（`RECENT_TASK_SCHEDULE` §0.5 P0 勾选）  
- [x] P1-1 四份 prompt 已增补 Fresh Context 条款  
- [x] P1-3 首条 Linter **CI 绿**（PR #92 · 2026-05-29）  
- [x] P1-2 README 含半自动决策表  
- [x] `RECENT_TASK_SCHEDULE.md` **§0.5** P1 标 **done**

---

## 7. 与卷三公众稿

| 节 | P1 支撑 |
| --- | --- |
| §14 | 半自动 ≠ 全自动；`human_gate` 通俗版 |
| §14.1 | Linter 作手动门禁的 **机器替代** 示例（一句） |

需 **Linter 合并后首次绿** 数据的句子 → 标 `【待后端 P1 验收后核对】`。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-29 | 关账：PR #92 合并 · 50 复检 · RECENT §0.5 done |
| 2026-05-29 | 初版：理论对齐 P1 |
