# Task：P7 - Cross-Repo Contract Check 接入 CI（v1）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：done（2026-04-27 验收通过）  
> **关联图谱**：`docs/_tech_graph/15_e2e_boundary.ai.md`、`docs/_tech_graph/14_runtime_observability.ai.md`  
> **关联 Issue/PR**：无  
> **前端依赖**：`ai-ink-brain/content/tasks/active/task_frontend_unified_chat_sse_request_id_v1.md`（可并行；CI 只需要可 checkout 前端仓）

---

## 背景与目标

当前后端仓已具备跨仓契约校验脚本 `tools/tech_graph_contract_check.py`，并通过 `_contract_manifest.json` 约束：

- 后端输出必须覆盖契约（backend_truth ⊇ contract）
- 前端消费必须不越界（frontend_expect ⊆ contract）

但该检查目前仅能在本地手动运行。为避免契约漂移在 PR 合并后才暴露，需要在 GitHub Actions 中加入门禁：**每次 PR / push main 自动执行跨仓契约检查**。

---

## 范围

- [ ] 新增一个 GitHub Actions workflow（建议命名：`tech-graph-contract.yml` 或并入现有 `tech-graph.yml`）用于运行跨仓契约检查
- [ ] CI 中同时 checkout：
  - 后端仓（当前仓）
  - 前端仓 `ai-ink-brain/`（作为第二仓 checkout 到固定相对路径，满足脚本静态扫描）
- [ ] 在 CI 中运行：
  - `python tools/tech_graph_contract_check.py`
- [ ] 约束：CI 只做**静态检查（键名集合/枚举）**，不运行前后端服务、不进行 e2e

## 非范围

- 不在 CI 中做运行态 SSE 回放/端到端 UI 测试
- 不引入外部私有依赖（除非明确需要并补充 secret 管理方案）
- 不修改契约脚本的规则语义（除非 CI 环境暴露出路径/兼容性问题）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 现有 CI（manifest） | `.github/workflows/tech-graph.yml` |
| 契约真值 | `docs/_tech_graph/_contract_manifest.json` |
| 校验脚本 | `tools/tech_graph_contract_check.py` |
| E2E 边界图 | `docs/_tech_graph/15_e2e_boundary.ai.md`（说明跨仓关系） |
| 前端仓 | `../ai-ink-brain/`（本地约定路径；CI 需模拟出相同相对路径结构） |

---

## 设计要点（CI checkout 策略）

> 关键点：`tech_graph_contract_check.py` 会静态扫描前端文件，且历史上使用过相对路径（`../ai-ink-brain/...`）。  
> 因此 CI 需要把前端仓 checkout 到一个固定位置，并确保脚本能找到它。

推荐两种做法（二选一）：

### 方案 A（推荐）：把前端 checkout 到 `../ai-ink-brain` 可达的位置
- 在 Actions workspace 下：
  - 先 checkout 后端到默认目录（例如 `ai-ink-brain-api-python/`）
  - 再 checkout 前端到同级目录 `ai-ink-brain/`
- 好处：与本地路径习惯一致，脚本无需改动
- 风险：需要明确 `working-directory` 与 checkout `path` 组合

### 方案 B：在 CI 里给脚本提供前端路径参数（脚本增强）
- 给 `tech_graph_contract_check.py` 增加 CLI 参数（例如 `--frontend-root`）
- CI 里用 `--frontend-root` 指向 checkout 的目录
- 好处：更稳健、可支持不同 repo 命名/路径
- 代价：需要修改脚本 + 更新文档；属于本任务可选扩展

---

## 验收标准

- [ ] 新增/更新 workflow 后，在 PR 中自动执行跨仓契约检查
- [ ] 正向：当前 `main`/目标分支能在 CI 上输出 `OK`
- [ ] 负向：当契约缺失必需键（例如删掉 `done.data.request_id`）时，CI 必须失败并提示缺失项
- [ ] 负向：当前端消费越界字段（例如临时写入 `data.nonexistent_key`）时，CI 必须失败并提示越界字段
- [ ] 文档更新：在 `docs/_tech_graph/15_e2e_boundary.ai.md` 或 `99_spec.md`（二选一）补一句说明“跨仓契约门禁已接入 CI”，并给出 workflow 路径

---

## 手动测试用例（必须执行）

> 这些用例可以在本地用 `act`（可选）或直接通过 PR 触发验证。

### 用例 1：正向（baseline OK）
- 操作：提交 workflow 后开 PR
- 期望：Actions job 成功，日志包含 `OK: cross-repo contract check passed`

### 用例 2：负向（contract 缺失）
- 操作：临时从 `docs/_tech_graph/_contract_manifest.json` 删除 `request_id`（或其他必需键），推送到 PR 分支
- 期望：Actions job 失败，并明确指出 `contract.sse.done.data_keys must include ... request_id`
- 回滚：恢复契约后应恢复 OK

### 用例 3：负向（前端越界读取）
- 操作：在前端仓（PR 分支或临时 patch）加入越界读取（`data.nonexistent_key`），推送
- 期望：Actions job 失败并指出 forbidden key
- 回滚：撤销越界读取后恢复 OK

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `.github/workflows/tech-graph-contract.yml`（新增）、`docs/_tech_graph/15_e2e_boundary.ai.md`（补充说明） |
| checkout 策略 | 方案 A：后端 checkout 到 `ai-ink-brain-api-python/`，前端 checkout 到同级 `ai-ink-brain/`，保持 `../ai-ink-brain/...` 相对路径可达 |
| 关键限制 | CI 环境必须能拿到前端仓源码（public repo / 或配置 token） |
| 图谱变更点 | `docs/_tech_graph/15_e2e_boundary.ai.md`（补充 CI 门禁说明） |

### 已落地

- workflow：`.github/workflows/tech-graph-contract.yml`（`pull_request` + `push(main)` 触发）
- job：`contract_check` 会执行 `python tools/tech_graph_contract_check.py`
