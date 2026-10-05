# -*- coding: utf-8 -*-
"""多进程.context —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/context.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.context.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'AuthenticationError': '认证错误', 'BaseContext': '上下文基类', 'BufferTooShort': '缓冲过短', 'DefaultContext': '默认上下文', 'Process': '进程', 'ProcessError': '进程错误'}

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
import os
import sys
import threading
from . import process
from . import reduction
__all__ = ()

class 进程错误(Exception):
    pass

class 缓冲过短(进程错误):
    pass

class TimeoutError(进程错误):
    pass

class 认证错误(进程错误):
    pass

class 上下文基类(object):
    进程错误 = 进程错误
    缓冲过短 = 缓冲过短
    TimeoutError = TimeoutError
    认证错误 = 认证错误
    current_process = staticmethod(process.current_process)
    parent_process = staticmethod(process.parent_process)
    active_children = staticmethod(process.active_children)

    def cpu_count(self):
        """Returns the number of CPUs in the system"""
        num = os.cpu_count()
        if num is None:
            raise NotImplementedError('cannot determine number of cpus')
        else:
            return num

    def Manager(self):
        """Returns a manager associated with a running server process

        The managers methods such as `Lock()`, `Condition()` and `Queue()`
        can be used to create shared objects.
        """
        from .managers import SyncManager
        m = SyncManager(ctx=self.get_context())
        m.start()
        return m

    def Pipe(self, duplex=True):
        """Returns two connection object connected by a pipe"""
        from .connection import Pipe
        return Pipe(duplex)

    def Lock(self):
        """Returns a non-recursive lock object"""
        from .synchronize import Lock
        return Lock(ctx=self.get_context())

    def RLock(self):
        """Returns a recursive lock object"""
        from .synchronize import RLock
        return RLock(ctx=self.get_context())

    def Condition(self, lock=None):
        """Returns a condition object"""
        from .synchronize import Condition
        return Condition(lock, ctx=self.get_context())

    def Semaphore(self, value=1):
        """Returns a semaphore object"""
        from .synchronize import Semaphore
        return Semaphore(value, ctx=self.get_context())

    def BoundedSemaphore(self, value=1):
        """Returns a bounded semaphore object"""
        from .synchronize import BoundedSemaphore
        return BoundedSemaphore(value, ctx=self.get_context())

    def Event(self):
        """Returns an event object"""
        from .synchronize import Event
        return Event(ctx=self.get_context())

    def Barrier(self, parties, action=None, timeout=None):
        """Returns a barrier object"""
        from .synchronize import Barrier
        return Barrier(parties, action, timeout, ctx=self.get_context())

    def Queue(self, maxsize=0):
        """Returns a queue object"""
        from .queues import Queue
        return Queue(maxsize, ctx=self.get_context())

    def JoinableQueue(self, maxsize=0):
        """Returns a queue object"""
        from .queues import JoinableQueue
        return JoinableQueue(maxsize, ctx=self.get_context())

    def SimpleQueue(self):
        """Returns a queue object"""
        from .queues import SimpleQueue
        return SimpleQueue(ctx=self.get_context())

    def Pool(self, processes=None, initializer=None, initargs=(), maxtasksperchild=None):
        """Returns a process pool object"""
        from .pool import Pool
        return Pool(processes, initializer, initargs, maxtasksperchild, context=self.get_context())

    def RawValue(self, typecode_or_type, *args):
        """Returns a shared object"""
        from .sharedctypes import RawValue
        return RawValue(typecode_or_type, *args)

    def RawArray(self, typecode_or_type, size_or_initializer):
        """Returns a shared array"""
        from .sharedctypes import RawArray
        return RawArray(typecode_or_type, size_or_initializer)

    def Value(self, typecode_or_type, *args, lock=True):
        """Returns a synchronized shared object"""
        from .sharedctypes import Value
        return Value(typecode_or_type, *args, lock=lock, ctx=self.get_context())

    def Array(self, typecode_or_type, size_or_initializer, *, lock=True):
        """Returns a synchronized shared array"""
        from .sharedctypes import Array
        return Array(typecode_or_type, size_or_initializer, lock=lock, ctx=self.get_context())

    def freeze_support(self):
        """Check whether this is a fake forked process in a frozen executable.
        If so then run code specified by commandline and exit.
        """
        if getattr(sys, 'frozen', False) and self.get_start_method(allow_none=True) in ('spawn', None):
            from .spawn import freeze_support
            freeze_support()

    def get_logger(self):
        """Return package logger -- if it does not already exist then
        it is created.
        """
        from .util import get_logger
        return get_logger()

    def log_to_stderr(self, level=None):
        """Turn on logging and add a handler which prints to stderr"""
        from .util import log_to_stderr
        return log_to_stderr(level)

    def allow_connection_pickling(self):
        """Install support for sending connections and sockets
        between processes
        """
        from . import connection

    def set_executable(self, executable):
        """Sets the path to a python.exe or pythonw.exe binary used to run
        child processes instead of sys.executable when using the 'spawn'
        start method.  Useful for people embedding Python.
        """
        from .spawn import set_executable
        set_executable(executable)

    def set_forkserver_preload(self, module_names):
        """Set list of module names to try to load in forkserver process.
        This is really just a hint.
        """
        from .forkserver import set_forkserver_preload
        set_forkserver_preload(module_names)

    def get_context(self, method=None):
        if method is None:
            return self
        try:
            ctx = _concrete_contexts[method]
        except KeyError:
            raise ValueError('cannot find context for %r' % method) from None
        ctx._check_available()
        return ctx

    def get_start_method(self, allow_none=False):
        return self._name

    def set_start_method(self, method, force=False):
        raise ValueError('cannot set start method of concrete context')

    @property
    def reducer(self):
        """Controls how objects will be reduced to a form that can be
        shared with other processes."""
        return globals().get('reduction')

    @reducer.setter
    def reducer(self, reduction):
        globals()['reduction'] = reduction

    def _check_available(self):
        pass
_装类转发(上下文基类, {'AuthenticationError': '认证错误', 'BufferTooShort': '缓冲过短', 'ProcessError': '进程错误'}, {'AuthenticationError': '认证错误', 'BufferTooShort': '缓冲过短', 'ProcessError': '进程错误'})

class 进程(process.BaseProcess):
    _start_method = None

    @staticmethod
    def _Popen(process_obj):
        return _default_context.get_context().Process._Popen(process_obj)

    @staticmethod
    def _after_fork():
        return _default_context.get_context().Process._after_fork()

class 默认上下文(上下文基类):
    进程 = 进程

    def __init__(self, context):
        self._default_context = context
        self._actual_context = None

    def get_context(self, method=None):
        if method is None:
            if self._actual_context is None:
                self._actual_context = self._default_context
            return self._actual_context
        else:
            return super().get_context(method)

    def set_start_method(self, method, force=False):
        if self._actual_context is not None and (not force):
            raise RuntimeError('context has already been set')
        if method is None and force:
            self._actual_context = None
            return
        self._actual_context = self.get_context(method)

    def get_start_method(self, allow_none=False):
        if self._actual_context is None:
            if allow_none:
                return None
            self._actual_context = self._default_context
        return self._actual_context._name

    def get_all_start_methods(self):
        """Returns a list of the supported start methods, default first."""
        default = self._default_context.get_start_method()
        start_method_names = [default]
        start_method_names.extend((name for name in _concrete_contexts if name != default))
        return start_method_names
_装类转发(默认上下文, {'Process': '进程'}, {'Process': '进程'})
if sys.platform != 'win32':

    class ForkProcess(process.BaseProcess):
        _start_method = 'fork'

        @staticmethod
        def _Popen(process_obj):
            from .popen_fork import Popen
            return Popen(process_obj)

    class SpawnProcess(process.BaseProcess):
        _start_method = 'spawn'

        @staticmethod
        def _Popen(process_obj):
            from .popen_spawn_posix import Popen
            return Popen(process_obj)

        @staticmethod
        def _after_fork():
            pass

    class ForkServerProcess(process.BaseProcess):
        _start_method = 'forkserver'

        @staticmethod
        def _Popen(process_obj):
            from .popen_forkserver import Popen
            return Popen(process_obj)

    class ForkContext(上下文基类):
        _name = 'fork'
        进程 = ForkProcess
    _装类转发(ForkContext, {'Process': '进程'}, {'Process': '进程'})

    class SpawnContext(上下文基类):
        _name = 'spawn'
        进程 = SpawnProcess
    _装类转发(SpawnContext, {'Process': '进程'}, {'Process': '进程'})

    class ForkServerContext(上下文基类):
        _name = 'forkserver'
        进程 = ForkServerProcess

        def _check_available(self):
            if not reduction.HAVE_SEND_HANDLE:
                raise ValueError('forkserver start method not available')
    _装类转发(ForkServerContext, {'Process': '进程'}, {'Process': '进程'})
    _concrete_contexts = {'fork': ForkContext(), 'spawn': SpawnContext(), 'forkserver': ForkServerContext()}
    if reduction.HAVE_SEND_HANDLE and sys.platform != 'darwin':
        _default_context = 默认上下文(_concrete_contexts['forkserver'])
    else:
        _default_context = 默认上下文(_concrete_contexts['spawn'])
else:

    class SpawnProcess(process.BaseProcess):
        _start_method = 'spawn'

        @staticmethod
        def _Popen(process_obj):
            from .popen_spawn_win32 import Popen
            return Popen(process_obj)

        @staticmethod
        def _after_fork():
            pass

    class SpawnContext(上下文基类):
        _name = 'spawn'
        进程 = SpawnProcess
    _装类转发(SpawnContext, {'Process': '进程'}, {'Process': '进程'})
    _concrete_contexts = {'spawn': SpawnContext()}
    _default_context = 默认上下文(_concrete_contexts['spawn'])

def _force_start_method(method):
    _default_context._actual_context = _concrete_contexts[method]
_tls = threading.local()

def get_spawning_popen():
    return getattr(_tls, 'spawning_popen', None)

def set_spawning_popen(popen):
    _tls.spawning_popen = popen

def assert_spawning(obj):
    if get_spawning_popen() is None:
        raise RuntimeError('%s objects should only be shared between processes through inheritance' % type(obj).__name__)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '超时错误': 'TimeoutError',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'AuthenticationError': '认证错误',
    'BaseContext': '上下文基类',
    'BufferTooShort': '缓冲过短',
    'DefaultContext': '默认上下文',
    'Process': '进程',
    'ProcessError': '进程错误',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'ForkContext': {
        'Process': '进程',
    },
    'ForkServerContext': {
        'Process': '进程',
    },
    'SpawnContext': {
        'Process': '进程',
    },
    '上下文基类': {
        'AuthenticationError': '认证错误',
        'BufferTooShort': '缓冲过短',
        'ProcessError': '进程错误',
    },
    '默认上下文': {
        'Process': '进程',
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
    'ForkContext': {
        'Process': '进程',
    },
    'ForkServerContext': {
        'Process': '进程',
    },
    'SpawnContext': {
        'Process': '进程',
    },
    '上下文基类': {
        'AuthenticationError': '认证错误',
        'BufferTooShort': '缓冲过短',
        'ProcessError': '进程错误',
    },
    '默认上下文': {
        'Process': '进程',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
