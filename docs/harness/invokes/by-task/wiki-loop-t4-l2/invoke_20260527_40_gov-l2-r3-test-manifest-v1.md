# Invoke · 40 自检 · R3 · gov-l2-r3-test-manifest

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md` |
> | task_slug | gov-l2-r3-test-manifest |
> | freeze_id | GOV-L2-R3-TEST-MANIFEST@2026-05-27 |
> | git_branch | task/gov-spec-t4-l2-v1 |

---

## §1 角色与纪律

- 本帽为 **40 自检**（`docs/harness/prompts/hats/40-self-check.md`）。
- 上一帽 30 已结束；本帽独立重跑 VERIFY、回填 task 自检结论。

## §2 自检结果

### 2.1 命令输出

**V1 · _test_manifest.json 存在**：
```bash
$ test -f docs/_tech_graph/_test_manifest.json
EXIT:0
```

**V2 · entries ≥ 5**：
```bash
$ python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5; print(f'entries: {len(m[\"entries\"])}')"
entries: 6
OK
```

**V3 · manifest_check**：
```bash
$ python tools/tech_graph_manifest_check.py
OK: manifest matches code/SQL truth
EXIT:0
```

**V4 · graph_export --check**：
```bash
$ python tools/tech_graph_graph_export.py --check
EXIT:0
```

### 2.2 验收表

| 检查项 | 结果 | 证据 |
|--------|------|------|
| _test_manifest.json 存在 | **pass** | `test -f` exit 0 |
| entries ≥ 5 | **pass** | 6 entries |
| manifest_check | **pass** | exit 0 |
| graph_export --check | **pass** | exit 0 |
| 99_spec 测试 manifest 小节 | **pass** | `+L2 · _test_manifest` 小节 |
| CODING_WIKI §8 链 L2 SPEC | **pass** | 1 行替换 |
| RECENT §6.6 done | **pass** | T4+L2 → done |
| graph_nodes_optional ≥ 1 | **pass** | 3 条（C1, RAG） |

**全部 pass。无阻塞。**

## §3 回填确认

task 正文 `### 自检结论（执行者）` 已回填（8 项全 pass）。
`实现备忘` 表已填 `entry ids` 与 `commits`。

## §4 下一棒可复制 Prompt（50 独立复检）

```text
你正在执行 Wiki Loop T4+L2 **R3** 的 **50 独立复检帽**。上一帽（40 自检）已结束；本帽只按下文执行。

【元信息】
- round: R3
- hat: 50
- task: docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md
- task_slug: gov-l2-r3-test-manifest
- freeze_id: GOV-L2-R3-TEST-MANIFEST@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1

### 50 帽职责
按 `docs/harness/prompts/hats/50-independent-reinspect.md`：
1. 独立重跑 task §VERIFY 命令（不引用 40 结论为证据）。
2. 对照 task §验收标准逐条 pass/fail。
3. 检查 human_gate diff（确认未由 Agent 代填 approved）。
4. 落盘复检报告到 `docs/tasks/reinspect_results/reinspect_gov-l2-r3-test-manifest_20260527_v1.md`。
5. 若建议合并且无返工：输出关账 CLOSE_TRACE。
6. 按 HANDOFF_AUTO_COMMIT 提交。

### VERIFY（须独立重跑）
```bash
test -f docs/_tech_graph/_test_manifest.json
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5"
python tools/tech_graph_manifest_check.py
python tools/tech_graph_graph_export.py --check
```

### 落盘路径
`docs/tasks/reinspect_results/reinspect_gov-l2-r3-test-manifest_20260527_v1.md`
```

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── task：task_governance_l2_r3_test_manifest_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：VERIFY 全绿 + task 回填
├── 下一棒：A=50 独立复检 · B=—
├── 推荐：A
└── 阻塞：无
```
