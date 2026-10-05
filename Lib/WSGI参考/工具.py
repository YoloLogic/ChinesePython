# -*- coding: utf-8 -*-
"""WSGI参考.工具 —— 汉语库（由 tools/汉化库.py 从 Lib/wsgiref/util.py 机械生成，**不要手改**）。

英文库 Lib/wsgiref.util.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py wsgiref
"""


"""Miscellaneous WSGI-related Utilities"""
_英文原名表 = {'FileWrapper': '文件包装器', 'application_uri': '应用URI', 'guess_scheme': '猜协议', 'is_hop_by_hop': '是逐跳头吗', 'request_uri': '请求URI', 'setup_testing_defaults': '设测试默认值', 'shift_path_info': '摘路径段'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import posixpath
__all__ = ['FileWrapper', 'guess_scheme', 'application_uri', 'request_uri', 'shift_path_info', 'setup_testing_defaults', 'is_hop_by_hop']

class 文件包装器:
    """Wrapper to convert file-like objects to iterables"""

    def __init__(self, filelike, blksize=8192):
        self.filelike = filelike
        self.blksize = blksize
        if hasattr(filelike, 'close'):
            self.close = filelike.close

    def __iter__(self):
        return self

    def __next__(self):
        data = self.filelike.read(self.blksize)
        if data:
            return data
        raise StopIteration

def 猜协议(environ):
    """Return a guess for whether 'wsgi.url_scheme' should be 'http' or 'https'
    """
    if environ.get('HTTPS') in ('yes', 'on', '1'):
        return 'https'
    else:
        return 'http'

def 应用URI(environ):
    """Return the application's base URI (no PATH_INFO or QUERY_STRING)"""
    url = environ['wsgi.url_scheme'] + '://'
    from urllib.parse import quote
    if environ.get('HTTP_HOST'):
        url += environ['HTTP_HOST']
    else:
        url += environ['SERVER_NAME']
        if environ['wsgi.url_scheme'] == 'https':
            if environ['SERVER_PORT'] != '443':
                url += ':' + environ['SERVER_PORT']
        elif environ['SERVER_PORT'] != '80':
            url += ':' + environ['SERVER_PORT']
    url += quote(environ.get('SCRIPT_NAME') or '/', encoding='latin1')
    return url

def 请求URI(environ, include_query=True):
    """Return the full request URI, optionally including the query string"""
    url = 应用URI(environ)
    from urllib.parse import quote
    path_info = quote(environ.get('PATH_INFO', ''), safe='/;=,', encoding='latin1')
    if not environ.get('SCRIPT_NAME'):
        url += path_info[1:]
    else:
        url += path_info
    if include_query and environ.get('QUERY_STRING'):
        url += '?' + environ['QUERY_STRING']
    return url

def 摘路径段(environ):
    """Shift a name from PATH_INFO to SCRIPT_NAME, returning it

    If there are no remaining path segments in PATH_INFO, return None.
    Note: 'environ' is modified in-place; use a copy if you need to keep
    the original PATH_INFO or SCRIPT_NAME.

    Note: when PATH_INFO is just a '/', this returns '' and appends a trailing
    '/' to SCRIPT_NAME, even though empty path segments are normally ignored,
    and SCRIPT_NAME doesn't normally end in a '/'.  This is intentional
    behavior, to ensure that an application can tell the difference between
    '/x' and '/x/' when traversing to objects.
    """
    path_info = environ.get('PATH_INFO', '')
    if not path_info:
        return None
    path_parts = path_info.split('/')
    path_parts[1:-1] = [p for p in path_parts[1:-1] if p and p != '.']
    name = path_parts[1]
    del path_parts[1]
    script_name = environ.get('SCRIPT_NAME', '')
    script_name = posixpath.normpath(script_name + '/' + name)
    if script_name.endswith('/'):
        script_name = script_name[:-1]
    if not name and (not script_name.endswith('/')):
        script_name += '/'
    environ['SCRIPT_NAME'] = script_name
    environ['PATH_INFO'] = '/'.join(path_parts)
    if name == '.':
        name = None
    return name

def 设测试默认值(environ):
    """Update 'environ' with trivial defaults for testing purposes

    This adds various parameters required for WSGI, including HTTP_HOST,
    SERVER_NAME, SERVER_PORT, REQUEST_METHOD, SCRIPT_NAME, PATH_INFO,
    and all of the wsgi.* variables.  It only supplies default values,
    and does not replace any existing settings for these variables.

    This routine is intended to make it easier for unit tests of WSGI
    servers and applications to set up dummy environments.  It should *not*
    be used by actual WSGI servers or applications, since the data is fake!
    """
    environ.setdefault('SERVER_NAME', '127.0.0.1')
    environ.setdefault('SERVER_PROTOCOL', 'HTTP/1.0')
    environ.setdefault('HTTP_HOST', environ['SERVER_NAME'])
    environ.setdefault('REQUEST_METHOD', 'GET')
    if 'SCRIPT_NAME' not in environ and 'PATH_INFO' not in environ:
        environ.setdefault('SCRIPT_NAME', '')
        environ.setdefault('PATH_INFO', '/')
    environ.setdefault('wsgi.version', (1, 0))
    environ.setdefault('wsgi.run_once', 0)
    environ.setdefault('wsgi.multithread', 0)
    environ.setdefault('wsgi.multiprocess', 0)
    from io import StringIO, BytesIO
    environ.setdefault('wsgi.input', BytesIO())
    environ.setdefault('wsgi.errors', StringIO())
    environ.setdefault('wsgi.url_scheme', 猜协议(environ))
    if environ['wsgi.url_scheme'] == 'http':
        environ.setdefault('SERVER_PORT', '80')
    elif environ['wsgi.url_scheme'] == 'https':
        environ.setdefault('SERVER_PORT', '443')
_hoppish = {'connection', 'keep-alive', 'proxy-authenticate', 'proxy-authorization', 'te', 'trailers', 'transfer-encoding', 'upgrade'}.__contains__

def 是逐跳头吗(header_name):
    """Return true if 'header_name' is an HTTP/1.1 "Hop-by-Hop" header"""
    return _hoppish(header_name.lower())


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'FileWrapper': '文件包装器',
    'application_uri': '应用URI',
    'guess_scheme': '猜协议',
    'is_hop_by_hop': '是逐跳头吗',
    'request_uri': '请求URI',
    'setup_testing_defaults': '设测试默认值',
    'shift_path_info': '摘路径段',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '应用URI',
    '摘路径段',
    '文件包装器',
    '是逐跳头吗',
    '猜协议',
    '设测试默认值',
    '请求URI',
]

# ---- 转发层结束 ----
