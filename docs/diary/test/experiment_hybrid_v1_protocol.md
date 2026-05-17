# 实验协议 · AB Hybrid V1（取长补短）

> 定位：**不再与纯 A / 纯 B 做对照相等的「第三赛道」**，而是把 V3 对照结论 **产品化** 为单一推荐 Prompt。  
> 与 `experiment_v3_protocol.md` 关系：**并行**，不废止 V3；历史结果仍以 `result_A_*` / `result_B_*` 为准。

---

## 1. 设计来源（摘要）

| 来源 | 纳入 Hybrid 的内容 |
|------|---------------------|
| **B** | `00_main*`、`01_struct`、按需 `10–15_flow`、图谱缩写与漂移警觉、`_manifest.json` / `_contract_manifest.json` 索引位、`漂移防线` |
| **A（补丁）** | 行级/函数级锚点、Legacy 行为细节、三卡门禁配方、`pytest`/curl 落地步骤 |
| **补丁共识** | 新增端点必提 manifest + `tech_graph_manifest_check.py` |
| **增量** | **第四张配方卡（SSE 契约）**、强制 **`t_graph`/`t_code` 分账**便于复盘成本 |

---

## 2. 产出文件

| 类型 | 路径 |
|------|------|
| Prompt | `docs/diary/test/prompt_AB_hybrid_v1.md` |
| 执行结果 | `docs/diary/test/result_AB_hybrid_v1.md` |

可选：混合跑通后，将结论摘录进团队 Wiki；**无需**强制再写 `compare_core_*`，除非要做 Hybrid vs A/B 量化。

---

## 3. 何时仍保留纯 A / 纯 B

| 场景 | 建议 |
|------|------|
| **消融实验**（论文式：图谱有无的影响） | 继续用 `prompt_A_*` / `prompt_B_*` |
| **门禁脚本调试**（只关心 manifest） | 可直接读 `_manifest.json` + `tools/`，不必跑全套 Hybrid |
| **日常接手与文档迭代** | **默认 Hybrid V1** |

---

## 4. KPI 权重（与 V3 一致）

易交接（40%）> 可靠性（35%）> 省钱（15%）> 省时（10%）。

---

*本协议仅定义 Hybrid V1 的定位与落盘路径。*
