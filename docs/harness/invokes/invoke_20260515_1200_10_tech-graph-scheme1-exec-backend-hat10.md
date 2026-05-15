# Harness invoke snapshot

| 字段 | 值 |
|------|-----|
| hat_id | 10（执行帽 · 后端子仓） |
| template | 用户结构化指令（`ai-ink-brain-api-python` 技术图谱 / 闸口 A · 后端执行帽） |
| task_paths | `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_graph_json_export_v1.md`；`ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_token_compare_v1.md` |
| related_review_or_none | 无 |
| prev_invoke | `docs/harness/invokes/invoke_20260515_0000_10_tech-graph-scheme1-exec-converge-hat10.md`（工作区根） |
| created_utc_or_local | 2026-05-15 12:00 CST |
| notes | 分支 `agent-v3`；`freeze_id`=`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`；三脚本并行不合并 |

## 可复制 Prompt 快照（与对话首条 user 一致）

```text
【角色】`ai-ink-brain-api-python` 子仓执行帽（技术图谱 / 闸口 A · 后端）

【cwd】
- 一切命令与改文件均在 **`ai-ink-brain-api-python` 仓根** 下执行（`pwd` 须为该仓根）。

【硬约束】
- **`freeze_id` 行不得改**：与前端 task **逐字一致** → `TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`（勿写入 commit hash）。
- **`tools/tech_graph_contract_check.py`**、**`tools/tech_graph_graph_export.py`**、**`tools/tech_graph_token_estimate.py`** **三脚本并行**；**禁止**把契约校验、graph `--check`、token 估算 **合并进同一 .py 文件**。
- 改 `.ai.md` 须同 PR 更新 **`docs/_tech_graph/graph.json`** 并保证 `python tools/tech_graph_graph_export.py --check` 绿。

【必读 task（相对工作区根 `Projects/`）】
1. `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_graph_json_export_v1.md`（方案1：导出 / `--check` / pytest / `tech-graph`；§4～§8、CI 命令摘要）
2. `ai-ink-brain-api-python/docs/tasks/active/task_engineering_tech_graph_gate_a_token_compare_v1.md`（闸口 A 附录：token 粗估；§4～§6）

【必读闸口 / SOP】
- `ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_backend.md`（尤其「仓库或 CI 快照引用」、§2 代号 A/B、§3 指标含可选 token 行）
- `ai-ink-brain-api-python/docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md`
- 规划（工作区）：`docs/tech_graph/改进方向.md` v1.1.3；SPEC：`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`

【可选链上节】
- `docs/harness/invokes/invoke_20260515_0000_10_tech-graph-scheme1-exec-converge-hat10.md`

【交付清单（按优先级自检）】
1. **本地必绿**
   - `python tools/tech_graph_contract_check.py`
   - `python tools/tech_graph_manifest_check.py`
   - `python tools/tech_graph_graph_export.py --check`
   - `python tools/tech_graph_token_estimate.py`（及 `python tools/tech_graph_token_estimate.py --json`）
   - `pytest tests/test_tech_graph_graph_export.py tests/test_tech_graph_token_estimate.py -q`
   - （与 CI 对齐）`pytest tests -m "not intent_eval and not intent_benchmark" -q` 若本次改动可能影响全量
2. **PR 描述**：按 task_engineering_tech_graph_graph_json_export_v1.md「CI 命令摘要」写清 **contract** 与 **graph**（含 manifest → graph `--check` → token `--json`）两条路径及顺序；可附 **Actions run URL**。
3. **闸口父文档回填**：在 `gate_a_scheme1_backend.md`「**仓库或 CI 快照引用**」中，若 task `gate_a_token_compare` §4 仍 **`[ ]`**：从 **已绿** 的 `tech-graph` run 日志中 **粘贴一行** `python tools/tech_graph_token_estimate.py --json` 的 JSON 输出（或同内容 fenced），并把该条验收 **`[x]`**。
4. **task 状态**：若 §4 全部满足且已合并默认分支，按 `docs/tasks/README.md` 将 **`task_engineering_tech_graph_graph_json_export_v1.md`** **`git mv` 至 `docs/tasks/done/`**，更新 **`docs/tasks/_views/done.md`**，头部改为 `done（YYYY-MM-DD 验收通过）`；**`gate_a_token_compare`** 同步勾选后同样归档或保持 `draft` 直至你确认——以 task 正文为准。
5. **Invoke 快照（新帽开节时）**：若本消息为对话首条执行帽，按 `docs/harness/invokes/README.md` 在 `ai-ink-brain-api-python/docs/harness/invokes/`（或工作区 `docs/harness/invokes/` 指针对应子仓）落盘一份 invoke 快照，正文含本段 Prompt。

【禁止】
- 改 `freeze_id` 行写 hash；合并 contract/graph/token 脚本；无 pytest 仍宣称 `test_strategy: required` 已满足。

【完成后输出】
- 变更文件列表 + 本地/CI 验证命令与结果摘要 + 若已开 PR 给链接。
```
