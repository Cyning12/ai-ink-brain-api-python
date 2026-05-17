# 实验方案：`graph.json` vs Mermaid 语料 — LLM 上下文形态对比（V3 KPI · v1）

> **符号表**：[`NOTATION_zh.md`](./NOTATION_zh.md) — **段·S0–S2** · **KPI·P1–P4** · **阶段·Phase·P0/P1** · 本文件另用 **Repeat·R**（重复轮次）与 **Reviewer·R1/R2**（评审员），**≠** 定稿文 **Rule·R1–R6**（签收规则）  
> **日期**：2026-05-15  
> **状态**：`draft`（协议草案；P0 跑数见 [`EXPERIMENT_LOG.md`](./EXPERIMENT_LOG.md)）  
> **依赖旧总结**：[`00_legacy_compare_summary.md`](./00_legacy_compare_summary.md)  
> **KPI 权重（沿用 V3 Patch）**：**KPI·P1 易交接 40% > P2 可靠性 35% > P3 省钱 15% > P4 省时 10%**

---

## 1. 实验目的

在**同一批工程题**、**同一模型与工具策略**下，对比两种 **LLM 主上下文载荷**：

| 分支 | 建议代号 | 主载荷 | 允许的「Patch 式」附件（与旧 A/B Patch 对齐） |
|------|-----------|--------|-----------------------------------------------|
| **A** | `CTX_JSON` | 仓库已提交的 **`docs/_tech_graph/graph.json`**（全文或协议规定的上限策略） | **`docs/_tech_graph/_manifest.json`**、**`docs/_tech_graph/_contract_manifest.json`**；**不**提供 `_tech_graph` 下 Markdown 正文 |
| **B** | `CTX_MERMAID` | 与闸口 A 一致的 **Mermaid 语料总串**（由 `tools/tech_graph_token_estimate.py` 同规则从 `*.ai.md` 收集，**跳过 `99_*`**） | 同左 manifest/contract |

**任务**：给定需求描述，模型须输出 **入口点**、**影响点**，并给出 **可核验证据链**。

**与闸口 A 专文关系**：专文 `gate_a_scheme1_perf_compare_backend_detail.md` 提供 **静态字节 / 启发式 token** 基线；本实验在此基础上增加 **行为与 KPI**，**不**修改专文数字除非另开变更说明。

---

## 2. 控制变量（强制；违反则该 run 作废）

