# PROMPT · Kimi Code Agent 链 T1 实例 · RECENT 同步 + done/ 卫生（A+B）

> **Round**：T1  
> **task_slug**：`kimi_harness_pilot_recentsync_v1`  
> **task_path**：`docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md`  
> **git_branch**：`task/kimi-harness-pilot-recentsync-v1`  
> **slug**：`kimi-harness-recentsync`  
> **merge_policy**：`stop_before_merge`  
> **通用模板**：[`PROMPT_kimi_task_chain_serial_v1.md`](PROMPT_kimi_task_chain_serial_v1.md)

---

## 0. 开跑前门禁

| gate_id | 须 | 阻塞帽 |
| --- | --- | --- |
| `HG-TASK-DRAFT` | `approved` | 22-R1, 30 |
| `HG-KIMI-PILOT-EXEC` | `approved` | explore, 22, 30, 40, CLOSE |

任一为 `pending` → Lead **只报 gate_id + task 路径**，不 spawn Agent。

**开分支（Lead）**：

```bash
git checkout main && git pull
git checkout -b task/kimi-harness-pilot-recentsync-v1
```

---

## 1. §3 Lead 正文（Kimi 主会话 · 可复制）

```text
你 = Harness Lead（Kimi Code · 串行 Agent 链 · Round T1 · A+B 合并试点）。遵循：
- docs/harness/prompts/PROMPT_kimi_task_chain_serial_v1.md
- docs/harness/prompts/PROMPT_kimi_task_chain_serial_v1_T1_recentsync_zh.md（本文件 §2–§6）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

输入：
- task：docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
- slug：kimi-harness-recentsync
- git_branch：task/kimi-harness-pilot-recentsync-v1
- merge_policy：stop_before_merge

Round T1 帽链（串行，禁止并行 Agent）：
  explore → 22 → 30 → 40 → CLOSE → PR → CI（停于 merge 前）

纪律：
1. GATE_SCAN 通过后按 §2–§6：每帽 invoke 落盘 → Lead commit → Agent(§3全文) → 收 ≤10 行
2. 各帽 Agent prompt 必须使用本文件对应节 **全文**（含 canonical/forbidden）
3. 禁止 subagent 再 spawn · 禁止 subagent 任何 git 命令
4. test_strategy=not_applicable：40 不跑 pytest
5. CLOSE 后 gh pr create；CI Required 全绿后 stop_before_merge → 停，不 merge
6. 禁止代签 human_gate

完成后：HANDOFF_CLOSE_TRACE · 建议 diary docs/diary/2026-06-XX-kimi-harness-pilot-recentsync_zh.md
```

---

## 2. §3 explore 帽（Agent · 只读）

**invoke 建议名**：`invoke_YYYYMMDD_explore_kimi-harness-recentsync.md`  
**交付物**：`docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md`

```text
【角色】Harness explore · Kimi 试点 A+B · 只读差分；不改 RECENT/done 正文。

【canonical 读序 · 必须按序打开】
1. AGENTS.md §必读
2. docs/_tech_graph/00_main.md
3. docs/tasks/RECENT_TASK_SCHEDULE.md §1.2 全文
4. docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md §子批状态
5. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md §范围 A/B

【须核对】
- RECENT §1.2 vs MANIFEST：MANIFEST 路径是否仍写 active/；P1/P2/P3 状态是否过期
- 5 个 gov-docs-noise done task 文首 **状态** 行格式是否一致、是否含 PR 号
- 用 rg 扫描 docs/tasks/done/ 中 **状态** 行缺 PR 或缺日期的候选（列出路径，上限 15 条供 22/30 选用）

【forbidden】
docs/spec/v3-agent/** · api/** · tests/** · .github/**
docs/diary/** · docs/harness/invokes/by-task/**（除本交付物）
git log · git blame · 改任何业务文件

【你必须完成】
1. **A 段**：RECENT §1.2 现状 vs 期望（引用行号）
2. **B 段**：5 文件状态行对照表 + rg 候选清单（标注建议修/跳过）
3. 落盘 explore 报告（Summary / A / B / Blockers / 30 帽改动清单）
4. **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. §3 22 帽（Agent）

**invoke 建议名**：`invoke_YYYYMMDD_22_kimi-harness-recentsync.md`  
**交付物**：`docs/harness/reviews/by-task/kimi-harness-recentsync/task_governance_kimi_harness_pilot_recentsync_v1_audit_R1_YYYYMMDD.md`

```text
【角色】Harness 22 任务审核帽。遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/reviews/README.md

