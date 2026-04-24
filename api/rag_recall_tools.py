from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal


def should_retry_error(msg: str) -> bool:
    m = (msg or "").lower()
    return any(
        k in m
        for k in (
            "connection reset",
            "econnreset",
            "connection aborted",
            "broken pipe",
            "timed out",
            "timeout",
            "server disconnected",
            "remote protocol error",
        )
    )


def rpc_execute_with_retry(
    sb: Any,
    fn: str,
    params: dict[str, Any],
    *,
    retries: int = 2,
    backoff_base_s: float = 0.15,
) -> tuple[list[dict[str, Any]], int, str | None]:
    """对 Supabase RPC 做有限重试，返回 (rows, retry_count, last_error)。"""
    last_err: str | None = None
    attempt = 0
    while True:
        try:
            data = sb.rpc(fn, params).execute().data
            rows = data if isinstance(data, list) else []
            return ([r for r in rows if isinstance(r, dict)], attempt, None)
        except Exception as exc:  # noqa: BLE001
            last_err = str(exc)
            if attempt >= retries or not should_retry_error(last_err):
                return ([], attempt, last_err)
            time.sleep(float(backoff_base_s) * (2**attempt))
            attempt += 1


_DATE_RE = re.compile(r"\b(\d{4})[./-](\d{1,2})[./-](\d{1,2})\b")
_ZH_MD_RE = re.compile(r"(?:\b|^)(\d{1,2})\s*月\s*(\d{1,2})\s*(?:日|号)(?:\b|$)")
_ZH_FULL_RE = re.compile(r"(?:\b|^)(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*(?:日|号)(?:\b|$)")
_CN_DIGIT_MAP: dict[str, int] = {
    "〇": 0,
    "零": 0,
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    # 大写/财务数字（常见于票据/正式文本）
    "壹": 1,
    "贰": 2,
    "叁": 3,
    "肆": 4,
    "伍": 5,
    "陆": 6,
    "柒": 7,
    "捌": 8,
    "玖": 9,
    # 两/兩：口语与繁体常见
    "两": 2,
    "兩": 2,
}
_CN_YEAR_RE = re.compile(
    r"(?:^|)([〇零一二三四五六七八九壹贰叁肆伍陆柒捌玖两兩]{4})\s*年\s*([〇零一二三四五六七八九壹贰叁肆伍陆柒捌玖两兩十拾]{1,3})\s*月\s*([〇零一二三四五六七八九壹贰叁肆伍陆柒捌玖两兩十拾]{1,3})\s*(?:日|号)"
)
_CN_MD_RE = re.compile(r"(?:^|)([〇零一二三四五六七八九壹贰叁肆伍陆柒捌玖两兩十拾]{1,3})\s*月\s*([〇零一二三四五六七八九壹贰叁肆伍陆柒捌玖两兩十拾]{1,3})\s*(?:日|号)")

_VER3_RE = re.compile(r"\bv?(\d{1,3})[._-](\d{1,3})[._-](\d{1,3})\b", re.IGNORECASE)


def date_candidates_for_keyword(query: str) -> list[str]:
    """
    从 query 中抽取日期并生成多形态候选，用于 keyword（FTS）召回。
    - 仅用于 keyword query_text，不改变原始 query 的展示/生成。
    - 针对 FTS 对 '04' vs '4' 敏感的问题，覆盖补零与不补零。
    """
    s = (query or "").strip()
    if not s:
        return []
    m = _DATE_RE.search(s)
    if not m:
        return []
    y, mo_s, d_s = m.group(1), m.group(2), m.group(3)
    mo_i = max(1, min(12, int(mo_s)))
    d_i = max(1, min(31, int(d_s)))
    mo2 = f"{mo_i:02d}"
    d2 = f"{d_i:02d}"
    base = {f"{y}-{mo_s}-{d_s}", f"{y}-{mo2}-{d2}"}
    out: set[str] = set()
    for dt in base:
        out.add(dt)
        out.add(dt.replace("-", "/"))
        out.add(dt.replace("-", "."))
        out.add(dt.replace("-", " "))
    return [x for x in out if x]


