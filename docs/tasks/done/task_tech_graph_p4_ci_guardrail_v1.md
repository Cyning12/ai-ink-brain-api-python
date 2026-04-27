# Task：Tech Graph P4 — CI 门禁（manifest_check 作为必过检查）

> **状态**：done（2026-04-27 验收通过）  
> **范围**：仅后端仓 `ai-ink-brain-api-python`（不改业务代码）  
> **关联图谱**：`docs/_tech_graph/_manifest.json`、`docs/_tech_graph/99_spec.md`  
> **前端依赖**：无

---

## 背景与目标

目前 Tech Graph 的真值与校验已具备：

- `docs/_tech_graph/_manifest.json`（机器可读真值）
- `tools/tech_graph_manifest_check.py`（严格校验）

但若不接入 CI，仍可能出现“本地通过、合并后漂移”的问题。

目标：把 `python tools/tech_graph_manifest_check.py` 变成 **PR/合并门禁**（失败即阻止合并）。

---

## 范围

- [ ] 新增 `.github/workflows/tech-graph.yml`
  - [ ] 触发：`pull_request` + `push`（main 分支）
  - [ ] Python：3.11（与本仓一致）
  - [ ] 步骤：
    - [ ] checkout
    - [ ] setup-python
    - [ ] run `python tools/tech_graph_manifest_check.py`
  - [ ] 约束：不依赖网络、不依赖密钥、不安装额外包（纯标准库执行）

- [ ] 更新 `docs/_tech_graph/99_spec.md`
  - [ ] 增加一条“CI 门禁约束”：任何端点/RPC/表/env/锚点变更必须同步 manifest，否则 CI fail

---

## 非范围

- 不做自动渲染（另见 P5）
- 不要求图谱 `.md/.ai.md` 全量生成（保持增量）

---

## 验收标准

- [ ] 仓库存在 `.github/workflows/tech-graph.yml`
- [ ] PR 提交时 Actions 能运行并展示检查结果
- [ ] 人为制造漂移（例如删掉 manifest 中一个 endpoint）时，CI 必须失败且输出差异

---

## 手动测试用例（必须执行）

### 用例 1：正向（无漂移）
- 操作：
  - 新建分支，保持不改任何端点/RPC/表/env/manifest
  - 提交一个无关改动（例如修改一个任务文档拼写）
- 期望：
  - GitHub Actions 中 `tech-graph` workflow 运行成功
  - 日志包含 `OK: manifest matches code/SQL truth ...`

### 用例 2：负向（制造漂移 → CI 必失败）
- 操作：
  - 在分支上编辑 `docs/_tech_graph/_manifest.json`，删除任意一个 `endpoints[]` 条目（或改错一个 rpc 名称）
  - 提交并推送触发 CI
- 期望：
  - workflow 失败（红）
  - 日志明确指出缺失项（例如 `Endpoints 缺失...` 或 `Supabase RPC ... FAIL`）

### 用例 3：修复（恢复一致 → CI 转绿）
- 操作：
  - 补回缺失 endpoint/rpc
  - 再次提交推送
- 期望：
  - workflow 成功（绿）

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `.github/workflows/tech-graph.yml`、`docs/_tech_graph/99_spec.md` |
| 关键命令 | `python tools/tech_graph_manifest_check.py` |

### 已落地

- `.github/workflows/tech-graph.yml`：在 `pull_request` + `push(main)` 触发，使用 Python 3.11 直接运行 `tools/tech_graph_manifest_check.py`（无网络、无密钥、无额外依赖）。
- `docs/_tech_graph/99_spec.md`：补充“CI 门禁约束”，要求端点/RPC/表/env/anchors 变更必须同步更新 `_manifest.json`，否则 CI 拦截。

