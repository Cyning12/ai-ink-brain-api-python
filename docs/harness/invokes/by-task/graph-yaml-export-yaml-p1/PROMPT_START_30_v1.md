# 启动 Prompt · 30 执行 · graph-yaml-export-yaml-p1

> **用法**：Open Folder **`ai-ink-brain-api-python/`** → 新对话 → 复制下方代码块。  
> **人签**：**HG-TASK-DRAFT approved**（2026-06-16）  
> **硬闸门**：须 **P0 PR CI 全绿且已 merge 入 `main`** 后再开 30（见 task §P1 硬闸门）  
> **串行链**：**#2/2** — 常模 [`PROMPT_START_SERIAL_v1.md`](../graph-yaml-inform-closure-chain/PROMPT_START_SERIAL_v1.md)  
> **blocked_by**：P0 → `docs/tasks/done/` + HG-REINSPECT + **merge**

| 项 | 值 |
| --- | --- |
| **task_slug** | `graph-yaml-export-yaml-p1` |
| **git_branch** | `task/graph-yaml-export-yaml-p1` |
| **test_strategy** | `required` |
| **freeze_id** | `GRAPH-YAML-EXPORT-YAML-P1` |

---

```text
你是 **30 执行 Agent**（Ink 后端仓 · graph.json 导出改读 YAML · P1）。

【开帽 · GATE_SCAN · P1 硬闸门 · 四项齐备缺一 STOP】
- HG-TASK-DRAFT: **approved** ✓
- docs/tasks/done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md 存在 · HG-REINSPECT signed
- **P0 PR CI 全绿**（GitHub Actions · tech-graph + 合并前必绿 pytest）
- **P0 PR 已 merge 入 origin/main**
- `git checkout main && git pull` 后 `git log -1 --oneline` 含 P0 merge
- 任一不满足 → STOP · 只报缺哪一项 · **不得改 export 代码**
- cwd: ai-ink-brain-api-python/
- 分支: task/graph-yaml-export-yaml-p1（无则创建 · 基于最新 main）

严格遵循：
- docs/tasks/active/task_engineering_graph_yaml_export_from_yaml_p1_v1.md（D1–D7 · 非范围）
- docs/harness/prompts/hats/30-execute-code.md
- AGENTS.md

---

## 真值问题

CI 仍 `tech_graph_graph_export.py --check` 读 ***.ai.md** Mermaid，与 YAML 编辑源脱节。
目标：`build_graph_payload()` 默认自 7× `.graph.yaml` 构建 graph_v2，--check 与已提交 graph.json 语义一致。

---

## 执行项（D1–D7）

### D1 · YAML→graph_v2 builder
新增模块（建议 `tools/tech_graph_graph_v2_yaml.py`）：
- 遍历 `scripts/graph_yaml_compile.all_graph_ids()` 或 `*.graph.yaml`
- 合并 nodes/edges/anchors 为 graph_v2 载荷
- 边 type/sync 复用 `tech_graph_graph_export._classify_label` 或等价逻辑

### D2 · 切换 export 主路径
`tools/tech_graph_graph_export.py` · `build_graph_payload()` 改调 YAML builder。
更新 CLI description / 模块 docstring（不再写「仅 *.ai.md」）。

### D3 · 保留 ai 解析供单测
`_iter_ai_md_files` / Mermaid 解析 **不删**，但 CI 主路径不依赖。

### D4 · manifest_check TIP
`tools/tech_graph_manifest_check.py` L487–492：
移除「同步 00_main.ai.md auto 区块」TIP → 改为 `_manifest.json` / YAML 编辑提示。

### D5 · 99_spec
§机器轨：`graph.json` 由 **YAML export** 生成；删除「export 仍为过渡方案」歧义句。

### D6 · pytest
- `tests/test_tech_graph_graph_export.py`：`--check` exit 0
- **F3 回归**：tmp fixture 故意改 `.ai.md` Mermaid，export 结果 **不变**（证明 YAML 权威）

### D7 · verify-tech-graph
步骤顺序不变 · 全绿。

---

## 非范围（STOP）

- 不删 `.ai.md`
- 不手改 graph.json 拓扑（除非 export bug · 须书面说明）
- 不做 external_ref schema
- 不改 P0 已改的 Sub-graph 模板

---

## 实现顺序建议

1. 写 YAML builder + 单测（对照当前 graph.json）
2. 切换 build_graph_payload
3. `--check` 绿后再改 manifest TIP / 99_spec
4. 加 F3 回归测试

---

## 验收命令

```bash
python tools/tech_graph_graph_export.py --check
python scripts/graph_yaml_compile.py --all --check
pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q
bash scripts/verify-tech-graph.sh
pytest tests -m "not intent_eval and not intent_benchmark" -q
ruff check api tests
```

---

## 关账交付

1. 回填 task §实现备忘 · §自检结论
2. invoke 30/40 落盘于 `docs/harness/invokes/by-task/graph-yaml-export-yaml-p1/`
3. HG-REINSPECT → task → `done/` · 更新 RECENT §1.6 续
4. 可选：在 QNA / RECENT 标注「Inform YAML 单源闭环完成 · 删 .ai.md 待 G0」
```

---

## 前置检查（开 30 前 · 须全过）

```bash
test -f docs/tasks/done/task_engineering_graph_yaml_doc_hygiene_p0_v1.md || { echo "STOP: P0 未 done"; exit 1; }
git checkout main && git pull
# 人工/Agent：确认 P0 PR 已 merge · CI 全绿（gh pr view / Actions）
echo "OK: 可开 P1 30"
```
