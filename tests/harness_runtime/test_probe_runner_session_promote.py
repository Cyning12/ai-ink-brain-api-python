"""probe_runner · session promote verify 测试。"""

from __future__ import annotations

from pathlib import Path

from api.harness_runtime.adapters import probe_runner


def test_verify_for_session_promote_waives_audit_r1(tmp_path: Path, monkeypatch) -> None:
    task = tmp_path / "docs/harness/sessions/sess_x/task_demo_v1.md"
    task.parent.mkdir(parents=True)
    task.write_text(
        """# Task

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| --- | --- | --- | --- |
| HG-EXEC-AUTH | pending | 30 | |
| HG-AUDIT-R1 | pending | 30 | |
""",
        encoding="utf-8",
    )

    def fake_validate_exec_pending(task_path: Path, *, timeout: int = 30):
        return False, [
            {
                "ok": False,
                "errors": [
                    "HUMAN-GATE-BLOCKS-30: HG-EXEC-AUTH status=pending blocks_hats=[30]",
                    "HUMAN-GATE-BLOCKS-30: HG-AUDIT-R1 status=pending blocks_hats=[30]",
                ],
            }
        ]

    monkeypatch.setattr(probe_runner, "task_validate", fake_validate_exec_pending)
    passed, report = probe_runner.verify_for_session_promote(task)
    assert passed is False
    assert report["blocking_errors"]

    def fake_validate_audit_only(task_path: Path, *, timeout: int = 30):
        return False, [
            {
                "ok": False,
                "errors": ["HUMAN-GATE-BLOCKS-30: HG-AUDIT-R1 status=pending blocks_hats=[30]"],
            }
        ]

    monkeypatch.setattr(probe_runner, "task_validate", fake_validate_audit_only)
    passed, report = probe_runner.verify_for_session_promote(task)
    assert passed is True
    assert report["waived_gate_errors"]
