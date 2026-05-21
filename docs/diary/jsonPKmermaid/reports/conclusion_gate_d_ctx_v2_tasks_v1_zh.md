# 闸口 D 结论：v2 五题扩域（graph_query 轨 · draft）

> **状态**：`draft`（PR-1 已落地；PR-3 LLM batch **阻塞** `SILICONFLOW_API_KEY` · FP-GD7）  
> **freeze_id**：`TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0`  
> **graph_v2_freeze_id**：`TECH_GRAPH_S2_FREEZE_20260519_V2_3`  
> **回归基线（只读）**：[`runs/gate_ctx_c_v1_batch_20260518_102810`](../runs/gate_ctx_c_v1_batch_20260518_102810/)  
> **本批主 run**：待 `SILICONFLOW_API_KEY` 后新建 `runs/gate_ctx_c_v1_batch_<YYYYMMDD>_<HHMMSS>/`（**禁止**覆盖 `052803` / `083014` / `102810`）

---

## 0. PR-1 / PR-2 工程摘要（已验收）

| 项 | 内容 |
| --- | --- |
| **题集** | `fixtures/gate_ctx_ab_v2/tasks.json` · 五题 · v1 三题 gold 与 ab_v1 **一致** |
| **物化** | `materialize_gate_c_payloads.py` · T001～T003 继承 C″ 分支；T004/T005 增量 manifest/impact |
| **PR-2** | D 五题中位数 **658** ≤ **701**（步骤：T004/T005 depth=1；省略 T004/T005 contract_slice） |
| **pytest** | `204 passed` · `pytest tests -m "not intent_eval and not intent_benchmark"` |

---

## 1. 表 1 · v1 回归（D 臂 vs `102810`）

> **待 PR-3 batch + score_gold_f1** 后填 F1 列。

| task | C″ D impact | C″ D entry | 本批 D impact | 本批 D entry | Δimpact |
| --- | ---: | ---: | ---: | ---: | ---: |
| T001 | 0.200 | 0.857 | — | — | — |
| T002 | 0.800 | 0.923 | — | — | — |
| T003 | 0.857 | 0.923 | — | — | — |

---

## 2. 表 2 · v2 扩展（D 臂）

> **待 PR-3**；表 2 脚注：「无题专属物化」基线 = 关闭 T004/T005 专属 `manifest_slice`/`impact_surface` 的一次 ablation（执行帽记录目录）。

| task | 本批 D impact | 本批 D entry | 备注 |
| --- | ---: | ---: | --- |
| T004 | — | — | 待 batch |
| T005 | — | — | 待 batch |

---

## 3. 表 3 · D vs E（token / F1）

> 待本批主 run 与 `gold_f1.md`。

---

## 4. 复现命令

```bash
python tools/tech_graph_graph_export.py --check
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/materialize_gate_c_payloads.py
pytest tests/test_gate_ctx_c_v1_materialize.py tests/test_gate_ctx_ab_v2_tasks.py
# PR-3（须 SILICONFLOW_API_KEY + RUBRIC_REVIEW_BACKEND=siliconflow）
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/scripts/run_gate_c_batch.py
python docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py \
  --run-dir docs/diary/jsonPKmermaid/runs/gate_ctx_c_v1_batch_<YYYYMMDD>_<HHMMSS>
pytest tests -m "not intent_eval and not intent_benchmark"
```

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-05-21 | 30 帽 PR-1/PR-2 落盘；PR-3 draft 占位（API Key 阻塞） |
