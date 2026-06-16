# PROMPT · Cursor 串行 Task 链 · T1 · 图谱 YAML Inform 闭环（P0→P1）

> **日期**：2026-06-16  
> **Round**：T1  
> **性质**：后端仓链式常模实例 · Open **`ai-ink-brain-api-python/`**  
> **通用模板**：[PROMPT_cursor_task_chain_serial_v1.md](PROMPT_cursor_task_chain_serial_v1.md)  
> **启动块**：[PROMPT_START_SERIAL_v1.md](../invokes/by-task/graph-yaml-inform-closure-chain/PROMPT_START_SERIAL_v1.md)

---

## 0. 链概览

| # | slug | task | 分支 | freeze_id | HG-TASK-DRAFT |
| --- | --- | --- | --- | --- | --- |
| P0 | `graph-yaml-doc-hygiene-p0` | `docs/tasks/active/task_engineering_graph_yaml_doc_hygiene_p0_v1.md` | `task/graph-yaml-doc-hygiene-p0` | `GRAPH-YAML-DOC-HYGIENE-P0` | **approved** |
| P1 | `graph-yaml-export-yaml-p1` | `docs/tasks/active/task_engineering_graph_yaml_export_from_yaml_p1_v1.md` | `task/graph-yaml-export-yaml-p1` | `GRAPH-YAML-EXPORT-YAML-P1` | **approved** |

**merge_policy**：**`ci_green_merge`（强制）** — P0 PR **CI 全绿且 merge 入 `main`** 后，方可开 P1 30 / 建 P1 分支。禁止 cherry-pick 跳过 merge（除非 task 书面例外 + 维护者批）。

**帽链（每 task）**：30 → 40 → CLOSE → **PR → CI 绿 → merge**（**skip 50** · `audit_profile: post_close`）

---

## 1. GATE_SCAN

| gate_id | P0 | P1 | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | approved | approved | 2026-06-16 人签 |
| HG-REINSPECT | pending→signed @40 | pending→signed @40 | 40 自检 PASS 后标 signed |
| P0 done + merge | — | **required** | 见下 **P1 硬闸门** |

### P1 硬闸门（四项齐备 · 缺一 BLOCKED）

| # | 条件 |
| --- | --- |
| 1 | `docs/tasks/done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md` · HG-REINSPECT **signed** |
| 2 | P0 PR **GitHub Actions CI 全绿**（`tech-graph` · 合并前必绿 pytest） |
| 3 | P0 PR **已 merge 入 `origin/main`** |
| 4 | `git checkout main && git pull` 拉到 P0 merge commit |

---

## 2. P0 · 30 帽要点

**task**：`docs/tasks/active/task_engineering_graph_yaml_doc_hygiene_p0_v1.md`  
**invoke 目录**：`docs/harness/invokes/by-task/graph-yaml-doc-hygiene-p0/`

| ID | 交付 |
| --- | --- |
| D1 | `generate_sub_graph_links()` → `.graph.yaml` 编辑源链 |
| D2 | 重生成 `00_main.md` |
| D3 | QNA §已知遗留 · 幽灵节点 |
| D4 | `_tech_graph` grep 清扫 |
| D5 | pytest 防回归 |

**验收**：`pytest tests/test_graph_yaml*.py` · `--all --check` · `verify-tech-graph.sh`

---

## 3. P1 · 30 帽要点

**task**：`docs/tasks/active/task_engineering_graph_yaml_export_from_yaml_p1_v1.md`  
**invoke 目录**：`docs/harness/invokes/by-task/graph-yaml-export-yaml-p1/`

| ID | 交付 |
| --- | --- |
| D1 | YAML→graph_v2 builder |
| D2 | `build_graph_payload()` 切 YAML |
| D3 | 保留 ai 解析 · CI 不依赖 |
| D4 | manifest_check TIP 清理 |
| D5 | `99_spec` 去过渡表述 |
| D6 | export pytest + F3 回归 |
| D7 | verify-tech-graph 全绿 |

**验收**：`tech_graph_graph_export.py --check` · graph+yaml pytest · 全量 pytest

---

## 4. 40 帽（两 task 同构）

1. 独立复跑该 task 验收命令表  
2. 核对 §实现备忘与 git diff 范围  
3. 落盘 `invoke_YYYYMMDD_40_<slug>.md`  
4. 回填 task §自检结论（40 帽）  
5. HG-REINSPECT → **signed**（维护者确认或 Agent 标 PASS 后 signed）  
6. `git mv` task → `docs/tasks/done/` · 更新 `_views/done.md` · `done_by_domain.md` · RECENT §1.6 续

---

## 5. CLOSE · PR · CI · 串行纪律

```bash
# 每 task 合并前必绿
pytest tests -m "not intent_eval and not intent_benchmark"
bash scripts/verify-tech-graph.sh   # CI 对齐
```

**串行纪律（强制）**：

| 阶段 | 动作 |
| --- | --- |
| P0 | 30 → 40 → CLOSE → PR → **等 CI 绿** → **merge 入 main** → **STOP** |
| P1 | **仅在上表 P0 merge 完成后** → 从 `main` 拉最新 → 开 `task/graph-yaml-export-yaml-p1` → 30 |

**禁止**：P0 PR 未 merge 时开 P1 分支或改 export 代码。

**PR 标题建议**：
- P0：`docs(graph): Sub-graph 去 .ai.md 链 · QNA 幽灵节点遗留`
- P1：`feat(graph): graph.json export 改读 YAML · 单源闭环`

---

## 6. 链外后续

- G0 本体扫描（cyning-harness Prompt 已就绪）→ 删 `.ai.md`  
- `external_ref` schema · 幽灵节点正式建模

---

## 给 Cursor

`graph-yaml-inform-closure-chain` · `PROMPT_START_SERIAL` · `HG-TASK-DRAFT approved` · `串行` · `blocked_by` · `post_close` · `skip 50`
