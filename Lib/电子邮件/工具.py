# -*- coding: utf-8 -*-
"""电子邮件.工具 —— 汉语库（由 tools/汉化库.py 从 Lib/email/utils.py 机械生成，**不要手改**）。

英文库 Lib/email.utils.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py email
"""


"""Miscellaneous utilities."""
_英文原名表 = {'collapse_rfc2231_value': '合并RFC2231值', 'decode_params': '解码参数', 'decode_rfc2231': '解码RFC2231', 'encode_rfc2231': '编码RFC2231', 'format_datetime': '格式化日期时间', 'formataddr': '格式化地址', 'formatdate': '格式化日期', 'getaddresses': '取地址表', 'localtime': '本地时间', 'make_msgid': '造消息ID', 'parseaddr': '解析地址', 'parsedate_to_datetime': '解析日期为日期时间', 'supports_strict_parsing': '支持严格解析', 'unquote': '去引号'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['collapse_rfc2231_value', 'decode_params', 'decode_rfc2231', 'encode_rfc2231', 'formataddr', 'formatdate', 'format_datetime', 'getaddresses', 'make_msgid', 'mktime_tz', 'parseaddr', 'parsedate', 'parsedate_tz', 'parsedate_to_datetime', 'unquote']
import os
import re
import time
import datetime
import urllib.parse
from 电子邮件._地址解析 import quote
from 电子邮件._地址解析 import AddressList as _AddressList
from 电子邮件._地址解析 import mktime_tz
from 电子邮件._地址解析 import parsedate, parsedate_tz, _parsedate_tz
COMMASPACE = ', '
EMPTYSTRING = ''
UEMPTYSTRING = ''
CRLF = '\r\n'
TICK = "'"
specialsre = re.compile('[][\\\\()<>@,:;".]')
escapesre = re.compile('[\\\\"]')

def _has_surrogates(s):
    """Return True if s may contain surrogate-escaped binary data."""
    try:
        s.encode()
        return False
    except UnicodeEncodeError:
        return True

def _sanitize(string):
    original_bytes = string.encode('utf-8', 'surrogateescape')
    return original_bytes.decode('utf-8', 'replace')

def 格式化地址(pair, charset='utf-8'):
    """The inverse of parseaddr(), this takes a 2-tuple of the form
    (realname, email_address) and returns the string value suitable
    for an RFC 2822 From, To or Cc header.

    If the first element of pair is false, then the second element is
    returned unmodified.

    The optional charset is the character set that is used to encode
    realname in case realname is not ASCII safe.  Can be an instance of str or
    a Charset-like object which has a header_encode method.  Default is
    'utf-8'.
    """
    name, address = pair
    address.encode('ascii')
    if name:
        try:
            name.encode('ascii')
        except UnicodeEncodeError:
            if isinstance(charset, str):
                from 电子邮件.字符集 import Charset
                charset = Charset(charset)
            encoded_name = charset.header_encode(name)
            return '%s <%s>' % (encoded_name, address)
        else:
            quotes = ''
            if specialsre.search(name):
                quotes = '"'
            name = escapesre.sub('\\\\\\g<0>', name)
            return '%s%s%s <%s>' % (quotes, name, quotes, address)
    return address

def _iter_escaped_chars(addr):
    pos = 0
    escape = False
    for pos, ch in enumerate(addr):
        if escape:
            yield (pos, '\\' + ch)
            escape = False
        elif ch == '\\':
            escape = True
        else:
            yield (pos, ch)
    if escape:
        yield (pos, '\\')

def _strip_quoted_realnames(addr):
    """Strip real names between quotes."""
    if '"' not in addr:
        return addr
    start = 0
    open_pos = None
    result = []
    for pos, ch in _iter_escaped_chars(addr):
        if ch == '"':
            if open_pos is None:
                open_pos = pos
            else:
                if start != open_pos:
                    result.append(addr[start:open_pos])
                start = pos + 1
                open_pos = None
    if start < len(addr):
        result.append(addr[start:])
    return ''.join(result)
支持严格解析 = True

def 取地址表(fieldvalues, *, strict=True):
    """Return a list of (REALNAME, EMAIL) or ('','') for each fieldvalue.

    When parsing fails for a fieldvalue, a 2-tuple of ('', '') is returned in
    its place.

    If strict is true, use a strict parser which rejects malformed inputs.
    """
    if not strict:
        all = COMMASPACE.join((str(v) for v in fieldvalues))
        a = _AddressList(all)
        return a.addresslist
    fieldvalues = [str(v) for v in fieldvalues]
    fieldvalues = _pre_parse_validation(fieldvalues)
    addr = COMMASPACE.join(fieldvalues)
    a = _AddressList(addr)
    result = _post_parse_validation(a.addresslist)
    n = 0
    for v in fieldvalues:
        v = _strip_quoted_realnames(v)
        n += 1 + v.count(',')
    if len(result) != n:
        return [('', '')]
    return result

def _check_parenthesis(addr):
    addr = _strip_quoted_realnames(addr)
    opens = 0
    for pos, ch in _iter_escaped_chars(addr):
        if ch == '(':
            opens += 1
        elif ch == ')':
            opens -= 1
            if opens < 0:
                return False
    return opens == 0

def _pre_parse_validation(email_header_fields):
    accepted_values = []
    for v in email_header_fields:
        if not _check_parenthesis(v):
            v = "('', '')"
        accepted_values.append(v)
    return accepted_values

def _post_parse_validation(parsed_email_header_tuples):
    accepted_values = []
    for v in parsed_email_header_tuples:
        if '[' in v[1]:
            v = ('', '')
        accepted_values.append(v)
    return accepted_values

def _format_timetuple_and_zone(timetuple, zone):
    return '%s, %02d %s %04d %02d:%02d:%02d %s' % (['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][timetuple[6]], timetuple[2], ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][timetuple[1] - 1], timetuple[0], timetuple[3], timetuple[4], timetuple[5], zone)

def 格式化日期(timeval=None, localtime=False, usegmt=False):
    """Returns a date string as specified by RFC 2822, e.g.:

    Fri, 09 Nov 2001 01:08:47 -0000

    Optional timeval if given is a floating-point time value as accepted by
    gmtime() and localtime(), otherwise the current time is used.

    Optional localtime is a flag that when True, interprets timeval, and
    returns a date relative to the local timezone instead of UTC, properly
    taking daylight savings time into account.

    Optional argument usegmt means that the timezone is written out as
    an ascii string, not numeric one (so "GMT" instead of "+0000"). This
    is needed for HTTP, and is only used when localtime==False.
    """
    if timeval is None:
        timeval = time.time()
    dt = datetime.datetime.fromtimestamp(timeval, datetime.timezone.utc)
    if localtime:
        dt = dt.astimezone()
        usegmt = False
    elif not usegmt:
        dt = dt.replace(tzinfo=None)
    return 格式化日期时间(dt, usegmt)

def 格式化日期时间(dt, usegmt=False):
    """Turn a datetime into a date string as specified in RFC 2822.

    If usegmt is True, dt must be an aware datetime with an offset of zero.  In
    this case 'GMT' will be rendered instead of the normal +0000 required by
    RFC2822.  This is to support HTTP headers involving date stamps.
    """
    now = dt.timetuple()
    if usegmt:
        if dt.tzinfo is None or dt.tzinfo != datetime.timezone.utc:
            raise ValueError('usegmt option requires a UTC datetime')
        zone = 'GMT'
    elif dt.tzinfo is None:
        zone = '-0000'
    else:
        zone = dt.strftime('%z')
    return _format_timetuple_and_zone(now, zone)

def 造消息ID(idstring=None, domain=None):
    """Returns a string suitable for RFC 2822 compliant Message-ID, e.g:

    <142480216486.20800.16526388040877946887@nightshade.la.mastaler.com>

    Optional idstring if given is a string used to strengthen the
    uniqueness of the message id.  Optional domain if given provides the
    portion of the message id after the '@'.  It defaults to the locally
    defined hostname.
    """
    import random
    import socket
    timeval = int(time.time() * 100)
    pid = os.getpid()
    randint = random.getrandbits(64)
    if idstring is None:
        idstring = ''
    else:
        idstring = '.' + idstring
    if domain is None:
        domain = socket.getfqdn()
    msgid = '<%d.%d.%d%s@%s>' % (timeval, pid, randint, idstring, domain)
    return msgid

def 解析日期为日期时间(data):
    parsed_date_tz = _parsedate_tz(data)
    if parsed_date_tz is None:
        raise ValueError('Invalid date value or format "%s"' % str(data))
    *dtuple, tz = parsed_date_tz
    try:
        if tz is None:
            return datetime.datetime(*dtuple[:6])
        return datetime.datetime(*dtuple[:6], tzinfo=datetime.timezone(datetime.timedelta(seconds=tz)))
    except OverflowError as exc:
        raise ValueError('Invalid date value or format "%s"' % str(data)) from exc

def 解析地址(addr, *, strict=True):
    """
    Parse addr into its constituent realname and email address parts.

    Return a tuple of realname and email address, unless the parse fails, in
    which case return a 2-tuple of ('', '').

    If strict is True, use a strict parser which rejects malformed inputs.
    """
    if not strict:
        addrs = _AddressList(addr).addresslist
        if not addrs:
            return ('', '')
        return addrs[0]
    if isinstance(addr, list):
        addr = addr[0]
    if not isinstance(addr, str):
        return ('', '')
    addr = _pre_parse_validation([addr])[0]
    addrs = _post_parse_validation(_AddressList(addr).addresslist)
    if not addrs or len(addrs) > 1:
        return ('', '')
    return addrs[0]

def 去引号(str):
    """Remove quotes from a string."""
    if len(str) > 1:
        if str.startswith('"') and str.endswith('"'):
            return str[1:-1].replace('\\\\', '\\').replace('\\"', '"')
        if str.startswith('<') and str.endswith('>'):
            return str[1:-1]
    return str

def 解码RFC2231(s):
    """Decode string according to RFC 2231"""
    parts = s.split(TICK, 2)
    if len(parts) <= 2:
        return (None, None, s)
    return parts

def 编码RFC2231(s, charset=None, language=None):
    """Encode string according to RFC 2231.

    If neither charset nor language is given, then s is returned as-is.  If
    charset is given but not language, the string is encoded using the empty
    string for language.
    """
    s = urllib.parse.quote(s, safe='', encoding=charset or 'ascii')
    if charset is None and language is None:
        return s
    if language is None:
        language = ''
    return "%s'%s'%s" % (charset, language, s)
rfc2231_continuation = re.compile('^(?P<name>\\w+)\\*((?P<num>[0-9]+)\\*?)?$', re.ASCII)

def 解码参数(params):
    """Decode parameters list according to RFC 2231.

    params is a sequence of 2-tuples containing (param name, string value).
    """
    new_params = [params[0]]
    rfc2231_params = {}
    for name, value in params[1:]:
        encoded = name.endswith('*')
        value = 去引号(value)
        mo = rfc2231_continuation.match(name)
        if mo:
            name, num = mo.group('name', 'num')
            if num is not None:
                num = int(num)
            rfc2231_params.setdefault(name, []).append((num, value, encoded))
        else:
            new_params.append((name, '"%s"' % quote(value)))
    if rfc2231_params:
        for name, continuations in rfc2231_params.items():
            value = []
            extended = False
            has_zero = any((x[0] == 0 for x in continuations))
            if has_zero:
                continuations = [x for x in continuations if x[0] is not None]
            else:
                continuations = [(x[0] or 0, x[1], x[2]) for x in continuations]
            continuations.sort(key=lambda x: x[0])
            for num, s, encoded in continuations:
                if encoded:
                    s = urllib.parse.unquote(s, encoding='latin-1')
                    extended = True
                value.append(s)
            value = quote(EMPTYSTRING.join(value))
            if extended:
                字符集, language, value = 解码RFC2231(value)
                new_params.append((name, (字符集, language, '"%s"' % value)))
            else:
                new_params.append((name, '"%s"' % value))
    return new_params

def 合并RFC2231值(value, errors='replace', fallback_charset='us-ascii'):
    if not isinstance(value, tuple) or len(value) != 3:
        return 去引号(value)
    字符集, language, text = value
    if 字符集 is None:
        字符集 = fallback_charset
    rawbytes = bytes(text, 'raw-unicode-escape')
    try:
        return str(rawbytes, 字符集, errors)
    except LookupError:
        return 去引号(text)

def 本地时间(dt=None):
    """Return local time as an aware datetime object.

    If called without arguments, return current time.  Otherwise *dt*
    argument should be a datetime instance, and it is converted to the
    local time zone according to the system time zone database.  If *dt* is
    naive (that is, dt.tzinfo is None), it is assumed to be in local time.

    """
    if dt is None:
        dt = datetime.datetime.now()
    return dt.astimezone()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'collapse_rfc2231_value': '合并RFC2231值',
    'decode_params': '解码参数',
    'decode_rfc2231': '解码RFC2231',
    'encode_rfc2231': '编码RFC2231',
    'format_datetime': '格式化日期时间',
    'formataddr': '格式化地址',
    'formatdate': '格式化日期',
    'getaddresses': '取地址表',
    'localtime': '本地时间',
    'make_msgid': '造消息ID',
    'parseaddr': '解析地址',
    'parsedate_to_datetime': '解析日期为日期时间',
    'supports_strict_parsing': '支持严格解析',
    'unquote': '去引号',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '去引号',
    '取地址表',
    '合并RFC2231值',
    '格式化地址',
    '格式化日期',
    '格式化日期时间',
    '编码RFC2231',
    '解析地址',
    '解析日期为日期时间',
    '解码RFC2231',
    '解码参数',
    '造消息ID',
]

# ---- 转发层结束 ----