def keyword_query_text(query: str) -> str:
    """
    构造适配 websearch_to_tsquery 的 query_text。
    - 若包含日期：生成 `"a" OR "b" OR "c"`，提升日期类召回稳定性。
    - 否则：原样返回。
    """
    qt, _meta = keyword_query_text_with_i18n_meta(query)
    return qt


I18nExpandMode = Literal["glossary", "llm", "off"]


@dataclass(frozen=True)
class I18nExpandResult:
    raw: str
    expanded: str
    candidates: list[str]
    source: Literal["glossary", "llm", "none", "error"]
    truncated: bool
    enabled: bool
    mode: I18nExpandMode


_I18N_ALLOWED_RE = re.compile(r"[^A-Za-z0-9\s._/\-]+")
_I18N_HAS_ZH_RE = re.compile(r"[\u4e00-\u9fff]")


def _env_bool(name: str, default: bool) -> bool:
    raw = (os.getenv(name, "").strip() or ("1" if default else "0")).lower()
    return raw in ("1", "true", "yes", "on")


def _env_int(name: str, default: int, *, min_v: int, max_v: int) -> int:
    raw = (os.getenv(name, "").strip() or str(default)).strip()
    try:
        v = int(raw)
    except Exception:  # noqa: BLE001
        return default
    return max(min_v, min(max_v, v))


def _i18n_mode() -> I18nExpandMode:
    v = (os.getenv("I18N_EXPAND_MODE", "glossary") or "glossary").strip().lower()
    if v in ("glossary", "llm", "off"):
        return v  # type: ignore[return-value]
    return "glossary"


def _i18n_glossary_path() -> Path:
    # api/rag_recall_tools.py -> repo_root/data/i18n_glossary.json
    return (Path(__file__).resolve().parents[1] / "data" / "i18n_glossary.json").resolve()


_I18N_GLOSSARY_CACHE: tuple[float, dict[str, list[str]]] | None = None


def _load_i18n_glossary() -> dict[str, list[str]]:
    """
    轻量术语表：中文短语 -> 英文候选短语列表。
    - 文件不存在/解析失败：返回空表（必须优雅降级）
    - 做简单缓存：按 mtime 失效
    """
    global _I18N_GLOSSARY_CACHE  # noqa: PLW0603
    p = _i18n_glossary_path()
    try:
        st = p.stat()
    except Exception:  # noqa: BLE001
        _I18N_GLOSSARY_CACHE = (0.0, {})
        return {}

    if _I18N_GLOSSARY_CACHE is not None and _I18N_GLOSSARY_CACHE[0] == float(st.st_mtime):
        return _I18N_GLOSSARY_CACHE[1]

    try:
        raw = p.read_text(encoding="utf-8")
        obj = json.loads(raw)
        out: dict[str, list[str]] = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if not isinstance(k, str) or not k.strip():
                    continue
                if isinstance(v, str) and v.strip():
                    out[k.strip()] = [v.strip()]
                elif isinstance(v, list):
                    vals = [x.strip() for x in v if isinstance(x, str) and x.strip()]
                    if vals:
                        out[k.strip()] = vals
        _I18N_GLOSSARY_CACHE = (float(st.st_mtime), out)
        return out
    except Exception:  # noqa: BLE001
        _I18N_GLOSSARY_CACHE = (float(st.st_mtime), {})
        return {}


def _clean_i18n_candidate(s: str, *, max_chars: int) -> str:
    t = (s or "").strip()
    if not t:
        return ""
    # 去掉引号与控制字符，避免破坏 websearch_to_tsquery 语法
    t = t.replace("\u0000", "").replace("\r", " ").replace("\n", " ").replace("\t", " ")
    t = t.replace('"', "").replace("'", "")
    t = _I18N_ALLOWED_RE.sub(" ", t)
    t = re.sub(r"\s+", " ", t).strip()
    if not t:
        return ""
    if len(t) > max_chars:
        t = t[:max_chars].strip()
    return t


