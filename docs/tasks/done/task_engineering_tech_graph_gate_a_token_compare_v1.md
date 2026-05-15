# Task：闸口 A 附录 — `graph.json` vs Mermaid 拼接体 **token 粗估** 工具与 CI

> **状态**：`done（2026-05-15 验收通过）`  
> **关联**：`docs/tech_graph/gate_a_scheme1_backend.md` §3「Agent / LM context（可选）」；[`gate_a_scheme1_perf_compare_backend_detail.md`](../../tech_graph/gate_a_scheme1_perf_compare_backend_detail.md)  
> **test_strategy**：`required`  
> **test_strategy_note**：输出为确定性 JSON；须有 pytest 锁 `measure` 与 CLI 冒烟，避免规则静默漂移。  
> **freeze_id**：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`

---

## 1. 背景与目标

为闸口 A **附录**提供可复现命令：在**同一扫描范围**（与 `tech_graph_graph_export.py` 一致：`docs/_tech_graph/*.ai.md`，跳过 `99_*`）下，对比

- **代号 A**：已提交 **`graph.json`** 全文（UTF-8 字节、字符数、粗估 token）；  
- **代号 B**：上述 `.ai.md` 中 **所有 mermaid fence 正文按文件名排序后拼接** 的全文（同三项指标及 **B/A 比值**）。

**粗估规则**（非官方 tokenizer）：`heuristic_tokens = max(1, chars // 4)`，仅用于 **A/B 同口径**相对比较；正式 LLM 计费须另声明编码器。

---

## 2. 范围 / 非范围

**范围**

- 脚本：`tools/tech_graph_token_estimate.py`（`--json` 一行输出 + 默认 Markdown 表）。  
- `tests/test_tech_graph_token_estimate.py`。  
- `.github/workflows/tech-graph.yml` 在 **`tech_graph_graph_export.py --check` 之后** 增一步（**并行**于 contract；**不**并入 `tech_graph_contract_check` / `tech_graph_graph_export`）。

**非范围**

- 引入 `tiktoken` 或绑定某一厂商模型为「真 token」真值（若未来要加，须单独立项 bump 依赖）。  
- 前端仓内重复实现同一算法（见下文「跨仓」）。

---

## 3. 依赖与跨仓

| 项 | 说明 |
|----|------|
| 前端 | **不必**为附录单独写 tokenizer；在 **`ai-ink-brain`** 若需在 `quality` 中展示或归档，**调用本仓脚本**（工作区 `../ai-ink-brain-api-python/tools/tech_graph_token_estimate.py`，参数 `--input` / `--graph-json` 指向前端 `docs/_tech_graph`）即可。 |
| 配对前端 task | `ai-ink-brain/content/tasks/done/task_engineering_tech_graph_graph_json_export_v1.md`（已增加「闸口附录」引用条） |

---

## 4. 验收标准

- [x] `python tools/tech_graph_token_estimate.py` 默认输出 Markdown 表；`--json` 输出单行 JSON 且含 `ratio_B_per_A`。  
- [x] `pytest tests/test_tech_graph_token_estimate.py` 绿。  
- [x] `tech-graph` workflow 含 **Tech graph token estimate** step 且成功。  
- [x] 在 `gate_a_scheme1_backend.md`「仓库或 CI 快照引用」或附录中 **贴过一次** `--json` 输出（merge 后回填）。

---

## 5. failure_paths

| ID | 触发 | 行为 |
|----|------|------|
| FP-1 | `--input` 或 `--graph-json` 不存在 | 退出码 2，stderr 说明路径 |
| FP-2 | 读盘编码错误 | 非 0，stderr 含文件路径 |

---

## 6. 实现备忘（回填）

| 项 | 内容 |
|----|------|
| 脚本 | `tools/tech_graph_token_estimate.py` |
| 测试 | `tests/test_tech_graph_token_estimate.py` |
| CI | `.github/workflows/tech-graph.yml` → `Tech graph token estimate (Gate A appendix)` |

---

## 给 Cursor

`tech_graph_token_estimate`、`gate_a`、`heuristic_tokens`、`freeze_id`、`tech-graph`
