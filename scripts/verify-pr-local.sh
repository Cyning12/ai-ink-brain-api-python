#!/usr/bin/env bash
# PR 合并前本地验收：tech-graph Required checks + pytest Required checks
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

bash scripts/verify-tech-graph.sh

echo "==> verify-pr-local: contract (tech-graph-contract.yml)"
python tools/tech_graph_contract_check.py

echo "==> verify-pr-local: pytest"
pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short

echo "OK: verify-pr-local passed (tech-graph + contract + pytest)"
