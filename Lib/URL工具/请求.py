# -*- coding: utf-8 -*-
"""URL工具.请求 —— 汉语库（由 tools/汉化库.py 从 Lib/urllib/request.py 机械生成，**不要手改**）。

英文库 Lib/urllib.request.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py urllib
"""


"""An extensible library for opening URLs using a variety of protocols

The simplest way to use this module is to call the urlopen function,
which accepts a string containing a URL or a Request object (described
below).  It opens the URL and returns the results as file-like
object; the returned object has some extra methods described below.

The OpenerDirector manages a collection of Handler objects that do
all the actual work.  Each Handler implements a particular protocol or
option.  The OpenerDirector is a composite object that invokes the
Handlers needed to open the requested URL.  For example, the
HTTPHandler performs HTTP GET and POST requests and deals with
non-error returns.  The HTTPRedirectHandler automatically deals with
HTTP 301, 302, 303, 307, and 308 redirect errors, and the
HTTPDigestAuthHandler deals with digest authentication.

urlopen(url, data=None) -- Basic usage is the same as original
urllib.  pass the url and optionally data to post to an HTTP URL, and
get a file-like object back.  One difference is that you can also pass
a Request instance instead of URL.  Raises a URLError (subclass of
OSError); for HTTP errors, raises an HTTPError, which can also be
treated as a valid response.

build_opener -- Function that creates a new OpenerDirector instance.
Will install the default handlers.  Accepts one or more Handlers as
arguments, either instances or Handler classes that it will
instantiate.  If one of the argument is a subclass of the default
handler, the argument will be installed instead of the default.

install_opener -- Installs a new opener as the default opener.

objects of interest:

OpenerDirector -- Sets up the User Agent as the Python-urllib client and manages
the Handler classes, while dealing with requests and responses.

Request -- An object that encapsulates the state of a request.  The
state can be as simple as the URL.  It can also include extra HTTP
headers, e.g. a User-Agent.

BaseHandler --

internals:
BaseHandler and parent
_call_chain conventions

Example usage:

import urllib.request

# set up authentication info
authinfo = urllib.request.HTTPBasicAuthHandler()
authinfo.add_password(realm='PDQ Application',
                      uri='https://mahler:8092/site-updates.py',
                      user='klem',
                      passwd='geheim$parole')

proxy_support = urllib.request.ProxyHandler({"http" : "http://ahad-haam:3128"})

# build a new opener that adds authentication and caching FTP handlers
opener = urllib.request.build_opener(proxy_support, authinfo,
                                     urllib.request.CacheFTPHandler)

# install it
urllib.request.install_opener(opener)

f = urllib.request.urlopen('https://www.python.org/')
"""
_英文原名表 = {'AbstractBasicAuthHandler': '基本认证处理基类', 'AbstractDigestAuthHandler': '摘要认证处理基类', 'AbstractHTTPHandler': 'HTTP处理器基类', 'BaseHandler': '处理器基类', 'CacheFTPHandler': '带缓存FTP处理器', 'ContentTooShortError': '内容过短错误', 'DataHandler': 'data协议处理器', 'FTPHandler': 'FTP处理器', 'FileHandler': '文件处理器', 'HTTPBasicAuthHandler': 'HTTP基本认证处理器', 'HTTPCookieProcessor': 'HTTP的Cookie处理器', 'HTTPDefaultErrorHandler': 'HTTP默认错误处理器', 'HTTPDigestAuthHandler': 'HTTP摘要认证处理器', 'HTTPErrorProcessor': 'HTTP错误处理器', 'HTTPHandler': 'HTTP处理器', 'HTTPPasswordMgr': 'HTTP口令管理', 'HTTPPasswordMgrWithDefaultRealm': 'HTTP口令管理带默认领域', 'HTTPPasswordMgrWithPriorAuth': 'HTTP口令管理带预认证', 'HTTPRedirectHandler': 'HTTP重定向处理器', 'HTTPSHandler': 'HTTPS处理器', 'OpenerDirector': '打开器', 'ProxyBasicAuthHandler': '代理基本认证处理器', 'ProxyDigestAuthHandler': '代理摘要认证处理器', 'ProxyHandler': '代理处理器', 'Request': '请求', 'UnknownHandler': '未知协议处理器', 'build_opener': '造打开器', 'getproxies': '取代理设置', 'getproxies_environment': '从环境取代理', 'install_opener': '装上打开器', 'parse_http_list': '解析HTTP列表', 'parse_keqv_list': '解析键值列表', 'pathname2url': '路径转URL', 'proxy_bypass': '代理绕过', 'proxy_bypass_environment': '环境代理绕过', 'url2pathname': 'URL转路径', 'urlcleanup': '清理URL临时文件', 'urlopen': '打开URL', 'urlretrieve': '取URL到文件'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import base64
import bisect
import contextlib
import email
import hashlib
import http.client
import io
import os
import re
import socket
import string
import sys
import time
import tempfile
from URL工具.错误 import URLError, HTTPError, 内容过短错误
from URL工具.解析 import urlparse, urlsplit, urljoin, unwrap, quote, unquote, _splittype, _splithost, _splitport, _splituser, _splitpasswd, _splitattr, _splitvalue, _splittag, unquote_to_bytes, urlunparse
from URL工具.响应 import addinfourl, addclosehook
try:
    import ssl
except ImportError:
    _have_ssl = False
else:
    _have_ssl = True
__all__ = ['Request', 'OpenerDirector', 'BaseHandler', 'HTTPDefaultErrorHandler', 'HTTPRedirectHandler', 'HTTPCookieProcessor', 'ProxyHandler', 'HTTPPasswordMgr', 'HTTPPasswordMgrWithDefaultRealm', 'HTTPPasswordMgrWithPriorAuth', 'AbstractBasicAuthHandler', 'HTTPBasicAuthHandler', 'ProxyBasicAuthHandler', 'AbstractDigestAuthHandler', 'HTTPDigestAuthHandler', 'ProxyDigestAuthHandler', 'HTTPHandler', 'FileHandler', 'FTPHandler', 'CacheFTPHandler', 'DataHandler', 'UnknownHandler', 'HTTPErrorProcessor', 'urlopen', 'install_opener', 'build_opener', 'pathname2url', 'url2pathname', 'getproxies', 'urlretrieve', 'urlcleanup']
__version__ = '%d.%d' % sys.version_info[:2]
_opener = None

def 打开URL(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *, context=None):
    """Open the URL url, which can be either a string or a Request object.

    *data* must be an object specifying additional data to be sent to
    the server, or None if no such data is needed.  See Request for
    details.

    urllib.request module uses HTTP/1.1 and includes a "Connection:close"
    header in its HTTP requests.

    The optional *timeout* parameter specifies a timeout in seconds for
    blocking operations like the connection attempt (if not specified, the
    global default timeout setting will be used). This only works for HTTP,
    HTTPS and FTP connections.

    If *context* is specified, it must be a ssl.SSLContext instance describing
    the various SSL options. See HTTPSConnection for more details.


    This function always returns an object which can work as a
    context manager and has the properties url, headers, and status.
    See urllib.response.addinfourl for more detail on these properties.

    For HTTP and HTTPS URLs, this function returns a http.client.HTTPResponse
    object slightly modified. In addition to the three new methods above, the
    msg attribute contains the same information as the reason attribute ---
    the reason phrase returned by the server --- instead of the response
    headers as it is specified in the documentation for HTTPResponse.

    For FTP, file, and data URLs, this function returns a
    urllib.response.addinfourl object.

    Note that None may be returned if no handler handles the request (though
    the default installed global OpenerDirector uses UnknownHandler to ensure
    this never happens).

    In addition, if proxy settings are detected (for example, when a *_proxy
    environment variable like http_proxy is set), ProxyHandler is default
    installed and makes sure the requests are handled through the proxy.

    """
    global _opener
    if context:
        https_handler = HTTPS处理器(context=context)
        opener = 造打开器(https_handler)
    elif _opener is None:
        _opener = opener = 造打开器()
    else:
        opener = _opener
    return opener.open(url, data, timeout)

def 装上打开器(opener):
    global _opener
    _opener = opener
_url_tempfiles = []

def 取URL到文件(url, filename=None, reporthook=None, data=None):
    """
    Retrieve a URL into a temporary location on disk.

    Requires a URL argument. If a filename is passed, it is used as
    the temporary file location. The reporthook argument should be
    a callable that accepts a block number, a read size, and the
    total file size of the URL target. The data argument should be
    valid URL encoded data.

    If a filename is passed and the URL points to a local resource,
    the result is a copy from local file to new file.

    Returns a tuple containing the path to the newly created
    data file as well as the resulting HTTPMessage object.
    """
    url_type, path = _splittype(url)
    with contextlib.closing(打开URL(url, data)) as fp:
        headers = fp.info()
        if url_type == 'file' and (not filename):
            return (os.path.normpath(path), headers)
        if filename:
            tfp = open(filename, 'wb')
        else:
            tfp = tempfile.NamedTemporaryFile(delete=False)
            filename = tfp.name
            _url_tempfiles.append(filename)
        with tfp:
            result = (filename, headers)
            bs = 1024 * 8
            size = -1
            read = 0
            blocknum = 0
            if 'content-length' in headers:
                size = int(headers['Content-Length'])
            if reporthook:
                reporthook(blocknum, bs, size)
            while (block := fp.read(bs)):
                read += len(block)
                tfp.write(block)
                blocknum += 1
                if reporthook:
                    reporthook(blocknum, bs, size)
    if size >= 0 and read < size:
        raise 内容过短错误('retrieval incomplete: got only %i out of %i bytes' % (read, size), result)
    return result

def 清理URL临时文件():
    """Clean up temporary files from urlretrieve calls."""
    for temp_file in _url_tempfiles:
        try:
            os.unlink(temp_file)
        except OSError:
            pass
    del _url_tempfiles[:]
    global _opener
    if _opener:
        _opener = None
_cut_port_re = re.compile(':\\d+$', re.ASCII)

def request_host(request):
    """Return request-host, as defined by RFC 2965.

    Variation from RFC: returned value is lowercased, for convenient
    comparison.

    """
    url = request.full_url
    host = urlparse(url)[1]
    if host == '':
        host = request.get_header('Host', '')
    host = _cut_port_re.sub('', host, 1)
    return host.lower()

class 请求:

    def __init__(self, url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None):
        self.full_url = url
        self.headers = {}
        self.unredirected_hdrs = {}
        self._data = None
        self.data = data
        self._tunnel_host = None
        for key, value in headers.items():
            self.add_header(key, value)
        if origin_req_host is None:
            origin_req_host = request_host(self)
        self.origin_req_host = origin_req_host
        self.unverifiable = unverifiable
        if method:
            self.method = method

    @property
    def full_url(self):
        if self.fragment:
            return '{}#{}'.format(self._full_url, self.fragment)
        return self._full_url

    @full_url.setter
    def full_url(self, url):
        self._full_url = unwrap(url)
        self._full_url, self.fragment = _splittag(self._full_url)
        self._parse()

    @full_url.deleter
    def full_url(self):
        self._full_url = None
        self.fragment = None
        self.selector = ''

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data != self._data:
            self._data = data
            if self.has_header('Content-length'):
                self.remove_header('Content-length')

    @data.deleter
    def data(self):
        self.data = None

    def _parse(self):
        self.type, rest = _splittype(self._full_url)
        if self.type is None:
            raise ValueError('unknown url type: %r' % self.full_url)
        self.host, self.selector = _splithost(rest)
        if self.host:
            self.host = unquote(self.host)

    def get_method(self):
        """Return a string indicating the HTTP request method."""
        default_method = 'POST' if self.data is not None else 'GET'
        return getattr(self, 'method', default_method)

    def get_full_url(self):
        return self.full_url

    def set_proxy(self, host, type):
        if self.type == 'https' and (not self._tunnel_host):
            self._tunnel_host = self.host
        else:
            self.type = type
            self.selector = self.full_url
        self.host = host

    def has_proxy(self):
        return self.selector == self.full_url

    def add_header(self, key, val):
        self.headers[key.capitalize()] = val

    def add_unredirected_header(self, key, val):
        self.unredirected_hdrs[key.capitalize()] = val

    def has_header(self, header_name):
        return header_name in self.headers or header_name in self.unredirected_hdrs

    def get_header(self, header_name, default=None):
        return self.headers.get(header_name, self.unredirected_hdrs.get(header_name, default))

    def remove_header(self, header_name):
        self.headers.pop(header_name, None)
        self.unredirected_hdrs.pop(header_name, None)

    def header_items(self):
        hdrs = {**self.unredirected_hdrs, **self.headers}
        return list(hdrs.items())

class 打开器:

    def __init__(self):
        client_version = 'Python-urllib/%s' % __version__
        self.addheaders = [('User-agent', client_version)]
        self.handlers = []
        self.handle_open = {}
        self.handle_error = {}
        self.process_response = {}
        self.process_request = {}

    def add_handler(self, handler):
        if not hasattr(handler, 'add_parent'):
            raise TypeError('expected BaseHandler instance, got %r' % type(handler))
        added = False
        for meth in dir(handler):
            if meth in ['redirect_request', 'do_open', 'proxy_open']:
                continue
            i = meth.find('_')
            protocol = meth[:i]
            condition = meth[i + 1:]
            if condition.startswith('error'):
                j = condition.find('_') + i + 1
                kind = meth[j + 1:]
                try:
                    kind = int(kind)
                except ValueError:
                    pass
                lookup = self.handle_error.get(protocol, {})
                self.handle_error[protocol] = lookup
            elif condition == 'open':
                kind = protocol
                lookup = self.handle_open
            elif condition == 'response':
                kind = protocol
                lookup = self.process_response
            elif condition == 'request':
                kind = protocol
                lookup = self.process_request
            else:
                continue
            handlers = lookup.setdefault(kind, [])
            if handlers:
                bisect.insort(handlers, handler)
            else:
                handlers.append(handler)
            added = True
        if added:
            bisect.insort(self.handlers, handler)
            handler.add_parent(self)

    def close(self):
        pass

    def _call_chain(self, chain, kind, meth_name, *args):
        handlers = chain.get(kind, ())
        for handler in handlers:
            func = getattr(handler, meth_name)
            result = func(*args)
            if result is not None:
                return result

    def open(self, fullurl, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        if isinstance(fullurl, str):
            req = 请求(fullurl, data)
        else:
            req = fullurl
            if data is not None:
                req.data = data
        req.timeout = timeout
        protocol = req.type
        meth_name = protocol + '_request'
        for processor in self.process_request.get(protocol, []):
            meth = getattr(processor, meth_name)
            req = meth(req)
        sys.audit('urllib.Request', req.full_url, req.data, req.headers, req.get_method())
        响应 = self._open(req, data)
        meth_name = protocol + '_response'
        for processor in self.process_response.get(protocol, []):
            meth = getattr(processor, meth_name)
            响应 = meth(req, 响应)
        return 响应

    def _open(self, req, data=None):
        result = self._call_chain(self.handle_open, 'default', 'default_open', req)
        if result:
            return result
        protocol = req.type
        result = self._call_chain(self.handle_open, protocol, protocol + '_open', req)
        if result:
            return result
        return self._call_chain(self.handle_open, 'unknown', 'unknown_open', req)

    def error(self, proto, *args):
        if proto in ('http', 'https'):
            dict = self.handle_error['http']
            proto = args[2]
            meth_name = 'http_error_%s' % proto
            http_err = 1
            orig_args = args
        else:
            dict = self.handle_error
            meth_name = proto + '_error'
            http_err = 0
        args = (dict, proto, meth_name) + args
        result = self._call_chain(*args)
        if result:
            return result
        if http_err:
            args = (dict, 'default', 'http_error_default') + orig_args
            return self._call_chain(*args)

def 造打开器(*handlers):
    """Create an opener object from a list of handlers.

    The opener will use several default handlers, including support
    for HTTP, FTP and when applicable HTTPS.

    If any of the handlers passed as arguments are subclasses of the
    default handlers, the default handlers will not be used.
    """
    opener = 打开器()
    default_classes = [代理处理器, 未知协议处理器, HTTP处理器, HTTP默认错误处理器, HTTP重定向处理器, FTP处理器, 文件处理器, HTTP错误处理器, data协议处理器]
    if hasattr(http.client, 'HTTPSConnection'):
        default_classes.append(HTTPS处理器)
    skip = set()
    for klass in default_classes:
        for check in handlers:
            if isinstance(check, type):
                if issubclass(check, klass):
                    skip.add(klass)
            elif isinstance(check, klass):
                skip.add(klass)
    for klass in skip:
        default_classes.remove(klass)
    for klass in default_classes:
        opener.add_handler(klass())
    for h in handlers:
        if isinstance(h, type):
            h = h()
        opener.add_handler(h)
    return opener

class 处理器基类:
    handler_order = 500

    def add_parent(self, parent):
        self.parent = parent

    def close(self):
        pass

    def __lt__(self, other):
        if not hasattr(other, 'handler_order'):
            return True
        return self.handler_order < other.handler_order

class HTTP错误处理器(处理器基类):
    """Process HTTP error responses."""
    handler_order = 1000

    def http_response(self, request, response):
        code, msg, hdrs = (response.code, response.msg, response.info())
        if not 200 <= code < 300:
            response = self.parent.error('http', request, response, code, msg, hdrs)
        return response
    https_response = http_response

class HTTP默认错误处理器(处理器基类):

    def http_error_default(self, req, fp, code, msg, hdrs):
        raise HTTPError(req.full_url, code, msg, hdrs, fp)

class HTTP重定向处理器(处理器基类):
    max_repeats = 4
    max_redirections = 10

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Return a Request or None in response to a redirect.

        This is called by the http_error_30x methods when a
        redirection response is received.  If a redirection should
        take place, return a new Request to allow http_error_30x to
        perform the redirect.  Otherwise, raise HTTPError if no-one
        else should try to handle this url.  Return None if you can't
        but another Handler might.
        """
        m = req.get_method()
        if not (code in (301, 302, 303, 307, 308) and m in ('GET', 'HEAD') or (code in (301, 302, 303) and m == 'POST')):
            raise HTTPError(req.full_url, code, msg, headers, fp)
        newurl = newurl.replace(' ', '%20')
        CONTENT_HEADERS = ('content-length', 'content-type')
        newheaders = {k: v for k, v in req.headers.items() if k.lower() not in CONTENT_HEADERS}
        return 请求(newurl, method='HEAD' if m == 'HEAD' else 'GET', headers=newheaders, origin_req_host=req.origin_req_host, unverifiable=True)

    def http_error_302(self, req, fp, code, msg, headers):
        if 'location' in headers:
            newurl = headers['location']
        elif 'uri' in headers:
            newurl = headers['uri']
        else:
            return
        urlparts = urlparse(newurl)
        if urlparts.scheme not in ('http', 'https', 'ftp', ''):
            raise HTTPError(newurl, code, "%s - Redirection to url '%s' is not allowed" % (msg, newurl), headers, fp)
        if not urlparts.path and urlparts.netloc:
            urlparts = list(urlparts)
            urlparts[2] = '/'
        newurl = urlunparse(urlparts)
        newurl = quote(newurl, encoding='iso-8859-1', safe=string.punctuation)
        newurl = urljoin(req.full_url, newurl)
        new = self.redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return
        if hasattr(req, 'redirect_dict'):
            visited = new.redirect_dict = req.redirect_dict
            if visited.get(newurl, 0) >= self.max_repeats or len(visited) >= self.max_redirections:
                raise HTTPError(req.full_url, code, self.inf_msg + msg, headers, fp)
        else:
            visited = new.redirect_dict = req.redirect_dict = {}
        visited[newurl] = visited.get(newurl, 0) + 1
        fp.read()
        fp.close()
        return self.parent.open(new, timeout=req.timeout)
    http_error_301 = http_error_303 = http_error_307 = http_error_308 = http_error_302
    inf_msg = 'The HTTP server returned a redirect error that would lead to an infinite loop.\nThe last 30x error message was:\n'

def _parse_proxy(proxy):
    """Return (scheme, user, password, host/port) given a URL or an authority.

    If a URL is supplied, it must have an authority (host:port) component.
    According to RFC 3986, having an authority component means the URL must
    have two slashes after the scheme.
    """
    scheme, r_scheme = _splittype(proxy)
    if not r_scheme.startswith('/'):
        scheme = None
        authority = proxy
    else:
        if not r_scheme.startswith('//'):
            raise ValueError('proxy URL with no authority: %r' % proxy)
        if '@' in r_scheme:
            host_separator = r_scheme.find('@')
            end = r_scheme.find('/', host_separator)
        else:
            end = r_scheme.find('/', 2)
        if end == -1:
            end = None
        authority = r_scheme[2:end]
    userinfo, hostport = _splituser(authority)
    if userinfo is not None:
        user, password = _splitpasswd(userinfo)
    else:
        user = password = None
    return (scheme, user, password, hostport)

class 代理处理器(处理器基类):
    handler_order = 100

    def __init__(self, proxies=None):
        if proxies is None:
            proxies = 取代理设置()
        assert hasattr(proxies, 'keys'), 'proxies must be a mapping'
        self.proxies = proxies
        for type, url in proxies.items():
            type = type.lower()
            setattr(self, '%s_open' % type, lambda r, proxy=url, type=type, meth=self.proxy_open: meth(r, proxy, type))

    def proxy_open(self, req, proxy, type):
        orig_type = req.type
        proxy_type, user, password, hostport = _parse_proxy(proxy)
        if proxy_type is None:
            proxy_type = orig_type
        if req.host and 代理绕过(req.host):
            return None
        if user and password:
            user_pass = '%s:%s' % (unquote(user), unquote(password))
            creds = base64.b64encode(user_pass.encode()).decode('ascii')
            req.add_header('Proxy-authorization', 'Basic ' + creds)
        hostport = unquote(hostport)
        req.set_proxy(hostport, proxy_type)
        if orig_type == proxy_type or orig_type == 'https':
            return None
        else:
            return self.parent.open(req, timeout=req.timeout)

class HTTP口令管理:

    def __init__(self):
        self.passwd = {}

    def add_password(self, realm, uri, user, passwd):
        if isinstance(uri, str):
            uri = [uri]
        if realm not in self.passwd:
            self.passwd[realm] = {}
        for default_port in (True, False):
            reduced_uri = tuple((self.reduce_uri(u, default_port) for u in uri))
            self.passwd[realm][reduced_uri] = (user, passwd)

    def find_user_password(self, realm, authuri):
        domains = self.passwd.get(realm, {})
        for default_port in (True, False):
            reduced_authuri = self.reduce_uri(authuri, default_port)
            for uris, authinfo in domains.items():
                for uri in uris:
                    if self.is_suburi(uri, reduced_authuri):
                        return authinfo
        return (None, None)

    def reduce_uri(self, uri, default_port=True):
        """Accept authority or URI and extract only the authority and path."""
        parts = urlsplit(uri)
        if parts[1]:
            scheme = parts[0]
            authority = parts[1]
            path = parts[2] or '/'
        else:
            scheme = None
            authority = uri
            path = '/'
        host, port = _splitport(authority)
        if default_port and port is None and (scheme is not None):
            dport = {'http': 80, 'https': 443}.get(scheme)
            if dport is not None:
                authority = '%s:%d' % (host, dport)
        return (authority, path)

    def is_suburi(self, base, test):
        """Check if test is below base in a URI tree

        Both args must be URIs in reduced form.
        """
        if base == test:
            return True
        if base[0] != test[0]:
            return False
        prefix = base[1]
        if prefix[-1:] != '/':
            prefix += '/'
        return test[1].startswith(prefix)

class HTTP口令管理带默认领域(HTTP口令管理):

    def find_user_password(self, realm, authuri):
        user, password = HTTP口令管理.find_user_password(self, realm, authuri)
        if user is not None:
            return (user, password)
        return HTTP口令管理.find_user_password(self, None, authuri)

class HTTP口令管理带预认证(HTTP口令管理带默认领域):

    def __init__(self):
        self.authenticated = {}
        super().__init__()

    def add_password(self, realm, uri, user, passwd, is_authenticated=False):
        self.update_authenticated(uri, is_authenticated)
        if realm is not None:
            super().add_password(None, uri, user, passwd)
        super().add_password(realm, uri, user, passwd)

    def update_authenticated(self, uri, is_authenticated=False):
        if isinstance(uri, str):
            uri = [uri]
        for default_port in (True, False):
            for u in uri:
                reduced_uri = self.reduce_uri(u, default_port)
                self.authenticated[reduced_uri] = is_authenticated

    def is_authenticated(self, authuri):
        for default_port in (True, False):
            reduced_authuri = self.reduce_uri(authuri, default_port)
            for uri in self.authenticated:
                if self.is_suburi(uri, reduced_authuri):
                    return self.authenticated[uri]

class 基本认证处理基类:
    rx = re.compile('(?:^|,)[ \t]*([^ \t,]+)[ \t]+realm=(["\']?)([^"\']*)\\2', re.I)

    def __init__(self, password_mgr=None):
        if password_mgr is None:
            password_mgr = HTTP口令管理()
        self.passwd = password_mgr
        self.add_password = self.passwd.add_password

    def _parse_realm(self, header):
        found_challenge = False
        for mo in 基本认证处理基类.rx.finditer(header):
            scheme, quote, realm = mo.groups()
            if quote not in ['"', "'"]:
                import warnings
                warnings.warn('Basic Auth Realm was unquoted', UserWarning, 3)
            yield (scheme, realm)
            found_challenge = True
        if not found_challenge:
            if header:
                scheme = header.split()[0]
            else:
                scheme = ''
            yield (scheme, None)

    def http_error_auth_reqed(self, authreq, host, req, headers):
        headers = headers.get_all(authreq)
        if not headers:
            return
        unsupported = None
        for header in headers:
            for scheme, realm in self._parse_realm(header):
                if scheme.lower() != 'basic':
                    unsupported = scheme
                    continue
                if realm is not None:
                    return self.retry_http_basic_auth(host, req, realm)
        if unsupported is not None:
            raise ValueError('AbstractBasicAuthHandler does not support the following scheme: %r' % (scheme,))

    def retry_http_basic_auth(self, host, req, realm):
        user, pw = self.passwd.find_user_password(realm, host)
        if pw is not None:
            raw = '%s:%s' % (user, pw)
            auth = 'Basic ' + base64.b64encode(raw.encode()).decode('ascii')
            if req.get_header(self.auth_header, None) == auth:
                return None
            req.add_unredirected_header(self.auth_header, auth)
            return self.parent.open(req, timeout=req.timeout)
        else:
            return None

    def http_request(self, req):
        if not hasattr(self.passwd, 'is_authenticated') or not self.passwd.is_authenticated(req.full_url):
            return req
        if not req.has_header('Authorization'):
            user, passwd = self.passwd.find_user_password(None, req.full_url)
            credentials = '{0}:{1}'.format(user, passwd).encode()
            auth_str = base64.standard_b64encode(credentials).decode()
            req.add_unredirected_header('Authorization', 'Basic {}'.format(auth_str.strip()))
        return req

    def http_response(self, req, response):
        if hasattr(self.passwd, 'is_authenticated'):
            if 200 <= response.code < 300:
                self.passwd.update_authenticated(req.full_url, True)
            else:
                self.passwd.update_authenticated(req.full_url, False)
        return response
    https_request = http_request
    https_response = http_response

class HTTP基本认证处理器(基本认证处理基类, 处理器基类):
    auth_header = 'Authorization'

    def http_error_401(self, req, fp, code, msg, headers):
        url = req.full_url
        响应 = self.http_error_auth_reqed('www-authenticate', url, req, headers)
        return 响应

class 代理基本认证处理器(基本认证处理基类, 处理器基类):
    auth_header = 'Proxy-authorization'

    def http_error_407(self, req, fp, code, msg, headers):
        authority = req.host
        响应 = self.http_error_auth_reqed('proxy-authenticate', authority, req, headers)
        return 响应
_randombytes = os.urandom

class 摘要认证处理基类:

    def __init__(self, passwd=None):
        if passwd is None:
            passwd = HTTP口令管理()
        self.passwd = passwd
        self.add_password = self.passwd.add_password
        self.retried = 0
        self.nonce_count = 0
        self.last_nonce = None

    def reset_retry_count(self):
        self.retried = 0

    def http_error_auth_reqed(self, auth_header, host, req, headers):
        authreq = headers.get(auth_header, None)
        if self.retried > 5:
            raise HTTPError(req.full_url, 401, 'digest auth failed', headers, None)
        else:
            self.retried += 1
        if authreq:
            scheme = authreq.split()[0]
            if scheme.lower() == 'digest':
                return self.retry_http_digest_auth(req, authreq)
            elif scheme.lower() != 'basic':
                raise ValueError("AbstractDigestAuthHandler does not support the following scheme: '%s'" % scheme)

    def retry_http_digest_auth(self, req, auth):
        token, challenge = auth.split(' ', 1)
        chal = 解析键值列表(filter(None, 解析HTTP列表(challenge)))
        auth = self.get_authorization(req, chal)
        if auth:
            auth_val = 'Digest %s' % auth
            if req.headers.get(self.auth_header, None) == auth_val:
                return None
            req.add_unredirected_header(self.auth_header, auth_val)
            resp = self.parent.open(req, timeout=req.timeout)
            return resp

    def get_cnonce(self, nonce):
        s = '%s:%s:%s:' % (self.nonce_count, nonce, time.ctime())
        b = s.encode('ascii') + _randombytes(8)
        dig = hashlib.sha1(b).hexdigest()
        return dig[:16]

    def get_authorization(self, req, chal):
        try:
            realm = chal['realm']
            nonce = chal['nonce']
            qop = chal.get('qop')
            algorithm = chal.get('algorithm', 'MD5')
            opaque = chal.get('opaque', None)
        except KeyError:
            return None
        H, KD = self.get_algorithm_impls(algorithm)
        if H is None:
            return None
        user, pw = self.passwd.find_user_password(realm, req.full_url)
        if user is None:
            return None
        if req.data is not None:
            entdig = self.get_entity_digest(req.data, chal)
        else:
            entdig = None
        A1 = '%s:%s:%s' % (user, realm, pw)
        A2 = '%s:%s' % (req.get_method(), req.selector)
        if qop is None:
            respdig = KD(H(A1), '%s:%s' % (nonce, H(A2)))
        elif 'auth' in qop.split(','):
            if nonce == self.last_nonce:
                self.nonce_count += 1
            else:
                self.nonce_count = 1
                self.last_nonce = nonce
            ncvalue = '%08x' % self.nonce_count
            cnonce = self.get_cnonce(nonce)
            noncebit = '%s:%s:%s:%s:%s' % (nonce, ncvalue, cnonce, 'auth', H(A2))
            respdig = KD(H(A1), noncebit)
        else:
            raise URLError("qop '%s' is not supported." % qop)
        base = 'username="%s", realm="%s", nonce="%s", uri="%s", response="%s"' % (user, realm, nonce, req.selector, respdig)
        if opaque:
            base += ', opaque="%s"' % opaque
        if entdig:
            base += ', digest="%s"' % entdig
        base += ', algorithm="%s"' % algorithm
        if qop:
            base += ', qop=auth, nc=%s, cnonce="%s"' % (ncvalue, cnonce)
        return base

    def get_algorithm_impls(self, algorithm):
        if algorithm == 'MD5':
            H = lambda x: hashlib.md5(x.encode('ascii')).hexdigest()
        elif algorithm == 'SHA':
            H = lambda x: hashlib.sha1(x.encode('ascii')).hexdigest()
        elif algorithm == 'SHA-256':
            H = lambda x: hashlib.sha256(x.encode('ascii')).hexdigest()
        else:
            raise ValueError('Unsupported digest authentication algorithm %r' % algorithm)
        KD = lambda s, d: H('%s:%s' % (s, d))
        return (H, KD)

    def get_entity_digest(self, data, chal):
        return None

class HTTP摘要认证处理器(处理器基类, 摘要认证处理基类):
    """An authentication protocol defined by RFC 2069

    Digest authentication improves on basic authentication because it
    does not transmit passwords in the clear.
    """
    auth_header = 'Authorization'
    handler_order = 490

    def http_error_401(self, req, fp, code, msg, headers):
        host = urlparse(req.full_url)[1]
        retry = self.http_error_auth_reqed('www-authenticate', host, req, headers)
        self.reset_retry_count()
        return retry

class 代理摘要认证处理器(处理器基类, 摘要认证处理基类):
    auth_header = 'Proxy-Authorization'
    handler_order = 490

    def http_error_407(self, req, fp, code, msg, headers):
        host = req.host
        retry = self.http_error_auth_reqed('proxy-authenticate', host, req, headers)
        self.reset_retry_count()
        return retry

class HTTP处理器基类(处理器基类):

    def __init__(self, debuglevel=None):
        self._debuglevel = debuglevel if debuglevel is not None else http.client.HTTPConnection.debuglevel

    def set_http_debuglevel(self, level):
        self._debuglevel = level

    def _get_content_length(self, request):
        return http.client.HTTPConnection._get_content_length(request.data, request.get_method())

    def do_request_(self, request):
        host = request.host
        if not host:
            raise URLError('no host given')
        if request.data is not None:
            data = request.data
            if isinstance(data, str):
                msg = 'POST data should be bytes, an iterable of bytes, or a file object. It cannot be of type str.'
                raise TypeError(msg)
            if not request.has_header('Content-type'):
                request.add_unredirected_header('Content-type', 'application/x-www-form-urlencoded')
            if not request.has_header('Content-length') and (not request.has_header('Transfer-encoding')):
                content_length = self._get_content_length(request)
                if content_length is not None:
                    request.add_unredirected_header('Content-length', str(content_length))
                else:
                    request.add_unredirected_header('Transfer-encoding', 'chunked')
        sel_host = host
        if request.has_proxy():
            scheme, sel = _splittype(request.selector)
            sel_host, sel_path = _splithost(sel)
        if not request.has_header('Host'):
            request.add_unredirected_header('Host', sel_host)
        for name, value in self.parent.addheaders:
            name = name.capitalize()
            if not request.has_header(name):
                request.add_unredirected_header(name, value)
        return request

    def do_open(self, http_class, req, **http_conn_args):
        """Return an HTTPResponse object for the request, using http_class.

        http_class must implement the HTTPConnection API from http.client.
        """
        host = req.host
        if not host:
            raise URLError('no host given')
        h = http_class(host, timeout=req.timeout, **http_conn_args)
        h.set_debuglevel(self._debuglevel)
        headers = dict(req.unredirected_hdrs)
        headers.update(req.headers)
        headers['Connection'] = 'close'
        headers = {name.title(): val for name, val in headers.items()}
        if req._tunnel_host:
            tunnel_headers = {}
            proxy_auth_hdr = 'Proxy-Authorization'
            if proxy_auth_hdr in headers:
                tunnel_headers[proxy_auth_hdr] = headers[proxy_auth_hdr]
                del headers[proxy_auth_hdr]
            h.set_tunnel(req._tunnel_host, headers=tunnel_headers)
        try:
            try:
                h.request(req.get_method(), req.selector, req.data, headers, encode_chunked=req.has_header('Transfer-encoding'))
            except OSError as err:
                raise URLError(err)
            r = h.getresponse()
        except:
            h.close()
            raise
        if h.sock:
            h.sock.close()
            h.sock = None
        r.url = req.get_full_url()
        r.msg = r.reason
        return r

class HTTP处理器(HTTP处理器基类):

    def http_open(self, req):
        return self.do_open(http.client.HTTPConnection, req)
    http_request = HTTP处理器基类.do_request_
if hasattr(http.client, 'HTTPSConnection'):

    class HTTPS处理器(HTTP处理器基类):

        def __init__(self, debuglevel=None, context=None, check_hostname=None):
            debuglevel = debuglevel if debuglevel is not None else http.client.HTTPSConnection.debuglevel
            HTTP处理器基类.__init__(self, debuglevel)
            if context is None:
                http_version = http.client.HTTPSConnection._http_vsn
                context = http.client._create_https_context(http_version)
            if check_hostname is not None:
                context.check_hostname = check_hostname
            self._context = context

        def https_open(self, req):
            return self.do_open(http.client.HTTPSConnection, req, context=self._context)
        https_request = HTTP处理器基类.do_request_
    __all__.append('HTTPSHandler')

class HTTP的Cookie处理器(处理器基类):

    def __init__(self, cookiejar=None):
        import http.cookiejar
        if cookiejar is None:
            cookiejar = http.cookiejar.CookieJar()
        self.cookiejar = cookiejar

    def http_request(self, request):
        self.cookiejar.add_cookie_header(request)
        return request

    def http_response(self, request, response):
        self.cookiejar.extract_cookies(response, request)
        return response
    https_request = http_request
    https_response = http_response

class 未知协议处理器(处理器基类):

    def unknown_open(self, req):
        type = req.type
        raise URLError('unknown url type: %s' % type)

def 解析键值列表(l):
    """Parse list of key=value strings where keys are not duplicated."""
    parsed = {}
    for elt in l:
        k, v = elt.split('=', 1)
        if v[0] == '"' and v[-1] == '"':
            v = v[1:-1]
        parsed[k] = v
    return parsed

def 解析HTTP列表(s):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Neither commas nor quotes count if they are escaped.
    Only double-quotes count, not single-quotes.
    """
    res = []
    part = ''
    escape = quote = False
    for cur in s:
        if escape:
            part += cur
            escape = False
            continue
        if quote:
            if cur == '\\':
                escape = True
                continue
            elif cur == '"':
                quote = False
            part += cur
            continue
        if cur == ',':
            res.append(part)
            part = ''
            continue
        if cur == '"':
            quote = True
        part += cur
    if part:
        res.append(part)
    return [part.strip() for part in res]

class 文件处理器(处理器基类):
    names = None

    def get_names(self):
        if 文件处理器.names is None:
            try:
                文件处理器.names = tuple(socket.gethostbyname_ex('localhost')[2] + socket.gethostbyname_ex(socket.gethostname())[2])
            except socket.gaierror:
                文件处理器.names = (socket.gethostbyname('localhost'),)
        return 文件处理器.names

    def open_local_file(self, req):
        import email.utils
        import mimetypes
        localfile = URL转路径(req.full_url, require_scheme=True, resolve_host=True)
        try:
            stats = os.stat(localfile)
            size = stats.st_size
            modified = email.utils.formatdate(stats.st_mtime, usegmt=True)
            mtype = mimetypes.guess_file_type(localfile)[0]
            headers = email.message_from_string('Content-type: %s\nContent-length: %d\nLast-modified: %s\n' % (mtype or 'text/plain', size, modified))
            origurl = 路径转URL(localfile, add_scheme=True)
            return addinfourl(open(localfile, 'rb'), headers, origurl)
        except OSError as exp:
            raise URLError(exp, exp.filename)
    file_open = open_local_file

def _is_local_authority(authority, resolve):
    if not authority or authority == 'localhost':
        return True
    try:
        hostname = socket.gethostname()
    except (socket.gaierror, AttributeError):
        pass
    else:
        if authority == hostname:
            return True
    if not resolve:
        return False
    try:
        address = socket.gethostbyname(authority)
    except (socket.gaierror, AttributeError, UnicodeEncodeError):
        return False
    return address in 文件处理器().get_names()

class FTP处理器(处理器基类):

    def ftp_open(self, req):
        import ftplib
        import mimetypes
        host = req.host
        if not host:
            raise URLError('ftp error: no host given')
        host, port = _splitport(host)
        if port is None:
            port = ftplib.FTP_PORT
        else:
            port = int(port)
        user, host = _splituser(host)
        if user:
            user, passwd = _splitpasswd(user)
        else:
            passwd = None
        host = unquote(host)
        user = user or ''
        passwd = passwd or ''
        try:
            host = socket.gethostbyname(host)
        except OSError as msg:
            raise URLError(msg)
        path, attrs = _splitattr(req.selector)
        dirs = path.split('/')
        dirs = list(map(unquote, dirs))
        dirs, file = (dirs[:-1], dirs[-1])
        if dirs and (not dirs[0]):
            dirs = dirs[1:]
        fw = None
        try:
            fw = self.connect_ftp(user, passwd, host, port, dirs, req.timeout)
            type = file and 'I' or 'D'
            for attr in attrs:
                attr, value = _splitvalue(attr)
                if attr.lower() == 'type' and value in ('a', 'A', 'i', 'I', 'd', 'D'):
                    type = value.upper()
            fp, retrlen = fw.retrfile(file, type)
            headers = ''
            mtype = mimetypes.guess_type(req.full_url)[0]
            if mtype:
                headers += 'Content-type: %s\n' % mtype
            if retrlen is not None and retrlen >= 0:
                headers += 'Content-length: %d\n' % retrlen
            headers = email.message_from_string(headers)
            return addinfourl(fp, headers, req.full_url)
        except Exception as exp:
            if fw is not None and (not fw.keepalive):
                fw.close()
            if isinstance(exp, ftplib.all_errors):
                raise URLError(f'ftp error: {exp}') from exp
            raise

    def connect_ftp(self, user, passwd, host, port, dirs, timeout):
        return ftpwrapper(user, passwd, host, port, dirs, timeout, persistent=False)

class 带缓存FTP处理器(FTP处理器):

    def __init__(self):
        self.cache = {}
        self.timeout = {}
        self.soonest = 0
        self.delay = 60
        self.max_conns = 16

    def setTimeout(self, t):
        self.delay = t

    def setMaxConns(self, m):
        self.max_conns = m

    def connect_ftp(self, user, passwd, host, port, dirs, timeout):
        key = (user, host, port, '/'.join(dirs), timeout)
        conn = self.cache.get(key)
        if conn is None or not conn.keepalive:
            if conn is not None:
                conn.close()
            conn = self.cache[key] = ftpwrapper(user, passwd, host, port, dirs, timeout)
        self.timeout[key] = time.time() + self.delay
        self.check_cache()
        return conn

    def check_cache(self):
        t = time.time()
        if self.soonest <= t:
            for k, v in list(self.timeout.items()):
                if v < t:
                    self.cache[k].close()
                    del self.cache[k]
                    del self.timeout[k]
        self.soonest = min(list(self.timeout.values()))
        if len(self.cache) == self.max_conns:
            for k, v in list(self.timeout.items()):
                if v == self.soonest:
                    del self.cache[k]
                    del self.timeout[k]
                    break
            self.soonest = min(list(self.timeout.values()))

    def clear_cache(self):
        for conn in self.cache.values():
            conn.close()
        self.cache.clear()
        self.timeout.clear()

class data协议处理器(处理器基类):

    def data_open(self, req):
        url = req.full_url
        scheme, data = url.split(':', 1)
        mediatype, data = data.split(',', 1)
        if re.search('[\\x00-\\x1F\\x7F]', mediatype):
            raise ValueError('Control characters not allowed in data: mediatype')
        data = unquote_to_bytes(data)
        if mediatype.endswith(';base64'):
            data = base64.decodebytes(data)
            mediatype = mediatype[:-7]
        if not mediatype:
            mediatype = 'text/plain;charset=US-ASCII'
        headers = email.message_from_string('Content-type: %s\nContent-length: %d\n' % (mediatype, len(data)))
        return addinfourl(io.BytesIO(data), headers, url)

def URL转路径(url, *, require_scheme=False, resolve_host=False):
    """Convert the given file URL to a local file system path.

    The 'file:' scheme prefix must be omitted unless *require_scheme*
    is set to true.

    The URL authority may be resolved with gethostbyname() if
    *resolve_host* is set to true.
    """
    if not require_scheme:
        url = 'file:' + url
    scheme, authority, url = urlsplit(url)[:3]
    if scheme != 'file':
        raise URLError("URL is missing a 'file:' scheme")
    if os.name == 'nt':
        if authority[1:2] == ':':
            url = authority + url
        elif not _is_local_authority(authority, resolve_host):
            url = '//' + authority + url
        elif url[:3] == '///':
            url = url[1:]
        else:
            if url[:1] == '/' and url[2:3] in (':', '|'):
                url = url[1:]
            if url[1:2] == '|':
                url = url[:1] + ':' + url[2:]
        url = url.replace('/', '\\')
    elif not _is_local_authority(authority, resolve_host):
        raise URLError('file:// scheme is supported only on localhost')
    encoding = sys.getfilesystemencoding()
    errors = sys.getfilesystemencodeerrors()
    return unquote(url, encoding=encoding, errors=errors)

def 路径转URL(pathname, *, add_scheme=False):
    """Convert the given local file system path to a file URL.

    The 'file:' scheme prefix is omitted unless *add_scheme*
    is set to true.
    """
    if os.name == 'nt':
        pathname = pathname.replace('\\', '/')
    encoding = sys.getfilesystemencoding()
    errors = sys.getfilesystemencodeerrors()
    scheme = 'file:' if add_scheme else ''
    drive, root, tail = os.path.splitroot(pathname)
    if drive:
        if drive[:4] == '//?/':
            drive = drive[4:]
            if drive[:4].upper() == 'UNC/':
                drive = '//' + drive[4:]
        if drive[1:] == ':':
            drive = '///' + drive
        drive = quote(drive, encoding=encoding, errors=errors, safe='/:')
    elif root:
        root = '//' + root
    tail = quote(tail, encoding=encoding, errors=errors)
    return scheme + drive + root + tail
_localhost = None

def localhost():
    """Return the IP address of the magic hostname 'localhost'."""
    global _localhost
    if _localhost is None:
        _localhost = socket.gethostbyname('localhost')
    return _localhost
_thishost = None

def thishost():
    """Return the IP addresses of the current host."""
    global _thishost
    if _thishost is None:
        try:
            _thishost = tuple(socket.gethostbyname_ex(socket.gethostname())[2])
        except socket.gaierror:
            _thishost = tuple(socket.gethostbyname_ex('localhost')[2])
    return _thishost
_ftperrors = None

def ftperrors():
    """Return the set of errors raised by the FTP class."""
    global _ftperrors
    if _ftperrors is None:
        import ftplib
        _ftperrors = ftplib.all_errors
    return _ftperrors
_noheaders = None

def noheaders():
    """Return an empty email Message object."""
    global _noheaders
    if _noheaders is None:
        _noheaders = email.message_from_string('')
    return _noheaders

class ftpwrapper:
    """Class used by open_ftp() for cache of open FTP connections."""

    def __init__(self, user, passwd, host, port, dirs, timeout=None, persistent=True):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.dirs = dirs
        self.timeout = timeout
        self.refcount = 0
        self.keepalive = persistent
        try:
            self.init()
        except:
            self.close()
            raise

    def init(self):
        import ftplib
        self.busy = 0
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.host, self.port, self.timeout)
        self.ftp.login(self.user, self.passwd)
        _target = '/'.join(self.dirs)
        self.ftp.cwd(_target)

    def retrfile(self, file, type):
        import ftplib
        self.endtransfer()
        if type in ('d', 'D'):
            cmd = 'TYPE A'
            isdir = 1
        else:
            cmd = 'TYPE ' + type
            isdir = 0
        try:
            self.ftp.voidcmd(cmd)
        except ftplib.all_errors:
            self.init()
            self.ftp.voidcmd(cmd)
        conn = None
        if file and (not isdir):
            try:
                cmd = 'RETR ' + file
                conn, retrlen = self.ftp.ntransfercmd(cmd)
            except ftplib.error_perm as reason:
                if str(reason)[:3] != '550':
                    raise URLError(f'ftp error: {reason}') from reason
        if not conn:
            self.ftp.voidcmd('TYPE A')
            if file:
                pwd = self.ftp.pwd()
                try:
                    try:
                        self.ftp.cwd(file)
                    except ftplib.error_perm as reason:
                        raise URLError('ftp error: %r' % reason) from reason
                finally:
                    self.ftp.cwd(pwd)
                cmd = 'LIST ' + file
            else:
                cmd = 'LIST'
            conn, retrlen = self.ftp.ntransfercmd(cmd)
        self.busy = 1
        ftpobj = addclosehook(conn.makefile('rb'), self.file_close)
        self.refcount += 1
        conn.close()
        return (ftpobj, retrlen)

    def endtransfer(self):
        if not self.busy:
            return
        self.busy = 0
        try:
            self.ftp.voidresp()
        except ftperrors():
            pass

    def close(self):
        self.keepalive = False
        if self.refcount <= 0:
            self.real_close()

    def file_close(self):
        self.endtransfer()
        self.refcount -= 1
        if self.refcount <= 0 and (not self.keepalive):
            self.real_close()

    def real_close(self):
        self.endtransfer()
        try:
            self.ftp.close()
        except ftperrors():
            pass

def 从环境取代理():
    """Return a dictionary of scheme -> proxy server URL mappings.

    Scan the environment for variables named <scheme>_proxy;
    this seems to be the standard convention.
    """
    proxies = {}
    environment = []
    for name in os.environ:
        if len(name) > 5 and name[-6] == '_' and (name[-5:].lower() == 'proxy'):
            value = os.environ[name]
            proxy_name = name[:-6].lower()
            environment.append((name, value, proxy_name))
            if value:
                proxies[proxy_name] = value
    if 'REQUEST_METHOD' in os.environ:
        proxies.pop('http', None)
    for name, value, proxy_name in environment:
        if name[-6:] == '_proxy':
            if value:
                proxies[proxy_name] = value
            else:
                proxies.pop(proxy_name, None)
    return proxies

def 环境代理绕过(host, proxies=None):
    """Test if proxies should not be used for a particular host.

    Checks the proxy dict for the value of no_proxy, which should
    be a list of comma separated DNS suffixes, or '*' for all hosts.

    """
    if proxies is None:
        proxies = 从环境取代理()
    try:
        no_proxy = proxies['no']
    except KeyError:
        return False
    if no_proxy == '*':
        return True
    host = host.lower()
    hostonly, port = _splitport(host)
    for name in no_proxy.split(','):
        name = name.strip()
        if name:
            name = name.lstrip('.')
            name = name.lower()
            if hostonly == name or host == name:
                return True
            name = '.' + name
            if hostonly.endswith(name) or host.endswith(name):
                return True
    return False

def _proxy_bypass_macosx_sysconf(host, proxy_settings):
    """
    Return True iff this host shouldn't be accessed using a proxy

    This function uses the MacOSX framework SystemConfiguration
    to fetch the proxy information.

    proxy_settings come from _scproxy._get_proxy_settings or get mocked ie:
    { 'exclude_simple': bool,
      'exceptions': ['foo.bar', '*.bar.com', '127.0.0.1', '10.1', '10.0/16']
    }
    """
    from fnmatch import fnmatch
    from ipaddress import AddressValueError, IPv4Address
    hostonly, port = _splitport(host)

    def ip2num(ipAddr):
        parts = ipAddr.split('.')
        parts = list(map(int, parts))
        if len(parts) != 4:
            parts = (parts + [0, 0, 0, 0])[:4]
        return parts[0] << 24 | parts[1] << 16 | parts[2] << 8 | parts[3]
    if '.' not in host:
        if proxy_settings['exclude_simple']:
            return True
    hostIP = None
    try:
        hostIP = int(IPv4Address(hostonly))
    except AddressValueError:
        pass
    for value in proxy_settings.get('exceptions', ()):
        if not value:
            continue
        m = re.match('(\\d+(?:\\.\\d+)*)(/\\d+)?', value)
        if m is not None and hostIP is not None:
            base = ip2num(m.group(1))
            mask = m.group(2)
            if mask is None:
                mask = 8 * (m.group(1).count('.') + 1)
            else:
                mask = int(mask[1:])
            if mask < 0 or mask > 32:
                continue
            mask = 32 - mask
            if hostIP >> mask == base >> mask:
                return True
        elif fnmatch(host, value):
            return True
    return False

def _proxy_bypass_winreg_override(host, override):
    """Return True if the host should bypass the proxy server.

    The proxy override list is obtained from the Windows
    Internet settings proxy override registry value.

    An example of a proxy override value is:
    "www.example.com;*.example.net; 192.168.0.1"
    """
    from fnmatch import fnmatch
    host, _ = _splitport(host)
    proxy_override = override.split(';')
    for test in proxy_override:
        test = test.strip()
        if test == '<local>':
            if '.' not in host:
                return True
        elif fnmatch(host, test):
            return True
    return False
if sys.platform == 'darwin':
    from _scproxy import _get_proxy_settings, _get_proxies

    def proxy_bypass_macosx_sysconf(host):
        proxy_settings = _get_proxy_settings()
        return _proxy_bypass_macosx_sysconf(host, proxy_settings)

    def getproxies_macosx_sysconf():
        """Return a dictionary of scheme -> proxy server URL mappings.

        This function uses the MacOSX framework SystemConfiguration
        to fetch the proxy information.
        """
        return _get_proxies()

    def 代理绕过(host):
        """Return True, if host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or from the MacOSX framework SystemConfiguration.

        """
        proxies = 从环境取代理()
        if proxies:
            return 环境代理绕过(host, proxies)
        else:
            return proxy_bypass_macosx_sysconf(host)

    def 取代理设置():
        return 从环境取代理() or getproxies_macosx_sysconf()
elif os.name == 'nt':

    def getproxies_registry():
        """Return a dictionary of scheme -> proxy server URL mappings.

        Win32 uses the registry to store proxies.

        """
        proxies = {}
        try:
            import winreg
        except ImportError:
            return proxies
        try:
            internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
            proxyEnable = winreg.QueryValueEx(internetSettings, 'ProxyEnable')[0]
            if proxyEnable:
                proxyServer = str(winreg.QueryValueEx(internetSettings, 'ProxyServer')[0])
                if '=' not in proxyServer and ';' not in proxyServer:
                    proxyServer = 'http={0};https={0};ftp={0}'.format(proxyServer)
                for p in proxyServer.split(';'):
                    protocol, address = p.split('=', 1)
                    if not re.match('(?:[^/:]+)://', address):
                        if protocol in ('http', 'https', 'ftp'):
                            address = 'http://' + address
                        elif protocol == 'socks':
                            address = 'socks://' + address
                    proxies[protocol] = address
                if proxies.get('socks'):
                    address = re.sub('^socks://', 'socks4://', proxies['socks'])
                    proxies['http'] = proxies.get('http') or address
                    proxies['https'] = proxies.get('https') or address
            internetSettings.Close()
        except (OSError, ValueError, TypeError):
            pass
        return proxies

    def 取代理设置():
        """Return a dictionary of scheme -> proxy server URL mappings.

        Returns settings gathered from the environment, if specified,
        or the registry.

        """
        return 从环境取代理() or getproxies_registry()

    def proxy_bypass_registry(host):
        try:
            import winreg
        except ImportError:
            return False
        try:
            internetSettings = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings')
            proxyEnable = winreg.QueryValueEx(internetSettings, 'ProxyEnable')[0]
            proxyOverride = str(winreg.QueryValueEx(internetSettings, 'ProxyOverride')[0])
        except OSError:
            return False
        if not proxyEnable or not proxyOverride:
            return False
        return _proxy_bypass_winreg_override(host, proxyOverride)

    def 代理绕过(host):
        """Return True, if host should be bypassed.

        Checks proxy settings gathered from the environment, if specified,
        or the registry.

        """
        proxies = 从环境取代理()
        if proxies:
            return 环境代理绕过(host, proxies)
        else:
            return proxy_bypass_registry(host)
else:
    取代理设置 = 从环境取代理
    代理绕过 = 环境代理绕过


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'AbstractBasicAuthHandler': '基本认证处理基类',
    'AbstractDigestAuthHandler': '摘要认证处理基类',
    'AbstractHTTPHandler': 'HTTP处理器基类',
    'BaseHandler': '处理器基类',
    'CacheFTPHandler': '带缓存FTP处理器',
    'ContentTooShortError': '内容过短错误',
    'DataHandler': 'data协议处理器',
    'FTPHandler': 'FTP处理器',
    'FileHandler': '文件处理器',
    'HTTPBasicAuthHandler': 'HTTP基本认证处理器',
    'HTTPCookieProcessor': 'HTTP的Cookie处理器',
    'HTTPDefaultErrorHandler': 'HTTP默认错误处理器',
    'HTTPDigestAuthHandler': 'HTTP摘要认证处理器',
    'HTTPErrorProcessor': 'HTTP错误处理器',
    'HTTPHandler': 'HTTP处理器',
    'HTTPPasswordMgr': 'HTTP口令管理',
    'HTTPPasswordMgrWithDefaultRealm': 'HTTP口令管理带默认领域',
    'HTTPPasswordMgrWithPriorAuth': 'HTTP口令管理带预认证',
    'HTTPRedirectHandler': 'HTTP重定向处理器',
    'HTTPSHandler': 'HTTPS处理器',
    'OpenerDirector': '打开器',
    'ProxyBasicAuthHandler': '代理基本认证处理器',
    'ProxyDigestAuthHandler': '代理摘要认证处理器',
    'ProxyHandler': '代理处理器',
    'Request': '请求',
    'UnknownHandler': '未知协议处理器',
    'build_opener': '造打开器',
    'getproxies': '取代理设置',
    'getproxies_environment': '从环境取代理',
    'install_opener': '装上打开器',
    'parse_http_list': '解析HTTP列表',
    'parse_keqv_list': '解析键值列表',
    'pathname2url': '路径转URL',
    'proxy_bypass': '代理绕过',
    'proxy_bypass_environment': '环境代理绕过',
    'url2pathname': 'URL转路径',
    'urlcleanup': '清理URL临时文件',
    'urlopen': '打开URL',
    'urlretrieve': '取URL到文件',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'FTP处理器',
    'HTTPS处理器',
    'HTTP口令管理',
    'HTTP口令管理带预认证',
    'HTTP口令管理带默认领域',
    'HTTP基本认证处理器',
    'HTTP处理器',
    'HTTP摘要认证处理器',
    'HTTP的Cookie处理器',
    'HTTP重定向处理器',
    'HTTP错误处理器',
    'HTTP默认错误处理器',
    'URL转路径',
    'data协议处理器',
    '代理基本认证处理器',
    '代理处理器',
    '代理摘要认证处理器',
    '取URL到文件',
    '取代理设置',
    '基本认证处理基类',
    '处理器基类',
    '带缓存FTP处理器',
    '打开URL',
    '打开器',
    '摘要认证处理基类',
    '文件处理器',
    '未知协议处理器',
    '清理URL临时文件',
    '装上打开器',
    '请求',
    '路径转URL',
    '造打开器',
])

# ---- 转发层结束 ----
