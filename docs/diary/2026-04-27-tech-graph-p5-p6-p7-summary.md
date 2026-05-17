# 技术点总结：Tech Graph — 自动渲染 + 跨仓契约 + CI 门禁

> **记录日期**: 2026-04-27  
> **涉及任务**: 自动渲染 .ai.md、跨仓契约定义、CI 自动门禁  
> **核心主题**: Architecture Graph 的工程化落地 —— 从"人工维护"到"真值驱动 + 自动校验"

---

## 一、三个任务的关系

```
单仓真值校验      自动渲染 .ai.md         跨仓契约定义           CI 自动门禁
(manifest_check)  (render_ai)            (contract_check)       (GitHub Actions)
  │                    │                      │                      │
  ▼                    ▼                      ▼                      ▼
  └────────────────────┴──────────────────────┴──────────────────────┘
                              │
                              ▼
                    技术图谱工程化闭环
```

**递进关系**:
- **单仓真值校验**（已完成）：解决"单仓内部"的真值一致性（端点/RPC/表/env）
- **自动渲染 .ai.md**（本次）：解决"真值 → 文档"的自动同步（减少人工维护）
- **跨仓契约定义**（本次）：解决"前后端"的隐式耦合（SSE events 字段契约）
- **CI 自动门禁**（本次）：解决"校验自动化"（PR 阶段拦截契约漂移）

---

## 二、"三类图谱"的对应关系


| 图谱类型 | 文章中的名称 | 当前落地 | 状态 |
|----------|-------------|---------|------|
| **Architecture Graph** | 架构图谱 / 系统边界 | `docs/_tech_graph/` 下的入口总图、流程图、Struct 图 | ✅ **已落地 + 本次强化** |
| **Runtime Graph** | 运行图谱 / 观测链路 | `14_runtime_observability.md` + `_contract_manifest.json` | ✅ **已落地** |
| **System Graph** | 系统图谱 / 跨仓契约 | `15_e2e_boundary.md` + 跨仓校验脚本 | ✅ **已落地** |

**本次工作的本质**: 围绕 **Architecture Graph** 做工程化增强 —— 把"人工维护的架构文档"升级为"真值驱动、自动渲染、CI 校验"的可信架构事实源。

---

## 三、自动补全/增量渲染（从 manifest 生成 .ai.md）

### 核心问题

改端点后，需要手工同步 `00_main.ai.md`，容易"manifest 更新了，但 .ai.md 没更新"。

### 解决方案

**区块替换策略**: 在 `00_main.ai.md` 中标记可机械生成的区块，脚本只替换该区块。

```markdown
<!-- 00_main.ai.md -->
## 端点列表

<!-- AUTO:ENDPOINTS_AND_ANCHORS BEGIN -->
<!-- 以下内容由 tools/tech_graph_render_ai.py 自动生成 -->
- `GET /api/py/health`
- `POST /api/py/chat`
...
<!-- AUTO:ENDPOINTS_AND_ANCHORS END -->

## 业务子流程（手写，不动）
...
```

### 关键技术点

| 技术点 | 说明 |
|--------|------|
| **幂等设计** | 多次运行输出一致，无额外 diff |
| **最小 diff** | 只替换 auto 区块，手写内容不动 |
| **真值来源** | 从 `_manifest.json` 读取，不扫描代码 |
| **解耦策略** | "可机械生成的真值段落"与"人工维护的业务子流程"分离 |

### 涉及文件

- `tools/tech_graph_render_ai.py` — 渲染脚本
- `docs/_tech_graph/00_main.ai.md` — 新增 auto 区块标记
- `tools/tech_graph_manifest_check.py` — 增加"建议运行 render"提示

---

## 四、跨仓契约 + Cross-Repo 门禁脚本

### 核心问题

前后端隐式耦合：后端改了 SSE events 字段，前端解析崩；前端依赖了字段，但后端未承诺稳定。

### 解决方案

**契约真值 + 双向校验**:

```
后端产出 (truth)  ──⊇──  契约 (contract)  ──⊇──  前端消费 (expect)
     │                       │                       │
     └─────── 脚本校验 ──────┴─────── 脚本校验 ──────┘
```

### 契约文件结构

```json
// docs/_tech_graph/_contract_manifest.json
{
  "sse": {
    "envelope": {
      "event_values": ["chain", "done"]
    },
    "chain": {
      "data_keys": ["type", "ts", "step_id", "payload"]
    },
    "done": {
      "data_keys": ["ok", "mode", "run_id", "session_id"]
    }
  },
  "frontend_anchors": [
    "../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx",
    "../ai-ink-brain/app/api/py/unified/chat/stream/route.ts"
  ]
}
```

### 校验规则

| 规则 | 说明 |
|------|------|
| `backend_truth ⊇ contract_manifest` | 后端至少产出承诺的键 |
| `frontend_expect ⊆ contract_manifest` | 前端不得读取未承诺的键 |
| `frontend_expect.event_values ⊆ allowed_events` | 事件枚举一致性 |

### 关键技术点

| 技术点 | 说明 |
|--------|------|
| **静态抽取** | 用 regex/轻量解析抽键名，不做 AST/语义分析 |
| **双向约束** | 后端"至少产出" + 前端"不得越界" |
| **返回码语义** | `0=OK`, `1=drift`, `2=运行错误` |
| **契约优先** | 变更顺序：先改契约 → 再改后端 → 再改前端 |

### 涉及文件

- `docs/_tech_graph/_contract_manifest.json` — 跨仓契约真值
- `tools/tech_graph_contract_check.py` — 校验脚本
- `tools/tech_graph_contract_demo.py` — 演示脚本（一键体验负向→恢复）
- `docs/_tech_graph/15_e2e_boundary.ai.md` — 图谱补充说明

---

## 五、Cross-Repo Contract Check 接入 CI

### 核心问题

契约校验目前只能本地手动运行，PR 合并后才暴露漂移。

### 解决方案

**GitHub Actions 自动门禁**: 每次 PR / push main 自动执行跨仓契约检查。

### CI 设计要点

**Checkout 策略（方案 A）**:

```yaml
# .github/workflows/tech-graph-contract.yml
jobs:
  contract_check:
    steps:
      - name: Checkout backend
        uses: actions/checkout@v4
        with:
          path: ai-ink-brain-api-python
      
      - name: Checkout frontend
        uses: actions/checkout@v4
        with:
          repository: cyning/ai-ink-brain
          path: ai-ink-brain
      
      - name: Run contract check
        working-directory: ai-ink-brain-api-python
        run: python tools/tech_graph_contract_check.py
```

**关键约束**:
- CI 只做**静态检查**（键名集合/枚举），不运行服务
- 前端仓 checkout 到 `../ai-ink-brain/` 保持相对路径一致
- 不引入外部私有依赖

### 涉及文件

- `.github/workflows/tech-graph-contract.yml` — CI workflow
- `docs/_tech_graph/15_e2e_boundary.ai.md` — 补充 CI 门禁说明

---

## 六、今日技术点汇总

### 1. 真值驱动（Single Source of Truth）

```
_manifest.json          → 单仓真值（端点/RPC/表/env）
_contract_manifest.json → 跨仓真值（SSE events 字段契约）
     │
     ▼
tools/xxx_check.py      → 校验脚本（返回码 0/1/2）
tools/xxx_render_ai.py  → 渲染脚本（增量更新文档）
```

**核心思想**: 先定义真值，再让代码和文档都向真值对齐。

### 2. 区块替换（Incremental Render）

不是全量生成文档，而是标记可机械生成的区块，只替换该区块。

```markdown
<!-- AUTO:XXX BEGIN -->
<!-- 机器生成 -->
<!-- AUTO:XXX END -->
```

**好处**: 减少 diff、避免误伤手写内容、可一键修复。

