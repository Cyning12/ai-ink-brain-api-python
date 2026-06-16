# HumanGate · HG-GRAPH-P0-SIGNOFF（图谱 YAML P0 · 00_main 关账）

> **用途**：维护者 **关账前逐项勾选**；**非 Agent 代签**。  
> **全勾 + task 内 gate approved 后** → `git mv` → `docs/tasks/done/`。  
> **关联 task**：[`task_engineering_graph_yaml_p0_00_main_v1.md`](../../../tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md)

| 字段 | 值 |
| --- | --- |
| **gate_id** | `HG-GRAPH-P0-SIGNOFF` |
| **blocks** | task → done · P1 立项 · cyning-harness 回灌评估 |
| **前置** | `HG-REINSPECT` = approved · 50 reinspect 已落盘 |

---

## §0 维护者签收（关账最后一行）

| 项 | 勾选 |
| --- | --- |
| 我已完成下表 **§1–§5** 全部 applicable 项 | [ ] |
| 我确认 **HG-REINSPECT** 已在 task 人工闸表改为 `approved` | [ ] |
| 我将把 **HG-GRAPH-P0-SIGNOFF** 改为 `approved` 并执行 `git mv` | [ ] |
| **签收日期** | YYYY-MM-DD |
| **签收人** | |

---

## §1 帽链与落盘（Agent 填 · 维护者核）

| # | 项 | 路径 / 证据 | 维护者 ✓ |
| --- | --- | --- | --- |
| 1 | 10 invoke + R0–R5 闭合 | `invokes/by-task/graph-yaml-p0-00-main/invoke_*_10_*` | [ ] |
| 2 | 22 R1 review | `reviews/by-task/graph-yaml-p0-00-main/*_audit_R1_*` | [ ] |
| 3 | HG-AUDIT-R1 approved | task 人工闸表 | [ ] |
| 4 | 30 invoke | `invoke_*_30_*` | [ ] |
| 5 | 40 自检 | task `### 自检结论` | [ ] |
| 6 | 50 reinspect | `docs/tasks/reinspect_results/task_graph-yaml-p0-00-main_*` | [ ] |
| 7 | HG-REINSPECT approved | task 人工闸表 | [ ] |
| 8 | CLOSE trace | HANDOFF_CLOSE_TRACE 或 invoke CLOSE | [ ] |
| 9 | ### KPI（00） | task 内已填 · 非占位 | [ ] |

---

## §2 P0 交付物（技术 · 维护者核）

| # | 验收项 | 证据（命令/路径） | 维护者 ✓ |
| --- | --- | --- | --- |
| 1 | `00_main.graph.yaml` 存在且可解析 | 路径 + `python -c "import yaml"` 或脚本 `--check` | [ ] |
| 2 | 转换脚本可生成 `00_main.md` | 命令 + 退出码 0 | [ ] |
| 3 | `00_main` 与 `graph.json` 一致或 **书面例外**（§2.1） | diff 脚本输出 | [ ] |
| 4 | pytest 用例 ≥1 绿 | `pytest tests/...` | [ ] |
| 5 | **未** 删除 `00_main.ai.md` | `git ls-files` | [ ] |
| 6 | **未** 引入 `.cyning-harness/` | 无 manifest | [ ] |
| 7 | CI / workflow 绿（若改 CI） | PR checks | [ ] |

### §2.1 图谱 diff 例外（仅当有 intentional diff 时填）

| 节点/边 ID | 原因 | 是否已更新 graph.json |
| --- | --- | --- |
| （无则写「无例外」） | | |

---

## §3 非范围确认（维护者 ✓）

- [ ] 未对 `10_flow_*.ai.md` 做 YAML 迁移（P1 另 task）
- [ ] 未在本 task 执行 `npx @cyning/harness init`
- [ ] 未改 `ai-ink-brain` 前端仓
- [ ] 未将未评审 schema 写入 cyning-harness 产品仓

---

## §4 后续动作（关账后 · 非阻塞）

| 动作 | 负责 | 目标日期 |
| --- | --- | --- |
| P1：`10_flow_rag` YAML 试点 | engineering task | |
| cyning-harness `graph compile` 回灌评估 | 工作区 Epic / v1.1 | |
| 更新 QNA §修订记录 · synthesis wiki | coding_wiki | |
| AGENTS §7 双轨规范修订（废 .ai.md） | 工作区 · P2 后 | |

---

## §5 task 文件改动清单（关账时人工执行）

| 步骤 | 文件 | 位置 | 改什么 |
| --- | --- | --- | --- |
| 1 | `docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md` | `### 人工闸` · **HG-GRAPH-P0-SIGNOFF** | `pending` → **`approved`** |
| 2 | 同上 | 文首 `> 状态` | **`done`** |
| 3 | Git | — | `git mv docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md docs/tasks/done/` |
| 4 | `docs/tasks/_views/done.md` | 索引 | 追加一行 |

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-16 | 初版 · 00→10→50→双 gate 关账 |
