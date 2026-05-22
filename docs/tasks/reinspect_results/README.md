# reinspect_results / 三方复检落盘（本后端仓）

> **用途**：**50 帽（独立复检）** 的 **人类可读、可查收** 书面结论；供维护者合并决策与事后审计。  
> **真值**：[`../harness/ACCEPTANCE_LANDING.md`](../harness/ACCEPTANCE_LANDING.md)、[`../harness/prompts/50-independent-reinspect.md`](../harness/prompts/50-independent-reinspect.md)。  
> **模板**：[`../harness/prompts/TEMPLATE-independent-reinspect-invoke.md`](../harness/prompts/TEMPLATE-independent-reinspect-invoke.md)（占位符 `{{REINSPECT_OUTPUT_PATH}}` 指向本目录）。

---

## 何时写入（强制）

- task `test_strategy: required` 或验收标准要求「三方复检 / 50 帽」；  
- **40 自检** 已回填 task 后，**50 开帽**；  
- **禁止** 仅在对话输出 pass/fail 而不落盘本目录。

证据不足时仍须落盘，并列出需补充材料。

---

## 命名

- `reinspect_<主题简写>_YYYYMMDD_vN.md`  
- 例：`reinspect_docs_tasks_p0_20260522_v1.md`

---

## 正文最小结构

1. **元信息**：关联 task 路径、`git_branch`、commit 短哈希、复检日期。  
2. **验收表**：`验收项 | pass/fail | 证据 | 备注`。  
3. **阻塞合并项**（无则写「无」）。  
4. **结论**：建议合并 / 不建议合并 / 证据不足。  
5. **给需求帽回填**（仅文档缺口；无则「无」）。

---

## 与 invoke / 人工闸

- 50 开帽 invoke 快照：[`../harness/invokes/`](../harness/invokes/README.md)  
- `human_gate`（如 `HG-REINSPECT`、`HG-GLOBAL-SIGNOFF`）**approved** 后方可 `done` / 合并（人改，见 [`../harness/prompts/HANDOFF_SEMI_AUTO.md`](../harness/prompts/HANDOFF_SEMI_AUTO.md)）

---

## 回填闭环

文档缺口 → [`../harness/prompts/10-requirements.md`](../harness/prompts/10-requirements.md) 更新 task/SPEC → 可开 **50 v2** 复检文件。

---

## 给 Cursor

`Harness`、`50`、`reinspect_results`、`三方复检`、`pass/fail`、`证据`、`ACCEPTANCE_LANDING`
