from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
API_DIR = REPO_ROOT / "api"
TG_DIR = REPO_ROOT / "docs" / "_tech_graph"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_endpoints_from_index(index_py: str) -> set[str]:
    # @app.get("/api/py/xxx") / @app.post("/api/py/xxx")
    return set(re.findall(r'@app\.(?:get|post)\("(/api/py/[^"]+)"\)', index_py))


def _extract_rpc_names_from_api(api_text: str) -> set[str]:
    # sb.rpc("keyword_documents", {...})
    return set(re.findall(r'\.rpc\("([A-Za-z0-9_]+)"\s*,', api_text))


def _extract_table_names_from_api(api_text: str) -> set[str]:
    # sb.table("documents")
    return set(re.findall(r'\.table\("([A-Za-z0-9_]+)"\)', api_text))


def _extract_env_names_from_api(api_text: str) -> set[str]:
    # os.getenv("FOO", ...) / os.getenv("FOO")
    return set(re.findall(r'os\.getenv\("([A-Z0-9_]+)"', api_text))


def _collect_api_text() -> str:
    buf: list[str] = []
    for p in sorted(API_DIR.glob("*.py")):
        buf.append(_read_text(p))
    return "\n".join(buf)


def _collect_tech_graph_text() -> str:
    buf: list[str] = []
    for p in sorted(TG_DIR.glob("*.md")):
        buf.append(_read_text(p))
    return "\n".join(buf)


def _check_contains(*, items: set[str], haystack: str, label: str) -> list[str]:
    missing = sorted([x for x in items if x not in haystack])
    if not missing:
        return []
    head = "\n  - ".join(missing[:20])
    tail = "" if len(missing) <= 20 else f"\n  ... and {len(missing) - 20} more"
    return [f"{label} missing in docs/_tech_graph:\n  - {head}{tail}"]


def main() -> int:
    index_path = API_DIR / "index.py"
    if not index_path.exists():
        print("FAIL: missing api/index.py")
        return 2

    # source of truth (code)
    index_text = _read_text(index_path)
    api_text = _collect_api_text()
    endpoints = _extract_endpoints_from_index(index_text)
    rpcs = _extract_rpc_names_from_api(api_text)
    tables = _extract_table_names_from_api(api_text)
    envs = _extract_env_names_from_api(api_text)

    # docs snapshot
    tg_text = _collect_tech_graph_text()

    problems: list[str] = []
    problems += _check_contains(items=endpoints, haystack=tg_text, label="Endpoints")
    problems += _check_contains(items=rpcs, haystack=tg_text, label="Supabase RPC")
    problems += _check_contains(items=tables, haystack=tg_text, label="Supabase tables")

    # env 过多：只检查“关键子集”是否被覆盖（避免把测试/偶发变量全拉进图谱）
    key_env_prefix = (
        "NEXT_PUBLIC_SUPABASE_",
        "SUPABASE_",
        "SILICONFLOW_",
        "RAG_",
        "DEBUG_",
        "TEXT2SQL_",
        "API_KEY",
        "SYNC_ADMIN_SECRET",
        "CHAT_API_SECRET",
    )
    key_env_exact = {"API_KEY", "SYNC_ADMIN_SECRET", "CHAT_API_SECRET", "NEXT_PUBLIC_ADMIN_SECRET"}
    key_envs = {
        e for e in envs if e in key_env_exact or e.startswith(key_env_prefix)
    }
    problems += _check_contains(items=key_envs, haystack=tg_text, label="Key env vars")

    if problems:
        print("FAIL: tech graph drift detected.\n")
        for msg in problems:
            print(msg)
            print()
        return 1

    print("OK: docs/_tech_graph covers endpoints/rpc/env/tables (minimal drift check).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

