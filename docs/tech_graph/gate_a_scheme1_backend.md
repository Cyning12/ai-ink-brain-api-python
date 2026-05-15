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
- **tech-graph（CI）留痕**：workflow run（job `manifest_check`）— [GitHub Actions run / job](https://github.com/Cyning12/ai-ink-brain-api-python/actions/runs/25897412659/job/76113312774)（merge PR #25；日志头 **checkout `fb0b54c…`**；**job 总时长约 5s**；其中 step **「Tech graph graph.json drift check」** UI 约 **1s**、日志内脚本执行约 **0s～1s** 量级属正常取整）。Runner：`ubuntu-latest`，Python **3.11.15**（hostedtoolcache）。
- **Token 附录工具（本地/CI）**：`python tools/tech_graph_token_estimate.py`（默认 Markdown；`--json` 一行）；与 `graph_export` **同输入根**；CI 见 `tech-graph` workflow step **「Tech graph token estimate (Gate A appendix)」**。
- **Token 粗估 `--json` 快照（本地 cwd=本仓根，2026-05-15；与 `docs/_tech_graph/graph.json` 已提交版一致）**：

```json
{"schema": "tech_graph_token_estimate_v1", "input_root": "docs/_tech_graph", "graph_json": "docs/_tech_graph/graph.json", "A": {"bytes_utf8": 20224, "chars": 20224, "heuristic_tokens": 5056}, "B": {"bytes_utf8": 20953, "chars": 20105, "heuristic_tokens": 5026}, "ratio_B_per_A": {"bytes_utf8": 1.036, "heuristic_tokens": 0.9941}, "rules": {"heuristic_tokens": "chars//4, min 1; not official tiktoken"}}
```
- 性能对比验收完成后，在本小节追加 **对比分支/commit、跑数环境、原始日志或导出表格路径**（本小节已含 §3.1 首批后端采样，可继续叠代）。

### 术语消歧：**代号** A/B（对比对象）≠ **计时** A/B（跑数环境）

| 名称 | 含义 |
| --- | --- |
| **§2 代号 A** | **消费侧输入**为静态 **`graph.json`**（浏览器里多为 `JSON.parse` 成对象）。 |
| **§2 代号 B** | **消费侧输入**为与 A **同拓扑**的 **Mermaid 源字符串**（旧链路：词法 / 解析 / layout）。 |
| **上文「计时 A」** | **维护者本机**终端 `/usr/bin/time` 粗测（与 JSON/Mermaid 代号无关）。 |
| **上文「计时 B」** | **Agent 批跑** N=10 的 P50/P95（与 JSON/Mermaid 代号无关）。 |

**结论句怎么读**：父文档 **§3「指标」**表里写的 **「A（JSON）/ B（Mermaid）」** 一律指 **§2 对比对象**；不要把「计时 A/B」误当成 Mermaid。

### 第三步（固定取样）— 后端视角结论

- **已满足（后端子集 / §3.1）**：「中档」= 与仓内 **`docs/_tech_graph/*.ai.md`**（解析器跳过 `99_*`）同拓扑；与已提交 **`docs/_tech_graph/graph.json`** 对齐（当前体量见下表 **字节 / nodes / edges**）。即：**在只评「导出/校验/pytest/CI 步」时，第三步要求的固定样本已成立**。
- **尚未完成（全链路 A vs B）**：父文档 **§2** 要求 **B** 为与 A **拓扑等价**的 Mermaid 源串；该 **B 的固定版本** 与浏览器侧 **§3.2** 指标仍待 **`ai-ink-brain`** 与（可选）micro-benchmark 定稿。全表结论与 **§5 阈值**判定须等 **§3.2 + 总对比表**补齐。

### 后端 §3.1 采样记录（`gate_a_scheme1_perf_compare_backend_detail.md` §9）

**产物体量（与仓内已提交 `graph.json` 一致；本地文档落盘时可随 bump 更新一行计数）**

| 项 | 值 |
| --- | --- |
| `graph.json` 字节 | 20224 |
| nodes / edges | 134 / 180 |
| CI 对应 commit | `fb0b54c`（merge PR #25，见 Actions 日志） |

**CI（已回填）**：见上节 **tech-graph** run 链接；merge **commit `fb0b54c`**（以 Actions checkout 为准）。同一 run 内 step **「Tech graph graph.json drift check」** 约 **1s**（与 UI 一致）。

**计时 A — 维护者本机（终端粗测，N=1～2，cwd=本仓根）**

| 指标 | real（s） | 备注 |
| --- | --- | --- |
| `python tools/tech_graph_graph_export.py` | ~0.12 | 单次 |
| `python tools/tech_graph_graph_export.py --check` | ~0.12 / ~0.11 | 两次 |
| `pytest tests/test_tech_graph_graph_export.py -q`（整进程 `/usr/bin/time`） | ~0.45 | pytest 内部约 0.01s 为收集内耗时 |

**计时 B — N=10 批跑（Agent：`/usr/bin/time -p`；输入为 `docs/_tech_graph` 同内容 `.ai.md` 复制至临时目录，**不写仓内** `graph.json`；跑完目录已删）**

| 指标 | P50 (s) | P95 (s) | min–max (s) |
| --- | --- | --- | --- |
| 导出（写临时 `graph.json`） | 0.030 | 0.035 | 0.030–0.040 |
| `--check`（对临时产物） | 0.030 | 0.030 | 0.030–0.030 |
| `pytest tests/test_tech_graph_graph_export.py`（整进程） | 0.390 | 0.400 | 0.390–0.400 |

> 注：上表 N=10 在本地开发提交 **`42a6419`** 上跑数；与上表 **CI `fb0b54c`** 若不一致，以 **CI commit** 为线上真值，**P50/P95** 可在同 commit 上重跑覆盖。

**说明**：「**计时 A**（本机粗测）」与「**计时 B**（Agent N=10）」两列的秒级差异来自机器负载、`time` 粒度与冷启动等，**与 §2 代号 A/B（JSON vs Mermaid）不是同一概念**。主结论应写清以哪列为主真值（建议：**本机同 commit 再跑 N≥7** 与 Agent 表并列）；Agent 批跑用于 **同口径 P50/P95** 的辅助记录。

## 结论

- **是否进入方案2 筹备**：**暂缓**。在 **「静态 `graph.json` vs 旧 Mermaid」性能对比验收** 形成书面结论（通过/不通过/附条件通过）之前，不启动方案2 的实质性排期与接口冻结讨论。  
- **理由**：方案1 已满足「确定性解析 + 无漂移门禁」；下一阶段风险从「正确性」转向「体验与成本」（首屏、交互、包体、内存、CI 耗时）。若无基线对比，易在方案2 中重复投入或选错优化面。

---

## 下一阶段：静态 `graph.json` vs 旧 Mermaid — **初步对比方案**（v0）

> **边界**：**生成与校验成本** 在本仓（`ai-ink-brain-api-python`）完成；**页面首屏 / 交互 / 包体 / 浏览器内解析** 在 `ai-ink-brain` 完成（见 **§3.2**）。全链路书面结论仍只维护 **本文件一处**；`ai-ink-brain` 侧须在 task 中链回本节并完成 §3.2 后，在 **「仓库或 CI 快照引用」** 回链数据路径（见下 **链回要求**）。

**后端先行（SOP）**：§3.1 采集的逐步说明、**failure_paths** 与记录模板见 [`gate_a_scheme1_perf_compare_backend_detail.md`](./gate_a_scheme1_perf_compare_backend_detail.md)。前端 §3.2 建议复用该文档的统计口径与表格结构；全链路结论句仍只写回本文件 **「结论」** 与 **§6**。  
**链回要求**：`ai-ink-brain` 侧 graph.json / 闸口 A 任务须在正文或依赖表中 **显式链回** 本文件及上列 SOP（避免「父文档写了、子仓 task 未写」的双轨漂移）。

### 1. 目标与问题陈述

- **目标**：在同等内容规模下，对比 **消费静态 `graph.json`** 与 **消费 `.ai.md` 内 Mermaid 文本（旧链路）** 的关键性能指标，判断是否值得在方案2 继续加码「运行时图能力」或应优先做「静态分发 + 轻渲染」。  
- **非目标**：不在本阶段改业务功能；不将对比结果写入 `freeze_id` 行；不替代契约门禁与 `--check` 语义。

### 2. 对比对象（须固定版本）

| 代号 | 输入 | 说明 |
| --- | --- | --- |
| A | `docs/_tech_graph/graph.json`（已提交或与 `--check` 一致产物） | 静态 JSON；解析器为 `JSON.parse` 类实现（具体以前端/工具为准） |
| B | 与 A **拓扑等价** 的 Mermaid 源（推荐：由同一批 `.ai.md` fence 拼接或选取单文件最大子图） | 旧链路：Mermaid 词法/语法解析 + layout |

**与 `docs/_tech_graph/` 的关系（消歧）**：该目录里**同时**有 **`.ai.md`（内含 Mermaid fence）** 和产物 **`graph.json`**。**代号 A** = 消费 **`graph.json` 这一条链路**；**代号 B** = 消费 **从上述 `.ai.md` 抽出来的 Mermaid 源文**（词法 + layout 那条链路），**不是**把「整个目录」当成 B。

**母集合（与 `graph.json` 同源）**：`tools/tech_graph_graph_export.py` 与 `tools/tech_graph_token_estimate.py` 使用**同一扫描规则**——**`docs/_tech_graph/*.ai.md`**，**跳过 `99_*.md`**（与 `99_mermaid_protocol` 等规约一致）。**`graph.json` 不是**「所有 `.md` 原文的拼接」，而是从这些 `*.ai.md` 的 **Mermaid fence** 里解析出的 **节点/边** 再序列化得到的 JSON。

**代号 B 的「默认固定样本」（本仓附录已采纳）**：在上述同一母集合下，**按文件名排序**，将每个文件内 **所有** Mermaid 围栏（与导出脚本相同的 fence 正则）正文用空行拼接，得到 **一条 Mermaid 语料总串** —— 实现为 **`python tools/tech_graph_token_estimate.py`**（与 `--check` 同 commit 的 `graph.json` 对照）。若主对比表要改用 **「仅最大单文件 fence」** 或 **「不含 classDiagram」** 等其它 B，须在对比文档 **显式另起一行声明**，并与附录结果**分列**，不得 silent 混用。

**等价性**：以「节点数、边数、标签字符量」与一次人工 spot-check 为最低门槛；若 A/B 规模不一致，对比结果仅作附录，不得作为主结论。

### 3. 指标（建议最小集）

| 维度 | A（JSON） | B（Mermaid） | 采集建议 |
| --- | --- | --- | --- |
| **载荷体积** | HTTP/磁盘字节数；gzip/br 后字节数 | 同上 | Network 面板或构建产物统计 |
| **冷解析耗时** | 自拿到字符串到结构化对象就绪 | 自拿到字符串到 AST/中间结构就绪（若不可测则记「首 layout 前」） | `performance.now()`，重复 ≥30 次取 **P50/P95** |
| **首屏/首帧**（以前端为准） | 首节点/首边可见或可交互时间 | 同上 | Lighthouse 或自定义 mark；同一 throttle |
| **内存峰值**（可选） | DevTools heap snapshot 差分或采样 | 同上 | 大样本图再开；注意 GC 噪声 |
| **CI / 构建**（可选） | 若引入前端依赖：对 build 时长影响 | Mermaid 相关 chunk 体积与 tree-shaking | 同一 CI runner 标签下对比 |
| **Agent / LM context（可选）** | 同一提示骨架下，嵌入 **整份 `graph.json` 文本** 的 **估算 token** | 同一骨架下嵌入 **§2 代号 B 的 Mermaid 源文** 的 **估算 token** | 须声明 tokenizer 规则（如某 `tiktoken` 编码器或「UTF-8 字节 + 换算假设」），避免跨模型硬比绝对值。与 [`改进方向.md`](../../../docs/tech_graph/改进方向.md)「极低 token」叙事对齐；**闸口 B（方案2 后）** 已把 Agent **token/轮次** 列为正式对比项——闸口 A 阶段可将本行作为 **附录**，不阻塞 §3.1 后端子表。 |

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
# 与 scheme1 子仓 task 一致：须能调用「与后端同语义」的导出/校验（Python 3.11+）。
# 工作区聚合布局（task §7 模式 B）示例 — 路径以实际 clone 为准：
# python ../ai-ink-brain-api-python/tools/tech_graph_graph_export.py --check
#
# 单仓仅 checkout 前端时（task §7 模式 A）：须在 CI 中额外 checkout 后端到固定相对路径，
# 再对上述路径执行 --check；勿使用已废弃占位名 export_graph_json.py。
#
# 若团队已在本仓 package.json 增加封装脚本（如 pnpm tech-graph:graph-check），
# 以该仓 task「实现备忘」中的真值命令为准，本段不替代子仓定稿。

# 构建产物体积粗测（§3.2 包体 / chunk 分析；与 graph 校验独立）
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
| 2026-05-15 | 入库 CI run URL（tech-graph / `manifest_check` / merge `fb0b54c`）；增「术语消歧：代号 A/B vs 计时 A/B」 |
| 2026-05-15 | §2 增补「B vs `docs/_tech_graph`」消歧；§3 增可选 **Agent/LM token** 维度（与规划、闸口 B 对齐） |
| 2026-05-15 | 落地 `tools/tech_graph_token_estimate.py`、pytest、`tech-graph` CI step；快照区链命令 |
| 2026-05-15 | 「仓库或 CI 快照引用」回填 `tech_graph_token_estimate.py --json` 一行（本地 2026-05-15） |
| 2026-05-15 | §2：写明 `graph.json` 与 `*.ai.md` 母集合关系；**默认 B** 与 `tech_graph_token_estimate` 对齐 |
