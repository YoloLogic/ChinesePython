# -*- coding: utf-8 -*-
"""URL工具.解析 —— 汉语库（由 tools/汉化库.py 从 Lib/urllib/parse.py 机械生成，**不要手改**）。

英文库 Lib/urllib.parse.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py urllib
"""


"""Parse (absolute and relative) URLs.

urllib.parse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL's by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zawinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urllib.parse module should conform with it.  The urllib.parse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.

The WHATWG URL Parser spec should also be considered.  We are not compliant with
it either due to existing user code API behavior expectations (Hyrum's Law).
It serves as a useful guide when making changes.
"""
_英文原名表 = {'DefragResult': '去片段结果', 'DefragResultBytes': '字节去片段结果', 'ParseResult': '解析结果', 'ParseResultBytes': '字节解析结果', 'SplitResult': '拆分结果', 'SplitResultBytes': '字节拆分结果', 'clear_cache': '清缓存', 'non_hierarchical': '非层级协议', 'parse_qs': '解析查询串', 'parse_qsl': '解析查询串成表', 'quote': '引用', 'quote_from_bytes': '字节引用', 'quote_plus': '引用加号', 'scheme_chars': '协议字符集', 'to_bytes': '转字节', 'unquote': '去引用', 'unquote_plus': '去引用加号', 'unquote_to_bytes': '去引用成字节', 'unwrap': '去包装', 'urldefrag': '去片段', 'urlencode': 'URL编码', 'urljoin': '拼接URL', 'urlparse': '解析URL', 'urlsplit': '拆分URL', 'urlunparse': '拼URL', 'urlunsplit': '拼回URL', 'uses_fragment': '支持片段', 'uses_netloc': '支持网络位置', 'uses_params': '支持参数', 'uses_relative': '支持相对地址'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from collections import namedtuple
import functools
import math
import re
import types
import warnings
import ipaddress
__all__ = ['urlparse', 'urlunparse', 'urljoin', 'urldefrag', 'urlsplit', 'urlunsplit', 'urlencode', 'parse_qs', 'parse_qsl', 'quote', 'quote_plus', 'quote_from_bytes', 'unquote', 'unquote_plus', 'unquote_to_bytes', 'DefragResult', 'ParseResult', 'SplitResult', 'DefragResultBytes', 'ParseResultBytes', 'SplitResultBytes']
支持相对地址 = ['', 'ftp', 'http', 'gopher', 'nntp', 'imap', 'wais', 'file', 'https', 'shttp', 'mms', 'prospero', 'rtsp', 'rtsps', 'rtspu', 'sftp', 'svn', 'svn+ssh', 'ws', 'wss']
支持网络位置 = ['', 'ftp', 'http', 'gopher', 'nntp', 'telnet', 'imap', 'wais', 'file', 'mms', 'https', 'shttp', 'snews', 'prospero', 'rtsp', 'rtsps', 'rtspu', 'rsync', 'svn', 'svn+ssh', 'sftp', 'nfs', 'git', 'git+ssh', 'ws', 'wss', 'itms-services']
支持参数 = ['', 'ftp', 'hdl', 'prospero', 'http', 'imap', 'https', 'shttp', 'rtsp', 'rtsps', 'rtspu', 'sip', 'sips', 'mms', 'sftp', 'tel']
非层级协议 = ['gopher', 'hdl', 'mailto', 'news', 'telnet', 'wais', 'imap', 'snews', 'sip', 'sips']
uses_query = ['', 'http', 'wais', 'imap', 'https', 'shttp', 'mms', 'gopher', 'rtsp', 'rtsps', 'rtspu', 'sip', 'sips']
支持片段 = ['', 'ftp', 'hdl', 'http', 'gopher', 'news', 'nntp', 'wais', 'https', 'shttp', 'snews', 'file', 'prospero']
协议字符集 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+-.'
_WHATWG_C0_CONTROL_OR_SPACE = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f '
_UNSAFE_URL_BYTES_TO_REMOVE = ['\t', '\r', '\n']

def 清缓存():
    """Clear internal performance caches. Undocumented; some tests want it."""
    拆分URL.cache_clear()
    _byte_quoter_factory.cache_clear()
_implicit_encoding = 'ascii'
_implicit_errors = 'strict'

def _noop(obj):
    return obj

def _encode_result(obj, encoding=_implicit_encoding, errors=_implicit_errors):
    return obj.encode(encoding, errors)

def _decode_args(args, encoding=_implicit_encoding, errors=_implicit_errors):
    return tuple((x.decode(encoding, errors) if x else '' for x in args))

def _coerce_args(*args):
    str_input = isinstance(args[0], str)
    for arg in args[1:]:
        if arg and isinstance(arg, str) != str_input:
            raise TypeError('Cannot mix str and non-str arguments')
    if str_input:
        return args + (_noop,)
    return _decode_args(args) + (_encode_result,)

class _ResultMixinStr(object):
    """Standard approach to encoding parsed results from str to bytes"""
    __slots__ = ()

    def encode(self, encoding='ascii', errors='strict'):
        return self._encoded_counterpart(*(x.encode(encoding, errors) for x in self))

class _ResultMixinBytes(object):
    """Standard approach to decoding parsed results from bytes to str"""
    __slots__ = ()

    def decode(self, encoding='ascii', errors='strict'):
        return self._decoded_counterpart(*(x.decode(encoding, errors) for x in self))

class _NetlocResultMixinBase(object):
    """Shared methods for the parsed result objects containing a netloc element"""
    __slots__ = ()

    @property
    def username(self):
        return self._userinfo[0]

    @property
    def password(self):
        return self._userinfo[1]

    @property
    def hostname(self):
        hostname = self._hostinfo[0]
        if not hostname:
            return None
        separator = '%' if isinstance(hostname, str) else b'%'
        hostname, percent, zone = hostname.partition(separator)
        return hostname.lower() + percent + zone

    @property
    def port(self):
        port = self._hostinfo[1]
        if port is not None:
            if port.isdigit() and port.isascii():
                port = int(port)
            else:
                raise ValueError(f'Port could not be cast to integer value as {port!r}')
            if not 0 <= port <= 65535:
                raise ValueError('Port out of range 0-65535')
        return port
    __class_getitem__ = classmethod(types.GenericAlias)

class _NetlocResultMixinStr(_NetlocResultMixinBase, _ResultMixinStr):
    __slots__ = ()

    @property
    def _userinfo(self):
        netloc = self.netloc
        userinfo, have_info, hostinfo = netloc.rpartition('@')
        if have_info:
            username, have_password, password = userinfo.partition(':')
            if not have_password:
                password = None
        else:
            username = password = None
        return (username, password)

    @property
    def _hostinfo(self):
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition('@')
        _, have_open_br, bracketed = hostinfo.partition('[')
        if have_open_br:
            hostname, _, port = bracketed.partition(']')
            _, _, port = port.partition(':')
        else:
            hostname, _, port = hostinfo.partition(':')
        if not port:
            port = None
        return (hostname, port)

class _NetlocResultMixinBytes(_NetlocResultMixinBase, _ResultMixinBytes):
    __slots__ = ()

    @property
    def _userinfo(self):
        netloc = self.netloc
        userinfo, have_info, hostinfo = netloc.rpartition(b'@')
        if have_info:
            username, have_password, password = userinfo.partition(b':')
            if not have_password:
                password = None
        else:
            username = password = None
        return (username, password)

    @property
    def _hostinfo(self):
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition(b'@')
        _, have_open_br, bracketed = hostinfo.partition(b'[')
        if have_open_br:
            hostname, _, port = bracketed.partition(b']')
            _, _, port = port.partition(b':')
        else:
            hostname, _, port = hostinfo.partition(b':')
        if not port:
            port = None
        return (hostname, port)
_DefragResultBase = namedtuple('_DefragResultBase', 'url fragment')
_SplitResultBase = namedtuple('_SplitResultBase', 'scheme netloc path query fragment')
_ParseResultBase = namedtuple('_ParseResultBase', 'scheme netloc path params query fragment')
_DefragResultBase.__doc__ = '\nDefragResult(url, fragment)\n\nA 2-tuple that contains the url without fragment identifier and the fragment\nidentifier as a separate argument.\n'
_DefragResultBase.url.__doc__ = 'The URL with no fragment identifier.'
_DefragResultBase.fragment.__doc__ = '\nFragment identifier separated from URL, that allows indirect identification of a\nsecondary resource by reference to a primary resource and additional identifying\ninformation.\n'
_SplitResultBase.__doc__ = '\nSplitResult(scheme, netloc, path, query, fragment)\n\nA 5-tuple that contains the different components of a URL. Similar to\nParseResult, but does not split params.\n'
_SplitResultBase.scheme.__doc__ = 'Specifies URL scheme for the request.'
_SplitResultBase.netloc.__doc__ = '\nNetwork location where the request is made to.\n'
_SplitResultBase.path.__doc__ = '\nThe hierarchical path, such as the path to a file to download.\n'
_SplitResultBase.query.__doc__ = "\nThe query component, that contains non-hierarchical data, that along with data\nin path component, identifies a resource in the scope of URI's scheme and\nnetwork location.\n"
_SplitResultBase.fragment.__doc__ = '\nFragment identifier, that allows indirect identification of a secondary resource\nby reference to a primary resource and additional identifying information.\n'
_ParseResultBase.__doc__ = '\nParseResult(scheme, netloc, path, params, query, fragment)\n\nA 6-tuple that contains components of a parsed URL.\n'
_ParseResultBase.scheme.__doc__ = _SplitResultBase.scheme.__doc__
_ParseResultBase.netloc.__doc__ = _SplitResultBase.netloc.__doc__
_ParseResultBase.path.__doc__ = _SplitResultBase.path.__doc__
_ParseResultBase.params.__doc__ = '\nParameters for last path element used to dereference the URI in order to provide\naccess to perform some operation on the resource.\n'
_ParseResultBase.query.__doc__ = _SplitResultBase.query.__doc__
_ParseResultBase.fragment.__doc__ = _SplitResultBase.fragment.__doc__
ResultBase = _NetlocResultMixinStr

class 去片段结果(_DefragResultBase, _ResultMixinStr):
    __slots__ = ()

    def geturl(self):
        if self.fragment:
            return self.url + '#' + self.fragment
        else:
            return self.url

class 拆分结果(_SplitResultBase, _NetlocResultMixinStr):
    __slots__ = ()

    def geturl(self):
        return 拼回URL(self)

class 解析结果(_ParseResultBase, _NetlocResultMixinStr):
    __slots__ = ()

    def geturl(self):
        return 拼URL(self)

class 字节去片段结果(_DefragResultBase, _ResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        if self.fragment:
            return self.url + b'#' + self.fragment
        else:
            return self.url

class 字节拆分结果(_SplitResultBase, _NetlocResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        return 拼回URL(self)

class 字节解析结果(_ParseResultBase, _NetlocResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        return 拼URL(self)

def _fix_result_transcoding():
    _result_pairs = ((去片段结果, 字节去片段结果), (拆分结果, 字节拆分结果), (解析结果, 字节解析结果))
    for _decoded, _encoded in _result_pairs:
        _decoded._encoded_counterpart = _encoded
        _encoded._decoded_counterpart = _decoded
_fix_result_transcoding()
del _fix_result_transcoding

def 解析URL(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

    The result is a named 6-tuple with fields corresponding to the
    above. It is either a ParseResult or ParseResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.

    urlsplit() should generally be used instead of urlparse().
    """
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    scheme, netloc, url, params, query, fragment = _urlparse(url, scheme, allow_fragments)
    result = 解析结果(scheme or '', netloc or '', url, params or '', query or '', fragment or '')
    return _coerce_result(result)

def _urlparse(url, scheme=None, allow_fragments=True):
    scheme, netloc, url, query, fragment = _urlsplit(url, scheme, allow_fragments)
    if (scheme or '') in 支持参数 and ';' in url:
        url, params = _splitparams(url, allow_none=True)
    else:
        params = None
    return (scheme, netloc, url, params, query, fragment)

def _splitparams(url, allow_none=False):
    if '/' in url:
        i = url.find(';', url.rfind('/'))
        if i < 0:
            return (url, None if allow_none else '')
    else:
        i = url.find(';')
    return (url[:i], url[i + 1:])

def _splitnetloc(url, start=0):
    delim = len(url)
    for c in '/?#':
        wdelim = url.find(c, start)
        if wdelim >= 0:
            delim = min(delim, wdelim)
    return (url[start:delim], url[delim:])

def _checknetloc(netloc):
    if not netloc or netloc.isascii():
        return
    import unicodedata
    n = netloc.replace('@', '')
    n = n.replace(':', '')
    n = n.replace('#', '')
    n = n.replace('?', '')
    netloc2 = unicodedata.normalize('NFKC', n)
    if n == netloc2:
        return
    for c in '/?#@:':
        if c in netloc2:
            raise ValueError("netloc '" + netloc + "' contains invalid " + 'characters under NFKC normalization')

def _check_bracketed_netloc(netloc):
    hostname_and_port = netloc.rpartition('@')[2]
    before_bracket, have_open_br, bracketed = hostname_and_port.partition('[')
    if have_open_br:
        if before_bracket:
            raise ValueError('Invalid IPv6 URL')
        hostname, _, port = bracketed.partition(']')
        if port and (not port.startswith(':')):
            raise ValueError('Invalid IPv6 URL')
    else:
        hostname, _, port = hostname_and_port.partition(':')
    _check_bracketed_host(hostname)

def _check_bracketed_host(hostname):
    if hostname.startswith(('v', 'V')):
        if not re.match('\\A[vV][a-fA-F0-9]+\\..+\\z', hostname):
            raise ValueError(f'IPvFuture address is invalid')
    else:
        ip = ipaddress.ip_address(hostname)
        if isinstance(ip, ipaddress.IPv4Address):
            raise ValueError(f'An IPv4 address cannot be in brackets')

@functools.lru_cache(typed=True)
def 拆分URL(url, scheme='', allow_fragments=True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>

    The result is a named 5-tuple with fields corresponding to the
    above. It is either a SplitResult or SplitResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.
    """
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    scheme, netloc, url, query, fragment = _urlsplit(url, scheme, allow_fragments)
    v = 拆分结果(scheme or '', netloc or '', url, query or '', fragment or '')
    return _coerce_result(v)

def _urlsplit(url, scheme=None, allow_fragments=True):
    url = url.lstrip(_WHATWG_C0_CONTROL_OR_SPACE)
    for b in _UNSAFE_URL_BYTES_TO_REMOVE:
        url = url.replace(b, '')
    if scheme is not None:
        scheme = scheme.strip(_WHATWG_C0_CONTROL_OR_SPACE)
        for b in _UNSAFE_URL_BYTES_TO_REMOVE:
            scheme = scheme.replace(b, '')
    allow_fragments = bool(allow_fragments)
    netloc = query = fragment = None
    i = url.find(':')
    if i > 0 and url[0].isascii() and url[0].isalpha():
        for c in url[:i]:
            if c not in 协议字符集:
                break
        else:
            scheme, url = (url[:i].lower(), url[i + 1:])
    if url[:2] == '//':
        netloc, url = _splitnetloc(url, 2)
        if '[' in netloc and ']' not in netloc or (']' in netloc and '[' not in netloc):
            raise ValueError('Invalid IPv6 URL')
        if '[' in netloc and ']' in netloc:
            _check_bracketed_netloc(netloc)
    if allow_fragments and '#' in url:
        url, fragment = url.split('#', 1)
    if '?' in url:
        url, query = url.split('?', 1)
    _checknetloc(netloc)
    return (scheme, netloc, url, query, fragment)

def 拼URL(components):
    """Put a parsed URL back together again.  This may result in a
    slightly different, but equivalent URL, if the URL that was parsed
    originally had redundant delimiters, e.g. a ? with an empty query
    (the draft states that these are equivalent)."""
    scheme, netloc, url, params, query, fragment, _coerce_result = _coerce_args(*components)
    if not netloc:
        if scheme and scheme in 支持网络位置 and (not url or url[:1] == '/'):
            netloc = ''
        else:
            netloc = None
    if params:
        url = '%s;%s' % (url, params)
    return _coerce_result(_urlunsplit(scheme or None, netloc, url, query or None, fragment or None))

def 拼回URL(components):
    """Combine the elements of a tuple as returned by urlsplit() into a
    complete URL as a string. The data argument can be any five-item iterable.
    This may result in a slightly different, but equivalent URL, if the URL that
    was parsed originally had unnecessary delimiters (for example, a ? with an
    empty query; the RFC states that these are equivalent)."""
    scheme, netloc, url, query, fragment, _coerce_result = _coerce_args(*components)
    if not netloc:
        if scheme and scheme in 支持网络位置 and (not url or url[:1] == '/'):
            netloc = ''
        else:
            netloc = None
    return _coerce_result(_urlunsplit(scheme or None, netloc, url, query or None, fragment or None))

def _urlunsplit(scheme, netloc, url, query, fragment):
    if netloc is not None:
        if url and url[:1] != '/':
            url = '/' + url
        url = '//' + netloc + url
    elif url[:2] == '//':
        url = '//' + url
    if scheme:
        url = scheme + ':' + url
    if query is not None:
        url = url + '?' + query
    if fragment is not None:
        url = url + '#' + fragment
    return url

def 拼接URL(base, url, allow_fragments=True):
    """Join a base URL and a possibly relative URL to form an absolute
    interpretation of the latter."""
    if not base:
        return url
    if not url:
        return base
    base, url, _coerce_result = _coerce_args(base, url)
    bscheme, bnetloc, bpath, bquery, bfragment = _urlsplit(base, None, allow_fragments)
    scheme, netloc, path, query, fragment = _urlsplit(url, None, allow_fragments)
    if scheme is None:
        scheme = bscheme
    if scheme != bscheme or (scheme and scheme not in 支持相对地址):
        return _coerce_result(url)
    if not scheme or scheme in 支持网络位置:
        if netloc:
            return _coerce_result(_urlunsplit(scheme, netloc, path, query, fragment))
        netloc = bnetloc
    if not path:
        path = bpath
        if query is None:
            query = bquery
            if fragment is None:
                fragment = bfragment
        return _coerce_result(_urlunsplit(scheme, netloc, path, query, fragment))
    base_parts = bpath.split('/')
    if base_parts[-1] != '':
        del base_parts[-1]
    if path[:1] == '/':
        segments = path.split('/')
    else:
        segments = base_parts + path.split('/')
        segments[1:-1] = filter(None, segments[1:-1])
    resolved_path = []
    for seg in segments:
        if seg == '..':
            try:
                resolved_path.pop()
            except IndexError:
                pass
        elif seg == '.':
            continue
        else:
            resolved_path.append(seg)
    if segments[-1] in ('.', '..'):
        resolved_path.append('')
    return _coerce_result(_urlunsplit(scheme, netloc, '/'.join(resolved_path) or '/', query, fragment))

def 去片段(url):
    """Removes any existing fragment from URL.

    Returns a tuple of the defragmented URL and the fragment.  If
    the URL contained no fragments, the second element is the
    empty string.
    """
    url, _coerce_result = _coerce_args(url)
    if '#' in url:
        s, n, p, q, frag = _urlsplit(url)
        defrag = _urlunsplit(s, n, p, q, None)
    else:
        frag = ''
        defrag = url
    return _coerce_result(去片段结果(defrag, frag or ''))
_hexdig = '0123456789ABCDEFabcdef'
_hextobyte = None

def 去引用成字节(string):
    """unquote_to_bytes('abc%20def') -> b'abc def'."""
    return bytes(_unquote_impl(string))

def _unquote_impl(string: bytes | bytearray | str) -> bytes | bytearray:
    if not string:
        string.split
        return b''
    if isinstance(string, str):
        string = string.encode('utf-8')
    bits = string.split(b'%')
    if len(bits) == 1:
        return string
    res = bytearray(bits[0])
    append = res.extend
    global _hextobyte
    if _hextobyte is None:
        _hextobyte = {(a + b).encode(): bytes.fromhex(a + b) for a in _hexdig for b in _hexdig}
    for item in bits[1:]:
        try:
            append(_hextobyte[item[:2]])
            append(item[2:])
        except KeyError:
            append(b'%')
            append(item)
    return res
_asciire = re.compile('([\x00-\x7f]+)')

def _generate_unquoted_parts(string, encoding, errors):
    previous_match_end = 0
    for ascii_match in _asciire.finditer(string):
        start, end = ascii_match.span()
        yield string[previous_match_end:start]
        yield _unquote_impl(ascii_match[1]).decode(encoding, errors)
        previous_match_end = end
    yield string[previous_match_end:]

def 去引用(string, encoding='utf-8', errors='replace'):
    """Replace %xx escapes by their single-character equivalent. The optional
    encoding and errors parameters specify how to decode percent-encoded
    sequences into Unicode characters, as accepted by the bytes.decode()
    method.
    By default, percent-encoded sequences are decoded with UTF-8, and invalid
    sequences are replaced by a placeholder character.

    unquote('abc%20def') -> 'abc def'.
    """
    if isinstance(string, bytes):
        return _unquote_impl(string).decode(encoding, errors)
    if '%' not in string:
        string.split
        return string
    if encoding is None:
        encoding = 'utf-8'
    if errors is None:
        errors = 'replace'
    return ''.join(_generate_unquoted_parts(string, encoding, errors))

def 解析查询串(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None, separator='&'):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError if there
            are more than n fields read by parse_qsl().

        separator: str. The symbol to use for separating the query arguments.
            Defaults to &.

        Returns a dictionary.
    """
    parsed_result = {}
    pairs = 解析查询串成表(qs, keep_blank_values, strict_parsing, encoding=encoding, errors=errors, max_num_fields=max_num_fields, separator=separator, _stacklevel=2)
    for name, value in pairs:
        if name in parsed_result:
            parsed_result[name].append(value)
        else:
            parsed_result[name] = [value]
    return parsed_result

def 解析查询串成表(qs, keep_blank_values=False, strict_parsing=False, encoding='utf-8', errors='replace', max_num_fields=None, separator='&', *, _stacklevel=1):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as blank
            strings.  The default false value indicates that blank values
            are to be ignored and treated as if they were  not included.

        strict_parsing: flag indicating what to do with parsing errors. If
            false (the default), errors are silently ignored. If true,
            errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError
            if there are more than n fields read by parse_qsl().

        separator: str. The symbol to use for separating the query arguments.
            Defaults to &.

        Returns a list, as G-d intended.
    """
    if not separator or not isinstance(separator, (str, bytes)):
        raise ValueError('Separator must be of type string or bytes.')
    if isinstance(qs, str):
        if not isinstance(separator, str):
            separator = str(separator, 'ascii')
        eq = '='

        def _unquote(s):
            return 去引用加号(s, encoding=encoding, errors=errors)
    elif qs is None:
        return []
    else:
        try:
            qs = bytes(memoryview(qs))
        except TypeError:
            if not qs:
                warnings.warn(f'Accepting {type(qs).__name__} objects with false value in urllib.parse.parse_qsl() is deprecated as of 3.14', DeprecationWarning, stacklevel=_stacklevel + 1)
                return []
            raise
        if isinstance(separator, str):
            separator = bytes(separator, 'ascii')
        eq = b'='

        def _unquote(s):
            return 去引用成字节(s.replace(b'+', b' '))
    if not qs:
        return []
    if max_num_fields is not None:
        num_fields = 1 + qs.count(separator)
        if max_num_fields < num_fields:
            raise ValueError('Max number of fields exceeded')
    r = []
    for name_value in qs.split(separator):
        if name_value or strict_parsing:
            name, has_eq, value = name_value.partition(eq)
            if not has_eq and strict_parsing:
                raise ValueError('bad query field: %r' % (name_value,))
            if value or keep_blank_values:
                name = _unquote(name)
                value = _unquote(value)
                r.append((name, value))
    return r

def 去引用加号(string, encoding='utf-8', errors='replace'):
    """Like unquote(), but also replace plus signs by spaces, as required for
    unquoting HTML form values.

    unquote_plus('%7e/abc+def') -> '~/abc def'
    """
    string = string.replace('+', ' ')
    return 去引用(string, encoding, errors)
_ALWAYS_SAFE = frozenset(b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-~')
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)

class _Quoter(dict):
    """A mapping from bytes numbers (in range(0,256)) to strings.

    String values are percent-encoded byte values, unless the key < 128, and
    in either of the specified safe set, or the always safe set.
    """

    def __init__(self, safe):
        """safe: bytes object."""
        self.safe = _ALWAYS_SAFE.union(safe)

    def __repr__(self):
        return f'<Quoter {dict(self)!r}>'

    def __missing__(self, b):
        res = chr(b) if b in self.safe else '%{:02X}'.format(b)
        self[b] = res
        return res

def 引用(string, safe='/', encoding=None, errors=None):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted. The
    quote function offers a cautious (not minimal) way to quote a
    string for most of these parts.

    RFC 3986 Uniform Resource Identifier (URI): Generic Syntax lists
    the following (un)reserved characters.

    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
    reserved      = gen-delims / sub-delims
    gen-delims    = ":" / "/" / "?" / "#" / "[" / "]" / "@"
    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
                  / "*" / "+" / "," / ";" / "="

    Each of the reserved characters is reserved in some component of a URL,
    but not necessarily in all of them.

    The quote function %-escapes all characters that are neither in the
    unreserved chars ("always safe") nor the additional chars set via the
    safe arg.

    The default for the safe arg is '/'. The character is reserved, but in
    typical usage the quote function is being called on a path where the
    existing slash characters are to be preserved.

    Python 3.7 updates from using RFC 2396 to RFC 3986 to quote URL strings.
    Now, "~" is included in the set of unreserved characters.

    string and safe may be either str or bytes objects. encoding and errors
    must not be specified if string is a bytes object.

    The optional encoding and errors parameters specify how to deal with
    non-ASCII characters, as accepted by the str.encode method.
    By default, encoding='utf-8' (characters are encoded with UTF-8), and
    errors='strict' (unsupported characters raise a UnicodeEncodeError).
    """
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = 'utf-8'
        if errors is None:
            errors = 'strict'
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return 字节引用(string, safe)

def 引用加号(string, safe='', encoding=None, errors=None):
    """Like quote(), but also replace ' ' with '+', as required for quoting
    HTML form values. Plus signs in the original string are escaped unless
    they are included in safe. It also does not have safe default to '/'.
    """
    if isinstance(string, str) and ' ' not in string or (isinstance(string, bytes) and b' ' not in string):
        return 引用(string, safe, encoding, errors)
    if isinstance(safe, str):
        space = ' '
    else:
        space = b' '
    string = 引用(string, safe + space, encoding, errors)
    return string.replace(' ', '+')

@functools.lru_cache
def _byte_quoter_factory(safe):
    return _Quoter(safe).__getitem__

def 字节引用(bs, safe='/'):
    """Like quote(), but accepts a bytes object rather than a str, and does
    not perform string-to-bytes encoding.  It always returns an ASCII string.
    quote_from_bytes(b'abc def?') -> 'abc%20def%3f'
    """
    if not isinstance(bs, (bytes, bytearray)):
        raise TypeError('quote_from_bytes() expected bytes')
    if not bs:
        return ''
    if isinstance(safe, str):
        safe = safe.encode('ascii', 'ignore')
    else:
        safe = bytes([c for c in safe if c < 128])
    if not bs.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bs.decode()
    quoter = _byte_quoter_factory(safe)
    if (bs_len := len(bs)) < 200000:
        return ''.join(map(quoter, bs))
    else:
        chunk_size = math.isqrt(bs_len)
        chunks = [''.join(map(quoter, bs[i:i + chunk_size])) for i in range(0, bs_len, chunk_size)]
        return ''.join(chunks)

def URL编码(query, doseq=False, safe='', encoding=None, errors=None, quote_via=引用加号):
    """Encode a dict or sequence of two-element tuples into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.

    The components of a query arg may each be either a string or a bytes type.

    The safe, encoding, and errors parameters are passed down to the function
    specified by quote_via (encoding and errors only if a component is a str).
    """
    if hasattr(query, 'items'):
        query = query.items()
    else:
        try:
            if len(query) and (not isinstance(query[0], tuple)):
                raise TypeError
        except TypeError as err:
            raise TypeError('not a valid non-string sequence or mapping object') from err
    l = []
    if not doseq:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)
            if isinstance(v, bytes):
                v = quote_via(v, safe)
            else:
                v = quote_via(str(v), safe, encoding, errors)
            l.append(k + '=' + v)
    else:
        for k, v in query:
            if isinstance(k, bytes):
                k = quote_via(k, safe)
            else:
                k = quote_via(str(k), safe, encoding, errors)
            if isinstance(v, bytes):
                v = quote_via(v, safe)
                l.append(k + '=' + v)
            elif isinstance(v, str):
                v = quote_via(v, safe, encoding, errors)
                l.append(k + '=' + v)
            else:
                try:
                    x = len(v)
                except TypeError:
                    v = quote_via(str(v), safe, encoding, errors)
                    l.append(k + '=' + v)
                else:
                    for elt in v:
                        if isinstance(elt, bytes):
                            elt = quote_via(elt, safe)
                        else:
                            elt = quote_via(str(elt), safe, encoding, errors)
                        l.append(k + '=' + elt)
    return '&'.join(l)

def 转字节(url):
    warnings.warn('urllib.parse.to_bytes() is deprecated as of 3.8', DeprecationWarning, stacklevel=2)
    return _to_bytes(url)

def _to_bytes(url):
    """to_bytes(u"URL") --> 'URL'."""
    if isinstance(url, str):
        try:
            url = url.encode('ASCII').decode()
        except UnicodeError:
            raise UnicodeError('URL ' + repr(url) + ' contains non-ASCII characters')
    return url

def 去包装(url):
    """Transform a string like '<URL:scheme://host/path>' into 'scheme://host/path'.

    The string is returned unchanged if it's not a wrapped URL.
    """
    url = str(url).strip()
    if url[:1] == '<' and url[-1:] == '>':
        url = url[1:-1].strip()
    if url[:4] == 'URL:':
        url = url[4:].strip()
    return url

def splittype(url):
    warnings.warn('urllib.parse.splittype() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splittype(url)
_typeprog = None

def _splittype(url):
    """splittype('type:opaquestring') --> 'type', 'opaquestring'."""
    global _typeprog
    if _typeprog is None:
        _typeprog = re.compile('([^/:]+):(.*)', re.DOTALL)
    match = _typeprog.match(url)
    if match:
        scheme, data = match.groups()
        return (scheme.lower(), data)
    return (None, url)

def splithost(url):
    warnings.warn('urllib.parse.splithost() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splithost(url)
_hostprog = None

def _splithost(url):
    """splithost('//host[:port]/path') --> 'host[:port]', '/path'."""
    global _hostprog
    if _hostprog is None:
        _hostprog = re.compile('//([^/#?]*)(.*)', re.DOTALL)
    match = _hostprog.match(url)
    if match:
        host_port, path = match.groups()
        if path and path[0] != '/':
            path = '/' + path
        return (host_port, path)
    return (None, url)

def splituser(host):
    warnings.warn('urllib.parse.splituser() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splituser(host)

def _splituser(host):
    """splituser('user[:passwd]@host[:port]') --> 'user[:passwd]', 'host[:port]'."""
    user, delim, host = host.rpartition('@')
    return (user if delim else None, host)

def splitpasswd(user):
    warnings.warn('urllib.parse.splitpasswd() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splitpasswd(user)

def _splitpasswd(user):
    """splitpasswd('user:passwd') -> 'user', 'passwd'."""
    user, delim, passwd = user.partition(':')
    return (user, passwd if delim else None)

def splitport(host):
    warnings.warn('urllib.parse.splitport() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splitport(host)
_portprog = None

def _splitport(host):
    """splitport('host:port') --> 'host', 'port'."""
    global _portprog
    if _portprog is None:
        _portprog = re.compile('(.*):([0-9]*)', re.DOTALL)
    match = _portprog.fullmatch(host)
    if match:
        host, port = match.groups()
        if port:
            return (host, port)
    return (host, None)

def splitnport(host, defport=-1):
    warnings.warn('urllib.parse.splitnport() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splitnport(host, defport)

def _splitnport(host, defport=-1):
    """Split host and port, returning numeric port.
    Return given default port if no ':' found; defaults to -1.
    Return numerical port if a valid number is found after ':'.
    Return None if ':' but not a valid number."""
    host, delim, port = host.rpartition(':')
    if not delim:
        host = port
    elif port:
        if port.isdigit() and port.isascii():
            nport = int(port)
        else:
            nport = None
        return (host, nport)
    return (host, defport)

def splitquery(url):
    warnings.warn('urllib.parse.splitquery() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splitquery(url)

def _splitquery(url):
    """splitquery('/path?query') --> '/path', 'query'."""
    path, delim, query = url.rpartition('?')
    if delim:
        return (path, query)
    return (url, None)

def splittag(url):
    warnings.warn('urllib.parse.splittag() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splittag(url)

def _splittag(url):
    """splittag('/path#tag') --> '/path', 'tag'."""
    path, delim, tag = url.rpartition('#')
    if delim:
        return (path, tag)
    return (url, None)

def splitattr(url):
    warnings.warn('urllib.parse.splitattr() is deprecated as of 3.8, use urllib.parse.urlparse() instead', DeprecationWarning, stacklevel=2)
    return _splitattr(url)

def _splitattr(url):
    """splitattr('/path;attr1=value1;attr2=value2;...') ->
        '/path', ['attr1=value1', 'attr2=value2', ...]."""
    words = url.split(';')
    return (words[0], words[1:])

def splitvalue(attr):
    warnings.warn('urllib.parse.splitvalue() is deprecated as of 3.8, use urllib.parse.parse_qsl() instead', DeprecationWarning, stacklevel=2)
    return _splitvalue(attr)

def _splitvalue(attr):
    """splitvalue('attr=value') --> 'attr', 'value'."""
    attr, delim, value = attr.partition('=')
    return (attr, value if delim else None)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'DefragResult': '去片段结果',
    'DefragResultBytes': '字节去片段结果',
    'ParseResult': '解析结果',
    'ParseResultBytes': '字节解析结果',
    'SplitResult': '拆分结果',
    'SplitResultBytes': '字节拆分结果',
    'clear_cache': '清缓存',
    'non_hierarchical': '非层级协议',
    'parse_qs': '解析查询串',
    'parse_qsl': '解析查询串成表',
    'quote': '引用',
    'quote_from_bytes': '字节引用',
    'quote_plus': '引用加号',
    'scheme_chars': '协议字符集',
    'to_bytes': '转字节',
    'unquote': '去引用',
    'unquote_plus': '去引用加号',
    'unquote_to_bytes': '去引用成字节',
    'unwrap': '去包装',
    'urldefrag': '去片段',
    'urlencode': 'URL编码',
    'urljoin': '拼接URL',
    'urlparse': '解析URL',
    'urlsplit': '拆分URL',
    'urlunparse': '拼URL',
    'urlunsplit': '拼回URL',
    'uses_fragment': '支持片段',
    'uses_netloc': '支持网络位置',
    'uses_params': '支持参数',
    'uses_relative': '支持相对地址',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'URL编码',
    '去引用',
    '去引用加号',
    '去引用成字节',
    '去片段',
    '去片段结果',
    '字节去片段结果',
    '字节引用',
    '字节拆分结果',
    '字节解析结果',
    '引用',
    '引用加号',
    '拆分URL',
    '拆分结果',
    '拼URL',
    '拼回URL',
    '拼接URL',
    '解析URL',
    '解析查询串',
    '解析查询串成表',
    '解析结果',
])

# ---- 转发层结束 ----
