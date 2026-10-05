# -*- coding: utf-8 -*-
"""基64编码 —— 汉语库（由 tools/汉化库.py 从 Lib/base64.py 机械生成，**不要手改**）。

英文库 Lib/base64.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 基64编码
"""


"""Base16, Base32, Base64 (RFC 4648), Base85 and Ascii85 data encodings"""
_英文原名表 = {'MAXBINSIZE': '最大二进制块', 'MAXLINESIZE': '最大行宽', 'a85decode': 'ASCII85解码', 'a85encode': 'ASCII85编码', 'b16decode': '基16解码', 'b16encode': '基16编码', 'b32decode': '基32解码', 'b32encode': '基32编码', 'b32hexdecode': '基32HEX解码', 'b32hexencode': '基32HEX编码', 'b64decode': '基64解码', 'b64encode': '基64编码', 'b85decode': '基85解码', 'b85encode': '基85编码', 'decode': '解码', 'decodebytes': '解码字节串', 'encode': '编码', 'encodebytes': '编码字节串', 'main': '主函数', 'standard_b64decode': '标准基64解码', 'standard_b64encode': '标准基64编码', 'urlsafe_b64decode': '网址安全基64解码', 'urlsafe_b64encode': '网址安全基64编码', 'z85decode': 'Z85解码', 'z85encode': 'Z85编码'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import struct
import binascii
__all__ = ['encode', 'decode', 'encodebytes', 'decodebytes', 'b64encode', 'b64decode', 'b32encode', 'b32decode', 'b32hexencode', 'b32hexdecode', 'b16encode', 'b16decode', 'b85encode', 'b85decode', 'a85encode', 'a85decode', 'z85encode', 'z85decode', 'standard_b64encode', 'standard_b64decode', 'urlsafe_b64encode', 'urlsafe_b64decode']
bytes_types = (bytes, bytearray)

def _bytes_from_decode_data(s):
    if isinstance(s, str):
        try:
            return s.encode('ascii')
        except UnicodeEncodeError:
            raise ValueError('string argument should contain only ASCII characters')
    if isinstance(s, bytes_types):
        return s
    try:
        return memoryview(s).tobytes()
    except TypeError:
        raise TypeError('argument should be a bytes-like object or ASCII string, not %r' % s.__class__.__name__) from None

def 基64编码(s, altchars=None):
    """Encode the bytes-like object s using Base64 and return a bytes object.

    Optional altchars should be a byte string of length 2 which specifies an
    alternative alphabet for the '+' and '/' characters.  This allows an
    application to e.g. generate url or filesystem safe Base64 strings.
    """
    encoded = binascii.b2a_base64(s, newline=False)
    if altchars is not None:
        assert len(altchars) == 2, repr(altchars)
        return encoded.translate(bytes.maketrans(b'+/', altchars))
    return encoded

def 基64解码(s, altchars=None, validate=False):
    """Decode the Base64 encoded bytes-like object or ASCII string s.

    Optional altchars must be a bytes-like object or ASCII string of length 2
    which specifies the alternative alphabet used instead of the '+' and '/'
    characters.

    The result is returned as a bytes object.  A binascii.Error is raised if
    s is incorrectly padded.

    If validate is False (the default), characters that are neither in the
    normal base-64 alphabet nor the alternative alphabet are discarded prior
    to the padding check.  If validate is True, these non-alphabet characters
    in the input result in a binascii.Error.
    For more information about the strict base64 check, see:

    https://docs.python.org/3.11/library/binascii.html#binascii.a2b_base64
    """
    s = _bytes_from_decode_data(s)
    if altchars is not None:
        altchars = _bytes_from_decode_data(altchars)
        assert len(altchars) == 2, repr(altchars)
        s = s.translate(bytes.maketrans(altchars, b'+/'))
    return binascii.a2b_base64(s, strict_mode=validate)

def 标准基64编码(s):
    """Encode bytes-like object s using the standard Base64 alphabet.

    The result is returned as a bytes object.
    """
    return 基64编码(s)

def 标准基64解码(s):
    """Decode bytes encoded with the standard Base64 alphabet.

    Argument s is a bytes-like object or ASCII string to decode.  The result
    is returned as a bytes object.  A binascii.Error is raised if the input
    is incorrectly padded.  Characters that are not in the standard alphabet
    are discarded prior to the padding check.
    """
    return 基64解码(s)
_urlsafe_encode_translation = bytes.maketrans(b'+/', b'-_')
_urlsafe_decode_translation = bytes.maketrans(b'-_', b'+/')

def 网址安全基64编码(s):
    """Encode bytes using the URL- and filesystem-safe Base64 alphabet.

    Argument s is a bytes-like object to encode.  The result is returned as a
    bytes object.  The alphabet uses '-' instead of '+' and '_' instead of
    '/'.
    """
    return 基64编码(s).translate(_urlsafe_encode_translation)

def 网址安全基64解码(s):
    """Decode bytes using the URL- and filesystem-safe Base64 alphabet.

    Argument s is a bytes-like object or ASCII string to decode.  The result
    is returned as a bytes object.  A binascii.Error is raised if the input
    is incorrectly padded.  Characters that are not in the URL-safe base-64
    alphabet, and are not a plus '+' or slash '/', are discarded prior to the
    padding check.

    The alphabet uses '-' instead of '+' and '_' instead of '/'.
    """
    s = _bytes_from_decode_data(s)
    s = s.translate(_urlsafe_decode_translation)
    return 基64解码(s)
_B32_ENCODE_DOCSTRING = '\nEncode the bytes-like objects using {encoding} and return a bytes object.\n'
_B32_DECODE_DOCSTRING = '\nDecode the {encoding} encoded bytes-like object or ASCII string s.\n\nOptional casefold is a flag specifying whether a lowercase alphabet is\nacceptable as input.  For security purposes, the default is False.\n{extra_args}\nThe result is returned as a bytes object.  A binascii.Error is raised if\nthe input is incorrectly padded or if there are non-alphabet\ncharacters present in the input.\n'
_B32_DECODE_MAP01_DOCSTRING = '\nRFC 4648 allows for optional mapping of the digit 0 (zero) to the\nletter O (oh), and for optional mapping of the digit 1 (one) to\neither the letter I (eye) or letter L (el).  The optional argument\nmap01 when not None, specifies which letter the digit 1 should be\nmapped to (when map01 is not None, the digit 0 is always mapped to\nthe letter O).  For security purposes the default is None, so that\n0 and 1 are not allowed in the input.\n'
_b32alphabet = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
_b32hexalphabet = b'0123456789ABCDEFGHIJKLMNOPQRSTUV'
_b32tab2 = {}
_b32rev = {}

def _b32encode(alphabet, s):
    if alphabet not in _b32tab2:
        b32tab = [bytes((i,)) for i in alphabet]
        _b32tab2[alphabet] = [a + b for a in b32tab for b in b32tab]
        b32tab = None
    if not isinstance(s, bytes_types):
        s = memoryview(s).tobytes()
    leftover = len(s) % 5
    if leftover:
        s = s + b'\x00' * (5 - leftover)
    encoded = bytearray()
    from_bytes = int.from_bytes
    b32tab2 = _b32tab2[alphabet]
    for i in range(0, len(s), 5):
        c = from_bytes(s[i:i + 5])
        encoded += b32tab2[c >> 30] + b32tab2[c >> 20 & 1023] + b32tab2[c >> 10 & 1023] + b32tab2[c & 1023]
    if leftover == 1:
        encoded[-6:] = b'======'
    elif leftover == 2:
        encoded[-4:] = b'===='
    elif leftover == 3:
        encoded[-3:] = b'==='
    elif leftover == 4:
        encoded[-1:] = b'='
    return bytes(encoded)

def _b32decode(alphabet, s, casefold=False, map01=None):
    if alphabet not in _b32rev:
        _b32rev[alphabet] = {v: k for k, v in enumerate(alphabet)}
    s = _bytes_from_decode_data(s)
    if len(s) % 8:
        raise binascii.Error('Incorrect padding')
    if map01 is not None:
        map01 = _bytes_from_decode_data(map01)
        assert len(map01) == 1, repr(map01)
        s = s.translate(bytes.maketrans(b'01', b'O' + map01))
    if casefold:
        s = s.upper()
    l = len(s)
    s = s.rstrip(b'=')
    padchars = l - len(s)
    decoded = bytearray()
    b32rev = _b32rev[alphabet]
    for i in range(0, len(s), 8):
        quanta = s[i:i + 8]
        acc = 0
        try:
            for c in quanta:
                acc = (acc << 5) + b32rev[c]
        except KeyError:
            raise binascii.Error('Non-base32 digit found') from None
        decoded += acc.to_bytes(5)
    if l % 8 or padchars not in {0, 1, 3, 4, 6}:
        raise binascii.Error('Incorrect padding')
    if padchars and decoded:
        acc <<= 5 * padchars
        last = acc.to_bytes(5)
        leftover = (43 - 5 * padchars) // 8
        decoded[-5:] = last[:leftover]
    return bytes(decoded)

def 基32编码(s):
    return _b32encode(_b32alphabet, s)
基32编码.__doc__ = _B32_ENCODE_DOCSTRING.format(encoding='base32')

def 基32解码(s, casefold=False, map01=None):
    return _b32decode(_b32alphabet, s, casefold, map01)
基32解码.__doc__ = _B32_DECODE_DOCSTRING.format(encoding='base32', extra_args=_B32_DECODE_MAP01_DOCSTRING)

def 基32HEX编码(s):
    return _b32encode(_b32hexalphabet, s)
基32HEX编码.__doc__ = _B32_ENCODE_DOCSTRING.format(encoding='base32hex')

def 基32HEX解码(s, casefold=False):
    return _b32decode(_b32hexalphabet, s, casefold)
基32HEX解码.__doc__ = _B32_DECODE_DOCSTRING.format(encoding='base32hex', extra_args='')

def 基16编码(s):
    """Encode the bytes-like object s using Base16 and return a bytes object.
    """
    return binascii.hexlify(s).upper()

def 基16解码(s, casefold=False):
    """Decode the Base16 encoded bytes-like object or ASCII string s.

    Optional casefold is a flag specifying whether a lowercase alphabet is
    acceptable as input.  For security purposes, the default is False.

    The result is returned as a bytes object.  A binascii.Error is raised if
    s is incorrectly padded or if there are non-alphabet characters present
    in the input.
    """
    s = _bytes_from_decode_data(s)
    if casefold:
        s = s.upper()
    if s.translate(None, delete=b'0123456789ABCDEF'):
        raise binascii.Error('Non-base16 digit found')
    return binascii.unhexlify(s)
_a85chars = None
_a85chars2 = None
_A85START = b'<~'
_A85END = b'~>'

def _85encode(b, chars, chars2, pad=False, foldnuls=False, foldspaces=False):
    if not isinstance(b, bytes_types):
        b = memoryview(b).tobytes()
    padding = -len(b) % 4
    if padding:
        b = b + b'\x00' * padding
    words = struct.Struct('!%dI' % (len(b) // 4)).unpack(b)
    chunks = [b'z' if foldnuls and (not word) else b'y' if foldspaces and word == 538976288 else chars2[word // 614125] + chars2[word // 85 % 7225] + chars[word % 85] for word in words]
    if padding and (not pad):
        if chunks[-1] == b'z':
            chunks[-1] = chars[0] * 5
        chunks[-1] = chunks[-1][:-padding]
    return b''.join(chunks)

def ASCII85编码(b, *, foldspaces=False, wrapcol=0, pad=False, adobe=False):
    """Encode bytes-like object b using Ascii85 and return a bytes object.

    foldspaces is an optional flag that uses the special short sequence 'y'
    instead of 4 consecutive spaces (ASCII 0x20) as supported by 'btoa'. This
    feature is not supported by the standard encoding used in PDF.

    If wrapcol is non-zero, insert a newline (b'\\n') character after at most
    every wrapcol characters.

    pad controls whether zero-padding applied to the end of the input
    is fully retained in the output encoding, as done by btoa,
    producing an exact multiple of 5 bytes of output.

    adobe controls whether the encoded byte sequence is framed with <~
    and ~>, as in a PostScript base-85 string literal.  Note that
    while ASCII85Decode streams in PDF documents must be terminated
    with ~>, they must not use a leading <~.

    """
    global _a85chars, _a85chars2
    if _a85chars2 is None:
        _a85chars = [bytes((i,)) for i in range(33, 118)]
        _a85chars2 = [a + b for a in _a85chars for b in _a85chars]
    result = _85encode(b, _a85chars, _a85chars2, pad, True, foldspaces)
    if adobe:
        result = _A85START + result
    if wrapcol:
        wrapcol = max(2 if adobe else 1, wrapcol)
        chunks = [result[i:i + wrapcol] for i in range(0, len(result), wrapcol)]
        if adobe:
            if len(chunks[-1]) + 2 > wrapcol:
                chunks.append(b'')
        result = b'\n'.join(chunks)
    if adobe:
        result += _A85END
    return result

def ASCII85解码(b, *, foldspaces=False, adobe=False, ignorechars=b' \t\n\r\x0b'):
    """Decode the Ascii85 encoded bytes-like object or ASCII string b.

    foldspaces is a flag that specifies whether the 'y' short sequence
    should be accepted as shorthand for 4 consecutive spaces (ASCII
    0x20).  This feature is not supported by the standard Ascii85
    encoding used in PDF and PostScript.

    adobe controls whether the <~ and ~> markers are present. While
    the leading <~ is not required, the input must end with ~>, or a
    ValueError is raised.

    ignorechars should be a byte string containing characters to ignore from the
    input. This should only contain whitespace characters, and by default
    contains all whitespace characters in ASCII.

    The result is returned as a bytes object.
    """
    b = _bytes_from_decode_data(b)
    if adobe:
        if not b.endswith(_A85END):
            raise ValueError('Ascii85 encoded byte sequences must end with {!r}'.format(_A85END))
        if b.startswith(_A85START):
            b = b[2:-2]
        else:
            b = b[:-2]
    packI = struct.Struct('!I').pack
    decoded = []
    decoded_append = decoded.append
    curr = []
    curr_append = curr.append
    curr_clear = curr.clear
    for x in b + b'u' * 4:
        if b'!'[0] <= x <= b'u'[0]:
            curr_append(x)
            if len(curr) == 5:
                acc = 0
                for x in curr:
                    acc = 85 * acc + (x - 33)
                try:
                    decoded_append(packI(acc))
                except struct.error:
                    raise ValueError('Ascii85 overflow') from None
                curr_clear()
        elif x == b'z'[0]:
            if curr:
                raise ValueError('z inside Ascii85 5-tuple')
            decoded_append(b'\x00\x00\x00\x00')
        elif foldspaces and x == b'y'[0]:
            if curr:
                raise ValueError('y inside Ascii85 5-tuple')
            decoded_append(b'    ')
        elif x in ignorechars:
            continue
        else:
            raise ValueError('Non-Ascii85 digit found: %c' % x)
    result = b''.join(decoded)
    padding = 4 - len(curr)
    if padding:
        result = result[:-padding]
    return result
_b85alphabet = b'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~'
_b85chars = None
_b85chars2 = None
_b85dec = None

def 基85编码(b, pad=False):
    """Encode bytes-like object b in base85 format and return a bytes object.

    The input is padded with b'\x00' so its length is a multiple of 4
    bytes before encoding.  If pad is true, all the resulting
    characters are retained in the output, which will always be a
    multiple of 5 bytes.
    """
    global _b85chars, _b85chars2
    if _b85chars2 is None:
        _b85chars = [bytes((i,)) for i in _b85alphabet]
        _b85chars2 = [a + b for a in _b85chars for b in _b85chars]
    return _85encode(b, _b85chars, _b85chars2, pad)

def 基85解码(b):
    """Decode the base85-encoded bytes-like object or ASCII string b

    The result is returned as a bytes object.
    """
    global _b85dec
    if _b85dec is None:
        b85dec_tmp = [None] * 256
        for i, c in enumerate(_b85alphabet):
            b85dec_tmp[c] = i
        _b85dec = b85dec_tmp
    b = _bytes_from_decode_data(b)
    padding = -len(b) % 5
    b = b + b'~' * padding
    out = []
    packI = struct.Struct('!I').pack
    for i in range(0, len(b), 5):
        chunk = b[i:i + 5]
        acc = 0
        try:
            for c in chunk:
                acc = acc * 85 + _b85dec[c]
        except TypeError:
            for j, c in enumerate(chunk):
                if _b85dec[c] is None:
                    raise ValueError('bad base85 character at position %d' % (i + j)) from None
            raise
        try:
            out.append(packI(acc))
        except struct.error:
            raise ValueError('base85 overflow in hunk starting at byte %d' % i) from None
    result = b''.join(out)
    if padding:
        result = result[:-padding]
    return result
_z85alphabet = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-:+=^!/*?&<>()[]{}@%$#'
_z85_b85_decode_diff = b';_`|~'
_z85_decode_translation = bytes.maketrans(_z85alphabet + _z85_b85_decode_diff, _b85alphabet + b'\x00' * len(_z85_b85_decode_diff))
_z85_encode_translation = bytes.maketrans(_b85alphabet, _z85alphabet)

def Z85编码(s):
    """Encode bytes-like object b in z85 format and return a bytes object."""
    return 基85编码(s).translate(_z85_encode_translation)

def Z85解码(s):
    """Decode the z85-encoded bytes-like object or ASCII string b

    The result is returned as a bytes object.
    """
    s = _bytes_from_decode_data(s)
    s = s.translate(_z85_decode_translation)
    try:
        return 基85解码(s)
    except ValueError as e:
        raise ValueError(e.args[0].replace('base85', 'z85')) from None
最大行宽 = 76
最大二进制块 = 最大行宽 // 4 * 3

def 编码(input, output):
    """Encode a file; input and output are binary files."""
    while (s := input.read(最大二进制块)):
        while len(s) < 最大二进制块 and (ns := input.read(最大二进制块 - len(s))):
            s += ns
        line = binascii.b2a_base64(s)
        output.write(line)

def 解码(input, output):
    """Decode a file; input and output are binary files."""
    while (line := input.readline()):
        s = binascii.a2b_base64(line)
        output.write(s)

def _input_type_check(s):
    try:
        m = memoryview(s)
    except TypeError as err:
        msg = 'expected bytes-like object, not %s' % s.__class__.__name__
        raise TypeError(msg) from err
    if m.format not in ('c', 'b', 'B'):
        msg = 'expected single byte elements, not %r from %s' % (m.format, s.__class__.__name__)
        raise TypeError(msg)
    if m.ndim != 1:
        msg = 'expected 1-D data, not %d-D data from %s' % (m.ndim, s.__class__.__name__)
        raise TypeError(msg)

def 编码字节串(s):
    """Encode a bytestring into a bytes object containing multiple lines
    of base-64 data."""
    _input_type_check(s)
    pieces = []
    for i in range(0, len(s), 最大二进制块):
        chunk = s[i:i + 最大二进制块]
        pieces.append(binascii.b2a_base64(chunk))
    return b''.join(pieces)

def 解码字节串(s):
    """Decode a bytestring of base-64 data into a bytes object."""
    _input_type_check(s)
    return binascii.a2b_base64(s)

def 主函数():
    """Small main program"""
    import sys, getopt
    usage = f'usage: {sys.argv[0]} [-h|-d|-e|-u] [file|-]\n        -h: print this help message and exit\n        -d, -u: decode\n        -e: encode (default)'
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hdeu')
    except getopt.error as msg:
        sys.stdout = sys.stderr
        print(msg)
        print(usage)
        sys.exit(2)
    func = 编码
    for o, a in opts:
        if o == '-e':
            func = 编码
        if o == '-d':
            func = 解码
        if o == '-u':
            func = 解码
        if o == '-h':
            print(usage)
            return
    if args and args[0] != '-':
        with open(args[0], 'rb') as f:
            func(f, sys.stdout.buffer)
    else:
        if sys.stdin.isatty():
            import io
            data = sys.stdin.buffer.read()
            buffer = io.BytesIO(data)
        else:
            buffer = sys.stdin.buffer
        func(buffer, sys.stdout.buffer)
if __name__ == '__main__':
    主函数()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'MAXBINSIZE': '最大二进制块',
    'MAXLINESIZE': '最大行宽',
    'a85decode': 'ASCII85解码',
    'a85encode': 'ASCII85编码',
    'b16decode': '基16解码',
    'b16encode': '基16编码',
    'b32decode': '基32解码',
    'b32encode': '基32编码',
    'b32hexdecode': '基32HEX解码',
    'b32hexencode': '基32HEX编码',
    'b64decode': '基64解码',
    'b64encode': '基64编码',
    'b85decode': '基85解码',
    'b85encode': '基85编码',
    'decode': '解码',
    'decodebytes': '解码字节串',
    'encode': '编码',
    'encodebytes': '编码字节串',
    'main': '主函数',
    'standard_b64decode': '标准基64解码',
    'standard_b64encode': '标准基64编码',
    'urlsafe_b64decode': '网址安全基64解码',
    'urlsafe_b64encode': '网址安全基64编码',
    'z85decode': 'Z85解码',
    'z85encode': 'Z85编码',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'ASCII85编码',
    'ASCII85解码',
    'Z85编码',
    'Z85解码',
    '基16编码',
    '基16解码',
    '基32HEX编码',
    '基32HEX解码',
    '基32编码',
    '基32解码',
    '基64编码',
    '基64解码',
    '基85编码',
    '基85解码',
    '标准基64编码',
    '标准基64解码',
    '编码',
    '编码字节串',
    '网址安全基64编码',
    '网址安全基64解码',
    '解码',
    '解码字节串',
])

# ---- 转发层结束 ----
