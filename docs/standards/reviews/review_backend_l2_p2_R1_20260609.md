# 三方验收 — Ink 后端 L2/P2（R1）

| 项 | 内容 |
| --- | --- |
| **状态** | 建议签收 → **L2 active**（2026-06-09 · 人签 HG-L2-ACTIVE） |
| **评审方** | Cursor 三方新会话 |
| **焦点** | 全稿 + P3 + P4（L2 draft + 可发现性 + CI 背压 + 对称性） |
| **被审稿** | `CODING_BACKEND_L2_v1_zh.md` v1.0 · `README.md` v1 |
| **Open Folder** | Projects/ |

---

## 1. 阅读确认

| 路径 | 已读 | 摘要 |
| --- | --- | --- |
| `ai-ink-brain-api-python/docs/standards/README.md` | ✅ | 后端L2索引；链L1真值、前端对称L2、P3/P4标注 |
| `ai-ink-brain-api-python/docs/standards/CODING_BACKEND_L2_v1_zh.md` | ✅ | P-01~P-15 + AP-01~AP-06 + PR自检6项 + REF/工具映射 |
| `docs/standards/CODING_BASELINE_L1_v1_zh.md` | ✅ | L1 active v1.1；B-01~B-12；§4 PR自检6项（含B-11） |
| `ai-ink-brain-api-python/docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | ✅ | §C环境变量真值（rag_env.py统一读取）；§F契约；§E目录地图 |
| `ai-ink-brain-api-python/docs/harness/linters/structured_error_registry_v1.json` | ✅ | 必填键`ok`/`error_code`/`message`；cases: rate_limit_429, circuit_breaker_open |
| `ai-ink-brain-api-python/.github/workflows/pytest.yml` | ✅ | `pytest` workflow；`pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short`；dummy env对齐PROJECT_CONFIG |
| `ai-ink-brain/docs/standards/CODING_FRONTEND_L2_v1_zh.md` | ✅（前次评审已读） | F-01~F-14；用于V5对称性抽样 |
| `ai-ink-brain-api-python/AGENTS.md`（系统加载） | ✅ | 必读第7条链`docs/standards/README.md`；合并前必绿命令；规则索引 |

---

## 2. 维度评分（pass / pass-with-notes / fail）

| 维度 | 结论 | 证据与说明 |
| --- | --- | --- |
| **V1 L2 与 L1 映射** | pass | P-01~P-15 全部标注 `遵循 B-xx`。B-01~B-12 每条均有 ≥1 条 P-xx 覆盖：B-01(P-01,P-09)、B-02(P-02,P-10)、B-03(P-03)、B-04(P-04)、B-05(P-05)、B-06(P-06)、B-07(P-07)、B-08(P-08)、B-09(P-11)、B-10(P-12,P-15)、B-11(P-13)、B-12(P-14)。无遗漏。 |
| **V2 后端栈落地** | pass-with-notes | P-03 "所有env读取经`rag_env.py`"与`PROJECT_CONFIG` §C全表一致（`pick_supabase_url()`/`must_siliconflow_api_key()`/`admin_secret()`等）。P-05 "须满足structured_error_registry必填键"与`structured_error_registry_v1.json`第5行`["ok","error_code","message"]`一致；cases覆盖rate_limit/circuit_breaker与`PROJECT_CONFIG` §C对应env变量对齐。P-13安全项与`PROJECT_CONFIG` §G安全红线一致。P-09/P-10 FastAPI async/SSE约束与`PROJECT_CONFIG` §F契约（StreamingResponse/SSE/`CHATBI_SSE_EMIT_QUEUE_MAX`）一致。AP-01~AP-06覆盖后端典型坏例（os.getenv散落、index.py上帝函数、裸except、字符串判型、硬编码URL、裸500字符串）。 |
| **V3 可发现性** | pass-with-notes | `AGENTS.md` 必读第7条明确链至`docs/standards/README.md`（"编码规范L2 · P-xx · 遵循 B-xx"）。`docs/standards/README.md` 链L1真值、前端对称L2、`PROJECT_CONFIG`。L2 §6标注P3 `.cursor/rules/07-coding-standards-l2.mdc`为"待办"，诚实。**Note**：当前后端尚无`.cursor/rules/07-coding-standards-l2.mdc`文件，与前端P3已落地存在差距，但不影响L2本身签收。 |
| **V4 工具背压** | pass | P-15命令`pytest tests -m "not intent_eval and not intent_benchmark"`与`pytest.yml`第46行完全一致。`bash scripts/verify-tech-graph.sh`/`python tools/tech_graph_contract_check.py`与`AGENTS.md` "合并前必绿"一致。P-08/Ruff P4明确标注"（待P4）""当前CI以pytest为主""**未**入CI"，无虚假声称。 |
| **V5 对称性（抽样）** | pass-with-notes | 后端P-01~P-15与前端F-01~F-14结构高度对称：模块边界/早返回/env/命名/错误/策略/diff/类型/栈边界/异步纪律/重复/测试/安全/可观测/CI各有一对。后端多P-14独立日志（前端合并于F-05），因后端有更复杂的`rag_conversation_logs`/`CHATBI_JSON_LOG`体系，独立成条合理。反模式后端6条vs前端5条，多AP-06"裸字符串500"，属后端HTTP特有场景，合理。 |
| **V6 缺口** | pass-with-notes | 历史债（`CHAT_API_SECRET`/`NEXT_PUBLIC_ADMIN_SECRET`已废弃）、纯文档task、多子仓差异均有覆盖。P-03明确"新代码不得新增散落读取"，对历史代码渐进收敛。 |

---

## 3. 阻塞项（须 fix 才能 active）

| ID | 位置 | 问题 | 修改建议 |
| --- | --- | --- | --- |
| （无） | — | — | — |

---

## 4. 非阻塞建议

| ID | 位置 | 建议 |
| --- | --- | --- |
| **S-01** | `CODING_BACKEND_L2_v1_zh.md` §4 | `code_quality_bar: strict` 在 L2 §4 中被引用，但 Harness V2 PLAN §5 无此字段定义（与前/后端 R1 S-01/S-03 为同一引用悬空）。**建议**：同步消解——要么 Harness §5.9 落盘该字段，要么从 L2 §4 中移除/替换。 |
| **S-02** | `CODING_BACKEND_L2_v1_zh.md` P-08 | P-08 对 Python `Any` 用"**避免** 无说明的 `Any`"，力度弱于 L1 B-08 "**禁止** 无注解的万能 dict 穿越层"。**建议**：统一措辞为"禁止新增无说明的`Any`；边界保留须`# noqa`附理由"，与L1力度对齐。 |
| **S-03** | `CODING_BACKEND_L2_v1_zh.md` P-14 | `rag_conversation_logs` 要求引用了 `.cursor/rules/30-rag-implementation.mdc`，但该规则文件未在必读列表中。**建议**：在L2 §6或P-14中增加".cursor/rules/30-rag-implementation.mdc 见`AGENTS.md`规则索引"的可发现性指引。 |
| **S-04** | `CODING_BACKEND_L2_v1_zh.md` P-03 | P-03 禁止新代码依赖 `CHAT_API_SECRET` / `NEXT_PUBLIC_ADMIN_SECRET`，但 `pytest.yml` 第27行仍设 `NEXT_PUBLIC_ADMIN_SECRET` dummy值。**建议**：在P-03或P-13中增加一行注释说明"CI dummy值用于兼容旧代码回退路径，新代码不得新增读取"。 |
| **S-05** | `CODING_BACKEND_L2_v1_zh.md` §5 工具表 | Ruff状态为"（待P4）""**未**入CI"。**建议**：P4 task中明确Ruff规则集（`E,F,I,UP,B,ANN`子集）与升严时间表，保持与OUTLINE §1.4 P1路线一致。 |

