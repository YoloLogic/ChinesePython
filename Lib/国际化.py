# -*- coding: utf-8 -*-
"""国际化 —— 汉语库（由 tools/汉化库.py 从 Lib/gettext.py 机械生成，**不要手改**）。

英文库 Lib/gettext.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 国际化
"""


"""Internationalization and localization support.

This module provides internationalization (I18N) and localization (L10N)
support for your Python programs by providing an interface to the GNU gettext
message catalog library.

I18N refers to the operation by which a program is made aware of multiple
languages.  L10N refers to the adaptation of your program, once
internationalized, to the local language and cultural habits.

"""
_英文原名表 = {'Catalog': '翻译目录', 'GNUTranslations': 'GNU翻译', 'NullTranslations': '空翻译', 'bindtextdomain': '绑定文本域', 'c2py': '复数式转Python', 'dgettext': '按域取翻译', 'dngettext': '按域取复数翻译', 'dnpgettext': '按域按上下文取复数翻译', 'dpgettext': '按域按上下文取翻译', 'install': '装入', 'textdomain': '设文本域', 'translation': '取翻译器'}

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
import operator
import os
import sys
__all__ = ['NullTranslations', 'GNUTranslations', 'Catalog', 'bindtextdomain', 'find', 'translation', 'install', 'textdomain', 'dgettext', 'dngettext', 'gettext', 'ngettext', 'pgettext', 'dpgettext', 'npgettext', 'dnpgettext']
_default_localedir = os.path.join(sys.base_prefix, 'share', 'locale')
_token_pattern = None

def _tokenize(plural):
    global _token_pattern
    if _token_pattern is None:
        import re
        _token_pattern = re.compile('\n                (?P<WHITESPACES>[ \\t]+)                    | # spaces and horizontal tabs\n                (?P<NUMBER>[0-9]+\\b)                       | # decimal integer\n                (?P<NAME>n\\b)                              | # only n is allowed\n                (?P<PARENTHESIS>[()])                      |\n                (?P<OPERATOR>[-*/%+?:]|[><!]=?|==|&&|\\|\\|) | # !, *, /, %, +, -, <, >,\n                                                             # <=, >=, ==, !=, &&, ||,\n                                                             # ? :\n                                                             # unary and bitwise ops\n                                                             # not allowed\n                (?P<INVALID>\\w+|.)                           # invalid token\n            ', re.VERBOSE | re.DOTALL)
    for mo in _token_pattern.finditer(plural):
        kind = mo.lastgroup
        if kind == 'WHITESPACES':
            continue
        value = mo.group(kind)
        if kind == 'INVALID':
            raise ValueError('invalid token in plural form: %s' % value)
        yield value
    yield ''

def _error(value):
    if value:
        return ValueError('unexpected token in plural form: %s' % value)
    else:
        return ValueError('unexpected end of plural form')
_binary_ops = (('||',), ('&&',), ('==', '!='), ('<', '>', '<=', '>='), ('+', '-'), ('*', '/', '%'))
_binary_ops = {op: i for i, ops in enumerate(_binary_ops, 1) for op in ops}
_c2py_ops = {'||': 'or', '&&': 'and', '/': '//'}

def _parse(tokens, priority=-1):
    result = ''
    nexttok = next(tokens)
    while nexttok == '!':
        result += 'not '
        nexttok = next(tokens)
    if nexttok == '(':
        sub, nexttok = _parse(tokens)
        result = '%s(%s)' % (result, sub)
        if nexttok != ')':
            raise ValueError('unbalanced parenthesis in plural form')
    elif nexttok == 'n':
        result = '%s%s' % (result, nexttok)
    else:
        try:
            value = int(nexttok, 10)
        except ValueError:
            raise _error(nexttok) from None
        result = '%s%d' % (result, value)
    nexttok = next(tokens)
    j = 100
    while nexttok in _binary_ops:
        i = _binary_ops[nexttok]
        if i < priority:
            break
        if i in (3, 4) and j in (3, 4):
            result = '(%s)' % result
        op = _c2py_ops.get(nexttok, nexttok)
        right, nexttok = _parse(tokens, i + 1)
        result = '%s %s %s' % (result, op, right)
        j = i
    if j == priority == 4:
        result = '(%s)' % result
    if nexttok == '?' and priority <= 0:
        if_true, nexttok = _parse(tokens, 0)
        if nexttok != ':':
            raise _error(nexttok)
        if_false, nexttok = _parse(tokens)
        result = '%s if %s else %s' % (if_true, result, if_false)
        if priority == 0:
            result = '(%s)' % result
    return (result, nexttok)

