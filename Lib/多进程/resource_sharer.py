# -*- coding: utf-8 -*-
"""多进程.resource_sharer —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/resource_sharer.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.resource_sharer.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


import os
import signal
import socket
import sys
import threading
from . import process
from .context import reduction
from . import util
__all__ = ['stop']
if sys.platform == 'win32':
    __all__ += ['DupSocket']

    class DupSocket(object):
        """Picklable wrapper for a socket."""

        def __init__(self, sock):
            new_sock = sock.dup()

            def send(conn, pid):
                share = new_sock.share(pid)
                conn.send_bytes(share)
            self._id = _resource_sharer.register(send, new_sock.close)

        def detach(self):
            """Get the socket.  This should only be called once."""
            with _resource_sharer.get_connection(self._id) as conn:
                share = conn.recv_bytes()
                return socket.fromshare(share)
else:
    __all__ += ['DupFd']

    class DupFd(object):
        """Wrapper for fd which can be used at any time."""

        def __init__(self, fd):
            new_fd = os.dup(fd)

            def send(conn, pid):
                reduction.send_handle(conn, new_fd, pid)

            def close():
                os.close(new_fd)
            self._id = _resource_sharer.register(send, close)

        def detach(self):
            """Get the fd.  This should only be called once."""
            with _resource_sharer.get_connection(self._id) as conn:
                return reduction.recv_handle(conn)

class _ResourceSharer(object):
    """Manager for resources using background thread."""

    def __init__(self):
        self._key = 0
        self._cache = {}
        self._lock = threading.Lock()
        self._listener = None
        self._address = None
        self._thread = None
        util.register_after_fork(self, _ResourceSharer._afterfork)

    def register(self, send, close):
        """Register resource, returning an identifier."""
        with self._lock:
            if self._address is None:
                self._start()
            self._key += 1
            self._cache[self._key] = (send, close)
            return (self._address, self._key)

    @staticmethod
    def get_connection(ident):
        """Return connection from which to receive identified resource."""
        from .connection import Client
        address, key = ident
        c = Client(address, authkey=process.current_process().authkey)
        c.send((key, os.getpid()))
        return c

    def stop(self, timeout=None):
        """Stop the background thread and clear registered resources."""
        from .connection import Client
        with self._lock:
            if self._address is not None:
                c = Client(self._address, authkey=process.current_process().authkey)
                c.send(None)
                c.close()
                self._thread.join(timeout)
                if self._thread.is_alive():
                    util.sub_warning('_ResourceSharer thread did not stop when asked')
                self._listener.close()
                self._thread = None
                self._address = None
                self._listener = None
                for key, (send, close) in self._cache.items():
                    close()
                self._cache.clear()

    def _afterfork(self):
        for key, (send, close) in self._cache.items():
            close()
        self._cache.clear()
        self._lock._at_fork_reinit()
        if self._listener is not None:
            self._listener.close()
        self._listener = None
        self._address = None
        self._thread = None

    def _start(self):
        from .connection import Listener
        assert self._listener is None, 'Already have Listener'
        util.debug('starting listener and thread for sending handles')
        self._listener = Listener(authkey=process.current_process().authkey, backlog=128)
        self._address = self._listener.address
        t = threading.Thread(target=self._serve)
        t.daemon = True
        t.start()
        self._thread = t

    def _serve(self):
        if hasattr(signal, 'pthread_sigmask'):
            signal.pthread_sigmask(signal.SIG_BLOCK, signal.valid_signals())
        while 1:
            try:
                with self._listener.accept() as conn:
                    msg = conn.recv()
                    if msg is None:
                        break
                    key, destination_pid = msg
                    send, close = self._cache.pop(key)
                    try:
                        send(conn, destination_pid)
                    finally:
                        close()
            except:
                if not util.is_exiting():
                    sys.excepthook(*sys.exc_info())
_resource_sharer = _ResourceSharer()
stop = _resource_sharer.stop


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
