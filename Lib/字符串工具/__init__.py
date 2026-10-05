# -*- coding: utf-8 -*-
"""字符串工具.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/string/__init__.py 机械生成，**不要手改**）。

英文库 Lib/string.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py string
"""


"""A collection of string constants.

Public module variables:

whitespace -- a string containing all ASCII whitespace
ascii_lowercase -- a string containing all ASCII lowercase letters
ascii_uppercase -- a string containing all ASCII uppercase letters
ascii_letters -- a string containing all ASCII letters
digits -- a string containing all ASCII decimal digits
hexdigits -- a string containing all ASCII hexadecimal digits
octdigits -- a string containing all ASCII octal digits
punctuation -- a string containing all ASCII punctuation characters
printable -- a string containing all ASCII characters considered printable

"""
_英文原名表 = {'Formatter': '格式化器', 'Template': '模板', 'ascii_letters': 'ASCII字母', 'ascii_lowercase': 'ASCII小写', 'ascii_uppercase': 'ASCII大写', 'capwords': '首字母大写', 'digits': '数字', 'hexdigits': '十六进制数字', 'octdigits': '八进制数字', 'printable': '可打印字符', 'punctuation': '标点', 'whitespace': '空白'}

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
__all__ = ['ascii_letters', 'ascii_lowercase', 'ascii_uppercase', 'capwords', 'digits', 'hexdigits', 'octdigits', 'printable', 'punctuation', 'whitespace', 'Formatter', 'Template']
import _string
空白 = ' \t\n\r\x0b\x0c'
ASCII小写 = 'abcdefghijklmnopqrstuvwxyz'
ASCII大写 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
ASCII字母 = ASCII小写 + ASCII大写
数字 = '0123456789'
十六进制数字 = 数字 + 'abcdef' + 'ABCDEF'
八进制数字 = '01234567'
标点 = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
可打印字符 = 数字 + ASCII字母 + 标点 + 空白

def 首字母大写(s, sep=None):
    """capwords(s [,sep]) -> string

    Split the argument into words using split, capitalize each
    word using capitalize, and join the capitalized words using
    join.  If the optional second argument sep is absent or None,
    runs of whitespace characters are replaced by a single space
    and leading and trailing whitespace are removed, otherwise
    sep is used to split and join the words.

    """
    return (sep or ' ').join(map(str.capitalize, s.split(sep)))
_sentinel_dict = {}

class _TemplatePattern:

    def __get__(self, instance, cls=None):
        if cls is None:
            return self
        return cls._compile_pattern()
_TemplatePattern = _TemplatePattern()

class 模板:
    """A string class for supporting $-substitutions."""
    delimiter = '$'
    idpattern = '(?a:[_a-z][_a-z0-9]*)'
    braceidpattern = None
    flags = None
    模式 = _TemplatePattern

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._compile_pattern()

    @classmethod
    def _compile_pattern(cls):
        import re
        模式 = cls.__dict__.get('pattern', _TemplatePattern)
        if isinstance(模式, re.Pattern):
            return 模式
        if 模式 is _TemplatePattern:
            delim = re.escape(cls.delimiter)
            id = cls.idpattern
            bid = cls.braceidpattern or cls.idpattern
            模式 = f'\n            {delim}(?:\n              (?P<escaped>{delim})  |   # Escape sequence of two delimiters\n              (?P<named>{id})       |   # delimiter and a Python identifier\n              {{(?P<braced>{bid})}} |   # delimiter and a braced identifier\n              (?P<invalid>)             # Other ill-formed delimiter exprs\n            )\n            '
        if cls.flags is None:
            cls.flags = re.IGNORECASE
        pat = cls.模式 = re.compile(模式, cls.flags | re.VERBOSE)
        return pat

    def __init__(self, template):
        self.template = template

    def _invalid(self, mo):
        i = mo.start('invalid')
        lines = self.template[:i].splitlines(keepends=True)
        if not lines:
            colno = 1
            lineno = 1
        else:
            colno = i - len(''.join(lines[:-1]))
            lineno = len(lines)
        raise ValueError('Invalid placeholder in string: line %d, col %d' % (lineno, colno))

    def 替换(self, mapping=_sentinel_dict, /, **kws):
        if mapping is _sentinel_dict:
            mapping = kws
        elif kws:
            from collections import ChainMap
            mapping = ChainMap(kws, mapping)

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                return str(mapping[named])
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern', self.模式)
        return self.模式.sub(convert, self.template)

    def 安全替换(self, mapping=_sentinel_dict, /, **kws):
        if mapping is _sentinel_dict:
            mapping = kws
        elif kws:
            from collections import ChainMap
            mapping = ChainMap(kws, mapping)

        def convert(mo):
            named = mo.group('named') or mo.group('braced')
            if named is not None:
                try:
                    return str(mapping[named])
                except KeyError:
                    return mo.group()
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                return mo.group()
            raise ValueError('Unrecognized named group in pattern', self.模式)
        return self.模式.sub(convert, self.template)

    def 有效吗(self):
        for mo in self.模式.finditer(self.template):
            if mo.group('invalid') is not None:
                return False
            if mo.group('named') is None and mo.group('braced') is None and (mo.group('escaped') is None):
                raise ValueError('Unrecognized named group in pattern', self.模式)
        return True

    def 取标识符(self):
        ids = []
        for mo in self.模式.finditer(self.template):
            named = mo.group('named') or mo.group('braced')
            if named is not None and named not in ids:
                ids.append(named)
            elif named is None and mo.group('invalid') is None and (mo.group('escaped') is None):
                raise ValueError('Unrecognized named group in pattern', self.模式)
        return ids
