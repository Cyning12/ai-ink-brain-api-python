# 启动 Prompt · 10 需求 + R0–R5 思考 · graph-yaml-p0-00-main

> **用法**：由 **00 总调度** 派发 · 或 HG-TASK-DRAFT 已签后直接开此对话。  
> **Open Folder**：`ai-ink-brain-api-python/`  
> **task**：[`task_engineering_graph_yaml_p0_00_main_v1.md`](../../../tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md)

---

```text
你正在扮演 **10 需求 / 任务分析 Agent**（含高复杂度 R0–R5 思考轮）。

严格遵循：
- docs/harness/prompts/hats/10-requirements.md（§思考轮 · §下一棒 A/B）
- docs/tasks/active/task_engineering_graph_yaml_p0_00_main_v1.md
- docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md

【开帽】确认：
- HG-TASK-DRAFT = approved（否则 STOP · 只报 gate_id）
- 非范围：不接 cyning-harness · P0 不删 .ai.md · 仅 00_main

---

## 阶段 A · 读真值（R0 材料）

在 cwd 阅读并摘要（各 ≤5 行）：
1. docs/_tech_graph/00_main.ai.md
2. docs/_tech_graph/00_main.md
3. docs/_tech_graph/graph.json 中 graph_id=00_main 的 nodes/edges
4. docs/_tech_graph/99_mermaid_protocol.md（边标记）
5. docs/_tech_graph/graph_v2_schema.md

---

## 阶段 B · R0–R5 逐轮回填

将结论写入 task §思考轮次对应槽位 + 更新「思考轮控制」表。

### R0 · 读 task / QNA / 非范围
- task 范围/非范围是否清晰？缺口清单？

### R1 · 代码与图谱事实
- 00_main 节点数/边类型/锚点路径
- 现有 CI 如何触达 graph（tech-graph workflow 若有则引用）

### R2 · 方案对比（≥2 方案 + 推荐）
至少对比：
- **方案 1**：YAML 源 → Python 生成 .md + 校验 graph.json
- **方案 2**：YAML 源 → 直接 emit graph.json 子集 + 再生成 .md
- **方案 3**（可选）：JSON 源替代 YAML
给出推荐 + 弃选理由 · P0 最小 diff

### R3 · 边界 / CI / failure_paths
- F1/F2/F3 是否可操作
- pre-commit vs CI only
- 与 _manifest 是否需联动（P0 建议：否）

### R4 · pytest / 命令表
列出 30/40 须跑的命令（占位符填真实路径）：
- python scripts/graph_yaml_compile.py --check
- pytest tests/test_graph_yaml_*.py
- （可选）现有 graph CI 命令

### R5 · 图谱增量 · P1 · 关账
- P0 完成后 P1 迁移哪张 flow
- 何时回灌 cyning-harness（v1.1+）
- 关账条件与 HG-GRAPH-P0-CLOSE 对齐

**思考轮控制**（必填）：
- actual_last_round
- early_stop（若 R3 已收敛可 yes + reason + residual_risks）
- 禁止留「待填」却宣称完成

---

## 阶段 C · 下一棒 A/B（硬）

1. **推荐判定**（1–3 行）：本 task 推荐 **路径 A（22）**（audit_profile: full · test_strategy: required）
2. **路径 A 全文**：TEMPLATE-task-audit-invoke §3（占位符已替换）
3. **路径 B 全文**：TEMPLATE-execute-invoke §3（占位符已替换）

---

## 阶段 D · 落盘

1. invoke：docs/harness/invokes/by-task/graph-yaml-p0-00-main/invoke_YYYYMMDD_10_graph-yaml-p0-00-main.md
2. 更新 task 正文（思考轮 + 必要时微调验收标准）
3. commit（HANDOFF_AUTO_COMMIT · 分支 task/graph-yaml-p0-00-main）

禁止：写 30 实现代码 · 接 cyning-harness · 删 .ai.md

关键词：10、R0-R5、00_main、YAML、graph-yaml-p0
```
