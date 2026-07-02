# 书面审查 · Ops Session S4 Verify API · 20-task-audit R1

## 元信息

| 字段 | 值 |
| --- | --- |
| **帽** | `20-task-audit` |
| **task_slug** | `ops-session-s4-verify-api` |
| **task_path** | [`docs/tasks/active/task_ops_session_s4_verify_api_v1.md`](../../../../tasks/active/task_ops_session_s4_verify_api_v1.md) |
| **freeze_id** | `OPS-SESSION-ORCH-SPEC-V1` |
| **审查轮** | `R1` |
| **日期** | `2026-07-02` |
| **acceptance_verdict** | **conditional_pass** |
| **HG-AUDIT-R1 建议** | **recommend approved** |

---

## 对照 SPEC · BLOCKERS

| 检查项 | 来源 | 判定 |
| --- | --- | --- |
| subprocess CLI · 禁止 Runtime import probe | §10.4.2 · §11.2 · B7 | **pass**（task D1 · 非范围明确） |
| promote 前 `verify --ci` 阻塞 | §5.3 step 7 · §10.5.1 | **pass**（D2 · 失败路径 `VERIFY_FAILED`） |
| 00 半自动 · maintainer 显式确认 | B4 · §5.3 | **pass**（`confirm: true` · 无 auto-commit） |
| `POST .../promote` 契约 | §9.2 | **pass**（`target_repo` / `target_branch`） |
| `session.promoted` 事件 | §9.4 | **pass**（范围已列） |
| `HG-PROMOTE` / `HG-EXEC-AUTH` 同步 | §6.1 | **pass**（范围已列 · 30 须对齐 gate_sync） |
| Vercel 不同步全量 verify | §10.4.4 · D5 | **pass** |
| test_strategy `required` | §12.4 | **pass** |
| S3 前置 / blocked_by | §12.1 | **pass**（S3 done · HG-S3-LOCAL-ACCEPTANCE） |
| graph_delta / B6 | B6 | **pass**（非范围 · S5+） |

---

## 契约与配对

| 端点（草案） | 与 UI task 对齐 | 判定 |
| --- | --- | --- |
| `GET .../promote/preview` | UI BFF 同路径 | **pass**（建议 30 冻结 JSON 形状后 ui 开工） |
| `POST .../promote` | UI 二次确认后 POST | **pass** |
| 错误码 `PROBE_UNAVAILABLE` / `VERIFY_FAILED` / `PROMOTE_CONFLICT` | UI D3 inline 展示 | **pass** |

---

## 阻塞项

**无。**

---

## 非阻塞（30 消化）

| # | 建议 |
| --- | --- |
| N1 | probe v0.10.1 `--repo-root` 未就绪时：`verify_task` 用 `HARNESS_PROBE_REPO_ROOT` 指向 **提升后的业务仓根** · 过渡路径 task 已写 · 30 实现须单测 mock |
| N2 | `target_repo` 路径映射写死表：`api-python` → `docs/tasks/active/` · `Ink` → `content/tasks/active/` · 建议 `promote.py` 集中常量 |
| N3 | auth 后 `task validate` warn-only：与 S2 可选探针一致 · **勿**阻塞 dispatch · 日志/事件即可 |
| N4 | preview 与 promote 共用 `run_id` 写 `verify_report.json` · 避免覆盖 dispatched 深析 deliverables 目录混淆 |
| N5 | 本地须 `harness-probe` 在 PATH（或 `HARNESS_PROBE_BIN`）· checklist §0 增一项 |

---

## 风险

| 级别 | 说明 |
| --- | --- |
| Medium | harness-probe 工作区为 worktree 碎片 · 维护者需 `pip install -e` 或 PATH 指向可用 v0.10+ |
| Low | 合并批次 PR 含 S2–S4 · 30 勿提前 push main |

---

## 30 开工

**conditional_pass · 零 fail · recommend HG-AUDIT-R1 approved**

**Open Folder**：`ai-ink-brain-api-python/` · 分支 `task/ops-session-s4-verify-api`（自 S3 分支切出或延续）
