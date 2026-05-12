"""CHATBI_JSON_LOG 单行 JSON 与 Text2SQL 阶段字段形状。"""

from __future__ import annotations

import json
import logging

import pytest

from api import chatbi_json_log as cjl


def _reset_chatbi_obs_logger() -> None:
    lg = logging.getLogger("chatbi.obs")
    lg.handlers.clear()
    lg.propagate = False


def test_log_chatbi_record_disabled_by_default(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.delenv("CHATBI_JSON_LOG", raising=False)
    _reset_chatbi_obs_logger()
    cjl.log_chatbi_record(message="noop", run_id="x")
    assert capsys.readouterr().err == ""


def test_log_chatbi_record_emits_json_line(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("CHATBI_JSON_LOG", "1")
    _reset_chatbi_obs_logger()
    try:
        cjl.log_chatbi_record(
            message="text2sql_tool_call_end",
            request_id="rid-1",
            run_id="rid-1",
            session_id="sid-1",
            route="agent",
            mode="text2sql",
            tool="text2sql_query",
            latency_ms=42,
            text2sql_phases_ms={"retrieve": 1, "llm_sql": 2},
        )
        err = capsys.readouterr().err
        line = err.strip().splitlines()[-1]
        obj = json.loads(line)
        assert obj["message"] == "text2sql_tool_call_end"
        assert obj["request_id"] == "rid-1"
        assert obj["run_id"] == "rid-1"
        assert obj["session_id"] == "sid-1"
        assert obj["text2sql_phases_ms"] == {"retrieve": 1, "llm_sql": 2}
        assert obj["service"] == "chatbi-api"
    finally:
        _reset_chatbi_obs_logger()
