# Task：Tech Graph P5 — 自动补全/增量渲染（从 manifest 生成 .ai.md 局部）

> **状态**：done（2026-04-27 验收通过）  
> **范围**：仅后端仓 `ai-ink-brain-api-python`（不改业务代码）  
> **关联图谱**：`docs/_tech_graph/_manifest.json`、`docs/_tech_graph/00_main.ai.md`  
> **前端依赖**：无

---

## 背景与目标

目前已经有“真值 + 校验”，但仍存在维护成本：

- 改端点/锚点后，需要手工同步 `00_main.ai.md`
- 容易出现“manifest 更新了，但 .ai.md 没更新”的滞后

目标：提供一个 **自动补全脚本**，用 manifest 增量渲染 `00_main.ai.md` 的“端点与锚点段落”。

> 约束：只更新可机械生成的部分（端点列表/锚点注释/按需加载链接），不重绘业务子流程。

---

## 范围

- [ ] 新增 `tools/tech_graph_render_ai.py`
  - [ ] 输入：`docs/_tech_graph/_manifest.json`
  - [ ] 输出：增量更新 `docs/_tech_graph/00_main.ai.md`
  - [ ] 渲染策略：
    - [ ] 在 `00_main.ai.md` 中引入一个可识别的区块标记，例如：
      - `<!-- AUTO:ENDPOINTS BEGIN -->` ... `<!-- AUTO:ENDPOINTS END -->`
    - [ ] 脚本仅替换该区块内容，其余手写内容保持不变（减少 diff）
  - [ ] 幂等：多次运行输出一致

- [ ] 更新 `tools/tech_graph_manifest_check.py`（可选）
  - [ ] 增加提示：当校验通过但 `00_main.ai.md` 未同步时，给出“建议运行 render 脚本”的提示（不强制失败，避免过度耦合）

---

## 非范围

- 不自动生成 `10~15_flow_*.ai.md`（这些仍以人工维护为主）
- 不修改 Mermaid 拓扑协议

---

## 验收标准

- [ ] `python tools/tech_graph_render_ai.py` 能成功运行并只改动 `00_main.ai.md` 的 auto 区块
- [ ] 改一个 endpoint 后（`api/index.py`），按顺序执行：
  1) 更新 manifest  
  2) 运行 render  
  3) `python tools/tech_graph_manifest_check.py` 仍为 OK  
  结果：`00_main.ai.md` 对应端点块自动更新

---

## 手动测试用例（必须执行）

> ✅ 已执行：用例 1-3 全部通过（2026-04-27）。

### 用例 1：幂等（重复运行无额外 diff）
- 操作：
  - 连续运行两次：`python tools/tech_graph_render_ai.py`
  - 对比第二次运行前后 `git diff`
- 期望：
  - 第二次运行不产生任何 diff（脚本幂等）

### 用例 2：负向（手工破坏 auto 区块 → render 可修复）
- 操作：
  - 手工编辑 `docs/_tech_graph/00_main.ai.md` 的 auto 区块内容（乱序/删行）
  - 运行 `python tools/tech_graph_render_ai.py`
- 期望：
  - auto 区块被恢复为与 manifest 一致的内容
  - 非 auto 区块保持不变（最小 diff）

### 用例 3：端点变更链路（truth→manifest→render）
- 操作：
  - 在 `api/index.py` 新增一个测试端点（或在测试分支临时改名一个端点路径）
  - 更新 `docs/_tech_graph/_manifest.json` 同步端点（保持校验 OK）
  - 运行 render，观察 `00_main.ai.md` auto 区块更新
  - 运行 `python tools/tech_graph_manifest_check.py`
- 期望：
  - render 更新 `00_main.ai.md` 端点段落
  - manifest_check 仍为 OK

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `tools/tech_graph_render_ai.py`、`docs/_tech_graph/00_main.ai.md`、（可选）`tools/tech_graph_manifest_check.py` |
| 设计取舍 | 为什么采用区块替换而不是全量生成 |

### 已落地

- `docs/_tech_graph/00_main.ai.md`：新增 auto 区块标记 `<!-- AUTO:ENDPOINTS_AND_ANCHORS BEGIN -->` / `<!-- AUTO:ENDPOINTS_AND_ANCHORS END -->`。
- `tools/tech_graph_render_ai.py`：从 `docs/_tech_graph/_manifest.json` 渲染端点与 anchors，并 **只替换** auto 区块内容（其余手写内容不动）；多次运行幂等（无额外 diff）。
- `tools/tech_graph_manifest_check.py`（可选项已做）：当 manifest 校验通过且检测到 auto 标记存在时，输出提示建议运行 render（不强制失败，避免过度耦合）。

### 设计取舍

- 采用“区块替换”而不是全量生成：把“可机械生成的真值段落”与“人工维护的业务子流程/拓扑图”解耦，减少无关 diff，避免误伤手写结构，同时保证自动段落可被一键修复。