def _clean_raw_query_phrase(s: str, *, max_chars: int) -> str:
    """
    原 query 必须保留（含中文/标识符），只做最小清洗避免语法破坏：
    - 去掉控制字符与引号
    - 折叠空白
    - 截断上限
    """
    t = (s or "").strip()
    if not t:
        return ""
    t = t.replace("\u0000", "").replace("\r", " ").replace("\n", " ").replace("\t", " ")
    t = t.replace('"', "").replace("'", "")
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) > max_chars:
        t = t[:max_chars].strip()
    return t


def _i18n_candidates_from_glossary(query: str, *, max_candidates: int, max_candidate_chars: int) -> list[str]:
    if not query.strip():
        return []
    if not _I18N_HAS_ZH_RE.search(query):
        return []
    glossary = _load_i18n_glossary()
    if not glossary:
        return []
    found: list[str] = []
    # v1：仅做子串命中（不引入中文分词）
    for zh, ens in glossary.items():
        if zh and zh in query:
            for en in ens:
                c = _clean_i18n_candidate(en, max_chars=max_candidate_chars)
                if c:
                    found.append(c)
        if len(found) >= max_candidates * 2:
            break
    # 去重 + 稳定输出
    out: list[str] = []
    seen: set[str] = set()
    for c in found:
        key = c.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
        if len(out) >= max_candidates:
            break
    return out


def keyword_query_text_with_i18n_meta(query: str) -> tuple[str, dict[str, Any] | None]:
    """
    构造 keyword/FTS 的 query_text，并返回 i18n expand 元信息（用于 events/log）。
    约束：任何异常必须优雅降级为仅原 query。
    """
    q_raw = (query or "").strip()
    if not q_raw:
        return ("", None)

    enabled = _env_bool("I18N_EXPAND_ENABLED", True)
    mode = _i18n_mode()
    max_candidates = _env_int("I18N_EXPAND_MAX_CANDIDATES", 5, min_v=0, max_v=50)
    max_candidate_chars = _env_int("I18N_EXPAND_MAX_CANDIDATE_CHARS", 48, min_v=8, max_v=256)
    max_query_chars = _env_int("I18N_EXPAND_MAX_QUERY_TEXT_CHARS", 240, min_v=64, max_v=2048)

    # 1) 先保留原 query（强制）
    parts: list[str] = []
    seen: set[str] = set()

    def _push_phrase(phrase: str) -> None:
        if phrase == q_raw:
            p = _clean_raw_query_phrase(phrase, max_chars=max_query_chars)
        else:
            p = _clean_i18n_candidate(phrase, max_chars=max_candidate_chars)
        if not p:
            return
        key = p.lower()
        if key in seen:
            return
        seen.add(key)
        parts.append(f"\"{p}\"")

    _push_phrase(q_raw)

    # 2) 既有日期/版本扩展（保持逻辑，但不再丢掉原 query）
    try:
        for c in date_candidates_for_keyword(q_raw):
            _push_phrase(c)
        for m in _VER3_RE.finditer(q_raw):
            a, b, c = m.group(1), m.group(2), m.group(3)
            _push_phrase(f"{a}.{b}.{c}")
            _push_phrase(f"v{a}.{b}.{c}")
            _push_phrase(f"{a}_{b}_{c}")
            _push_phrase(f"{a}-{b}-{c}")
    except Exception:  # noqa: BLE001
        # v1：不让扩展影响可靠性
        return (q_raw, None)

    # 3) i18n expand（glossary 优先，LLM 默认关闭）
    candidates: list[str] = []
    source: Literal["glossary", "llm", "none", "error"] = "none"
    truncated = False
    if enabled and max_candidates > 0 and mode != "off":
        try:
            if mode == "glossary":
                candidates = _i18n_candidates_from_glossary(
                    q_raw,
                    max_candidates=max_candidates,
                    max_candidate_chars=max_candidate_chars,
                )
                source = "glossary" if candidates else "none"
            elif mode == "llm":
                # v1：预留开关，默认关闭；实现必须保证失败回退
                candidates = []
                source = "none"
        except Exception:  # noqa: BLE001
            candidates = []
            source = "error"

    for c in candidates:
        _push_phrase(c)

    # 4) 总长度保护（按字符，尽量保留前面更重要的 phrase）
    joined = " OR ".join(parts)
    if len(joined) > max_query_chars:
        trimmed: list[str] = []
        cur = 0
        for p in parts:
            add = len(p) if not trimmed else (4 + len(p))  # " OR "
            if cur + add > max_query_chars:
                truncated = True
                break
            trimmed.append(p)
            cur += add
        joined = " OR ".join(trimmed) if trimmed else f"\"{_clean_i18n_candidate(q_raw, max_chars=max_query_chars)}\""

    meta: dict[str, Any] = {
        "raw": q_raw,
        "expanded": joined,
        "candidates": candidates,
        "source": source,
        "truncated": bool(truncated),
        "enabled": bool(enabled),
        "mode": mode,
        "limits": {
            "max_candidates": max_candidates,
            "max_candidate_chars": max_candidate_chars,
            "max_query_text_chars": max_query_chars,
        },
    }
    return (joined, meta)


