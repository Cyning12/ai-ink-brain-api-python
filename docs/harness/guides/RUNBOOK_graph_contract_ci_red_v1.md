# Runbook · 图谱 manifest / contract CI 红字

> **用途**：开发者或 22 帽审查时，对照 CI stderr 三段式（位置 · 文档声明 · 当前代码 · 下一步）快速修复。  
> **关联**：IMP-B-01 · FAQ F20 卷四主失败分支 · `tech-graph.yml` / `tech-graph-contract.yml`

---

## 1. 何时打开本文

| CI job | 命令 | 典型触发 |
|--------|------|----------|
| `manifest_check` | `python tools/tech_graph_manifest_check.py` | 改 `api/`、`supabase/sql/` 未同步 `_manifest.json` |
| `contract_check` | `python tools/tech_graph_contract_check.py` | 改 SSE 事件/字段未同步 `_contract_manifest.json` |
| `graph export --check` | `python tools/tech_graph_graph_export.py --check` | 改 `.ai.md` 未 export `graph.json` |

stderr 首行以 `❌` 开头，每条 drift 含 **位置 / 文档声明 / 当前代码**。

---

## 2. 修复路径（路径 A · 推荐）

1. 在 **active task** 的 `§行为变更（Delta）` 写明 ADDED/MODIFIED（触达 `api/` 时 `test_strategy: required` + 50 落盘）。  
2. **同 PR** 更新：
   - `_manifest.json`（端点 / RPC / 表 / env / anchors）
   - `_contract_manifest.json`（SSE 契约，若涉 Unified Chat）
   - 受影响 `docs/_tech_graph/*.ai.md` → `python tools/tech_graph_graph_export.py`
3. 本地跑与 CI 相同命令（见 stderr 末尾）。  
4. `pytest tests -m "not intent_eval and not intent_benchmark"` 绿后再 push。

**禁止**：merge 后再开单独 PR 只改图谱（FAQ 已拒）。

---

## 3. 修复路径（路径 B · 误改）

```bash
git checkout -- api/   # 或 git revert 指定 commit
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
```

确认 stderr 无 `❌` 后再 push。

---

## 4. 常见 drift 对照

| stderr 位置前缀 | 文档侧 | 代码侧 | 下一步 |
|-----------------|--------|--------|--------|
| `manifest.endpoints` | `_manifest.json` endpoints | `api/index.py` 路由装饰器 | 补/删 manifest 条目或回滚路由 |
| `manifest.supabase.tables` | manifest tables | `.table("…")` / SQL CREATE | 同步表名清单 |
| `contract.sse.*` | `_contract_manifest.json` | `api/unified_chat.py` 等 | 同步 allowed_events / payload keys |
| `manifest.anchors` | anchors path+symbol | 源文件 def/class | 修正锚点或符号名 |

---

## 5. 22 帽审查粘贴

CI 日志中 `--- 问题 N/M ---` 至 `Runbook:` 行可直接贴入 `reviews/` R1，无需重写。

---

## 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-05-31 | IMP-B-01 初版；链 tech_graph_ci_stderr |
