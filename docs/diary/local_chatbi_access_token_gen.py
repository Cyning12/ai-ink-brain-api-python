#!/usr/bin/env python3
"""
本地生成 ChatBI `chatbi_access_tokens.key_hash` 与 INSERT 模板（勿提交明文 token）。

哈希算法须与运行时 `api/chatbi_access_hash.py::hash_chatbi_access_token` 一致：
  SHA256( (CHATBI_ACCESS_TOKEN_PEPPER 或空).encode() + 明文 token bytes ).hexdigest() 小写

用法（仓库根）：
  python3 docs/diary/local_chatbi_access_token_gen.py --level 0 --label super-demo
  python3 docs/diary/local_chatbi_access_token_gen.py --level 2 --subject-user-id u_demo_001 --label l2-demo
  # 带到期：自「当前北京时间」起 90 天后（写入 DB 为 timestamptz / UTC 瞬时点）
  python3 docs/diary/local_chatbi_access_token_gen.py --level 2 --subject-user-id u1 --label l2-temp --expires-in-days 90
  # 固定时刻：无时区则按 **北京时间**；含 +08:00 / Z 则按该时区解析
  python3 docs/diary/local_chatbi_access_token_gen.py --level 1 --label admin-temp --expires-at 2027-06-01T00:00:00
  # 自当前时刻起 120 分钟后过期（分钟可小数，如 30.5）
  python3 docs/diary/local_chatbi_access_token_gen.py --level 2 --subject-user-id u1 --label l2-short --expires-in-minutes 120

**时区口径**：
- **运行时**（`api/chatbi_principal.py`）：`expires_at` 与当前时刻比较在 **UTC 瞬时点** 上进行；若接口/驱动返回 **无时区** 字符串，按 **Asia/Shanghai（北京时间）** 绑定后再转 UTC。
- **本脚本**：`--expires-in-days` / `--expires-in-minutes` 的「当前」取 **北京时间** 锚定的同一物理时刻；`--expires-at` **无时区** 时默认 **北京时间**；写入 SQL 的 `timestamptz '…'` 为 **UTC 的 ISO 表示**（与 Supabase 一致）。

**当前默认有效期**：INSERT **不写** `expires_at` → 库中为 **NULL** → 运行时 **不因过期拒绝**（与 L0/L1/L2 档位无关，仅看列是否有值）。

说明：本文件位于 `docs/diary/`，受仓库 `.gitignore` 中 `docs/*` 例外策略影响，默认不参与 Git 跟踪；
      若你曾 `git add -f` 过 diary，请勿将含真实 token 的输出提交到 GitHub。
"""

from __future__ import annotations

import argparse
import os
import secrets
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

# 允许从任意 cwd 运行：把仓库根加入 path 以复用运行时哈希实现
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from api.chatbi_access_hash import hash_chatbi_access_token  # noqa: E402


def _gen_plain_token(*, nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)


_SHANGHAI = ZoneInfo("Asia/Shanghai")


def _utc_now_anchor() -> datetime:
    """当前瞬间，以 UTC aware 表示（与北京时间同一物理时刻）。"""
    return datetime.now(_SHANGHAI).astimezone(timezone.utc)


def _parse_expires_at_iso(s: str) -> datetime:
    """解析 ISO8601，归一化为 UTC aware datetime。无时区时默认 **北京时间**。"""
    t = s.strip()
    if not t:
        raise ValueError("empty expires-at")
    # 兼容 Z 结尾（显式 UTC）
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    dt = datetime.fromisoformat(t)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=_SHANGHAI)
    return dt.astimezone(timezone.utc)


