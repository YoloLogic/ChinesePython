# -*- coding: utf-8 -*-
"""电子邮件.生成器 —— 汉语库（由 tools/汉化库.py 从 Lib/email/generator.py 机械生成，**不要手改**）。

英文库 Lib/email.generator.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Classes to generate plain text from a message object tree."""
_英文原名表 = {'BytesGenerator': '字节生成器', 'DecodedGenerator': '解码生成器', 'Generator': '生成器'}

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
__all__ = ['Generator', 'DecodedGenerator', 'BytesGenerator']
import re
import sys
import time
import random
from copy import deepcopy
from io import StringIO, BytesIO
from 电子邮件.工具 import _has_surrogates
from 电子邮件.错误 import HeaderWriteError
UNDERSCORE = '_'
NL = '\n'
NLCRE = re.compile('\\r\\n|\\r|\\n')
fcre = re.compile('^From ', re.MULTILINE)
NEWLINE_WITHOUT_FWSP = re.compile('\\r\\n[^ \\t]|\\r[^ \\n\\t]|\\n[^ \\t]')
NEWLINE_WITHOUT_FWSP_BYTES = re.compile(b'\\r\\n[^ \\t]|\\r[^ \\n\\t]|\\n[^ \\t]')

class 生成器:
    """Generates output from a Message object tree.

    This basic generator writes the message to the given file object as plain
    text.
    """

    def __init__(self, outfp, mangle_from_=None, maxheaderlen=None, *, policy=None):
        """Create the generator for message flattening.

        outfp is the output file-like object for writing the message to.  It
        must have a write() method.

        Optional mangle_from_ is a flag that, when True (the default if policy
        is not set), escapes From_ lines in the body of the message by putting
        a '>' in front of them.

        Optional maxheaderlen specifies the longest length for a non-continued
        header.  When a header line is longer (in characters, with tabs
        expanded to 8 spaces) than maxheaderlen, the header will split as
        defined in the Header class.  Set maxheaderlen to zero to disable
        header wrapping.  The default is 78, as recommended (but not required)
        by RFC 5322 section 2.1.1.

        The policy keyword specifies a policy object that controls a number of
        aspects of the generator's operation.  If no policy is specified,
        the policy associated with the Message object passed to the
        flatten method is used.

        """
        if mangle_from_ is None:
            mangle_from_ = True if policy is None else policy.mangle_from_
        self._fp = outfp
        self._mangle_from_ = mangle_from_
        self.maxheaderlen = maxheaderlen
        self.policy = policy

    def 写出(self, s):
        self._fp.write(s)

    def 展平(self, msg, unixfrom=False, linesep=None):
        """Print the message object tree rooted at msg to the output file
        specified when the Generator instance was created.

        unixfrom is a flag that forces the printing of a Unix From_ delimiter
        before the first object in the message tree.  If the original message
        has no From_ delimiter, a 'standard' one is crafted.  By default, this
        is False to inhibit the printing of any From_ delimiter.

        Note that for subobjects, no From_ line is printed.

        linesep specifies the characters used to indicate a new line in
        the output.  The default value is determined by the policy specified
        when the Generator instance was created or, if none was specified,
        from the policy associated with the msg.

        """
        策略 = msg.policy if self.policy is None else self.policy
        if linesep is not None:
            策略 = 策略.clone(linesep=linesep)
        if self.maxheaderlen is not None:
            策略 = 策略.clone(max_line_length=self.maxheaderlen)
        self._NL = 策略.linesep
        self._encoded_NL = self._encode(self._NL)
        self._EMPTY = ''
        self._encoded_EMPTY = self._encode(self._EMPTY)
        old_gen_policy = self.policy
        old_msg_policy = msg.policy
        try:
            self.policy = 策略
            msg.policy = 策略
            if unixfrom:
                ufrom = msg.get_unixfrom()
                if not ufrom:
                    ufrom = 'From nobody ' + time.ctime(time.time())
                self.write(ufrom + self._NL)
            self._write(msg)
        finally:
            self.policy = old_gen_policy
            msg.policy = old_msg_policy

    def 克隆(self, fp):
        """Clone this generator with the exact same options."""
        return self.__class__(fp, self._mangle_from_, None, policy=self.policy)

    def _new_buffer(self):
        return StringIO()

    def _encode(self, s):
        return s

    def _write_lines(self, lines):
        if not lines:
            return
        lines = NLCRE.split(lines)
        for line in lines[:-1]:
            self.write(line)
            self.write(self._NL)
        if lines[-1]:
            self.write(lines[-1])

    def _write(self, msg):
        oldfp = self._fp
        try:
            self._munge_cte = None
            self._fp = sfp = self._new_buffer()
            self._dispatch(msg)
        finally:
            self._fp = oldfp
            munge_cte = self._munge_cte
            del self._munge_cte
        if munge_cte:
            msg = deepcopy(msg)
            if msg.get('content-transfer-encoding') is None:
                msg['Content-Transfer-Encoding'] = munge_cte[0]
            else:
                msg.replace_header('content-transfer-encoding', munge_cte[0])
            msg.replace_header('content-type', munge_cte[1])
        meth = getattr(msg, '_write_headers', None)
        if meth is None:
            self._write_headers(msg)
        else:
            meth(self)
        self._fp.write(sfp.getvalue())

    def _dispatch(self, msg):
        main = msg.get_content_maintype()
        sub = msg.get_content_subtype()
        specific = UNDERSCORE.join((main, sub)).replace('-', '_')
        meth = getattr(self, '_handle_' + specific, None)
        if meth is None:
            generic = main.replace('-', '_')
            meth = getattr(self, '_handle_' + generic, None)
            if meth is None:
                meth = self._writeBody
        meth(msg)

    def _write_headers(self, msg):
        for h, v in msg.raw_items():
            folded = self.policy.fold(h, v)
            if self.policy.verify_generated_headers:
                linesep = self.policy.linesep
                if not folded.endswith(linesep):
                    raise HeaderWriteError(f'folded header does not end with {linesep!r}: {folded!r}')
                if NEWLINE_WITHOUT_FWSP.search(folded.removesuffix(linesep)):
                    raise HeaderWriteError(f'folded header contains newline: {folded!r}')
            self.write(folded)
        self.write(self._NL)

    def _handle_text(self, msg):
        payload = msg.get_payload()
        if payload is None:
            return
        if not isinstance(payload, str):
            raise TypeError('string payload expected: %s' % type(payload))
        if _has_surrogates(msg._payload):
            字符集 = msg.get_param('charset')
            if 字符集 is not None:
                msg = deepcopy(msg)
                del msg['content-transfer-encoding']
                msg.set_payload(msg._payload, 字符集)
                payload = msg.get_payload()
                self._munge_cte = (msg['content-transfer-encoding'], msg['content-type'])
        if self._mangle_from_:
            payload = fcre.sub('>From ', payload)
        self._write_lines(payload)
    _writeBody = _handle_text

    def _handle_multipart(self, msg):
        msgtexts = []
        subparts = msg.get_payload()
        if subparts is None:
            subparts = []
        elif isinstance(subparts, str):
            self.write(subparts)
            return
        elif not isinstance(subparts, list):
            subparts = [subparts]
        for part in subparts:
            s = self._new_buffer()
            g = self.克隆(s)
            g.flatten(part, unixfrom=False, linesep=self._NL)
            msgtexts.append(s.getvalue())
        boundary = msg.get_boundary()
        if not boundary:
            alltext = self._encoded_NL.join(msgtexts)
            boundary = self._make_boundary(alltext)
            msg.set_boundary(boundary)
        if msg.preamble is not None:
            if self._mangle_from_:
                preamble = fcre.sub('>From ', msg.preamble)
            else:
                preamble = msg.preamble
            self._write_lines(preamble)
            self.write(self._NL)
        self.write('--' + boundary + self._NL)
        if msgtexts:
            self._fp.write(msgtexts.pop(0))
        for body_part in msgtexts:
            self.write(self._NL + '--' + boundary + self._NL)
            self._fp.write(body_part)
        self.write(self._NL + '--' + boundary + '--' + self._NL)
        if msg.epilogue is not None:
            if self._mangle_from_:
                epilogue = fcre.sub('>From ', msg.epilogue)
            else:
                epilogue = msg.epilogue
            self._write_lines(epilogue)

    def _handle_multipart_signed(self, msg):
        p = self.policy
        self.policy = p.clone(max_line_length=0)
        try:
            self._handle_multipart(msg)
        finally:
            self.policy = p

    def _handle_message_delivery_status(self, msg):
        blocks = []
        for part in msg.get_payload():
            s = self._new_buffer()
            g = self.克隆(s)
            g.flatten(part, unixfrom=False, linesep=self._NL)
            text = s.getvalue()
            lines = text.split(self._encoded_NL)
            if lines and lines[-1] == self._encoded_EMPTY:
                blocks.append(self._encoded_NL.join(lines[:-1]))
            else:
                blocks.append(text)
        self._fp.write(self._encoded_NL.join(blocks))

    def _handle_message(self, msg):
        s = self._new_buffer()
        g = self.克隆(s)
        payload = msg._payload
        if isinstance(payload, list):
            g.flatten(msg.get_payload(0), unixfrom=False, linesep=self._NL)
            payload = s.getvalue()
        else:
            payload = self._encode(payload)
        self._fp.write(payload)

    @classmethod
    def _make_boundary(cls, text=None):
        token = random.randrange(sys.maxsize)
        boundary = '=' * 15 + _fmt % token + '=='
        if text is None:
            return boundary
        b = boundary
        counter = 0
        while True:
            cre = cls._compile_re('^--' + re.escape(b) + '(--)?\r?$', re.MULTILINE)
            if not cre.search(text):
                break
            b = boundary + '.' + str(counter)
            counter += 1
        return b

    @classmethod
    def _compile_re(cls, s, flags):
        return re.compile(s, flags)
