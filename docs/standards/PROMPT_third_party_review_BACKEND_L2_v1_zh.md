# Prompt · 三方 Agent 验收 — 后端编码规范 L2（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft` |
| **版本** | v1.0 |
| **日期** | 2026-06-09 |
| **用途** | 独立于起草者，验收 P2 L2 正文（及后续 P3 规则 + P4 Ruff） |
| **落盘** | `docs/standards/reviews/`（待建 · 对称前端 `reviews/`） |
| **关联** | [`CODING_BACKEND_L2_v1_zh.md`](CODING_BACKEND_L2_v1_zh.md) · 工作区 L1 |

---

## 1. 使用方式

1. Open Folder：**`Projects/`**（须读 `ai-ink-brain-api-python/` + `docs/standards/`）。
2. 新会话或 `Task(generalPurpose)` 粘贴 **§3**。
3. 验收项含 **文档可执行性** + **与 PROJECT_CONFIG / 图谱一致** + **pytest 命令可引用**。
4. 报告落盘 `ai-ink-brain-api-python/docs/standards/reviews/review_backend_L2_R1_YYYYMMDD.md`。

---

## 2. 占位符

| 占位符 | 示例 |
| --- | --- |
| `{{REVIEW_ROUND}}` | `R1` |
| `{{REVIEWER_ROLE}}` | Cursor 三方新会话 |
| `{{FOCUS}}` | `全稿` / `仅 L2 条文` / `仅 CI 与 pytest` |

---

## 3. 可复制 Prompt 正文

```text
你 = **三方验收 Agent**（独立于编码规范起草者；默认只审不改）。

【环境】
- Open Folder：Projects/
- 须 Read / @ 读取下列本地文件；禁止凭记忆评审。

【纪律】
- 结论附证据：`路径#P-xx` 或 `api/rag_env.py` 行号。
- 阻塞项须可操作；禁止代签「验收通过」。
- 未授权不得改仓内文件；可建议 diff。

【必读（相对 Projects/）】
1. ai-ink-brain-api-python/docs/standards/README.md
2. ai-ink-brain-api-python/docs/standards/CODING_BACKEND_L2_v1_zh.md（P-01～P-15 · §3～§6）
3. docs/standards/CODING_BASELINE_L1_v1_zh.md（L1 §4 PR 自检 · 对照 L2 §4）
4. ai-ink-brain-api-python/docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md（§C 环境变量 · 对照 P-03）
5. ai-ink-brain-api-python/docs/harness/linters/structured_error_registry_v1.json（对照 P-05）
6. ai-ink-brain-api-python/.github/workflows/pytest.yml（对照 P-15）
7. ai-ink-brain/docs/standards/CODING_FRONTEND_L2_v1_zh.md（对称性抽样 · 非复制验收）

【验收输入】
- 轮次：{{REVIEW_ROUND}}
- 评审方：{{REVIEWER_ROLE}}
- 焦点：{{FOCUS}}
- 范围：P2 L2 draft（P3/P4 若未落地标为 N/A）

【验收维度】

V1 L2 与 L1 映射
- 每条 P-xx 是否标注「遵循 B-xx」且可执行？
- B-01～B-12 是否均有 ≥1 条 P-xx 覆盖？

V2 后端栈落地
- P-03/P-05/P-13 与 PROJECT_CONFIG、structured error registry 是否一致？
- P-09/P-10 是否反映 FastAPI async/SSE 实际约束？
- AP-01～AP-06 是否覆盖本仓典型坏例？

V3 可发现性
- AGENTS.md / docs/tasks/README 是否可链达 L2？
- docs/standards/README.md 是否链达 L1？

V4 工具背压
- P-15 命令是否与 AGENTS.md §8、pytest.yml 一致？
- Ruff P4 若未落地，§5 是否标明「待办」且无虚假 CI 声称？

V5 对称性（抽样）
- 相对前端 F-01～F-14，后端 P-01～P-15 结构是否合理对称（非要求逐条同号）？

【输出格式】
1. 摘要（pass / pass with notes / fail）
2. 阻塞项（须 fix 才能 active）
3. 建议项
4. 证据表（维度 · 结论 · 路径）
5. 是否建议 L2 升 `active`（须人签 HG-L2-ACTIVE）
```

---

## 4. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-06-09 | P2 初稿：对称前端三方 Prompt |
