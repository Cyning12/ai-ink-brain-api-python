"""ChatBI V3 P1-2：用户侧 Prompt 注入规则 PoC（输入侧 scan，早于上游 LLM）。"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Literal

GuardMode = Literal["off", "warn", "block"]


def chatbi_prompt_guard_mode() -> GuardMode:
    """`CHATBI_PROMPT_GUARD_MODE`：`off`（默认）| `warn` | `block`。"""
    raw = (os.getenv("CHATBI_PROMPT_GUARD_MODE", "off") or "").strip().lower()
    if raw == "warn":
        return "warn"
    if raw == "block":
        return "block"
    return "off"


@dataclass(frozen=True)
class GuardResult:
    """`blocked=True` 表示命中规则或 fail-closed 内部错误（均不向下游 LLM 传递用户原文意图）。"""

    blocked: bool
    reason_code: str | None
    matched_rule_id: str | None
    internal_error: bool = False


def _compiled_rules() -> list[tuple[str, re.Pattern[str]]]:
    """PoC 规则表：标题与 task §4 对齐，命中顺序为表序。"""
    return [
        (
            "RULE_IGNORE_PREV",
            re.compile(
                r"(?i)(\bignore\s+(all\s+)?(previous|prior)\s+(instructions|context)\b|"
                r"\bdisregard\s+(the\s+)?(above|prior)\b|"
                r"忽略上文|忽略以上的|忽略\s*之前\s*(的\s*)?(指令|规则|提示|system)\b)",
                re.UNICODE,
            ),
        ),
        (
            "RULE_FAKE_SYSTEM",
            re.compile(
                r"(?i)(<\|im_start\|>\s*system|<\|system\|>|\[SYSTEM\]\s*:|###\s*System\s*Message|"
                r"\brole\s*[:=]\s*['\"]system['\"])",
                re.UNICODE,
            ),
        ),
        (
            "RULE_EXFIL_SECRET",
            re.compile(
                r"(?i)(\b(OPENAI_API_KEY|ANTHROPIC_API_KEY|SILICONFLOW_API_KEY|AWS_SECRET_ACCESS_KEY)\b|"
                r"列出\s*所有\s*环境变量|打印\s*\.env|export\s+[\w_]*(KEY|SECRET|TOKEN)\b|"
                r"把\s*(api|访问)?\s*密钥\s*发给我)",
                re.UNICODE,
            ),
        ),
        (
            "RULE_AUDIT_WIPE",
            re.compile(
                r"(?i)(删除\s*审计\s*日志|清空\s*(访问|操作)?日志|\bwipe\s+audit\s+logs?\b|"
                r"\bdisable\s+auditing\b|关闭\s*审计)",
                re.UNICODE,
            ),
        ),
        (
            "RULE_DATA_EXFIL",
            re.compile(
                r"(?i)(把\s*(整个|全部)?\s*数据库\s*(导出|备份|发到)|\bdump\s+(the\s+)?full\s+(schema|database)\b|"
                r"复制\s*所有\s*用户\s*(密码|token))",
                re.UNICODE,
            ),
        ),
    ]


def scan(text: str) -> GuardResult:
    """扫描用户侧文本；**fail-closed**：异常时返回 `blocked=True` 且 `internal_error=True`。"""
    try:
        t = text or ""
        for rule_id, pat in _compiled_rules():
            if pat.search(t):
                return GuardResult(
                    blocked=True,
                    reason_code="prompt_injection_pattern",
                    matched_rule_id=rule_id,
                    internal_error=False,
                )
        return GuardResult(blocked=False, reason_code=None, matched_rule_id=None, internal_error=False)
    except Exception:  # noqa: BLE001
        return GuardResult(
            blocked=True,
            reason_code="guard_scan_internal_error",
            matched_rule_id=None,
            internal_error=True,
        )
