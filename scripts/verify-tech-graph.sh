#!/usr/bin/env bash
# 与 .github/workflows/tech-graph.yml · job manifest_check 步骤对齐（本地 / CI 同命令）
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> verify-tech-graph: manifest"
python tools/tech_graph_manifest_check.py

echo "==> verify-tech-graph: test manifest (Phase B)"
python tools/tech_graph_test_manifest_check.py

echo "==> verify-tech-graph: test manifest failure paths (Phase C)"
python tools/tech_graph_test_manifest_check.py --check-failure-paths

echo "==> verify-tech-graph: harness human_gate (PR diff vs origin/main)"
git fetch origin main --depth=1 2>/dev/null || true
python tools/harness_human_gate_check.py --pr-diff --base origin/main

echo "==> verify-tech-graph: graph.json export --check"
python tools/tech_graph_graph_export.py --check

echo "==> verify-tech-graph: docs literal drift"
python tools/tech_graph_drift_check.py

echo "==> verify-tech-graph: graph_v2 equivalence"
python tools/tech_graph_graph_equivalence_check.py

echo "==> verify-tech-graph: token estimate"
python tools/tech_graph_token_estimate.py --json

echo "OK: verify-tech-graph passed (same as CI tech-graph · manifest_check job)"
