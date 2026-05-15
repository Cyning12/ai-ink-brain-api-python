# 闸口 A（方案1）— 后端仓 `ai-ink-brain-api-python`：现状 vs 静态 `graph.json`

> 对应规划：工作区 `docs/tech_graph/改进方向.md` 闸口 A；SPEC：`docs/tech_graph/SPEC/json_graph/scheme_1_graph_json.md`  
> `freeze_id`：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`（与前端 task **同一行**；bump 时双仓同改）

## 闸口状态（人审维护）

| 项 | 状态 |
| --- | --- |
| 合并前 CI（`pytest` / `verify-fast` / `tech-graph` / `tech-graph-contract` 等） | **已通过**（远程 PR 全绿、无报错；具体 run id 见 PR 描述留痕） |
| 方案1 基建（导出、`--check`、单测、与契约门禁并行） | **已落地** |
| 下一阶段 | **静态 `graph.json` 与旧 Mermaid 消费链路的性能对比验收**（见下文「初步对比方案」）；**验收结论落地后再启动方案2 筹备** |

## 指标（最低集）

| 指标 | 方法 / 观察 |
| --- | --- |
| 解析正确性 | `pytest tests/test_tech_graph_graph_export.py`（golden、空图、FP-1 解析失败）；与 `docs/_tech_graph/*.ai.md` 拓扑子集对齐 |
| `graph.json` 体量 | `wc -l docs/_tech_graph/graph.json`；`nodes` / `edges` 计数见文件内数组 |
| 维护成本 | 变更 `.ai.md` 后须同 PR 运行 `python tools/tech_graph_graph_export.py` 并提交 `graph.json` |
| CI 增量 | `tech-graph` workflow 增加 `tech_graph_graph_export.py --check`（秒级；失败率与耗时在 GitHub Actions run 上观察） |

## 复现命令（cwd = 本仓根）

```bash
# 1) 契约门禁（与 graph 导出并行互补；跨仓真值见 tech-graph-contract workflow）
python tools/tech_graph_contract_check.py

# 2) 架构依赖图门禁（与契约脚本独立；顺序：先 contract 再 graph 便于本地排障）
python tools/tech_graph_graph_export.py --check

# 3) pytest 子集（解析 / 空图 / golden）
pytest tests/test_tech_graph_graph_export.py -q
```

## 仓库或 CI 快照引用

- 合入 PR 请在 PR 描述中填写 **短 commit hash** 与 **Actions run id**（**不**写入各仓 task 的 `freeze_id` 行，以免机械比对漂移）。
- 性能对比验收完成后，在本小节追加 **对比分支/commit、跑数环境、原始日志或导出表格路径**。

## 结论

- **是否进入方案2 筹备**：**暂缓**。在 **「静态 `graph.json` vs 旧 Mermaid」性能对比验收** 形成书面结论（通过/不通过/附条件通过）之前，不启动方案2 的实质性排期与接口冻结讨论。  
- **理由**：方案1 已满足「确定性解析 + 无漂移门禁」；下一阶段风险从「正确性」转向「体验与成本」（首屏、交互、包体、内存、CI 耗时）。若无基线对比，易在方案2 中重复投入或选错优化面。

---

## 下一阶段：静态 `graph.json` vs 旧 Mermaid — **初步对比方案**（v0）

> **边界**：**生成与校验成本** 在本仓（`ai-ink-brain-api-python`）完成；**页面首屏 / 交互 / 包体 / 浏览器内解析** 在 `ai-ink-brain` 完成（见 **§3.2**）。全链路书面结论仍只维护 **本文件一处**，前端 task 已链入本节；执行完毕后须在 **「仓库或 CI 快照引用」** 回链数据路径。

**后端先行（SOP）**：§3.1 采集的逐步说明、**failure_paths** 与记录模板见 [`gate_a_scheme1_perf_compare_backend_detail.md`](./gate_a_scheme1_perf_compare_backend_detail.md)。前端 §3.2 建议复用该文档的统计口径与表格结构；全链路结论句仍只写回本文件 **「结论」** 与 **§6**。

### 1. 目标与问题陈述

- **目标**：在同等内容规模下，对比 **消费静态 `graph.json`** 与 **消费 `.ai.md` 内 Mermaid 文本（旧链路）** 的关键性能指标，判断是否值得在方案2 继续加码「运行时图能力」或应优先做「静态分发 + 轻渲染」。  
- **非目标**：不在本阶段改业务功能；不将对比结果写入 `freeze_id` 行；不替代契约门禁与 `--check` 语义。

### 2. 对比对象（须固定版本）

| 代号 | 输入 | 说明 |
| --- | --- | --- |
| A | `docs/_tech_graph/graph.json`（已提交或与 `--check` 一致产物） | 静态 JSON；解析器为 `JSON.parse` 类实现（具体以前端/工具为准） |
| B | 与 A **拓扑等价** 的 Mermaid 源（推荐：由同一批 `.ai.md` fence 拼接或选取单文件最大子图） | 旧链路：Mermaid 词法/语法解析 + layout |

**等价性**：以「节点数、边数、标签字符量」与一次人工 spot-check 为最低门槛；若 A/B 规模不一致，对比结果仅作附录，不得作为主结论。

### 3. 指标（建议最小集）

| 维度 | A（JSON） | B（Mermaid） | 采集建议 |
| --- | --- | --- | --- |
| **载荷体积** | HTTP/磁盘字节数；gzip/br 后字节数 | 同上 | Network 面板或构建产物统计 |
| **冷解析耗时** | 自拿到字符串到结构化对象就绪 | 自拿到字符串到 AST/中间结构就绪（若不可测则记「首 layout 前」） | `performance.now()`，重复 ≥30 次取 **P50/P95** |
| **首屏/首帧**（以前端为准） | 首节点/首边可见或可交互时间 | 同上 | Lighthouse 或自定义 mark；同一 throttle |
| **内存峰值**（可选） | DevTools heap snapshot 差分或采样 | 同上 | 大样本图再开；注意 GC 噪声 |
| **CI / 构建**（可选） | 若引入前端依赖：对 build 时长影响 | Mermaid 相关 chunk 体积与 tree-shaking | 同一 CI runner 标签下对比 |

### 3.1 后端仓 `ai-ink-brain-api-python`（生成 / 校验 / CI）

| 子指标 | 含义 | 采集方式（cwd = 本仓根） |
| --- | --- | --- |
| 导出 wall time | 自进程启动到写出 `graph.json` 结束 | `time python tools/tech_graph_graph_export.py`（再跑 `--check` 对比是否近似 2× I/O） |
| `--check` 纯校验 | 无写盘 diff 时的失败发现延迟 | `time python tools/tech_graph_graph_export.py --check` |
| 产物体积 | 磁盘字节数 | `wc -c docs/_tech_graph/graph.json`；与 `wc -l` 交叉核对 |
| 单测成本 | 回归解析器与 golden 的耗时 | `time pytest tests/test_tech_graph_graph_export.py -q` |
| CI 步耗时 | `tech-graph` workflow 中含 `--check` 的 step | GitHub Actions 日志中该 step 的 **Duration**；须记录 **runner 镜像标签** 与日期 |

**说明**：上表与上文「指标（最低集）」互补；性能对比主结论仍以 **§3 全表** 为准，后端子表用于证明「生成侧不是瓶颈」或暴露需优化的导出热点。

### 3.2 前端仓 `ai-ink-brain`（运行时消费）

| 子指标 | A（`graph.json` + `JSON.parse` 或等价） | B（Mermaid 运行时：词法 / layout） | 采集建议 |
| --- | --- | --- | --- |
| **JS 包体** | 不包含 `mermaid` 时的相关 chunk 体积 | 引入 `mermaid` 及相关插件后的 chunk | `pnpm build` 后分析 `.next/static/chunks` 或 Next Bundle Analyzer（若已接入）；同一 commit |
| **冷解析** | 从 `fetch`/读盘得到字符串到 **图数据对象** 就绪 | 从字符串到 **首帧 layout 完成前** 的可测点（以 Performance mark 为准） | DevTools **Performance** 录制；`performance.now()` 循环 ≥30 次，报 **P50/P95** |
| **首屏 / LCP** | 含图页面在「仅 JSON 路径」下的 LCP | 同 URL 在「Mermaid 路径」下的 LCP | Lighthouse（同一 throttle、禁用扩展）；或自定义 E2E mark |
| **quality 增量** | `Tech graph graph.json (--check)` step | （无直接对照） | 本仓 `quality` workflow 中该 step 的 Actions Duration；与合并前基线 run 对比 |

**复现命令（cwd = `ai-ink-brain` 仓根）**

```bash
# 本地与 CI 对齐的 graph 校验（Python 3.11+）
pnpm tech-graph:graph-check
# 或：python3 tools/export_graph_json.py --input docs/_tech_graph --output docs/_tech_graph/graph.json --check

# 构建产物体积粗测（示例：按产物目录体积排序，具体以团队惯用分析工具为准）
pnpm build
```

**样本约定**：与 §2 中 A/B **同一拓扑**；若消费页尚未同时接两条链路，可先用 **离线脚本** 在浏览器控制台注入两段字符串跑 micro-benchmark，再补页面级 Lighthouse。**书面结论**须声明采用的是「页级」还是「控制台 micro-benchmark」以免误读。

### 4. 方法与可复现性

1. **固定环境**：浏览器主版本 + CPU 节流档位 + 网络预设（或纯本地 `file://` 仅测解析）；CI 对比须注明 runner 镜像与日期。  
2. **固定样本**：至少 **小（<50 边）**、**中（≈仓库当前量级）** 两档；若有超大图再加一档。  
3. **统计**：每指标每样本重复 N 次，报告 **P50 / P95** 与标准差；剔除冷启动第一次或单独报告「首次」。  
4. **记录**：表格 + 原始 JSON/CSV 路径 + 截图（可选）写入工作区 `docs/tech_graph/` 或 PR 附件，并在上文「仓库或 CI 快照引用」回链。

### 5. 初步通过阈值（待执行前由维护者二选一收紧）

- **默认（宽松）**：在「中」样本下，A 相对 B 在 **P95 解析耗时** 或 **首帧** 至少一项 **不劣于 B 的 120%**，且 **gzip 体积不大于 B 的 150%** → 记为 **「静态链路可接受，可进入方案2」**。  
- **严格**：上述改为 **不劣于 100%**（即全面优于或持平）→ 记为 **「强建议方案2 侧重运行时增强以外的工作」**。  
- 若不达宽松线：结论为 **「附条件通过」**——方案2 须带 **性能 OKR** 与回归用例，而不是直接扩特性。

### 6. 交付物清单（性能验收完成定义）

- [ ] **总对比表**（A/B、§3 各维度、小/中样本、P50/P95）。  
- [ ] **后端子表**（§3.1：导出、`--check`、单测、CI step；附 run id 或本地 `time` 输出路径）。  
- [ ] **前端子表**（§3.2：包体、冷解析、首屏/LCP、quality 增量；注明页级或 micro-benchmark）。  
- [ ] 等价性说明与差异声明（若有）。  
- [ ] 书面结论一句：**可进入方案2 / 暂缓方案2 / 附条件进入**，并与本文件「结论」互链或同步改写。  

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-14 | 闸口状态更新；结论暂缓方案2；增加性能对比初步方案 v0 |
| 2026-05-14 | 性能对比：补全 §3.1 后端子指标与 §3.2 前端消费侧任务书；扩展 §6 交付物 |
