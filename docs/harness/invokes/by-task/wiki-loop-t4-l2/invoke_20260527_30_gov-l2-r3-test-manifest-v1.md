# Invoke · 30 执行编码 · R3 · gov-l2-r3-test-manifest

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md` |
> | task_slug | gov-l2-r3-test-manifest |
> | freeze_id | GOV-L2-R3-TEST-MANIFEST@2026-05-27 |
> | git_branch | task/gov-spec-t4-l2-v1 |

---

## §1 角色与纪律

- 本帽为 **30 执行编码**（`docs/harness/prompts/hats/30-execute-code.md`）。
- 上一帽 22 已结束；本帽执行 task §范围。
- 仅 docs + `_test_manifest.json`；不改 api/、tests/、prompts/、CI。

## §2 执行摘要

**已交付**（5 文件，+71/-3）：

| 文件 | 动作 | 说明 |
|------|------|------|
| `docs/_tech_graph/_test_manifest.json` | **新增** | 6 entries；3 条含 `graph_nodes_optional`（C1/RAG） |
| `docs/_tech_graph/99_spec.md` | 增小节 | 「测试 manifest（L2）」链 L2 SPEC + 脚本表 |
| `docs/coding_wiki/CODING_WIKI.md` | 改 1 行 | §8 链 L2 SPEC |
| `docs/tasks/RECENT_TASK_SCHEDULE.md` | 改 1 行 | T4+L2 → **done** |
| `docs/harness/invokes/by-task/wiki-loop-t4-l2/README.md` | 改 1 行 | R3 验收说明 |

**_test_manifest.json entries**：

| id | error_codes | test_paths | graph_nodes_optional |
|----|-------------|------------|----------------------|
| FP-RAG-DB-DISCONNECT | DATABASE_DISCONNECT | tests/test_chatbi_principal_network.py | C1 |
| FP-UNIFIED-INVALID-JSON | Invalid JSON | tests/test_unified_chat_backend_v1.py | C1 |
| FP-CODE-RETRIEVAL-UNAUTHORIZED | Unauthorized | tests/test_code_api_routes.py | — |
| FP-SQL-GATE-DENIED | ChatBiSqlGateDenied | tests/test_chatbi_sql_ast_gate_v1.py | RAG |
| FP-QUERY-REWRITE-ANCHOR-LOST | QUERY_REWRITE_ANCHOR_LOST | tests/test_query_rewrite_compare_anchor.py | C1, RAG |
| FP-HEALTH-PROBE-FAIL | HEALTH_PROBE_FAIL | tests/test_health_probe_routes.py | — |

## §3 下一棒可复制 Prompt（40 自检）

```text
你正在执行 Wiki Loop T4+L2 **R3** 的 **40 自检帽**。上一帽（30 执行编码）已结束；本帽只按下文执行。

【元信息】
- round: R3
- hat: 40
- task: docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md
- task_slug: gov-l2-r3-test-manifest
- freeze_id: GOV-L2-R3-TEST-MANIFEST@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 40 帽职责
按 `docs/harness/prompts/hats/40-self-check.md`：
1. 逐条对照 task §验收标准，标记 pass/fail。
2. 运行 task 所列 VERIFY 命令，粘贴原始输出要点。
3. 将结论回填至 task 正文 `### 自检结论（执行者）` 小节。
4. 输出 50 独立复检 invoke。
5. 按 HANDOFF_AUTO_COMMIT 提交。

### 验收标准与 VERIFY

- [ ] `test -f docs/_tech_graph/_test_manifest.json`
- [ ] `python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5"`
- [ ] `python tools/tech_graph_manifest_check.py` exit 0
- [ ] `python tools/tech_graph_graph_export.py --check` exit 0

### 回填位置
task 文件末尾 `### 自检结论（执行者）` 空表（若不存在则新增于「实现备忘」之上）。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── task：task_governance_l2_r3_test_manifest_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：_test_manifest.json（6 entries）+ 4 文件修改
├── 下一棒：A=40 自检 · B=—
├── 推荐：A
└── 阻塞：无
```
