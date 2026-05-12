"""Unified Chat 单测：注入 `require_chatbi_principal` 依赖，避免真实查 `chatbi_access_tokens`。"""

from __future__ import annotations

import uuid
from typing import Any

from api.chatbi_principal import ChatBiPrincipal, require_chatbi_principal


def chatbi_super_principal() -> ChatBiPrincipal:
    return ChatBiPrincipal(
        principal_kind="super",
        access_level=0,
        subject_user_id=None,
        token_id=uuid.UUID("00000000-0000-0000-0000-000000000001"),
    )


async def _override_super_principal() -> ChatBiPrincipal:
    return chatbi_super_principal()


def install_unified_chat_auth_override(app: Any) -> None:
    app.dependency_overrides[require_chatbi_principal] = _override_super_principal


def clear_unified_chat_auth_override(app: Any) -> None:
    app.dependency_overrides.pop(require_chatbi_principal, None)
