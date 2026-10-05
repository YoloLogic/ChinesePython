# -*- coding: utf-8 -*-
"""套接字服务器 —— 汉语库（由 tools/汉化库.py 从 Lib/socketserver.py 机械生成，**不要手改**）。

英文库 Lib/socketserver.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 套接字服务器
"""


"""Generic socket server classes.

This module tries to capture the various aspects of defining a server:

For socket-based servers:

- address family:
        - AF_INET{,6}: IP (Internet Protocol) sockets (default)
        - AF_UNIX: Unix domain sockets
        - others, e.g. AF_DECNET are conceivable (see <socket.h>
- socket type:
        - SOCK_STREAM (reliable stream, e.g. TCP)
        - SOCK_DGRAM (datagrams, e.g. UDP)

For request-based servers (including socket-based):

- client address verification before further looking at the request
        (This is actually a hook for any processing that needs to look
         at the request before anything else, e.g. logging)
- how to handle multiple requests:
        - synchronous (one request is handled at a time)
        - forking (each request is handled by a new process)
        - threading (each request is handled by a new thread)

The classes in this module favor the server type that is simplest to
write: a synchronous TCP/IP server.  This is bad class design, but
saves some typing.  (There's also the issue that a deep class hierarchy
slows down method lookups.)

There are five classes in an inheritance diagram, four of which represent
synchronous servers of four types:

        +------------+
        | BaseServer |
        +------------+
              |
              v
        +-----------+        +------------------+
        | TCPServer |------->| UnixStreamServer |
        +-----------+        +------------------+
              |
              v
        +-----------+        +--------------------+
        | UDPServer |------->| UnixDatagramServer |
        +-----------+        +--------------------+

Note that UnixDatagramServer derives from UDPServer, not from
UnixStreamServer -- the only difference between an IP and a Unix
stream server is the address family, which is simply repeated in both
unix server classes.

Forking and threading versions of each type of server can be created
using the ForkingMixIn and ThreadingMixIn mix-in classes.  For
instance, a threading UDP server class is created as follows:

        class ThreadingUDPServer(ThreadingMixIn, UDPServer): pass

The Mix-in class must come first, since it overrides a method defined
in UDPServer! Setting the various member variables also changes
the behavior of the underlying server mechanism.

To implement a service, you must derive a class from
BaseRequestHandler and redefine its handle() method.  You can then run
various versions of the service by combining one of the server classes
with your request handler class.

The request handler class must be different for datagram or stream
services.  This can be hidden by using the request handler
subclasses StreamRequestHandler or DatagramRequestHandler.

Of course, you still have to use your head!

For instance, it makes no sense to use a forking server if the service
contains state in memory that can be modified by requests (since the
modifications in the child process would never reach the initial state
kept in the parent process and passed to each child).  In this case,
you can use a threading server, but you will probably have to use
locks to avoid two requests that come in nearly simultaneous to apply
conflicting changes to the server state.

On the other hand, if you are building e.g. an HTTP server, where all
data is stored externally (e.g. in the file system), a synchronous
class will essentially render the service "deaf" while one request is
being handled -- which may be for a very long time if a client is slow
to read all the data it has requested.  Here a threading or forking
server is appropriate.

In some cases, it may be appropriate to process part of a request
synchronously, but to finish processing in a forked child depending on
the request data.  This can be implemented by using a synchronous
server and doing an explicit fork in the request handler class
handle() method.

Another approach to handling multiple simultaneous requests in an
environment that supports neither threads nor fork (or where these are
too expensive or inappropriate for the service) is to maintain an
explicit table of partially finished requests and to use a selector to
decide which request to work on next (or whether to handle a new
incoming request).  This is particularly important for stream services
where each client can potentially be connected for a long time (if
threads or subprocesses cannot be used).

Future work:
- Standard classes for Sun RPC (which uses either UDP or TCP)
- Standard mix-in classes to implement various authentication
  and encryption schemes

XXX Open problems:
- What to do with out-of-band data?

BaseServer:
- split generic "request" functionality out into BaseServer class.
  Copyright (C) 2000  Luke Kenneth Casson Leighton <lkcl@samba.org>

  example: read entries from a SQL database (requires overriding
  get_request() to return a table entry from the database).
  entry is processed by a RequestHandlerClass.

"""
_英文原名表 = {'BaseRequestHandler': '请求处理基类', 'BaseServer': '基础服务器', 'DatagramRequestHandler': '数据报请求处理器', 'ForkingMixIn': '多进程混入', 'ForkingTCPServer': '多进程TCP服务器', 'ForkingUDPServer': '多进程UDP服务器', 'ForkingUnixDatagramServer': '多进程Unix数据报服务器', 'ForkingUnixStreamServer': '多进程Unix流服务器', 'StreamRequestHandler': '流请求处理器', 'TCPServer': 'TCP服务器', 'ThreadingMixIn': '多线程混入', 'ThreadingTCPServer': '多线程TCP服务器', 'ThreadingUDPServer': '多线程UDP服务器', 'ThreadingUnixDatagramServer': '多线程Unix数据报服务器', 'ThreadingUnixStreamServer': '多线程Unix流服务器', 'UDPServer': 'UDP服务器', 'UnixDatagramServer': 'Unix数据报服务器', 'UnixStreamServer': 'Unix流服务器'}

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
__version__ = '0.4'
import socket
import selectors
import os
import sys
import threading
from io import BufferedIOBase
from time import monotonic as time
__all__ = ['BaseServer', 'TCPServer', 'UDPServer', 'ThreadingUDPServer', 'ThreadingTCPServer', 'BaseRequestHandler', 'StreamRequestHandler', 'DatagramRequestHandler', 'ThreadingMixIn']
if hasattr(os, 'fork'):
    __all__.extend(['ForkingUDPServer', 'ForkingTCPServer', 'ForkingMixIn'])
