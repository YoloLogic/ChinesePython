# -*- coding: utf-8 -*-
"""WSGI参考.简单服务器 —— 汉语库（由 tools/汉化库.py 从 Lib/wsgiref/simple_server.py 机械生成，**不要手改**）。

英文库 Lib/wsgiref.simple_server.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py wsgiref
"""


"""BaseHTTPServer that implements the Python WSGI protocol (PEP 3333)

This is both an example of how WSGI can be implemented, and a basis for running
simple web applications on a local machine, such as might be done when testing
or debugging an application.  It has not been reviewed for security issues,
however, and we strongly recommend that you use a "real" web server for
production use.

For example usage, see the 'if __name__=="__main__"' block at the end of the
module.  See also the BaseHTTPServer module docs for other API information.
"""
_英文原名表 = {'ServerHandler': '服务器处理器', 'WSGIRequestHandler': 'WSGI请求处理器', 'WSGIServer': 'WSGI服务器', 'demo_app': '演示应用', 'make_server': '造服务器', 'server_version': '服务器版本', 'software_version': '软件版本', 'sys_version': '系统版本'}

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
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import urllib.parse
from WSGI参考.处理器 import SimpleHandler
from platform import python_implementation
__version__ = '0.2'
__all__ = ['WSGIServer', 'WSGIRequestHandler', 'demo_app', 'make_server']
服务器版本 = 'WSGIServer/' + __version__
系统版本 = python_implementation() + '/' + sys.version.split()[0]
软件版本 = 服务器版本 + ' ' + 系统版本

class 服务器处理器(SimpleHandler):
    server_software = 软件版本

    def close(self):
        try:
            self.request_handler.log_request(self.status.split(' ', 1)[0], self.bytes_sent)
        finally:
            SimpleHandler.close(self)

class WSGI服务器(HTTPServer):
    """BaseHTTPServer that implements the Python WSGI protocol"""
    application = None

    def server_bind(self):
        """Override server_bind to store the server name."""
        HTTPServer.server_bind(self)
        self.准备环境()

    def 准备环境(self):
        env = self.base_environ = {}
        env['SERVER_NAME'] = self.server_name
        env['GATEWAY_INTERFACE'] = 'CGI/1.1'
        env['SERVER_PORT'] = str(self.server_port)
        env['REMOTE_HOST'] = ''
        env['CONTENT_LENGTH'] = ''
        env['SCRIPT_NAME'] = ''

    def 取应用(self):
        return self.application

    def 设应用(self, application):
        self.application = application
_装类转发(WSGI服务器, {'get_app': '取应用', 'set_app': '设应用', 'setup_environ': '准备环境'}, {'get_app': '取应用', 'set_app': '设应用', 'setup_environ': '准备环境'})

class WSGI请求处理器(BaseHTTPRequestHandler):
    服务器版本 = 'WSGIServer/' + __version__

    def 取环境(self):
        env = self.server.base_environ.copy()
        env['SERVER_PROTOCOL'] = self.request_version
        env['SERVER_SOFTWARE'] = self.服务器版本
        env['REQUEST_METHOD'] = self.command
        if '?' in self.path:
            path, query = self.path.split('?', 1)
        else:
            path, query = (self.path, '')
        env['PATH_INFO'] = urllib.parse.unquote(path, 'iso-8859-1')
        env['QUERY_STRING'] = query
        env['REMOTE_ADDR'] = self.client_address[0]
        if self.headers.get('content-type') is None:
            env['CONTENT_TYPE'] = self.headers.get_content_type()
        else:
            env['CONTENT_TYPE'] = self.headers['content-type']
        length = self.headers.get('content-length')
        if length:
            env['CONTENT_LENGTH'] = length
        for k, v in self.headers.items():
            k = k.replace('-', '_').upper()
            v = v.strip()
            if k in env:
                continue
            if 'HTTP_' + k in env:
                env['HTTP_' + k] += ',' + v
            else:
                env['HTTP_' + k] = v
        return env

    def get_stderr(self):
        return sys.stderr

    def 处理(self):
        """Handle a single HTTP request"""
        self.raw_requestline = self.rfile.readline(65537)
        if len(self.raw_requestline) > 65536:
            self.requestline = ''
            self.request_version = ''
            self.command = ''
            self.send_error(414)
            return
        if not self.parse_request():
            return
        handler = 服务器处理器(self.rfile, self.wfile, self.get_stderr(), self.取环境(), multithread=False)
        handler.request_handler = self
        handler.run(self.server.get_app())
_装类转发(WSGI请求处理器, {'get_environ': '取环境', 'handle': '处理', 'server_version': '服务器版本'}, {'get_environ': '取环境', 'handle': '处理', 'server_version': '服务器版本'})

def 演示应用(environ, start_response):
    from io import StringIO
    stdout = StringIO()
    print('Hello world!', file=stdout)
    print(file=stdout)
    h = sorted(environ.items())
    for k, v in h:
        print(k, '=', repr(v), file=stdout)
    start_response('200 OK', [('Content-Type', 'text/plain; charset=utf-8')])
    return [stdout.getvalue().encode('utf-8')]

def 造服务器(host, port, app, server_class=WSGI服务器, handler_class=WSGI请求处理器):
    """Create a new WSGI server listening on `host` and `port` for `app`"""
    server = server_class((host, port), handler_class)
    server.set_app(app)
    return server
if __name__ == '__main__':
    with 造服务器('', 8000, 演示应用) as httpd:
        sa = httpd.socket.getsockname()
        print('Serving HTTP on', sa[0], 'port', sa[1], '...')
        import webbrowser
        webbrowser.open('http://localhost:8000/xyz?abc')
        httpd.handle_request()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ServerHandler': '服务器处理器',
    'WSGIRequestHandler': 'WSGI请求处理器',
    'WSGIServer': 'WSGI服务器',
    'demo_app': '演示应用',
    'make_server': '造服务器',
    'server_version': '服务器版本',
    'software_version': '软件版本',
    'sys_version': '系统版本',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'WSGI服务器': {
        'get_app': '取应用',
        'set_app': '设应用',
        'setup_environ': '准备环境',
    },
    'WSGI请求处理器': {
        'get_environ': '取环境',
        'handle': '处理',
        'server_version': '服务器版本',
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
    'WSGI服务器': {
        'get_app': '取应用',
        'set_app': '设应用',
        'setup_environ': '准备环境',
    },
    'WSGI请求处理器': {
        'get_environ': '取环境',
        'handle': '处理',
        'server_version': '服务器版本',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'WSGI服务器',
    'WSGI请求处理器',
    '演示应用',
    '造服务器',
]

# ---- 转发层结束 ----