def date_norm_candidates_for_structured(query: str) -> list[str]:
    """
    为结构化召回提取日期候选（YYYY-MM-DD）。
    支持：
    - 2026-4-14 / 2026/4/14 / 2026.4.14
    - 2026年4月14日 / 2026年4月14号
    - 二零二六年四月十四号
    - 四月十四号（缺年：尝试当年与上一年）
    """
    s = (query or "").strip()
    if not s:
        return []
    out: set[str] = set()

    def _cn_int(tok: str) -> int | None:
        t = (tok or "").strip()
        if not t:
            return None
        # “拾”按“十”处理
        t = t.replace("拾", "十")
        if t.isdigit():
            return int(t)
        if all(ch in _CN_DIGIT_MAP for ch in t):
            v = 0
            for ch in t:
                v = v * 10 + int(_CN_DIGIT_MAP[ch])
            return v
        if any(ch not in (set(_CN_DIGIT_MAP.keys()) | {"十"}) for ch in t):
            return None
        if t == "十":
            return 10
        if "十" not in t:
            if len(t) == 1 and t in _CN_DIGIT_MAP:
                return int(_CN_DIGIT_MAP[t])
            return None
        left, _, right = t.partition("十")
        tens = 1 if left == "" else (int(_CN_DIGIT_MAP[left]) if left in _CN_DIGIT_MAP else None)
        if tens is None:
            return None
        ones = 0
        if right:
            if len(right) == 1 and right in _CN_DIGIT_MAP:
                ones = int(_CN_DIGIT_MAP[right])
            else:
                return None
        return tens * 10 + ones

    m1 = _DATE_RE.search(s)
    if m1:
        y, mo_s, d_s = m1.group(1), m1.group(2), m1.group(3)
        mo_i = max(1, min(12, int(mo_s)))
        d_i = max(1, min(31, int(d_s)))
        out.add(f"{int(y):04d}-{mo_i:02d}-{d_i:02d}")

    m2 = _ZH_FULL_RE.search(s)
    if m2:
        y, mo_s, d_s = m2.group(1), m2.group(2), m2.group(3)
        mo_i = max(1, min(12, int(mo_s)))
        d_i = max(1, min(31, int(d_s)))
        out.add(f"{int(y):04d}-{mo_i:02d}-{d_i:02d}")

    m2b = _CN_YEAR_RE.search(s)
    if m2b:
        y = _cn_int(m2b.group(1))
        mo = _cn_int(m2b.group(2))
        d = _cn_int(m2b.group(3))
        if y and mo and d:
            mo_i = max(1, min(12, int(mo)))
            d_i = max(1, min(31, int(d)))
            out.add(f"{int(y):04d}-{mo_i:02d}-{d_i:02d}")

    m3 = _ZH_MD_RE.search(s)
    if m3:
        mo_s, d_s = m3.group(1), m3.group(2)
        mo_i = max(1, min(12, int(mo_s)))
        d_i = max(1, min(31, int(d_s)))
        y0 = datetime.now(timezone.utc).year
        out.add(f"{y0:04d}-{mo_i:02d}-{d_i:02d}")
        out.add(f"{(y0 - 1):04d}-{mo_i:02d}-{d_i:02d}")

    m3b = _CN_MD_RE.search(s)
    if m3b:
        mo = _cn_int(m3b.group(1))
        d = _cn_int(m3b.group(2))
        if mo and d:
            mo_i = max(1, min(12, int(mo)))
            d_i = max(1, min(31, int(d)))
            y0 = datetime.now(timezone.utc).year
            out.add(f"{y0:04d}-{mo_i:02d}-{d_i:02d}")
            out.add(f"{(y0 - 1):04d}-{mo_i:02d}-{d_i:02d}")

    return sorted(out)


