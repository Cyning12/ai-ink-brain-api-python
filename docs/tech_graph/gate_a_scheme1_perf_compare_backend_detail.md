# 闸口 A 性能对比 — **后端子集**详细执行说明（SOP）

> **父文档**：[`gate_a_scheme1_backend.md`](./gate_a_scheme1_backend.md) 自 **「初步对比方案（v0）」**（约 L48 起）  
> **职责边界**：仅覆盖 **生成 / 校验 / CI / pytest** 侧指标（父文档 **§3.1**）；**不**覆盖浏览器运行时、Mermaid 消费链路与包体（父文档 **§3.2**，待后端子表通过后再由前端仓复用本文件的**统计口径与表格结构**）。  
> **全链路结论**：仍以父文档 **「结论」** 与 **§6 交付物** 为唯一落点；本文件产出 **原始数据路径** 须在父文档 **「仓库或 CI 快照引用」** 回链。

---

## 1. 固定真值与版本

| 项 | 值 / 说明 |
| --- | --- |
| `freeze_id` | 与父文档、导出脚本一致：`TECH_GRAPH_S1_FREEZE_20260514_V1_1_3`（bump 时双仓同改，**不**写入性能原始表） |
| 输入根目录 | 默认 `docs/_tech_graph`（`*.ai.md`，解析器跳过 `99_*`） |
| 输出文件 | 默认 `docs/_tech_graph/graph.json` |
| 导出脚本 | `tools/tech_graph_graph_export.py` |
| 契约门禁（并行互补） | `tools/tech_graph_contract_check.py`（**禁止**与导出脚本合并逻辑） |
| Python | 与 CI 对齐：**3.11**（见 `.github/workflows/tech-graph.yml`） |
| 工作目录 | **本仓根**（下文命令默认 `cwd = ai-ink-brain-api-python`） |

**样本档位（与父文档 §4 对齐）**

| 档位 | 用途 |
| --- | --- |
| **中（默认）** | 与仓库当前 `docs/_tech_graph` 已提交内容一致；主结论必须包含本档 |
| **小** | 临时目录仅含少量 `.ai.md` fence（用于回归「小图」导出是否线性）；可选 |
| **超大（可选）** | 仅当需要暴露热点时再构造；须在记录中声明「非生产目录」 |

---

## 2. 指标与父文档映射

| 本 SOP 小节 | 父文档 §3.1 子指标 | 通过含义（后端视角） |
| --- | --- | --- |
| §3 | 导出 wall time | 有 **P50/P95**（或单次 `time` + 声明仅作粗测）；与 `--check` 量级关系可解释 |
| §4 | `--check` 纯校验 | 同环境下重复 N 次；失败时按 **§8** 分类而非记为性能差 |
| §5 | 产物体积 | 字节数 + `nodes`/`edges` 计数；变更 `.ai.md` 后体积变化可解释 |
| §6 | 单测成本 | `pytest tests/test_tech_graph_graph_export.py` 耗时稳定可引用 |
| §7 | CI step 耗时 | `tech-graph` workflow 中 **「Tech graph graph.json drift check」** step 的 Actions Duration |

**说明**：父文档 **§3** 全表含前端维度；**主结论**仍由父文档汇总。本 SOP 的目标是证明 **「生成侧不是全链路瓶颈」** 或标出 **导出热点**。

---

## 3. 子指标 SOP：导出 wall time

### 3.1 前置检查

```bash
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
pytest tests/test_tech_graph_graph_export.py -q
```

任一步失败：**不得**进入性能读数（先修解析/漂移/测试）。

### 3.2 正式导出（写盘）

```bash
# 单次粗测（bash）
/usr/bin/time -p python tools/tech_graph_graph_export.py
```

- **记录字段**：`real` / `user` / `sys`；**commit 短 hash**；**日期（UTC 或本地 + 时区）**；**机器型号或 CI 标识**（本地写「laptop/workstation」即可）。  
- **推荐**：对同一 `commit` 重复 **≥7** 次（若每次 <1s 可增至 30），丢弃第 1 次或单独标注 **cold start**，报告 **P50/P95**（可用简单脚本或粘贴到表格手算）。

### 3.3 与 `--check` 的关系（可选对照）

假设：`--check` 路径会再生成一遍语义等价 payload 但不写盘，耗时通常与「纯导出」同量级或略低/高（I/O 差异）。可跑：

```bash
/usr/bin/time -p python tools/tech_graph_graph_export.py --check
```

在记录中写一句：**export 与 check 的比值**（例如 `check/export ≈ 0.9`），避免误读为「2× 必成立」。

---

## 4. 子指标 SOP：`--check` 纯校验

```bash
/usr/bin/time -p python tools/tech_graph_graph_export.py --check
echo $?
```

- **期望退出码**：`0`。  
- **非 0**：见 **§8 failure_paths**，该次计时**不计入**性能对比，记入「门禁失败事件」。

---

## 5. 子指标 SOP：产物体积

```bash
wc -c docs/_tech_graph/graph.json
wc -l docs/_tech_graph/graph.json
python -c "import json; p='docs/_tech_graph/graph.json'; g=json.load(open(p,encoding='utf-8')); print('nodes', len(g.get('nodes',[])), 'edges', len(g.get('edges',[])))"
```

