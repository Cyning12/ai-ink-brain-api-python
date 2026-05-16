# Rubric 元分析 — 可复制 Prompt 与结论文档

> **用途**：存放 **已填占位符**、可直接复制到对话的 User 消息，以及基于同批数据的 **元分析结论文档**（人读）。  
> **真值**：机器原始输出仍以 [`../rubric_runs/`](../rubric_runs/) 下 `rubric_multiround_*` / `rubric_review_*` 为准；本目录为派生物。

| 文件 | 说明 |
|------|------|
| [`copy_ready_user_message_rubric_201818.md`](./copy_ready_user_message_rubric_201818.md) | `batch_stamp=20260515_201818`、`run_name=examples_builtin`：角色 + 已嵌工件与合并 JSON 的完整消息 |
| [`meta_review_rubric_multiround_examples_builtin_201818.md`](./meta_review_rubric_multiround_examples_builtin_201818.md) | 对上列输入按 Prompt 结构撰写的元分析结论（示例） |

新建批次时：复制 `copy_ready_*.md` 命名规则，替换内文 JSON 与各轮 artifact 即可。
