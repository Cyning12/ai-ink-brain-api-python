from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class KeywordFallbackConfig:
    enabled: bool
    min_hits: int
    match_count: int
    max_tokens: int

    @staticmethod
    def from_env() -> "KeywordFallbackConfig":
        enabled_raw = (os.getenv("KEYWORD_FALLBACK_ENABLED", "1") or "").strip().lower()
        enabled = enabled_raw not in ("0", "false", "no", "off")
        try:
            min_hits = int(os.getenv("KEYWORD_FALLBACK_MIN_HITS", "1"))
        except ValueError:
            min_hits = 1
        try:
            match_count = int(os.getenv("KEYWORD_FALLBACK_MATCH_COUNT", "12"))
        except ValueError:
            match_count = 12
        try:
            max_tokens = int(os.getenv("KEYWORD_FALLBACK_MAX_TOKENS", "12"))
        except ValueError:
            max_tokens = 12
        return KeywordFallbackConfig(
            enabled=enabled,
            min_hits=max(0, min_hits),
            match_count=max(1, match_count),
            max_tokens=max(1, max_tokens),
        )


@dataclass(frozen=True)
class KeywordFallbackResult:
    triggered: bool
    reason: str
    query_used: str | None
    query_text: str | None
    anchor_tokens: list[str]
    latency_ms: int
    initial_hits: int
    final_hits: int


# --- Anchor token patterns (易于增删改) ---
#
# 规则定位：当用户输入里出现这些“高价值锚点”时，说明用户更像在找具体文件/标识符，
# 此时若 keyword_hits=0，则很可能是 rewrite 把锚点“意译”掉了，需要回退。
ANCHOR_TOKEN_PATTERNS: list[re.Pattern[str]] = [
    # 文件名/后缀（含路径片段）
    re.compile(r"(?i)\b[\w./-]+\.(md|mdx|pdf|txt|png|jpe?g|webp)\b"),
    # task_04 / task-04 / Task 04
    re.compile(r"(?i)\btask[_-]?\d+\b"),
    re.compile(r"(?i)\btask\s+\d+\b"),
    # 日期（含 2026-4-14.md / 2026-04-14）
    re.compile(r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b"),
]


def normalize_for_fts(text: str) -> str:
    """将常见分隔符归一化为空格，降低 websearch_to_tsquery 的解析偏差。"""
    t = (text or "").strip()
    if not t:
        return ""
    t = re.sub(r"[_./\\-]+", " ", t)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def extract_anchor_tokens(text: str) -> list[str]:
    raw = (text or "").strip()
    if not raw:
        return []
    tokens: list[str] = []
    for pat in ANCHOR_TOKEN_PATTERNS:
        for m in pat.finditer(raw):
            s = m.group(0).strip()
            if not s:
                continue
            tokens.append(s)
    # 去重但保序
    seen: set[str] = set()
    out: list[str] = []
    for t in tokens:
        key = t.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(t)
    return out


def compare_anchor_tokens(raw_query: str, rewritten_query: str) -> dict[str, Any]:
    """比较 raw vs rewrite 的锚点 token 是否丢失（用于可观测性与后续方案 2）。"""
    raw_tokens = extract_anchor_tokens(raw_query)
    rw_tokens = extract_anchor_tokens(rewritten_query)
    rw_set = {t.lower() for t in rw_tokens}
    missing = [t for t in raw_tokens if t.lower() not in rw_set]
    return {
        "tokens_raw": raw_tokens,
        "tokens_rewrite": rw_tokens,
        "missing": missing,
        "is_key_entity_lost": len(missing) > 0,
    }


def should_trigger_keyword_fallback(
    *,
    cfg: KeywordFallbackConfig,
    raw_query: str,
    keyword_hits_count: int,
) -> tuple[bool, str, list[str]]:
    if not cfg.enabled:
        return False, "disabled", []
    if keyword_hits_count >= cfg.min_hits:
        return False, "enough_hits", []
    tokens = extract_anchor_tokens(raw_query)
    if not tokens:
        return False, "no_anchor_tokens", []
    return True, "keyword_hits_below_min_and_has_anchor_tokens", tokens


def run_keyword_fallback(
    *,
    sb: Any,
    raw_query: str,
    cfg: KeywordFallbackConfig,
    fetch_keyword_hits: Callable[[Any, str, int], list[dict[str, Any]]],
    initial_hits: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], KeywordFallbackResult]:
    """当 keyword_hits 为 0（或低于阈值）时，用更保守的 query 再检索一次。"""
    t0 = time.perf_counter()
    initial_n = len(initial_hits)

    trigger, reason, tokens = should_trigger_keyword_fallback(
        cfg=cfg, raw_query=raw_query, keyword_hits_count=initial_n
    )
    if not trigger:
        return initial_hits, KeywordFallbackResult(
            triggered=False,
            reason=reason,
            query_used=None,
            query_text=None,
            anchor_tokens=tokens,
            latency_ms=0,
            initial_hits=initial_n,
            final_hits=initial_n,
        )

    # 回退策略：
    # 1) tokens_joined（强锚点）
    # 2) normalized raw query（弱锚点，尽量保留原意）
    tokens_limited = tokens[: cfg.max_tokens]
    q_tokens = " ".join(tokens_limited).strip()
    q_norm = normalize_for_fts(raw_query)

    # 注意：不在这里做复杂融合，企业上更建议“只要回退命中就替换 keyword_hits”，
    # 后续由 RRF 在更上层融合 vector/keyword。
    hits: list[dict[str, Any]] = []
    query_used: str | None = None
    query_text: str | None = None

    if q_tokens:
        hits = fetch_keyword_hits(sb, q_tokens, cfg.match_count)
        if hits:
            query_used = "fallback_tokens"
            query_text = q_tokens
    if not hits and q_norm and q_norm != q_tokens:
        hits = fetch_keyword_hits(sb, q_norm, cfg.match_count)
        if hits:
            query_used = "fallback_normalized"
            query_text = q_norm

    final_n = len(hits) if hits else initial_n
    latency_ms = int((time.perf_counter() - t0) * 1000)
    return (hits or initial_hits), KeywordFallbackResult(
        triggered=True,
        reason=reason,
        query_used=query_used or "fallback_none",
        query_text=query_text,
        anchor_tokens=tokens_limited,
        latency_ms=latency_ms,
        initial_hits=initial_n,
        final_hits=final_n,
    )