_装类转发(模板, {'get_identifiers': '取标识符', 'is_valid': '有效吗', 'pattern': '模式', 'safe_substitute': '安全替换', 'substitute': '替换'}, {'get_identifiers': '取标识符', 'is_valid': '有效吗', 'pattern': '模式', 'safe_substitute': '安全替换', 'substitute': '替换'})

class 格式化器:

    def format(self, format_string, /, *args, **kwargs):
        return self.vformat(format_string, args, kwargs)

    def vformat(self, format_string, args, kwargs):
        used_args = set()
        result, _ = self._vformat(format_string, args, kwargs, used_args, 2)
        self.check_unused_args(used_args, args, kwargs)
        return result

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth, auto_arg_index=0):
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')
        result = []
        for literal_text, field_name, format_spec, conversion in self.parse(format_string):
            if literal_text:
                result.append(literal_text)
            if field_name is not None:
                field_first, _ = _string.formatter_field_name_split(field_name)
                if field_first == '':
                    if auto_arg_index is False:
                        raise ValueError('cannot switch from manual field specification to automatic field numbering')
                    field_name = str(auto_arg_index) + field_name
                    auto_arg_index += 1
                elif isinstance(field_first, int):
                    if auto_arg_index:
                        raise ValueError('cannot switch from automatic field numbering to manual field specification')
                    auto_arg_index = False
                obj, arg_used = self.get_field(field_name, args, kwargs)
                used_args.add(arg_used)
                obj = self.convert_field(obj, conversion)
                format_spec, auto_arg_index = self._vformat(format_spec, args, kwargs, used_args, recursion_depth - 1, auto_arg_index=auto_arg_index)
                result.append(self.format_field(obj, format_spec))
        return (''.join(result), auto_arg_index)

    def get_value(self, key, args, kwargs):
        if isinstance(key, int):
            return args[key]
        else:
            return kwargs[key]

    def check_unused_args(self, used_args, args, kwargs):
        pass

    def format_field(self, value, format_spec):
        return format(value, format_spec)

    def convert_field(self, value, conversion):
        if conversion is None:
            return value
        elif conversion == 's':
            return str(value)
        elif conversion == 'r':
            return repr(value)
        elif conversion == 'a':
            return ascii(value)
        raise ValueError('Unknown conversion specifier {0!s}'.format(conversion))

    def parse(self, format_string):
        return _string.formatter_parser(format_string)

    def get_field(self, field_name, args, kwargs):
        first, rest = _string.formatter_field_name_split(field_name)
        obj = self.get_value(first, args, kwargs)
        for is_attr, i in rest:
            if is_attr:
                obj = getattr(obj, i)
            else:
                obj = obj[i]
        return (obj, first)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 子模块的英文名也留着（照「英文原名一个都不能少」）：
# `JSON解析.decoder` 跟 `JSON解析.解码模块` 是**同一个模块对象**。
from . import 模板库 as templatelib
_模块别名 = {
    'Formatter': '格式化器',
    'Template': '模板',
    'ascii_letters': 'ASCII字母',
    'ascii_lowercase': 'ASCII小写',
    'ascii_uppercase': 'ASCII大写',
    'capwords': '首字母大写',
    'digits': '数字',
    'hexdigits': '十六进制数字',
    'octdigits': '八进制数字',
    'printable': '可打印字符',
    'punctuation': '标点',
    'whitespace': '空白',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '模板': {
        'get_identifiers': '取标识符',
        'is_valid': '有效吗',
        'pattern': '模式',
        'safe_substitute': '安全替换',
        'substitute': '替换',
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
    '模板': {
        'get_identifiers': '取标识符',
        'is_valid': '有效吗',
        'pattern': '模式',
        'safe_substitute': '安全替换',
        'substitute': '替换',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'ASCII大写',
    'ASCII字母',
    'ASCII小写',
    '八进制数字',
    '十六进制数字',
    '可打印字符',
    '数字',
    '标点',
    '格式化器',
    '模板',
    '空白',
    '首字母大写',
])

# ---- 转发层结束 ----