| 维度 | 固定项 |
|------|--------|
| 模型 | provider / model / temperature / `max_tokens` 写入本协议版本表（见 §8） |
| 题集 | 同一 `fixtures` 版本；每题含 **gold**（入口集合、影响集合、证据类型要求） |
| Persona | 同一 system / developer 提示；**仅**替换 A/B 主载荷块 |
| 工具 | 全程一致：例如 **禁止工具** 或 **仅允许 `read_file` 白名单路径`**（二选一写死） |
| 上下文粘贴策略 | **策略 α** 或 **策略 β** 全实验一致（见 §4.1） |
| 计分 | P1/P2 采用 **双人盲审 + rubric**（见 **§5.5～§5.7**）；禁止仅模型自评作为唯一真值 |

---

## 3. 输出 Schema（每轮强制 JSON）

模型每轮须输出可解析 JSON（字段名可微调，但须在 `fixtures` 中冻结一版）：

```json
{
  "entrypoints": [{"path": "...", "symbol": "...", "confidence": 0.0}],
  "impacts": [{"path": "...", "kind": "contract|data|control|ci|other", "confidence": 0.0}],
  "evidence": [{"ref": "graph_node_or_edge_id|file:line", "note": "..."}],
  "unknowns": [{"topic": "...", "why": "..."}]
}
```

**硬规则**：`evidence` 每条必须可映射到 **graph id** 或 **仓库相对路径 + 行号/符号**；无证据的断言必须进入 `unknowns`。

---

## 4. 三段协议（每题 × 每分支各跑一遍）

### 4.1 上下文粘贴策略（二选一，全实验锁定）

| 策略 | 定义 |
|------|------|
| **α（最坏 token）** | 每轮 user 消息均 **重贴全量主载荷** + manifest/contract |
| **β（较真实工程）** | 仅 **S0** 全量主载荷；S1/S2 **增量摘要**（由协议规定模板生成）+ manifest/contract |

### 4.2 S0 — 冷启动

1. **输入**：系统说明 + 主载荷（A 或 B）+ manifest/contract（若启用）+ **题目正文**。  
2. **输出**：满足 §3 schema。  
3. **记录**：`wall_total`（外部墙钟：发题 → JSON 落盘）、`prompt_tokens`、`completion_tokens`、（可选）`t_first_token`；工具调用次数。

### 4.3 S1 — 多轮追问（同一题）

- **轮数**：固定 **K = 3**（可 bump 版本，但 A/B 同题必须相同）。  
- **user 脚本**：预写在 `fixtures`（示例）：  
  1. 「把入口收敛到函数级，并说明理由」  
  2. 「列出对 CI / 契约最敏感的影响点」  
  3. 「给出最小验证路径（命令级，cwd=仓根）」  
- **记录**：每轮 token 与 wall；累计 token。

### 4.4 S2 — 少交集多轮（换题、同线程）

- **轮数**：固定 **M = 2** 道新题，与 S0–S1 **主题标签**不同（题集事先标注 `topic_id`，禁止相邻同 tag）。  
- **目的**：测 **上下文膨胀** 与 **串题泄漏**。  
- **记录**：同 S1；另记 **泄漏计数**：输出中引用路径落在「前序题 gold 集」且与本题无关的条数（人工或脚本）。

---

## 5. V3 KPI 操作化与合成

对每题、每分支、每段（S0/S1/S2）可分别打子分，再合成题级分数：

\[
S = 0.40 \cdot S_{P1} + 0.35 \cdot S_{P2} + 0.15 \cdot S_{P3} + 0.10 \cdot S_{P4}
\]

### 5.1 P1 易交接（40%）

| 档位 | 参考条件 |
|------|----------|
| 高 | `entrypoints`/`impacts` 结构清晰；含 **下一步 ≤5 步**；含 **门禁动作**（manifest / contract / 相关 workflow 名）；`unknowns` 诚实 |
| 中 | 有入口与影响但缺少命令级验证或步骤松散 |
| 低 | 散文式、缺证据索引、无法直接交接 |

### 5.2 P2 可靠性（35%）

| 指标 | 说明 |
|------|------|
| 入口 F1 | 与 gold `entrypoints` 算 P/R/F1 → 映射 0–100 |
| 影响 F1 | 与 gold `impacts`（允许目录级匹配规则事先写死） |
| 证据合规率 | `evidence` 可解析且可回放比例 |
| 泄漏惩罚 | S2 泄漏条数 → 扣 P2 |
| 漂移加分（上限封顶） | 显式指出 CONFIG / workflows / 图谱缩写与 SQL 全名等 **可验证矛盾** 并有复查命令 |

### 5.3 P3 省钱（15%）

- **主指标**：`sum(prompt_tokens + completion_tokens)`，分 S0 / S1 / S2 汇报。  
- **归一化**：建议以「同一题两分支中较低者为 100」做相对分，或全实验 z-score；在报告中写死选用哪一种。

### 5.4 P4 省时（10%）

- **主指标**：`wall_total`（中位数 **Repeat·R** 次可选，**R 建议 3**；此处 **R = Repeat 重复轮次**，见 [`NOTATION_zh.md`](./NOTATION_zh.md) §5）。  
- **归一化**：同 P3。

### 5.5 计分方案详解：rubric 是什么

**Rubric**（常译 **评分量规**）指：把「好/坏」拆成 **可重复观测的检查项**，每项有 **档位说明或数值规则**，评审只对照规则填分，而不是凭整体印象一句话定输赢。

在本协议里：

| 层级 | 作用 |
|------|------|
| **KPI 层** | P1～P4 与权重（沿用 V3 Patch 的优先级思想） |
| **Rubric 层** | 把每个 KPI 再拆成子项（例：P1 下拆「结构清晰度 / 下一步可执行性 / 门禁动作是否出现 / unknowns 是否诚实」），每子项规定 **0～N 分或高/中/低** 的判定句 |
| **证据层** | 打分必须能指回 **模型 JSON**、**gold** 或 **仓库路径**（便于复核与 PR 讨论） |

**P3 / P4**：以 API 或日志中的 **usage / 墙钟** 为主，rubric 成分少（主要是异常值是否剔除、重复 R 次取中位数的规则写死）。

### 5.6「结构化表 + 仲裁」指什么、怎么做

**结构化表**（本协议推荐落盘为 `runs/<run_id>/scores/*.yaml` 或等价 CSV）：

- **一行（或一条记录）** = 一次「评审单元」，至少包含：`run_id`、`task_id`、`branch`（A/B）、`segment`（段·S0/S1/S2）、`reviewer_id`（如 **Reviewer·R1/R2**，**非** Rule·R1）、各 **rubric 子项得分**、`notes`（引用 `evidence` 条目或 gold 条目 id）。
- **目的**：把主观分变成 **可 diff 的数据**；后续可做第二人复核、脚本聚合、或发现某评审系统性偏严/偏松。

**双人盲审**（针对 P1、P2 中「定性 rubric」占比较高的部分）：

- **盲什么**：两名评审在打分前 **不被告知** 该输出是 `CTX_JSON` 还是 `CTX_MERMAID`（可用匿名 `arm_x` / `arm_y`，汇总阶段再映射 A/B）。
- **不盲什么**：`task_id`、`segment`、原始 JSON 与 gold **必须可见**，否则无法判对错。

**仲裁**：

- **何时启动**：同一 `(task_id, branch, segment, rubric_subitem)` 上，两名评审 **分差 ≥ 预设阈值**（建议 **15～20 分** / 100，或定性档跨两档），或一人标「无法判」。
- **仲裁员**：第三人（**Reviewer·R3**）；只看 **结构化表 + 原始 JSON + gold**，必要时 **只打开** 被争议的那几条 `evidence` 指向的文件片段（**≠** 定稿文 Rule-3）。
- **输出**：在结构化表增加一行 `reviewer_id: R3_arbitration`、`final_score` 字段，或在子项上覆盖为 **终值**；**禁止**无记录地口头改分。

### 5.7 来源说明（与 `docs/diary/test` 的关系）

| 内容 | 来源 |
|------|------|
| **KPI 权重 P1>P2>P3>P4** | 直接沿用 `docs/diary/test/compare_core_A_vs_B_v3_patch.md` 与 `compare_three_versions_summary.md` 中的 **V3 Patch 叙事**（易交接 / 可靠性 / 省钱 / 省时）。 |
| **§5.1～§5.4 的子项表** | 本协议在 V3 定性结论之上做的 **操作化展开**（便于执行与验收），**不是** diary 里已写死的逐字条款。 |
| **rubric、结构化计分表、双人盲审、仲裁** | **本 v1 协议采纳的通用评测工程习惯**（教育/人审领域的 rubric、工业界 benchmark 常见的 **多标注员 + adjudication**）；用于补齐 **P1/P2 可重复、可审计** —— **diary 历史实验未强制要求** 这一套表单流程，当时以 **对照结论长文** 为主。 |
| **若需引用外部概念** | 不必绑定某一本书；团队内部可把本 **§5.5～§5.7** 即视为 **jsonPKmermaid v1 的计分 SOP**；若以后要贴参考文献，可在 `protocol_version.yaml` 增加 `scoring_references: []` 自行维护。 |

### 5.8 汇总

对题集取 **mean(S)**、**std**，并给 **win-rate（A vs B）** 与分段 token 曲线；**S 中 P1/P2 须已按 §5.6 终裁**，不得混用未仲裁的双人原始分。

---

## 6. 交付物目录约定（建议）

> 实施时可在本目录下新建子目录，避免与 `docs/diary/test` 混淆。

```
docs/diary/jsonPKmermaid/
  README.md
  00_legacy_compare_summary.md
  01_experiment_json_vs_mermaid_kpi_v1.md   # 本文件
  fixtures/
    gate_ctx_ab_v1/
      protocol_version.yaml    # 模型名、策略 α/β、K/M
      tasks.json               # 题面 + gold + topic_id
      user_scripts.yaml        # S1/S2 固定 user 文案
  runs/
    <run_id>/
      raw/*.jsonl              # 每轮原始响应 + usage
      scores/*.yaml            # 人工/半自动子分
  reports/
    compare_gate_ctx_json_vs_mermaid_v1.md   # 最终表与结论
```

---

## 7. failure_paths（文档级）

| ID | 触发 | 处理 |
|----|------|------|
| FP-1 | 模型未输出合法 JSON | 该轮记 **fail**，是否重试由协议版本规定 |
| FP-2 | A/B 控制变量不一致（模型/工具/策略混用） | **整 run 作废** |
| FP-3 | gold 本身与仓库漂移 | **冻结 commit** 于 `protocol_version.yaml`；先修 gold 再重跑 |
| FP-4 | 将静态专文 §4 数字与本次 LLM token **混写为同一「结论句」** | 禁止；两轴分述 |

---

## 8. 版本表（ bump 时追加一行）

| protocol_version | 日期 | 模型 | 策略 | 备注 |
|------------------|------|------|------|------|
| v1 | 2026-05-15 | _TBD_ | α 或 β **待填** | 初稿 |

---

## 给 Cursor

`CTX_JSON`、`CTX_MERMAID`、`V3 KPI`、`S0` `S1` `S2`、`fixtures`、`graph.json`、`tech_graph_token_estimate`、`compare_gate_ctx_json_vs_mermaid`
