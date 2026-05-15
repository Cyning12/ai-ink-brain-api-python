# tools/rubric_review — Rubric 双人 LLM 评审 CLI

> **位置**：`ai-ink-brain-api-python/tools/rubric_review/`  
> **用途**：对 PR 正文、技术方案等 **文本工件** 按 JSON Rubric 做 **两次独立模型调用**，按 `adjudication_rules` 自动合并或 **LLM 仲裁** / **仅 webhook 待人工**。  
> **默认 Rubric（与本项目对齐）**：`docs/diary/jsonPKmermaid/rubric_pr_and_design_v1.json`（与 `可复用 Rubric 模板.json` 内容一致）。

## 依赖

- `requirements.txt`：`openai`（SiliconFlow 亦为 OpenAI 兼容协议）、`anthropic`、`requests`。
- **默认后端 `siliconflow`**：与 `api/chain_chat.py` 一致，使用 **`SILICONFLOW_API_KEY`** + `api.rag_env.siliconflow_base()`（`SILICONFLOW_BASE_URL` 可选）。
- **不使用 `SILICONFLOW_CHAT_MODEL`**。双人盲审模型池写死在 `config.SILICONFLOW_REVIEWER_MODEL_POOL`：
  - `deepseek-ai/DeepSeek-V4-Flash`
  - `Pro/moonshotai/Kimi-K2.6`  
  每次运行将 **池内两模型洗牌** 分配给 R1/R2；**仲裁**再从池中 **随机选一**（可与 R1 或 R2 相同）。报告与 JSON 的 `meta` / `run` 会写明 **R1/R2/仲裁** 各自模型；可用 `--random-seed` 固定分配以便复现。

## 常用环境变量

| 变量 | 说明 |
|------|------|
| `RUBRIC_REVIEW_BACKEND` | `siliconflow`（**默认**）、`openai`、`anthropic` |
| `SILICONFLOW_API_KEY` | SiliconFlow 密钥（与 `chain_chat` 同源） |
| `SILICONFLOW_BASE_URL` | 可选；未设置时用 `rag_env` 默认 |
| `RUBRIC_REVIEW_MODEL` | 仅 **openai / anthropic**：单模型（R1/R2/仲裁相同） |
| `RUBRIC_REVIEW_OPENAI_MODEL` / `RUBRIC_REVIEW_ANTHROPIC_MODEL` | 同上后端默认模型 |
| `RUBRIC_REVIEW_WEBHOOK_URL` | 争议/完成时 POST 的回调 URL |

## CLI

在 **`ai-ink-brain-api-python` 仓根**执行：

```bash
python -m tools.rubric_review \
  --artifact-file path/to/pr_body.md \
  --rubric docs/diary/jsonPKmermaid/rubric_pr_and_design_v1.json \
  --random-seed 42 \
  --webhook-url "https://example.com/hooks/rubric" \
  -v
```

| 参数 | 说明 |
|------|------|
| `--artifact-file` | 待评审 UTF-8 文本文件（必填） |
| `--rubric` | Rubric JSON（必填） |
| `--backend` | `siliconflow` \| `openai` \| `anthropic` |
| `--model` | 仅 openai/anthropic：覆盖 R1/R2/仲裁共用模型 |
| `--random-seed` | 可选 `int`，固定 SiliconFlow 下 R1/R2/仲裁 的随机分配 |
| `--output-dir` | 默认 `docs/harness/reviews/` |
| `--slug` | 输出文件名前缀 |
| `--webhook-url` | 覆盖环境变量；见 `webhook.py` |
| `--arbitration-override` | `llm` \| `human_webhook` |
| `--max-retries` | API 重试次数（默认 5） |
| `--log-file` | 追加日志 |
| `-v` | DEBUG |

**退出码**：`0` 正常；`2` 参数/文件错误；`3` `human_webhook` 待人工（终分含 `null`）。

## Webhook 载荷

见 `webhook.build_generic_arbitration_payload`：

- `rubric_review.dispute_opened`
- `rubric_review.arbitration_llm_done`
- `rubric_review.human_arbitration_required`

## 输出

- `docs/harness/reviews/rubric_review_<slug>_<timestamp>.md`（元信息表含 **R1/R2/仲裁模型** 与随机种子）
- `docs/harness/reviews/rubric_review_<slug>_<timestamp>.json`

**注意**：此类文件 **不等价** 于任务审核帽的 `task_*_audit_R*.md`。

## 给 Cursor

`rubric_review`、`SILICONFLOW_API_KEY`、`SILICONFLOW_REVIEWER_MODEL_POOL`、`DoubleBlindReviewer`、`docs/harness/reviews`
