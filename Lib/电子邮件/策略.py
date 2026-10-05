# -*- coding: utf-8 -*-
"""电子邮件.策略 —— 汉语库（由 tools/汉化库.py 从 Lib/email/policy.py 机械生成，**不要手改**）。

英文库 Lib/email.policy.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""This will be the home for the policy that hooks in the new
code that adds all the email6 features.
"""
_英文原名表 = {'EmailPolicy': '邮件策略', 'HTTP': 'HTTP策略', 'SMTP': 'SMTP策略', 'SMTPUTF8': 'SMTPUTF8策略', 'default': '默认策略', 'strict': '严格策略'}

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
import sys
from 电子邮件._策略基类 import Compat32, Policy, _extend_docstrings, compat32, validate_header_name
from 电子邮件.工具 import _has_surrogates
from 电子邮件.邮件头登记 import HeaderRegistry as HeaderRegistry
from 电子邮件.内容管理 import raw_data_manager
from 电子邮件.消息 import EmailMessage
__all__ = ['Compat32', 'compat32', 'Policy', 'EmailPolicy', 'default', 'strict', 'SMTP', 'HTTP']
linesep_splitter = re.compile('\\n|\\r\\n?')

@_extend_docstrings
class 邮件策略(Policy):
    """+
    PROVISIONAL

    The API extensions enabled by this policy are currently provisional.
    Refer to the documentation for details.

    This policy adds new header parsing and folding algorithms.  Instead of
    simple strings, headers are custom objects with custom attributes
    depending on the type of the field.  The folding algorithm fully
    implements RFCs 2047 and 5322.

    In addition to the settable attributes listed above that apply to
    all Policies, this policy adds the following additional attributes:

    utf8                -- if False (the default) message headers will be
                           serialized as ASCII, using encoded words to encode
                           any non-ASCII characters in the source strings.  If
                           True, the message headers will be serialized using
                           utf8 and will not contain encoded words (see RFC
                           6532 for more on this serialization format).

    refold_source       -- if the value for a header in the Message object
                           came from the parsing of some source, this attribute
                           indicates whether or not a generator should refold
                           that value when transforming the message back into
                           stream form.  The possible values are:

                           none  -- all source values use original folding
                           long  -- source values that have any line that is
                                    longer than max_line_length will be
                                    refolded
                           all  -- all values are refolded.

                           The default is 'long'.

    header_factory      -- a callable that takes two arguments, 'name' and
                           'value', where 'name' is a header field name and
                           'value' is an unfolded header field value, and
                           returns a string-like object that represents that
                           header.  A default header_factory is provided that
                           understands some of the RFC5322 header field types.
                           (Currently address fields and date fields have
                           special treatment, while all other fields are
                           treated as unstructured.  This list will be
                           completed before the extension is marked stable.)

    content_manager     -- an object with at least two methods: get_content
                           and set_content.  When the get_content or
                           set_content method of a Message object is called,
                           it calls the corresponding method of this object,
                           passing it the message object as its first argument,
                           and any arguments or keywords that were passed to
                           it as additional arguments.  The default
                           content_manager is
                           :data:`~email.contentmanager.raw_data_manager`.

    """
    message_factory = EmailMessage
    utf8 = False
    refold_source = 'long'
    header_factory = HeaderRegistry()
    content_manager = raw_data_manager

    def __init__(self, **kw):
        if 'header_factory' not in kw:
            object.__setattr__(self, 'header_factory', HeaderRegistry())
        super().__init__(**kw)

    def 邮件头最大个数(self, name):
        """+
        The implementation for this class returns the max_count attribute from
        the specialized header class that would be used to construct a header
        of type 'name'.
        """
        return self.header_factory[name].max_count

    def 解析邮件头源(self, sourcelines):
        """+
        The name is parsed as everything up to the ':' and returned unmodified.
        The value is determined by stripping leading whitespace off the
        remainder of the first line joined with all subsequent lines, and
        stripping any trailing carriage return or linefeed characters.  (This
        is the same as Compat32).

        """
        name, value = sourcelines[0].split(':', 1)
        value = ''.join((value, *sourcelines[1:])).lstrip(' \t\r\n')
        return (name, value.rstrip('\r\n'))

    def 存储时解析邮件头(self, name, value):
        """+
        The name is returned unchanged.  If the input value has a 'name'
        attribute and it matches the name ignoring case, the value is returned
        unchanged.  Otherwise the name and value are passed to header_factory
        method, and the resulting custom header object is returned as the
        value.  In this case a ValueError is raised if the input value contains
        CR or LF characters.

        """
        validate_header_name(name)
        if hasattr(value, 'name') and value.name.lower() == name.lower():
            return (name, value)
        if isinstance(value, str) and len(value.splitlines()) > 1:
            raise ValueError('Header values may not contain linefeed or carriage return characters')
        return (name, self.header_factory(name, value))

    def 取出时解析邮件头(self, name, value):
        """+
        If the value has a 'name' attribute, it is returned to unmodified.
        Otherwise the name and the value with any linesep characters removed
        are passed to the header_factory method, and the resulting custom
        header object is returned.  Any surrogateescaped bytes get turned
        into the unicode unknown-character glyph.

        """
        if hasattr(value, 'name'):
            return value
        value = ''.join(linesep_splitter.split(value))
        return self.header_factory(name, value)

    def 折行(self, name, value):
        """+
        Header folding is controlled by the refold_source policy setting.  A
        value is considered to be a 'source value' if and only if it does not
        have a 'name' attribute (having a 'name' attribute means it is a header
        object of some sort).  If a source value needs to be refolded according
        to the policy, it is converted into a custom header object by passing
        the name and the value with any linesep characters removed to the
        header_factory method.  Folding of a custom header object is done by
        calling its fold method with the current policy.

        Source values are split into lines using splitlines.  If the value is
        not to be refolded, the lines are rejoined using the linesep from the
        policy and returned.  The exception is lines containing non-ascii
        binary data.  In that case the value is refolded regardless of the
        refold_source setting, which causes the binary data to be CTE encoded
        using the unknown-8bit charset.

        """
        return self._fold(name, value, refold_binary=True)

    def 折行字节(self, name, value):
        """+
        The same as fold if cte_type is 7bit, except that the returned value is
        bytes.

        If cte_type is 8bit, non-ASCII binary data is converted back into
        bytes.  Headers with binary data are not refolded, regardless of the
        refold_header setting, since there is no way to know whether the binary
        data consists of single byte characters or multibyte characters.

        If utf8 is true, headers are encoded to utf8, otherwise to ascii with
        non-ASCII unicode rendered as encoded words.

        """
        folded = self._fold(name, value, refold_binary=self.cte_type == '7bit')
        字符集 = 'utf8' if self.utf8 else 'ascii'
        return folded.encode(字符集, 'surrogateescape')

    def _fold(self, name, value, refold_binary=False):
        if hasattr(value, 'name'):
            return value.fold(policy=self)
        maxlen = self.max_line_length if self.max_line_length else sys.maxsize
        lines = linesep_splitter.split(value)
        refold = self.refold_source == 'all' or (self.refold_source == 'long' and (lines and len(lines[0]) + len(name) + 2 > maxlen or any((len(x) > maxlen for x in lines[1:]))))
        if not refold:
            if not self.utf8:
                refold = not value.isascii()
            elif refold_binary:
                refold = _has_surrogates(value)
        if refold:
            return self.header_factory(name, ''.join(lines)).fold(policy=self)
        return name + ': ' + self.linesep.join(lines) + self.linesep
