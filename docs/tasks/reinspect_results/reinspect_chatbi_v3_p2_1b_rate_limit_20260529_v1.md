# 50 复检报告：ChatBI V3 P2-1b 高消耗端点限流

## 元信息

| 项 | 值 |
|---|---|
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_rate_limit_v1.md` |
| git_branch | `task/chatbi-v3-p2-1b-rate-limit` |
| 复检基线 | `e7d9b0d`（40 自检）· 实现提交 `f803f87` |
| freeze_id | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| test_strategy | `required` |
| 复检日期 | 2026-05-29 |
| 复检模式 | 独立复检 |
| 22 审查 | `docs/harness/reviews/by-task/chatbi-v3-p2-1b-rate-limit/task_chatbi_v3_p2_resilience_rate_limit_v1_audit_R1_20260529.md`（R1 · 零阻塞） |
| 复检输入 | `git diff origin/main...HEAD` · task 自检结论 · 独立 pytest 重跑 |

---

## human_gate 审查

task 正文 **无** `human_gate` 表（22-R1 NB-5 已记录）；`git diff origin/main...HEAD -- task` 中 **无** `human_gate` / `approved` / `pending` 变更。**无需** 追溯 gate author；`post_close` 关账仍建议维护者人签终轮（与 P2-1a 惯例一致）。

---

## 独立重跑结果

```text
$ pytest tests/test_rate_limit_routes.py -v
4 passed in 72.70s

$ pytest tests -m "not intent_eval and not intent_benchmark" -q
253 passed, 1 skipped, 2 deselected in 157.89s
```

两条命令均 `exit_code=0`；与 task「### 自检结论（执行者）」记录一致。

---

## 验收表（50 独立复检）

| 验收项 | 结果 | 证据 | 备注 |
|---|---|---|---|
| 使用压测脚本（`hey` 或 pytest 并发桩）可稳定触发 429 | **pass** | `tests/test_rate_limit_routes.py::test_chat_route_returns_429_after_threshold` · `test_unified_stream_returns_429_after_threshold`：`MAX=2` 时第 3 次 POST `status_code==429` | 未跑 `hey`；pytest 桩满足 task「或」语义与 22 NB-1 |
| 429 响应体含 `error_code`，可选 `retry_after` 字段语义明确 | **pass** | `api/chatbi_rate_limit.py:157-165` `rate_limit_response_body` → `error_code=RATE_LIMIT_EXCEEDED`、`retry_after`（int ≥1）；`tests/test_rate_limit_routes.py:41-47` `_assert_rate_limit_body`；响应头 `Retry-After` 与 body 一致（`:182`） | 闭合 22 NB-6 |
| 阈值可通过 env 调整，调整后行为变化可复现 | **pass** | `load_rate_limit_config()`（`:96-111`）；`test_rate_limit_disabled_when_max_requests_zero`：`MAX=0` 时 4 次 POST 均非 429；专项测试默认 `MAX=2`/`WINDOW=60` | `PROJECT_CONFIG` 已文档化三 env（见下） |
| 至少覆盖 `/api/py/unified/chat/stream` 与 `/api/py/chat` 两条路径 | **pass** | `_PROTECTED_POST_PATHS`（`:19-24`）含两路径；`register_rate_limit_middleware` 在 `api/index.py:56` 注册；两条专项测试分别覆盖 | F3 双端点均覆盖 |

---

## failure_paths 一致性复核

| task 失败路径 | 复检结论 | 证据 |
|---|---|---|
| F1 流量超阈值 → 429 + 结构化错误码 | **一致** | middleware `:178-183` 返回 429 JSON；测试断言 `RATE_LIMIT_EXCEEDED` |
| F2 阈值 env 缺失或非法 → 回退默认并告警 | **一致** | `_parse_positive_int` / `_parse_positive_float`（`:48-93`）非法值 `logger.warning` 后回退默认；task 实现备忘与 PROJECT_CONFIG 已冻结「回退+告警」 | 闭合 22 NB-2 |
| F3 限流只覆盖一个端点导致绕过 | **未发生** | 两高消耗 POST 路径均在 `_PROTECTED_POST_PATHS`；`/api/py/live` 探针 `test_live_probe_not_rate_limited` 5 次 GET 均 200 | 符合非范围（不改 P2-1a 探针） |

---

## test_strategy: required 复核

| 检查项 | 结果 | 证据 |
|---|---|---|
| 专用 pytest 模块存在且可失败语义 | **pass** | `tests/test_rate_limit_routes.py`（4 tests）；与实现同 PR `f803f87` |
| 合并前必绿命令 | **pass** | 全量 `253 passed, 1 skipped, 2 deselected` |
| 测试与实现关系合理 | **pass** | 测试通过 `importlib.reload` + env monkeypatch 隔离；`_reload_index` 重置内存桶 |

---

## SPEC / 范围 / 非范围

| 项 | 结果 | 证据 |
|---|---|---|
| SPEC §2 粒度（IP 或 API Key） | **pass（MVP IP）** | `client_ip_from_request`（`:148-154`）`X-Forwarded-For` 首跳，否则 `request.client.host` | 闭合 22 NB-4；API Key 分桶为 follow-up |
| SPEC §2 429 结构化 body | **pass** | 见验收表第 2 行 |
| env 进 PROJECT_CONFIG、禁硬编码 | **pass** | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 新增 `CHATBI_RATE_LIMIT_*` 三行；默认值在 `chatbi_rate_limit.py` 为 `_DEFAULT_*` 常量，经 env 覆盖 |
| 非范围：不改 `/live` `/ready` | **pass** | 仅 POST + 白名单路径限流；live 探针测试通过 |
| 非范围：不实现熔断 | **pass** | diff 无 circuit breaker 代码 |

---

## 阻塞合并项

**无。**

---

## 非阻塞项（供关账 / 运维）

| ID | 说明 | 建议 |
|---|---|---|
| NB-50-1 | 未做 `hey` 真实压测 | 生产前可选冒烟；pytest 已覆盖 429 契约 |
| NB-50-2 | 内存桶不跨副本共享 | 多实例部署须运维知晓（task 自检「已知未测项」已记录） |
| NB-50-3 | `_manifest.json` 未新增 `CHATBI_RATE_LIMIT_*` env 条目 | 可选 follow-up 同步 manifest；不阻塞本 PR（PROJECT_CONFIG 已为真值表） |
| NB-50-4 | task 无 `human_gate` 表 | `post_close` 关账前建议维护者人签；非 50 阻塞 |

---

## 结论

**复检结果：通过（建议合并）**

高消耗双路径限流、429 结构化契约、env 可调与 F1–F3 失败路径均满足 task 与 `SPEC-ChatBI-V3-Resilience-Ops` §2；`test_strategy: required` 证据齐全；未发现阻塞性偏差。

---

## 给需求帽回填

- **无阻塞文档缺口**；`PROJECT_CONFIG` 与实现已对齐。  
- **可选**：task 归档至 `done/` 时新增 `### 复检结论（50 · 独立复检）` 链向本文件；`RECENT_TASK_SCHEDULE` 标记 P2-1b done。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-29 | v1：50 独立复检通过，验收表与 pytest 证据齐全 |
