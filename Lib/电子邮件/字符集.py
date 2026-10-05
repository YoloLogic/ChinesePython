# -*- coding: utf-8 -*-
"""电子邮件.字符集 —— 汉语库（由 tools/汉化库.py 从 Lib/email/charset.py 机械生成，**不要手改**）。

英文库 Lib/email.charset.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


_英文原名表 = {'Charset': '邮件字符集', 'add_alias': '加别名', 'add_charset': '加字符集', 'add_codec': '加编解码器'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['Charset', 'add_alias', 'add_charset', 'add_codec']
from functools import partial
import 电子邮件.base64编码
import 电子邮件.可打印编码
from 电子邮件 import 错误
from 电子邮件.编码器 import encode_7or8bit
QP = 1
BASE64 = 2
SHORTEST = 3
RFC2047_CHROME_LEN = 7
DEFAULT_CHARSET = 'us-ascii'
UNKNOWN8BIT = 'unknown-8bit'
EMPTYSTRING = ''
CHARSETS = {'iso-8859-1': (QP, QP, None), 'iso-8859-2': (QP, QP, None), 'iso-8859-3': (QP, QP, None), 'iso-8859-4': (QP, QP, None), 'iso-8859-9': (QP, QP, None), 'iso-8859-10': (QP, QP, None), 'iso-8859-13': (QP, QP, None), 'iso-8859-14': (QP, QP, None), 'iso-8859-15': (QP, QP, None), 'iso-8859-16': (QP, QP, None), 'windows-1252': (QP, QP, None), 'viscii': (QP, QP, None), 'us-ascii': (None, None, None), 'big5': (BASE64, BASE64, None), 'gb2312': (BASE64, BASE64, None), 'euc-jp': (BASE64, None, 'iso-2022-jp'), 'shift_jis': (BASE64, None, 'iso-2022-jp'), 'iso-2022-jp': (BASE64, None, None), 'koi8-r': (BASE64, BASE64, None), 'utf-8': (SHORTEST, BASE64, 'utf-8')}
ALIASES = {'latin_1': 'iso-8859-1', 'latin-1': 'iso-8859-1', 'latin_2': 'iso-8859-2', 'latin-2': 'iso-8859-2', 'latin_3': 'iso-8859-3', 'latin-3': 'iso-8859-3', 'latin_4': 'iso-8859-4', 'latin-4': 'iso-8859-4', 'latin_5': 'iso-8859-9', 'latin-5': 'iso-8859-9', 'latin_6': 'iso-8859-10', 'latin-6': 'iso-8859-10', 'latin_7': 'iso-8859-13', 'latin-7': 'iso-8859-13', 'latin_8': 'iso-8859-14', 'latin-8': 'iso-8859-14', 'latin_9': 'iso-8859-15', 'latin-9': 'iso-8859-15', 'latin_10': 'iso-8859-16', 'latin-10': 'iso-8859-16', 'cp949': 'ks_c_5601-1987', 'euc_jp': 'euc-jp', 'euc_kr': 'euc-kr', 'ascii': 'us-ascii'}
CODEC_MAP = {'us-ascii': None}

def 加字符集(charset, header_enc=None, body_enc=None, output_charset=None):
    """Add character set properties to the global registry.

    charset is the input character set, and must be the canonical name of a
    character set.

    Optional header_enc and body_enc is either charset.QP for
    quoted-printable, charset.BASE64 for base64 encoding, charset.SHORTEST for
    the shortest of qp or base64 encoding, or None for no encoding.  SHORTEST
    is only valid for header_enc.  It describes how message headers and
    message bodies in the input charset are to be encoded.  Default is no
    encoding.

    Optional output_charset is the character set that the output should be
    in.  Conversions will proceed from input charset, to Unicode, to the
    output charset when the method Charset.convert() is called.  The default
    is to output in the same character set as the input.

    Both input_charset and output_charset must have Unicode codec entries in
    the module's charset-to-codec mapping; use add_codec(charset, codecname)
    to add codecs the module does not know about.  See the codecs module's
    documentation for more information.
    """
    if body_enc == SHORTEST:
        raise ValueError('SHORTEST not allowed for body_enc')
    CHARSETS[charset] = (header_enc, body_enc, output_charset)

def 加别名(alias, canonical):
    """Add a character set alias.

    alias is the alias name, e.g. latin-1
    canonical is the character set's canonical name, e.g. iso-8859-1
    """
    ALIASES[alias] = canonical

def 加编解码器(charset, codecname):
    """Add a codec that map characters in the given charset to/from Unicode.

    charset is the canonical name of a character set.  codecname is the name
    of a Python codec, as appropriate for the second argument to the unicode()
    built-in, or to the encode() method of a Unicode string.
    """
    CODEC_MAP[charset] = codecname

def _encode(string, codec):
    if codec == UNKNOWN8BIT:
        return string.encode('ascii', 'surrogateescape')
    else:
        return string.encode(codec)

class 邮件字符集:
    """Map character sets to their email properties.

    This class provides information about the requirements imposed on email
    for a specific character set.  It also provides convenience routines for
    converting between character sets, given the availability of the
    applicable codecs.  Given a character set, it will do its best to provide
    information on how to use that character set in an email in an
    RFC-compliant way.

    Certain character sets must be encoded with quoted-printable or base64
    when used in email headers or bodies.  Certain character sets must be
    converted outright, and are not allowed in email.  Instances of this
    module expose the following information about a character set:

    input_charset: The initial character set specified.  Common aliases
                   are converted to their 'official' email names (e.g. latin_1
                   is converted to iso-8859-1).  Defaults to 7-bit us-ascii.

    header_encoding: If the character set must be encoded before it can be
                     used in an email header, this attribute will be set to
                     charset.QP (for quoted-printable), charset.BASE64 (for
                     base64 encoding), or charset.SHORTEST for the shortest of
                     QP or BASE64 encoding.  Otherwise, it will be None.

    body_encoding: Same as header_encoding, but describes the encoding for the
                   mail message's body, which indeed may be different than the
                   header encoding.  charset.SHORTEST is not allowed for
                   body_encoding.

    output_charset: Some character sets must be converted before they can be
                    used in email headers or bodies.  If the input_charset is
                    one of them, this attribute will contain the name of the
                    charset output will be converted to.  Otherwise, it will
                    be None.

    input_codec: The name of the Python codec used to convert the
                 input_charset to Unicode.  If no conversion codec is
                 necessary, this attribute will be None.

    output_codec: The name of the Python codec used to convert Unicode
                  to the output_charset.  If no conversion codec is necessary,
                  this attribute will have the same value as the input_codec.
    """

    def __init__(self, input_charset=DEFAULT_CHARSET):
        try:
            if isinstance(input_charset, str):
                input_charset.encode('ascii')
            else:
                input_charset = str(input_charset, 'ascii')
        except UnicodeError:
            raise 错误.CharsetError(input_charset)
        input_charset = input_charset.lower()
        self.input_charset = ALIASES.get(input_charset, input_charset)
        henc, benc, conv = CHARSETS.get(self.input_charset, (SHORTEST, BASE64, None))
        if not conv:
            conv = self.input_charset
        self.header_encoding = henc
        self.body_encoding = benc
        self.output_charset = ALIASES.get(conv, conv)
        self.input_codec = CODEC_MAP.get(self.input_charset, self.input_charset)
        self.output_codec = CODEC_MAP.get(self.output_charset, self.output_charset)

    def __repr__(self):
        return self.input_charset.lower()

    def __eq__(self, other):
        return str(self) == str(other).lower()

    def get_body_encoding(self):
        """Return the content-transfer-encoding used for body encoding.

        This is either the string 'quoted-printable' or 'base64' depending on
        the encoding used, or it is a function in which case you should call
        the function with a single argument, the Message object being
        encoded.  The function should then set the Content-Transfer-Encoding
        header itself to whatever is appropriate.

        Returns "quoted-printable" if self.body_encoding is QP.
        Returns "base64" if self.body_encoding is BASE64.
        Returns conversion function otherwise.
        """
        assert self.body_encoding != SHORTEST
        if self.body_encoding == QP:
            return 'quoted-printable'
        elif self.body_encoding == BASE64:
            return 'base64'
        else:
            return encode_7or8bit

    def get_output_charset(self):
        """Return the output character set.

        This is self.output_charset if that is not None, otherwise it is
        self.input_charset.
        """
        return self.output_charset or self.input_charset

    def header_encode(self, string):
        """Header-encode a string by converting it first to bytes.

        The type of encoding (base64 or quoted-printable) will be based on
        this charset's `header_encoding`.

        :param string: A unicode string for the header.  It must be possible
            to encode this string to bytes using the character set's
            output codec.
        :return: The encoded string, with RFC 2047 chrome.
        """
        codec = self.output_codec or 'us-ascii'
        header_bytes = _encode(string, codec)
        encoder_module = self._get_encoder(header_bytes)
        if encoder_module is None:
            return string
        return encoder_module.header_encode(header_bytes, codec)

    def header_encode_lines(self, string, maxlengths):
        """Header-encode a string by converting it first to bytes.

        This is similar to `header_encode()` except that the string is fit
        into maximum line lengths as given by the argument.

        :param string: A unicode string for the header.  It must be possible
            to encode this string to bytes using the character set's
            output codec.
        :param maxlengths: Maximum line length iterator.  Each element
            returned from this iterator will provide the next maximum line
            length.  This parameter is used as an argument to built-in next()
            and should never be exhausted.  The maximum line lengths should
            not count the RFC 2047 chrome.  These line lengths are only a
            hint; the splitter does the best it can.
        :return: Lines of encoded strings, each with RFC 2047 chrome.
        """
        codec = self.output_codec or 'us-ascii'
        header_bytes = _encode(string, codec)
        encoder_module = self._get_encoder(header_bytes)
        encoder = partial(encoder_module.header_encode, charset=codec)
        字符集 = self.get_output_charset()
        extra = len(字符集) + RFC2047_CHROME_LEN
        lines = []
        current_line = []
        maxlen = next(maxlengths) - extra
        for character in string:
            current_line.append(character)
            this_line = EMPTYSTRING.join(current_line)
            length = encoder_module.header_length(_encode(this_line, 字符集))
            if length > maxlen:
                current_line.pop()
                if not lines and (not current_line):
                    lines.append(None)
                else:
                    joined_line = EMPTYSTRING.join(current_line)
                    header_bytes = _encode(joined_line, codec)
                    lines.append(encoder(header_bytes))
                current_line = [character]
                maxlen = next(maxlengths) - extra
        joined_line = EMPTYSTRING.join(current_line)
        header_bytes = _encode(joined_line, codec)
        lines.append(encoder(header_bytes))
        return lines

    def _get_encoder(self, header_bytes):
        if self.header_encoding == BASE64:
            return 电子邮件.base64编码
        elif self.header_encoding == QP:
            return 电子邮件.可打印编码
        elif self.header_encoding == SHORTEST:
            len64 = 电子邮件.base64编码.header_length(header_bytes)
            lenqp = 电子邮件.可打印编码.header_length(header_bytes)
            if len64 < lenqp:
                return 电子邮件.base64编码
            else:
                return 电子邮件.可打印编码
        else:
            return None

    def body_encode(self, string):
        """Body-encode a string by converting it first to bytes.

        The type of encoding (base64 or quoted-printable) will be based on
        self.body_encoding.  If body_encoding is None, we assume the
        output charset is a 7bit encoding, so re-encoding the decoded
        string using the ascii codec produces the correct string version
        of the content.
        """
        if not string:
            return string
        if self.body_encoding is BASE64:
            if isinstance(string, str):
                string = string.encode(self.output_charset)
            return 电子邮件.base64编码.body_encode(string)
        elif self.body_encoding is QP:
            if isinstance(string, str):
                string = string.encode(self.output_charset)
            string = string.decode('latin1')
            return 电子邮件.可打印编码.body_encode(string)
        else:
            if isinstance(string, str):
                string = string.encode(self.output_charset).decode('ascii')
            return string


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Charset': '邮件字符集',
    'add_alias': '加别名',
    'add_charset': '加字符集',
    'add_codec': '加编解码器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '加别名',
    '加字符集',
    '加编解码器',
    '邮件字符集',
])

# ---- 转发层结束 ----