def _as_int(n):
    try:
        round(n)
    except TypeError:
        raise TypeError('Plural value must be an integer, got %s' % (n.__class__.__name__,)) from None
    return _as_int2(n)

def _as_int2(n):
    try:
        return operator.index(n)
    except TypeError:
        pass
    import warnings
    frame = sys._getframe(1)
    stacklevel = 2
    while frame.f_back is not None and frame.f_globals.get('__name__') == __name__:
        stacklevel += 1
        frame = frame.f_back
    warnings.warn('Plural value must be an integer, got %s' % (n.__class__.__name__,), DeprecationWarning, stacklevel)
    return n

def 复数式转Python(plural):
    """Gets a C expression as used in PO files for plural forms and returns a
    Python function that implements an equivalent expression.
    """
    if len(plural) > 1000:
        raise ValueError('plural form expression is too long')
    try:
        result, nexttok = _parse(_tokenize(plural))
        if nexttok:
            raise _error(nexttok)
        depth = 0
        for c in result:
            if c == '(':
                depth += 1
                if depth > 20:
                    raise ValueError('plural form expression is too complex')
            elif c == ')':
                depth -= 1
        ns = {'_as_int': _as_int, '__name__': __name__}
        exec('if True:\n            def func(n):\n                if not isinstance(n, int):\n                    n = _as_int(n)\n                return int(%s)\n            ' % result, ns)
        return ns['func']
    except RecursionError:
        raise ValueError('plural form expression is too complex')

def _expand_lang(loc):
    import locale
    loc = locale.normalize(loc)
    COMPONENT_CODESET = 1 << 0
    COMPONENT_TERRITORY = 1 << 1
    COMPONENT_MODIFIER = 1 << 2
    mask = 0
    pos = loc.find('@')
    if pos >= 0:
        modifier = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_MODIFIER
    else:
        modifier = ''
    pos = loc.find('.')
    if pos >= 0:
        codeset = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_CODESET
    else:
        codeset = ''
    pos = loc.find('_')
    if pos >= 0:
        territory = loc[pos:]
        loc = loc[:pos]
        mask |= COMPONENT_TERRITORY
    else:
        territory = ''
    language = loc
    ret = []
    for i in range(mask + 1):
        if not i & ~mask:
            val = language
            if i & COMPONENT_TERRITORY:
                val += territory
            if i & COMPONENT_CODESET:
                val += codeset
            if i & COMPONENT_MODIFIER:
                val += modifier
            ret.append(val)
    ret.reverse()
    return ret

