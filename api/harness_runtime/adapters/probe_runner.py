"""harness-probe subprocess 适配（S4 实现 · MVP 零依赖）。

真值：task §5 import 与 probe 边界 · SPEC §10.4.2 · BLOCKERS B7。
禁止：import harness_probe / harness_sdk（运行时）。
唯一生产路径：subprocess + JSON stdout 解析。
"""

# S4: task_validate / verify 在此实现
