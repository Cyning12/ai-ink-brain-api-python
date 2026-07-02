"""Harness Runtime 结构化错误。"""

from __future__ import annotations


class HarnessRuntimeError(Exception):
    """带机器可读 code 的运行时错误。"""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


class SessionSchemaUnsupportedError(HarnessRuntimeError):
    def __init__(self, message: str = "unsupported session schema") -> None:
        super().__init__("SESSION_SCHEMA_UNSUPPORTED", message)


class SessionIdMismatchError(HarnessRuntimeError):
    def __init__(self, message: str = "session_id does not match directory name") -> None:
        super().__init__("SESSION_ID_MISMATCH", message)


class SessionStatusInvalidError(HarnessRuntimeError):
    def __init__(self, message: str = "invalid session status") -> None:
        super().__init__("SESSION_STATUS_INVALID", message)


class GateTableMissingError(HarnessRuntimeError):
    def __init__(self, message: str = "human_gate table not found in task") -> None:
        super().__init__("GATE_TABLE_MISSING", message)


class GateStatusInvalidError(HarnessRuntimeError):
    def __init__(self, message: str = "gate status must be pending or approved") -> None:
        super().__init__("GATE_STATUS_INVALID", message)


class GateNotFoundError(HarnessRuntimeError):
    def __init__(self, gate_id: str) -> None:
        super().__init__("GATE_NOT_FOUND", f"human_gate_id not found: {gate_id}")
