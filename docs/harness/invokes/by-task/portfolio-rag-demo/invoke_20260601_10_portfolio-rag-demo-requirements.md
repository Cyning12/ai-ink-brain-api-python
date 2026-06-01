# Invoke · 10 需求帽 · Portfolio RAG Demo task 草案

| 项 | 内容 |
| --- | --- |
| **帽** | 10 · 需求与任务分析 |
| **task_slug** | `portfolio-rag-demo` |
| **git_branch** | `task/portfolio-rag-demo-v1`（建议；10 帽可确认或调整） |
| **Open Folder** | `ai-ink-brain-api-python` |
| **freeze_id** | `PORTFOLIO-RAG-DEMO@2026-06-01` |
| **上游** | Prompt 00 SPEC 细化已关账（3/5 轮 · `active`） |
| **日期** | 2026-06-01 |

---

## 快照（§3 全文 · 占位符已替换）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（身份、只做什么、禁止什么、输出形状、停止条件、交接物）
- docs/harness/HARNESS_V2_PLAN.md §5（与 task 字段对齐时可引用）
- docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md（**SDD 三轮** · §4 待确认清单 · §5 完成后下一棒）

输入（已由人工替换占位符；若你仍看到 {{…}} 字样，须先追问用户，不得开工）：

【目标与上下文】
冻结 SPEC `PORTFOLIO-RAG-DEMO@2026-06-01` 已 active。请从 `docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md` §7 工作包（W2 RUNBOOK · W3 env 文档 · W5 预跑留证）拆出本仓 **`docs/tasks/active/task_portfolio_rag_demo_v1.md`** 可执行 task 草案。硬 deadline：**2026-06-09** 投递前 ingest 对齐 + 五问 RUNBOOK + 预发/生产等价环境 sync 与五问预跑留证。**禁止**改 `api/`/`tests/` 业务实现（本帽仅 task）；**禁止**执行生产 `admin/sync`。

【已有材料路径或粘贴说明】
ai-ink-brain-api-python/docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md
ai-ink-brain-api-python/docs/spec/governance/投递冲刺_20260609_v1_zh.md
ai-ink-brain-api-python/docs/spec/governance/PROMPT_00_SPEC-refine_Portfolio-RAG-Demo-v1_zh.md（只读 · 已关账）
ai-ink-brain/content/tasks/specs/SPEC-portfolio_demo_site_v1_zh.md（配对前端 · 只读）
ai-ink-brain-api-python/docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md（§C CONTENT_ROOT · §F admin/sync）

【是否按任务审核文档回填】（无则写「无」；有则写相对路径）
无

【SDD 三轮状态】（§2 合法取值之一）
轮0+1+2 已完成，清单已人确认

【是否新建或重大修订 SPEC】
否

你必须完成：
0. **Invoke 快照（开帽起点）**：在输出下列第 1 条起的实质性结果之前，先将 **本用户消息全文**（= 本模板 §3、占位符已全部替换）按 docs/harness/invokes/README.md 落盘到 `docs/harness/invokes/by-task/<task_slug>/`（含元数据表 + 快照 fenced code）。同一会话内追问 **不** 再新增快照文件。
1. **SDD 纪律（硬）**：
   - 若 `否` = **是**：须遵守三轮模型（§1）；**禁止** 在本帽一次生成整本 L1 SPEC。
   - 若 `轮0+1+2 已完成，清单已人确认`：可据 §下一棒 A/B 规则推荐 A 或 B；**三轮完成 ≠ 自动跳过 22**（见 SPEC §5）。
   - 若 `否` 且状态 = **`轮0+1+2 已完成，清单已人确认`**：跳过待确认清单，直接 task 定稿。
2. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表；矛盾单独小节（若有）。
2. 注明建议 test_strategy（required | recommended | not_applicable）及 test_strategy_note（若 not_applicable 须附理由）。
   - SPEC §7 建议：`test_strategy: recommended`；`failure_paths` 含 sync 维度失败、空 CONTENT_ROOT、job 404、五问 sources 不足。
   - task 元信息须含：`freeze_id: PORTFOLIO-RAG-DEMO@2026-06-01`、`semi_auto: true`（若适用）、`audit_profile: post_close`。
3. 若 AUDIT 路径非「无」：按该审查文档的回填清单逐条映射到 task 小节建议，并在建议文末注明「按审查 R<n> 回填」应指向的文件名。
4. 禁止：写业务实现代码；改 CI；在 task 中写绝对本机路径；把未在依赖中声明的契约当真值；执行生产 sync。
5. 对话回复 — **下一棒须输出两条 Prompt（由人择一执行，不可只给一条）**：
   - 先输出 **推荐判定**（1～3 行）：依据 10-requirements §下一棒 A/B 与 task 元信息；本 Epic 以 **docs 为主 + 人工 RUNBOOK**，推荐 **路径 A（22）** 除非人明示 hotfix。
   - **路径 A · 22 任务审核**：标题 `### 下一棒 A：22 任务审核 R1（推荐）`。正文 = TEMPLATE-task-audit-invoke §3 全文（占位符指向 `task_portfolio_rag_demo_v1`）。
   - **路径 B · 30 执行（跳过 22）**：标题 `### 下一棒 B：30 执行（跳过 22）`。正文 = TEMPLATE-execute-invoke §3 全文。
6. 回复末尾输出 HANDOFF_SEMI_AUTO §3.4 `📋 Harness 状态栏（版本 B）`。
7. **自动 commit**：若本轮已落盘 invoke 或已按用户授权写入 task，按 HANDOFF_AUTO_COMMIT 分仓 commit。用户写明「不要 commit」则跳过。

**task 落盘路径（硬）**：`docs/tasks/active/task_portfolio_rag_demo_v1.md`（本仓；禁止只写工作区 invokes 不落 task）。
```
