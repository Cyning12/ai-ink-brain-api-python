# Task · 图谱 YAML Epic 后修复（Post-Epic Fix）

> **状态**：`done`（**HG-REINSPECT signed** · 2026-06-16 关账）  
> **前置 Epic**：`[task_engineering_graph_yaml_migration_epic_v1.md](../done/task_engineering_graph_yaml_migration_epic_v1.md)` · **done**  
> **复查依据**：2026-06-16 维护者复查 · YAML↔JSON 一致 · `--all` bug · CI 双源 · 文档漂移  
> **invoke**：`[PROMPT_START_30_v1.md](../harness/invokes/by-task/graph-yaml-post-epic-fix/PROMPT_START_30_v1.md)`

---

## Harness 元信息


| 字段                     | 值                                         |
| ---------------------- | ----------------------------------------- |
| **task_slug**          | `graph-yaml-post-epic-fix`                |
| **test_strategy**      | `required`                                |
| **test_strategy_note** | 修 `--all` + CI 步骤 + 7 图 compile 一致性       |
| **audit_profile**      | `post_close`                              |
| **orchestration**      | `Claude Code`（30→40，50 可选 · task 明示 skip） |
| **git_branch**         | `task/graph-yaml-post-epic-fix`           |
| **worktree_root**      | `ai-ink-brain-api-python/`                |
| **freeze_id**          | `GRAPH-YAML-POST-EPIC-FIX`                |


### 人工闸


| human_gate_id     | status  | blocks_hats | 说明                                                          |
| ----------------- | ------- | ----------- | ----------------------------------------------------------- |
| **HG-TASK-DRAFT** | **approved** | 30          | 范围与非范围人签                                                    |
| **HG-REINSPECT**  | **signed** | done        | 40 复检通过 · 本 task skip 50（纯工具+文档 · audit_profile: post_close） |


---

## 背景与目标

Epic YAML 迁移已关账（7×`.graph.yaml` · pytest 62 绿 · 逐图 `--check` 绿）。复查发现 **Inform 闭环仍有缺口**：

1. `graph_yaml_compile.py --all --check` **因 `all_graph_ids()` stem 错误而失败**
2. `**10_flow_rag.md` Mermaid 与当前 YAML 编译结果不一致**（锚点行数 16 vs 13）
3. **CI `verify-tech-graph.sh` 仍仅 export 自 `.ai.md`**，未校验 YAML 单源
4. `**99_spec.md` 等仍写「机器轨 = `.ai.md`」**，与 Epic 编辑源声明冲突

**完成态**：工具与 CI 认 YAML；7 张 `.md` 与 YAML 同步；规约文档更新；**不删** `.ai.md`、**不改** `graph.json` 拓扑。

---

## 范围

- [x] **D1** 修复 `scripts/graph_yaml_compile.py` · `all_graph_ids()`（`*.graph.yaml` → graph_id 不含 `.graph`）
- [x] **D2** 新增/扩展 pytest：`--all --check` exit 0
- [x] **D3** `python scripts/graph_yaml_compile.py --all` 重生成 7 张 `.md`（仅 `generated_at` 与 Mermaid/notes 漂移）
- [x] **D4** `scripts/verify-tech-graph.sh` 增加 YAML 校验步骤（在 export 前或后 · 见 invoke）
- [x] **D5** 更新 `docs/_tech_graph/99_spec.md` §机器轨表述（编辑源 YAML · `.ai.md` deprecated · export 过渡）
- [x] **D6** 更新 `docs/_tech_graph/99_mermaid_protocol.md` · `QNA_graph_wiki_history_upgrade_v1_zh.md` 相关节（最小 diff）
- [x] **D7** 检查 `15_e2e_boundary.md` / `.graph.yaml` 内对 `.ai.md` 的正文引用 → 改 pointer 到 `.md` 或 `notes`

## 非范围

- **不** 删除任意 `.ai.md`（G0 扫描前置 · 另 task）
- **不** 改 `tools/tech_graph_graph_export.py` 读 YAML（另 task · export 迁移）
- **不** 手改 `graph.json` 节点/边
- **不** 引入 `.cyning-harness/`
- **不** 幽灵节点 schema（`external_ref`）— 仅可在 QNA 加一行「已知遗留」

---

## 失败路径


