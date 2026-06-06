# explore · C1–C3 差分报告 · gov-docs-noise P0

> **日期**：2026-06-06  
> **task**：`docs/tasks/active/task_gov_docs_noise_p0_readme_v1.md`  
> **SPEC**：§8.1 P0-1/2/3  
> **只读核对**；未改业务 README。

---

## Summary

三处冲突均 **可修、无阻塞**。C1 存在「reviews 已移除」误表述；C2 `docs/README` §1 仍推 `flows/` 为端到端主入口，与 AGENTS L0 `_tech_graph` 不一致；C3 `docs/tech_graph/` 仅 2 份 gate 留痕、无 README，易与 `docs/_tech_graph/` 混淆。

---

## C1 · `docs/harness/invokes/README.md`

| 维度 | 现状 | 期望（SPEC §8.1 P0-1） |
| --- | --- | --- |
| L25 | 「**不**使用已移除的 `harness/reviews/`」 | 删除「已移除」类表述 |
| 分工 | 仅提 20→`review_results/` | 22→`docs/harness/reviews/`；20→`review_results/`；50→`reinspect_results/` |
| 真值对照 | 与 `reviews/README.md` §「与 20 / 50 分工」矛盾 | 与 reviews/README 一致 |

**reviews/README 真值**（L31–37）：

| 帽 | 目录 |
| --- | --- |
| 20 | `docs/tasks/review_results/` |
| 22 | **本目录** |
| 50 | `docs/tasks/reinspect_results/` |

---

## C2 · `docs/README.md` §1

| 维度 | 现状 | 期望（SPEC §8.1 P0-2） |
| --- | --- | --- |
| L13 | 「理解端到端怎么跑」→ 读 `docs/flows/` | 端到端 **优先** `docs/_tech_graph/` |
| flows 定位 | 与 tasks/meta 并列，未标 Legacy | `docs/flows/` 标 **历史快照 · Legacy · 非 L0** |
| AGENTS 对照 | AGENTS §必读 L3 推 `_tech_graph` | 本 task **不改 AGENTS**（留 P2） |

---

## C3 · `docs/tech_graph/`

| 维度 | 现状 | 期望（SPEC §8.1 P0-3） |
| --- | --- | --- |
| 目录内容 | 2 文件：`gate_a_scheme1_backend.md`、`gate_a_scheme1_perf_compare_backend_detail.md` | 保留不动 |
| README | **不存在** | 新建 `docs/tech_graph/README.md` |
| 用途说明 | 无 | POINTER → `docs/_tech_graph/`；gate 两份 md 为闸口留痕、**非 L0** |

---

## Blockers

无。human_gate `HG-TASK-DRAFT`、`HG-GOV-P0-EXEC` 均为 `approved`。

---

## 建议 30 帽改动清单

1. **C1**：重写 `invokes/README.md`「规则（摘要）」第 3 条为 22/20/50 分工表；删除「已移除」措辞。
2. **C2**：在 `docs/README.md` §1 新增 `_tech_graph` 端到端优先 bullet；将 flows bullet 改为 Legacy 历史快照。
3. **C3**：新建 `docs/tech_graph/README.md`（POINTER + gate 留痕说明 + 链至 `_tech_graph/`）。
4. **SPEC 导图**：`docs/spec/governance/docs-noise-inventory/README.md` §3 C1/C2/C3 → `done`。
5. **task**：回填「### 自检结论（执行者）」。
