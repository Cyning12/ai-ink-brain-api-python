# Explore Report · RECENT §1.2 vs done/ 状态卫生差分

> **帽**: explore · **Agent**: Kimi Code · **日期**: 2026-06-08
> **Task**: `task_governance_kimi_harness_pilot_recentsync_v1` · A+B 合并范围
> **冻结**: 只读差分；不改 RECENT/done 正文

---

## Summary

本次 explore 完成 RECENT_TASK_SCHEDULE.md §1.2 与 MANIFEST / 5 个 gov-docs-noise done task 的对照，并扫描 `docs/tasks/done/` 文首状态行缺 PR/日期候选。

**核心发现**：
1. RECENT §1.2 **仍写过期状态**（MANIFEST 链 `active/`、P1「脚手架」、P2/P3 pending），与 done/ 真值不一致
2. 5 个 gov-docs-noise done task 状态行 **格式不统一**（3 种变体），仅 P0 含完整 `日期 · PR #xxx @ commit`
3. `done/` 扫描发现 **11 个文件** 文首状态行缺 PR 或缺日期（含 5 个 legacy 消化文件 + 6 个早期 tech_graph/task）

**建议**：30 帽须修 RECENT §1.2（A-1~A-5）；B-2 优先统一 5 个 gov-docs-noise 文件格式；B-3 可选回填 0~5 个额外候选。

---

## A 段 · RECENT §1.2 现状 vs 期望

### A-1 · MANIFEST 路径仍写 `active/`

| 行号 | 现状文本 | 问题 |
|------|----------|------|
| L147 | `> **MANIFEST**：[`task_governance_docs_noise_line_manifest_v1.md`](active/task_governance_docs_noise_line_manifest_v1.md)` | **路径错误**：MANIFEST 已于 2026-06-06 关账并 `git mv` → `done/`；RECENT 仍链至 `active/` |

**期望**: `done/task_governance_docs_noise_line_manifest_v1.md`

### A-2 · P0–P3 子批表状态过期

| 行号 | 现状文本 | 问题 |
|------|----------|------|
| L153 | `P0` · `**done** · #121` | ✅ 正确 |
| L154 | `P1` · `**脚手架** · 分支已开` | **状态过期**：P1 已于 2026-06-06 done（PR #123） |
| L155 | `P2/P3` · `未建` / `pending` | **状态过期**：P2（PR #126）、P3（PR #129）均已于 2026-06-06 done |

**期望**: P1/P2/P3 均标 `**done**` + PR 号，删除「脚手架 / 分支已开 / pending」表述。

### A-3 · 执行器行未注明治理线 CLOSE

| 行号 | 现状文本 | 问题 |
|------|----------|------|
| L148 | `**执行器**：P0 **Cursor Task 链**（done）· P1+ **Claude Code spawn 链**` | 未反映 P1–P3 已完成；未注明治理线 CLOSE |

**期望**: 补充「P0 Cursor · P1–P3 Claude Code · 治理线 **CLOSE**（2026-06-06）」。

### A-4 · 分支行过期

| 行号 | 现状文本 | 问题 |
|------|----------|------|
| L149 | `**分支**：task/gov-docs-noise-p1-v1` | 分支名仅对应 P1；治理线已 CLOSE，此条可删或改为历史记录 |

### A-5 · 缺少 docs-noise CLOSE 标注

RECENT §1.2 段首（L145-L149）无「docs-noise 治理线已 CLOSE」声明，与 MANIFEST 文首状态 `done（2026-06-06 · 治理线 CLOSE · P0–P3 全量 done）` 不一致。

**期望**: §1.2 标题或段首加 `> **状态**：docs-noise 治理线 **CLOSE**（2026-06-06）`。

---

## B 段 · 5 文件状态行对照表 + rg 候选清单

### B-1 · 5 个 gov-docs-noise done task 状态行格式对照

| # | 文件路径 | 当前状态行 | 格式评估 | 建议 |
|---|----------|-----------|----------|------|
| 1 | `done/task_gov_docs_noise_p0_readme_v1.md` | `> **状态**：done（2026-06-06 验收通过 · PR #121 @ 5184c10）` | ✅ **最优**（日期 + PR + commit） | 作为统一基准 |
| 2 | `done/task_gov_docs_noise_p1_archived_v1.md` | `> **状态**：done（2026-06-06 验收通过 · PR #123 @ 2de2902）` | ✅ 完整 | 与 P0 一致 |
| 3 | `done/task_gov_docs_noise_p2_readorder_v1.md` | `> **状态**：done（T2c 执行完成 · 40 自检全绿 · PR #126 merged @ 08d51bd）` | ⚠️ 格式偏长；含执行细节 | **建议修**：简化为 `done（2026-06-06 · PR #126 @ 08d51bd）` |
| 4 | `done/task_gov_docs_noise_p3_index_v1.md` | `> **状态**：done（T2d 执行完成 · 40 自检全绿 · PR #129 merged @ 1c52f27）` | ⚠️ 同上 | **建议修**：简化为 `done（2026-06-06 · PR #129 @ 1c52f27）` |
| 5 | `done/task_governance_docs_noise_line_manifest_v1.md` | `> **状态**：done（2026-06-06 · 治理线 CLOSE · P0–P3 全量 done）` | ⚠️ **缺 PR 号**（母单无独立 PR，但可注明 T3 关账方式） | **建议修**：补充 `· T3 母单关账` 或保持现状（母单性质特殊） |