class 空翻译:

    def __init__(self, fp=None):
        self._info = {}
        self._charset = None
        self._fallback = None
        if fp is not None:
            self._parse(fp)

    def _parse(self, fp):
        pass

    def 加后备翻译(self, fallback):
        if self._fallback:
            self._fallback.add_fallback(fallback)
        else:
            self._fallback = fallback

    def gettext(self, message):
        if self._fallback:
            return self._fallback.gettext(message)
        return message

    def ngettext(self, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.ngettext(msgid1, msgid2, n)
        n = _as_int2(n)
        if n == 1:
            return msgid1
        else:
            return msgid2

    def pgettext(self, context, message):
        if self._fallback:
            return self._fallback.pgettext(context, message)
        return message

    def npgettext(self, context, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.npgettext(context, msgid1, msgid2, n)
        n = _as_int2(n)
        if n == 1:
            return msgid1
        else:
            return msgid2

    def 取信息(self):
        return self._info

    def 取字符集(self):
        return self._charset

    def 装入(self, names=None):
        import builtins
        builtins.__dict__['_'] = self.gettext
        if names is not None:
            allowed = {'gettext', 'ngettext', 'npgettext', 'pgettext'}
            for name in allowed & set(names):
                builtins.__dict__[name] = getattr(self, name)
_装类转发(空翻译, {'add_fallback': '加后备翻译', 'charset': '取字符集', 'info': '取信息', 'install': '装入'}, {'add_fallback': '加后备翻译', 'charset': '取字符集', 'info': '取信息', 'install': '装入'})

class GNU翻译(空翻译):
    LE_MAGIC = 2500072158
    BE_MAGIC = 3725722773
    CONTEXT = '%s\x04%s'
    VERSIONS = (0, 1)

    def _get_versions(self, version):
        """Returns a tuple of major version, minor version"""
        return (version >> 16, version & 65535)

    def _parse(self, fp):
        """Override this method to support alternative .mo formats."""
        from struct import unpack
        filename = getattr(fp, 'name', '')
        self._catalog = catalog = {}
        self.plural = lambda n: int(n != 1)
        buf = fp.read()
        buflen = len(buf)
        magic = unpack('<I', buf[:4])[0]
        if magic == self.LE_MAGIC:
            version, msgcount, masteridx, transidx = unpack('<4I', buf[4:20])
            ii = '<II'
        elif magic == self.BE_MAGIC:
            version, msgcount, masteridx, transidx = unpack('>4I', buf[4:20])
            ii = '>II'
        else:
            raise OSError(0, 'Bad magic number', filename)
        major_version, minor_version = self._get_versions(version)
        if major_version not in self.VERSIONS:
            raise OSError(0, 'Bad version number ' + str(major_version), filename)
        for i in range(0, msgcount):
            mlen, moff = unpack(ii, buf[masteridx:masteridx + 8])
            mend = moff + mlen
            tlen, toff = unpack(ii, buf[transidx:transidx + 8])
            tend = toff + tlen
            if mend < buflen and tend < buflen:
                msg = buf[moff:mend]
                tmsg = buf[toff:tend]
            else:
                raise OSError(0, 'File is corrupt', filename)
            if mlen == 0:
                lastk = None
                for b_item in tmsg.split(b'\n'):
                    item = b_item.decode().strip()
                    if not item:
                        continue
                    if item.startswith('#-#-#-#-#') and item.endswith('#-#-#-#-#'):
                        continue
                    k = v = None
                    if ':' in item:
                        k, v = item.split(':', 1)
                        k = k.strip().lower()
                        v = v.strip()
                        self._info[k] = v
                        lastk = k
                    elif lastk:
                        self._info[lastk] += '\n' + item
                    if k == 'content-type':
                        self._charset = v.split('charset=')[1]
                    elif k == 'plural-forms':
                        v = v.split(';')
                        plural = v[1].split('plural=')[1]
                        self.plural = 复数式转Python(plural)
            取字符集 = self._charset or 'ascii'
            if b'\x00' in msg:
                msgid1, msgid2 = msg.split(b'\x00')
                tmsg = tmsg.split(b'\x00')
                msgid1 = str(msgid1, 取字符集)
                for i, x in enumerate(tmsg):
                    catalog[msgid1, i] = str(x, 取字符集)
            else:
                catalog[str(msg, 取字符集)] = str(tmsg, 取字符集)
            masteridx += 8
            transidx += 8

    def gettext(self, message):
        missing = object()
        tmsg = self._catalog.get(message, missing)
        if tmsg is missing:
            tmsg = self._catalog.get((message, self.plural(1)), missing)
        if tmsg is not missing:
            return tmsg
        if self._fallback:
            return self._fallback.gettext(message)
        return message

    def ngettext(self, msgid1, msgid2, n):
        try:
            tmsg = self._catalog[msgid1, self.plural(n)]
        except KeyError:
            if self._fallback:
                return self._fallback.ngettext(msgid1, msgid2, n)
            if n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        return tmsg

    def pgettext(self, context, message):
        ctxt_msg_id = self.CONTEXT % (context, message)
        missing = object()
        tmsg = self._catalog.get(ctxt_msg_id, missing)
        if tmsg is missing:
            tmsg = self._catalog.get((ctxt_msg_id, self.plural(1)), missing)
        if tmsg is not missing:
            return tmsg
        if self._fallback:
            return self._fallback.pgettext(context, message)
        return message

    def npgettext(self, context, msgid1, msgid2, n):
        ctxt_msg_id = self.CONTEXT % (context, msgid1)
        try:
            tmsg = self._catalog[ctxt_msg_id, self.plural(n)]
        except KeyError:
            if self._fallback:
                return self._fallback.npgettext(context, msgid1, msgid2, n)
            if n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        return tmsg

def find(domain, localedir=None, languages=None, all=False):
    if localedir is None:
        localedir = _default_localedir
    if languages is None:
        languages = []
        for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
            val = os.environ.get(envar)
            if val:
                languages = val.split(':')
                break
        if 'C' not in languages:
            languages.append('C')
    nelangs = []
    for lang in languages:
        for nelang in _expand_lang(lang):
            if nelang not in nelangs:
                nelangs.append(nelang)
    if all:
        result = []
    else:
        result = None
    for lang in nelangs:
        if lang == 'C':
            break
        mofile = os.path.join(localedir, lang, 'LC_MESSAGES', '%s.mo' % domain)
        if os.path.exists(mofile):
            if all:
                result.append(mofile)
            else:
                return mofile
    return result
_translations = {}

def 取翻译器(domain, localedir=None, languages=None, class_=None, fallback=False):
    if class_ is None:
        class_ = GNU翻译
    mofiles = find(domain, localedir, languages, all=True)
    if not mofiles:
        if fallback:
            return 空翻译()
        from errno import ENOENT
        raise FileNotFoundError(ENOENT, 'No translation file found for domain', domain)
    result = None
    for mofile in mofiles:
        key = (class_, os.path.abspath(mofile))
        t = _translations.get(key)
        if t is None:
            with open(mofile, 'rb') as fp:
                t = _translations.setdefault(key, class_(fp))
        import copy
        t = copy.copy(t)
        if result is None:
            result = t
        else:
            result.add_fallback(t)
    return result

def 装入(domain, localedir=None, *, names=None):
    t = 取翻译器(domain, localedir, fallback=True)
    t.install(names)
_localedirs = {}
_current_domain = 'messages'

def 设文本域(domain=None):
    global _current_domain
    if domain is not None:
        _current_domain = domain
    return _current_domain

def 绑定文本域(domain, localedir=None):
    global _localedirs
    if localedir is not None:
        _localedirs[domain] = localedir
    return _localedirs.get(domain, _default_localedir)

def 按域取翻译(domain, message):
    try:
        t = 取翻译器(domain, _localedirs.get(domain, None))
    except OSError:
        return message
    return t.gettext(message)

def 按域取复数翻译(domain, msgid1, msgid2, n):
    try:
        t = 取翻译器(domain, _localedirs.get(domain, None))
    except OSError:
        n = _as_int2(n)
        if n == 1:
            return msgid1
        else:
            return msgid2
    return t.ngettext(msgid1, msgid2, n)

def 按域按上下文取翻译(domain, context, message):
    try:
        t = 取翻译器(domain, _localedirs.get(domain, None))
    except OSError:
        return message
    return t.pgettext(context, message)

def 按域按上下文取复数翻译(domain, context, msgid1, msgid2, n):
    try:
        t = 取翻译器(domain, _localedirs.get(domain, None))
    except OSError:
        n = _as_int2(n)
        if n == 1:
            return msgid1
        else:
            return msgid2
    return t.npgettext(context, msgid1, msgid2, n)

def gettext(message):
    return 按域取翻译(_current_domain, message)

def ngettext(msgid1, msgid2, n):
    return 按域取复数翻译(_current_domain, msgid1, msgid2, n)

def pgettext(context, message):
    return 按域按上下文取翻译(_current_domain, context, message)

def npgettext(context, msgid1, msgid2, n):
    return 按域按上下文取复数翻译(_current_domain, context, msgid1, msgid2, n)
翻译目录 = 取翻译器


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Catalog': '翻译目录',
    'GNUTranslations': 'GNU翻译',
    'NullTranslations': '空翻译',
    'bindtextdomain': '绑定文本域',
    'c2py': '复数式转Python',
    'dgettext': '按域取翻译',
    'dngettext': '按域取复数翻译',
    'dnpgettext': '按域按上下文取复数翻译',
    'dpgettext': '按域按上下文取翻译',
    'install': '装入',
    'textdomain': '设文本域',
    'translation': '取翻译器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '空翻译': {
        'add_fallback': '加后备翻译',
        'charset': '取字符集',
        'info': '取信息',
        'install': '装入',
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
    '空翻译': {
        'add_fallback': '加后备翻译',
        'charset': '取字符集',
        'info': '取信息',
        'install': '装入',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'GNU翻译',
    '取翻译器',
    '按域取复数翻译',
    '按域取翻译',
    '按域按上下文取复数翻译',
    '按域按上下文取翻译',
    '空翻译',
    '绑定文本域',
    '翻译目录',
    '装入',
    '设文本域',
])

# ---- 转发层结束 ----
