# -*- coding: utf-8 -*-
"""多进程.forkserver —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/forkserver.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.forkserver.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


import atexit
import errno
import os
import selectors
import signal
import socket
import struct
import sys
import threading
import warnings
from . import AuthenticationError
from . import connection
from . import process
from .context import reduction
from . import resource_tracker
from . import spawn
from . import util
__all__ = ['ensure_running', 'get_inherited_fds', 'connect_to_new_process', 'set_forkserver_preload']
MAXFDS_TO_SEND = 256
SIGNED_STRUCT = struct.Struct('q')
_AUTHKEY_LEN = 32

class ForkServer(object):

    def __init__(self):
        self._forkserver_authkey = None
        self._forkserver_address = None
        self._forkserver_alive_fd = None
        self._forkserver_pid = None
        self._inherited_fds = None
        self._lock = threading.Lock()
        self._preload_modules = ['__main__']

    def _stop(self):
        with self._lock:
            self._stop_unlocked()

    def _stop_unlocked(self):
        if self._forkserver_pid is None:
            return
        os.close(self._forkserver_alive_fd)
        self._forkserver_alive_fd = None
        os.waitpid(self._forkserver_pid, 0)
        self._forkserver_pid = None
        if not util.is_abstract_socket_namespace(self._forkserver_address):
            os.unlink(self._forkserver_address)
        self._forkserver_address = None
        self._forkserver_authkey = None

    def set_forkserver_preload(self, modules_names):
        """Set list of module names to try to load in forkserver process."""
        if not all((type(mod) is str for mod in modules_names)):
            raise TypeError('module_names must be a list of strings')
        self._preload_modules = modules_names

    def get_inherited_fds(self):
        """Return list of fds inherited from parent process.

        This returns None if the current process was not started by fork
        server.
        """
        return self._inherited_fds

    def connect_to_new_process(self, fds):
        """Request forkserver to create a child process.

        Returns a pair of fds (status_r, data_w).  The calling process can read
        the child process's pid and (eventually) its returncode from status_r.
        The calling process should write to data_w the pickled preparation and
        process data.
        """
        self.ensure_running()
        assert self._forkserver_authkey
        if len(fds) + 4 >= MAXFDS_TO_SEND:
            raise ValueError('too many fds')
        with socket.socket(socket.AF_UNIX) as client:
            client.connect(self._forkserver_address)
            parent_r, child_w = os.pipe()
            child_r, parent_w = os.pipe()
            allfds = [child_r, child_w, self._forkserver_alive_fd, resource_tracker.getfd()]
            allfds += fds
            try:
                client.setblocking(True)
                wrapped_client = connection.Connection(client.fileno())
                try:
                    connection.answer_challenge(wrapped_client, self._forkserver_authkey)
                    connection.deliver_challenge(wrapped_client, self._forkserver_authkey)
                finally:
                    wrapped_client._detach()
                    del wrapped_client
                reduction.sendfds(client, allfds)
                return (parent_r, parent_w)
            except:
                os.close(parent_r)
                os.close(parent_w)
                raise
            finally:
                os.close(child_r)
                os.close(child_w)

    def ensure_running(self):
        """Make sure that a fork server is running.

        This can be called from any process.  Note that usually a child
        process will just reuse the forkserver started by its parent, so
        ensure_running() will do nothing.
        """
        with self._lock:
            resource_tracker.ensure_running()
            if self._forkserver_pid is not None:
                pid, status = os.waitpid(self._forkserver_pid, os.WNOHANG)
                if not pid:
                    return
                os.close(self._forkserver_alive_fd)
                self._forkserver_authkey = None
                self._forkserver_address = None
                self._forkserver_alive_fd = None
                self._forkserver_pid = None
            cmd = 'import sys; from multiprocessing.forkserver import main; main(%d, %d, %r, sys_argv=sys.argv[1:], **%r)'
            main_kws = {}
            sys_argv = None
            if self._preload_modules:
                data = spawn.get_preparation_data('ignore')
                if 'sys_path' in data:
                    main_kws['sys_path'] = data['sys_path']
                if 'init_main_from_path' in data:
                    main_kws['main_path'] = data['init_main_from_path']
                if 'sys_argv' in data:
                    sys_argv = data['sys_argv']
            with socket.socket(socket.AF_UNIX) as listener:
                address = connection.arbitrary_address('AF_UNIX')
                listener.bind(address)
                if not util.is_abstract_socket_namespace(address):
                    os.chmod(address, 384)
                listener.listen()
                alive_r, alive_w = os.pipe()
                authkey_r, authkey_w = os.pipe()
                try:
                    fds_to_pass = [listener.fileno(), alive_r, authkey_r]
                    main_kws['authkey_r'] = authkey_r
                    cmd %= (listener.fileno(), alive_r, self._preload_modules, main_kws)
                    exe = spawn.get_executable()
                    args = [exe] + util._args_from_interpreter_flags()
                    args += ['-c', cmd]
                    if sys_argv is not None:
                        args += sys_argv
                    pid = util.spawnv_passfds(exe, args, fds_to_pass)
                except:
                    os.close(alive_w)
                    os.close(authkey_w)
                    raise
                finally:
                    os.close(alive_r)
                    os.close(authkey_r)
                try:
                    self._forkserver_authkey = os.urandom(_AUTHKEY_LEN)
                    os.write(authkey_w, self._forkserver_authkey)
                finally:
                    os.close(authkey_w)
                self._forkserver_address = address
                self._forkserver_alive_fd = alive_w
                self._forkserver_pid = pid

def main(listener_fd, alive_r, preload, main_path=None, sys_path=None, *, sys_argv=None, authkey_r=None):
    """Run forkserver."""
    if authkey_r is not None:
        try:
            authkey = os.read(authkey_r, _AUTHKEY_LEN)
            assert len(authkey) == _AUTHKEY_LEN, f'{len(authkey)} < {_AUTHKEY_LEN}'
        finally:
            os.close(authkey_r)
    else:
        authkey = b''
    if preload:
        if sys_argv is not None:
            sys.argv[:] = sys_argv
        if sys_path is not None:
            sys.path[:] = sys_path
        if '__main__' in preload and main_path is not None:
            process.current_process()._inheriting = True
            try:
                spawn.import_main_path(main_path)
            finally:
                del process.current_process()._inheriting
        for modname in preload:
            try:
                __import__(modname)
            except ImportError:
                pass
        util._flush_std_streams()
    util._close_stdin()
    sig_r, sig_w = os.pipe()
    os.set_blocking(sig_r, False)
    os.set_blocking(sig_w, False)

    def sigchld_handler(*_unused):
        pass
    handlers = {signal.SIGCHLD: sigchld_handler, signal.SIGINT: signal.SIG_IGN}
    old_handlers = {sig: signal.signal(sig, val) for sig, val in handlers.items()}
    signal.set_wakeup_fd(sig_w)
    pid_to_fd = {}
    with socket.socket(socket.AF_UNIX, fileno=listener_fd) as listener, selectors.DefaultSelector() as selector:
        _forkserver._forkserver_address = listener.getsockname()
        selector.register(listener, selectors.EVENT_READ)
        selector.register(alive_r, selectors.EVENT_READ)
        selector.register(sig_r, selectors.EVENT_READ)
        while True:
            try:
                while True:
                    rfds = [key.fileobj for key, events in selector.select()]
                    if rfds:
                        break
                if alive_r in rfds:
                    assert os.read(alive_r, 1) == b'', 'Not at EOF?'
                    raise SystemExit
                if sig_r in rfds:
                    os.read(sig_r, 65536)
                    while True:
                        try:
                            pid, sts = os.waitpid(-1, os.WNOHANG)
                        except ChildProcessError:
                            break
                        if pid == 0:
                            break
                        child_w = pid_to_fd.pop(pid, None)
                        if child_w is not None:
                            returncode = os.waitstatus_to_exitcode(sts)
                            try:
                                write_signed(child_w, returncode)
                            except BrokenPipeError:
                                pass
                            os.close(child_w)
                        else:
                            warnings.warn('forkserver: waitpid returned unexpected pid %d' % pid)
                if listener in rfds:
                    with listener.accept()[0] as s:
                        try:
                            if authkey:
                                wrapped_s = connection.Connection(s.fileno())
                                try:
                                    connection.deliver_challenge(wrapped_s, authkey)
                                    connection.answer_challenge(wrapped_s, authkey)
                                finally:
                                    wrapped_s._detach()
                                    del wrapped_s
                            fds = reduction.recvfds(s, MAXFDS_TO_SEND + 1)
                        except (EOFError, BrokenPipeError, AuthenticationError):
                            s.close()
                            continue
                        if len(fds) > MAXFDS_TO_SEND:
                            raise RuntimeError('Too many ({0:n}) fds to send'.format(len(fds)))
                        child_r, child_w, *fds = fds
                        s.close()
                        pid = os.fork()
                        if pid == 0:
                            code = 1
                            try:
                                listener.close()
                                selector.close()
                                unused_fds = [alive_r, child_w, sig_r, sig_w]
                                unused_fds.extend(pid_to_fd.values())
                                atexit._clear()
                                atexit.register(util._exit_function)
                                code = _serve_one(child_r, fds, unused_fds, old_handlers)
                            except Exception:
                                sys.excepthook(*sys.exc_info())
                                sys.stderr.flush()
                            finally:
                                atexit._run_exitfuncs()
                                os._exit(code)
                        else:
                            try:
                                write_signed(child_w, pid)
                            except BrokenPipeError:
                                pass
                            pid_to_fd[pid] = child_w
                            os.close(child_r)
                            for fd in fds:
                                os.close(fd)
            except OSError as e:
                if e.errno != errno.ECONNABORTED:
                    raise

def _serve_one(child_r, fds, unused_fds, handlers):
    signal.set_wakeup_fd(-1)
    for sig, val in handlers.items():
        signal.signal(sig, val)
    for fd in unused_fds:
        os.close(fd)
    _forkserver._forkserver_alive_fd, resource_tracker._resource_tracker._fd, *_forkserver._inherited_fds = fds
    parent_sentinel = os.dup(child_r)
    code = spawn._main(child_r, parent_sentinel)
    return code

def read_signed(fd):
    data = bytearray(SIGNED_STRUCT.size)
    unread = memoryview(data)
    while unread:
        count = os.readinto(fd, unread)
        if count == 0:
            raise EOFError('unexpected EOF')
        unread = unread[count:]
    return SIGNED_STRUCT.unpack(data)[0]

def write_signed(fd, n):
    msg = SIGNED_STRUCT.pack(n)
    while msg:
        nbytes = os.write(fd, msg)
        if nbytes == 0:
            raise RuntimeError('should not get here')
        msg = msg[nbytes:]
_forkserver = ForkServer()
ensure_running = _forkserver.ensure_running
get_inherited_fds = _forkserver.get_inherited_fds
connect_to_new_process = _forkserver.connect_to_new_process
set_forkserver_preload = _forkserver.set_forkserver_preload


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
