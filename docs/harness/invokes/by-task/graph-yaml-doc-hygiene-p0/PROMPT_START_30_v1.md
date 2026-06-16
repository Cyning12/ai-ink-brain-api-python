# 启动 Prompt · 30 执行 · graph-yaml-doc-hygiene-p0

> **用法**：Open Folder **`ai-ink-brain-api-python/`** → 新对话 → 复制下方代码块。  
> **人签**：**HG-TASK-DRAFT approved**（2026-06-16）  
> **串行链**：**#1/2** — 完整串行见 [`PROMPT_START_SERIAL_v1.md`](../graph-yaml-inform-closure-chain/PROMPT_START_SERIAL_v1.md)  
> **前置**：Post-Epic 修复 **done** · [`task_engineering_graph_yaml_post_epic_fix_v1.md`](../../../tasks/done/task_engineering_graph_yaml_post_epic_fix_v1.md)

| 项 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-doc-hygiene-p0` |
| **git_branch** | `task/graph-yaml-doc-hygiene-p0` |
| **test_strategy** | `required` |
| **freeze_id** | `GRAPH-YAML-DOC-HYGIENE-P0` |

---

```text
你是 **30 执行 Agent**（Ink 后端仓 · 图谱 YAML 文档卫生 P0）。

【开帽 · GATE_SCAN】
- HG-TASK-DRAFT: **approved** ✓
- cwd: ai-ink-brain-api-python/
- 分支: task/graph-yaml-doc-hygiene-p0（无则创建）
- **禁止** 开 P1（export-yaml）直到本 task 40 CLOSE

严格遵循：
- docs/tasks/active/task_engineering_graph_yaml_doc_hygiene_p0_v1.md（D1–D5 · 非范围）
- docs/harness/prompts/hats/30-execute-code.md
- AGENTS.md

---

## 真值问题（必须修复）

### D1 · Sub-graph 仍链 `.ai.md`
`scripts/graph_yaml_compile.py` · `generate_sub_graph_links()`（约 L170）仍输出：
  （[AI 协议版](10_flow_rag.ai.md)）
与 `99_spec`「YAML 编辑源 · .ai.md deprecated」矛盾。

**修复**：改为 `（编辑源：[10_flow_rag.graph.yaml](10_flow_rag.graph.yaml)）` 格式（7 张子流程均改）。

### D2 · 重生成 00_main.md
```bash
python scripts/graph_yaml_compile.py --graph-id 00_main
```
确认 Sub-graph Links 段已更新；`--check --graph-id 00_main` exit 0。

### D3 · QNA 幽灵节点遗留
在 `docs/_tech_graph/QNA_graph_wiki_history_upgrade_v1_zh.md` 增小节 **§已知遗留 · 幽灵节点**（1～3 句）：
- YAML/graph.json 边可引用未在 nodes 声明的节点（如 AUTH、FTS）
- 继承历史设计 · 非 compile bug
- `external_ref` schema 另 task
修订记录增 v1.2 行。

### D4 · grep 清扫
```bash
rg '\.ai\.md' docs/_tech_graph --glob '!*.ai.md'
```
除 `@deprecated` 注释外，正文不得将 `.ai.md` 标为编辑源；发现则改 pointer，清单写入 task §实现备忘。

### D5 · pytest 防回归
`tests/test_graph_yaml_compile.py` 新增：
`test_00_main_subgraph_links_no_ai_md_href`
断言 `generate_md(load_yaml('00_main'))` 的 Sub-graph 段不含 `.ai.md`。

---

## 非范围（STOP 若越界）

- 不改 `tools/tech_graph_graph_export.py`（→ P1）
- 不改 `tech_graph_manifest_check.py` TIP（→ P1）
- 不删 `.ai.md` · 不改 graph.json 拓扑

---

## 验收命令（须全绿）

```bash
pytest tests/test_graph_yaml_compile.py -q
python scripts/graph_yaml_compile.py --all --check
bash scripts/verify-tech-graph.sh
pytest tests -m "not intent_eval and not intent_benchmark" -q
ruff check api tests
```

---

## 关账交付

1. 回填 task §实现备忘 · §自检结论
2. 落盘 invoke：`docs/harness/invokes/by-task/graph-yaml-doc-hygiene-p0/invoke_YYYYMMDD_30_*.md`
3. 40 自检 → HG-REINSPECT → task `git mv` → `docs/tasks/done/`
4. 更新 `docs/tasks/_views/done.md` · `RECENT_TASK_SCHEDULE` §1.6 续
5. **STOP** · 等 P0 PR **CI 绿 + merge** · **不得**在同会话开 P1（见串行链硬闸门）
```

---

## 40 自检清单（供下一对话）

- [ ] Sub-graph 源码 + `00_main.md` 无 `.ai.md` href
- [ ] QNA v1.2 + §已知遗留
- [ ] 新 pytest 绿
- [ ] verify-tech-graph 全绿