### 3. 双向契约校验（Cross-Repo Contract）

不是单向的"后端定义、前端遵守"，而是双向约束：
- 后端必须**覆盖**契约（不能少字段）
- 前端必须**不越界**（不能读未承诺字段）

### 4. 返回码语义化

```python
0  # OK — 校验通过
1  # drift — 真值不一致（可被 CI 识别为失败）
2  # error — 运行错误（文件缺失、脚本异常）
```

### 5. CI 静态检查

不运行服务、不做 e2e，只做**静态键名/枚举校验**，速度快、稳定性高。

### 6. 变更 SOP（契约优先）

```
端点变更:     改后端 → 更新 manifest → 跑 manifest_check → （可选）跑 render
Events 变更:  更新 contract → 改后端 → 跑 contract_check → 改前端 → 再跑 contract_check
```

---

## 七、三类图谱的后续设计思考

根据文章中的框架，当前三类图谱的落地状态：

### Architecture Graph（架构图谱）— 本次强化

**已落地**:
- `00_main.md` — 入口总图（Mermaid 拓扑）
- `01_struct.md` — 数据库结构
- `10~13_flow_*.md` — 业务流程图（RAG/Text2SQL/FTS/RPC）
- `_manifest.json` — 真值来源
- `tech_graph_manifest_check.py` — 漂移校验
- `tech_graph_render_ai.py` — 自动渲染

**待增强**:
- 模块依赖图（当前只有入口图，无模块间调用关系）
- 配置依赖图（39 个 env 变量的依赖关系）
- 失败路径图（当前只有 happy path）

### Runtime Graph（运行图谱）— 已落地

**已落地**:
- `14_runtime_observability.md` — 事件流、日志落点
- `_contract_manifest.json` — SSE 事件契约
- `tech_graph_contract_check.py` — 跨仓校验
- `tech-graph-contract.yml` — CI 门禁

**待增强**:
- 错误码分层图（当前只有事件类型，无错误分级）
- 超时/重试策略图（散落在代码中，未集中）
- 降级策略图（当前无显式定义）

### System Graph（系统图谱 / 跨仓契约）— 已落地

**已落地**:
- `15_e2e_boundary.md` — E2E 边界、锚点
- `_contract_manifest.json` — 前后端契约
- `tech_graph_contract_check.py` — 双向校验

**待增强**:
- 前端状态机图（当前只有后端流程）
- API 版本演进图（当前无版本管理）
- 数据流图（内容仓库 → 向量库 → 前端展示的完整链路）

---

## 八、落地文件清单

| 文件 | 任务 | 作用 |
|------|------|------|
| `docs/_tech_graph/_manifest.json` | 单仓真值 | 单仓真值（端点/RPC/表/env/anchors） |
| `docs/_tech_graph/_contract_manifest.json` | 跨仓契约 | 跨仓契约真值（SSE events 字段） |
| `tools/tech_graph_manifest_check.py` | 单仓真值 | 单仓真值校验 |
| `tools/tech_graph_render_ai.py` | 自动渲染 | 从 manifest 增量渲染 .ai.md |
| `tools/tech_graph_contract_check.py` | 跨仓契约 | 跨仓契约校验 |
| `tools/tech_graph_contract_demo.py` | 跨仓契约 | 演示脚本（负向→恢复） |
| `.github/workflows/tech-graph.yml` | 单仓真值 | 单仓 drift CI |
| `.github/workflows/tech-graph-contract.yml` | CI 门禁 | 跨仓契约 CI |

---

## 九、一句话总结

> **今天的核心成果：把 Architecture Graph 从人工维护的文档，升级为"真值驱动 + 自动渲染 + CI 门禁"的工程化体系。**
>
> **关键思想：先定义真值（manifest），再让代码、文档、前后端都向真值对齐，用脚本自动发现和拦截漂移。**
>
> **后续方向：补齐 Runtime Graph 的错误分级/超时策略、System Graph 的前端状态机/数据流。**

---