_装类转发(邮件策略, {'fold': '折行', 'fold_binary': '折行字节', 'header_fetch_parse': '取出时解析邮件头', 'header_max_count': '邮件头最大个数', 'header_source_parse': '解析邮件头源', 'header_store_parse': '存储时解析邮件头'}, {'fold': '折行', 'fold_binary': '折行字节', 'header_fetch_parse': '取出时解析邮件头', 'header_max_count': '邮件头最大个数', 'header_source_parse': '解析邮件头源', 'header_store_parse': '存储时解析邮件头'})
默认策略 = 邮件策略()
del 默认策略.header_factory
严格策略 = 默认策略.clone(raise_on_defect=True)
SMTP策略 = 默认策略.clone(linesep='\r\n')
HTTP策略 = 默认策略.clone(linesep='\r\n', max_line_length=None)
SMTPUTF8策略 = SMTP策略.clone(utf8=True)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'EmailPolicy': '邮件策略',
    'HTTP': 'HTTP策略',
    'SMTP': 'SMTP策略',
    'SMTPUTF8': 'SMTPUTF8策略',
    'default': '默认策略',
    'strict': '严格策略',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '邮件策略': {
        'fold': '折行',
        'fold_binary': '折行字节',
        'header_fetch_parse': '取出时解析邮件头',
        'header_max_count': '邮件头最大个数',
        'header_source_parse': '解析邮件头源',
        'header_store_parse': '存储时解析邮件头',
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
    '邮件策略': {
        'fold': '折行',
        'fold_binary': '折行字节',
        'header_fetch_parse': '取出时解析邮件头',
        'header_max_count': '邮件头最大个数',
        'header_source_parse': '解析邮件头源',
        'header_store_parse': '存储时解析邮件头',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'HTTP策略',
    'SMTP策略',
    '严格策略',
    '邮件策略',
    '默认策略',
]

# ---- 转发层结束 ----