---

## 5. 证据表

| 维度 | 结论 | 路径/行号 |
| --- | --- | --- |
| P-03 env经rag_env.py | pass | `PROJECT_CONFIG` §C 全表；`rag_env.py:pick_supabase_url()` 等 |
| P-05 structured error registry | pass | `structured_error_registry_v1.json` L5: `["ok","error_code","message"]` |
| P-05 rate_limit/circuit_breaker cases | pass | `structured_error_registry_v1.json` L8-L17; `PROJECT_CONFIG` §C `CHATBI_RATE_LIMIT_*` / `CHATBI_CIRCUIT_BREAKER_*` |
| P-08 no-explicit-any | N/A(P4待办) | `ruff.toml` 未入CI；L2 §5标注"（待P4）" |
| P-12/P-15 pytest命令 | pass | `pytest.yml` L46; `AGENTS.md` "合并前必绿" |
| P-09 FastAPI路由/SSE | pass | `PROJECT_CONFIG` §F: StreamingResponse / SSE / `_contract_manifest.json` |
| P-10 SSE背压 | pass | `PROJECT_CONFIG` §C: `CHATBI_SSE_EMIT_QUEUE_MAX` 默认512, clamp 8~8192 |
| P-13 prompt guard | pass | `PROJECT_CONFIG` §C: `CHATBI_PROMPT_GUARD_MODE` 默认`off` |
| P-01 路由软上限80行 | pass-with-notes | P-01已说明"因须串联鉴权、解析、调用子模块与响应组装" |
| L1→P-xx全覆盖 | pass | B-01~B-12 每条均有≥1 P-xx |

---

## 6. 签收建议

- [x] **建议 L2 升 `active`**（须人签 **HG-L2-ACTIVE**）
- [ ] **须修订后再审**（列阻塞 ID）
- [ ] **阻塞**（说明原因）

**评审结论**：本稿 **无阻塞项**。P-01~P-15 与 B-01~B-12 映射完整无遗漏；P-03/P-05/P-13 与 `PROJECT_CONFIG`、`structured_error_registry` 一致；P-09/P-10 反映 FastAPI async/SSE 实际约束；AP-01~AP-06 覆盖后端典型坏例；P-15 CI 与 `pytest.yml`/`AGENTS.md` 一致；Ruff P4 诚实标注"待办"；前后端结构对称且差异有合理解释。

建议在消化 S-01（`code_quality_bar` 引用悬空，与前端 R1 联动）后，由人签 **HG-L2-ACTIVE** 升 `active`。

**评审方签字**：Cursor 三方新会话 · 2026-06-09
