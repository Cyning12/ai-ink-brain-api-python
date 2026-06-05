# Portfolio · 岗位 JD 匹配 — 三次 QA 留证与改进 backlog

| 项 | 内容 |
| --- | --- |
| **日期** | 2026-06-01 |
| **场景** | Portfolio 演示站 Unified Chat · 用户粘贴 **Moonshot「AI Coding Mentor」** 岗位 JD，问「匹配度如何」 |
| **站点 subject** | 演示站默认「他」= **刘新宁**（`intent_hints.yaml` · `content/resume/`） |
| **关联 task** | [`task_portfolio_jd_match_p0_rewrite_rubric_v1.md`](../tasks/active/task_portfolio_jd_match_p0_rewrite_rubric_v1.md) |
| **模型 PR** | [#118](https://github.com/Cyning12/ai-ink-brain-api-python/pull/118) — Chat/Intent 默认 **DeepSeek-V4-Pro**（本 QA ③ 实测模型） |
| **性质** | **diary 留证**；非 L0 实现真值；结论冻结后须同步 task / SPEC |

---

## 今日结论（TL;DR）

1. **三次跑法差异巨大**：单轮弱模型 → RAG 失败 + 错误降级；多轮有历史 → rewrite 借摘要勉强可用；单轮 + V4-Pro → 主观「非常好」，但 **rewrite 仍未压缩 JD**。
2. **根因不在 Intent 路由**：三次均为 `rag_search`、高置信；问题在 **长 Query 无改写**、**generate 不确定判定**、**RAG 失败 → direct_answer** 降级链。
3. **模型升级是必要非充分**：PR #118 解决 generate 质量；**P0 仍须**单轮 JD 切分/改写、Portfolio subject 默认、禁止 Portfolio 场景错误 direct_answer。
4. **③ 存在输入污染**：`user.message` 末尾误含 `assistant\n刘新宁简介…`（非 session 历史）；须排查前端复制/拼接，**不能**当产品能力依赖。

---

## 测试问法（共用 JD 骨架）

用户消息形态（三次相同 JD 正文，问句略有差异）：

```text
我的岗位JD如下，你觉得（他/刘新宁）的匹配度如何？
——————
AI Coding Mentor
…（造题/数据集/评测/RL 后训练 · 3–10 年一线工程 · 代码洁癖 · 「助教人格」…）
```

**与五问 chip 的差异**：五问为 **短问、单主题**；JD 匹配为 **复合任务**（解析 JD 维度 + 对齐 resume/evidence 证据 + 输出 rubric 式结论）。

---

## 三次 QA 对照表

| 维度 | ① 单轮 · 弱模型 | ② 多轮 · 弱模型 | ③ 单轮 · V4-Pro |
| --- | --- | --- | --- |
| **前置** | 直接贴 JD | 先问「简单介绍下刘新宁」再贴 JD | **新对话**（Intent：**无历史对话**） |
| **Intent** | `rag_search` ~0.92 | 同左 | 同左 |
| **模型（Timeline debug）** | 推测 Qwen2.5-7B / Flash | 同左 | **deepseek-ai/DeepSeek-V4-Pro**（Intent + `rag.generate`） |
| **rewrite** | `latency_ms: 0`；`rewritten_query` = **全文 JD** | ~6.7s；压成带 **刘新宁摘要** 的短检索句 | `latency_ms: 0`；**未改写**（= 超长原文） |
| **rewrite 原因** | 无 session 历史 → `build_rewrite_llm_messages` 返回 `None` | 有 history → 走 LLM 改写 | 同① |
| **rag_search** | `RAG_GENERATE_UNCERTAIN` | 成功 | 成功 |
| **sources** | 无有效答案 | resume×4 + methodology 卷一×6 | resume + methodology；含 Mentor/评测映射 chunk |
| **最终路径** | **direct_answer** | RAG 直答 | RAG 直答 |
| **答案基调** | 「您没提供背景信息」 | 「较高，**方向偏差**」（偏 RL/训练侧） | 「**非常高** / 量身定制」 |
| **耗时** | ~143s | ~73s | ~58s |

---

## 分轮根因（Timeline 对齐）

### ① 单轮 · 最差路径

| 环节 | 代码落点 | 现象 |
| --- | --- | --- |
| rewrite 空转 | `api/query_rewrite.py::build_rewrite_llm_messages` — **无 history 返回 None** | 首轮长问句零压缩 |
| generate 失败 | `api/tools.py::rag_search_execute` — `_rag_should_treat_as_uncertain` | 答案含「无法/不确定」即整段失败 |
| 错误降级 | `api/chatbi_failure.py` — `RAG_GENERATE_UNCERTAIN → direct_answer` | Portfolio 无简历上下文时 **语义反转** |

### ② 多轮 · 「碰巧修好」

- rewrite 将上一轮 assistant **简介摘要**写入 `rewritten_query`，等价于补全 subject，检索噪声下降。
- **不是产品设计**：依赖用户先问 Q1；单轮 JD 场景仍失败。
- 生成仍偏 **RL/造题/后训练**，对 **Harness/方法论/带教** 证据利用不足 → 「方向偏差」。

### ③ 单轮 · V4-Pro · 需更正的变量

| 因素 | 是否成立 | 说明 |
| --- | --- | --- |
| Session 多轮历史 | ❌ | Intent 明确「无历史对话」 |
| rewrite 压缩 JD | ❌ | `rewritten_query` 仍等于原文 |
| **生成模型 V4-Pro** | ✅ **主因** | 同一套 sources/score 下，generate 能把 Harness/连载对齐到「设计作业/助教」叙事 |
| **user 内误贴 assistant 简介** | ✅ **次因** | 单条 message 含 JD + 分隔符 + 误粘贴的候选人摘要；**非**服务端 session 恢复 |
| Mentor 映射 chunk | ✅ 小加分 | sources 命中「Mentor/评测」相关 methodology 块 |

**待排查（前端）**：新对话下 `user.message` 为何带 `assistant\n…` 前缀段 — 复制污染 vs UI 拼接 bug。

---

## 与现有栈的能力边界

| 能力 | 五问 short query | JD 匹配 long query |
| --- | --- | --- |
| 512 字固定分块 ingest | 够用 | JD 噪声淹没 embedding |
| 无历史 rewrite | 可接受 | **不可用** |
| 单次 rag_search | 够用 | 应多维度 / 分条检索 |
| Intent hints（人名） | Q4 够用 | 未覆盖「粘贴 JD + 他=谁」 |
| `RAG_GENERATE_UNCERTAIN → direct_answer` | 偶发 | Portfolio **高危** |

---

## 改进 backlog（摘要 · 详 task）

### P0 — 投递后优先（不依赖多 Agent）

| ID | 项 | 要点 |
| --- | --- | --- |
| **P0-1** | **长 Query / JD 切分改写** | 无 history 时也须 LLM：拆 JD 维度 + 固定 subject=刘新宁 + 输出短检索句 |
| **P0-2** | **Portfolio subject 默认** | 「匹配度」类问句默认指站点主人 |
| **P0-3** | **降级策略** | Portfolio + rag intent 下禁止 `RAG_GENERATE_UNCERTAIN → direct_answer` |
| **P0-4** | **generate rubric 提示** | 维度对齐 / 证据引用 / 缺口说明 |
| **P0-5** | **语料** | `content/evidence/jd-match-profile.md` |
| **P0-6** | **前端** | 排查 user 消息误含 assistant 段 |

### P1 — 质量与性能

| ID | 项 | 要点 |
| --- | --- | --- |
| **P1-1** | **并行 sub-RAG** | JD 维度切分 → 并行检索 → 合并 generate |
| **P1-2** | **标题感知分块** | ingest `section_header` |
| **P1-3** | **评测** | Moonshot JD fixture + Timeline 断言 |

### 已做

| 项 | 状态 |
| --- | --- |
| 默认模型 V4-Pro | PR #118 |

---

## 验收建议（改进完成后）

- [ ] **干净单轮**：仅 JD +「刘新宁匹配度如何」，无 assistant 污染
- [ ] `rewritten_query` 显著短于原 JD；含「刘新宁」
- [ ] 不出现 `RAG_GENERATE_UNCERTAIN → direct_answer`
- [ ] sources ≥1 `resume/*`；答案含 Harness/方法论/带教证据
- [ ] 模型：`deepseek-ai/DeepSeek-V4-Pro`

---

## 关联引用

| 用途 | 路径 |
| --- | --- |
| rewrite | `api/query_rewrite.py` |
| RAG 工具链 | `api/tools.py::rag_search_execute` |
| 失败降级 | `api/chatbi_failure.py::FailureTypeHandler` |
| Intent hints | `docs/chatbi/v1/intent_hints.yaml` |
| Portfolio SPEC | `docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md` §4.5 |
| 执行 task | `docs/tasks/active/task_portfolio_jd_match_p0_rewrite_rubric_v1.md` |
