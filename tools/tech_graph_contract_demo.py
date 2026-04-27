from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_PATH = REPO_ROOT / "docs" / "_tech_graph" / "_contract_manifest.json"
CHECK_SCRIPT = REPO_ROOT / "tools" / "tech_graph_contract_check.py"


def _run_check() -> tuple[int, str]:
    p = subprocess.run([sys.executable, str(CHECK_SCRIPT)], capture_output=True, text=True)
    out = (p.stdout or "") + (p.stderr or "")
    return p.returncode, out.strip()


def main() -> int:
    if not CONTRACT_PATH.exists():
        print(f"ERROR: missing {CONTRACT_PATH}")
        return 2
    if not CHECK_SCRIPT.exists():
        print(f"ERROR: missing {CHECK_SCRIPT}")
        return 2

    orig_contract = CONTRACT_PATH.read_text(encoding="utf-8")
    try:
        # 0) baseline
        code0, out0 = _run_check()
        print(f"[baseline] exit={code0}")
        print(out0)
        if code0 != 0:
            return 1

        # 1) negative: remove required done.data_keys key
        obj = json.loads(orig_contract)
        obj["sse"]["done"]["data_keys"] = [k for k in obj["sse"]["done"]["data_keys"] if k != "request_id"]
        CONTRACT_PATH.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        code1, out1 = _run_check()
        print(f"\n[neg1 contract-missing-key] exit={code1}")
        print(out1)
        if code1 == 0:
            print("ERROR: expected failure but got success")
            return 1

        # 2) restore and ensure OK again
        CONTRACT_PATH.write_text(orig_contract, encoding="utf-8")
        code2, out2 = _run_check()
        print(f"\n[restore] exit={code2}")
        print(out2)
        if code2 != 0:
            return 1

        print("\nOK: demo finished (baseline OK, negative fails, restore OK).")
        return 0
    finally:
        # best-effort restore
        try:
            CONTRACT_PATH.write_text(orig_contract, encoding="utf-8")
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    raise SystemExit(main())