| #   | Scenario ID            | 触发                       | 行为                  |
| --- | ---------------------- | ------------------------ | ------------------- |
| F1  | `fp-all-check-regress` | `--all --check` 失败       | exit 1 · CI 红       |
| F2  | `fp-md-mermaid-drift`  | 重编译后 pytest mermaid 对齐失败 | 修 YAML 或 compile 逻辑 |


---

## 验收标准

- [x] `python scripts/graph_yaml_compile.py --all --check` → **exit 0**
- [x] 7 张 `.md` 的 Mermaid body（忽略 `generated_at`）与 fresh compile **一致**
- [x] `pytest tests/test_graph_yaml*.py -q` 全绿
- [x] `bash scripts/verify-tech-graph.sh` 全绿（本地可 skip human_gate 步若 git 不可用 · CI 须绿）
- [x] `99_spec` 机器轨表述已更新 · 无「唯一真值仍是 .ai.md」歧义
- [x] task §自检结论已填 · invoke 30/40 落盘

**合并前必绿**：`pytest tests -m "not intent_eval and not intent_benchmark"`

---

## 实现备忘（30 回填）


| 路径 | 说明 |
| ---------------------------------- | --- |
| `scripts/graph_yaml_compile.py` | D1：修复 `all_graph_ids()` 用 `p.name[:-11]` 取 graph_id；同步修复 `format_anchor_comment()` 渲染裸 `path` 锚点 |
| `scripts/verify-tech-graph.sh` | D4：在 `tech_graph_graph_export.py --check` 前增加 `graph_yaml_compile.py --all --check` |
| `tests/test_graph_yaml_compile.py` | D2：新增 `test_all_graph_ids_returns_seven_ids_without_graph_suffix`、`test_compile_all_check_mode_exits_zero` |
| `tests/test_graph_yaml_p*.py` | D2：锚点格式正则允许裸 `path`（`(?:#L\d+\|::\w+)?`） |
| `docs/_tech_graph/*.md` | D3：7 张 `.md` 由脚本重生成（仅 `generated_at` 与裸 path 锚点漂移） |
| `docs/_tech_graph/15_e2e_boundary.graph.yaml` | D7：`notes` 中 `14_runtime_observability.ai.md` → `.md` |
| `docs/_tech_graph/99_spec.md` | D5：§机器轨 更新为「YAML 编辑源 · `.ai.md` deprecated · export 过渡」 |
| `docs/_tech_graph/99_mermaid_protocol.md` | D6：双轨制表与转换方向更新为 YAML 源 |
| `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` | D6：修订记录新增 v1.1 行 |
| `docs/harness/invokes/by-task/graph-yaml-post-epic-fix/invoke_20260616_30_graph-yaml-post-epic-fix.md` | 30 invoke 落盘 |
| `docs/harness/invokes/by-task/graph-yaml-post-epic-fix/invoke_20260616_40_graph-yaml-post-epic-fix.md` | 40 invoke 落盘 |


### 自检结论（30 帽）


| # | 命令 | 退出码 | 摘要 |
| --- | ------- | --- | --- |
| 1 | `pytest tests/test_graph_yaml*.py -q` | 0 | 64 passed |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7 graph 全 OK |
| 3 | `bash scripts/verify-tech-graph.sh` | 0 | 全步骤 OK |
| 4 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | 0 | 416 passed, 1 skipped, 2 deselected |
| 5 | `ruff check api tests` | 0 | All checks passed |


### 自检结论（40 帽回填）

| # | 命令 | 退出码 | 摘要 |
| --- | --- | --- | --- |
| 1 | `pytest tests/test_graph_yaml*.py -q` | 0 | 64 passed |
| 2 | `python scripts/graph_yaml_compile.py --all --check` | 0 | 7 graph 全 OK |
| 3 | Mermaid body vs `generate_md()`（7 图） | — | 7/7 无 drift |
| 4 | `bash scripts/verify-tech-graph.sh` 核心步 | 0 | manifest → yaml check → export → drift → equiv 全绿 |

**结论**：**PASS** · merge `f12e2a6` · HG-REINSPECT signed · 50 skip

---

## 修订记录


| 日期         | 说明              |
| ---------- | --------------- |
| 2026-06-16 | 关账 · 40 复检 PASS · task → `done/` |
| 2026-06-16 | 初稿 · Epic 复查后修复 |


