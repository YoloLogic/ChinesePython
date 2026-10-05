# -*- coding: utf-8 -*-
"""多进程.reduction —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/reduction.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.reduction.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'AbstractReducer': '归约基类', 'ForkingPickler': '分叉序列化器', 'dump': '转储'}

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
from abc import ABCMeta
import copyreg
import functools
import io
import os
import pickle
import socket
import sys
from . import context
__all__ = ['send_handle', 'recv_handle', 'ForkingPickler', 'register', 'dump']
HAVE_SEND_HANDLE = sys.platform == 'win32' or (hasattr(socket, 'CMSG_LEN') and hasattr(socket, 'SCM_RIGHTS') and hasattr(socket.socket, 'sendmsg'))

class 分叉序列化器(pickle.Pickler):
    """Pickler subclass used by multiprocessing."""
    _extra_reducers = {}
    _copyreg_dispatch_table = copyreg.dispatch_table

    def __init__(self, *args):
        super().__init__(*args)
        self.dispatch_table = self._copyreg_dispatch_table.copy()
        self.dispatch_table.update(self._extra_reducers)

    @classmethod
    def register(cls, type, reduce):
        """Register a reduce function for a type."""
        cls._extra_reducers[type] = reduce

    @classmethod
    def dumps(cls, obj, protocol=None):
        buf = io.BytesIO()
        cls(buf, protocol).dump(obj)
        return buf.getbuffer()
    loads = pickle.loads
register = 分叉序列化器.register

def 转储(obj, file, protocol=None):
    """Replacement for pickle.dump() using ForkingPickler."""
    分叉序列化器(file, protocol).dump(obj)
if sys.platform == 'win32':
    __all__ += ['DupHandle', 'duplicate', 'steal_handle']
    import _winapi

    def duplicate(handle, target_process=None, inheritable=False, *, source_process=None):
        """Duplicate a handle.  (target_process is a handle not a pid!)"""
        current_process = _winapi.GetCurrentProcess()
        if source_process is None:
            source_process = current_process
        if target_process is None:
            target_process = current_process
        return _winapi.DuplicateHandle(source_process, handle, target_process, 0, inheritable, _winapi.DUPLICATE_SAME_ACCESS)

    def steal_handle(source_pid, handle):
        """Steal a handle from process identified by source_pid."""
        source_process_handle = _winapi.OpenProcess(_winapi.PROCESS_DUP_HANDLE, False, source_pid)
        try:
            return _winapi.DuplicateHandle(source_process_handle, handle, _winapi.GetCurrentProcess(), 0, False, _winapi.DUPLICATE_SAME_ACCESS | _winapi.DUPLICATE_CLOSE_SOURCE)
        finally:
            _winapi.CloseHandle(source_process_handle)

    def send_handle(conn, handle, destination_pid):
        """Send a handle over a local connection."""
        dh = DupHandle(handle, _winapi.DUPLICATE_SAME_ACCESS, destination_pid)
        conn.send(dh)

    def recv_handle(conn):
        """Receive a handle over a local connection."""
        return conn.recv().detach()

    class DupHandle(object):
        """Picklable wrapper for a handle."""

        def __init__(self, handle, access, pid=None):
            if pid is None:
                pid = os.getpid()
            proc = _winapi.OpenProcess(_winapi.PROCESS_DUP_HANDLE, False, pid)
            try:
                self._handle = _winapi.DuplicateHandle(_winapi.GetCurrentProcess(), handle, proc, access, False, 0)
            finally:
                _winapi.CloseHandle(proc)
            self._access = access
            self._pid = pid

        def detach(self):
            """Get the handle.  This should only be called once."""
            if self._pid == os.getpid():
                return self._handle
            proc = _winapi.OpenProcess(_winapi.PROCESS_DUP_HANDLE, False, self._pid)
            try:
                return _winapi.DuplicateHandle(proc, self._handle, _winapi.GetCurrentProcess(), self._access, False, _winapi.DUPLICATE_CLOSE_SOURCE)
            finally:
                _winapi.CloseHandle(proc)
else:
    __all__ += ['DupFd', 'sendfds', 'recvfds']
    import array

    def sendfds(sock, fds):
        """Send an array of fds over an AF_UNIX socket."""
        fds = array.array('i', fds)
        msg = bytes([len(fds) % 256])
        sock.sendmsg([msg], [(socket.SOL_SOCKET, socket.SCM_RIGHTS, fds)])
        if sock.recv(1) != b'A':
            raise RuntimeError('did not receive acknowledgement of fd')

    def recvfds(sock, size):
        """Receive an array of fds over an AF_UNIX socket."""
        a = array.array('i')
        bytes_size = a.itemsize * size
        msg, ancdata, flags, addr = sock.recvmsg(1, socket.CMSG_SPACE(bytes_size))
        if not msg and (not ancdata):
            raise EOFError
        try:
            sock.send(b'A')
            if len(ancdata) != 1:
                raise RuntimeError('received %d items of ancdata' % len(ancdata))
            cmsg_level, cmsg_type, cmsg_data = ancdata[0]
            if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
                if len(cmsg_data) % a.itemsize != 0:
                    raise ValueError
                a.frombytes(cmsg_data)
                if len(a) % 256 != msg[0]:
                    raise AssertionError('Len is {0:n} but msg[0] is {1!r}'.format(len(a), msg[0]))
                return list(a)
        except (ValueError, IndexError):
            pass
        raise RuntimeError('Invalid data received')

    def send_handle(conn, handle, destination_pid):
        """Send a handle over a local connection."""
        with socket.fromfd(conn.fileno(), socket.AF_UNIX, socket.SOCK_STREAM) as s:
            sendfds(s, [handle])

    def recv_handle(conn):
        """Receive a handle over a local connection."""
        with socket.fromfd(conn.fileno(), socket.AF_UNIX, socket.SOCK_STREAM) as s:
            return recvfds(s, 1)[0]

    def DupFd(fd):
        """Return a wrapper for an fd."""
        popen_obj = context.get_spawning_popen()
        if popen_obj is not None:
            return popen_obj.DupFd(popen_obj.duplicate_for_child(fd))
        elif HAVE_SEND_HANDLE:
            from . import resource_sharer
            return resource_sharer.DupFd(fd)
        else:
            raise ValueError('SCM_RIGHTS appears not to be available')

def _reduce_method(m):
    if m.__self__ is None:
        return (getattr, (m.__class__, m.__func__.__name__))
    else:
        return (getattr, (m.__self__, m.__func__.__name__))

class _C:

    def f(self):
        pass
register(type(_C().f), _reduce_method)

def _reduce_method_descriptor(m):
    return (getattr, (m.__objclass__, m.__name__))
register(type(list.append), _reduce_method_descriptor)
register(type(int.__add__), _reduce_method_descriptor)

def _reduce_partial(p):
    return (_rebuild_partial, (p.func, p.args, p.keywords or {}))

def _rebuild_partial(func, args, keywords):
    return functools.partial(func, *args, **keywords)
register(functools.partial, _reduce_partial)
if sys.platform == 'win32':

    def _reduce_socket(s):
        from .resource_sharer import DupSocket
        return (_rebuild_socket, (DupSocket(s),))

    def _rebuild_socket(ds):
        return ds.detach()
    register(socket.socket, _reduce_socket)
else:

    def _reduce_socket(s):
        df = DupFd(s.fileno())
        return (_rebuild_socket, (df, s.family, s.type, s.proto))

    def _rebuild_socket(df, family, type, proto):
        fd = df.detach()
        return socket.socket(family, type, proto, fileno=fd)
    register(socket.socket, _reduce_socket)

class 归约基类(metaclass=ABCMeta):
    """Abstract base class for use in implementing a Reduction class
    suitable for use in replacing the standard reduction mechanism
    used in multiprocessing."""
    分叉序列化器 = 分叉序列化器
    register = register
    转储 = 转储
    send_handle = send_handle
    recv_handle = recv_handle
    if sys.platform == 'win32':
        steal_handle = steal_handle
        duplicate = duplicate
        DupHandle = DupHandle
    else:
        sendfds = sendfds
        recvfds = recvfds
        DupFd = DupFd
    _reduce_method = _reduce_method
    _reduce_method_descriptor = _reduce_method_descriptor
    _rebuild_partial = _rebuild_partial
    _reduce_socket = _reduce_socket
    _rebuild_socket = _rebuild_socket

    def __init__(self, *args):
        register(type(_C().f), _reduce_method)
        register(type(list.append), _reduce_method_descriptor)
        register(type(int.__add__), _reduce_method_descriptor)
        register(functools.partial, _reduce_partial)
        register(socket.socket, _reduce_socket)
_装类转发(归约基类, {'ForkingPickler': '分叉序列化器', 'dump': '转储'}, {'ForkingPickler': '分叉序列化器', 'dump': '转储'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'AbstractReducer': '归约基类',
    'ForkingPickler': '分叉序列化器',
    'dump': '转储',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '归约基类': {
        'ForkingPickler': '分叉序列化器',
        'dump': '转储',
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
    '归约基类': {
        'ForkingPickler': '分叉序列化器',
        'dump': '转储',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '分叉序列化器',
    '转储',
]

# ---- 转发层结束 ----