@dataclass(frozen=True)
class StructuredRecallResult:
    hits: list[dict[str, Any]]
    date_norms: list[str]


def structured_recall_by_date(sb: Any, *, query: str, rewritten: str, limit_rows: int = 6) -> StructuredRecallResult:
    """
    结构化召回：优先按 metadata.date_norm / filename / slug / relativePath 精确匹配。
    - 不依赖 FTS 分词
    - 不依赖向量 embedding
    """
    date_norms = date_norm_candidates_for_structured(query) or date_norm_candidates_for_structured(rewritten)
    if not date_norms:
        return StructuredRecallResult(hits=[], date_norms=[])

    hits: list[dict[str, Any]] = []

    def _append(rows: Any) -> None:
        if isinstance(rows, list):
            for r in rows:
                if isinstance(r, dict) and r.get("id") is not None:
                    hits.append(r)

    def _dedup_limit(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        seen: set[Any] = set()
        out: list[dict[str, Any]] = []
        for h in rows:
            hid = h.get("id")
            if hid in seen:
                continue
            seen.add(hid)
            out.append(h)
            if len(out) >= limit_rows:
                break
        return out

    # 1) date_norm
    for dn in date_norms:
        res = sb.table("documents").select("id, content, metadata").eq("metadata->>date_norm", dn).limit(limit_rows).execute()
        _append(res.data)
        if len(hits) >= limit_rows:
            return StructuredRecallResult(hits=_dedup_limit(hits), date_norms=date_norms)

    # 2) 兼容旧数据：slug/filename/relativePath
    for dn in date_norms:
        y, mo, d = dn.split("-")
        mo_i, d_i = int(mo), int(d)
        slug1 = f"{y}-{mo_i}-{d_i}"
        slug2 = f"{y}-{mo}-{d}"
        for slug in (slug1, slug2):
            res = sb.table("documents").select("id, content, metadata").eq("metadata->>slug", slug).limit(limit_rows).execute()
            _append(res.data)
        fn1 = f"{y}-{mo_i}-{d_i}.md"
        fn2 = f"{y}-{mo}-{d}.md"
        for fn in (fn1, fn2):
            res = sb.table("documents").select("id, content, metadata").eq("metadata->>filename", fn).limit(limit_rows).execute()
            _append(res.data)
        rel1 = f"diary/{y}-{mo_i}-{d_i}.md"
        rel2 = f"diary/{y}-{mo}-{d}.md"
        for rel in (rel1, rel2):
            res = sb.table("documents").select("id, content, metadata").eq("metadata->>relativePath", rel).limit(limit_rows).execute()
            _append(res.data)

    return StructuredRecallResult(hits=_dedup_limit(hits), date_norms=date_norms)

