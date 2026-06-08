#!/usr/bin/env bash
# BE-1 公开测（解题 Agent 自测）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../.." && pwd)"
cd "$ROOT"
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/test_public_validate_sql_readonly.py -v "$@"
