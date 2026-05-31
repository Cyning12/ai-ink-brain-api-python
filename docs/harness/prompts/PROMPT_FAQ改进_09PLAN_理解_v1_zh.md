# Prompt · 理解 FAQ 改进方案（09 PLAN）并执行 Batch A

> **用途**：后端 Agent **开工前** 读本文 + 链内文档，理解「三卷发表后读者 FAQ → Ink 后端改进项」全貌，再动 `api/` / CI / Harness。  
> **真值规划**：治理仓 [`ai_coding_governance/09_PLAN_Ink后端改进方案_可推广_v1_zh.md`](../../../../ai_coding_governance/09_PLAN_Ink后端改进方案_可推广_v1_zh.md)  
> **合成结论**：[`SUMMARY_三卷读者FAQ_完整结论_20260530_v1_zh.md`](../../../../ai_coding_governance/narrative/reviews/SUMMARY_三卷读者FAQ_完整结论_20260530_v1_zh.md)

---

## 你的角色

你是 **Ink 后端（ai-ink-brain-api-python）** 执行 Agent。当前任务类型：**FAQ 驱动的工程补齐**（非重写方法论）。  
**Open Folder**：本仓根。跨仓只读治理仓 `ai_coding_governance/narrative/reviews/` 与 `09_PLAN`，**禁止**改工作区 `Projects/docs/harness/`。

---

## 必须先建立的结论（30 秒）

1. **方法论不 redesign**：Harness 三支柱、`.ai.md`→export 双轨图谱、manifest/contract CI、`human_gate` + 50 — **保持不变**。  
2. **读者误读要纠**：冷/温/热 ≠ 架构/契约/实现 → 见本仓 [`../guides/GUIDE_冷温热层_对内术语_v1_zh.md`](../guides/GUIDE_冷温热层_对内术语_v1_zh.md)。  
3. **本批要做**：降低合并摩擦 + CI 红字可读 + 模板可复制 — **IMP-B Batch A**（见下）。  
4. **明确不做**：`graph.auto.json` 全仓扫描、PR `/approve` 唯一合闸、维护成本归零、merge 模型 KPI。

---

## 阅读顺序（按序打开）

| 序 | 文档 | 目的 |
|----|------|------|
| 1 | 本仓 [`AGENTS.md`](../../../AGENTS.md) | 地图与禁止项 |
| 2 | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) | 契约/目录/安全 |
| 3 | 治理仓 **SUMMARY** §2、§5、§10 | FAQ 合成结论与五条原则 |
| 4 | 治理仓 **09_PLAN** §1～§3 | 缺口、IMP-B 全表、批次 A/B/C |
| 5 | 本仓 **active task** | [`docs/tasks/active/task_backend_improve_batch_a_p0_v1.md`](../../tasks/active/task_backend_improve_batch_a_p0_v1.md)（**draft** · Batch A） |
| 6 | 动 CI/契约时：[`GUIDE_续卷编写_Ink后端真值对照_v1_zh.md`](../../../../ai_coding_governance/narrative/GUIDE_续卷编写_Ink后端真值对照_v1_zh.md) §3 | workflow/命令真值 |

**不必读**：`docs/diary/` 全文、`invokes/` 扁平扫描、Public 公众稿粘贴版。

---

## FAQ → 后端改进项（IMP-B 全表 · 状态以 task 为准）

### Batch A · P0（优先）

| ID | 做什么 | 交付物 |
|----|--------|--------|
| IMP-B-01 | manifest/contract CI **三段式 stderr** + Runbook | `tools/tech_graph_*_check.py` · `docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md` |
| IMP-B-02 | 改 task 时 CI 跑 `task_validate` | `verify-fast.yml` 或 `tech-graph.yml` |
| IMP-B-10 | Ink 轨 **PR 模板** | `.github/pull_request_template.md` |
| IMP-B-11 | **22 帽 Blocking 表** | `prompts/hats/22-task-audit.md` §Blocking |
| IMP-B-20 | **冷/温/热术语卡** | `docs/harness/guides/GUIDE_冷温热层_对内术语_v1_zh.md` |

### Batch B · P1

IMP-B-03 L2 manifest SPEC 关账 · IMP-B-04 领域 Linter · IMP-B-12 Test plan 分层 · IMP-B-13 存量 task 抽样 · IMP-B-21 合并入口图 · IMP-B-30/31 failure-cases + 复盘模板

### Batch C · P2

IMP-B-05 增量 manifest · IMP-B-14 Delta→spec · IMP-B-22 卷四对内样例 PR

---

## 执行纪律（FAQ 约束）

| 约束 | 要求 |
|------|------|
| 成本 | 新流程 **不** 使稳态额外耗时 >15%；不加专职岗 |
| 高敏 | 动 `api/` → `test_strategy: required` + **50 落盘**；小团队可角色兼任，**不可删步骤** |
| 合并 | **同 PR** 提交代码 + manifest/`.ai.md`（若触达）；禁止 merge 后 bot 单独改图 |
| 签收 | 闸在 **`reviews/` / `reinspect_results/` + human_gate**；PR 模板 **辅助**，不替代 |
| 测试 | 合并前：`pytest tests -m "not intent_eval and not intent_benchmark"` |

---

## 开工检查清单

- [ ] 已读 active task 的 **非范围** 与 **验收**  
- [ ] 改动范围 **仅** task 所列 IMP-ID  
- [ ] 未引入 FAQ **已拒绝** 方案（见 SUMMARY §3 拒绝列）  
- [ ] 若改 CI：本地或 PR 上 **故意红一次** 验证 stderr/Runbook  
- [ ] 关账：22 review 落盘 + pytest 绿 + task → done 流程

---

## 输出要求

1. **变更摘要**：按 IMP-ID 列出文件与行为。  
2. **未做项**：Batch A 中本轮 **刻意不做** 的 ID 及原因。  
3. **公众稿**：**不** 把本 Prompt 或 governance reviews 整段复制进 PR/对外仓库。  
4. **图谱**：若动 `api/` 或锚点，同步 `_manifest` / 契约 fixture / `.ai.md`（同 PR）。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-05-30 | FAQ Batch A kickoff；链 09_PLAN + SUMMARY |
