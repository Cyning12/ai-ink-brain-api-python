from __future__ import annotations

import importlib

import pytest
from fastapi.testclient import TestClient


def test_chat_suggested_questions_returns_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    index = importlib.import_module("api.index")
    importlib.reload(index)

    client = TestClient(index.app)
    res = client.get("/api/py/chat/suggested-questions")

    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    questions = data["questions"]
    assert isinstance(questions, list)
    assert len(questions) >= 1
    assert all(isinstance(q, str) and q.strip() for q in questions)
