# 帽链逐步 · gov-wiki-ingest-batch（v1）

> 全链入口：[`PROMPT_START_full_chain_v1.md`](./PROMPT_START_full_chain_v1.md)

## 3. 可复制 Prompt 正文

```text
单 task gov-wiki-ingest-batch · 22→关账

步骤 1 · 22：审 SPEC §2 十 slug · review · invoke_22 · commit

步骤 2 · 30：按 SPEC §3 写 10× syntheses + index + log
（可 3+3+4 分批 commit，但同会话完成）
invoke_30 · commit

步骤 3 · 40：task §VERIFY + §自检 · invoke_40 · commit

步骤 4 · 50：reinspect · 对照 10 slug 与 index · invoke_50 · commit

步骤 5 · 关账：done · git mv · _views · RECENT §6.6 ingest batch 行 · CLOSE_TRACE

关账前：syntheses 数 ≥15 · ST1–ST6。
```
