# Task：治理 — L2 `_test_manifest` Phase B（扩面 + CI 校验）

> **状态**：done（2026-05-27 · GOV-L2-MANIFEST-CI@2026-05-27）  
> **前置**：Wiki Loop T4+L2 **实例 4** R3 · [`task_governance_l2_r3_test_manifest_v1.md`](../done/task_governance_l2_r3_test_manifest_v1.md)  
> **SPEC**：[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md) §4.3 **Phase B**  
> **SKILL**：[`SKILL-docs-governance.md`](../skills/SKILL-docs-governance.md) · [`SKILL-harness-task.md`](../skills/SKILL-harness-task.md)（**单 task**，非 Loop）

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6/§8。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `recommended` |
| **test_strategy_note** | 新增 `tools/tech_graph_test_manifest_check.py` + 轻量 pytest；合并前仍须全仓 pytest 绿。 |
| **freeze_id** | `GOV-L2-MANIFEST-CI@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-l2-manifest-ci-v1` |
| **task_slug** | `gov-l2-manifest-ci` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22, 30 | manifest 扩面条目 + CI 接入方案人扫 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 落盘后人签 |
| HG-CI-WORKFLOW | approved | 30 | 若将 check 升为 **Required**，人确认 workflow diff |

---

## 帽子顺序

| 序 | 帽 | 启动 |
|----|-----|------|
| 0（可选） | **10** | 需求帽 · task 已冻结可跳过 |
| 1–5 | **22→50→关账** | [`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · invoke · [`PROMPT_START_full_chain_v1.md`](../../harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_START_full_chain_v1.md) |

---

## 背景与目标

Loop R3 已落盘 **`_test_manifest.json` v1 草案**（6 entries · Phase A · **不**阻塞 merge）。本 task 落实 L2 SPEC **Phase B**：

1. manifest **扩面**至 **≥12** 条真实 failure path 映射；  
2. 实现 **`tools/tech_graph_test_manifest_check.py`**；  
3. 接入 **`tech-graph.yml`**（与 `manifest_check` 同 job 增 step，或独立 job — **首版建议同 job Required**）；  
4. 更新 `99_spec.md` 脚本表与 VERIFY 命令。

**完成态**：

- CI 跑 manifest check 脚本 **exit 0**；本地 pytest 新增用例绿。  
- `_test_manifest.json` 条目可解析、glob 可展开、与现有 ERR 语义一致。

---

## 范围

- [x] 扩展 [`docs/_tech_graph/_test_manifest.json`](../../_tech_graph/_test_manifest.json)：**≥12 entries**（在现有 6 条上增量；`id` 稳定、带 Epic 前缀）。  
- [x] 新增 `tools/tech_graph_test_manifest_check.py`（L2 SPEC §4.3 Phase B 行为）：  
  - JSON schema / 必填字段；  
  - 每条 `test_paths`：`fnmatch` 在仓库根至少匹配一个 `tests/**/*.py`；  
  - （v1 最小）抽样校验 `error_codes` 在 `api/` 有字符串出现（可配置 `--strict`）。  
- [x] 新增 `tests/test_tech_graph_test_manifest_check.py`（≥3 cases：合法 manifest、坏 glob、缺字段）。  
- [x] [`.github/workflows/tech-graph.yml`](../../.github/workflows/tech-graph.yml)：`manifest_check` job 增 step 跑新脚本。  
- [x] [`docs/_tech_graph/99_spec.md`](../../_tech_graph/99_spec.md) 测试 manifest 小节补脚本与 VERIFY。  
- [x] [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §6.6 增 **L2 Phase B** 行 + §8 修订。  
- [x] 22/30/40/50 + reinspect + 关账 hygiene H1–H5。

## 非范围

- Phase C（task `failure_paths` 双向校验 · 高成本）。  
- 改 `tests/` **业务用例**源码（仅允许新增 manifest check 测试文件）。  
- 改 `api/` 业务逻辑。  
- Wiki `graph_nodes` 扩面（→ [`task_governance_wiki_t4_expand_v2.md`](task_governance_wiki_t4_expand_v2.md)）。  
- Harness prompts 正文。

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| L2 SPEC Phase B | `docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.3 |
| 现有 manifest | `docs/_tech_graph/_test_manifest.json` |
| 参照脚本 | `tools/tech_graph_manifest_check.py` |
| CI 真值 | `.github/workflows/tech-graph.yml` |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | `test_paths` glob 无匹配文件 | 脚本 **exit 1** · CI fail | 修 glob 或补测试文件 |
| F2 | manifest JSON 非法 | 脚本 **exit 1** | 修 JSON |
| F3 | `HG-CI-WORKFLOW` pending 却改 workflow | 30 拒开工 | 人批 |
| F4 | 新脚本未测即合入 | 50 **fail** | 补 pytest |
| F5 | 用 Wiki 替代 manifest 真值 | 违反 SPEC §4.2 · 50 fail | revert |

---

## 验收标准

- [x] `python tools/tech_graph_test_manifest_check.py` → **exit 0**  
- [x] `pytest tests/test_tech_graph_test_manifest_check.py -q` → 全绿  
- [x] `pytest tests -m "not intent_eval and not intent_benchmark"` → 全绿  
- [x] `python tools/tech_graph_manifest_check.py` · `contract_check` · `graph_export --check` → 绿  
- [x] `_test_manifest.json`：`len(entries) >= 12`  
- [x] GitHub Actions `manifest_check` job 含新 step 且 PR 上 **pass**（PR #70）  
- [x] 关账：`done/` + `_views` + reinspect + RECENT §8

**VERIFY（40 帽 · 合并前必跑）**：

```bash
python tools/tech_graph_test_manifest_check.py
pytest tests/test_tech_graph_test_manifest_check.py -q
pytest tests -m "not intent_eval and not intent_benchmark" -q
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m['entries'])>=12"
```

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/_test_manifest.json`、`tools/tech_graph_test_manifest_check.py`、`tests/test_tech_graph_test_manifest_check.py`、`.github/workflows/tech-graph.yml`、`docs/_tech_graph/99_spec.md`、`docs/tasks/RECENT_TASK_SCHEDULE.md` |
| 新增 env | 无 |
| CI 变更 | `tech-graph.yml` manifest_check job 增 step「Tech Graph test manifest check」 |
| 图谱变更点 | `99_spec.md` 测试 manifest 小节补脚本与 VERIFY；**不**手改 `graph.json` |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `python tools/tech_graph_test_manifest_check.py` · `pytest tests/test_tech_graph_test_manifest_check.py -q` · `pytest tests -m "not intent_eval and not intent_benchmark" -q` · `python tools/tech_graph_manifest_check.py` · `python tools/tech_graph_contract_check.py` · `python tools/tech_graph_graph_export.py --check` · `python -c "assert len(entries)>=12"` |
| 结论 | **pass** |
| 要点 | 7/7 VERIFY 全绿；233 passed 1 skipped；test_manifest 12 entries；严格模式仅 2 个已有 Phase A 条目的 error_code 不在 api/ 中（符合 SPEC 预期） |

---

## 给 Cursor

`gov-l2-manifest-ci`、L2 Phase B、`_test_manifest.json`、`tech_graph_test_manifest_check`、单 task、workflow
