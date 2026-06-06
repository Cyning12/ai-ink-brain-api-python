# `.claude/agents/` · Harness 子角色（docs-noise 治理线）

> **用途**：Claude Code **Lead 串行 spawn**；非 Cursor `Task()`。  
> **MANIFEST**：`docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`  
> **禁止**：内置 Explore/Plan 裸用（不读 CLAUDE.md/读序）

| 文件 | 帽 | 典型 Round |
| --- | --- | --- |
| `harness-10-requirements.md` | 10 | T0 写 task |
| `harness-explore-l0.md` | explore | T2b 差分 |
| `harness-22-audit.md` | 22 | T2b R1 |
| `harness-30-docs.md` | 30 | T2b 实现 |
| `harness-40-check.md` | 40 | T2b 自检 |
| `harness-50-reinspect.md` | 50 | api/required task；**P1 跳过** |

Lead 开跑：读 MANIFEST + Round 实例 PROMPT §1。
