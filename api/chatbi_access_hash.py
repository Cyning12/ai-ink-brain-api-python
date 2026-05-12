"""ChatBI 访问令牌哈希：与 `docs/diary/local_chatbi_access_token_gen.py` / 任务单 RUNBOOK 一致。"""

from __future__ import annotations

import hashlib
import os


def hash_chatbi_access_token(plaintext: str) -> str:
    """SHA256(pepper_bytes + token_bytes).hexdigest() 小写；pepper 来自 env CHATBI_ACCESS_TOKEN_PEPPER。"""
    p = (os.getenv("CHATBI_ACCESS_TOKEN_PEPPER", "") or "").encode("utf-8")
    t = (plaintext or "").encode("utf-8")
    return hashlib.sha256(p + t).hexdigest()