if hasattr(socket, 'AF_UNIX'):
    __all__.extend(['UnixStreamServer', 'UnixDatagramServer', 'ThreadingUnixStreamServer', 'ThreadingUnixDatagramServer'])
    if hasattr(os, 'fork'):
        __all__.extend(['ForkingUnixStreamServer', 'ForkingUnixDatagramServer'])
if hasattr(selectors, 'PollSelector'):
    _ServerSelector = selectors.PollSelector
else:
    _ServerSelector = selectors.SelectSelector

class 基础服务器:
    """Base class for server classes.

    Methods for the caller:

    - __init__(server_address, RequestHandlerClass)
    - serve_forever(poll_interval=0.5)
    - shutdown()
    - handle_request()  # if you do not use serve_forever()
    - fileno() -> int   # for selector

    Methods that may be overridden:

    - server_bind()
    - server_activate()
    - get_request() -> request, client_address
    - handle_timeout()
    - verify_request(request, client_address)
    - server_close()
    - process_request(request, client_address)
    - shutdown_request(request)
    - close_request(request)
    - service_actions()
    - handle_error()

    Methods for derived classes:

    - finish_request(request, client_address)

    Class variables that may be overridden by derived classes or
    instances:

    - timeout
    - address_family
    - socket_type
    - allow_reuse_address
    - allow_reuse_port

    Instance variables:

    - RequestHandlerClass
    - socket

    """
    timeout = None

    def __init__(self, server_address, RequestHandlerClass):
        """Constructor.  May be extended, do not override."""
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass
        self.__is_shut_down = threading.Event()
        self.__shutdown_request = False

    def 激活服务器(self):
        """Called by constructor to activate the server.

        May be overridden.

        """
        pass

    def 永久服务(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

        Polls for shutdown every poll_interval seconds. Ignores
        self.timeout. If you need to do periodic tasks, do them in
        another thread.
        """
        self.__is_shut_down.clear()
        try:
            with _ServerSelector() as selector:
                selector.register(self, selectors.EVENT_READ)
                while not self.__shutdown_request:
                    ready = selector.select(poll_interval)
                    if self.__shutdown_request:
                        break
                    if ready:
                        self._handle_request_noblock()
                    self.服务轮转动作()
        finally:
            self.__shutdown_request = False
            self.__is_shut_down.set()

    def 关闭服务(self):
        """Stops the serve_forever loop.

        Blocks until the loop has finished. This must be called while
        serve_forever() is running in another thread, or it will
        deadlock.
        """
        self.__shutdown_request = True
        self.__is_shut_down.wait()

    def 服务轮转动作(self):
        """Called by the serve_forever() loop.

        May be overridden by a subclass / Mixin to implement any code that
        needs to be run during the loop.
        """
        pass

    def 处理一次请求(self):
        """Handle one request, possibly blocking.

        Respects self.timeout.
        """
        timeout = self.socket.gettimeout()
        if timeout is None:
            timeout = self.timeout
        elif self.timeout is not None:
            timeout = min(timeout, self.timeout)
        if timeout is not None:
            deadline = time() + timeout
        with _ServerSelector() as selector:
            selector.register(self, selectors.EVENT_READ)
            while True:
                if selector.select(timeout):
                    return self._handle_request_noblock()
                elif timeout is not None:
                    timeout = deadline - time()
                    if timeout < 0:
                        return self.处理超时()

    def _handle_request_noblock(self):
        """Handle one request, without blocking.

        I assume that selector.select() has returned that the socket is
        readable before this function was called, so there should be no risk of
        blocking in get_request().
        """
        try:
            request, client_address = self.取请求()
        except OSError:
            return
        if self.verify_request(request, client_address):
            try:
                self.处理请求(request, client_address)
            except Exception:
                self.handle_error(request, client_address)
                self.shutdown_request(request)
            except:
                self.shutdown_request(request)
                raise
        else:
            self.shutdown_request(request)

    def 处理超时(self):
        """Called if no new request arrives within self.timeout.

        Overridden by ForkingMixIn.
        """
        pass

    def verify_request(self, request, client_address):
        """Verify the request.  May be overridden.

        Return True if we should proceed with this request.

        """
        return True

    def 处理请求(self, request, client_address):
        """Call finish_request.

        Overridden by ForkingMixIn and ThreadingMixIn.

        """
        self.完成请求(request, client_address)
        self.shutdown_request(request)

    def 关闭服务器(self):
        """Called to clean-up the server.

        May be overridden.

        """
        pass

    def 完成请求(self, request, client_address):
        """Finish one request by instantiating RequestHandlerClass."""
        self.RequestHandlerClass(request, client_address, self)

    def shutdown_request(self, request):
        """Called to shutdown and close an individual request."""
        self.结束请求(request)

    def 结束请求(self, request):
        """Called to clean up an individual request."""
        pass

    def handle_error(self, request, client_address):
        """Handle an error gracefully.  May be overridden.

        The default is to print a traceback and continue.

        """
        print('-' * 40, file=sys.stderr)
        print('Exception occurred during processing of request from', client_address, file=sys.stderr)
        import traceback
        traceback.print_exc()
        print('-' * 40, file=sys.stderr)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.关闭服务器()
_装类转发(基础服务器, {'close_request': '结束请求', 'finish_request': '完成请求', 'handle_request': '处理一次请求', 'handle_timeout': '处理超时', 'process_request': '处理请求', 'serve_forever': '永久服务', 'server_activate': '激活服务器', 'server_close': '关闭服务器', 'service_actions': '服务轮转动作', 'shutdown': '关闭服务'}, {'close_request': '结束请求', 'finish_request': '完成请求', 'get_request': '取请求', 'handle_request': '处理一次请求', 'handle_timeout': '处理超时', 'process_request': '处理请求', 'serve_forever': '永久服务', 'server_activate': '激活服务器', 'server_close': '关闭服务器', 'service_actions': '服务轮转动作', 'shutdown': '关闭服务'})

class TCP服务器(基础服务器):
    """Base class for various socket-based server classes.

    Defaults to synchronous IP stream (i.e., TCP).

    Methods for the caller:

    - __init__(server_address, RequestHandlerClass, bind_and_activate=True)
    - serve_forever(poll_interval=0.5)
    - shutdown()
    - handle_request()  # if you don't use serve_forever()
    - fileno() -> int   # for selector

    Methods that may be overridden:

    - server_bind()
    - server_activate()
    - get_request() -> request, client_address
    - handle_timeout()
    - verify_request(request, client_address)
    - process_request(request, client_address)
    - shutdown_request(request)
    - close_request(request)
    - handle_error()

    Methods for derived classes:

    - finish_request(request, client_address)

    Class variables that may be overridden by derived classes or
    instances:

    - timeout
    - address_family
    - socket_type
    - request_queue_size (only for stream sockets)
    - allow_reuse_address
    - allow_reuse_port

    Instance variables:

    - server_address
    - RequestHandlerClass
    - socket

    """
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    allow_reuse_address = False
    allow_reuse_port = False

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        """Constructor.  May be extended, do not override."""
        基础服务器.__init__(self, server_address, RequestHandlerClass)
        self.socket = socket.socket(self.address_family, self.socket_type)
        if bind_and_activate:
            try:
                self.server_bind()
                self.激活服务器()
            except:
                self.关闭服务器()
                raise

    def server_bind(self):
        """Called by constructor to bind the socket.

        May be overridden.

        """
        if self.allow_reuse_address and hasattr(socket, 'SO_REUSEADDR'):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.allow_reuse_port and hasattr(socket, 'SO_REUSEPORT') and (self.address_family in (socket.AF_INET, socket.AF_INET6)):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

    def 激活服务器(self):
        """Called by constructor to activate the server.

        May be overridden.

        """
        self.socket.listen(self.request_queue_size)

    def 关闭服务器(self):
        """Called to clean-up the server.

        May be overridden.

        """
        self.socket.close()

    def fileno(self):
        """Return socket file number.

        Interface required by selector.

        """
        return self.socket.fileno()

    def 取请求(self):
        """Get the request and client address from the socket.

        May be overridden.

        """
        return self.socket.accept()

    def shutdown_request(self, request):
        """Called to shutdown and close an individual request."""
        try:
            request.shutdown(socket.SHUT_WR)
        except OSError:
            pass
        self.结束请求(request)

    def 结束请求(self, request):
        """Called to clean up an individual request."""
        request.close()
_装类转发(TCP服务器, {'close_request': '结束请求', 'get_request': '取请求', 'server_activate': '激活服务器', 'server_close': '关闭服务器'}, {'close_request': '结束请求', 'get_request': '取请求', 'server_activate': '激活服务器', 'server_close': '关闭服务器'})

class UDP服务器(TCP服务器):
    """UDP server class."""
    allow_reuse_address = False
    allow_reuse_port = False
    socket_type = socket.SOCK_DGRAM
    max_packet_size = 8192

    def 取请求(self):
        data, client_addr = self.socket.recvfrom(self.max_packet_size)
        return ((data, self.socket), client_addr)

    def 激活服务器(self):
        pass

    def shutdown_request(self, request):
        self.结束请求(request)

    def 结束请求(self, request):
        pass
_装类转发(UDP服务器, {'close_request': '结束请求', 'get_request': '取请求', 'server_activate': '激活服务器'}, {'close_request': '结束请求', 'get_request': '取请求', 'server_activate': '激活服务器'})
if hasattr(os, 'fork'):

    class 多进程混入:
        """Mix-in class to handle each request in a new process."""
        timeout = 300
        active_children = None
        max_children = 40
        block_on_close = True

        def 收集子进程(self, *, blocking=False):
            """Internal routine to wait for children that have exited."""
            if self.active_children is None:
                return
            while len(self.active_children) >= self.max_children:
                try:
                    pid, _ = os.waitpid(-1, 0)
                    self.active_children.discard(pid)
                except ChildProcessError:
                    self.active_children.clear()
                except OSError:
                    break
            for pid in self.active_children.copy():
                try:
                    flags = 0 if blocking else os.WNOHANG
                    pid, _ = os.waitpid(pid, flags)
                    self.active_children.discard(pid)
                except ChildProcessError:
                    self.active_children.discard(pid)
                except OSError:
                    pass

        def 处理超时(self):
            """Wait for zombies after self.timeout seconds of inactivity.

            May be extended, do not override.
            """
            self.收集子进程()

        def 服务轮转动作(self):
            """Collect the zombie child processes regularly in the ForkingMixIn.

            service_actions is called in the BaseServer's serve_forever loop.
            """
            self.收集子进程()

        def 处理请求(self, request, client_address):
            """Fork a new subprocess to process the request."""
            pid = os.fork()
            if pid:
                if self.active_children is None:
                    self.active_children = set()
                self.active_children.add(pid)
                self.结束请求(request)
                return
            else:
                status = 1
                try:
                    self.完成请求(request, client_address)
                    status = 0
                except Exception:
                    self.handle_error(request, client_address)
                finally:
                    try:
                        self.shutdown_request(request)
                    finally:
                        os._exit(status)

        def 关闭服务器(self):
            super().server_close()
            self.收集子进程(blocking=self.block_on_close)
    _装类转发(多进程混入, {'collect_children': '收集子进程', 'handle_timeout': '处理超时', 'process_request': '处理请求', 'server_close': '关闭服务器', 'service_actions': '服务轮转动作'}, {'close_request': '结束请求', 'collect_children': '收集子进程', 'finish_request': '完成请求', 'handle_timeout': '处理超时', 'process_request': '处理请求', 'server_close': '关闭服务器', 'service_actions': '服务轮转动作'})

class _Threads(list):
    """
    Joinable list of all non-daemon threads.
    """

    def append(self, thread):
        self.reap()
        if thread.daemon:
            return
        super().append(thread)

    def pop_all(self):
        self[:], result = ([], self[:])
        return result

    def join(self):
        for thread in self.pop_all():
            thread.join()

    def reap(self):
        self[:] = (thread for thread in self if thread.is_alive())

class _NoThreads:
    """
    Degenerate version of _Threads.
    """

    def append(self, thread):
        pass

    def join(self):
        pass

class 多线程混入:
    """Mix-in class to handle each request in a new thread."""
    daemon_threads = False
    block_on_close = True
    _threads = _NoThreads()

    def 线程里处理请求(self, request, client_address):
        """Same as in BaseServer but as a thread.

        In addition, exception handling is done here.

        """
        try:
            self.完成请求(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)

    def 处理请求(self, request, client_address):
        """Start a new thread to process the request."""
        if self.block_on_close:
            vars(self).setdefault('_threads', _Threads())
        t = threading.Thread(target=self.线程里处理请求, args=(request, client_address))
        t.daemon = self.daemon_threads
        self._threads.append(t)
        t.start()

    def 关闭服务器(self):
        super().server_close()
        self._threads.join()
_装类转发(多线程混入, {'process_request': '处理请求', 'process_request_thread': '线程里处理请求', 'server_close': '关闭服务器'}, {'finish_request': '完成请求', 'process_request': '处理请求', 'process_request_thread': '线程里处理请求', 'server_close': '关闭服务器'})
if hasattr(os, 'fork'):

    class 多进程UDP服务器(多进程混入, UDP服务器):
        pass

    class 多进程TCP服务器(多进程混入, TCP服务器):
        pass

class 多线程UDP服务器(多线程混入, UDP服务器):
    pass

class 多线程TCP服务器(多线程混入, TCP服务器):
    pass
if hasattr(socket, 'AF_UNIX'):

    class Unix流服务器(TCP服务器):
        address_family = socket.AF_UNIX

    class Unix数据报服务器(UDP服务器):
        address_family = socket.AF_UNIX

    class 多线程Unix流服务器(多线程混入, Unix流服务器):
        pass

    class 多线程Unix数据报服务器(多线程混入, Unix数据报服务器):
        pass
    if hasattr(os, 'fork'):

        class 多进程Unix流服务器(多进程混入, Unix流服务器):
            pass

        class 多进程Unix数据报服务器(多进程混入, Unix数据报服务器):
            pass

class 请求处理基类:
    """Base class for request handler classes.

    This class is instantiated for each request to be handled.  The
    constructor sets the instance variables request, client_address
    and server, and then calls the handle() method.  To implement a
    specific service, all you need to do is to derive a class which
    defines a handle() method.

    The handle() method can find the request as self.request, the
    client address as self.client_address, and the server (in case it
    needs access to per-server information) as self.server.  Since a
    separate instance is created for each request, the handle() method
    can define other arbitrary instance variables.

    """

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        pass

    def handle(self):
        pass

    def finish(self):
        pass

class 流请求处理器(请求处理基类):
    """Define self.rfile and self.wfile for stream sockets."""
    rbufsize = -1
    wbufsize = 0
    timeout = None
    disable_nagle_algorithm = False

    def setup(self):
        self.connection = self.request
        if self.timeout is not None:
            self.connection.settimeout(self.timeout)
        if self.disable_nagle_algorithm:
            self.connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, True)
        self.rfile = self.connection.makefile('rb', self.rbufsize)
        if self.wbufsize == 0:
            self.wfile = _SocketWriter(self.connection)
        else:
            self.wfile = self.connection.makefile('wb', self.wbufsize)

    def finish(self):
        if not self.wfile.closed:
            try:
                self.wfile.flush()
            except socket.error:
                pass
        self.wfile.close()
        self.rfile.close()

class _SocketWriter(BufferedIOBase):
    """Simple writable BufferedIOBase implementation for a socket

    Does not hold data in a buffer, avoiding any need to call flush()."""

    def __init__(self, sock):
        self._sock = sock

    def writable(self):
        return True

    def write(self, b):
        self._sock.sendall(b)
        with memoryview(b) as view:
            return view.nbytes

    def fileno(self):
        return self._sock.fileno()

class 数据报请求处理器(请求处理基类):
    """Define self.rfile and self.wfile for datagram sockets."""

    def setup(self):
        from io import BytesIO
        self.packet, self.socket = self.request
        self.rfile = BytesIO(self.packet)
        self.wfile = BytesIO()

    def finish(self):
        self.socket.sendto(self.wfile.getvalue(), self.client_address)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseRequestHandler': '请求处理基类',
    'BaseServer': '基础服务器',
    'DatagramRequestHandler': '数据报请求处理器',
    'ForkingMixIn': '多进程混入',
    'ForkingTCPServer': '多进程TCP服务器',
    'ForkingUDPServer': '多进程UDP服务器',
    'ForkingUnixDatagramServer': '多进程Unix数据报服务器',
    'ForkingUnixStreamServer': '多进程Unix流服务器',
    'StreamRequestHandler': '流请求处理器',
    'TCPServer': 'TCP服务器',
    'ThreadingMixIn': '多线程混入',
    'ThreadingTCPServer': '多线程TCP服务器',
    'ThreadingUDPServer': '多线程UDP服务器',
    'ThreadingUnixDatagramServer': '多线程Unix数据报服务器',
    'ThreadingUnixStreamServer': '多线程Unix流服务器',
    'UDPServer': 'UDP服务器',
    'UnixDatagramServer': 'Unix数据报服务器',
    'UnixStreamServer': 'Unix流服务器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'TCP服务器': {
        'close_request': '结束请求',
        'get_request': '取请求',
        'server_activate': '激活服务器',
        'server_close': '关闭服务器',
    },
    'UDP服务器': {
        'close_request': '结束请求',
        'get_request': '取请求',
        'server_activate': '激活服务器',
    },
    '基础服务器': {
        'close_request': '结束请求',
        'finish_request': '完成请求',
        'handle_request': '处理一次请求',
        'handle_timeout': '处理超时',
        'process_request': '处理请求',
        'serve_forever': '永久服务',
        'server_activate': '激活服务器',
        'server_close': '关闭服务器',
        'service_actions': '服务轮转动作',
        'shutdown': '关闭服务',
    },
    '多线程混入': {
        'process_request': '处理请求',
        'process_request_thread': '线程里处理请求',
        'server_close': '关闭服务器',
    },
    '多进程混入': {
        'collect_children': '收集子进程',
        'handle_timeout': '处理超时',
        'process_request': '处理请求',
        'server_close': '关闭服务器',
        'service_actions': '服务轮转动作',
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
    'TCP服务器': {
        'close_request': '结束请求',
        'get_request': '取请求',
        'server_activate': '激活服务器',
        'server_close': '关闭服务器',
    },
    'UDP服务器': {
        'close_request': '结束请求',
        'get_request': '取请求',
        'server_activate': '激活服务器',
    },
    '基础服务器': {
        'close_request': '结束请求',
        'finish_request': '完成请求',
        'get_request': '取请求',
        'handle_request': '处理一次请求',
        'handle_timeout': '处理超时',
        'process_request': '处理请求',
        'serve_forever': '永久服务',
        'server_activate': '激活服务器',
        'server_close': '关闭服务器',
        'service_actions': '服务轮转动作',
        'shutdown': '关闭服务',
    },
    '多线程混入': {
        'finish_request': '完成请求',
        'process_request': '处理请求',
        'process_request_thread': '线程里处理请求',
        'server_close': '关闭服务器',
    },
    '多进程混入': {
        'close_request': '结束请求',
        'collect_children': '收集子进程',
        'finish_request': '完成请求',
        'handle_timeout': '处理超时',
        'process_request': '处理请求',
        'server_close': '关闭服务器',
        'service_actions': '服务轮转动作',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'TCP服务器',
    'UDP服务器',
    'Unix数据报服务器',
    'Unix流服务器',
    '基础服务器',
    '多线程TCP服务器',
    '多线程UDP服务器',
    '多线程Unix数据报服务器',
    '多线程Unix流服务器',
    '多线程混入',
    '多进程TCP服务器',
    '多进程UDP服务器',
    '多进程Unix数据报服务器',
    '多进程Unix流服务器',
    '多进程混入',
    '数据报请求处理器',
    '流请求处理器',
    '请求处理基类',
]

# ---- 转发层结束 ----
