# 50 复检报告：ChatBI V3 P2-1a 健康探针契约（/live + /ready）

## 元信息

| 项 | 值 |
|---|---|
| task | `docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` |
| git_branch | `task/chatbi-v3-p2-1a-health` |
| 复检基线 | `4dae83c`（实现提交） + `d06fe8b`（50 invoke 快照） |
| 复检日期 | 2026-05-25 |
| 复检输入 | task 验收标准、`api/index.py` 端点实现、`tests/test_health_probe_routes.py`、pytest 重跑证据 |

---

## 独立重跑结果

```text
$ pytest tests/test_health_probe_routes.py
2 passed

$ pytest tests -m "not intent_eval and not intent_benchmark"
210 passed, 1 skipped, 2 deselected
```

两条命令均 `exit_code=0`，与 task 自检记录一致。

---

## 验收表（50 独立复检）

| 验收项 | 结果 | 证据 | 备注 |
|---|---|---|---|
| `/api/py/live` 返回 200 且 `ok=true` | **pass** | `tests/test_health_probe_routes.py::test_live_returns_200_and_ok_true`；`api/index.py` 的 `live()` 直接返回 `_build_live_payload()` | `live` 未做外部依赖调用，符合轻量探活契约 |
| 依赖故障注入下 `/api/py/ready` 返回 503 且含 `components[]` | **pass** | `tests/test_health_probe_routes.py::test_ready_returns_503_with_components_when_supabase_missing` 断言 `status_code=503`、`ok=false`、`components` 列表且含 `supabase failed` | 与任务 F1 失败路径一致 |
| 文档与实现一致（端点字段说明） | **pass** | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §F 已列出 `/live` `/ready` 契约；`api/index.py` 返回字段 `ok/service/probe/components` 与文档一致 | `GET /api/py/health` 兼容语义也已注明 |
| pytest 覆盖 happy path + dependency-down path | **pass** | 上述专项测试 2/2 通过；全量门禁命令通过 | 满足 `test_strategy: required` |

---

## 失败路径一致性复核

| task 失败路径 | 复检结论 | 证据 |
|---|---|---|
| F1 依赖未就绪时 `/ready` 503 + `components` failed | **一致** | `ready()` 以 `all(status=="ok")` 判定就绪，失败走 `503`；测试已覆盖 Supabase 缺失分支 |
| F2 文档/实现不一致应阻塞 | **当前未发现不一致** | 端点与字段在 `PROJECT_CONFIG` 与实现中对齐 |
| F3 `/live` 不能引入重依赖外呼 | **满足** | `live()` 只返回常量 payload，不访问 DB/外部服务 |

---

## 阻塞合并项

无。

---

## 结论

**复检结果：通过（建议合并）**  
`/api/py/live` 与 `/api/py/ready` 契约、状态码、失败路径和测试证据均满足 task 验收标准；未发现阻塞性偏差。

---

## 回填 task（关账必做）

| 回填项 | 目标路径 | 动作 |
|---|---|---|
| 50 复检结论 | `docs/tasks/active/task_chatbi_v3_p2_resilience_health_ready_v1.md` | 新增 `### 复检结论（50 · 独立复检）`：结论 **pass**、复检报告相对路径、基线 commit `4dae83c` |
| 复检报告索引 | 同上 task 或 `docs/tasks/_views/done.md`（归档时） | 链向本文件 `reinspect_chatbi_v3_p2_1a_health_ready_20260525_v1.md` |
| 头部状态 | 同上 task | **PR 合并且人签关账后** 改为 `done（YYYY-MM-DD 验收通过）`，并 `git mv` → `docs/tasks/done/`（与 `docs/tasks/README.md` 归档流程一致） |
| 人工闸（若启用） | task 元信息 `human_gate` 表（可选补表） | `HG-REINSPECT`：**仅人** `pending`→`approved` 后再归档；本 task 未单独列闸时，沿用母单 `post_close` 关账人签惯例 |

**实现备忘（供 task 回填）**

| 项 | 内容 |
|---|---|
| 涉及文件 | `api/index.py`；`tests/test_health_probe_routes.py`；`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`；`docs/_tech_graph/_manifest.json` |
| 复检报告 | `docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_1a_health_ready_20260525_v1.md` |
| Harness invoke | `invoke_20260525_{30,40,50}_chatbi-v3-p2-1a-health.md` |
| 合并前必绿 | `pytest tests -m "not intent_eval and not intent_benchmark"`（本复检：`210 passed, 1 skipped, 2 deselected`） |

---

## 关账后验收清单（人 / 运维）

1. **PR**：`task/chatbi-v3-p2-1a-health` → `main`，CI **`pytest`** job 绿（与本地同 marker）。  
2. **可选冒烟**（本地已起 `uvicorn` 时）：  
   - `curl -sS http://127.0.0.1:8000/api/py/live` → `200`，body 含 `"ok":true`  
   - 临时去掉 `NEXT_PUBLIC_SUPABASE_URL` 后 `curl -i -sS http://127.0.0.1:8000/api/py/ready` → `503`，body 含 `"components"`  
3. **归档 task**：验收项已勾选 + 50 结论已回填 → `git mv` 至 `docs/tasks/done/`，更新 `docs/tasks/_views/done.md`。  
4. **下一实现棒**：按母单顺序启动 **P2-1b**（`task_chatbi_v3_p2_resilience_rate_limit_v1.md`），本单 **禁止** 夹带限流/熔断。

---

## 给需求帽回填

- **无阻塞文档缺口**；`PROJECT_CONFIG` §F 与实现已对齐。  
- **可选（非关账阻塞）**：运维/ diary 补一条 curl 故障注入示例（临时移除 `SUPABASE_URL` 验证 `503 + components`），便于非 pytest 环境快速复核。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-25 | v1：50 独立复检通过，验收表与 pytest 证据齐全 |
| 2026-05-25 | v1.1：补「回填 task」「关账后验收清单」闭环 |