【canonical 读序】
1. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
2. docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md
3. docs/tasks/done/task_governance_docs_noise_line_manifest_v1.md

【forbidden】
docs/spec/v3-agent/** · api/** · docs/diary/** · 改 task 正文（除非审查要求且非阻塞）

【你必须完成】
1. HG-TASK-DRAFT 须 approved，否则拒开工
2. 对照 explore：A/B 范围是否清晰；B 是否限 10 文件
3. failure_paths F1–F4 + Scenario ID 是否满足 task_validate
4. 落盘 R1 审查 md（AUDIT_ROUND=R1 · 结论：是否建议 30 开工）
5. **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. §3 30 帽（Agent · 执行）

**invoke 建议名**：`invoke_YYYYMMDD_30_kimi-harness-recentsync.md`

```text
【角色】Harness 30 执行帽（纯 docs · Kimi 试点）。遵循 task §范围 A/B。

【canonical 读序】
1. docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
2. docs/harness/reviews/by-task/kimi-harness-recentsync/（R1 · 须无阻塞）
3. docs/harness/invokes/by-task/kimi-harness-recentsync/explore_RECENT_and_done_status_diff.md

【forbidden】
git log · git blame · docs/spec/v3-agent/** · api/** · tests/** · .github/**
删除 docs/harness/invokes/** 或 reviews/** 历史
修改超过 10 个 done/ 文件（含 B-2 五文件）

【你必须完成】
**A（必做）** 更新 docs/tasks/RECENT_TASK_SCHEDULE.md §1.2：
- MANIFEST → done/ 路径
- P0–P3 done + PR 号
- 执行器：P0 Cursor · P1–P3 CC · 治理线 CLOSE
- 删过期「脚手架/pending/active MANIFEST」表述

**B（必做 B-2 + 可选 B-3）**：
- 统一 5 个 gov-docs-noise done task 状态行格式
- 若 explore 有合格候选且总数≤10：补 PR/日期；否则跳过并在 task 自检注明

**其它**：
- 回填 task「### 自检结论（执行者）」草稿
- **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 5. §3 40 帽（Agent · 自检）

**invoke 建议名**：`invoke_YYYYMMDD_40_kimi-harness-recentsync.md`

```text
【角色】Harness 40 自检帽。

【canonical 读序】
docs/tasks/active/task_governance_kimi_harness_pilot_recentsync_v1.md
docs/tasks/RECENT_TASK_SCHEDULE.md §1.2

【验证命令】
rg -n 'active/task_governance_docs_noise_line_manifest' docs/tasks/RECENT_TASK_SCHEDULE.md  # 期望无命中
rg -n '脚手架|P2/P3.*pending' docs/tasks/RECENT_TASK_SCHEDULE.md  # 期望无命中（§1.2 段）
# 不跑 pytest（not_applicable）

【你必须完成】
1. 逐条勾选 task 验收标准
2. 更新 task「### 自检结论（执行者）」含命令输出要点
3. 无阻塞 → 建议 CLOSE + PR
4. **不要** commit（Lead 负责）

【回报格式 · 硬】
Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 6. §3 CLOSE 帽（Lead 主会话 · 非 Agent）

```text
【角色】Harness CLOSE · Round T1 · Kimi 试点

【Lead 必须完成】
1. 落盘 invoke_YYYYMMDD_CLOSE_kimi-harness-recentsync.md
2. Lead commit 全部本轮路径
3. git push -u origin task/kimi-harness-pilot-recentsync-v1
4. gh pr create --title "docs(governance): Kimi Harness pilot RECENT sync + done status hygiene" \
     --body 含 Summary / Test plan（docs-only · Kimi 执行器试点 · CI Required）
5. gh pr checks --watch；全绿后 stop_before_merge → 报告 PR URL，不 merge
6. HANDOFF_CLOSE_TRACE · 提醒人审 Kimi KPI 后决定是否 merge
```

---

## 7. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T1 A+B 合并实例 · Kimi spawn 全文内联 |
