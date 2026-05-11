# ChatBI V3 — 韧性、容量与健康检查

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2.1** P2-1  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §3.3.1–3.3.2、§4.2 P1

---

## 1. 目标

在 **不**改变 V2 业务语义的前提下，为 FastAPI 服务增加：**过载保护**、**下游失败隔离**、**编排与探活** 的标准接口，便于 K8s / 负载均衡 / 监控采集。

---

## 2. 限流（Rate limiting）

| 项 | 初版约束 |
|----|----------|
| **粒度** | 至少支持 **每 IP** 或 **每 API Key**（与现有鉴权方式对齐） |
| **范围** | 建议优先 **`/api/py/unified/chat/stream`** 与 **`/api/py/chat`** 高消耗路径 |
| **响应** | HTTP `429` + 结构化 body（`error_code`、`retry_after` 可选） |
| **配置** | 阈值进 `PROJECT_CONFIG` / env，**禁止**硬编码魔法数合主分支 |

---

## 3. 熔断（Circuit breaker）

| 项 | 初版约束 |
|----|----------|
| **对象** | 上游 LLM HTTP、Supabase 客户端等 **外呼** |
| **状态** | 至少 **open / half-open / closed** 语义之一可观测（日志或 metrics 钩子） |
| **降级** | 与 V2 已有 `error_code` / fallback 路径兼容，**不**静默吞错误 |

---

## 4. 健康检查端点

| 路径（建议） | 语义 | 响应要点 |
|--------------|------|----------|
| **`/health` 或 `/live`** | 进程存活 | 轻量 200，**不**强制打外呼 |
| **`/ready`** | 依赖就绪 | DB / 关键 env 探测失败时 **503**，body 说明组件名 |

**契约**：JSON 字段集在实现 PR 写入 `PROJECT_CONFIG` 一行 + 可选 `_tech_graph` 流程边。

---

## 5. 非范围

- 全链路 APM 厂商选型。  
- 自动扩缩容策略（HPA）—— 运维侧，本规只保证 **探活契约**。

---

## 6. 关联

- [`SPEC-ChatBI-V3-Logging-Trace.md`](SPEC-ChatBI-V3-Logging-Trace.md)

---

## 7. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
