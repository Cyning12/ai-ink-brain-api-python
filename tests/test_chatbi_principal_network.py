"""ChatBI 鉴权：Supabase 网络抖动重试与 DATABASE_DISCONNECT 映射。"""

from __future__ import annotations

import errno
from typing import Any
from unittest.mock import MagicMock

import httpx
import pytest
from fastapi import HTTPException

from api import chatbi_principal as cp


def test_fetch_token_row_retries_then_succeeds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_HTTP_RETRIES", "4")
    monkeypatch.setenv("SUPABASE_HTTP_RETRY_BASE_DELAY_S", "0")
    calls = {"n": 0}

    def fake_client() -> MagicMock:
        calls["n"] += 1
        sb = MagicMock()
        if calls["n"] < 2:
            raise httpx.ConnectError("[Errno 54] Connection reset by peer")
        table = MagicMock()
        table.select.return_value = table
        table.eq.return_value = table
        table.is_.return_value = table
        table.limit.return_value = table
        table.execute.return_value = MagicMock(
            data=[{"id": "00000000-0000-0000-0000-000000000001", "access_level": 0}]
        )
        sb.table.return_value = table
        return sb

    monkeypatch.setattr(cp, "supabase_client", fake_client)
    row = cp._fetch_token_row_by_hash("deadbeef")
    assert row is not None
    assert row["access_level"] == 0
    assert calls["n"] == 2


def test_resolve_principal_maps_exhausted_network_to_database_disconnect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SUPABASE_HTTP_RETRIES", "2")
    monkeypatch.setenv("SUPABASE_HTTP_RETRY_BASE_DELAY_S", "0")

    def always_fail(_key_hash: str) -> Any:
        raise httpx.ConnectError("[Errno 54] Connection reset by peer")

    monkeypatch.setattr(cp, "_fetch_token_row_by_hash", always_fail)
    monkeypatch.setattr(cp, "hash_chatbi_access_token", lambda _t: "h")

    with pytest.raises(HTTPException) as ei:
        cp._resolve_principal_sync("Bearer plain-token", request_id="rid-1")
    exc = ei.value
    assert exc.status_code == 500
    det = exc.detail
    assert isinstance(det, dict)
    assert det.get("code") == "DATABASE_DISCONNECT"
    assert det.get("error_type") == "DATABASE_DISCONNECT"


def test_transient_detects_httpx_connect_error() -> None:
    from api.rag_env import transient_supabase_network_error

    assert transient_supabase_network_error(
        httpx.ConnectError("[Errno 54] Connection reset by peer")
    )
    assert transient_supabase_network_error(OSError(errno.ECONNRESET, "reset"))

