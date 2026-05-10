# 意图评测导出目录

- 默认输出：`intent_accuracy.jsonl` / `intent_accuracy.csv`（未设置 `CHATBI_V2_INTENT_EVAL_OUT` 时）。
- 自定义路径：见 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 中 `CHATBI_V2_INTENT_EVAL_OUT`。**相对路径**推荐 `tests/_out/<name>.jsonl` 或 `_out/<name>.jsonl`（锚定方式见真值表）。
- 自 `/private/tmp` 迁移的跑批样例：`intent_llm_*.jsonl` / `.csv`；是否纳入 git 由团队策略决定（体积与密钥残留风险）。
- **L4 / §7.5.5.1**：原始 SSE 可落 `sse_sample_l4.txt`、`l6_turn1.txt`、`l6_turn2.txt`；归档说明见 `docs/diary/2026-05-10-l4-sse-acceptance-archive.md`（含 prompt 全文，公开仓库勿盲提交）。
