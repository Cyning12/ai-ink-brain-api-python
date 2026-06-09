# R1 Audit · W1 · api-env-rag-env-consolidation

> **hat**: 22 · **date**: 2026-06-09 · **verdict**: **PASS（无阻塞）**

## D1 范围

- 仅 `rag_env.py` + `index.py` + tests — **符合** MANIFEST W1
- api/*.py 触达 ≤2 — **无 mega-refactor 风险**

## D2 测试计划

- 新建 `test_rag_env_helpers_w1.py` 锁 helper 行为 — **可接受**
- 既有 unified/legacy route 测试回归 — **required**

## D3 契约

- 无 HTTP path / SSE 变更 — **PASS**
- `bind_index_symbols` 值域须与现网一致 — **30 帽须对照**

## failure_paths

- F1/F2 已在 task 列出 — **充分**

## Blockers

无

## Judgment

**批准 30 帽实现** — 先写 pytest，再迁 index env，禁止触 MANIFEST 外模块。
