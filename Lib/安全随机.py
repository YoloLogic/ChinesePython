# -*- coding: utf-8 -*-
"""安全随机 —— 汉语库（由 tools/汉化库.py 从 Lib/secrets.py 机械生成，**不要手改**）。

英文库 Lib/secrets.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 安全随机
"""


"""Generate cryptographically strong pseudo-random numbers suitable for
managing secrets such as account authentication, tokens, and similar.

See PEP 506 for more information.
https://peps.python.org/pep-0506/

"""
_英文原名表 = {'DEFAULT_ENTROPY': '默认熵', 'choice': '选择', 'randbelow': '取小于', 'randbits': '随机位', 'token_bytes': '取字节令牌', 'token_hex': '取十六进制令牌', 'token_urlsafe': '取网址安全令牌'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['choice', 'randbelow', 'randbits', 'SystemRandom', 'token_bytes', 'token_hex', 'token_urlsafe', 'compare_digest']
import base64
from hmac import compare_digest
from random import SystemRandom
_sysrand = SystemRandom()
随机位 = _sysrand.getrandbits
选择 = _sysrand.choice

def 取小于(exclusive_upper_bound):
    """Return a random int in the range [0, n)."""
    if exclusive_upper_bound <= 0:
        raise ValueError('Upper bound must be positive.')
    return _sysrand._randbelow(exclusive_upper_bound)
默认熵 = 32

def 取字节令牌(nbytes=None):
    """Return a random byte string containing *nbytes* bytes.

    If *nbytes* is ``None`` or not supplied, a reasonable
    default is used.

    >>> token_bytes(16)  #doctest:+SKIP
    b'\\xebr\\x17D*t\\xae\\xd4\\xe3S\\xb6\\xe2\\xebP1\\x8b'

    """
    if nbytes is None:
        nbytes = 默认熵
    return _sysrand.randbytes(nbytes)

def 取十六进制令牌(nbytes=None):
    """Return a random text string, in hexadecimal.

    The string has *nbytes* random bytes, each byte converted to two
    hex digits.  If *nbytes* is ``None`` or not supplied, a reasonable
    default is used.

    >>> token_hex(16)  #doctest:+SKIP
    'f9bf78b9a18ce6d46a0cd2b0b86df9da'

    """
    return 取字节令牌(nbytes).hex()

def 取网址安全令牌(nbytes=None):
    """Return a random URL-safe text string, in Base64 encoding.

    The string has *nbytes* random bytes.  If *nbytes* is ``None``
    or not supplied, a reasonable default is used.

    >>> token_urlsafe(16)  #doctest:+SKIP
    'Drmhze6EPcv0fN_81Bj-nA'

    """
    tok = 取字节令牌(nbytes)
    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'DEFAULT_ENTROPY': '默认熵',
    'choice': '选择',
    'randbelow': '取小于',
    'randbits': '随机位',
    'token_bytes': '取字节令牌',
    'token_hex': '取十六进制令牌',
    'token_urlsafe': '取网址安全令牌',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '取十六进制令牌',
    '取字节令牌',
    '取小于',
    '取网址安全令牌',
    '选择',
    '随机位',
]

# ---- 转发层结束 ----
