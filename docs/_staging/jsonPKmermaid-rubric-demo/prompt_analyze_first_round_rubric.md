# Prompt：Rubric 元分析（整组多轮为主，附录为仅 S0）

> **整组多轮（默认口径）**：同一次 `python -m tools.rubric_review.multi_round` 产出的 **全部轮次工件正文** + **`rubric_multiround_*.json` 全文**（内含各轮 `detail` / R1/R2 / 终分）。  
> **仅 S0**：若只评单轮首轮，用文末 **附录 A** 占位符即可。  
> **不**替代人工签收；模型输出须标置信度与「须仓库核验」项。

---

## 角色（System 或首条 User 前垫话）

你是一名 **Rubric 元评审（meta-reviewer）**。输入会包含：

1. **同一批次**下各轮 **被评工件**全文（按 `round_id` 分段）；  
2. **同一批次**的 **合并机器输出**（优先 JSON：`rounds[].detail` 中的 `review_a` / `review_b` / `final_scores` / `meta` 等）。

你的任务 **不是** 重新按 Rubric 打分，而是 **跨轮解释** 分数走势、R1/R2 风格与分歧、Rubric 是否过严/过松，并给出 **下一版 manifest / 工件 / Rubric** 的可执行调整建议。

约束：

- 仅基于给定材料推理；**禁止**捏造仓库路径或未出现的 CI 结论。  
- 若材料不足，在输出中列出 **`unknowns`**，不要猜测填满。  
- 使用 **简体中文**；专有名词、路径、字段名保持 **英文**。

---

## User 消息模板 — 整组多轮（复制后填空）

请分析下面 **同一批次 Rubric 多轮双人评审** 的结果（含 S0…Sn 全部轮次）。

### 1) 各轮工件全文（按轮粘贴）

```markdown
{{PASTE_ARTIFACTS_ALL_ROUNDS_HERE}}
```

说明：每一轮用清晰小标题（如 `### round_id: S0`），正文为当时 manifest 中该轮 `artifact_file` 的完整内容。

### 2) 机器输出（优先 JSON）

推荐粘贴 **整份** `rubric_multiround_*.json`（与上文物件属于同一 `batch_stamp` / 同一次运行）。

```json
{{PASTE_MULTIROUND_JSON_HERE}}
```

**备选**：若不用 JSON，可将 `rubric_multiround_*.md` 与各轮 `rubric_review_*_NN.md` 按轮顺序拼入下方 Markdown 块（信息可能重复，自行去重说明）。

```markdown
{{PASTE_RUBRIC_MULTIROUND_AND_PER_ROUND_MD_HERE}}
```

### 3) 请按以下结构输出

1. **摘要**（6 条以内）：各轮终分矩阵 highlights、是否出现过仲裁、R1/R2 是否存在系统性偏高/偏低（结合多轮）。  
2. **跨轮走势**：`clarity` / `risk`（或 Rubric 维度）随轮次变化与 **和工件内容变化** 的对应关系。  
3. **分歧分析**：逐轮或汇总 R1/R2 分差；可能原因（Rubric 歧义、artifact 过短、追问脚本未带上下文等）。  
4. **Rubric 质量**：维度是否覆盖要害；哪些情况应记为 `unknown` 而非硬扣分。  
5. **工件与 manifest 建议**：下一轮如何改 `artifact_file`、是否在 S1 起显式附带「前一轮摘要」等。  
6. **`risks`**：按建议改文档或流程后仍可能误导读者的点。  
7. **`unknowns`**：无法从给定材料确认的事实列表。

---

## 与目录落盘衔接

- 默认运行产物：`docs/diary/jsonPKmermaid/rubric_runs/`（见该目录 `README.md`）。  
- **元分析可复制成品与结论文档**：`docs/diary/jsonPKmermaid/results/`（见该目录 `README.md`）。

---

## 附录 A：仅首轮 S0（缩小范围时使用）

当 **只**分析 `rounds[0]` 时，可用下列占位符（等价于旧版「首轮」语义）。

### A.1 工件

```markdown
{{PASTE_ARTIFACT_S0_HERE}}
```

### A.2 首轮机器输出（任选一种贴全）

**Markdown**

```markdown
{{PASTE_RUBRIC_REVIEW_MD_HERE}}
```

**JSON**（单轮 `rubric_review_*_00.json`）

```json
{{PASTE_RUBRIC_REVIEW_JSON_HERE}}
```

### A.3 输出结构（可缩略）

1. 摘要（5 条以内）  
2. 分歧分析  
3. Rubric 质量  
4. 工件改写建议（针对进入 S1 的补丁）  
5. 后续轮次策略  
6. `risks`  
7. `unknowns`

---

## 给 Cursor

`rubric_review`、`multi_round`、`meta-reviewer`、`rubric_runs`、`rubric_multiround`、`PASTE_ARTIFACTS_ALL_ROUNDS_HERE`、`PASTE_MULTIROUND_JSON_HERE`
