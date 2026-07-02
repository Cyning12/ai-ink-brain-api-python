#!/usr/bin/env bash
# 对齐 tech-graph.yml · task_validate：校验相对 base 分支变更的 task 单
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BASE="${VERIFY_TASK_BASE:-main}"
if git show-ref --verify --quiet "refs/remotes/origin/${BASE}"; then
  REF="origin/${BASE}"
elif git show-ref --verify --quiet "refs/heads/${BASE}"; then
  REF="${BASE}"
else
  echo "verify-task-changes: base ref ${BASE} not found; skip."
  exit 0
fi

FILES="$(git diff --name-only --diff-filter=ACMR "${REF}...HEAD" -- \
  'docs/tasks/active/*.md' 'docs/tasks/done/*.md' 2>/dev/null || true)"

if [ -z "${FILES}" ]; then
  echo "verify-task-changes: no task .md changes vs ${REF}; skip."
  exit 0
fi

echo "==> verify-task-changes: base=${REF}"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if [[ "$f" == *_AGENT_PROMPT* ]]; then
    continue
  fi
  if [[ "$(basename "$f")" == README.md ]]; then
    echo "Skip README index: $f"
    continue
  fi
  if [ ! -f "$f" ]; then
    echo "Skip missing path (deleted-only in diff): $f"
    continue
  fi
  echo "Validating $f"
  python tools/harness_task_validate.py "$f"
done <<< "$FILES"

echo "OK: verify-task-changes passed"
