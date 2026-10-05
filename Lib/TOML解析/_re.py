# -*- coding: utf-8 -*-
"""TOML解析._re —— 汉语库（由 tools/汉化库.py 从 Lib/tomllib/_re.py 机械生成，**不要手改**）。

英文库 Lib/tomllib._re.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py tomllib
"""


from __future__ import annotations
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from functools import lru_cache
import re
TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any
    from ._types import ParseFloat
_TIME_RE_STR = '([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(?:\\.([0-9]{1,6})[0-9]*)?'
RE_NUMBER = re.compile('\n0\n(?:\n    x[0-9A-Fa-f](?:_?[0-9A-Fa-f])*   # hex\n    |\n    b[01](?:_?[01])*                 # bin\n    |\n    o[0-7](?:_?[0-7])*               # oct\n)\n|\n[+-]?(?:0|[1-9](?:_?[0-9])*)         # dec, integer part\n(?P<floatpart>\n    (?:\\.[0-9](?:_?[0-9])*)?         # optional fractional part\n    (?:[eE][+-]?[0-9](?:_?[0-9])*)?  # optional exponent part\n)\n', flags=re.VERBOSE)
RE_LOCALTIME = re.compile(_TIME_RE_STR)
RE_DATETIME = re.compile(f'\n([0-9]{{4}})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])  # date, e.g. 1988-10-27\n(?:\n    [Tt ]\n    {_TIME_RE_STR}\n    (?:([Zz])|([+-])([01][0-9]|2[0-3]):([0-5][0-9]))?  # optional time offset\n)?\n', flags=re.VERBOSE)

def match_to_datetime(match: re.Match[str]) -> datetime | date:
    """Convert a `RE_DATETIME` match to `datetime.datetime` or `datetime.date`.

    Raises ValueError if the match does not correspond to a valid date
    or datetime.
    """
    year_str, month_str, day_str, hour_str, minute_str, sec_str, micros_str, zulu_time, offset_sign_str, offset_hour_str, offset_minute_str = match.groups()
    year, month, day = (int(year_str), int(month_str), int(day_str))
    if hour_str is None:
        return date(year, month, day)
    hour, minute, sec = (int(hour_str), int(minute_str), int(sec_str))
    micros = int(micros_str.ljust(6, '0')) if micros_str else 0
    if offset_sign_str:
        tz: tzinfo | None = cached_tz(offset_hour_str, offset_minute_str, offset_sign_str)
    elif zulu_time:
        tz = timezone.utc
    else:
        tz = None
    return datetime(year, month, day, hour, minute, sec, micros, tzinfo=tz)

@lru_cache(maxsize=None)
def cached_tz(hour_str: str, minute_str: str, sign_str: str) -> timezone:
    sign = 1 if sign_str == '+' else -1
    return timezone(timedelta(hours=sign * int(hour_str), minutes=sign * int(minute_str)))

def match_to_localtime(match: re.Match[str]) -> time:
    hour_str, minute_str, sec_str, micros_str = match.groups()
    micros = int(micros_str.ljust(6, '0')) if micros_str else 0
    return time(int(hour_str), int(minute_str), int(sec_str), micros)

def match_to_number(match: re.Match[str], parse_float: ParseFloat) -> Any:
    if match.group('floatpart'):
        return parse_float(match.group())
    return int(match.group(), 0)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
