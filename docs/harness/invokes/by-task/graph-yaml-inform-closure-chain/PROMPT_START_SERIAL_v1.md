# 启动 Prompt · 串行执行 · graph-yaml-inform-closure-chain（P0 → P1）

> **用法**：Open Folder **`ai-ink-brain-api-python/`** → **新对话** → 复制下方 **整段代码块** 发送。  
> **人签**：两 task **HG-TASK-DRAFT 均已 approved**（2026-06-16）  
> **帽链**：每 task **30 → 40 → CLOSE → PR → CI 绿 → merge**（各 skip 50 · `audit_profile: post_close`）  
> **硬闸门**：**P1 须在 P0 PR CI 全绿且已 merge 入 `main` 后** 方可开 30；禁止同会话跳过 merge 直连 P1

| 项 | 值 |
| --- | --- |
| **chain_slug** | `graph-yaml-inform-closure-chain` |
| **Round** | T1 |
| **P0** | `graph-yaml-doc-hygiene-p0` · `task/graph-yaml-doc-hygiene-p0` |
| **P1** | `graph-yaml-export-yaml-p1` · `task/graph-yaml-export-yaml-p1` |

---

```text
你是 **Harness 串行执行 Agent**（Ink 后端仓 · 图谱 YAML Inform 闭环 · T1）。

【角色】**两阶段串行** · P0 与 P1 各独立 PR；**P0 merge 前不得启动 P1**。

【开帽 · GATE_SCAN】
- P0 HG-TASK-DRAFT: approved ✓
- P1 HG-TASK-DRAFT: approved ✓（30 须满足下方 **P1 硬闸门**）
- Open Folder: ai-ink-brain-api-python/
- 禁止代签 HG-REINSPECT
- 禁止改 cyning-harness/ · 工作区 docs/harness/

【P1 硬闸门 · 四项齐备，缺一 STOP】
1. P0 task 在 docs/tasks/done/ 且 HG-REINSPECT signed
2. P0 PR **GitHub Actions CI 全绿**（至少 tech-graph · pytest 合并前必绿项）
3. P0 PR **已 merge 入 origin/main**
4. 本地 `git checkout main && git pull` 可拉到 P0 merge commit

未满足 → **只完成/汇报 P0** · 输出 PR URL 与 CI 状态 · **STOP，不得进入 PHASE B**

【canonical 读序】
1. docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1_T1_graph-yaml-inform-closure_zh.md
2. docs/tasks/active/task_engineering_graph_yaml_doc_hygiene_p0_v1.md
3. docs/tasks/active/task_engineering_graph_yaml_export_from_yaml_p1_v1.md
4. docs/harness/prompts/hats/30-execute-code.md
5. docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
6. AGENTS.md

═══════════════════════════════════════════════════════════
 PHASE A · P0 · graph-yaml-doc-hygiene-p0
═══════════════════════════════════════════════════════════

【A0 · 分支】
git checkout main && git pull
git checkout -b task/graph-yaml-doc-hygiene-p0

【A1 · 30 执行 · D1–D5】
- 改 scripts/graph_yaml_compile.py · generate_sub_graph_links()：
  「AI 协议版 *.ai.md」→「编辑源 *.graph.yaml」（7 张子流程）
- python scripts/graph_yaml_compile.py --graph-id 00_main
- QNA 增 §已知遗留 · 幽灵节点 + 修订 v1.2
- rg '.ai.md' docs/_tech_graph --glob '!*.ai.md' 清扫（@deprecated 除外）
- tests/test_graph_yaml_compile.py 新增 test_00_main_subgraph_links_no_ai_md_href

【A2 · 验收】
pytest tests/test_graph_yaml_compile.py -q
python scripts/graph_yaml_compile.py --all --check
bash scripts/verify-tech-graph.sh
pytest tests -m "not intent_eval and not intent_benchmark" -q
ruff check api tests

【A3 · 40 自检】
独立复跑 A2；核对 Sub-graph 无 .ai.md href；回填 P0 task §实现备忘 · §自检结论（40 帽）

【A4 · invoke 落盘】
docs/harness/invokes/by-task/graph-yaml-doc-hygiene-p0/invoke_YYYYMMDD_30_*.md
docs/harness/invokes/by-task/graph-yaml-doc-hygiene-p0/invoke_YYYYMMDD_40_*.md

【A5 · CLOSE P0 + PR】
- task 范围/验收 [x] · HG-REINSPECT → signed
- git mv docs/tasks/active/... → docs/tasks/done/
- 更新 docs/tasks/_views/done.md · done_by_domain.md · RECENT §1.6 续
- commit · push · **开 PR**（目标分支 main）

【A6 · CI + merge（P0 终点 · 进入 P1 前必完成）】
- 等待 PR **CI 全绿**（`.github/workflows/tech-graph.yml` · pytest 合并前必绿）
- **merge PR 入 main**（维护者或 Agent 有权限则 merge；否则 STOP 等人 merge）
- 回报：PR URL · CI 状态 · merge commit SHA

【A7 · 闸门 · 可否进入 PHASE B】
同时满足 P1 硬闸门四项 → 可开 PHASE B（建议 **新对话** 或维护者显式确认后续跑）
任一不满足 → **STOP** · 不得 checkout P1 分支 · 不得改 export 代码

═══════════════════════════════════════════════════════════
 PHASE B · P1 · graph-yaml-export-yaml-p1
═══════════════════════════════════════════════════════════

【B0 · 分支】（**仅 P0 已 merge 的 main**）
git checkout main && git pull   # 须含 P0 merge commit
git checkout -b task/graph-yaml-export-yaml-p1
# 禁止 cherry-pick 替代 merge，除非 task §实现备忘 书面记录且维护者批准

【B1 · 30 执行 · D1–D7】
- 新增 tools/tech_graph_graph_v2_yaml.py（或等价）：7× .graph.yaml → graph_v2
- tools/tech_graph_graph_export.py · build_graph_payload() 改读 YAML
- 保留 .ai.md 解析供单测 · CI 主路径不依赖 ai 内容
- tools/tech_graph_manifest_check.py：移除 00_main.ai.md TIP
- docs/_tech_graph/99_spec.md：graph.json 由 YAML export 生成
- pytest：export --check 绿 + F3 回归（污染 .ai.md 不影响 export）

【B2 · 验收】
python tools/tech_graph_graph_export.py --check
python scripts/graph_yaml_compile.py --all --check
pytest tests/test_tech_graph_graph*.py tests/test_graph_yaml*.py -q
bash scripts/verify-tech-graph.sh
pytest tests -m "not intent_eval and not intent_benchmark" -q
ruff check api tests

【B3 · 40 自检 + CLOSE P1】
同 P0 模式：回填 · invoke 30/40 · HG-REINSPECT signed · git mv → done/ · 更新索引

【B4 · 链收尾】
RECENT §1.6 续 标注「Inform YAML 单源闭环完成」；删 .ai.md 仍另 task（G0）

═══════════════════════════════════════════════════════════
 非范围（两 phase 均 STOP）
═══════════════════════════════════════════════════════════
- 不删 7× .ai.md
- 不手改 graph.json 拓扑（除非 export bug 且最小 fix + 书面说明）
- 不做 external_ref schema
- 不引入 .cyning-harness/

【回报格式 · 硬】
## P0 Status / Deliverables / Blockers
## P0 PR URL · CI 状态 · 是否已 merge
## P1 Status（若未开 30 写「等待 P0 CI 绿 + merge」）
## 建议下一步
```

---

## 分步启动（推荐）

| 阶段 | 动作 |
| --- | --- |
| **会话 1** | 复制上方代码块 → 仅执行 **PHASE A** → P0 PR **CI 绿 + merge** 后 **STOP** |
| **会话 2** | 确认 P1 硬闸门四项 → 用 [`../graph-yaml-export-yaml-p1/PROMPT_START_30_v1.md`](../graph-yaml-export-yaml-p1/PROMPT_START_30_v1.md) 开 P1 |

**禁止** 在 P0 PR 未 merge 时在同一会话继续 PHASE B。
