---
title: "技术修复摘要"
slug: vol-01-04-technical
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "04"
status: compiled
---

# 04 · 技术修复（非新功能）

> **Delta 口径**：相对 `origin/main` **修复漂移** · **非** 新 L1 SPEC。  
> 实现 commit：`eed212e` · merge：`26e1c45`（PR #106）

---

## 1. 变更一览

| 文件 | 变更 | 解决的验收项 |
| --- | --- | --- |
| `tests/conftest.py` | 固定 `INTENT_MIN_CONFIDENCE=0.6` | 10× v3 clarify/plan 测 |
| `api/agent.py` | `CHATBI_V3_LOW_CONFIDENCE_CLARIFY` 合法值 + `"on"` | 与 PROJECT_CONFIG / 部署习惯一致 |
| `docs/_tech_graph/_contract_manifest.json` | `frontend_ts_ignore_payload_like_keys` + `"label"` | `tech_graph_contract_check` |
| `docs/_tech_graph/02_version.md` | 时间线追加 | 图谱维护轨 |

**未修改**：`api/unified_chat.py` · `api/graph/*` · P0 专测。

---

## 2. conftest：测试环境真值

### 问题

- 规格默认 **`INTENT_MIN_CONFIDENCE=0.6`**
- 开发者 `.env` 常见 **`0.3`**
- v3 stub 意图 **confidence=0.35** → 低于 0.6 才走 clarify；0.3 阈值下 **永不触发** → 10 测 fail

### 修复

```python
# tests/conftest.py（节选）
os.environ["INTENT_MIN_CONFIDENCE"] = "0.6"
```

**先于** dotenv 加载生效（task §9 实现备忘）。CI 无 `.env` 时行为不变；本地与 CI **对齐**。

### 与「red-green」的关系

- 10 测 **pre-exist on main**（required 口径：**对齐既有失败可复现测试**）
- 本 PR **未**删测、**未**放宽断言

---

## 3. agent：clarify 开关 `on`

```python
# api/agent.py — clarify_gate 合法值增补 "on"
clarify_gate = os.getenv("CHATBI_V3_LOW_CONFIDENCE_CLARIFY", "").strip().lower() in (
    "1", "true", "yes", "on",
)
```

与 `PROJECT_CONFIG` 及运维文档中 `on` 写法一致；不改变默认关 clarify 的 CI 配置（`pytest.yml` 仍可关）。

---

## 4. contract：`label`（Runbook 路径 A）

- **ADDED**（Delta）：前端 SSE 消费者可读 UI 辅助字段 `label`
- **实现**：写入 `_contract_manifest.json` → `frontend_ts_ignore_payload_like_keys`
- **Scenario ID**：`baseline-contract-label-declared` · `fp-baseline-contract-label-drift`

```bash
python tools/tech_graph_contract_check.py
# OK: cross-repo contract check passed
```

Runbook：[`RUNBOOK_graph_contract_ci_red_v1.md`](../../../harness/guides/RUNBOOK_graph_contract_ci_red_v1.md) §2 路径 A。

---

## 5. Delta 与实现一致性（50 判定 pass）

| Delta | 实现 | 50 |
| --- | --- | --- |
| MODIFIED v3 plan/clarify 语义 | conftest + agent 环境对齐；**非** unified_chat 新 emit | pass · §9 根因留痕 |
| ADDED contract label | manifest L37 | pass |

叙事诚实点：Delta 写「恢复 SSE/JSON 事件语义」，实际为 **环境/配置真值** 对齐；task **`## 9. 实现备忘`** 已说明，避免面试过度承诺「大改 Agent 编排」。

---

## 6. 本地验证（与 40/50 同命令）

```bash
pytest tests/test_unified_chat_backend_v2_agent.py -k "v3 and (plan or low_confidence)" -q
# 10 passed

pytest tests -m "not intent_eval and not intent_benchmark" -q
# 277 passed, 1 skipped

python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py
```

---

## 指针

- task §9：`docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md`
- 50 变更表：[`reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md`](../../../tasks/reinspect_results/reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md)
