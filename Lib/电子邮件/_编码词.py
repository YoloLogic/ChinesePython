# -*- coding: utf-8 -*-
"""电子邮件._编码词 —— 汉语库（由 tools/汉化库.py 从 Lib/email/_encoded_words.py 机械生成，**不要手改**）。

英文库 Lib/email._encoded_words.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


""" Routines for manipulating RFC2047 encoded words.

This is currently a package-private API, but will be considered for promotion
to a public API if there is demand.

"""
_英文原名表 = {'decode': '解码', 'decode_b': '解码B', 'decode_q': '解码Q', 'encode_b': '编码B', 'encode_q': '编码Q', 'len_b': 'B长度', 'len_q': 'Q长度'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import re
import base64
import binascii
import functools
from string import ascii_letters, digits
from 电子邮件 import 错误
__all__ = ['decode_q', 'encode_q', 'decode_b', 'encode_b', 'len_q', 'len_b', 'decode', 'encode']
_q_byte_subber = functools.partial(re.compile(b'=([a-fA-F0-9]{2})').sub, lambda m: bytes.fromhex(m.group(1).decode()))

def 解码Q(encoded):
    encoded = encoded.replace(b'_', b' ')
    return (_q_byte_subber(encoded), [])

class _QByteMap(dict):
    safe = b'-!*+/' + ascii_letters.encode('ascii') + digits.encode('ascii')

    def __missing__(self, key):
        if key in self.safe:
            self[key] = chr(key)
        else:
            self[key] = '={:02X}'.format(key)
        return self[key]
_q_byte_map = _QByteMap()
_q_byte_map[ord(' ')] = '_'

def 编码Q(bstring):
    return ''.join((_q_byte_map[x] for x in bstring))

def Q长度(bstring):
    return sum((len(_q_byte_map[x]) for x in bstring))

def 解码B(encoded):
    pad_err = len(encoded) % 4
    missing_padding = b'==='[:4 - pad_err] if pad_err else b''
    try:
        return (base64.b64decode(encoded + missing_padding, validate=True), [错误.InvalidBase64PaddingDefect()] if pad_err else [])
    except binascii.Error:
        try:
            return (base64.b64decode(encoded, validate=False), [错误.InvalidBase64CharactersDefect()])
        except binascii.Error:
            try:
                return (base64.b64decode(encoded + b'==', validate=False), [错误.InvalidBase64CharactersDefect(), 错误.InvalidBase64PaddingDefect()])
            except binascii.Error:
                return (encoded, [错误.InvalidBase64LengthDefect()])

def 编码B(bstring):
    return base64.b64encode(bstring).decode('ascii')

def B长度(bstring):
    groups_of_3, leftover = divmod(len(bstring), 3)
    return groups_of_3 * 4 + (4 if leftover else 0)
_cte_decoders = {'q': 解码Q, 'b': 解码B}

def 解码(ew):
    """Decode encoded word and return (string, charset, lang, defects) tuple.

    An RFC 2047/2243 encoded word has the form:

        =?charset*lang?cte?encoded_string?=

    where '*lang' may be omitted but the other parts may not be.

    This function expects exactly such a string (that is, it does not check the
    syntax and may raise errors if the string is not well formed), and returns
    the encoded_string decoded first from its Content Transfer Encoding and
    then from the resulting bytes into unicode using the specified charset.  If
    the cte-decoded string does not successfully decode using the specified
    character set, a defect is added to the defects list and the unknown octets
    are replaced by the unicode 'unknown' character \\uFDFF.

    The specified charset and language are returned.  The default for language,
    which is rarely if ever encountered, is the empty string.

    """
    _, 字符集, cte, cte_string, _ = ew.split('?')
    字符集, _, lang = 字符集.partition('*')
    cte = cte.lower()
    bstring = cte_string.encode('ascii', 'surrogateescape')
    bstring, defects = _cte_decoders[cte](bstring)
    try:
        string = bstring.decode(字符集)
    except UnicodeDecodeError:
        defects.append(错误.UndecodableBytesDefect(f'Encoded word contains bytes not decodable using {字符集!r} charset'))
        string = bstring.decode(字符集, 'surrogateescape')
    except (LookupError, UnicodeEncodeError):
        string = bstring.decode('ascii', 'surrogateescape')
        if 字符集.lower() != 'unknown-8bit':
            defects.append(错误.CharsetError(f'Unknown charset {字符集!r} in encoded word; decoded as unknown bytes'))
    return (string, 字符集, lang, defects)
_cte_encoders = {'q': 编码Q, 'b': 编码B}
_cte_encode_length = {'q': Q长度, 'b': B长度}

def encode(string, charset='utf-8', encoding=None, lang=''):
    """Encode string using the CTE encoding that produces the shorter result.

    Produces an RFC 2047/2243 encoded word of the form:

        =?charset*lang?cte?encoded_string?=

    where '*lang' is omitted unless the 'lang' parameter is given a value.
    Optional argument charset (defaults to utf-8) specifies the charset to use
    to encode the string to binary before CTE encoding it.  Optional argument
    'encoding' is the cte specifier for the encoding that should be used ('q'
    or 'b'); if it is None (the default) the encoding which produces the
    shortest encoded sequence is used, except that 'q' is preferred if it is up
    to five characters longer.  Optional argument 'lang' (default '') gives the
    RFC 2243 language string to specify in the encoded word.

    """
    if charset == 'unknown-8bit':
        bstring = string.encode('utf-8', 'surrogateescape')
    else:
        bstring = string.encode(charset)
    if encoding is None:
        qlen = _cte_encode_length['q'](bstring)
        blen = _cte_encode_length['b'](bstring)
        encoding = 'q' if qlen - blen < 5 else 'b'
    encoded = _cte_encoders[encoding](bstring)
    if lang:
        lang = '*' + lang
    return '=?{}{}?{}?{}?='.format(charset, lang, encoding, encoded)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'decode': '解码',
    'decode_b': '解码B',
    'decode_q': '解码Q',
    'encode_b': '编码B',
    'encode_q': '编码Q',
    'len_b': 'B长度',
    'len_q': 'Q长度',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'B长度',
    'Q长度',
    '编码B',
    '编码Q',
    '解码',
    '解码B',
    '解码Q',
]

# ---- 转发层结束 ----
