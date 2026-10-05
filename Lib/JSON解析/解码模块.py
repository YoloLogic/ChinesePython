# -*- coding: utf-8 -*-
"""JSON解析.解码模块 —— 汉语库（由 tools/汉化库.py 从 Lib/json/decoder.py 机械生成，**不要手改**）。

英文库 Lib/json.decoder.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py json
"""


"""Implementation of JSONDecoder
"""
_英文原名表 = {'JSONArray': '数组类型', 'JSONDecodeError': '解码错误', 'JSONDecoder': '解码器', 'JSONObject': '对象类型', 'py_scanstring': '纯Python扫描', 'scanstring': '扫描字符串'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import re
from JSON解析 import 扫描模块
try:
    from _json import scanstring as c_scanstring
except ImportError:
    c_scanstring = None
__all__ = ['JSONDecoder', 'JSONDecodeError']
FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
NaN = float('nan')
PosInf = float('inf')
NegInf = float('-inf')

class 解码错误(ValueError):
    """Subclass of ValueError with the following additional properties:

    msg: The unformatted error message
    doc: The JSON document being parsed
    pos: The start index of doc where parsing failed
    lineno: The line corresponding to pos
    colno: The column corresponding to pos

    """

    def __init__(self, msg, doc, pos):
        lineno = doc.count('\n', 0, pos) + 1
        colno = pos - doc.rfind('\n', 0, pos)
        errmsg = '%s: line %d column %d (char %d)' % (msg, lineno, colno, pos)
        ValueError.__init__(self, errmsg)
        self.msg = msg
        self.doc = doc
        self.pos = pos
        self.lineno = lineno
        self.colno = colno

    def __reduce__(self):
        return (self.__class__, (self.msg, self.doc, self.pos))
import json.decoder as _英文身份源
解码错误 = _英文身份源.JSONDecodeError
_CONSTANTS = {'-Infinity': NegInf, 'Infinity': PosInf, 'NaN': NaN}
HEXDIGITS = re.compile('[0-9A-Fa-f]{4}', FLAGS)
STRINGCHUNK = re.compile('(.*?)(["\\\\\\x00-\\x1f])', FLAGS)
BACKSLASH = {'"': '"', '\\': '\\', '/': '/', 'b': '\x08', 'f': '\x0c', 'n': '\n', 'r': '\r', 't': '\t'}

def _decode_uXXXX(s, pos, _m=HEXDIGITS.match):
    esc = _m(s, pos + 1)
    if esc is not None:
        try:
            return int(esc.group(), 16)
        except ValueError:
            pass
    msg = 'Invalid \\uXXXX escape'
    raise 解码错误(msg, s, pos)

def 纯Python扫描(s, end, strict=True, _b=BACKSLASH, _m=STRINGCHUNK.match):
    """Scan the string s for a JSON string. End is the index of the
    character in s after the quote that started the JSON string.
    Unescapes all valid JSON string escape sequences and raises ValueError
    on attempt to decode an invalid string. If strict is False then literal
    control characters are allowed in the string.

    Returns a tuple of the decoded string and the index of the character in s
    after the end quote."""
    chunks = []
    _append = chunks.append
    begin = end - 1
    while 1:
        chunk = _m(s, end)
        if chunk is None:
            raise 解码错误('Unterminated string starting at', s, begin)
        end = chunk.end()
        content, terminator = chunk.groups()
        if content:
            _append(content)
        if terminator == '"':
            break
        elif terminator != '\\':
            if strict:
                msg = 'Invalid control character {0!r} at'.format(terminator)
                raise 解码错误(msg, s, end - 1)
            else:
                _append(terminator)
                continue
        try:
            esc = s[end]
        except IndexError:
            raise 解码错误('Unterminated string starting at', s, begin) from None
        if esc != 'u':
            try:
                char = _b[esc]
            except KeyError:
                msg = 'Invalid \\escape: {0!r}'.format(esc)
                raise 解码错误(msg, s, end)
            end += 1
        else:
            uni = _decode_uXXXX(s, end)
            end += 5
            if 55296 <= uni <= 56319 and s[end:end + 2] == '\\u':
                uni2 = _decode_uXXXX(s, end + 1)
                if 56320 <= uni2 <= 57343:
                    uni = 65536 + (uni - 55296 << 10 | uni2 - 56320)
                    end += 6
            char = chr(uni)
        _append(char)
    return (''.join(chunks), end)
扫描字符串 = c_scanstring or 纯Python扫描
WHITESPACE = re.compile('[ \\t\\n\\r]*', FLAGS)
WHITESPACE_STR = ' \t\n\r'

def 对象类型(s_and_end, strict, scan_once, object_hook, object_pairs_hook, memo=None, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
    s, 末尾 = s_and_end
    pairs = []
    pairs_append = pairs.append
    if memo is None:
        memo = {}
    memo_get = memo.setdefault
    nextchar = s[末尾:末尾 + 1]
    if nextchar != '"':
        if nextchar in _ws:
            末尾 = _w(s, 末尾).end()
            nextchar = s[末尾:末尾 + 1]
        if nextchar == '}':
            if object_pairs_hook is not None:
                result = object_pairs_hook(pairs)
                return (result, 末尾 + 1)
            pairs = {}
            if object_hook is not None:
                pairs = object_hook(pairs)
            return (pairs, 末尾 + 1)
        elif nextchar != '"':
            raise 解码错误('Expecting property name enclosed in double quotes', s, 末尾)
    末尾 += 1
    while True:
        key, 末尾 = 扫描字符串(s, 末尾, strict)
        key = memo_get(key, key)
        if s[末尾:末尾 + 1] != ':':
            末尾 = _w(s, 末尾).end()
            if s[末尾:末尾 + 1] != ':':
                raise 解码错误("Expecting ':' delimiter", s, 末尾)
        末尾 += 1
        try:
            if s[末尾] in _ws:
                末尾 += 1
                if s[末尾] in _ws:
                    末尾 = _w(s, 末尾 + 1).end()
        except IndexError:
            pass
        try:
            value, 末尾 = scan_once(s, 末尾)
        except StopIteration as err:
            raise 解码错误('Expecting value', s, err.value) from None
        pairs_append((key, value))
        try:
            nextchar = s[末尾]
            if nextchar in _ws:
                末尾 = _w(s, 末尾 + 1).end()
                nextchar = s[末尾]
        except IndexError:
            nextchar = ''
        末尾 += 1
        if nextchar == '}':
            break
        elif nextchar != ',':
            raise 解码错误("Expecting ',' delimiter", s, 末尾 - 1)
        comma_idx = 末尾 - 1
        末尾 = _w(s, 末尾).end()
        nextchar = s[末尾:末尾 + 1]
        末尾 += 1
        if nextchar != '"':
            if nextchar == '}':
                raise 解码错误('Illegal trailing comma before end of object', s, comma_idx)
            raise 解码错误('Expecting property name enclosed in double quotes', s, 末尾 - 1)
    if object_pairs_hook is not None:
        result = object_pairs_hook(pairs)
        return (result, 末尾)
    pairs = dict(pairs)
    if object_hook is not None:
        pairs = object_hook(pairs)
    return (pairs, 末尾)

def 数组类型(s_and_end, scan_once, _w=WHITESPACE.match, _ws=WHITESPACE_STR):
    s, 末尾 = s_and_end
    values = []
    nextchar = s[末尾:末尾 + 1]
    if nextchar in _ws:
        末尾 = _w(s, 末尾 + 1).end()
        nextchar = s[末尾:末尾 + 1]
    if nextchar == ']':
        return (values, 末尾 + 1)
    _append = values.append
    while True:
        try:
            value, 末尾 = scan_once(s, 末尾)
        except StopIteration as err:
            raise 解码错误('Expecting value', s, err.value) from None
        _append(value)
        nextchar = s[末尾:末尾 + 1]
        if nextchar in _ws:
            末尾 = _w(s, 末尾 + 1).end()
            nextchar = s[末尾:末尾 + 1]
        末尾 += 1
        if nextchar == ']':
            break
        elif nextchar != ',':
            raise 解码错误("Expecting ',' delimiter", s, 末尾 - 1)
        comma_idx = 末尾 - 1
        try:
            if s[末尾] in _ws:
                末尾 += 1
                if s[末尾] in _ws:
                    末尾 = _w(s, 末尾 + 1).end()
            nextchar = s[末尾:末尾 + 1]
        except IndexError:
            pass
        if nextchar == ']':
            raise 解码错误('Illegal trailing comma before end of array', s, comma_idx)
    return (values, 末尾)

class 解码器(object):
    """Simple JSON <https://json.org> decoder

    Performs the following translations in decoding by default:

    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | str               |
    +---------------+-------------------+
    | number (int)  | int               |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+

    It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as
    their corresponding ``float`` values, which is outside the JSON spec.

    """

    def __init__(self, *, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, strict=True, object_pairs_hook=None):
        """``object_hook``, if specified, will be called with the result
        of every JSON object decoded and its return value will be used in
        place of the given ``dict``.  This can be used to provide custom
        deserializations (e.g. to support JSON-RPC class hinting).

        ``object_pairs_hook``, if specified will be called with the result
        of every JSON object decoded with an ordered list of pairs.  The
        return value of ``object_pairs_hook`` will be used instead of the
        ``dict``.  This feature can be used to implement custom decoders.
        If ``object_hook`` is also defined, the ``object_pairs_hook`` takes
        priority.

        ``parse_float``, if specified, will be called with the string
        of every JSON float to be decoded. By default this is equivalent to
        float(num_str). This can be used to use another datatype or parser
        for JSON floats (e.g. decimal.Decimal).

        ``parse_int``, if specified, will be called with the string
        of every JSON int to be decoded. By default this is equivalent to
        int(num_str). This can be used to use another datatype or parser
        for JSON integers (e.g. float).

        ``parse_constant``, if specified, will be called with one of the
        following strings: -Infinity, Infinity, NaN.
        This can be used to raise an exception if invalid JSON numbers
        are encountered.

        If ``strict`` is false (true is the default), then control
        characters will be allowed inside strings.  Control characters in
        this context are those with character codes in the 0-31 range,
        including ``'\\t'`` (tab), ``'\\n'``, ``'\\r'`` and ``'\\0'``.
        """
        self.object_hook = object_hook
        self.parse_float = parse_float or float
        self.parse_int = parse_int or int
        self.parse_constant = parse_constant or _CONSTANTS.__getitem__
        self.strict = strict
        self.object_pairs_hook = object_pairs_hook
        self.parse_object = 对象类型
        self.parse_array = 数组类型
        self.parse_string = 扫描字符串
        self.memo = {}
        self.scan_once = 扫描模块.make_scanner(self)

    def 解码(self, s, _w=WHITESPACE.match):
        """Return the Python representation of ``s`` (a ``str`` instance
        containing a JSON document).

        """
        obj, 末尾 = self.原始解码(s, idx=_w(s, 0).end())
        末尾 = _w(s, 末尾).end()
        if 末尾 != len(s):
            raise 解码错误('Extra data', s, 末尾)
        return obj

    def 原始解码(self, s, idx=0):
        """Decode a JSON document from ``s`` (a ``str`` beginning with
        a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.

        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.

        """
        try:
            obj, 末尾 = self.scan_once(s, idx)
        except StopIteration as err:
            raise 解码错误('Expecting value', s, err.value) from None
        return (obj, 末尾)
_装类转发(解码器, {'decode': '解码', 'raw_decode': '原始解码'}, {'decode': '解码', 'raw_decode': '原始解码'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import json.decoder as _英文库
解码错误 = _英文库.JSONDecodeError
_模块别名 = {
    'JSONArray': '数组类型',
    'JSONDecodeError': '解码错误',
    'JSONDecoder': '解码器',
    'JSONObject': '对象类型',
    'py_scanstring': '纯Python扫描',
    'scanstring': '扫描字符串',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '解码器': {
        'decode': '解码',
        'raw_decode': '原始解码',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '解码器': {
        'decode': '解码',
        'raw_decode': '原始解码',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '解码器',
    '解码错误',
])

# ---- 转发层结束 ----
