# -*- coding: utf-8 -*-
"""JSON解析.扫描模块 —— 汉语库（由 tools/汉化库.py 从 Lib/json/scanner.py 机械生成，**不要手改**）。

英文库 Lib/json.scanner.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py json
"""


"""JSON token scanner
"""
_英文原名表 = {'py_make_scanner': '纯Python造扫描器'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import re
try:
    from _json import make_scanner as c_make_scanner
except ImportError:
    c_make_scanner = None
__all__ = ['make_scanner']
NUMBER_RE = re.compile('(-?(?:0|[1-9][0-9]*))(\\.[0-9]+)?([eE][-+]?[0-9]+)?', re.VERBOSE | re.MULTILINE | re.DOTALL)

def 纯Python造扫描器(context):
    parse_object = context.parse_object
    parse_array = context.parse_array
    parse_string = context.parse_string
    match_number = NUMBER_RE.match
    严格 = context.strict
    parse_float = context.parse_float
    parse_int = context.parse_int
    parse_constant = context.parse_constant
    object_hook = context.object_hook
    object_pairs_hook = context.object_pairs_hook
    memo = context.memo

    def _scan_once(string, idx):
        try:
            nextchar = string[idx]
        except IndexError:
            raise StopIteration(idx) from None
        if nextchar == '"':
            return parse_string(string, idx + 1, 严格)
        elif nextchar == '{':
            return parse_object((string, idx + 1), 严格, _scan_once, object_hook, object_pairs_hook, memo)
        elif nextchar == '[':
            return parse_array((string, idx + 1), _scan_once)
        elif nextchar == 'n' and string[idx:idx + 4] == 'null':
            return (None, idx + 4)
        elif nextchar == 't' and string[idx:idx + 4] == 'true':
            return (True, idx + 4)
        elif nextchar == 'f' and string[idx:idx + 5] == 'false':
            return (False, idx + 5)
        m = match_number(string, idx)
        if m is not None:
            integer, frac, exp = m.groups()
            if frac or exp:
                res = parse_float(integer + (frac or '') + (exp or ''))
            else:
                res = parse_int(integer)
            return (res, m.end())
        elif nextchar == 'N' and string[idx:idx + 3] == 'NaN':
            return (parse_constant('NaN'), idx + 3)
        elif nextchar == 'I' and string[idx:idx + 8] == 'Infinity':
            return (parse_constant('Infinity'), idx + 8)
        elif nextchar == '-' and string[idx:idx + 9] == '-Infinity':
            return (parse_constant('-Infinity'), idx + 9)
        else:
            raise StopIteration(idx)

    def scan_once(string, idx):
        try:
            return _scan_once(string, idx)
        finally:
            memo.clear()
    return scan_once
make_scanner = c_make_scanner or 纯Python造扫描器


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'py_make_scanner': '纯Python造扫描器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
