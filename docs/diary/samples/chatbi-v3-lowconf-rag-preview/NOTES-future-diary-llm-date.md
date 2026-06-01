# 联调备忘 · 「未来日记」误判（非 §5-3 缺陷）

**日期**：2026-05-31  
**关联样本**：[`round2_token_bypass_execute_timeline.json`](round2_token_bypass_execute_timeline.json) · `run_id=df8593fb-…`

## 现象

用户问「`2026-04-28日记的大致内容`」，在 **5-3 闸门已通过**（预览卡 → 按预览执行 → `plan_execution_token` 校验 → 执行 `rag_search`）后：

1. `rag_search` 返回 **`RAG_GENERATE_UNCERTAIN`** 或空，Timeline **无** `rag.sources`。
2. Agent **fallback** `direct_answer`，助手回复将 **2026-04-28** 当作「未来日期」（措辞含「截至当前（2025年）」类表述），与知识库内真实日记日期不符。

## 根因假设（待实现验证）

| 层级 | 说明 |
|------|------|
| **主因** | RAG **生成**与 **`direct_answer`** 的 system prompt **未注入「当前日期 / 仓库时间锚点 / 日记为知识库内历史文档」**，模型用训练截止默认「当前≈2025」，把 2026-04-28 判为未来。 |
| **代码锚点** | `api/tools.py` · `rag_search_execute` 生成段：`system = "你是一个检索增强问答助手…"`（约 L280–283），**无** `date.today()` 或 `PROJECT_CONFIG` 时间说明。 |
| **次因** | 检索命中弱或 generate 不确定 → 走 `direct_answer`，该路径 `system = "你是一个中文助手。请直接回答用户问题。"`（约 L835），同样 **无** 日期与 KB 边界。 |
| **非主因** | §5-3 低置信预览 / token / clarify 机制；Intent 联调 `INTENT_MIN_CONFIDENCE=1.0` 仅用于触发路线 A。 |

## 建议后续（单独 task，勿阻塞 5-3 关账）

1. **Prompt**：在 RAG generate 与 `direct_answer` system 中增加一行，例如：「今天是 {ISO 日期}；用户提到的日记日期指知识库内已入库文档，勿以模型训练截止年判断是否为未来。」
2. **配置**：是否在 `PROJECT_CONFIG` / `.env` 暴露 `AGENT_WALL_CLOCK_DATE`（测试可固定）。
3. **回归**：问句固定为 `2026-04-28日记的大致内容`，断言 **不** 出现「未来日期」且（有命中时）`rag.sources` 非空。
4. **Ink**：执行链仍可能显示 `SQL_DRAFT: -`（RAG 无 sql_draft），属展示层，与本案无关。

## 与验收边界

- **§5-3 机制**：预览、`plan_execution_token`、确认按钮、第二轮无 `clarify` 执行 `rag_search` → **已通过**（见 task done + reinspect）。
- **端到端答案质量**：依赖检索命中 + 生成 prompt；本案记为 **已知 gap**，不 retro 否决 5-3。
