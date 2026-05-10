# Task：ChatBI V2 —— 验收执行引导（Runner）

状态：active（随总规 §7.5 更新；**不替代** `SPEC-ChatBI-V2-Agent-Overview.md` 原文）  
范围：后端 `ai-ink-brain-api-python`；跨仓步骤仅列引用  
**权威真值**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` **§7**（验收勾选）、**§7.4**（全量对照）、**§7.5**（L0–L7 操作细则）  
关联：`SPEC-ChatBI-V2-Gap-Checklist.md` · `docs/tasks/done/task_chatbi_v2_agent_p1_behavior.md`（P1 已归档）· `docs/diary/L5-ChatBI-V2-FailureTypeHandler-pytest指南.md` · **`docs/tasks/done/task_chatbi_v2_docs_acceptance_archive_2026-05-11.md`**（V2 SPEC/任务归档总索引）· **`task_chatbi_v3_planning_after_resume_v1.md`**（V3 规划入口）

---

## 0. 开始前

1. **工作目录**：终端 `cd` 到本仓根目录 **`ai-ink-brain-api-python`**（下文命令均以此为 cwd）。  
2. **Python**：已激活 venv；`export PYTHONPATH=.`（或与总规 §7.5 一致的一行命令内联 `PYTHONPATH=.`）。  
3. **密钥**：`SILICONFLOW_API_KEY`、Supabase、Admin Token 等**仅本机 export**，勿写入仓库、勿贴公开处；详见总规 **§7.5.1**。  
4. **里程碑口径**（总规 **§11**）：L5–L7 曾**暂停集中验收**；恢复排期时继续执行 **§7.5.4–§7.5.6** 并回写 Gap / §7.4。本文用于**你个人按层跑通**，不自动表示「总规 100% 闭合」。

---

## 1. 推荐验收顺序（由浅入深）

| 顺序 | 层级 | 目的 | 何时必做 |
|:----:|------|------|----------|
| 1 | **L0** | 契约 + 全量 pytest（stub 为主） | **最小发布前必做**（总规 §7.5 摘要） |
| 2 | **L3** | Unified V2 Agent 单测 | **最小发布前必做** |
| 3 | **L1** | 60 条 Intent 真实 LLM 评测 | 发版说明**承诺 Intent 质量**时 |
| 4 | **L2** | Intent 延迟基准 | **承诺延迟 SLA** 时（纸面 §7.2 已知未达标，见总规 §7.2） |
| 5 | **L4** | 实 SSE 链路与事件序 | **上线前后烟测**建议 |
| 6 | **L5** | `error_code` fallback / gating 矩阵 | 对外宣称与 **§2.4 完全等价**前 |
| 7 | **L6** | 跨仓 UI + 可选多轮 §7.5.5.1 | **全栈体验**或宣称**多轮/记忆**时 |
| 8 | **L7** | 运维、env、DB 迁移 | **生产/staging** 发布前后 |

---

## 2. 各层操作步骤（命令与准则）

> **细则以总规为准**；下表为「一页能跑」的摘要，命令与总规 **§7.5.2** 一致。

### 2.1 L0 — 契约 + pytest

| 项 | 内容 |
|----|------|
| 目的 | `tech_graph_contract_check` + 默认 `pytest tests`（含若干 skip 为常态） |
| 命令 | `PYTHONPATH=. python tools/tech_graph_contract_check.py && PYTHONPATH=. python -m pytest tests -q --tb=short` |
| **`.env` 与卡死** | `api/rag_env` 使用 `load_dotenv(..., override=False)`：终端 `unset` **不能**撤销 pytest 进程里随后从 `.env` 补上的 `CHATBI_V2_INTENT_*`。仓库已用 **`tests/conftest.py`** 在导入 `api` 之前将 `CHATBI_V2_INTENT_EVAL` / `BENCH_RUN` / `LLM` 默认置为 `false`，避免 L0 误跑 60 条外呼卡死。若你**刻意**要在同一次 pytest 里沿用 `.env` 的评测开关，请设置 **`CHATBI_PYTEST_KEEP_INTENT_ENV=1`** 再执行。 |
| 通过 | contract **OK**；pytest 全绿或仅预期 skip；耗时通常 **一分钟内**（明显更长再查网络/杀毒） |
| 归档 | 终端输出或 CI 截图；可选记入 `docs/diary/`（若 `docs/` 被 ignore，归档需 `git add -f`，见既有 diary 说明） |

### 2.2 L3 — Unified V2 Agent 单测

| 项 | 内容 |
|----|------|
| 目的 | `CHATBI_USE_AGENT=true` 下 V2 Agent 路径单测全绿 |
| 命令 | `CHATBI_USE_AGENT=true PYTHONPATH=. python -m pytest tests/test_unified_chat_backend_v2_agent.py -q --tb=short` |
| 通过 | 全绿 |
| 扩展 | L5 向 mock 矩阵见 `docs/diary/L5-ChatBI-V2-FailureTypeHandler-pytest指南.md` · `tests/test_unified_chat_backend_v2_agent.py` 文件头注释 |

### 2.3 L1 — Intent 60 条（真实 LLM）

| 项 | 内容 |
|----|------|
| 前置 | 已 `export SILICONFLOW_API_KEY` 等（§7.5.1） |
| **必带** | **`CHATBI_PYTEST_KEEP_INTENT_ENV=1`**：否则 `tests/conftest.py` 会在导入用例前把 `CHATBI_V2_INTENT_*` 强制为 `false`，你在命令行写的 `CHATBI_V2_INTENT_EVAL=true` 会被覆盖，`-m intent_eval` 仍会 **skip**（见 §2.1「`.env` 与卡死」）。 |
| 命令 | `CHATBI_PYTEST_KEEP_INTENT_ENV=1 CHATBI_V2_INTENT_EVAL=true CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_EVAL_OUT=tests/_out/intent_llm_$(date +%Y%m%d_%H%M%S).jsonl PYTHONPATH=. python -m pytest tests/test_intent_agent_accuracy.py -m intent_eval -v -s --tb=short` |
| Stub 替代 | `CHATBI_V2_INTENT_LLM=false` 的 **L1′** 见总规 §7.5.2 表 |
| 通过 | `n==60`；macro / 三桶 / `v1_fallback` 对照任务红线或既有归档 |

### 2.4 L2 — Intent 延迟基准

| 项 | 内容 |
|----|------|
| 命令（pytest） | `CHATBI_PYTEST_KEEP_INTENT_ENV=1 CHATBI_V2_INTENT_BENCH_RUN=true CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_BENCH_N=100 PYTHONPATH=. python -m pytest tests/benchmark_intent_latency.py -m intent_benchmark -v -s --tb=short` |
| 脚本入口 | `CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_BENCH_N=100 PYTHONPATH=. python tests/benchmark_intent_latency.py` |
| 说明 | 纸面 P50/P95 见 §7.2；真实延迟常与纸面有差距，归档时写明环境 |

### 2.5 L4 — SSE 实链（curl）

| 项 | 内容 |
|----|------|
| 目的 | 运行中 API 的 `chain` / SSE 与 `_contract_manifest.json`、Events spec 一致 |
| 前置 | `CHATBI_USE_AGENT=true`；本地 `uvicorn`；`API_BASE`、`ADMIN_TOKEN`（总规 §7.5.3） |
| 示例 | 总规 §7.5.3 中 **`curl … /api/py/unified/chat/stream`** 一行示例（`session_id` 可 null 测单轮） |
| 通过 | 无 **500**；流至 **`done`**；`type` 序列与契约最小键可人工对照 |
| 已有归档 | `docs/diary/2026-05-07-l4-sse-acceptance.md` · **`docs/diary/2026-05-10-l4-sse-acceptance-archive.md`**（本批 curl 原始 SSE 落 **`tests/_out/`**，见该 diary） |

### 2.6 L5 — Fallback / `error_code` 矩阵

| 项 | 内容 |
|----|------|
| 目的 | `FailureTypeHandler` 与 **§2.4 / §2.4.1** 一致；**RAG 空命中 → SQL** 必须满足 gating |
| 步骤 | 总规 **§7.5.4**：列矩阵表 → 单测 mock 或集成打流 → **归档到 `docs/diary/` 或任务单**（commit / 日期） |
| 代码锚点 | `api/agent.py`（`FailureTypeHandler`）· `api/tools.py`（`ToolResult` / `error_code`） |

### 2.7 L6 — 跨仓 + 多轮

| 项 | 内容 |
|----|------|
| UI 路径 | 总规 **§7.5.5**：`ai-ink-brain` + `PY_API_URL`；至少 2 类 query（概念 + 查数） |
| 后端多轮（可与 UI 解耦） | 总规 **§7.5.5.1**：固定 `SESSION_ID` 两轮 **curl**；间隔 ≥1s；负例不同 `session_id` |
| 通过 | 单轮：无 401/500，回答与 mode 合理；多轮：准则见总规 §7.5.5.1 勾选表 |

### 2.8 L7 — 运维与配置

| 项 | 内容 |
|----|------|
| 核对 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 与部署 env 逐项 |
| 强制 | 生产 **`CHATBI_V2_INTENT_EVAL=false`**；bench 开关勿误开 |
| DB | `rag_conversation_logs` 含 **`agent_steps` / `tool_results`**（`supabase/sql/create_rag_conversation_logs.sql`） |
| 烟测 | 生产 **L4 同款 curl** + 可选 CI 上对 tag 跑 **L0** |

### 2.9 本机执行勾选（Runner 回填；**不替代**总规 §7 勾选）

> 总规 **`SPEC-ChatBI-V2-Agent-Overview.md` §7** 仍以该文档与 CI 为准；本节仅便于本任务单追踪「§2.x 命令是否跑过」。

| § | 层级 | 状态 | 证据（日期 / 分支 / 摘要） |
|---|------|------|---------------------------|
| 2.1 | **L0** | **通过** | **2026-05-10** · `feat/chatbi-v2-agent` · `tech_graph_contract_check` **OK**；`pytest tests -q --tb=short` → **71 passed, 2 skipped**（约 5s；skip 含 benchmark 默认、`intent_eval` 默认关；**L5 canonical 已默认执行**）。 |
| 2.2 | **L3** | **通过** | **2026-05-10** · `feat/chatbi-v2-agent` · `CHATBI_USE_AGENT=true … test_unified_chat_backend_v2_agent.py` → **9 passed**（含 L5 canonical：`test_v2_rag_empty_gated_fallback`、`test_v2_natural_diary_query_rag_empty_fallback_to_direct`）。 |
| 2.3 | **L1** | **通过** | **2026-05-10** · `feat/chatbi-v2-agent` · `intent_eval` 真实 LLM · 产物 **`tests/_out/intent_llm_20260510_173118.{jsonl,csv}`** · **n=60** · 对照 **`docs/tasks/done/task_chatbi_v2_agent_p1_eval_benchmark_v1.md`** 冻结线：**macro-F1≈0.948**、**T2S 19/20**、**RAG 22/24**、**Direct 16/16**、**多轮 9/10**（**57/60**）；**备注**：3 条错判与 **Intent 超时→V1 降级** 同因，属外呼稳定性留档，非红线未过。 |
| 2.4 | **L2** | **通过** | **2026-05-10** · `feat/chatbi-v2-agent` · §2.4 同款命令 · `n=100` · **P50 0.0ms / P95 0.1ms / P99 6806.6ms / Avg 253.1ms / Max 7967.6ms** · pytest **~25.5s**（`benchmark_intent` 为 `random.choice` 混合缓存命中与偶发全链路外呼，分位数与总规 §7.2 纸面目标对照时注明「本机归档」）。 |
| 2.5 | **L4** | **通过** | **2026-05-10** · `feat/chatbi-v2-agent` · 总规 **§7.5.3** `curl` SSE · 原始流归档 **`tests/_out/sse_sample_l4.txt`**（单轮 `session_id:null`，`done.ok=true`）；**§7.5.5.1** 两轮同会话佐证 **`tests/_out/l6_turn1.txt`**、**`tests/_out/l6_turn2.txt`**（`meta`/`done` 中 `session_id` 一致，第二轮 `agent.debug.llm_prompts` 含首轮锚点）。细节见 **`docs/diary/2026-05-10-l4-sse-acceptance-archive.md`**。 |
| 2.6 | **L5** | **通过** | **2026-05-10** · `feat/chatbi-v2-agent` · **`pytest tests` → 71 passed, 2 skipped**；**`RAG_RETRIEVE_EMPTY` gating** 与 **`SQL_EXEC_TABLE_NOT_FOUND`→RAG** 已由 `tests/test_unified_chat_backend_v2_agent.py` 覆盖；**全量 `error_code` 矩阵表**见 **`docs/diary/2026-05-10-l5-failure-matrix-acceptance.md`**（表中「待补」为后续专项 mock，不否掉本轮结论）。 |
| 2.7 | **L6** | **通过** | **2026-05-10** · **`ai-ink-brain`** Unified + **`PY_API_URL`** · **同一 `session_id`** 三轮：`agent_info` **总行数 10** → **男性 3** → **其中固定佣金模式 2**；指代与查数链正常。**后端 curl 两轮**仍见 **`tests/_out/l6_turn*.txt`** 与 **`docs/diary/2026-05-10-l4-sse-acceptance-archive.md`**。UI 摘录见 **`docs/diary/2026-05-10-l6-multiturn-ui-acceptance.md`**。 |
| 2.8 | **L7** | **通过** | **2026-05-10** · **生产已正常**（前后端联调与真实流量下 Unified / 多轮查数可用）；运维核对见 **§2.8**（**`CHATBI_V2_INTENT_EVAL=false`**、评测/bench 勿误开、**`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`** 与部署 env 一致；**`rag_conversation_logs`** 迁移与烟测按总规 **§7.5.6**）。摘录 **`docs/diary/2026-05-10-l7-prod-acceptance.md`**。 |

---

## 3. 与总规 §7.1「未勾选」的对应关系（验收要关的缺口）

| 总规 §7.1 项 | 建议用哪几层验收关单 / 留证据 |
|--------------|--------------------------------|
| 多步推理（≥2 工具串行）+ 压测 | **L4/L5 集成** 或 可控环境下的 **固定 query E2E**；必要时补 `tests/` 与 diary 归档 |
| Fallback 与 §2.4 **逐条等价** | **L5** 矩阵全勾 + 归档 |
| 性能纸面目标 | **L2** + 诚实记录与 §7.2 差距（总规已写明未达标口径） |

---

## 4. 已有归档（可对照填写）

| 文档 | 内容 |
|------|------|
| `docs/diary/2026-05-07-l0-l3-regression-acceptance.md` | L0–L3 |
| `docs/diary/2026-05-07-l4-sse-acceptance.md` | L4（2026-05-07 首轮） |
| `docs/diary/2026-05-10-l4-sse-acceptance-archive.md` | L4（2026-05-10；SSE 落 `tests/_out/`） |
| `docs/diary/L5-ChatBI-V2-FailureTypeHandler-pytest指南.md` | L5 pytest 写法 |
| `docs/diary/2026-05-10-l5-failure-matrix-acceptance.md` | L5 `error_code` 矩阵归档（§7.5.4） |
| `docs/diary/2026-05-10-l6-multiturn-ui-acceptance.md` | L6 前端多轮（§7.5.5）摘录 |
| `docs/diary/2026-05-10-l7-prod-acceptance.md` | L7 生产 / 运维（§7.5.6）摘录 |
| `docs/tasks/done/task_chatbi_v2_docs_acceptance_archive_2026-05-11.md` | **V2** SPEC + 任务「验收 + 归档」总索引（**已迁入 done/**） |
| `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md` | **V3** 规划入口（简历评估 + Enterprise Gap） |

---

## 5. 你下一步建议

1. ~~在本机跑通 **§2.1 L0** + **§2.2 L3**~~（均已通过，见 **§2.9**）。  
2. ~~**L4** `curl` 与样本归档~~（**2026-05-10** 已回填 **§2.9**，diary 见 **`docs/diary/2026-05-10-l4-sse-acceptance-archive.md`**，SSE 文件在 **`tests/_out/`**）。  
3. ~~**L5** / **L6** 按层验收~~（L5 见 **§2.6**；L6 见 **§2.7** 与 **`2026-05-10-l6-multiturn-ui-acceptance.md`**）。  
4. ~~**L7** 运维 / 生产烟测~~（**2026-05-10** 已回填 **§2.9**，见 **`docs/diary/2026-05-10-l7-prod-acceptance.md`**）。  
5. 后续：总规 **`SPEC-ChatBI-V2-Agent-Overview.md` §7** 正文勾选、Gap 清单与 **V3** 排期（如 **`task_chatbi_v3_text2sql_tool_latency_obs_v1.md`**）。

---

## 给 Cursor 的稳定关键词

验收、L0、L3、L4、L5、L6、L7、§7.5、`task_chatbi_v2_acceptance_runner_v1`、`CHATBI_USE_AGENT`
