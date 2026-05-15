# 闸口 A — 方案1 性能对比（后端）— SOP 与记录专文

> **父文档（结论 / §6 / §3 分解）**：[`gate_a_scheme1_backend.md`](./gate_a_scheme1_backend.md)  
> **`freeze_id`（契约基准，勿写 Actions run id）**：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`  
> **PR 描述须写一句（与 `task_engineering_tech_graph_gate_a_perf_compare_v1.md` §8 对齐）**：**总对比表主真值在本专文**；父文档以链回本节为主，避免双轨数字漂移（见下文 **单一真值策略**）。

---

## 1. 环境固定说明

| 项 | 约定 |
| --- | --- |
| **cwd** | `ai-ink-brain-api-python` 仓根 |
| **Python** | 建议 **3.11+**（与 CI `hostedtoolcache` 对齐；本地略差可接受，须在表内注明） |
| **输入根** | `docs/_tech_graph`；扫描 **`*.ai.md`**，**跳过 `99_*.md`**（与 `tech_graph_graph_export.py` / `tech_graph_token_estimate.py` 一致） |
| **CLI 真值** | **仅** `tools/tech_graph_graph_export.py`、`tools/tech_graph_token_estimate.py`（**禁止**以 `docs/tech_graph/改进方向.md` §1.4 中的 `export_graph_json.py` 等规划示例为复现来源 → 见父 task **FP-H**） |

---

## 2. 术语消歧（强制）

| 名称 | 含义 |
| --- | --- |
| **§2 代号 A** | 消费侧输入为已提交 **`docs/_tech_graph/graph.json`**（静态 JSON）。 |
| **§2 代号 B** | 消费侧输入为与 A **同母集合**下拼接的 **Mermaid 语料总串**（默认实现：`tech_graph_token_estimate.py` 内 `collect_mermaid_corpus`）。 |
| **计时 A** | 维护者本机 `/usr/bin/time` 粗测（**与 JSON/Mermaid 代号无关**）。 |
| **计时 B** | Agent 批跑 N=10 的 P50/P95（**与 JSON/Mermaid 代号无关**）。 |

**禁止**：在同一列表头或脚注中把「计时 A/B」与「§2 代号 A/B」混为一列且不标注 → 见 **FP-I**。

---

## 3. 逐步采集命令（SOP）

```bash
# cwd = 本仓根

# 契约门禁（与 graph 并行；顺序建议先 contract 再 graph）
python tools/tech_graph_contract_check.py

# 导出 / 漂移校验（真值脚本名）
python tools/tech_graph_graph_export.py
python tools/tech_graph_graph_export.py --check

# 解析 / golden 子集
pytest tests/test_tech_graph_graph_export.py -q

# 代号 A/B 载荷与启发式 token（一行 JSON；真值脚本名）
python tools/tech_graph_token_estimate.py --json

