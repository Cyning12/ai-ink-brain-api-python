# Wiki-CTX-AB Representative — Scorecard

| 项 | 值 |
| --- | --- |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **phase** | Representative · H-lean vs W × **6 slug** |
| **model** | `composer` |
| **date** | 2026-05-27 |

---

## 逐 slug 记录（30 帽）

### `harness-p1-docs-consolidation`

| 题 | 臂 | payload_chars | pass | 备注 |
|----|-----|---------------|------|------|
| Q1 | H-lean | 11466 | **pass** | P1-3 `human_gate` 速查 + P1-2 `docs/tasks/skills/README.md` |
| Q1 | W | 4042 | **pass** | synthesis 两项范围一致 |
| Q2 | H-lean | — | **pass** | `not_applicable` + 纯文档理由 |
| Q2 | W | — | **pass** | synthesis 摘要含 `not_applicable` |
| Q3 | H-lean | — | **pass** | `HARNESS-P1-DOCS@2026-05-23` · 关账 2026-05-23 |
| Q3 | W | — | **pass** | frontmatter 一致 |
| Q4 | H-lean | — | **pass** | P1-1 工作区 reviews **非**本 Epic |
| Q4 | W | — | **pass** | 非范围 pointer |

### `tech-graph-gate-d-v2-tasks`

| 题 | 臂 | payload_chars | pass | 备注 |
|----|-----|---------------|------|------|
| Q1 | H-lean | 20306 | **pass** | v2 五题 + T004/T005 |
| Q1 | W | 4602 | **pass** | synthesis 摘要一致 |
| Q2 | H-lean | — | **pass** | `CTX_V2_QUERY` / 禁止手改 graph.json |
| Q2 | W | — | **pass** | synthesis 架构决议 |
| Q3 | H-lean | — | **pass** | `TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0` |
| Q3 | W | — | **pass** | frontmatter freeze_id |
| Q4 | H-lean | — | **pass** | **禁止**手改 `graph.json` |
| Q4 | W | — | **pass** | 非范围 / 须 export |

### `chatbi-v3-p2-health-ready`

| 题 | 臂 | payload_chars | pass | 备注 |
|----|-----|---------------|------|------|
| Q1 | H-lean | 10457 | **pass** | `/live` · `/ready` 分层探针 |
| Q1 | W | 4053 | **pass** | synthesis 摘要 |
| Q2 | H-lean | — | **pass** | `required` + 可失败单测 |
| Q2 | W | — | **pass** | frontmatter `test_strategy: required` |
| Q3 | H-lean | — | **pass** | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` |
| Q3 | W | — | **pass** | frontmatter |
| Q4 | H-lean | — | **pass** | 前端 UI **非**范围 |
| Q4 | W | — | **pass** | 非范围 · BFF 另项 |

### `governance-l2-manifest-ci`

| 题 | 臂 | payload_chars | pass | 备注 |
|----|-----|---------------|------|------|
| Q1 | H-lean | 10901 | **pass** | manifest ≥12 + `tech_graph_test_manifest_check` + CI |
| Q1 | W | 4271 | **pass** | synthesis 摘要 |
| Q2 | H-lean | — | **pass** | `recommended` |
| Q2 | W | — | **pass** | frontmatter + §测试变更 |
| Q3 | H-lean | — | **pass** | `GOV-L2-MANIFEST-CI@2026-05-27` |
| Q3 | W | — | **pass** | frontmatter |
| Q4 | H-lean | — | **pass** | Wiki **不能**替代 `_test_manifest` CI |
| Q4 | W | — | **pass** | Phase B 机器门禁 vs Wiki 叙事分工 |

### `wiki-ctx-ab-v1`

| 题 | 臂 | payload_chars | pass | 备注 |
|----|-----|---------------|------|------|
| Q1 | H-lean | 14798 | **pass** | P1/P2 实验 + scorecard + conclusion |
| Q1 | W | 3902 | **pass** | synthesis 摘要 |
| Q2 | H-lean | — | **pass** | `not_applicable` |
| Q2 | W | — | **pass** | 实验填表 · 不改 api |
| Q3 | H-lean | — | **pass** | `WIKI-CTX-AB@2026-05-25` |
| Q3 | W | — | **pass** | frontmatter |
| Q4 | H-lean | — | **pass** | P2 **不可**外推 ChatBI 实现 |
| Q4 | W | — | **pass** | 局限节 · 单 slug 外推 |

### `harness-wiki-loop-t4-l2`

| 题 | 臂 | payload_chars | pass | 备注 |
|----|-----|---------------|------|------|
| Q1 | H-lean | 11977 | **pass** | T4 桥接 + L2 manifest 三子 round |
| Q1 | W | 4136 | **pass** | synthesis 子 round 表 |
| Q2 | H-lean | — | **pass** | `not_applicable`（母单编排） |
| Q2 | W | — | **fail** | synthesis **无** `test_strategy` 枚举（母单字段未蒸馏） |
| Q3 | H-lean | — | **pass** | `WIKI-LOOP-T4-L2@2026-05-27` |
| Q3 | W | — | **pass** | frontmatter |
| Q4 | H-lean | — | **pass** | 子 round **不可**跳过 invoke 落盘 |
| Q4 | W | — | **pass** | Loop 纪律 · HANDOFF |

---

## 聚合（SPEC §3）

| slug | H-lean chars | W chars | 降幅 % | 正确性 H-lean | 正确性 W |
| --- | --- | --- | --- | --- | --- |
| harness-p1-docs-consolidation | 11466 | 4042 | **64.7%** | 4/4 | 4/4 |
| tech-graph-gate-d-v2-tasks | 20306 | 4602 | **77.3%** | 4/4 | 4/4 |
| chatbi-v3-p2-health-ready | 10457 | 4053 | **61.2%** | 4/4 | 4/4 |
| governance-l2-manifest-ci | 10901 | 4271 | **60.8%** | 4/4 | 4/4 |
| wiki-ctx-ab-v1 | 14798 | 3902 | **73.6%** | 4/4 | 4/4 |
| harness-wiki-loop-t4-l2 | 11977 | 4136 | **65.4%** | 4/4 | 3/4 |

| 指标 | 结果 |
| --- | --- |
| **T7**（≥5/6 slug 降幅≥30%） | **pass**（**6/6**） |
| **T8**（≥5/6 slug ≥3/4） | **pass**（**6/6**；1 slug W 臂 3/4 为 ingest 缺口） |
| **T6** 无幻觉 | **pass**（48/48 无载荷外路径/freeze 编造） |
| **T-AGG** | **accepted（部分外推）** |

**物化**：`python tools/wiki_ctx_ab_materialize_w.py` · `python tools/wiki_ctx_ab_materialize_h_lean.py`（`--out-dir` 本实验 `payloads/` · `freeze_id` `WIKI-CTX-AB-REP@2026-05-27`）。