- **gzip（可选）**：`gzip -kc docs/_tech_graph/graph.json | wc -c`（或 `python -m gzip` 管道），与父文档 §3「载荷体积」对齐时注明 **gzip 层级**。  
- **变更对照**：若某 PR 修改了 `.ai.md`，在同一表格中增加 **Δbytes / Δedges**。

---

## 6. 子指标 SOP：单测成本

```bash
/usr/bin/time -p pytest tests/test_tech_graph_graph_export.py -q
```

- 与默认 `pytest` 全量区分：本 SOP **仅**引用该文件。  
- CI 中若未单独拆 step，可在 PR 描述中注明「仅本地 `time`」或从 **pytest job 日志**截取该文件相关行（若可解析）。

---

## 7. 子指标 SOP：CI step 耗时

1. 打开 GitHub Actions → workflow **`tech-graph`** → 目标 run。  
2. 记录 **Job** 名称（当前为 `manifest_check`）、镜像 **`ubuntu-latest`**、run **日期**。  
3. 展开 step **「Tech graph graph.json drift check」**，记录 **Duration**（秒）。  
4. 与「合并前基线」对比时，须 **同一 workflow 文件版本**（或注明 YAML 变更日期），否则对比无效。

---

## 8. failure_paths（后端采集）

| ID | 触发条件 | 系统行为 / 退出码 | 可重试性 | 记录到性能表？ |
| --- | --- | --- | --- | --- |
| BE-FP-1 | 输入目录不存在；`.ai.md` Mermaid 子集解析失败；写盘 OSError | 脚本 **2**（stderr 含 `FP-1` / `FP-4`） | 修源文件/环境后重试 | **否** |
| BE-FP-2a | `graph.json` 缺失或 JSON 无效或缺 `generated_at` | **`--check`** 退出 **3** | 先跑无 `--check` 导出并提交后再检 | **否** |
| BE-FP-2b | 再生成与已提交对象语义不一致 | **`--check`** 退出 **4**（stderr 差异摘要） | 同 PR 内重生成并提交 | **否** |
| BE-FP-env | 本机 Python 版本 ≠ 3.11、路径不在仓根、磁盘满 | 依具体命令失败 | 修正环境 | **否** |
| BE-OK | 上述均无；`time`/`pytest` 完成 | 退出码 0 | — | **是**，写入 §9 表 |

**用户可见类型**：后端阶段全部为 **维护者/CI 可见**；不映射到 API 错误码。

---

## 9. 记录模板（建议直接粘贴到 PR 或 `docs/tech_graph/` 附录）

### 9.1 元数据行

| 字段 | 示例 |
| --- | --- |
| commit | `abc1234` |
| 日期 | `2026-05-15` |
| 环境 | `macOS 14 / Python 3.11.9` 或 `GitHub Actions ubuntu-latest @ run 12345` |
| 样本档位 | `中（仓库默认 _tech_graph）` |

### 9.2 后端子表（§3.1 落地）

| 指标 | 单位 | N 次 / 备注 | P50 | P95 | 原始日志路径 |
| --- | --- | --- | --- | --- | --- |
| 导出 wall time | s | | | | |
| `--check` wall time | s | | | | |
| `graph.json` 字节 | B | 单次 | — | — | |
| gzip 字节（可选） | B | | — | — | |
| nodes 计数 | int | | — | — | |
| edges 计数 | int | | — | — | |
| pytest `test_tech_graph_graph_export` | s | | | | |
| CI step「Tech graph graph.json drift check」 | s | 1 run | — | — | Actions URL |

---

## 10. 与父文档 §5「通过阈值」的关系

- **§5 阈值**针对 **A vs B 全链路**（含前端解析与首帧），**不**直接套用本后端子表数值。  
- 本后端子表的用途：在总结论中写清 **「生成/校验占用相对全链路可忽略 / 不可忽略」**，并决定是否需要在导出脚本侧做 **profiling**（本 SOP 不强制 profiling，若做请另附 `cProfile` 路径）。

---

## 11. 前端复用（占位）

前端执行 **§3.2** 时建议新建 **`ai-ink-brain/docs/tech_graph/`（或该仓 `_tech_graph` 迁移后路径）** 下的对偶文档，**复用**：

- §9 **表格列**（把 CI step 换成 `quality` 中与 graph 相关 step）；  
- §4「固定环境 / 固定样本 / P50-P95」方法；  
- 父文档 **§2 等价性** 与 **§5 阈值** 的判定职责。

全链路 **§6 勾选** 仍只在父文档 [`gate_a_scheme1_backend.md`](./gate_a_scheme1_backend.md) 维护。

---

## 12. 依赖链接（相对本仓根）

- `tools/tech_graph_graph_export.py`  
- `tools/tech_graph_contract_check.py`  
- `tests/test_tech_graph_graph_export.py`  
- `.github/workflows/tech-graph.yml`  
- 工作区规划（若需对齐闸口叙事）：`docs/tech_graph/改进方向.md`（工作区根，路径以克隆布局为准）

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-15 | v1：从 `gate_a_scheme1_backend.md` §48 起拆出后端 SOP、failure_paths 与记录模板 |