**格式一致性结论**：5 文件存在 **3 种格式变体**：
- 变体 A（P0/P1）：`done（YYYY-MM-DD 验收通过 · PR #N @ commit）`
- 变体 B（P2/P3）：`done（T2x 执行完成 · 40 自检全绿 · PR #N merged @ commit）`
- 变体 C（MANIFEST）：`done（YYYY-MM-DD · 治理线 CLOSE · P0–P3 全量 done）`

**B-2 建议**：统一为 `done（YYYY-MM-DD · PR #N @ commit）`；MANIFEST 可保留 `· 治理线 CLOSE` 注释但须补日期。

### B-2 · rg 扫描候选清单（缺 PR 或缺日期）

扫描命令：`rg -n '^> \*\*状态\*\*' docs/tasks/done/` 后过滤掉含 PR/日期/active 的条目。

| # | 文件路径 | 当前状态行 | 缺什么 | 建议修/跳过 | 理由 |
|---|----------|-----------|--------|-------------|------|
| 1 | `done/task_03_hybrid_search_implementation.md` | `> **状态**：done` | 缺日期、缺 PR | **建议修** | P2-4 legacy 消化文件，应补 `done（2026-06-06 · PR #126）` |
| 2 | `done/Task 04.md` | `> **状态**：done` | 缺日期、缺 PR | **建议修** | 同上 |
| 3 | `done/task_rag_b1_metadata_structured_recall_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **建议修** | 同上 |
| 4 | `done/task_rag_b2_fts_alias_backfill_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **建议修** | 同上 |
| 5 | `done/task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` | `> **状态**：done` | 缺日期、缺 PR | **建议修** | 同上 |
| 6 | `done/task_rag_keyword_websearch_date_normalize_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **建议修** | 同上 |
| 7 | `done/task_tech_graph_p0_handoff_and_drift_check_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **跳过** | 早期 task（2026-04），历史遗留，非 gov-docs-noise 线 |
| 8 | `done/task_tech_graph_p1_manifest_and_validation_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **跳过** | 同上 |
| 9 | `done/task_tech_graph_p2_layered_views_and_failure_paths_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **跳过** | 同上 |
| 10 | `done/task_tech_graph_p6_cross_repo_contract_guardrail_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **跳过** | 同上 |
| 11 | `done/task_harness_wiki_loop_t4_l2_v1.md` | `> **状态**：done` | 缺日期、缺 PR | **跳过** | 同上；且含 freeze_id 可间接定位 |

**候选总数**: 11 个（含 5 个 legacy 消化 + 6 个早期 task）

**B-3 配额建议**：
- 若执行 B-2（5 个 gov-docs-noise 文件）+ 6 个 legacy 文件 = 11 个，**超出 B-3「最多再修 5 个」上限**
- 建议：B-2 必做 5 个；legacy 6 个中选 0~5 个（优先前 5 个），其余在 40 自检说明「历史早期 task，非本批次范围」

---

## Blockers

| # | Blocker | 严重度 | 说明 |
|---|---------|--------|------|
| B1 | P2/P3 状态行含执行细节（T2c/T2d/40 自检） | 低 | 非错误，但格式不统一；30 帽可简化 |
| B2 | MANIFEST 母单无独立 PR | 低 | 母单性质特殊，T3 关账未走独立 PR；可注明 `T3 母单关账` |
| B3 | legacy 6 文件缺元信息 | 中 | P2-4 消化时仅补 `状态: done`，未补日期/PR；需判定是否在本 task 回填 |

**无硬阻塞**：所有差异均为格式/元信息级别，不影响业务真值。

---

## 30 帽改动清单（供 22/30 选用）

### A 段改动（RECENT §1.2）

| ID | 文件 | 行号 | 改动 | 优先级 |
|----|------|------|------|--------|
| A-1 | `docs/tasks/RECENT_TASK_SCHEDULE.md` | L147 | MANIFEST 链 `active/` → `done/` | P0 |
| A-2 | 同上 | L154 | P1 状态 `脚手架` → `done · PR #123` | P0 |
| A-3 | 同上 | L155 | P2/P3 状态 `pending/未建` → `done · PR #126/#129` | P0 |
| A-4 | 同上 | L148 | 执行器行补充 `· 治理线 CLOSE` | P1 |
| A-5 | 同上 | L149 | 分支行改为历史记录或删除 | P2 |
| A-6 | 同上 | L145 | §1.2 段首加 `> docs-noise 治理线 CLOSE（2026-06-06）` | P1 |

