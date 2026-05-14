# 闸口 A（方案1）— 后端仓 `ai-ink-brain-api-python`：现状 vs 静态 `graph.json`

> 对应规划：工作区 `docs/tech_graph/改进方向.md` 闸口 A；SPEC：`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`  
> `freeze_id`：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`（与前端 task **同一行**；bump 时双仓同改）

## 指标（最低集）

| 指标 | 方法 / 观察 |
| --- | --- |
| 解析正确性 | `pytest tests/test_tech_graph_graph_export.py`（golden、空图、FP-1 解析失败）；与 `docs/_tech_graph/*.ai.md` 拓扑子集对齐 |
| `graph.json` 体量 | `wc -l docs/_tech_graph/graph.json`；`nodes` / `edges` 计数见文件内数组 |
| 维护成本 | 变更 `.ai.md` 后须同 PR 运行 `python tools/tech_graph_graph_export.py` 并提交 `graph.json` |
| CI 增量 | `tech-graph` workflow 增加 `tech_graph_graph_export.py --check`（秒级；失败率与耗时在 GitHub Actions run 上观察） |

## 复现命令（cwd = 本仓根）

```bash
# 1) 契约门禁（与 graph 导出并行互补；跨仓真值见 tech-graph-contract workflow）
python tools/tech_graph_contract_check.py

# 2) 架构依赖图门禁（与契约脚本独立；顺序：先 contract 再 graph 便于本地排障）
python tools/tech_graph_graph_export.py --check

# 3) pytest 子集（解析 / 空图 / golden）
pytest tests/test_tech_graph_graph_export.py -q
```

## 仓库或 CI 快照引用

- 合入 PR 请在 PR 描述中填写 **短 commit hash** 与 **Actions run id**（**不**写入各仓 task 的 `freeze_id` 行，以免机械比对漂移）。
- 本文件结论段在首轮全绿合入后由人审更新。

## 结论（占位）

是否进入方案2 筹备：**待更新**（需至少一次全绿 CI 与抽样解析对照后回填）。
