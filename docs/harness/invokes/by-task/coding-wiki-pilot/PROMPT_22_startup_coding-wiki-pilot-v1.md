# 启动 Prompt · 22 任务审核帽 · Coding Wiki 试点（v1.2）

> **帽链（本会话计划）**：**22 → 30 → 40 → 50 → 关账**（各帽建议 **新对话** + 对应 `PROMPT_*_startup`）  
> **用法**：Open Folder **`ai-ink-brain-api-python/`** → 新对话 → **全文复制**下方代码块。  
> **task**：`docs/tasks/active/task_coding_wiki_pilot_v1.md` · `git_branch`: `task/coding-wiki-pilot-v1`  
> **下一棒**：审查无阻塞后 → [`PROMPT_30_startup_coding-wiki-pilot-v1.md`](./PROMPT_30_startup_coding-wiki-pilot-v1.md)

| 后续帽 | 启动稿 |
|--------|--------|
| 30 | [`PROMPT_30_startup_coding-wiki-pilot-v1.md`](./PROMPT_30_startup_coding-wiki-pilot-v1.md) |
| 40 | [`PROMPT_40_startup_coding-wiki-pilot-v1.md`](./PROMPT_40_startup_coding-wiki-pilot-v1.md) |
| 50 | [`PROMPT_50_startup_coding-wiki-pilot-v1.md`](./PROMPT_50_startup_coding-wiki-pilot-v1.md) |
| 关账 | [`PROMPT_CLOSE_coding-wiki-pilot-v1.md`](./PROMPT_CLOSE_coding-wiki-pilot-v1.md) |

---

```text
你正在扮演 Harness「任务审核帽（22 · R1）」（本 Epic：Coding Wiki 试点 · T1b · 后端子仓），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/templates/TEMPLATE-task-audit-invoke.md §3
- docs/harness/reviews/README.md（落盘 by-task/<task_slug>/）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc
- 说明：Harness 帽子链 ≠ Cursor Skills

【开帽 · Invoke 快照】在输出审查正文之前，将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/coding-wiki-pilot/invoke_20260526_22_coding-wiki-pilot-v1.md
（元信息表：hat_id=22、task_slug=coding-wiki-pilot、freeze_id=CODING-WIKI-PILOT@2026-05-25；同会话追问不新建 invoke）

输入（占位符已替换；若仍见 {{…}} 须追问）：
- 待审 task（相对子仓根）：
  docs/tasks/active/task_coding_wiki_pilot_v1.md
- 关联 SPEC：
  docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md（T1b）
- 指导意见（只读 · 工作区）：
  Projects/docs/harness/guides/GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md
- 上一轮审查：
  无
- 本轮：R1 · 日期 20260526 · slug coding_wiki_pilot_v1
- worktree_root / git cwd：
  .（子仓根；分支 task/coding-wiki-pilot-v1）
- freeze_id：CODING-WIKI-PILOT@2026-05-25
- SDD 三轮：不涉及新 SPEC

0b. 人工闸：HG-TASK-DRAFT、HG-WIKI-INGEST-SCOPE 须为 **approved**；否则拒开工。

你必须完成（R1 · 按序）：

1. 通读 task：§帽子顺序、§范围/§非范围、§failure_paths、§验收标准、首期 ingest 三件套（done 路径须 `test -f` 验证）。

2. 对照 HARNESS_V2_PLAN §5：`test_strategy: not_applicable` 理由是否充分；`failure_paths` F1–F4 是否可操作。

3. **落盘审查 md**（零阻塞亦须写；禁止只在对话说「过了」）：
   docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md

   文内结构（硬）：
   - 元信息表（含 task_path、invoke_snapshot、freeze_id、audit_round=R1）
   - 审查结论摘要（阻塞 / 非阻塞分项）
   - 审查焦点结论：
     · Wiki vs Harness / _tech_graph **双真值** 风险
     · ingest「摘要 + 链 task」vs 复制 SPEC/review 全文
     · `docs/harness/prompts/` 零改动承诺
     · 三个 done task 路径存在性
   - 是否建议 **30 帽开工**（须无阻塞才可「建议开工」）
   - **签收 / 关闭**（R1：是否准许进入 30）
   - **下一棒可复制 Prompt**（`text` 围栏）：若准许开工，**全文嵌入**下一文件 §代码块内容（勿省略）：
     docs/harness/invokes/by-task/coding-wiki-pilot/PROMPT_30_startup_coding-wiki-pilot-v1.md
     并注明后续帽链：**30 → 40 → 50 → PROMPT_CLOSE**

4. **禁止**：写业务代码；新建 `docs/coding_wiki/`（属 30）；改 `docs/harness/prompts/`、api/、CI。

5. **Commit**（仅本子仓 · 禁止 git add -A）：
   git add docs/harness/reviews/by-task/coding-wiki-pilot/ docs/harness/invokes/by-task/coding-wiki-pilot/invoke_20260526_22_*.md
   message 含 freeze_id CODING-WIKI-PILOT@2026-05-25

6. 对话末尾：**📋 Harness 状态栏（版本 B）**；复述「下一棒 = 30」并提示人 **新开对话** 粘贴 PROMPT_30。

硬约束：
- Open Folder = **ai-ink-brain-api-python/**（非仅 Projects）
- 仍有阻塞时 **禁止** 指示 30 开工
- 审查 md 与对话末节 Prompt 须 **语义一致**

关键词：22、R1、Coding Wiki、ingest、双真值、by-task、coding-wiki-pilot、22→30→40→50
```