### B 段改动（done/ 状态行）

| ID | 文件 | 当前状态行 | 目标状态行 | 优先级 |
|----|------|-----------|-----------|--------|
| B-1 | `done/task_gov_docs_noise_p2_readorder_v1.md` | `done（T2c 执行完成 · 40 自检全绿 · PR #126 merged @ 08d51bd）` | `done（2026-06-06 · PR #126 @ 08d51bd）` | P1 |
| B-2 | `done/task_gov_docs_noise_p3_index_v1.md` | `done（T2d 执行完成 · 40 自检全绿 · PR #129 merged @ 1c52f27）` | `done（2026-06-06 · PR #129 @ 1c52f27）` | P1 |
| B-3 | `done/task_governance_docs_noise_line_manifest_v1.md` | `done（2026-06-06 · 治理线 CLOSE · P0–P3 全量 done）` | `done（2026-06-06 · 治理线 CLOSE · T3 母单关账）` | P2 |
| B-4 | `done/task_03_hybrid_search_implementation.md` | `done` | `done（2026-06-06 · PR #126）` | P2 |
| B-5 | `done/Task 04.md` | `done` | `done（2026-06-06 · PR #126）` | P2 |
| B-6 | `done/task_rag_b1_metadata_structured_recall_v1.md` | `done` | `done（2026-06-06 · PR #126）` | P2 |
| B-7 | `done/task_rag_b2_fts_alias_backfill_v1.md` | `done` | `done（2026-06-06 · PR #126）` | P2 |
| B-8 | `done/task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md` | `done` | `done（2026-06-06 · PR #126）` | P2 |
| B-9 | `done/task_rag_keyword_websearch_date_normalize_v1.md` | `done` | `done（2026-06-06 · PR #126）` | P2 |

**合计**: A 段 6 处 + B 段 9 处 = 15 处改动点；若 B-4~B-9 仅选 5 个，则总计 11 处。

---

## 附录 · rg 扫描原始输出

### 含 PR/日期的 done 状态行（已过滤，作为格式基准）

```
done/task_05_query_rewrite_observability.md:3:> **状态**：done（2026-05-22 验收通过 · [PR #46]...）
done/task_governance_l2_phase_c_impl_v1.md:3:> **状态**：done（2026-05-28 · 单元 B 关账 · PR-B #80 · CI #81）
done/task_gov_docs_noise_p0_readme_v1.md:3:> **状态**：done（2026-06-06 验收通过 · PR #121 @ 5184c10）
done/task_gov_docs_noise_p1_archived_v1.md:3:> **状态**：done（2026-06-06 验收通过 · PR #123 @ 2de2902）
done/task_gov_docs_noise_p2_readorder_v1.md:3:> **状态**：done（T2c 执行完成 · 40 自检全绿 · PR #126 merged @ 08d51bd）
done/task_gov_docs_noise_p3_index_v1.md:3:> **状态**：done（T2d 执行完成 · 40 自检全绿 · PR #129 merged @ 1c52f27）
done/task_governance_docs_noise_line_manifest_v1.md:3:> **状态**：done（2026-06-06 · 治理线 CLOSE · P0–P3 全量 done）
```

### 缺 PR/日期的候选（完整 11 条）

```
done/task_03_hybrid_search_implementation.md:1:> **状态**：done
done/Task 04.md:1:> **状态**：done
done/task_rag_b1_metadata_structured_recall_v1.md:1:> **状态**：done
done/task_rag_b2_fts_alias_backfill_v1.md:1:> **状态**：done
done/task_rag_b2_v2_fts_alias_symbols_versions_identifiers.md:1:> **状态**：done
done/task_rag_keyword_websearch_date_normalize_v1.md:1:> **状态**：done
done/task_tech_graph_p0_handoff_and_drift_check_v1.md:3:> **状态**：done
done/task_tech_graph_p1_manifest_and_validation_v1.md:3:> **状态**：done
done/task_tech_graph_p2_layered_views_and_failure_paths_v1.md:3:> **状态**：done
done/task_tech_graph_p6_cross_repo_contract_guardrail_v1.md:3:> **状态**：done
done/task_harness_wiki_loop_t4_l2_v1.md:3:> **状态**：done
```

---

*报告结束 · explore 帽完成 · 建议进入 22 审核帽*
