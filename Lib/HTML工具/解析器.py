# -*- coding: utf-8 -*-
"""HTML工具.解析器 —— 汉语库（由 tools/汉化库.py 从 Lib/html/parser.py 机械生成，**不要手改**）。

英文库 Lib/html.parser.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py html
"""


"""A parser for HTML and XHTML."""
_英文原名表 = {'HTMLParser': 'HTML解析器'}

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
import _markupbase
from HTML工具 import unescape
from HTML工具.实体表 import html5 as html5_entities
__all__ = ['HTMLParser']
interesting_normal = re.compile('[&<]')
incomplete = re.compile('&[a-zA-Z#]')
entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
incomplete_charref = re.compile('&#(?:[0-9]|[xX][0-9a-fA-F])')
attr_charref = re.compile('&(#[0-9]+|#[xX][0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*)[;=]?')
starttagopen = re.compile('<[a-zA-Z]')
endtagopen = re.compile('</[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile('--!?>')
commentabruptclose = re.compile('-?>')
tagfind_tolerant = re.compile('([a-zA-Z][^\\t\\n\\r\\f />]*)(?:[\\t\\n\\r\\f ]|/(?!>))*')
attrfind_tolerant = re.compile('\n  (\n    (?<=[\'"\\t\\n\\r\\f /])[^\\t\\n\\r\\f />][^\\t\\n\\r\\f /=>]*  # attribute name\n   )\n  ([\\t\\n\\r\\f ]*=[\\t\\n\\r\\f ]*        # value indicator\n    (\'[^\']*\'                        # LITA-enclosed value\n    |"[^"]*"                        # LIT-enclosed value\n    |(?![\'"])[^>\\t\\n\\r\\f ]*         # bare value\n    )\n   )?\n  (?:[\\t\\n\\r\\f ]|/(?!>))*           # possibly followed by a space\n', re.VERBOSE)
locatetagend = re.compile('\n  [a-zA-Z][^\\t\\n\\r\\f />]*           # tag name\n  [\\t\\n\\r\\f /]*                     # optional whitespace before attribute name\n  (?:(?<=[\'"\\t\\n\\r\\f /])[^\\t\\n\\r\\f />][^\\t\\n\\r\\f /=>]*  # attribute name\n    (?:[\\t\\n\\r\\f ]*=[\\t\\n\\r\\f ]*    # value indicator\n      (?:\'[^\']*\'                    # LITA-enclosed value\n        |"[^"]*"                    # LIT-enclosed value\n        |(?![\'"])[^>\\t\\n\\r\\f ]*     # bare value\n       )\n     )?\n    [\\t\\n\\r\\f /]*                   # possibly followed by a space\n   )*\n   >?\n', re.VERBOSE)
locatestarttagend_tolerant = re.compile('\n  <[a-zA-Z][^\\t\\n\\r\\f />\\x00]*       # tag name\n  (?:[\\s/]*                          # optional whitespace before attribute name\n    (?:(?<=[\'"\\s/])[^\\s/>][^\\s/=>]*  # attribute name\n      (?:\\s*=+\\s*                    # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |"[^"]*"                   # LIT-enclosed value\n          |(?![\'"])[^>\\s]*           # bare value\n         )\n        \\s*                          # possibly followed by a space\n       )?(?:\\s|/(?!>))*\n     )*\n   )?\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
endendtag = re.compile('>')
endtagfind = re.compile('</\\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\\s*>')

def _replace_attr_charref(match):
    ref = match.group(0)
    if ref.startswith('&#'):
        return unescape(ref)
    if not ref.endswith('=') and ref[1:] in html5_entities:
        return unescape(ref)
    return ref

def _unescape_attrvalue(s):
    return attr_charref.sub(_replace_attr_charref, s)

class HTML解析器(_markupbase.ParserBase):
    """Find tags and other markup and call handler functions.

    Usage:
        p = HTMLParser()
        p.feed(data)
        ...
        p.close()

    Start tags are handled by calling self.handle_starttag() or
    self.handle_startendtag(); end tags by self.handle_endtag().  The
    data between tags is passed from the parser to the derived class
    by calling self.handle_data() with the data as argument (the data
    may be split up in arbitrary chunks).  If convert_charrefs is
    True the character references are converted automatically to the
    corresponding Unicode character (and self.handle_data() is no
    longer split in chunks), otherwise they are passed by calling
    self.handle_entityref() or self.handle_charref() with the string
    containing respectively the named or numeric reference as the
    argument.
    """
    CDATA_CONTENT_ELEMENTS = ('script', 'style', 'xmp', 'iframe', 'noembed', 'noframes')
    RCDATA_CONTENT_ELEMENTS = ('textarea', 'title')

    def __init__(self, *, convert_charrefs=True, scripting=False):
        """Initialize and reset this instance.

        If convert_charrefs is true (the default), all character references
        are automatically converted to the corresponding Unicode characters.

        If *scripting* is false (the default), the content of the
        ``noscript`` element is parsed normally; if it's true,
        it's returned as is without being parsed.
        """
        super().__init__()
        self.convert_charrefs = convert_charrefs
        self.scripting = scripting
        self.重置()

    def 重置(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        self.cdata_elem = None
        self._support_cdata = True
        self._escapable = True
        self._pending = []
        self._pending_len = 0
        self._parse_threshold = 1
        super().reset()

    def 送入(self, data):
        """Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\\n').
        """
        self._pending_len += len(data)
        if self._pending_len < self._parse_threshold:
            self._pending.append(data)
        else:
            if not self._pending:
                self.rawdata += data
            else:
                self._pending.append(data)
                self.rawdata += ''.join(self._pending)
                self._pending.clear()
            self._pending_len = 0
            n = len(self.rawdata)
            self.goahead(0)
            if len(self.rawdata) < n:
                self._parse_threshold = 1
            else:
                self._parse_threshold = len(self.rawdata)

    def close(self):
        """Handle any buffered data."""
        if self._pending:
            self.rawdata += ''.join(self._pending)
            self._pending.clear()
            self._pending_len = 0
        self.goahead(1)
    __starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self.__starttag_text

    def set_cdata_mode(self, elem, *, escapable=False):
        self.cdata_elem = elem.lower()
        self._escapable = escapable
        if self.cdata_elem == 'plaintext':
            self.interesting = re.compile('\\z')
        elif escapable and (not self.convert_charrefs):
            self.interesting = re.compile('&|</%s(?=[\\t\\n\\r\\f />])' % self.cdata_elem, re.IGNORECASE | re.ASCII)
        else:
            self.interesting = re.compile('</%s(?=[\\t\\n\\r\\f />])' % self.cdata_elem, re.IGNORECASE | re.ASCII)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None
        self._escapable = True

    def _set_support_cdata(self, flag=True):
        """Enable or disable support of the CDATA sections.
        If enabled, "<[CDATA[" starts a CDATA section which ends with "]]>".
        If disabled, "<[CDATA[" starts a bogus comments which ends with ">".

        This method is not called by default. Its purpose is to be called
        in custom handle_starttag() and handle_endtag() methods, with
        value that depends on the adjusted current node.
        See https://html.spec.whatwg.org/multipage/parsing.html#markup-declaration-open-state
        for details.
        """
        self._support_cdata = flag

    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            if self.convert_charrefs and (not self.cdata_elem):
                j = rawdata.find('<', i)
                if j < 0:
                    amppos = rawdata.rfind('&', max(i, n - 34))
                    if amppos >= 0 and (not re.compile('[\\t\\n\\r\\f ;]').search(rawdata, amppos)):
                        break
                    j = n
            else:
                match = self.interesting.search(rawdata, i)
                if match:
                    j = match.start()
                else:
                    if self.cdata_elem:
                        break
                    j = n
            if i < j:
                if self.convert_charrefs and self._escapable:
                    self.handle_data(unescape(rawdata[i:j]))
                else:
                    self.handle_data(rawdata[i:j])
            i = self.updatepos(i, j)
            if i == n:
                break
            startswith = rawdata.startswith
            if startswith('<', i):
                if starttagopen.match(rawdata, i):
                    k = self.parse_starttag(i)
                elif startswith('</', i):
                    k = self.parse_endtag(i)
                elif startswith('<!--', i):
                    k = self.parse_comment(i)
                elif startswith('<?', i):
                    k = self.parse_pi(i)
                elif startswith('<!', i):
                    k = self.parse_html_declaration(i)
                elif i + 1 < n or end:
                    self.handle_data('<')
                    k = i + 1
                else:
                    break
                if k < 0:
                    if not end:
                        break
                    if starttagopen.match(rawdata, i):
                        pass
                    elif startswith('</', i):
                        if i + 2 == n:
                            self.handle_data('</')
                        elif endtagopen.match(rawdata, i):
                            pass
                        else:
                            self.handle_comment(rawdata[i + 2:])
                    elif startswith('<!--', i):
                        j = n
                        for suffix in ('--!', '--', '-'):
                            if rawdata.endswith(suffix, i + 4):
                                j -= len(suffix)
                                break
                        self.handle_comment(rawdata[i + 4:j])
                    elif startswith('<![CDATA[', i) and self._support_cdata:
                        self.unknown_decl(rawdata[i + 3:])
                    elif rawdata[i:i + 9].lower() == '<!doctype':
                        self.handle_decl(rawdata[i + 2:])
                    elif startswith('<!', i):
                        self.handle_comment(rawdata[i + 2:])
                    elif startswith('<?', i):
                        self.handle_pi(rawdata[i + 2:])
                    else:
                        raise AssertionError('we should not get here!')
                    k = n
                i = self.updatepos(i, k)
            elif startswith('&#', i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete_charref.match(rawdata, i)
                if match:
                    if end:
                        self.handle_charref(rawdata[i + 2:])
                        i = self.updatepos(i, n)
                        break
                    break
                elif i + 3 < n:
                    self.handle_data('&#')
                    i = self.updatepos(i, i + 2)
                else:
                    break
            elif startswith('&', i):
                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    if end:
                        self.handle_entityref(rawdata[i + 1:])
                        i = self.updatepos(i, n)
                        break
                    break
                elif i + 1 < n:
                    self.handle_data('&')
                    i = self.updatepos(i, i + 1)
                else:
                    break
            else:
                assert 0, 'interesting.search() lied'
        if end and i < n:
            if self.convert_charrefs and self._escapable:
                self.handle_data(unescape(rawdata[i:n]))
            else:
                self.handle_data(rawdata[i:n])
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    def parse_html_declaration(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '<!', 'unexpected call to parse_html_declaration()'
        if rawdata[i:i + 4] == '<!--':
            return self.parse_comment(i)
        elif rawdata[i:i + 9] == '<![CDATA[' and self._support_cdata:
            j = rawdata.find(']]>', i + 9)
            if j < 0:
                return -1
            self.unknown_decl(rawdata[i + 3:j])
            return j + 3
        elif rawdata[i:i + 9].lower() == '<!doctype':
            gtpos = rawdata.find('>', i + 9)
            if gtpos == -1:
                return -1
            self.handle_decl(rawdata[i + 2:gtpos])
            return gtpos + 1
        else:
            return self.parse_bogus_comment(i)

    def parse_comment(self, i, report=True):
        rawdata = self.rawdata
        assert rawdata.startswith('<!--', i), 'unexpected call to parse_comment()'
        match = commentabruptclose.match(rawdata, i + 4)
        if not match:
            match = commentclose.search(rawdata, i + 4)
            if not match:
                return -1
        if report:
            j = match.start()
            self.handle_comment(rawdata[i + 4:j])
        return match.end()

    def parse_bogus_comment(self, i, report=1):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] in ('<!', '</'), 'unexpected call to parse_bogus_comment()'
        pos = rawdata.find('>', i + 2)
        if pos == -1:
            return -1
        if report:
            self.handle_comment(rawdata[i + 2:pos])
        return pos + 1

    def parse_pi(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, i + 2)
        if not match:
            return -1
        j = match.start()
        self.handle_pi(rawdata[i + 2:j])
        j = match.end()
        return j

    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]
        attrs = []
        match = tagfind_tolerant.match(rawdata, i + 1)
        assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        self.lasttag = tag = match.group(1).lower()
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)
            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == "'" == attrvalue[-1:] or attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = _unescape_attrvalue(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            k = m.end()
        end = rawdata[k:endpos].strip()
        if end not in ('>', '/>'):
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith('/>'):
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS or (self.scripting and tag == 'noscript') or tag == 'plaintext':
                self.set_cdata_mode(tag, escapable=False)
            elif tag in self.RCDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag, escapable=True)
        return endpos

    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        match = locatetagend.match(rawdata, i + 1)
        assert match
        j = match.end()
        if rawdata[j - 1] != '>':
            return -1
        return j

    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i + 2] == '</', 'unexpected call to parse_endtag'
        if rawdata.find('>', i + 2) < 0:
            return -1
        if not endtagopen.match(rawdata, i):
            if rawdata[i + 2:i + 3] == '>':
                return i + 3
            else:
                return self.parse_bogus_comment(i)
        match = locatetagend.match(rawdata, i + 2)
        assert match
        j = match.end()
        if rawdata[j - 1] != '>':
            return -1
        match = tagfind_tolerant.match(rawdata, i + 2)
        assert match
        tag = match.group(1).lower()
        self.handle_endtag(tag)
        self.clear_cdata_mode()
        return j

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        pass
_装类转发(HTML解析器, {'feed': '送入', 'reset': '重置'}, {'feed': '送入', 'reset': '重置'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'HTMLParser': 'HTML解析器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'HTML解析器': {
        'feed': '送入',
        'reset': '重置',
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
    'HTML解析器': {
        'feed': '送入',
        'reset': '重置',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'HTML解析器',
]

# ---- 转发层结束 ----
