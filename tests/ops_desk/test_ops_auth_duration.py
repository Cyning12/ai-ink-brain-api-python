"""Ops Desk auth 有效期解析测试。"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from api.ops.auth import store as store_mod
from api.ops.auth.duration import (
    parse_session_ttl_hours,
    resolve_duration_hours,
)
from api.ops.auth.store import OpsAuthStore


def test_resolve_duration_hours_fractional() -> None:
    assert resolve_duration_hours(hours=0.01) == 0.01
    assert resolve_duration_hours(days=1) == 24.0


def test_resolve_duration_hours_rejects_both() -> None:
    with pytest.raises(ValueError):
        resolve_duration_hours(hours=1, days=1)


def test_resolve_duration_hours_min() -> None:
    with pytest.raises(ValueError):
        resolve_duration_hours(hours=0.001)


def test_parse_session_ttl_hours() -> None:
    assert parse_session_ttl_hours("0.01") == 0.01
    assert parse_session_ttl_hours("invalid") == 24.0
    assert parse_session_ttl_hours(None) == 24.0


def test_create_session_uses_invite_expires_at(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(store_mod, "_now", lambda: fixed)
    invite_exp = datetime(2026, 6, 26, 12, 0, 36, tzinfo=timezone.utc)

    client = MagicMock()
    captured: dict = {}

    insert_chain = MagicMock()
    insert_chain.execute = MagicMock(return_value=MagicMock())
    client.table.return_value.insert = MagicMock(
        side_effect=lambda payload: (captured.update(payload) or insert_chain)
    )

    store = OpsAuthStore(client)
    session = store.create_session("viewer", expires_at=invite_exp)

    assert session["expires_at"] == "2026-06-26T12:00:36Z"
    assert captured["expires_at"] == "2026-06-26T12:00:36Z"


def test_create_session_perpetual_when_no_invite_expiry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(store_mod, "_now", lambda: datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc))

    client = MagicMock()
    captured: dict = {}
    insert_chain = MagicMock()
    insert_chain.execute = MagicMock(return_value=MagicMock())
    client.table.return_value.insert = MagicMock(
        side_effect=lambda payload: (captured.update(payload) or insert_chain)
    )

    store = OpsAuthStore(client)
    store.create_session("viewer", expires_at=None)

    assert captured["expires_at"] == "2099-12-31T23:59:59Z"


def test_redeem_invite_expired(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(store_mod, "_now", lambda: fixed)

    store = OpsAuthStore(MagicMock())
    store._lookup_invite_row = lambda _t: (None, "expired", None)  # type: ignore[method-assign]
    role, err, _exp = store.redeem_invite_detail("any")
    assert role is None
    assert err == "expired"


def test_get_session_expired(monkeypatch: pytest.MonkeyPatch) -> None:
    fixed = datetime(2026, 6, 26, 12, 0, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(store_mod, "_now", lambda: fixed)

    client = MagicMock()
    row = MagicMock()
    row.data = [
        {
            "id": "s1",
            "role": "viewer",
            "expires_at": "2026-06-26T11:59:59Z",
            "revoked_at": None,
        }
    ]
    client.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = (
        row
    )
    store = OpsAuthStore(client)
    assert store.get_session("s1") is None
