# Reinspect · gov-l2-manifest-ci · 2026-05-27

> **task_slug**: gov-l2-manifest-ci
> **freeze_id**: GOV-L2-MANIFEST-CI@2026-05-27
> **分支**: task/gov-l2-manifest-ci-v1
> **复检人**: Agent（独立重跑）
> **结论**: **建议合并 · 无阻塞项**

---

## §1 独立 VERIFY

### 1.1 测试 manifest 校验

| # | 检查项 | 命令 | 结果 |
|---|--------|------|------|
| 1 | 基础校验 | `python tools/tech_graph_test_manifest_check.py` | **pass** (12 entries) |
| 2 | pytest 新增 | `pytest tests/test_tech_graph_test_manifest_check.py -q` | **pass** (12 passed) |
| 3 | 全仓 pytest | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | **pass** (233 passed, 1 skipped) |

### 1.2 现有图谱 CI

| 命令 | 结果 |
|------|------|
| `python tools/tech_graph_manifest_check.py` | **pass** |
| `python tools/tech_graph_contract_check.py` | **pass** |
| `python tools/tech_graph_graph_export.py --check` | **pass** |

### 1.3 条目数

| 命令 | 结果 |
|------|------|
| `python -c "assert len(entries)>=12"` | **pass** (entries=12) |

### 1.4 范围纪律

| 检查项 | 结果 | 备注 |
|--------|------|------|
| 未改 api/ 业务逻辑 | pass | diff 无 api/ 路径修改 |
| 未改 tests/ 业务用例 | pass | diff 仅新增 `test_tech_graph_test_manifest_check.py` |
| 未改 prompts/ | pass | diff 无 prompts/ 路径 |
| 未手改 graph.json | pass | diff 无 graph.json |
| workflow diff 人确认 | pass | HG-CI-WORKFLOW approved |

---

## §2 抽样精读

### 2.1 `_test_manifest.json` 新增 6 条

| id | error_codes | test_paths | api/ 匹配 |
|----|-------------|------------|-----------|
| FP-PROMPT-GUARD-BLOCKED | RULE_IGNORE_PREV / RULE_FAKE_SYSTEM / ... | `tests/test_chatbi_prompt_guard_*.py` | ✅ chatbi_prompt_guard.py |
| FP-ADMIN-INGEST-INVALID-TYPE | Invalid ingest type | `tests/test_admin_ingest_route.py` | ✅ index.py |
| FP-CHAIN-CHAT-MISSING-FIELD | Missing required field: query | `tests/test_chain_chat_events.py` | ✅ chain_chat.py |
| FP-CLIENT-CLOSED-REQUEST | Client Closed Request | `tests/test_unified_chat_backend_v1.py` | ✅ index.py |
| FP-TOKEN-INVALID | Invalid token id / Invalid access_level in token row | `tests/test_chatbi_access_*.py` | ✅ chatbi_principal.py |
| FP-SUPABASE-RETRY-EXHAUSTED | Connection reset by peer | `tests/test_supabase_http_retry.py` | ✅ rag_env.py |

### 2.2 `tech_graph_test_manifest_check.py`

- JSON schema：version/freeze_id/entries 结构校验 ✅
- 必填字段：id / error_codes / test_paths ✅
- glob 匹配：fnmatch 对 `tests/**/*.py` 至少匹配一个 ✅
- 可选 --strict：error_codes 子串扫描 api/*.py ✅

### 2.3 `99_spec.md`

- 测试 manifest 表格新增「脚本」行 ✅
- VERIFY 命令块新增（基础校验 + 严格模式 + 条目数）✅

---

## §3 结论

**7/7 VERIFY pass · 建议合并。**

无返工项。下一棒：关账（git mv → done/ + _views + CLOSE invoke + hygiene H1–H5）。
