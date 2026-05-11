# ChatBI V3 — 身份与访问控制（RBAC + 数据域）

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2.1** P1-3  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §3.1、§4.2 P0

---

## 1. 目标

从 **简单 Token 鉴权**（V2 明确不覆盖企业级权限）演进到：**角色（Role）**、**权限（Permission）**、**数据域（Data scope）** 可表述、可审计、可与 Text2SQL / RAG 工具链 **接合**。

---

## 2. 概念模型（初版 — 设计 PR 可调整命名）

| 概念 | 说明 |
|------|------|
| **主体** | 人用户 / 服务账号（若未来有） |
| **角色** | 如 `admin`、`analyst`、`viewer` |
| **权限** | API 路由级 + 工具级（能否触发 `text2sql_execute`、能否导出） |
| **数据域** | 行级/表级可见集合（与 Supabase RLS 或应用层过滤二选一或组合 — **实现 PR 必选其一为真值**） |

---

## 3. 与 ChatBI 链路的接合点（须在设计文档中画清）

| 接合点 | 要求 |
|--------|------|
| **Unified Chat 入口** | 解析身份 → 注入 `AgentMemoryStore` / Tool 上下文中的 **只读域提示** |
| **Text2SQL** | 生成 SQL 前已有 **表白名单** 或等价约束（与安全子规 **§2** 协同） |
| **RAG** | 检索命名空间或 `metadata` 过滤与角色绑定 |

---

## 4. 迁移策略（待决）

- 现有 Token 用户如何映射首个角色？  
- 是否允许「无角色 = 仅演示只读域」？  

**结论**：上表须在 **独立设计文档** 或任务单中拍板后再改本规 `状态` 为 `stable` 段落。

---

## 5. 非范围

- 多租户 **tenant_id** 全链路（划入 V4 / Enterprise §4.3）。  
- SSO/OAuth 完整 IdP 集成 —— **可**列为 V3.1，本初版不强制。

---

## 6. 关联

- [`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md)  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`

---

## 7. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
