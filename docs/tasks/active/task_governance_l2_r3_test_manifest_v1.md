# Task：治理 — L2 锚点与 `_test_manifest` 草案（R3）

> **状态**：active  
> **母 Loop**：[`task_harness_wiki_loop_t4_l2_v1.md`](task_harness_wiki_loop_t4_l2_v1.md) · round **R3**  
> **SPEC**：[`SPEC-Governance-L2-Anchor-Test-Manifest-v1.md`](../spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；**本 round 关账** 负责 RECENT §6.6 **done** + `_views/done.md` + invoke README 验收说明。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 仅新增 docs + `_test_manifest.json`；不跑 pytest 作 Loop 门禁。 |
| **freeze_id** | `GOV-L2-R3-TEST-MANIFEST@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-spec-t4-l2-v1` |
| **task_slug** | `gov-l2-r3-test-manifest` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 继承母闸 |

---

## 帽子顺序（**跳过 10** · Loop R3）

| 序 | 帽 | 启动 |
|----|-----|------|
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-t4-l2/PROMPT_LOOP_22_to_CLOSE_v1.md) · **round=R3** |

---

## 背景与目标

T4（R1–R2）完成后，落地 L2 工具链 **Phase A**：`docs/_tech_graph/_test_manifest.json`（≥5 条真实 ERR/pytest 映射），`test_paths` **仅** `tests/…` glob；`99_spec` + `CODING_WIKI` §8 指针。

**完成态**：

- `_test_manifest.json` 合法 JSON · ≥5 entries · 至少 1 条含 `graph_nodes_optional`（引用 R1 Pilot id，如 `C1`/`RAG`）。  
- `99_spec.md` 测试 manifest 小节链 L2 SPEC。  
- `CODING_WIKI.md` §8 一行链 L2 SPEC。  
- RECENT §6.6 本 Loop 行 → **done**。

---

## 范围

- [ ] 新增 `docs/_tech_graph/_test_manifest.json`（schema 见 L2 SPEC §4.1）。  
- [ ] `99_spec.md` 测试 manifest 指针。  
- [ ] `CODING_WIKI.md` §8 链 L2 SPEC。  
- [ ] RECENT done + `_views/done.md` + invoke README 验收一行。  
- [ ] 22/30/40/50 invoke C2 全绿。

## 非范围

- `tools/tech_graph_test_manifest_check.py`（Phase B）。  
- 改 `tests/` 源码。  
- api / Harness prompts / CI workflow。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | R2 未 done | 22 阻塞 |
| F2 | `test_paths` 非 glob 或缺 `tests/` 前缀 | 50 fail |
| F3 | `graph_export --check` 因误改 graph.json 失败 | 50 fail |
| F4 | 用 Wiki 替代 manifest 真值 | 违反 SPEC §8 |

---

## 验收标准

- [ ] `test -f docs/_tech_graph/_test_manifest.json`  
- [ ] `python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5"`  
- [ ] 图谱 CI 四脚本 exit 0  

**VERIFY**：

```bash
test -f docs/_tech_graph/_test_manifest.json
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m.get('entries',[]))>=5"
python tools/tech_graph_manifest_check.py
python tools/tech_graph_graph_export.py --check
```

---

## 实现备忘（执行者回填）

| 项 | 内容 |
| --- | --- |
| entry ids | |
| commits | |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| | | |
