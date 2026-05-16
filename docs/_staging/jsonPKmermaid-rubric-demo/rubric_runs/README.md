# Rubric 运行产物目录

本目录由 `python -m tools.rubric_review` / `python -m tools.rubric_review.multi_round` **默认写入**：

- `rubric_review_<slug>_<timestamp>.md` / `.json` — 单轮（或多轮中的每一轮）
- `rubric_multiround_<run_name>_<timestamp>.md` / `.json` — 多轮合并索引

与 **`docs/harness/reviews/`**（任务审核帽 `task_*_audit_R*`）**分开存放**，避免混读。
