# 可直接复制：Rubric 整组多轮元分析（examples_builtin · 201818）

> 用法：**先复制「角色」块**到 System（或首条 User 前单独一条）；**再复制「User 消息」块**整段到 User。  
> 数据来源：`rubric_runs/rubric_multiround_examples_builtin_20260515_201818.json` 与各轮示例 artifact（与 JSON 内路径一致）。

---

## 角色（System 或单独首条消息）

你是一名 **Rubric 元评审（meta-reviewer）**。输入会包含：

1. **同一批次**下各轮 **被评工件**全文（按 `round_id` 分段）；
2. **同一批次**的 **合并机器输出**（JSON：`rounds[].detail` 中的 `review_a` / `review_b` / `final_scores` / `meta` 等）。

你的任务 **不是** 重新按 Rubric 打分，而是 **跨轮解释** 分数走势、R1/R2 风格与分歧、Rubric 是否过严/过松，并给出 **下一版 manifest / 工件 / Rubric** 的可执行调整建议。

约束：

- 仅基于给定材料推理；**禁止**捏造仓库路径或未出现的 CI 结论。  
- 若材料不足，在输出中列出 `unknowns`，不要猜测填满。  
- 使用 **简体中文**；专有名词、路径、字段名保持 **英文**。

---

## User 消息（整段复制）

请分析下面 **同一批次 Rubric 多轮双人评审** 的结果（含 S0…Sn 全部轮次）。

### 1) 各轮工件全文（按轮粘贴）

```markdown
### round_id: S0

# 示例工件 S0（模拟 PR 描述）

## 摘要
为 Rubric 多轮批跑示例准备的一段短文本。

## 复现
- cwd：仓根
- 命令：`pytest tests/test_example.py -q`（示例，非真仓库命令）

## 范围
- 改 README 与一处配置。

### round_id: S1

# 示例工件 S1（模拟追问 / 第二轮）

请在前一轮基础上补充：**回滚策略**与 **对线上用户的影响**（若有）。

### round_id: S2

# 示例工件 S2（低重叠 / 另一主题）

独立需求：为内部工具增加 `--dry-run`，不得影响默认行为；需说明如何验证未写磁盘。
```

### 2) 机器输出（整组合并 JSON）

