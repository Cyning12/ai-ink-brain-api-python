# 系列时间轴

> **append-only**；与 [`SERIES_MANIFEST.yaml`](SERIES_MANIFEST.yaml) 同步维护。  
> **证据冻结点**：main `@ f53327a`（含 #106 + #107）

| 日期 | 事件 | 卷 | 证据 |
| --- | --- | --- | --- |
| 2026-06-03 | P0 Graph task 草案 · 22 R1 有阻塞 | vol-02 | task `chatbi_graph_p0_foundation_v1` |
| 2026-06-03 | 10 回填 §10 冻结 · 22 R2 零阻塞 · 人签 human_gate | vol-02 | `ab4ca03` |
| 2026-06-03 | P0 30 实现 · 40 自检 · **50 pass-with-notes**（main 基线 10 测仍红） | vol-02 | `b43ae3e` · `reinspect_chatbi_graph_p0_foundation_v1_20260603_v1` · **选 B** |
| 2026-06-04 | 基线闸 Harness 10→22→30→40→50 | vol-01 | invokes `chatbi_baseline_merge_gate_v1/` |
| 2026-06-04 | PR **#106** 合入 main（v3 测环境 + contract `label`） | vol-01 | merge `26e1c45` |
| 2026-06-04 | P0 rebase on #106 · PR **#107** 首跑 **drift_check** 红 | vol-02 | Q-8 端点未入 `99_spec.md` 索引 |
| 2026-06-04 | #107 补 drift 叙述层 + `02_version` · **合入 main** | vol-02 | merge `f53327a` · 全集 **287 passed** |
| 2026-06-04 | 展示系列骨架落盘 | — | commit `ea39959` |
| 2026-06-04 | vol-01 正文 compiled（01–06） | vol-01 | showcase 分支 3 commits |
| 2026-06-04 | vol-02 正文 compiled（01–07） | vol-02 | showcase 分支 3 commits |
| 2026-06-04 | vol-90 面试短稿 **v0.10** | vol-90 | 01 电梯 · 02 STAR · 03 演示脚本 |
| 2026-06-04 | vol-03 横切正文 compiled（01–05） | vol-03 | Harness 落盘 · required · CI 三门 · Agent playbook · 教训 |
