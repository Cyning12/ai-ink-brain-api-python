# Harness · task status (JSON)

Print Harness task status: meta, human_gate, pending blocks, suggested next hat, validate summary.

```bash
python tools/harness_change_status.py --task docs/tasks/active/<task>.md --json
```

**Example (Loop 母单)**:

```bash
python tools/harness_change_status.py --task docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md --json
```

**Spec**: `docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md` §5 (O5)
