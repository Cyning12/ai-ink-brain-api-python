# review_results / 审查结果落盘（本后端仓）

> **用途**：存放 **规格 / 任务审查帽**（工作区 [`docs/harness/prompts/20-review-spec-task.md`](../../../../docs/harness/prompts/20-review-spec-task.md)）对本仓 **task / SPEC** 的 **缺口与可测性** 审查结论，便于追溯与交给 **需求帽** 回填 `docs/tasks/`、`docs/spec/`。  
> **注意**：本目录 **不是** `task_*.md` 任务单本体；不替代 `active/`、`done/` 状态流。

---

## 何时写入

- 审查帽输出 **阻塞项 / 非阻塞建议 / 给需求帽的回填清单** 后，将 **可归档版本** 存一份于此（可选：注明关联 PR、关联 `docs/tasks/active/...` 路径）。

---

## 命名建议

- `review_<主题简写>_YYYYMMDD_vN.md`  
  例：`review_chatbi_v3_security_p1_p2_20260513_v1.md`

**现有归档**：

- [`review_chatbi_v3_security_p1_p2_20260513_v1.md`](review_chatbi_v3_security_p1_p2_20260513_v1.md) — ChatBI V3 Security，P1-1 / P1-2 + SPEC（**R1**，2026-05-13）  
- [`review_chatbi_v3_security_p1_p2_20260513_v2.md`](review_chatbi_v3_security_p1_p2_20260513_v2.md) — 同上主题 **R2**（回填后再审，**零阻塞** + 执行门闸，2026-05-13）；文末 **§七 R3**（2026-05-14 复核追加）

---

## 正文建议结构（最小）

1. **元信息**：关联 task / SPEC 路径（相对本仓根或工作区 `Projects/`）、审查日期、`freeze_id` 若适用。  
2. **阻塞项** / **非阻塞建议**（与帽子输出形状一致即可）。  
3. **给需求帽的回填清单**（可逐条勾选后由需求帽改文档）。

---

## 回填闭环

- 需求帽入口：[`docs/harness/prompts/10-requirements.md`](../../../../docs/harness/prompts/10-requirements.md)  
- 回填完成后：可在本文件顶部加一行 **「已回填 / 日期 / PR」**，不必强制移动文件。

---

## 与前端 `content/tasks/review_results/` 的关系

- **本仓 task / SPEC** 的审查归档 **以本目录为准**。  
- 前端仓 `ai-ink-brain/content/tasks/review_results/` 可作跨仓备忘或纯前端任务审查；勿与后端真值双份漂移。

---

## 给 Cursor 的稳定关键词

`Harness`、`审查帽`、`review_results`、`回填`、`failure_paths`、`test_strategy`、`freeze_id`
