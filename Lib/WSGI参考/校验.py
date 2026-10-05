# -*- coding: utf-8 -*-
"""WSGI参考.校验 —— 汉语库（由 tools/汉化库.py 从 Lib/wsgiref/validate.py 机械生成，**不要手改**）。

英文库 Lib/wsgiref.validate.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py wsgiref
"""


"""
Middleware to check for obedience to the WSGI specification.

Some of the things this checks:

* Signature of the application and start_response (including that
  keyword arguments are not used).

* Environment checks:

  - Environment is a dictionary (and not a subclass).

  - That all the required keys are in the environment: REQUEST_METHOD,
    SERVER_NAME, SERVER_PORT, wsgi.version, wsgi.input, wsgi.errors,
    wsgi.multithread, wsgi.multiprocess, wsgi.run_once

  - That HTTP_CONTENT_TYPE and HTTP_CONTENT_LENGTH are not in the
    environment (these headers should appear as CONTENT_LENGTH and
    CONTENT_TYPE).

  - Warns if QUERY_STRING is missing, as the cgi module acts
    unpredictably in that case.

  - That CGI-style variables (that don't contain a .) have
    (non-unicode) string values

  - That wsgi.version is a tuple

  - That wsgi.url_scheme is 'http' or 'https' (@@: is this too
    restrictive?)

  - Warns if the REQUEST_METHOD is not known (@@: probably too
    restrictive).

  - That SCRIPT_NAME and PATH_INFO are empty or start with /

  - That at least one of SCRIPT_NAME or PATH_INFO are set.

  - That CONTENT_LENGTH is a positive integer.

  - That SCRIPT_NAME is not '/' (it should be '', and PATH_INFO should
    be '/').

  - That wsgi.input has the methods read, readline, readlines, and
    __iter__

  - That wsgi.errors has the methods flush, write, writelines

* The status is a string, contains a space, starts with an integer,
  and that integer is in range (> 100).

* That the headers is a list (not a subclass, not another kind of
  sequence).

* That the items of the headers are tuples of strings.

* That there is no 'status' header (that is used in CGI, but not in
  WSGI).

* That the headers don't contain newlines or colons, end in _ or -, or
  contain characters codes below 037.

* That Content-Type is given if there is content (CGI often has a
  default content type, but WSGI does not).

* That no Content-Type is given when there is no content (@@: is this
  too restrictive?)

* That the exc_info argument to start_response is a tuple or None.

* That all calls to the writer are with strings, and no other methods
  on the writer are accessed.

* That wsgi.input is used properly:

  - .read() is called with exactly one argument

  - That it returns a string

  - That readline, readlines, and __iter__ return strings

  - That .close() is not called

  - No other methods are provided

* That wsgi.errors is used properly:

  - .write() and .writelines() is called with a string

  - That .close() is not called, and no other methods are provided.

* The response iterator:

  - That it is not a string (it should be a list of a single string; a
    string will work, but perform horribly).

  - That .__next__() returns a string

  - That the iterator is not iterated over until start_response has
    been called (that can signal either a server or application
    error).

  - That .close() is called (doesn't raise exception, only prints to
    sys.stderr, because we only know it isn't called when the object
    is garbage collected).
"""
_英文原名表 = {'ErrorWrapper': '错误包装器', 'InputWrapper': '输入包装器', 'IteratorWrapper': '迭代器包装器', 'PartialIteratorWrapper': '部分迭代器包装器', 'WSGIWarning': 'WSGI警告', 'WriteWrapper': '写包装器', 'assert_': '断言检查', 'bad_header_value_re': '坏头部值正则', 'check_content_type': '检查内容类型', 'check_environ': '检查环境', 'check_errors': '检查错误', 'check_exc_info': '检查异常信息', 'check_headers': '检查头部', 'check_input': '检查输入', 'check_iterator': '检查迭代器', 'check_status': '检查状态', 'check_string_type': '检查字符串类型', 'header_re': '头部正则', 'validator': '校验器'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['validator']
import re
import sys
import warnings
头部正则 = re.compile('^[a-zA-Z][a-zA-Z0-9\\-_]*$')
坏头部值正则 = re.compile('[\\000-\\037]')

class WSGI警告(Warning):
    """
    Raised in response to WSGI-spec-related warnings
    """

def 断言检查(cond, *args):
    if not cond:
        raise AssertionError(*args)

def 检查字符串类型(value, title):
    if type(value) is str:
        return value
    raise AssertionError('{0} must be of type str (got {1})'.format(title, repr(value)))

def 校验器(application):
    """
    When applied between a WSGI server and a WSGI application, this
    middleware will check for WSGI compliance on a number of levels.
    This middleware does not modify the request or response in any
    way, but will raise an AssertionError if anything seems off
    (except for a failure to close the application iterator, which
    will be printed to stderr -- there's no way to raise an exception
    at that point).
    """

    def lint_app(*args, **kw):
        断言检查(len(args) == 2, 'Two arguments required')
        断言检查(not kw, 'No keyword arguments allowed')
        environ, start_response = args
        检查环境(environ)
        start_response_started = []

        def start_response_wrapper(*args, **kw):
            断言检查(len(args) == 2 or len(args) == 3, 'Invalid number of arguments: %s' % (args,))
            断言检查(not kw, 'No keyword arguments allowed')
            status = args[0]
            headers = args[1]
            if len(args) == 3:
                exc_info = args[2]
            else:
                exc_info = None
            检查状态(status)
            检查头部(headers)
            检查内容类型(status, headers)
            检查异常信息(exc_info)
            start_response_started.append(None)
            return 写包装器(start_response(*args))
        environ['wsgi.input'] = 输入包装器(environ['wsgi.input'])
        environ['wsgi.errors'] = 错误包装器(environ['wsgi.errors'])
        iterator = application(environ, start_response_wrapper)
        断言检查(iterator is not None and iterator != False, 'The application must return an iterator, if only an empty list')
        检查迭代器(iterator)
        return 迭代器包装器(iterator, start_response_started)
    return lint_app

class 输入包装器:

    def __init__(self, wsgi_input):
        self.input = wsgi_input

    def read(self, *args):
        断言检查(len(args) == 1)
        v = self.input.read(*args)
        断言检查(type(v) is bytes)
        return v

    def readline(self, *args):
        断言检查(len(args) <= 1)
        v = self.input.readline(*args)
        断言检查(type(v) is bytes)
        return v

    def readlines(self, *args):
        断言检查(len(args) <= 1)
        lines = self.input.readlines(*args)
        断言检查(type(lines) is list)
        for line in lines:
            断言检查(type(line) is bytes)
        return lines

    def __iter__(self):
        while (line := self.readline()):
            yield line

    def close(self):
        断言检查(0, 'input.close() must not be called')

class 错误包装器:

    def __init__(self, wsgi_errors):
        self.errors = wsgi_errors

    def write(self, s):
        断言检查(type(s) is str)
        self.errors.write(s)

    def flush(self):
        self.errors.flush()

    def writelines(self, seq):
        for line in seq:
            self.write(line)

    def close(self):
        断言检查(0, 'errors.close() must not be called')

class 写包装器:

    def __init__(self, wsgi_writer):
        self.writer = wsgi_writer

    def __call__(self, s):
        断言检查(type(s) is bytes)
        self.writer(s)

class 部分迭代器包装器:

    def __init__(self, wsgi_iterator):
        self.iterator = wsgi_iterator

    def __iter__(self):
        return 迭代器包装器(self.iterator, None)

class 迭代器包装器:

    def __init__(self, wsgi_iterator, check_start_response):
        self.original_iterator = wsgi_iterator
        self.iterator = iter(wsgi_iterator)
        self.closed = False
        self.check_start_response = check_start_response

    def __iter__(self):
        return self

    def __next__(self):
        断言检查(not self.closed, 'Iterator read after closed')
        v = next(self.iterator)
        if type(v) is not bytes:
            断言检查(False, 'Iterator yielded non-bytestring (%r)' % (v,))
        if self.check_start_response is not None:
            断言检查(self.check_start_response, 'The application returns and we started iterating over its body, but start_response has not yet been called')
            self.check_start_response = None
        return v

    def close(self):
        self.closed = True
        if hasattr(self.original_iterator, 'close'):
            self.original_iterator.close()

    def __del__(self):
        if not self.closed:
            sys.stderr.write('Iterator garbage collected without being closed')
        断言检查(self.closed, 'Iterator garbage collected without being closed')

def 检查环境(environ):
    断言检查(type(environ) is dict, 'Environment is not of the right type: %r (environment: %r)' % (type(environ), environ))
    for key in ['REQUEST_METHOD', 'SERVER_NAME', 'SERVER_PORT', 'wsgi.version', 'wsgi.input', 'wsgi.errors', 'wsgi.multithread', 'wsgi.multiprocess', 'wsgi.run_once']:
        断言检查(key in environ, 'Environment missing required key: %r' % (key,))
    for key in ['HTTP_CONTENT_TYPE', 'HTTP_CONTENT_LENGTH']:
        断言检查(key not in environ, 'Environment should not have the key: %s (use %s instead)' % (key, key[5:]))
    if 'QUERY_STRING' not in environ:
        warnings.warn('QUERY_STRING is not in the WSGI environment; the cgi module will use sys.argv when this variable is missing, so application errors are more likely', WSGI警告)
    for key in environ.keys():
        if '.' in key:
            continue
        断言检查(type(environ[key]) is str, 'Environmental variable %s is not a string: %r (value: %r)' % (key, type(environ[key]), environ[key]))
    断言检查(type(environ['wsgi.version']) is tuple, 'wsgi.version should be a tuple (%r)' % (environ['wsgi.version'],))
    断言检查(environ['wsgi.url_scheme'] in ('http', 'https'), 'wsgi.url_scheme unknown: %r' % environ['wsgi.url_scheme'])
    检查输入(environ['wsgi.input'])
    检查错误(environ['wsgi.errors'])
    if environ['REQUEST_METHOD'] not in ('GET', 'HEAD', 'POST', 'OPTIONS', 'PATCH', 'PUT', 'DELETE', 'TRACE'):
        warnings.warn('Unknown REQUEST_METHOD: %r' % environ['REQUEST_METHOD'], WSGI警告)
    断言检查(not environ.get('SCRIPT_NAME') or environ['SCRIPT_NAME'].startswith('/'), "SCRIPT_NAME doesn't start with /: %r" % environ['SCRIPT_NAME'])
    断言检查(not environ.get('PATH_INFO') or environ['PATH_INFO'].startswith('/'), "PATH_INFO doesn't start with /: %r" % environ['PATH_INFO'])
    if environ.get('CONTENT_LENGTH'):
        断言检查(int(environ['CONTENT_LENGTH']) >= 0, 'Invalid CONTENT_LENGTH: %r' % environ['CONTENT_LENGTH'])
    if not environ.get('SCRIPT_NAME'):
        断言检查('PATH_INFO' in environ, "One of SCRIPT_NAME or PATH_INFO are required (PATH_INFO should at least be '/' if SCRIPT_NAME is empty)")
    断言检查(environ.get('SCRIPT_NAME') != '/', "SCRIPT_NAME cannot be '/'; it should instead be '', and PATH_INFO should be '/'")

def 检查输入(wsgi_input):
    for attr in ['read', 'readline', 'readlines', '__iter__']:
        断言检查(hasattr(wsgi_input, attr), "wsgi.input (%r) doesn't have the attribute %s" % (wsgi_input, attr))

def 检查错误(wsgi_errors):
    for attr in ['flush', 'write', 'writelines']:
        断言检查(hasattr(wsgi_errors, attr), "wsgi.errors (%r) doesn't have the attribute %s" % (wsgi_errors, attr))

def 检查状态(status):
    status = 检查字符串类型(status, 'Status')
    status_code = status.split(None, 1)[0]
    断言检查(len(status_code) == 3, 'Status codes must be three characters: %r' % status_code)
    status_int = int(status_code)
    断言检查(status_int >= 100, 'Status code is invalid: %r' % status_int)
    if len(status) < 4 or status[3] != ' ':
        warnings.warn('The status string (%r) should be a three-digit integer followed by a single space and a status explanation' % status, WSGI警告)

def 检查头部(headers):
    断言检查(type(headers) is list, 'Headers (%r) must be of type list: %r' % (headers, type(headers)))
    for item in headers:
        断言检查(type(item) is tuple, 'Individual headers (%r) must be of type tuple: %r' % (item, type(item)))
        断言检查(len(item) == 2)
        name, value = item
        name = 检查字符串类型(name, 'Header name')
        value = 检查字符串类型(value, 'Header value')
        断言检查(name.lower() != 'status', 'The Status header cannot be used; it conflicts with CGI script, and HTTP status is not given through headers (value: %r).' % value)
        断言检查('\n' not in name and ':' not in name, "Header names may not contain ':' or '\\n': %r" % name)
        断言检查(头部正则.search(name), 'Bad header name: %r' % name)
        断言检查(not name.endswith('-') and (not name.endswith('_')), "Names may not end in '-' or '_': %r" % name)
        if 坏头部值正则.search(value):
            断言检查(0, 'Bad header value: %r (bad char: %r)' % (value, 坏头部值正则.search(value).group(0)))

def 检查内容类型(status, headers):
    status = 检查字符串类型(status, 'Status')
    code = int(status.split(None, 1)[0])
    NO_MESSAGE_BODY = (204, 304)
    for name, value in headers:
        name = 检查字符串类型(name, 'Header name')
        if name.lower() == 'content-type':
            if code not in NO_MESSAGE_BODY:
                return
            断言检查(0, 'Content-Type header found in a %s response, which must not return content.' % code)
    if code not in NO_MESSAGE_BODY:
        断言检查(0, 'No Content-Type header found in headers (%s)' % headers)

def 检查异常信息(exc_info):
    断言检查(exc_info is None or type(exc_info) is tuple, 'exc_info (%r) is not a tuple: %r' % (exc_info, type(exc_info)))

def 检查迭代器(iterator):
    断言检查(not isinstance(iterator, (str, bytes)), 'You should not return a string as your application iterator, instead return a single-item list containing a bytestring.')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ErrorWrapper': '错误包装器',
    'InputWrapper': '输入包装器',
    'IteratorWrapper': '迭代器包装器',
    'PartialIteratorWrapper': '部分迭代器包装器',
    'WSGIWarning': 'WSGI警告',
    'WriteWrapper': '写包装器',
    'assert_': '断言检查',
    'bad_header_value_re': '坏头部值正则',
    'check_content_type': '检查内容类型',
    'check_environ': '检查环境',
    'check_errors': '检查错误',
    'check_exc_info': '检查异常信息',
    'check_headers': '检查头部',
    'check_input': '检查输入',
    'check_iterator': '检查迭代器',
    'check_status': '检查状态',
    'check_string_type': '检查字符串类型',
    'header_re': '头部正则',
    'validator': '校验器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '校验器',
]

# ---- 转发层结束 ----
