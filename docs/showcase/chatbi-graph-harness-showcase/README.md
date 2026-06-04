# ChatBI Graph · Harness 展示系列

> **系列 ID**：`chatbi-graph-harness-showcase`  
> **路径**：`docs/showcase/chatbi-graph-harness-showcase/`  
> **性质**：L2 展示轨 — AI Coding + Harness 闭环 **人类可读叙事**；**不替代** L0 图谱 / L1 task 真值。

---

## 读者与用途

| 读者 | 建议读序 |
| --- | --- |
| 维护者 / 复盘 | `_meta/TIMELINE.md` → vol-03 → vol-01/02 |
| 面试 / 投递 | vol-90 → vol-03 → vol-01/02 证据索引 |
| Agent 续写 P1 | vol-04 + [`SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md`](../../spec/research/SPEC-Plan-LangChain-Patterns-Roadmap-v1_zh.md) §5 |

---

## 真值优先级

1. **L0**：`docs/_tech_graph/`、代码、`PROJECT_CONFIG`
2. **L1**：`docs/tasks/`、`docs/harness/reviews/`、`docs/tasks/reinspect_results/`
3. **本系列**：故事线、验收口语、复现命令 — 与 L1 矛盾时 **以 L1 为准**

机器索引：[`_meta/SERIES_MANIFEST.yaml`](_meta/SERIES_MANIFEST.yaml)

---

## 卷册一览

| 卷 | 目录 | status | 对应交付 |
| --- | --- | --- | --- |
| 01 | [`vol-01-baseline-merge-gate/`](vol-01-baseline-merge-gate/README.md) | `done` | PR [#106](https://github.com/Cyning12/ai-ink-brain-api-python/pull/106) |
| 02 | [`vol-02-p0-foundation/`](vol-02-p0-foundation/README.md) | `done` | PR [#107](https://github.com/Cyning12/ai-ink-brain-api-python/pull/107) |
| 03 | [`vol-03-cross-cutting/`](vol-03-cross-cutting/README.md) | `done` | Harness / CI / Agent 横切 |
| 04 | [`vol-04-p1/`](vol-04-p1/README.md) | `compiled` · **规划** | Task-B 意图卡 · 未开工 |
| 05 | [`vol-05-roadmap-horizon/`](vol-05-roadmap-horizon/README.md) | `stub` | P2/P3 远景 |
| 90 | [`vol-90-portfolio/`](vol-90-portfolio/README.md) | `compiled` · **v0.10** | 投递 / 面试短稿 |

---

## 架构三层（全系列共用）

见 [`_meta/ARCHITECTURE_LAYERS.md`](_meta/ARCHITECTURE_LAYERS.md)：**运行面 · 代码面 · 治理面**。

---

## 扩展规则

- P1 关账后：vol-04 `status` → `done`，增补 `07-evidence-index.md`；可选增 vol-06-p2-planned。
- 新增卷须在 `_meta/SERIES_MANIFEST.yaml` 登记 `slug`、`status`、`source_prs`。
- 单卷正文 **禁止** 复制整份 `_manifest.json` / task 全文；用 **指针 + 摘要**。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | 系列骨架与卷册大纲落盘 |
| 2026-06-04 | vol-01/02 正文 compiled · vol-90 短稿 v0.10 · `_meta/TIMELINE` 同步 |
| 2026-06-04 | vol-03 横切正文 compiled（01–05） |
| 2026-06-04 | vol-04 P1 规划 narrative compiled（01–05 · planning_only） |
