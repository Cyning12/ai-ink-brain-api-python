# Rubric 元分析结论（示例）— `examples_builtin` · `20260515_201818`

> **定位**：基于同批输入（见 [`copy_ready_user_message_rubric_201818.md`](./copy_ready_user_message_rubric_201818.md)）中各轮工件全文与整组合并 JSON 撰写的 **人读结论文档**；**非**自动流水线产物。  
> **置信度**：高（材料为演示短工件 + 完整 JSON）；对真实 PR 须结合仓库与 CI 再核验。  
> **修订**：与「Rubric 元评审」七段结构对齐的落盘稿（`20260515`）。

---

## 1. 摘要

1. **终分矩阵**：S0 `clarity=2,risk=1`；S1 `clarity=2,risk=3`；S2 `clarity=4,risk=1`。  
2. **仲裁**：三轮 `arbitration_needed=false`，`arbitration_mode` 均为 `none`，`disputed_dimensions` 均为空；**未出现**仲裁与 `arbitration_justification`。  
3. **R1/R2（`review_a` / `review_b`）分差**：仅 S0、S1 的 **`clarity`** 为 R1（`Pro/moonshotai/Kimi-K2.6`）=3、R2（`deepseek-ai/DeepSeek-V4-Flash`）=2；**`risk` 三轮 R1/R2 完全一致**。  
4. **终分与双人**：S0、S1 的 **`final_scores.clarity` 与 R2 对齐（2）**；S1 `risk` 双方均为 3；S2 两维双方与终分一致。  
5. **与正文强相关**：S1 要求补充回滚与线上影响 → `risk` 从 1 **升至** 3；S2 一句话写清目标/范围/验收 → `clarity` **升至** 4。  
6. **演示边界**：文中 `pytest` 等为示例占位；**不得**外推为仓库真实测试、覆盖率或 CI 结论。

---

## 2. 跨轮走势（维度 ↔ 工件变化）

| `round_id` | 工件要点 | `clarity` | `risk` |
|------------|-----------|-----------|--------|
| S0 | 模拟 PR：有摘要/复现/范围；目标与验收弱；无失败/回滚叙述 | 2 | 1 |
| S1 | 追问稿：要求补回滚与线上影响；**未附带**前一轮正文 | 2 | 3 |
| S2 | 另一主题：内部工具、`--dry-run`、不改默认行为、验收写清 | 4 | 1 |

- **`clarity`**：S0→S1 **维持 2**——双方 justification 均强调缺前一轮、验收未定义等；S1→S2 **升至 4**——与「一句话说清目标、范围、验收」的叙述一致。  
- **`risk`**：S0、S2 **均为 1**（未写回滚/失败影响）；S1 **为 3**（正文指向需补回滚与线上影响，但未展开具体分析与缓解）。

---

## 3. 分歧分析

- **逐轮**：S0、S1 的 **`clarity`** 存在 R1=3 vs R2=2；**`risk`** 无 R1/R2 分差；S2 两维无分差。  
- **可能原因**：「少量含糊」与「范围不清/目标验收未显式」在极短文本上**相邻档**，两模型容忍度不同；S1 **未内嵌 S0**，双方把「缺前一轮」记入 **`clarity`**，易与「作者表达不清」混判。  
- **仲裁缺失**：`disputed_dimensions` 为空，**未**将 1 分档 `clarity` 差异标为争议；若产品需强制人审，须在规则或后处理中定义阈值。

---

## 4. Rubric 质量

- **覆盖**：对「目标/范围/验收是否显性」与「是否讨论失败面/回滚」敏感，适合**文档闸口粗筛**。  
- **过严信号（由本批判分行为反推，非条文）**：S2 已限定内部工具与 dry-run，双方仍因未写回滚给 `risk=1`；若需区分变更面，当前二维 **`risk` 可能偏齐一**。  
- **宜记 `unknown` 而非硬扣 `clarity`**：当 manifest 约定「第二轮不附带前文」时，建议单独标记 **`context_missing`** 类状态，避免**协议性缺信息**记成**写作者 clarity**。

---

## 5. 工件与 manifest 建议

1. **S1 起**：在 `artifact_file` 或 runner 输出中增加固定区块（如 `## Prior round (S0)`），**注入 S0 摘要或全文**。  
2. **低重叠轮（如 S2）**：在 manifest 或模板中注明 **`continuity: independent`** 或等价说明，减少误读为「遗忘承接」。  
3. **下一版 `min_rubric.json`**：为 `risk` 增加 **变更面 / 影响面** 或 **「不适用须声明」**；或与 `clarity` 正交约定 **「上下文是否由流水线提供」**。  
4. **`random_seed` 固定**（本批为 42）利于对比跨轮工件；换 seed 仅用于稳健性实验。  
5. **合并策略**：若需对 1 分档差异触发人审，须定义 **`disputed_dimensions` 填充规则**或仲裁阈值（本批 JSON 未体现）。

---

## 6. risks

- 放宽 `risk` 或增加「不适用」后，**真实用户面**变更可能被**低估**；须第二套 Rubric 或人工 gate。  
- 拼接 S0 进 S1 后**篇幅变长**，可能触发「冗长/跑题」类维度；应控制摘要长度与结构。

---

## 7. unknowns

- **`min_rubric.json` 各分档原文**与维度定义（材料仅有 `rubric_name`、`rubric_version`）。  
- **`final_scores` 合并规则**（例如 `clarity` 为何与 R2 的 2 对齐；材料未描述算法）。  
- **`effective_fallback: llm_arbiter`** 在未仲裁时的精确语义及对分数的影响路径。  
- 真实仓库 **diff、CI、线上影响面**（本批 JSON 未包含）。
