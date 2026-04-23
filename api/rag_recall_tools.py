from __future__ import annotations

import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


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
    q = (query or "").strip()
    if not q:
        return q

    out: set[str] = set()

    # 日期候选（用于 FTS 日期形态差异）
    out.update(date_candidates_for_keyword(q))

    # 版本号候选（用于 0-1-0 这类 FTS 不友好形态的 query-side 归一化）
    # 注意：这里用 OR 扩展 query_text，不要求文档侧一定产生同形态 token。
    for m in _VER3_RE.finditer(q):
        a, b, c = m.group(1), m.group(2), m.group(3)
        out.add(f"{a}.{b}.{c}")
        out.add(f"v{a}.{b}.{c}")
        out.add(f"{a}_{b}_{c}")
        out.add(f"{a}-{b}-{c}")

    if not out:
        return q
    parts = [f"\"{c}\"" for c in sorted(out)]
    return " OR ".join(parts)


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

