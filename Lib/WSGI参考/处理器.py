# -*- coding: utf-8 -*-
"""WSGI参考.处理器 —— 汉语库（由 tools/汉化库.py 从 Lib/wsgiref/handlers.py 机械生成，**不要手改**）。

英文库 Lib/wsgiref.handlers.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py wsgiref
"""


"""Base classes for server/gateway implementations"""
_英文原名表 = {'BaseCGIHandler': '基础CGI处理器', 'BaseHandler': '基础处理器', 'CGIHandler': 'CGI处理器', 'IISCGIHandler': 'IIS的CGI处理器', 'SimpleHandler': '简单处理器', 'format_date_time': '格式化日期时间', 'read_environ': '读环境变量'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
from .工具 import FileWrapper, guess_scheme, is_hop_by_hop
from .headers import Headers, _name_disallowed_re
import sys, os, time
__all__ = ['BaseHandler', 'SimpleHandler', 'BaseCGIHandler', 'CGIHandler', 'IISCGIHandler', 'read_environ']
_weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
_monthname = [None, 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def 格式化日期时间(timestamp):
    year, month, day, hh, mm, ss, wd, y, z = time.gmtime(timestamp)
    return '%s, %02d %3s %4d %02d:%02d:%02d GMT' % (_weekdayname[wd], day, _monthname[month], year, hh, mm, ss)
_is_request = {'SCRIPT_NAME', 'PATH_INFO', 'QUERY_STRING', 'REQUEST_METHOD', 'AUTH_TYPE', 'CONTENT_TYPE', 'CONTENT_LENGTH', 'HTTPS', 'REMOTE_USER', 'REMOTE_IDENT'}.__contains__

def _needs_transcode(k):
    return _is_request(k) or k.startswith('HTTP_') or k.startswith('SSL_') or (k.startswith('REDIRECT_') and _needs_transcode(k[9:]))

def 读环境变量():
    """Read environment, fixing HTTP variables"""
    enc = sys.getfilesystemencoding()
    esc = 'surrogateescape'
    try:
        ''.encode('utf-8', esc)
    except LookupError:
        esc = 'replace'
    environ = {}
    for k, v in os.environ.items():
        if _needs_transcode(k):
            if sys.platform == 'win32':
                software = os.environ.get('SERVER_SOFTWARE', '').lower()
                if software.startswith('microsoft-iis/'):
                    v = v.encode('utf-8').decode('iso-8859-1')
                elif software.startswith('apache/'):
                    pass
                elif software.startswith('simplehttp/') and 'python/3' in software:
                    v = v.encode('utf-8').decode('iso-8859-1')
                else:
                    v = v.encode(enc, 'replace').decode('iso-8859-1')
            else:
                v = v.encode(enc, esc).decode('iso-8859-1')
        environ[k] = v
    return environ

class 基础处理器:
    """Manage the invocation of a WSGI application"""
    wsgi_version = (1, 0)
    wsgi_multithread = True
    wsgi_multiprocess = True
    wsgi_run_once = False
    origin_server = True
    http_version = '1.0'
    server_software = None
    os_environ = 读环境变量()
    wsgi_file_wrapper = FileWrapper
    headers_class = Headers
    traceback_limit = None
    error_status = '500 Internal Server Error'
    error_headers = [('Content-Type', 'text/plain')]
    error_body = b'A server error occurred.  Please contact the administrator.'
    status = result = None
    headers_sent = False
    headers = None
    bytes_sent = 0

    def 运行(self, application):
        """Invoke the application"""
        try:
            self.准备环境()
            self.result = application(self.environ, self.开始响应)
            self.结束响应()
        except (ConnectionAbortedError, BrokenPipeError, ConnectionResetError):
            return
        except:
            try:
                self.处理错误()
            except:
                self.close()
                raise

    def 准备环境(self):
        """Set up the environment for one request"""
        env = self.environ = self.os_environ.copy()
        self.加CGI变量()
        env['wsgi.input'] = self.取标准输入()
        env['wsgi.errors'] = self.取标准错误()
        env['wsgi.version'] = self.wsgi_version
        env['wsgi.run_once'] = self.wsgi_run_once
        env['wsgi.url_scheme'] = self.取协议()
        env['wsgi.multithread'] = self.wsgi_multithread
        env['wsgi.multiprocess'] = self.wsgi_multiprocess
        if self.wsgi_file_wrapper is not None:
            env['wsgi.file_wrapper'] = self.wsgi_file_wrapper
        if self.origin_server and self.server_software:
            env.setdefault('SERVER_SOFTWARE', self.server_software)

    def 结束响应(self):
        """Send any iterable data, then close self and the iterable

        Subclasses intended for use in asynchronous servers will
        want to redefine this method, such that it sets up callbacks
        in the event loop to iterate over the data, and to call
        'self.close()' once the response is finished.
        """
        try:
            if not self.结果是文件吗() or not self.发送文件():
                for data in self.result:
                    self.write(data)
                self.结束内容()
        except:
            if hasattr(self.result, 'close'):
                self.result.close()
            raise
        else:
            self.close()

    def 取协议(self):
        """Return the URL scheme being used"""
        return guess_scheme(self.environ)

    def 设内容长度(self):
        """Compute Content-Length or switch to chunked encoding if possible"""
        try:
            blocks = len(self.result)
        except (TypeError, AttributeError, NotImplementedError):
            pass
        else:
            if blocks == 1:
                self.headers['Content-Length'] = str(self.bytes_sent)
                return

    def 清理头部(self):
        """Make any necessary header changes or defaults

        Subclasses can extend this to add other defaults.
        """
        if 'Content-Length' not in self.headers:
            self.设内容长度()

    def 开始响应(self, status, headers, exc_info=None):
        """'start_response()' callable as specified by PEP 3333"""
        if exc_info:
            try:
                if self.headers_sent:
                    raise
            finally:
                exc_info = None
        elif self.headers is not None:
            raise AssertionError('Headers already set!')
        self.status = status
        self.headers = self.headers_class(headers)
        status = self._convert_string_type(status, 'Status')
        self._validate_status(status)
        if __debug__:
            for name, val in headers:
                name = self._convert_string_type(name, 'Header name')
                val = self._convert_string_type(val, 'Header value')
                assert not is_hop_by_hop(name), f"Hop-by-hop header, '{name}: {val}', not allowed"
        return self.write

    def _validate_status(self, status):
        if _name_disallowed_re.search(status):
            raise ValueError('Control characters are not allowed in status')
        if len(status) < 4:
            raise AssertionError('Status must be at least 4 characters')
        if not status[:3].isdigit():
            raise AssertionError('Status message must begin w/3-digit code')
        if status[3] != ' ':
            raise AssertionError('Status message must have a space after code')

    def _convert_string_type(self, value, title):
        """Convert/check value type."""
        if type(value) is str:
            return value
        raise AssertionError('{0} must be of type str (got {1})'.format(title, repr(value)))

    def 发送前导(self):
        """Transmit version/status/date/server, via self._write()"""
        if self.origin_server:
            if self.客户端是现代的吗():
                self._write(('HTTP/%s %s\r\n' % (self.http_version, self.status)).encode('iso-8859-1'))
                if 'Date' not in self.headers:
                    self._write(('Date: %s\r\n' % 格式化日期时间(time.time())).encode('iso-8859-1'))
                if self.server_software and 'Server' not in self.headers:
                    self._write(('Server: %s\r\n' % self.server_software).encode('iso-8859-1'))
        else:
            self._write(('Status: %s\r\n' % self.status).encode('iso-8859-1'))

    def write(self, data):
        """'write()' callable as specified by PEP 3333"""
        assert type(data) is bytes, 'write() argument must be a bytes instance'
        if not self.status:
            raise AssertionError('write() before start_response()')
        elif not self.headers_sent:
            self.bytes_sent = len(data)
            self.发送头部()
        else:
            self.bytes_sent += len(data)
        self._write(data)
        self._flush()

    def 发送文件(self):
        """Platform-specific file transmission

        Override this method in subclasses to support platform-specific
        file transmission.  It is only called if the application's
        return iterable ('self.result') is an instance of
        'self.wsgi_file_wrapper'.

        This method should return a true value if it was able to actually
        transmit the wrapped file-like object using a platform-specific
        approach.  It should return a false value if normal iteration
        should be used instead.  An exception can be raised to indicate
        that transmission was attempted, but failed.

        NOTE: this method should call 'self.send_headers()' if
        'self.headers_sent' is false and it is going to attempt direct
        transmission of the file.
        """
        return False

    def 结束内容(self):
        """Ensure headers and content have both been sent"""
        if not self.headers_sent:
            self.headers.setdefault('Content-Length', '0')
            self.发送头部()
        else:
            pass

    def close(self):
        """Close the iterable (if needed) and reset all instance vars

        Subclasses may want to also drop the client connection.
        """
        try:
            if hasattr(self.result, 'close'):
                self.result.close()
        finally:
            self.result = self.headers = self.status = self.environ = None
            self.bytes_sent = 0
            self.headers_sent = False

    def 发送头部(self):
        """Transmit headers to the client, via self._write()"""
        self.清理头部()
        self.headers_sent = True
        if not self.origin_server or self.客户端是现代的吗():
            self.发送前导()
            self._write(bytes(self.headers))

    def 结果是文件吗(self):
        """True if 'self.result' is an instance of 'self.wsgi_file_wrapper'"""
        wrapper = self.wsgi_file_wrapper
        return wrapper is not None and isinstance(self.result, wrapper)

    def 客户端是现代的吗(self):
        """True if client can accept status and headers"""
        return self.environ['SERVER_PROTOCOL'].upper() != 'HTTP/0.9'

    def 记录异常(self, exc_info):
        """Log the 'exc_info' tuple in the server log

        Subclasses may override to retarget the output or change its format.
        """
        try:
            from traceback import print_exception
            stderr = self.取标准错误()
            print_exception(exc_info[0], exc_info[1], exc_info[2], self.traceback_limit, stderr)
            stderr.flush()
        finally:
            exc_info = None

    def 处理错误(self):
        """Log current error, and send error output to client if possible"""
        self.记录异常(sys.exc_info())
        if not self.headers_sent:
            self.result = self.错误输出(self.environ, self.开始响应)
            self.结束响应()

    def 错误输出(self, environ, start_response):
        """WSGI mini-app to create error output

        By default, this just uses the 'error_status', 'error_headers',
        and 'error_body' attributes to generate an output page.  It can
        be overridden in a subclass to dynamically generate diagnostics,
        choose an appropriate message for the user's preferred language, etc.

        Note, however, that it's not recommended from a security perspective to
        spit out diagnostics to any old user; ideally, you should have to do
        something special to enable diagnostic output, which is why we don't
        include any here!
        """
        start_response(self.error_status, self.error_headers[:], sys.exc_info())
        return [self.error_body]

    def _write(self, data):
        """Override in subclass to buffer data for send to client

        It's okay if this method actually transmits the data; BaseHandler
        just separates write and flush operations for greater efficiency
        when the underlying system actually has such a distinction.
        """
        raise NotImplementedError

    def _flush(self):
        """Override in subclass to force sending of recent '_write()' calls

        It's okay if this method is a no-op (i.e., if '_write()' actually
        sends the data.
        """
        raise NotImplementedError

    def 取标准输入(self):
        """Override in subclass to return suitable 'wsgi.input'"""
        raise NotImplementedError

    def 取标准错误(self):
        """Override in subclass to return suitable 'wsgi.errors'"""
        raise NotImplementedError

    def 加CGI变量(self):
        """Override in subclass to insert CGI variables in 'self.environ'"""
        raise NotImplementedError
_装类转发(基础处理器, {'add_cgi_vars': '加CGI变量', 'cleanup_headers': '清理头部', 'client_is_modern': '客户端是现代的吗', 'error_output': '错误输出', 'finish_content': '结束内容', 'finish_response': '结束响应', 'get_scheme': '取协议', 'get_stderr': '取标准错误', 'get_stdin': '取标准输入', 'handle_error': '处理错误', 'log_exception': '记录异常', 'result_is_file': '结果是文件吗', 'run': '运行', 'send_headers': '发送头部', 'send_preamble': '发送前导', 'sendfile': '发送文件', 'set_content_length': '设内容长度', 'setup_environ': '准备环境', 'start_response': '开始响应'}, {'add_cgi_vars': '加CGI变量', 'cleanup_headers': '清理头部', 'client_is_modern': '客户端是现代的吗', 'error_output': '错误输出', 'finish_content': '结束内容', 'finish_response': '结束响应', 'get_scheme': '取协议', 'get_stderr': '取标准错误', 'get_stdin': '取标准输入', 'handle_error': '处理错误', 'log_exception': '记录异常', 'result_is_file': '结果是文件吗', 'run': '运行', 'send_headers': '发送头部', 'send_preamble': '发送前导', 'sendfile': '发送文件', 'set_content_length': '设内容长度', 'setup_environ': '准备环境', 'start_response': '开始响应'})

class 简单处理器(基础处理器):
    """Handler that's just initialized with streams, environment, etc.

    This handler subclass is intended for synchronous HTTP/1.0 origin servers,
    and handles sending the entire response output, given the correct inputs.

    Usage::

        handler = SimpleHandler(
            inp,out,err,env, multithread=False, multiprocess=True
        )
        handler.run(app)"""

    def __init__(self, stdin, stdout, stderr, environ, multithread=True, multiprocess=False):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.base_env = environ
        self.wsgi_multithread = multithread
        self.wsgi_multiprocess = multiprocess

    def 取标准输入(self):
        return self.stdin

    def 取标准错误(self):
        return self.stderr

    def 加CGI变量(self):
        self.environ.update(self.base_env)

    def _write(self, data):
        result = self.stdout.write(data)
        if result is None or result == len(data):
            return
        from warnings import warn
        warn('SimpleHandler.stdout.write() should not do partial writes', DeprecationWarning)
        while (data := data[result:]):
            result = self.stdout.write(data)

    def _flush(self):
        self.stdout.flush()
        self._flush = self.stdout.flush
_装类转发(简单处理器, {'add_cgi_vars': '加CGI变量', 'get_stderr': '取标准错误', 'get_stdin': '取标准输入'}, {'add_cgi_vars': '加CGI变量', 'get_stderr': '取标准错误', 'get_stdin': '取标准输入'})

class 基础CGI处理器(简单处理器):
    """CGI-like systems using input/output/error streams and environ mapping

    Usage::

        handler = BaseCGIHandler(inp,out,err,env)
        handler.run(app)

    This handler class is useful for gateway protocols like ReadyExec and
    FastCGI, that have usable input/output/error streams and an environment
    mapping.  It's also the base class for CGIHandler, which just uses
    sys.stdin, os.environ, and so on.

    The constructor also takes keyword arguments 'multithread' and
    'multiprocess' (defaulting to 'True' and 'False' respectively) to control
    the configuration sent to the application.  It sets 'origin_server' to
    False (to enable CGI-like output), and assumes that 'wsgi.run_once' is
    False.
    """
    origin_server = False

class CGI处理器(基础CGI处理器):
    """CGI-based invocation via sys.stdin/stdout/stderr and os.environ

    Usage::

        CGIHandler().run(app)

    The difference between this class and BaseCGIHandler is that it always
    uses 'wsgi.run_once' of 'True', 'wsgi.multithread' of 'False', and
    'wsgi.multiprocess' of 'True'.  It does not take any initialization
    parameters, but always uses 'sys.stdin', 'os.environ', and friends.

    If you need to override any of these parameters, use BaseCGIHandler
    instead.
    """
    wsgi_run_once = True
    os_environ = {}

    def __init__(self):
        基础CGI处理器.__init__(self, sys.stdin.buffer, sys.stdout.buffer, sys.stderr, 读环境变量(), multithread=False, multiprocess=True)

class IIS的CGI处理器(基础CGI处理器):
    """CGI-based invocation with workaround for IIS path bug

    This handler should be used in preference to CGIHandler when deploying on
    Microsoft IIS without having set the config allowPathInfo option (IIS>=7)
    or metabase allowPathInfoForScriptMappings (IIS<7).
    """
    wsgi_run_once = True
    os_environ = {}

    def __init__(self):
        environ = 读环境变量()
        path = environ.get('PATH_INFO', '')
        script = environ.get('SCRIPT_NAME', '')
        if (path + '/').startswith(script + '/'):
            environ['PATH_INFO'] = path[len(script):]
        基础CGI处理器.__init__(self, sys.stdin.buffer, sys.stdout.buffer, sys.stderr, environ, multithread=False, multiprocess=True)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseCGIHandler': '基础CGI处理器',
    'BaseHandler': '基础处理器',
    'CGIHandler': 'CGI处理器',
    'IISCGIHandler': 'IIS的CGI处理器',
    'SimpleHandler': '简单处理器',
    'format_date_time': '格式化日期时间',
    'read_environ': '读环境变量',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '基础处理器': {
        'add_cgi_vars': '加CGI变量',
        'cleanup_headers': '清理头部',
        'client_is_modern': '客户端是现代的吗',
        'error_output': '错误输出',
        'finish_content': '结束内容',
        'finish_response': '结束响应',
        'get_scheme': '取协议',
        'get_stderr': '取标准错误',
        'get_stdin': '取标准输入',
        'handle_error': '处理错误',
        'log_exception': '记录异常',
        'result_is_file': '结果是文件吗',
        'run': '运行',
        'send_headers': '发送头部',
        'send_preamble': '发送前导',
        'sendfile': '发送文件',
        'set_content_length': '设内容长度',
        'setup_environ': '准备环境',
        'start_response': '开始响应',
    },
    '简单处理器': {
        'add_cgi_vars': '加CGI变量',
        'get_stderr': '取标准错误',
        'get_stdin': '取标准输入',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '基础处理器': {
        'add_cgi_vars': '加CGI变量',
        'cleanup_headers': '清理头部',
        'client_is_modern': '客户端是现代的吗',
        'error_output': '错误输出',
        'finish_content': '结束内容',
        'finish_response': '结束响应',
        'get_scheme': '取协议',
        'get_stderr': '取标准错误',
        'get_stdin': '取标准输入',
        'handle_error': '处理错误',
        'log_exception': '记录异常',
        'result_is_file': '结果是文件吗',
        'run': '运行',
        'send_headers': '发送头部',
        'send_preamble': '发送前导',
        'sendfile': '发送文件',
        'set_content_length': '设内容长度',
        'setup_environ': '准备环境',
        'start_response': '开始响应',
    },
    '简单处理器': {
        'add_cgi_vars': '加CGI变量',
        'get_stderr': '取标准错误',
        'get_stdin': '取标准输入',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'CGI处理器',
    'IIS的CGI处理器',
    '基础CGI处理器',
    '基础处理器',
    '简单处理器',
    '读环境变量',
]

# ---- 转发层结束 ----
