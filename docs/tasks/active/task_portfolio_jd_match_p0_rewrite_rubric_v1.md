# Task：Portfolio 岗位 JD 匹配 — P0 改写 / rubric / 降级（三次 QA 驱动）

> **状态**：`active（草案 · 待 22 审核）`  
> **Epic**：Portfolio RAG Demo · **投递后增强**（**非** 6/9 五问硬门槛）  
> **QA 留证**：[`docs/diary/2026-06-01-portfolio-jd-match-three-qa-improvements_zh.md`](../diary/2026-06-01-portfolio-jd-match-three-qa-improvements_zh.md)  
> **关联图谱**：`api/query_rewrite.py` · `api/tools.py` · `api/chatbi_failure.py` · `api/intent_agent.py` · `api/intent_hints.py`  
> **依赖**：模型默认 [#118](https://github.com/Cyning12/ai-ink-brain-api-python/pull/118) 合 main 后验收 JD 场景

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `portfolio_jd_match_p0_rewrite_rubric_v1` |
| **semi_auto** | `false`（待 22 定稿后再开 30） |
| **test_strategy** | `required` |
| **test_strategy_note** | 涉 `api/query_rewrite` / `api/tools` / `api/chatbi_failure`；须 mock LLM + Timeline 断言；Moonshot JD fixture |
| **audit_profile** | `post_close` |
| **freeze_id** | （待定 · 22 帽分配） |
| **git_branch** | `task/portfolio-jd-match-p0-v1`（从 **最新 `origin/main`** 拉出） |
| **Open Folder** | `ai-ink-brain-api-python` |
| **blocked_by** | 无（可与 #118 并行规划；**验收**建议 #118 merge 后） |
| **blocks** | P1 并行 sub-RAG task（未建） |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-TASK-DRAFT | pending | 22-R1, 30 | 本草案待人审 |

---

## 背景与目标

Portfolio 演示站在 **Moonshot「AI Coding Mentor」** 类 **长 JD + 匹配度** 问法下，经 **三次人工 QA**（见 diary）暴露：

1. **单轮**无 session 时 rewrite **完全不工作**，整段 JD 进检索/generate。
2. **`RAG_GENERATE_UNCERTAIN`** 触发 **`direct_answer`**，在 Portfolio 语义下输出「您没提供背景」——与产品意图相反。
3. **多轮**靠 rewrite 借历史摘要「碰巧」可用，不可作为正式能力。
4. **DeepSeek-V4-Pro**（#118）显著改善 generate，但 **不替代** JD 切分与 rubric。

**完成态**：干净 **单轮** JD 问法可稳定走 RAG，输出结构化匹配分析，且 **不** 错误降级 direct_answer。

---

## 范围

| 在范围 | 说明 |
| --- | --- |
| **P0-1** 无历史长 Query 改写 | 扩展 `build_rewrite_llm_messages`：检测 JD/长文 → 仍调 LLM（或专用 `jd_match_rewrite` 分支） |
| **P0-2** Portfolio subject | Intent hints / generate system：匹配度类默认 **刘新宁** |
| **P0-3** 降级策略 | `chatbi_failure`：Portfolio site_mode + rag intent 下禁止 `RAG_GENERATE_UNCERTAIN → direct_answer` |
| **P0-4** generate rubric | `rag.generate` system 增加 JD 维度对齐模板 |
| **P0-5** 语料（跨仓） | 前端 `content/evidence/jd-match-profile.md` + sync |
| **P0-6** 前端排查 | `ai-ink-brain`：user 消息误含 `assistant` 段（diary ③） |

| 非范围 | 说明 |
| --- | --- |
| 多 Agent 编排全链 | 归 P1 |
| 改 ingest 512 分块算法 | 归 P1 / 独立 ingest task |
| 五问 RUNBOOK 变更 | 除非验收项增补 JD smoke |

---

## 失败路径

| Scenario ID | 触发 | 期望行为 |
| --- | --- | --- |
| **JD-01** | 单轮长 JD，无 history | rewrite **非空**；`rewritten_query` 短于原文 |
| **JD-02** | generate 含「不确定」 | **不** direct_answer；返回 partial + sources 或澄清 |
| **JD-03** | retrieve 空 | 明确「站内无对应证据」，仍指刘新宁为 subject |
| **JD-04** | user 仅「匹配度」无指代 | 默认刘新宁，不问「您是谁」 |

---

## 验收标准

- [ ] diary §验收建议 全部可勾选
- [ ] `tests/` 新增 Moonshot JD fixture（mock SiliconFlow）；覆盖 JD-01～JD-04
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 绿
- [ ] 50 落盘（`test_strategy: required`）
- [ ] 前端 jd-match-profile 文稿 ingest 后 sources 可命中

---

## 实现备忘（30 帽回填）

| 模块 | 预期触点 |
| --- | --- |
| `api/query_rewrite.py` | 无 history 长 query 分支；JD 检测启发式（长度 / 「职位描述」等） |
| `api/tools.py` | `rag_search_execute` generate system；可选独立 `_jd_match_system` |
| `api/chatbi_failure.py` | site_mode / intent 条件降级 |
| `docs/chatbi/v1/intent_hints.yaml` | JD / 匹配度 triggers |
| 前端 | `content/evidence/jd-match-profile.md`；Unified Chat 输入排查 |

---

## 给 Cursor

`portfolio`、`JD 匹配`、`query_rewrite`、`RAG_GENERATE_UNCERTAIN`、`Moonshot`、`task_portfolio_jd_match_p0`
