# POINTER · ChatBI 访客 token 本地生成脚本

> **脚本本体不在 Git**（2026-06 自 `docs/diary/` 迁出）。  
> **本机路径（仓库根）**：`tmp/diary/local_chatbi_access_token_gen.py`  
> **目录约定**：见 [`tmp/README.md`](../../tmp/README.md) §`tmp/diary/`

## 用途

- 本地生成 ChatBI `chatbi_access_tokens.key_hash` 与 **INSERT SQL** 模板
- Portfolio **P0-E** 访客秘钥：可复制邮件正文（含北京时间发放/失效、`PORTFOLIO_DEMO_URL`）
- 哈希算法与运行时 [`api/chatbi_access_hash.py`](../../api/chatbi_access_hash.py) 一致

## 常用命令（仓库根）

```bash
# 普通访客 · 72h（投递冲刺 P0-E）
python3 tmp/diary/local_chatbi_access_token_gen.py \
  --level 2 --subject-user-id u_demo --label portfolio-visitor --expires-in-days 3 \
  --demo-url https://ai-ink-brain.vercel.app

# 五问验收 curl（RUNBOOK §1.4）
python3 tmp/diary/local_chatbi_access_token_gen.py \
  --level 2 --subject-user-id u_demo --label portfolio-five-q --expires-in-days 7
```

## 关联文档

| 文档 | 说明 |
| --- | --- |
| [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) | `CHATBI_ACCESS_TOKEN_PEPPER` 与脚本对齐 |
| [`docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) | §1.4 运维签发 visitor token |
| [`docs/spec/governance/投递冲刺_20260609_v1_zh.md`](../spec/governance/投递冲刺_20260609_v1_zh.md) | P0-E 访客秘钥 |
| [`docs/tasks/done/task_chatbi_level_gate_v1.md`](../tasks/done/task_chatbi_level_gate_v1.md) | 分级闸门与 key_hash RUNBOOK |

**历史路径** `docs/diary/local_chatbi_access_token_gen.py` 已废弃；全文检索请搜 `POINTER_local_chatbi` 或 `tmp/diary/local_chatbi_access_token_gen.py`。
