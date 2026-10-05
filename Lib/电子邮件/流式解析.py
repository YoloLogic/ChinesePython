# -*- coding: utf-8 -*-
"""电子邮件.流式解析 —— 汉语库（由 tools/汉化库.py 从 Lib/email/feedparser.py 机械生成，**不要手改**）。

英文库 Lib/email.feedparser.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""FeedParser - An email feed parser.

The feed parser implements an interface for incrementally parsing an email
message, line by line.  This has advantages for certain applications, such as
those reading email messages off a socket.

FeedParser.feed() is the primary interface for pushing new data into the
parser.  It returns when there's nothing more it can do with the available
data.  When you have no more data to push into the parser, call .close().
This completes the parsing and returns the root message object.

The other advantage of this parser is that it will never raise a parsing
exception.  Instead, when it finds something unexpected, it adds a 'defect' to
the current message.  Defects are just instances that live on the message
object's .defects attribute.
"""
_英文原名表 = {'BufferedSubFile': '缓冲子文件', 'BytesFeedParser': '字节流式解析器', 'FeedParser': '流式解析器'}

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
__all__ = ['FeedParser', 'BytesFeedParser']
import re
from 电子邮件 import 错误
from 电子邮件._策略基类 import compat32
from collections import deque
from io import StringIO
NLCRE = re.compile('\\r\\n|\\r|\\n')
NLCRE_bol = re.compile('(\\r\\n|\\r|\\n)')
NLCRE_eol = re.compile('(\\r\\n|\\r|\\n)\\z')
NLCRE_crack = re.compile('(\\r\\n|\\r|\\n)')
headerRE = re.compile('^(From |[\\041-\\071\\073-\\176]*:|[\\t ])')
EMPTYSTRING = ''
NL = '\n'
boundaryendRE = re.compile('(?P<end>--)?(?P<ws>[ \\t]*)(?P<linesep>\\r\\n|\\r|\\n)?$')
NeedMoreData = object()

class 缓冲子文件(object):
    """A file-ish object that can have new data loaded into it.

    You can also push and pop line-matching predicates onto a stack.  When the
    current predicate matches the current line, a false EOF response
    (i.e. empty string) is returned instead.  This lets the parser adhere to a
    simple abstraction -- it parses until EOF closes the current message.
    """

    def __init__(self):
        self._partial = StringIO(newline='')
        self._lines = deque()
        self._eofstack = []
        self._closed = False

    def push_eof_matcher(self, pred):
        self._eofstack.append(pred)

    def pop_eof_matcher(self):
        return self._eofstack.pop()

    def 关闭(self):
        self._partial.seek(0)
        self.pushlines(self._partial.readlines())
        self._partial.seek(0)
        self._partial.truncate()
        self._closed = True

    def readline(self):
        if not self._lines:
            if self._closed:
                return ''
            return NeedMoreData
        line = self._lines.popleft()
        for ateof in reversed(self._eofstack):
            if ateof(line):
                self._lines.appendleft(line)
                return ''
        return line

    def unreadline(self, line):
        assert line is not NeedMoreData
        self._lines.appendleft(line)

    def push(self, data):
        """Push some new data into this object."""
        self._partial.write(data)
        if '\n' not in data and '\r' not in data:
            return
        self._partial.seek(0)
        parts = self._partial.readlines()
        self._partial.seek(0)
        self._partial.truncate()
        if not parts[-1].endswith('\n'):
            self._partial.write(parts.pop())
        self.pushlines(parts)

    def pushlines(self, lines):
        self._lines.extend(lines)

    def __iter__(self):
        return self

    def __next__(self):
        line = self.readline()
        if line == '':
            raise StopIteration
        return line
_装类转发(缓冲子文件, {'close': '关闭'}, {'close': '关闭'})