# 产物字节（§2 代号 A 侧磁盘口径）
wc -c docs/_tech_graph/graph.json
```

**可选（本地 wall time，记入「计时 A」）**：

```bash
/usr/bin/time -p python tools/tech_graph_graph_export.py
/usr/bin/time -p python tools/tech_graph_graph_export.py --check
/usr/bin/time -p pytest tests/test_tech_graph_graph_export.py -q
```

---

<span id="sec4-master-table"></span>

## 4. 签收用总对比表（§3 各维度 · 主真值）

> **§3.2 浏览器向**：本阶段产品 **无**用户页大图谱 Mermaid → **全表 N/A**；**不得**将浏览器实测写入闸口主结论。主结论语义以父文档 **[「结论」](./gate_a_scheme1_backend.md#结论)**（Agent/LLM 口径 + §3.2 N/A）为准 —— 对应 task **FP-D / FP-E / FP-F** 的反面约束。

| §3 维度 | §2 代号 A（`graph.json` / 生成侧） | §2 代号 B（Mermaid 语料） | §3.2 浏览器向 | 证据 / 备注 |
| --- | --- | --- | --- | --- |
| **载荷 / 字节** | `wc -c` → **20224**（与下节一致） | `tech_graph_token_estimate.py` → **B.bytes_utf8 20953** | **N/A** | 见 **§9** JSON；启发式 token 同工具输出 |
| **冷解析 / 消费** | JSON 解析成本由消费端定义；本仓主表以 **生成 + 校验 + pytest** 为主 | Mermaid 词法/layout 由消费端定义；本仓附录为 **语料体量** 对照 | **N/A** | 不在本 task 假装完成浏览器 micro-benchmark |
| **首屏 / LCP / chunk** | — | — | **N/A** | 链父文档 **「结论」→ 与 §3.2 / §5 的关系** |
| **Agent / LM context** | **A**：heuristic_tokens **5056** | **B**：**5026**；ratio heuristic **0.9941** | **N/A** | `python tools/tech_graph_token_estimate.py --json` |
| **后端生成 / 校验 / CI（§3.1）** | 导出、`--check`、单测、CI step | 同左（非「代号 B 消费链」） | **N/A** | 数值见 **§9**；CI 链父文档 **「仓库或 CI 快照引用」** |

---

## 5. 等价性 spot-check（最低门槛）

| 项 | 结果 |
| --- | --- |
| **节点数 / 边数**（与已提交 `graph.json`） | **134 / 180**（与导出 golden 一致；若 bump 图须同步更新本行） |
| **标签字符量** | 以 `graph.json` 与语料解析规则为准；细账见导出器与 token 工具实现 |
| **spot-check** | **执行**：文档落盘 Agent；**日期**：2026-05-15；**方式**：对照 `pytest tests/test_tech_graph_graph_export.py` 与 `--check` 无漂移；PR 评论可链替换本行 |

若将来 A/B **拓扑不一致**，对比仅入 **附录**，**不得**写入父文档主结论句（**FP-A**）。

---

## 6. 记录表头模板（批跑 / 多轮）

| 指标名 | §2 代号或计时标签 | 原始值 | N | commit（短） | 备注 |
| --- | --- | --- | --- | --- | --- |
| 例：`导出 wall` | **计时 A** | real 0.12s | 1～2 | 本地 HEAD | 本机粗测 |
| 例：`导出 wall` | **计时 B** | P50 0.030s | 10 | `42a6419` | 临时目录写盘 |

---

## 7. failure_paths 模板（可与 task 同构）

| ID | 触发 | 行为 / 语义 | 可重试 |
| --- | --- | --- | --- |
| FP-A | A/B 拓扑或规模未对齐仍写入主结论 | 禁止合入；改附录或补 spot-check | 是 |
| FP-H | 复现命令使用 `export_graph_json.py` 等非落地脚本名 | 禁止；改用 **§3** 依赖表脚本 | 是 |
| FP-I | 「计时 A/B」与「§2 代号 A/B」混排 | 术语违规；拆列或拆脚注 | 是 |

（完整 ID 列表见 `docs/tasks/active/task_engineering_tech_graph_gate_a_perf_compare_v1.md` §5。）

---

## 8. 单一真值策略（与 task §7 对齐）

- **数字与总表**：以 **本专文 §4、§9** 为 **主维护面**；父文档 **`gate_a_scheme1_backend.md`** 保留 **结论句、§6 勾选、CI URL、§3.0 导航**，**不**重复粘贴大表与 `--json` 全文（仅链至本节锚点 **§9**），避免 **FP-G** 双轨漂移。  
- 若未来改在父文档内嵌等价小节，须在 PR 与 task「实现备忘」声明 **弃用专文** 或 **专文仅 SOP**，并消除死链。

---

<span id="sec9-perf-backend"></span>

## 9. 后端 §3.1 采样记录与 token 附录（单一真值主表）

**产物体量（与仓内已提交 `graph.json` 一致）**

| 项 | 值 |
| --- | --- |
| `graph.json` 字节（§2 代号 A） | **20224** |
| nodes / edges | **134 / 180** |
| CI 对应 commit（线上门禁） | `fb0b54c`（merge PR #25；见父文档 Actions 链） |

**`python tools/tech_graph_token_estimate.py --json`（cwd=本仓根；与上表同内容基线）**

```json
{"schema": "tech_graph_token_estimate_v1", "input_root": "docs/_tech_graph", "graph_json": "docs/_tech_graph/graph.json", "A": {"bytes_utf8": 20224, "chars": 20224, "heuristic_tokens": 5056}, "B": {"bytes_utf8": 20953, "chars": 20105, "heuristic_tokens": 5026}, "ratio_B_per_A": {"bytes_utf8": 1.036, "heuristic_tokens": 0.9941}, "rules": {"heuristic_tokens": "chars//4, min 1; not official tiktoken"}}
```

**CI（回填口径）**：见父文档 **「仓库或 CI 快照引用」** 内 `tech-graph` / `manifest_check` 链接；step **「Tech graph graph.json drift check」** UI 约 **1s**。

### 计时 A — 维护者本机（终端粗测；**非** §2 代号）

| 指标 | real（s） | 备注 |
| --- | --- | --- |
| `python tools/tech_graph_graph_export.py` | ~0.12 | 单次 |
| `python tools/tech_graph_graph_export.py --check` | ~0.12 / ~0.11 | 两次 |
| `pytest tests/test_tech_graph_graph_export.py -q`（整进程 `/usr/bin/time`） | ~0.45 | pytest 内部收集约 0.01s |

### 计时 B — N=10 批跑（**非** §2 代号；临时目录写 `graph.json`，不写仓内）

| 指标 | P50 (s) | P95 (s) | min–max (s) |
| --- | --- | --- | --- |
| 导出（临时 `graph.json`） | 0.030 | 0.035 | 0.030–0.040 |
| `--check`（对临时产物） | 0.030 | 0.030 | 0.030–0.030 |
| `pytest tests/test_tech_graph_graph_export.py`（整进程） | 0.390 | 0.400 | 0.390–0.400 |

> **注**：**计时 A** 与 **计时 B** 差异来自机器负载与测量粒度，**与 §2 代号 A/B（JSON vs Mermaid 消费链）无关**。线上签收以 **CI commit** 为优先；P50/P95 可在同 commit 上重跑覆盖。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-15 | 首版：SOP、总表（浏览器 N/A）、§9 单一真值主表、术语与 FP 模板；对齐 `task_engineering_tech_graph_gate_a_perf_compare_v1` |
