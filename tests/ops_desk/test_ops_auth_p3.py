"""Ops Desk P3-2a · DB session 鉴权测试。"""

from __future__ import annotations

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops.auth.store import OpsAuthStore, _hash_token


@pytest.fixture
def auth_client() -> TestClient:
    invite_exp = datetime(2099, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    fake_store = MagicMock()
    fake_store.redeem_invite_detail.side_effect = lambda t: (
        ("viewer", None, invite_exp) if t == "viewer-token" else (None, "invalid", None)
    )
    fake_store.create_session.return_value = {
        "id": "sess-test-1",
        "role": "viewer",
        "expires_at": "2099-01-01T00:00:00Z",
    }
    fake_store.get_session.side_effect = lambda sid: (
        {"id": sid, "role": "viewer", "expires_at": "2099-01-01T00:00:00Z"} if sid == "sess-test-1" else None
    )
    fake_store.revoke_session.return_value = True

    import api.ops.auth.router as auth_mod

    app.dependency_overrides[auth_mod._auth_store] = lambda: fake_store
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_auth_login_and_session(auth_client: TestClient) -> None:
    login = auth_client.post("/api/py/ops/auth/login", json={"token": "viewer-token"})
    assert login.status_code == 200
    body = login.json()
    assert body["ok"] is True
    session_id = body["session_id"]

    sess = auth_client.get("/api/py/ops/auth/session", headers={"x-ops-session": session_id})
    assert sess.status_code == 200
    assert sess.json()["role"] == "viewer"


def test_auth_login_invalid(auth_client: TestClient) -> None:
    res = auth_client.post("/api/py/ops/auth/login", json={"token": "bad"})
    assert res.status_code == 401
    detail = res.json()["detail"]
    assert detail["code"] == "INVITE_INVALID"
    assert detail["message"] == "秘钥无效"


def test_auth_login_expired_message() -> None:
    import api.ops.auth.router as auth_mod

    fake = MagicMock()
    fake.redeem_invite_detail.return_value = (None, "expired", None)
    app.dependency_overrides[auth_mod._auth_store] = lambda: fake
    client = TestClient(app)
    try:
        res = client.post("/api/py/ops/auth/login", json={"token": "x"})
        assert res.status_code == 401
        assert res.json()["detail"]["message"] == "秘钥已过期"
    finally:
        app.dependency_overrides.clear()


def test_hash_token_stable() -> None:
    assert _hash_token("abc") == _hash_token("abc")
    assert _hash_token("abc") != _hash_token("xyz")


def test_redeem_invite_db_only() -> None:
    store = OpsAuthStore(MagicMock())
    store._lookup_invite_row = lambda t: (  # type: ignore[method-assign]
        ("maintainer", None, None) if t == "ok-token" else (None, "invalid", None)
    )

    assert store.redeem_invite("ok-token") == "maintainer"
    assert store.redeem_invite("missing") is None


def test_redeem_invite_db_error_returns_none() -> None:
    store = OpsAuthStore(MagicMock())

    def _boom(_t: str) -> None:
        raise RuntimeError("ops_desk_invites does not exist")

    store._lookup_invite_row = _boom  # type: ignore[method-assign]
    role, err, _exp = store.redeem_invite_detail("any")
    assert role is None
    assert err == "invalid"


def test_upsert_invite_skips_existing_hash() -> None:
    client = MagicMock()
    existing_row = MagicMock()
    existing_row.data = [{"id": "uuid-1"}]
    client.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = (
        existing_row
    )

    store = OpsAuthStore(client)
    store.upsert_invite("viewer", "plain-token", "viewer")

    client.table.return_value.insert.assert_not_called()