```json
{
  "run_name": "examples_builtin",
  "manifest": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/multiround.example.json",
  "rubric": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/min_rubric.json",
  "backend": "siliconflow",
  "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
  "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
  "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
  "random_seed": 42,
  "batch_stamp": "20260515_201818",
  "rounds": [
    {
      "round_id": "S0",
      "artifact_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S0_pr_body.md",
      "stem": "rubric_review_examples_builtin_S0_20260515_201818_00",
      "markdown": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_review_examples_builtin_S0_20260515_201818_00.md",
      "json": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_review_examples_builtin_S0_20260515_201818_00.json",
      "final_scores": {
        "clarity": 2,
        "risk": 1
      },
      "arbitration_needed": false,
      "detail": {
        "rubric_name": "示例 Rubric（多轮脚本演示 · 2 维）",
        "rubric_version": "0.1.0",
        "review_a": {
          "dimension_scores": {
            "clarity": 3,
            "risk": 1
          },
          "justification": "clarity：范围已说明（改 README 与一处配置），但目标与验收标准未显式阐述，存在少量含糊；risk：全文未提及回滚、失败影响或风险缓解，完全缺失。",
          "model_used": "Pro/moonshotai/Kimi-K2.6"
        },
        "review_b": {
          "dimension_scores": {
            "clarity": 2,
            "risk": 1
          },
          "justification": "清晰度：范围仅提到改README与一处配置，但未明确目标、验收标准，属于范围不清或目标发散，故给2分。风险意识：完全未提及回滚或失败影响，完全缺失，故给1分。",
          "model_used": "deepseek-ai/DeepSeek-V4-Flash"
        },
        "final_scores": {
          "clarity": 2,
          "risk": 1
        },
        "arbitration_needed": false,
        "arbitration_mode": "none",
        "arbitration_justification": null,
        "disputed_dimensions": [],
        "meta": {
          "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
          "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
          "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
          "random_seed": 42,
          "effective_fallback": "llm_arbiter"
        },
        "run": {
          "artifact_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S0_pr_body.md",
          "rubric_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/min_rubric.json",
          "backend": "siliconflow",
          "slug": "rubric_review_examples_builtin_S0_20260515_201818_00",
          "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
          "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
          "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
          "random_seed": 42
        }
      }
    },
    {
      "round_id": "S1",
      "artifact_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S1_followup.md",
      "stem": "rubric_review_examples_builtin_S1_20260515_201818_01",
      "markdown": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_review_examples_builtin_S1_20260515_201818_01.md",
      "json": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_review_examples_builtin_S1_20260515_201818_01.json",
      "final_scores": {
        "clarity": 2,
        "risk": 3
      },
      "arbitration_needed": false,
      "detail": {
        "rubric_name": "示例 Rubric（多轮脚本演示 · 2 维）",
        "rubric_version": "0.1.0",
        "review_a": {
          "dimension_scores": {
            "clarity": 3,
            "risk": 3
          },
          "justification": "clarity：目标（补充回滚策略与线上用户影响）明确，但缺少前一轮上下文且未定义验收标准，存在少量含糊。risk：明确点出需补充回滚及线上用户影响，体现风险意识，但工件本身未给出具体风险分析与缓解措施。",
          "model_used": "Pro/moonshotai/Kimi-K2.6"
        },
        "review_b": {
          "dimension_scores": {
            "clarity": 2,
            "risk": 3
          },
          "justification": "清晰度：工件本身是要求补充回滚策略和影响，但未给出前一轮内容，导致目标和范围不完整，属于范围不清。风险意识：明确要求补充回滚策略和影响，体现了对风险的关注，但未具体展开，属于有提及但不具体。",
          "model_used": "deepseek-ai/DeepSeek-V4-Flash"
        },
        "final_scores": {
          "clarity": 2,
          "risk": 3
        },
        "arbitration_needed": false,
        "arbitration_mode": "none",
        "arbitration_justification": null,
        "disputed_dimensions": [],
        "meta": {
          "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
          "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
          "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
          "random_seed": 42,
          "effective_fallback": "llm_arbiter"
        },
        "run": {
          "artifact_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S1_followup.md",
          "rubric_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/min_rubric.json",
          "backend": "siliconflow",
          "slug": "rubric_review_examples_builtin_S1_20260515_201818_01",
          "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
          "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
          "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
          "random_seed": 42
        }
      }
    },
    {
      "round_id": "S2",
      "artifact_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S2_low_overlap.md",
      "stem": "rubric_review_examples_builtin_S2_20260515_201818_02",
      "markdown": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_review_examples_builtin_S2_20260515_201818_02.md",
      "json": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_review_examples_builtin_S2_20260515_201818_02.json",
      "final_scores": {
        "clarity": 4,
        "risk": 1
      },
      "arbitration_needed": false,
      "detail": {
        "rubric_name": "示例 Rubric（多轮脚本演示 · 2 维）",
        "rubric_version": "0.1.0",
        "review_a": {
          "dimension_scores": {
            "clarity": 4,
            "risk": 1
          },
          "justification": "clarity：目标（增加--dry-run）、范围（内部工具）及验收标准（不影响默认行为、验证未写磁盘）一句话能说清；risk：全文完全未提及回滚或失败影响。",
          "model_used": "Pro/moonshotai/Kimi-K2.6"
        },
        "review_b": {
          "dimension_scores": {
            "clarity": 4,
            "risk": 1
          },
          "justification": "清晰度：一句话清晰说明了目标（增加--dry-run）、范围（内部工具）、验收条件（验证未写磁盘），完全符合4分标准。风险意识：完全未提及回滚、失败影响或任何风险缓解措施，因此给1分。",
          "model_used": "deepseek-ai/DeepSeek-V4-Flash"
        },
        "final_scores": {
          "clarity": 4,
          "risk": 1
        },
        "arbitration_needed": false,
        "arbitration_mode": "none",
        "arbitration_justification": null,
        "disputed_dimensions": [],
        "meta": {
          "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
          "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
          "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
          "random_seed": 42,
          "effective_fallback": "llm_arbiter"
        },
        "run": {
          "artifact_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/round_S2_low_overlap.md",
          "rubric_file": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/tools/rubric_review/examples/min_rubric.json",
          "backend": "siliconflow",
          "slug": "rubric_review_examples_builtin_S2_20260515_201818_02",
          "reviewer_r1_model": "Pro/moonshotai/Kimi-K2.6",
          "reviewer_r2_model": "deepseek-ai/DeepSeek-V4-Flash",
          "arbitration_model": "deepseek-ai/DeepSeek-V4-Flash",
          "random_seed": 42
        }
      }
    }
  ],
  "summary_markdown": "/Users/cyning/Desktop/Projects/ai-ink-brain-api-python/docs/diary/jsonPKmermaid/rubric_runs/rubric_multiround_examples_builtin_20260515_201818.md"
}
```

### 3) 请按以下结构输出

1. **摘要**（6 条以内）：各轮终分矩阵 highlights、是否出现过仲裁、R1/R2 是否存在系统性偏高/偏低（结合多轮）。
2. **跨轮走势**：`clarity` / `risk`（或 Rubric 维度）随轮次变化与 **和工件内容变化** 的对应关系。
3. **分歧分析**：逐轮或汇总 R1/R2 分差；可能原因（Rubric 歧义、artifact 过短、追问脚本未带上下文等）。
4. **Rubric 质量**：维度是否覆盖要害；哪些情况应记为 `unknown` 而非硬扣分。
5. **工件与 manifest 建议**：下一轮如何改 `artifact_file`、是否在 S1 起显式附带「前一轮摘要」等。
6. `**risks`**：按建议改文档或流程后仍可能误导读者的点。
7. `**unknowns**`：无法从给定材料确认的事实列表。

