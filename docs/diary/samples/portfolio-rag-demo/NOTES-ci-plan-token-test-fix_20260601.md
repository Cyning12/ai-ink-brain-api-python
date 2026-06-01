# PR #101 CI：plan_execution_token 测试碰撞 · 复盘

> **日期**：2026-06-01  
> **PR**：[#101](https://github.com/Cyning12/ai-ink-brain-api-python/pull/101) · `task/portfolio-rag-demo-v1`  
> **修复 commit**：`1823ba7`  
> **关联测试**：`tests/test_unified_chat_backend_v2_agent.py::test_v3_plan_execution_token_invalid_json_denies_bypass`

---

## 1. 现象

portfolio 文档 PR 的 CI 中 **pytest 红**，失败断言：

```text
assert 'agent.clarify' in types_bad
```

表象像 Unified Chat 低置信澄清回归；**与 portfolio 文档改动无直接关系**（全仓 pytest 扫到既有用例）。

---

## 2. 根因

测试用「末位 base64 字符 `A`↔`B`」构造「无效」`plan_execution_token`：

```python
tampered = tok[:-1] + ("A" if tok[-1] != "A" else "B")
```

在 **urlsafe base64** 下，末位有时只编码 **padding 位**。`A` 与 `B` 可能解码为**相同字节**，HMAC 验签仍通过 → 请求走全量 Text2SQL，不出现 `agent.clarify`。

本地可复现（示例）：

| 操作 | `verify_clarify_plan_bypass_token` |
| --- | --- |
| 原 token | True |
| 末位 A→B（碰撞） | **True**（测试误以为已无效） |
| 中间字符翻转 | False |

**结论**：实现逻辑正确；是测试篡改策略不可靠，非 ChatBI / portfolio 业务 bug。

---

## 3. 修复

改为翻转 **中间字符**，稳定构造无效 token：

```python
mid = max(1, len(tok) // 2)
tampered = tok[:mid] + ("X" if tok[mid] != "X" else "Y") + tok[mid + 1 :]
```

---

## 4. 经验（可复用）

### 4.1 文档 PR 也会跑全量 pytest

后端 **任何 PR** 均跑 `pytest tests -m "not intent_eval and not intent_benchmark"`。文档-only 分支也可能因**无关测试**挡 merge。排查时先看失败栈是否在本 PR diff 内。

### 4.2 负向安全/鉴权测试的写法

1. 篡改后 **先断言** `verify_*()` 为 `False`，再测 HTTP 行为。  
2. **勿依赖** base64 末位单字符翻转 — 存在编码等价碰撞。  
3. 更稳的无效 token：中间位翻转、`tok + "x"`、或手工损坏 JSON/HMAC 段。

### 4.3 与 portfolio 鉴权勿混读

| 场景 | 机制 |
| --- | --- |
| 五问 Unified Chat | Bearer → `chatbi_access_tokens` 查库 |
| admin/sync ingest | `SYNC_ADMIN_SECRET`（前端）/ `CHAT_API_SECRET`（后端）同值 |

本次失败与 admin/sync 迁移、五问 token **无关**。

### 4.4 CI 排查顺序（简表）

- [ ] 失败是否在本 PR 改动文件内？  
- [ ] 本地单测能否复现？中间层（如 `verify_*`）结果如何？  
- [ ] flaky / 测试假设错 vs 实现回归？  
- [ ] 最小修复：只动测试还是动实现？

---

## 5. CI 结果（修复后）

| Check | 结果 |
| --- | --- |
| pytest | pass |
| verify | pass |
| task_validate | pass |
| contract_check / manifest_check | pass |

PR #101 Required checks 全绿，可 merge。