class 流式解析器:
    """A feed-style parser of email."""

    def __init__(self, _factory=None, *, policy=compat32):
        """_factory is called with no arguments to create a new message obj

        The policy keyword specifies a policy object that controls a number of
        aspects of the parser's operation.  The default policy maintains
        backward compatibility.

        """
        self.policy = policy
        self._old_style_factory = False
        if _factory is None:
            if policy.message_factory is None:
                from 电子邮件.消息 import Message
                self._factory = Message
            else:
                self._factory = policy.message_factory
        else:
            self._factory = _factory
            try:
                _factory(policy=self.policy)
            except TypeError:
                self._old_style_factory = True
        self._input = 缓冲子文件()
        self._msgstack = []
        self._parse = self._parsegen().__next__
        self._cur = None
        self._last = None
        self._headersonly = False

    def _set_headersonly(self):
        self._headersonly = True

    def 喂入(self, data):
        """Push more data into the parser."""
        self._input.push(data)
        self._call_parse()

    def _call_parse(self):
        try:
            self._parse()
        except StopIteration:
            pass

    def 关闭(self):
        """Parse all remaining data and return the root message object."""
        self._input.close()
        self._call_parse()
        root = self._pop_message()
        assert not self._msgstack
        if root.get_content_maintype() == 'multipart' and (not root.is_multipart()) and (not self._headersonly):
            defect = 错误.MultipartInvariantViolationDefect()
            self.policy.handle_defect(root, defect)
        return root

    def _new_message(self):
        if self._old_style_factory:
            msg = self._factory()
        else:
            msg = self._factory(policy=self.policy)
        if self._cur and self._cur.get_content_type() == 'multipart/digest':
            msg.set_default_type('message/rfc822')
        if self._msgstack:
            self._msgstack[-1].attach(msg)
        self._msgstack.append(msg)
        self._cur = msg
        self._last = msg

    def _pop_message(self):
        retval = self._msgstack.pop()
        if self._msgstack:
            self._cur = self._msgstack[-1]
        else:
            self._cur = None
        return retval

    def _parsegen(self):
        self._new_message()
        headers = []
        for line in self._input:
            if line is NeedMoreData:
                yield NeedMoreData
                continue
            if not headerRE.match(line):
                if not NLCRE.match(line):
                    defect = 错误.MissingHeaderBodySeparatorDefect()
                    self.policy.handle_defect(self._cur, defect)
                    self._input.unreadline(line)
                break
            headers.append(line)
        self._parse_headers(headers)
        if self._headersonly:
            lines = []
            while True:
                line = self._input.readline()
                if line is NeedMoreData:
                    yield NeedMoreData
                    continue
                if line == '':
                    break
                lines.append(line)
            self._cur.set_payload(EMPTYSTRING.join(lines))
            return
        if self._cur.get_content_type() == 'message/delivery-status':
            while True:
                self._input.push_eof_matcher(NLCRE.match)
                for retval in self._parsegen():
                    if retval is NeedMoreData:
                        yield NeedMoreData
                        continue
                    break
                self._pop_message()
                self._input.pop_eof_matcher()
                while True:
                    line = self._input.readline()
                    if line is NeedMoreData:
                        yield NeedMoreData
                        continue
                    break
                while True:
                    line = self._input.readline()
                    if line is NeedMoreData:
                        yield NeedMoreData
                        continue
                    break
                if line == '':
                    break
                self._input.unreadline(line)
            return
        if self._cur.get_content_maintype() == 'message':
            for retval in self._parsegen():
                if retval is NeedMoreData:
                    yield NeedMoreData
                    continue
                break
            self._pop_message()
            return
        if self._cur.get_content_maintype() == 'multipart':
            boundary = self._cur.get_boundary()
            if boundary is None:
                defect = 错误.NoBoundaryInMultipartDefect()
                self.policy.handle_defect(self._cur, defect)
                lines = []
                for line in self._input:
                    if line is NeedMoreData:
                        yield NeedMoreData
                        continue
                    lines.append(line)
                self._cur.set_payload(EMPTYSTRING.join(lines))
                return
            if str(self._cur.get('content-transfer-encoding', '8bit')).lower() not in ('7bit', '8bit', 'binary'):
                defect = 错误.InvalidMultipartContentTransferEncodingDefect()
                self.policy.handle_defect(self._cur, defect)
            separator = '--' + boundary

            def boundarymatch(line):
                if not line.startswith(separator):
                    return None
                return boundaryendRE.match(line, len(separator))
            capturing_preamble = True
            preamble = []
            linesep = False
            close_boundary_seen = False
            while True:
                line = self._input.readline()
                if line is NeedMoreData:
                    yield NeedMoreData
                    continue
                if line == '':
                    break
                mo = boundarymatch(line)
                if mo:
                    if mo.group('end'):
                        close_boundary_seen = True
                        linesep = mo.group('linesep')
                        break
                    if capturing_preamble:
                        if preamble:
                            lastline = preamble[-1]
                            eolmo = NLCRE_eol.search(lastline)
                            if eolmo:
                                preamble[-1] = lastline[:-len(eolmo.group(0))]
                            self._cur.preamble = EMPTYSTRING.join(preamble)
                        capturing_preamble = False
                        self._input.unreadline(line)
                        continue
                    while True:
                        line = self._input.readline()
                        if line is NeedMoreData:
                            yield NeedMoreData
                            continue
                        mo = boundarymatch(line)
                        if not mo:
                            self._input.unreadline(line)
                            break
                    self._input.push_eof_matcher(boundarymatch)
                    for retval in self._parsegen():
                        if retval is NeedMoreData:
                            yield NeedMoreData
                            continue
                        break
                    if self._last.get_content_maintype() == 'multipart':
                        epilogue = self._last.epilogue
                        if epilogue == '':
                            self._last.epilogue = None
                        elif epilogue is not None:
                            mo = NLCRE_eol.search(epilogue)
                            if mo:
                                end = len(mo.group(0))
                                self._last.epilogue = epilogue[:-end]
                    else:
                        payload = self._last._payload
                        if isinstance(payload, str):
                            mo = NLCRE_eol.search(payload)
                            if mo:
                                payload = payload[:-len(mo.group(0))]
                                self._last._payload = payload
                    self._input.pop_eof_matcher()
                    self._pop_message()
                    self._last = self._cur
                else:
                    assert capturing_preamble
                    preamble.append(line)
            if capturing_preamble:
                defect = 错误.StartBoundaryNotFoundDefect()
                self.policy.handle_defect(self._cur, defect)
                self._cur.set_payload(EMPTYSTRING.join(preamble))
                epilogue = []
                for line in self._input:
                    if line is NeedMoreData:
                        yield NeedMoreData
                        continue
                self._cur.epilogue = EMPTYSTRING.join(epilogue)
                return
            if not close_boundary_seen:
                defect = 错误.CloseBoundaryNotFoundDefect()
                self.policy.handle_defect(self._cur, defect)
                return
            if linesep:
                epilogue = ['']
            else:
                epilogue = []
            for line in self._input:
                if line is NeedMoreData:
                    yield NeedMoreData
                    continue
                epilogue.append(line)
            if epilogue:
                firstline = epilogue[0]
                bolmo = NLCRE_bol.match(firstline)
                if bolmo:
                    epilogue[0] = firstline[len(bolmo.group(0)):]
            self._cur.epilogue = EMPTYSTRING.join(epilogue)
            return
        lines = []
        for line in self._input:
            if line is NeedMoreData:
                yield NeedMoreData
                continue
            lines.append(line)
        self._cur.set_payload(EMPTYSTRING.join(lines))

    def _parse_headers(self, lines):
        lastheader = ''
        lastvalue = []
        for lineno, line in enumerate(lines):
            if line[0] in ' \t':
                if not lastheader:
                    defect = 错误.FirstHeaderLineIsContinuationDefect(line)
                    self.policy.handle_defect(self._cur, defect)
                    continue
                lastvalue.append(line)
                continue
            if lastheader:
                self._cur.set_raw(*self.policy.header_source_parse(lastvalue))
                lastheader, lastvalue = ('', [])
            if line.startswith('From '):
                if lineno == 0:
                    mo = NLCRE_eol.search(line)
                    if mo:
                        line = line[:-len(mo.group(0))]
                    self._cur.set_unixfrom(line)
                    continue
                elif lineno == len(lines) - 1:
                    self._input.unreadline(line)
                    return
                else:
                    defect = 错误.MisplacedEnvelopeHeaderDefect(line)
                    self.policy.handle_defect(self._cur, defect)
                    continue
            i = line.find(':')
            if i == 0:
                defect = 错误.InvalidHeaderDefect('Missing header name.')
                self.policy.handle_defect(self._cur, defect)
                continue
            assert i > 0, '_parse_headers fed line with no : and no leading WS'
            lastheader = line[:i]
            lastvalue = [line]
        if lastheader:
            self._cur.set_raw(*self.policy.header_source_parse(lastvalue))
_装类转发(流式解析器, {'close': '关闭', 'feed': '喂入'}, {'close': '关闭', 'feed': '喂入'})

class 字节流式解析器(流式解析器):
    """Like FeedParser, but feed accepts bytes."""

    def 喂入(self, data):
        super().feed(data.decode('ascii', 'surrogateescape'))
_装类转发(字节流式解析器, {'feed': '喂入'}, {'feed': '喂入'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BufferedSubFile': '缓冲子文件',
    'BytesFeedParser': '字节流式解析器',
    'FeedParser': '流式解析器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '字节流式解析器': {
        'feed': '喂入',
    },
    '流式解析器': {
        'close': '关闭',
        'feed': '喂入',
    },
    '缓冲子文件': {
        'close': '关闭',
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
    '字节流式解析器': {
        'feed': '喂入',
    },
    '流式解析器': {
        'close': '关闭',
        'feed': '喂入',
    },
    '缓冲子文件': {
        'close': '关闭',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '字节流式解析器',
    '流式解析器',
])

# ---- 转发层结束 ----
