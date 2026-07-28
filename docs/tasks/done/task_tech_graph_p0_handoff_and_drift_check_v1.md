# Task：Tech Graph P0 — 可接手性补强 + 最小漂移校验

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

 
> **状态**：done  
> **关联图谱**：`docs/_tech_graph/00_main.md`、`docs/_tech_graph/01_struct.md`、`docs/_tech_graph/99_spec.md`  
> **前端依赖**：无
 
---
 
## 背景与目标
 
为 `_tech_graph` 图谱补齐“新 Agent 直接接手”的最低保障，并提供最小机制防止图谱静默过期：
 
- 图谱入口可直接定位到 **代码入口 handler/关键函数**
- Struct 明确字段 **required/optional**，降低误用与幻觉
- 引入最小漂移校验：端点/RPC/env/表名变更能被检测
 
---
 
## 范围
 
- [x] `00_main.md`：入口节点补齐 **文件 + handler/关键函数 + 行号锚点**；补齐遗漏端点入口
- [x] `00_main.ai.md`：同步补齐上述锚点（AI 协议版）
- [x] `01_struct.md`：为 `metadata` 字段标注 `(req)/(opt)`，补齐 code_chunks 扩展字段
- [x] `tools/tech_graph_drift_check.py`：新增最小漂移校验脚本
- [x] `99_spec.md`：写入漂移校验运行方式，并把关键 env 覆盖到 Env Truth Table
 
## 非范围
 
- 不引入 manifest（P1 才做）
- 不引入 CI 工作流改造（P1 才做）
- 不重绘现有子流程图（保持增量）
 
---
 
## 依赖与引用
 
| 依赖项 | 路径/说明 |
|--------|-----------|
| Mermaid 协议 | `docs/_tech_graph/99_mermaid_protocol.md` |
| 路由真值 | `api/index.py` |
| RPC/表调用点 | `api/*.py` |
| SQL 真值 | `supabase/sql/*.sql` |
 
---
 
## 验收标准
 
- [x] 新 Agent 只读 `00_main.md` + `99_spec.md`，即可定位主要入口与下一步任务
- [x] `01_struct.md` 明确区分 `(req)` 与 `(opt)`（尤其 `metadata.*`）
- [x] 执行 `python tools/tech_graph_drift_check.py` 返回 `OK`
 
---
 
## 实现备忘（回填）
 
| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/00_main.md`、`docs/_tech_graph/00_main.ai.md`、`docs/_tech_graph/01_struct.md`、`docs/_tech_graph/99_spec.md`、`tools/tech_graph_drift_check.py` |
| 关键 env | 覆盖检查：`NEXT_PUBLIC_SUPABASE_URL`/`SUPABASE_URL`、`SUPABASE_SERVICE_ROLE_KEY`/`SUPABASE_SERVICE_KEY`、`SILICONFLOW_*`、`RAG_*`、`DEBUG_*`、`TEXT2SQL_*`、`API_KEY`、`CHAT_API_SECRET` |
| 接口变更 | 无（仅图谱补全与工具新增） |
| 图谱变更点 | 锚点升级（含行号/handler）、Struct req/opt、Backlog/Env 补齐、Parking Lot 保留 |
| 验收命令 | `python tools/tech_graph_drift_check.py` |

