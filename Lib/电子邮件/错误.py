# -*- coding: utf-8 -*-
"""电子邮件.错误 —— 汉语库（由 tools/汉化库.py 从 Lib/email/errors.py 机械生成，**不要手改**）。

英文库 Lib/email.errors.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""email package exception classes."""
_英文原名表 = {'BoundaryError': '边界错误', 'CharsetError': '字符集错误', 'CloseBoundaryNotFoundDefect': '结束边界找不到缺陷', 'FirstHeaderLineIsContinuationDefect': '首行是续行缺陷', 'HeaderDefect': '邮件头缺陷', 'HeaderMissingRequiredValue': '邮件头缺必填值', 'HeaderParseError': '邮件头解析错误', 'HeaderWriteError': '邮件头写出错误', 'InvalidBase64CharactersDefect': '无效base64字符缺陷', 'InvalidBase64LengthDefect': '无效base64长度缺陷', 'InvalidBase64PaddingDefect': '无效base64填充缺陷', 'InvalidDateDefect': '无效日期缺陷', 'InvalidHeaderDefect': '无效邮件头缺陷', 'InvalidMultipartContentTransferEncodingDefect': '无效多部分传输编码缺陷', 'MalformedHeaderDefect': '头格式错误缺陷', 'MessageDefect': '邮件缺陷', 'MessageError': '邮件错误', 'MessageParseError': '邮件解析错误', 'MisplacedEnvelopeHeaderDefect': '信封头位置不对缺陷', 'MissingHeaderBodySeparatorDefect': '缺头体分隔符缺陷', 'MultipartConversionError': '多部分转换错误', 'MultipartInvariantViolationDefect': '多部分不变式违反缺陷', 'NoBoundaryInMultipartDefect': '多部分无边界缺陷', 'NonASCIILocalPartDefect': '本地部分非ASCII缺陷', 'NonPrintableDefect': '不可打印字符缺陷', 'ObsoleteHeaderDefect': '过时邮件头缺陷', 'StartBoundaryNotFoundDefect': '起始边界找不到缺陷', 'UndecodableBytesDefect': '无法解码字节缺陷'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)

class 邮件错误(Exception):
    """Base class for errors in the email package."""

class 邮件解析错误(邮件错误):
    """Base class for message parsing errors."""

class 邮件头解析错误(邮件解析错误):
    """Error while parsing headers."""

class 边界错误(邮件解析错误):
    """Couldn't find terminating boundary."""

class 多部分转换错误(邮件错误, TypeError):
    """Conversion to a multipart is prohibited."""

class 字符集错误(邮件错误):
    """An illegal charset was given."""

class 邮件头写出错误(邮件错误):
    """Error while writing headers."""

class 邮件缺陷(ValueError):
    """Base class for a message defect."""

    def __init__(self, line=None):
        if line is not None:
            super().__init__(line)
        self.line = line

class 多部分无边界缺陷(邮件缺陷):
    """A message claimed to be a multipart but had no boundary parameter."""

class 起始边界找不到缺陷(邮件缺陷):
    """The claimed start boundary was never found."""

class 结束边界找不到缺陷(邮件缺陷):
    """A start boundary was found, but not the corresponding close boundary."""

class 首行是续行缺陷(邮件缺陷):
    """A message had a continuation line as its first header line."""

class 信封头位置不对缺陷(邮件缺陷):
    """A 'Unix-from' header was found in the middle of a header block."""

class 缺头体分隔符缺陷(邮件缺陷):
    """Found line with no leading whitespace and no colon before blank line."""
头格式错误缺陷 = 缺头体分隔符缺陷

class 多部分不变式违反缺陷(邮件缺陷):
    """A message claimed to be a multipart but no subparts were found."""

class 无效多部分传输编码缺陷(邮件缺陷):
    """An invalid content transfer encoding was set on the multipart itself."""

class 无法解码字节缺陷(邮件缺陷):
    """Header contained bytes that could not be decoded"""

class 无效base64填充缺陷(邮件缺陷):
    """base64 encoded sequence had an incorrect length"""

class 无效base64字符缺陷(邮件缺陷):
    """base64 encoded sequence had characters not in base64 alphabet"""

class 无效base64长度缺陷(邮件缺陷):
    """base64 encoded sequence had invalid length (1 mod 4)"""

class 邮件头缺陷(邮件缺陷):
    """Base class for a header defect."""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)

class 无效邮件头缺陷(邮件头缺陷):
    """Header is not valid, message gives details."""

class 邮件头缺必填值(邮件头缺陷):
    """A header that must have a value had none"""

class 不可打印字符缺陷(邮件头缺陷):
    """ASCII characters outside the ascii-printable range found"""

    def __init__(self, non_printables):
        super().__init__(non_printables)
        self.non_printables = non_printables

    def __str__(self):
        return 'the following ASCII non-printables found in header: {}'.format(self.non_printables)

class 过时邮件头缺陷(邮件头缺陷):
    """Header uses syntax declared obsolete by RFC 5322"""

class 本地部分非ASCII缺陷(邮件头缺陷):
    """local_part contains non-ASCII characters"""

class 无效日期缺陷(邮件头缺陷):
    """Header has unparsable or invalid date"""


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BoundaryError': '边界错误',
    'CharsetError': '字符集错误',
    'CloseBoundaryNotFoundDefect': '结束边界找不到缺陷',
    'FirstHeaderLineIsContinuationDefect': '首行是续行缺陷',
    'HeaderDefect': '邮件头缺陷',
    'HeaderMissingRequiredValue': '邮件头缺必填值',
    'HeaderParseError': '邮件头解析错误',
    'HeaderWriteError': '邮件头写出错误',
    'InvalidBase64CharactersDefect': '无效base64字符缺陷',
    'InvalidBase64LengthDefect': '无效base64长度缺陷',
    'InvalidBase64PaddingDefect': '无效base64填充缺陷',
    'InvalidDateDefect': '无效日期缺陷',
    'InvalidHeaderDefect': '无效邮件头缺陷',
    'InvalidMultipartContentTransferEncodingDefect': '无效多部分传输编码缺陷',
    'MalformedHeaderDefect': '头格式错误缺陷',
    'MessageDefect': '邮件缺陷',
    'MessageError': '邮件错误',
    'MessageParseError': '邮件解析错误',
    'MisplacedEnvelopeHeaderDefect': '信封头位置不对缺陷',
    'MissingHeaderBodySeparatorDefect': '缺头体分隔符缺陷',
    'MultipartConversionError': '多部分转换错误',
    'MultipartInvariantViolationDefect': '多部分不变式违反缺陷',
    'NoBoundaryInMultipartDefect': '多部分无边界缺陷',
    'NonASCIILocalPartDefect': '本地部分非ASCII缺陷',
    'NonPrintableDefect': '不可打印字符缺陷',
    'ObsoleteHeaderDefect': '过时邮件头缺陷',
    'StartBoundaryNotFoundDefect': '起始边界找不到缺陷',
    'UndecodableBytesDefect': '无法解码字节缺陷',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
