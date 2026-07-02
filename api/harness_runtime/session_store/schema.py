"""Session meta YAML schema（v1）。"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

import yaml
from pydantic import BaseModel, Field, field_validator

from api.harness_runtime.errors import SessionSchemaUnsupportedError, SessionStatusInvalidError

SUPPORTED_SCHEMA_VERSION = "1.0"
META_FILENAME = "session.meta.yaml"


class SessionStatus(StrEnum):
    CREATED = "created"
    PLANNING = "planning"
    AWAITING_AUTH = "awaiting_auth"
    DISPATCHED = "dispatched"
    REVIEWING = "reviewing"
    DONE = "done"
    BLOCKED = "blocked"
    PARTIAL = "partial"


class WorktreeHint(BaseModel):
    repo: str
    branch: str


class GateSummary(BaseModel):
    pending: list[str] = Field(default_factory=list)
    approved: list[str] = Field(default_factory=list)


class SessionLinks(BaseModel):
    plan: str | None = None
    spec: str | None = None


class SessionMeta(BaseModel):
    schema_version: str
    session_id: str
    slug: str
    title: str
    status: SessionStatus
    created_at: datetime
    updated_at: datetime
    created_by: str = "maintainer"
    worktree_hint: WorktreeHint | None = None
    primary_task_path: str
    latest_run_id: str | None = None
    gate_summary: GateSummary = Field(default_factory=GateSummary)
    links: SessionLinks | None = None

    @field_validator("schema_version")
    @classmethod
    def validate_schema_version(cls, value: str) -> str:
        if value != SUPPORTED_SCHEMA_VERSION:
            raise SessionSchemaUnsupportedError(
                f"schema_version must be {SUPPORTED_SCHEMA_VERSION!r}, got {value!r}"
            )
        return value

    @field_validator("status", mode="before")
    @classmethod
    def coerce_status(cls, value: Any) -> SessionStatus:
        if isinstance(value, SessionStatus):
            return value
        try:
            return SessionStatus(str(value))
        except ValueError as exc:
            raise SessionStatusInvalidError(f"invalid status: {value!r}") from exc

    def to_yaml_dict(self) -> dict[str, Any]:
        data = self.model_dump(mode="json")
        for key in ("created_at", "updated_at"):
            if key in data and data[key]:
                data[key] = self.__getattribute__(key).strftime("%Y-%m-%dT%H:%M:%SZ")
        return data

    def dump_yaml(self) -> str:
        return yaml.safe_dump(
            self.to_yaml_dict(),
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
        )

    @classmethod
    def from_yaml_text(cls, text: str) -> SessionMeta:
        raw = yaml.safe_load(text)
        if not isinstance(raw, dict):
            raise SessionSchemaUnsupportedError("session.meta.yaml must be a mapping")
        if "schema_version" not in raw:
            raise SessionSchemaUnsupportedError("schema_version is required")
        return cls.model_validate(raw)
