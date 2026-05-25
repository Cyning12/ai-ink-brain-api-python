# docs/spec（后端 SDD 规格目录）

> **性质**：**行为/架构规格**（SDD）真值；与 `docs/tasks/`（执行单）、`docs/harness/`（过程工件）、`docs/_tech_graph/`（拓扑）分工。  
> **排期**：近期治理与 Wiki 实验见 [`governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](./governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)；任务级顺序见 [`../tasks/RECENT_TASK_SCHEDULE.md`](../tasks/RECENT_TASK_SCHEDULE.md)。

---

## 目录

| 目录 / 文件 | 领域 | 说明 |
| --- | --- | --- |
| [`v3-agent/`](./v3-agent/README.md) | ChatBI V3 | L0 `SPEC-ChatBI-V3-Overview` + L1 子规（**主业务线**） |
| [`v2-agent/`](./v2-agent/README.md) | ChatBI V2 | 冻结参考 |
| [`governance/`](./governance/README.md) | 治理 / Harness / Wiki | **2026-05 起** 非功能需求与推广顺序 |
| [`SPEC-ChatBI-Enterprise-Gap.md`](./SPEC-ChatBI-Enterprise-Gap.md) | 企业差距 | 跨版本差距表 |

---

## 新建 SPEC 约定

- **业务功能**：`docs/spec/v3-agent/SPEC-<域>-<主题>.md`，在 `v3-agent/README.md` 登记。  
- **治理 / 跨-cutting**：`docs/spec/governance/SPEC-Governance-<主题>-v1.md`。  
- **不**把 Harness invoke/review 全文写入 SPEC；过程真值在 `docs/harness/`；蒸馏进 **`docs/coding_wiki/`**（试点）。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | 初版：根 README；新增 `governance/` 索引 |
