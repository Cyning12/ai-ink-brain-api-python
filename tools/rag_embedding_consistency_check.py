#!/usr/bin/env python3
"""校验运行时 Embedding 配置与 Supabase documents.metadata 指纹是否一致（CI / 运维）。"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from api import rag_env  # noqa: F401
from api.rag_embedding_guard import check_embedding_alignment, embedding_mismatch_mode
from api.rag_env import expected_embedding_dim, siliconflow_embedding_model, supabase_client


def main() -> int:
    runtime_model = siliconflow_embedding_model()
    runtime_dim = expected_embedding_dim()
    mode = embedding_mismatch_mode()
    print(f"runtime: model={runtime_model!r} dim={runtime_dim} mode={mode}")

    sb = supabase_client()
    alignment = check_embedding_alignment(sb)
    if alignment.legacy_unstamped:
        print("WARN: 抽样 documents 无 metadata.embedding_model；请全量 re-sync 以写入指纹。")
        return 0

    if alignment.ok:
        stored = ", ".join(alignment.stored_models) or "(none)"
        print(f"OK: stored_models=[{stored}]")
        return 0

    print(f"FAIL: {alignment.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