def main() -> None:
    p = argparse.ArgumentParser(description="生成 chatbi_access_tokens 的 key_hash 与 INSERT SQL 模板")
    p.add_argument("--level", type=int, required=True, choices=(0, 1, 2), help="0=Super 1=Admin 2=L2")
    p.add_argument("--subject-user-id", default="", help="L2 必填，与 chatbi_user_portrait.user_id 一致")
    p.add_argument("--label", default="manual", help="令牌备注 label")
    p.add_argument("--plain-token", default="", help="指定明文 token；不设则随机生成")
    p.add_argument("--token-bytes", type=int, default=32, help="随机明文长度（仅未指定 --plain-token 时）")
    p.add_argument(
        "--expires-in-days",
        type=float,
        default=None,
        help="expires_at = 当前时刻 + N 天（可小数）；与 --expires-in-minutes、--expires-at 三选一",
    )
    p.add_argument(
        "--expires-in-minutes",
        type=float,
        default=None,
        help="expires_at = 当前时刻 + N 分钟（可小数，如 90 或 30.5）；与 --expires-in-days、--expires-at 三选一",
    )
    p.add_argument(
        "--expires-at",
        default="",
        help="固定到期 ISO8601；无时区默认 **北京时间**；含偏移或 Z 则按该时区。与上述相对时间参数互斥",
    )
    args = p.parse_args()

    if args.level == 2 and not (args.subject_user_id or "").strip():
        p.error("L2 (--level 2) 必须提供 --subject-user-id")

    expire_specs = [
        args.expires_in_days is not None,
        args.expires_in_minutes is not None,
        bool((args.expires_at or "").strip()),
    ]
    if sum(expire_specs) > 1:
        p.error("--expires-at、--expires-in-days、--expires-in-minutes 仅能使用其中一个")

    expires_at_utc: datetime | None = None
    if args.expires_in_days is not None:
        if args.expires_in_days <= 0:
            p.error("--expires-in-days 须为正数")
        expires_at_utc = _utc_now_anchor() + timedelta(days=float(args.expires_in_days))
    elif args.expires_in_minutes is not None:
        if args.expires_in_minutes <= 0:
            p.error("--expires-in-minutes 须为正数")
        expires_at_utc = _utc_now_anchor() + timedelta(minutes=float(args.expires_in_minutes))
    elif (args.expires_at or "").strip():
        try:
            expires_at_utc = _parse_expires_at_iso(args.expires_at)
        except ValueError as e:
            p.error(f"无法解析 --expires-at: {e}")

    plain = (args.plain_token or "").strip() or _gen_plain_token(nbytes=max(16, int(args.token_bytes)))
    key_hash = hash_chatbi_access_token(plain)
    subj_sql = "null" if not (args.subject_user_id or "").strip() else "'" + (args.subject_user_id or "").replace("'", "''") + "'"

    print("--- 明文 token（仅本地保存，勿提交日志/仓库）---")
    print(plain)
    print()
    print("--- key_hash（写入 DB）---")
    print(key_hash)
    print()
    print("--- 可选环境（与哈希一致）---")
    print(f"CHATBI_ACCESS_TOKEN_PEPPER={os.environ.get('CHATBI_ACCESS_TOKEN_PEPPER', '')!r}")
    print()
    if expires_at_utc is not None:
        exp_sql = expires_at_utc.isoformat()
        exp_cn = expires_at_utc.astimezone(_SHANGHAI).strftime("%Y-%m-%d %H:%M:%S %Z")
        print("--- expires_at（timestamptz，INSERT 内为 UTC ISO）---")
        print(exp_sql)
        print(f"（北京时间: {exp_cn}）")
        print()
    print("--- Supabase / psql 用 INSERT（自行执行，勿含明文 key_hash 以外的 token）---")
    label_esc = (args.label or "manual").replace("'", "''")
    if expires_at_utc is not None:
        exp_sql = expires_at_utc.isoformat()
        print(
            f"insert into public.chatbi_access_tokens (key_hash, access_level, subject_user_id, label, expires_at)\n"
            f"values ('{key_hash}', {int(args.level)}, {subj_sql}, '{label_esc}', timestamptz '{exp_sql}');"
        )
    else:
        print(
            f"insert into public.chatbi_access_tokens (key_hash, access_level, subject_user_id, label)\n"
            f"values ('{key_hash}', {int(args.level)}, {subj_sql}, '{label_esc}');"
        )


if __name__ == "__main__":
    main()