_装类转发(生成器, {'clone': '克隆', 'flatten': '展平', 'write': '写出'}, {'clone': '克隆', 'flatten': '展平', 'write': '写出'})

class 字节生成器(生成器):
    """Generates a bytes version of a Message object tree.

    Functionally identical to the base Generator except that the output is
    bytes and not string.  When surrogates were used in the input to encode
    bytes, these are decoded back to bytes for output.  If the policy has
    cte_type set to 7bit, then the message is transformed such that the
    non-ASCII bytes are properly content transfer encoded, using the charset
    unknown-8bit.

    The outfp object must accept bytes in its write method.
    """

    def 写出(self, s):
        self._fp.write(s.encode('ascii', 'surrogateescape'))

    def _new_buffer(self):
        return BytesIO()

    def _encode(self, s):
        return s.encode('ascii')

    def _write_headers(self, msg):
        for h, v in msg.raw_items():
            folded = self.policy.fold_binary(h, v)
            if self.policy.verify_generated_headers:
                linesep = self.policy.linesep.encode()
                if not folded.endswith(linesep):
                    raise HeaderWriteError(f'folded header does not end with {linesep!r}: {folded!r}')
                if NEWLINE_WITHOUT_FWSP_BYTES.search(folded.removesuffix(linesep)):
                    raise HeaderWriteError(f'folded header contains newline: {folded!r}')
            self._fp.write(folded)
        self.write(self._NL)

    def _handle_text(self, msg):
        if msg._payload is None:
            return
        if _has_surrogates(msg._payload) and (not self.policy.cte_type == '7bit'):
            if self._mangle_from_:
                msg._payload = fcre.sub('>From ', msg._payload)
            self._write_lines(msg._payload)
        else:
            super(字节生成器, self)._handle_text(msg)
    _writeBody = _handle_text

    @classmethod
    def _compile_re(cls, s, flags):
        return re.compile(s.encode('ascii'), flags)
