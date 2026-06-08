#!/usr/bin/env bash
# BE-1 全量评测（公开 + 隐藏）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../../.." && pwd)"
cd "$ROOT"
pytest docs/harness/eval/be-sql-readonly-gate-align-v1/tests/ -v "$@"
