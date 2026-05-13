# reinspect_results / 任务复检落盘（本后端仓）

> **用途**：存放 **独立复检帽**（工作区 [`docs/harness/prompts/50-independent-reinspect.md`](../../../../docs/harness/prompts/50-independent-reinspect.md)）对 **diff + 日志 + 验收表** 的逐项 **pass / fail** 结论，便于合并决策与事后审计。若复检指出文档缺口，可将 **回填清单** 交给 **需求帽** 更新 task / SPEC。  
> **注意**：本目录 **不是** 任务单；复检 Agent **默认不改代码**（除非任务明确要求复检提交 patch）。

---

## 何时写入

- PR / 分支自检后，复检帽输出 **验收项表格 + 阻塞合并项** 时，将定稿存于此。  
- **证据不足** 时：仍落盘，并列出需补充材料，避免口头结论漂移。

---

## 命名建议

- `reinspect_<主题简写>_YYYYMMDD_vN.md`  
  例：`reinspect_chatbi_v3_sql_gate_pr123_20260513_v1.md`

---

## 正文建议结构（最小）

1. **元信息**：关联 PR / 分支、commit 短哈希、关联 `docs/tasks/.../task_*.md` 路径。  
2. **验收表**：`验收项 | pass/fail | 证据 | 备注`。  
3. **阻塞合并项**（若有）。  
4. **给需求帽的回填清单**（仅当 fail 根因是 SPEC/task 缺口时填写；无则写「无」）。

---

## 回填闭环

- 需求帽入口：[`docs/harness/prompts/10-requirements.md`](../../../../docs/harness/prompts/10-requirements.md)  
- 文档已按清单修正后：可在本文件顶部标注 **「文档已回填 / PR」**。

---

## 与前端 `content/tasks/reinspect_results/` 的关系

- **本仓任务** 的复检归档 **以本目录为准**。  
- 前端仓同名目录仅用于前端任务或跨仓备忘。

---

## 给 Cursor 的稳定关键词

`Harness`、`复检帽`、`reinspect_results`、`pass/fail`、`证据`、`阻塞合并`、`回填`