_装类转发(字节生成器, {'write': '写出'}, {'write': '写出'})
_FMT = '[Non-text (%(type)s) part of message omitted, filename %(filename)s]'

class 解码生成器(生成器):
    """Generates a text representation of a message.

    Like the Generator base class, except that non-text parts are substituted
    with a format string representing the part.
    """

    def __init__(self, outfp, mangle_from_=None, maxheaderlen=None, fmt=None, *, policy=None):
        """Like Generator.__init__() except that an additional optional
        argument is allowed.

        Walks through all subparts of a message.  If the subpart is of main
        type 'text', then it prints the decoded payload of the subpart.

        Otherwise, fmt is a format string that is used instead of the message
        payload.  fmt is expanded with the following keywords (in
        %(keyword)s format):

        type       : Full MIME type of the non-text part
        maintype   : Main MIME type of the non-text part
        subtype    : Sub-MIME type of the non-text part
        filename   : Filename of the non-text part
        description: Description associated with the non-text part
        encoding   : Content transfer encoding of the non-text part

        The default value for fmt is None, meaning

        [Non-text (%(type)s) part of message omitted, filename %(filename)s]
        """
        生成器.__init__(self, outfp, mangle_from_, maxheaderlen, policy=policy)
        if fmt is None:
            self._fmt = _FMT
        else:
            self._fmt = fmt

    def _dispatch(self, msg):
        for part in msg.walk():
            maintype = part.get_content_maintype()
            if maintype == 'text':
                print(part.get_payload(decode=False), file=self)
            elif maintype == 'multipart':
                pass
            else:
                print(self._fmt % {'type': part.get_content_type(), 'maintype': part.get_content_maintype(), 'subtype': part.get_content_subtype(), 'filename': part.get_filename('[no filename]'), 'description': part.get('Content-Description', '[no description]'), 'encoding': part.get('Content-Transfer-Encoding', '[no encoding]')}, file=self)
_width = len(repr(sys.maxsize - 1))
_fmt = '%%0%dd' % _width
_make_boundary = 生成器._make_boundary


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BytesGenerator': '字节生成器',
    'DecodedGenerator': '解码生成器',
    'Generator': '生成器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '字节生成器': {
        'write': '写出',
    },
    '生成器': {
        'clone': '克隆',
        'flatten': '展平',
        'write': '写出',
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
    '字节生成器': {
        'write': '写出',
    },
    '生成器': {
        'clone': '克隆',
        'flatten': '展平',
        'write': '写出',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '字节生成器',
    '生成器',
    '解码生成器',
])

# ---- 转发层结束 ----
