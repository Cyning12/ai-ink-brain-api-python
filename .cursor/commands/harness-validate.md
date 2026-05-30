# Harness · task validate

Run mechanical checks on a Harness task file (OpenSpec Delta + TDD rules).

```bash
python tools/harness_task_validate.py docs/tasks/active/<task>.md
python tools/harness_task_validate.py --all-active
python tools/harness_task_validate.py --json docs/tasks/active/<task>.md
```

**Rules**: `docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md` §4.1  
**Branch**: use task `git_branch`, not `main`.
