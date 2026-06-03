# Prompt · Portfolio W6 LoopTask 启动（RAG 五问预跑 · 00 → 止于 50）

> **用途**：**W2 合 main + W3 访客秘钥可用 + content 五卷 sync 后** 再开；**现在不要开**。  
> **Open Folder**：`ai-ink-brain-api-python`（联调时 `@` 前端 `ai-ink-brain`）  
> **真值**：[`RUNBOOK_portfolio_rag_five_questions_v1_zh.md`](../guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md) · [`SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md`](../../spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md)

---

## 1. 何时开（门禁）

| 门禁 | 必须满足 |
|------|----------|
| G1 | 前端 **W2** merged：`/resume` `/methodology` `/evidence` portfolio 200 |
| G2 | 前端 **W3** merged：visitor unlock + `PORTFOLIO_VISITOR_*` |
| G3 | `ai-ink-brain/content/methodology/` **含卷一～五**（非仅 vol3）；resume/evidence **非 stub** |
| G4 | `CONTENT_ROOT` 指向前端 `content/`；`POST /api/py/admin/sync` job **done** |
| G5 | 演示 URL（Vercel portfolio 模式）可访问 `/unified-chat` |

**未全绿 G1～G3 → 停工**，回前端 W2/W3 或 W5 补丁 sync。

---

## 2. LoopTask 帽链

```text
00 → 10 → 22(R1) ⇄ 10 → 30 → 40 → 22(R2) → Task·50 → STOP
```

| 帽 | 要点 |
|----|------|
| **10** | task 草案：sync 留证 + 五问 Q1～Q5 表 + sources 判定 + 录屏 checklist |
| **30** | 按 RUNBOOK §2–§4 执行 sync；生产/预发五问；留证默认 **`tmp/portfolio-rag-demo/`**（`PORTFOLIO_RAG_EVIDENCE_DIR`）；人签后脱敏复制至 `docs/diary/samples/portfolio-rag-demo/` |
| **40** | 5/5 能答 · sources ≥4/5 · 单问重试 ≤3 记录 |
| **50** | Task 子代理复检 RUNBOOK 可复现性 |

---

## 3. 可复制 Prompt 正文（G1～G5 全绿后 · 00 开帽）

```text
## 角色

你是 **Harness 00 总调度 + LoopTask 编排 Agent（Portfolio W6 · RAG 五问 E2E）**，严格遵循：
- docs/harness/prompts/00-orchestrator.md
- docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md（执行真值）
- docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md
- docs/planning/投递冲刺_20260609_v1_zh.md §2（Q1～Q5 原文 · Q3 仅 evidence）
- 配对前端 SPEC §6.3–§6.5 · W6

Open Folder = ai-ink-brain-api-python
（跨仓只读 ai-ink-brain/content/ · 前端 deploy URL）
git_branch = task/portfolio-rag-e2e-v1（从 main 拉）
task_slug = portfolio-rag-e2e-v1
freeze_id = PORTFOLIO-RAG-DEMO@2026-06-01
stop_after_hat = 50

## 硬规则

1. **入库路径仅** `POST /api/py/admin/sync`（RUNBOOK · 禁止 admin/ingest 备用）
2. **五问环境**：预发/生产等价 · 同 Supabase · 同 EMBEDDING_DIM · 同 CONTENT_ROOT 语义
3. **visitor token**：从前端 unlock 取得 · **不写** 明文进 Git
4. **全绿判定**：5/5 能答；sources ≥4/5 正确 category；单问重试 ≤3
5. **50 = Task 子代理** · STOP 不关账

## W6 交付物（30 帽）

| # | 产出 |
|---|------|
| 1 | sync job 日志摘要（jobId · filesScanned · done） |
| 2 | 五问逐条：提问 · 回答要点 · sources 路径 · 重试次数 |
| 3 | 本地 `$PORTFOLIO_RAG_EVIDENCE_DIR`（默认 `tmp/portfolio-rag-demo/`）留证；人签后脱敏复制至 `docs/diary/samples/portfolio-rag-demo/` |
| 4 | 录屏 checklist 勾选（3～5 min 路径见前端 SPEC §4.6.5） |

## 禁止

- 改 Next.js 页面（属前端 W2/W4）
- 新建向量 schema 大改
- 声称五问全绿但 sources 未核对

---

### 【当前棒：00 → 派 10】

扫描 RUNBOOK 与当前 content 目录差距 → 派 10 写/细化 `task_portfolio_rag_e2e_v1.md`（若尚未 active）

### 【帽 30 · 执行顺序】

1. 确认 CONTENT_ROOT 三目录 + 五卷 md 存在
2. RUNBOOK §2 POST sync → 轮询 done
3. RUNBOOK §3–§4 五问（Bearer visitor）
4. 失败：按 category / 维度 / CONTENT_ROOT 排查（RUNBOOK §5）

### 【STOP】

reinspect 落盘 → 待 HG-REINSPECT · 前端 W6 task 关账协调

## 给 Cursor

looptask、portfolio-rag-e2e、RUNBOOK、admin/sync、五问验收、PORTFOLIO-RAG-DEMO@2026-06-01
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-01 | v1：W6 后端联调 · **门禁 G1～G5** · 止于 50 |
