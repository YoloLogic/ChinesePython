# -*- coding: utf-8 -*-
"""多进程.synchronize —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/synchronize.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.synchronize.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Barrier': '栅栏', 'BoundedSemaphore': '有界信号量', 'Condition': '条件', 'Semaphore': '信号量'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Condition', 'Event']
import threading
import sys
import tempfile
import _multiprocessing
import time
from . import context
from . import process
from . import util
try:
    from _multiprocessing import SemLock, sem_unlink
except ImportError:
    raise ImportError('This platform lacks a functioning sem_open' + ' implementation. https://github.com/python/cpython/issues/48020.')
RECURSIVE_MUTEX = 0
SEMAPHORE = 1
SEM_VALUE_MAX = _multiprocessing.SemLock.SEM_VALUE_MAX

class SemLock(object):
    _rand = tempfile._RandomNameSequence()

    def __init__(self, kind, value, maxvalue, *, ctx):
        if ctx is None:
            ctx = context._default_context.get_context()
        self._is_fork_ctx = ctx.get_start_method() == 'fork'
        unlink_now = sys.platform == 'win32' or self._is_fork_ctx
        for i in range(100):
            try:
                sl = self._semlock = _multiprocessing.SemLock(kind, value, maxvalue, self._make_name(), unlink_now)
            except FileExistsError:
                pass
            else:
                break
        else:
            raise FileExistsError('cannot find name for semaphore')
        util.debug('created semlock with handle %s' % sl.handle)
        self._make_methods()
        if sys.platform != 'win32':

            def _after_fork(obj):
                obj._semlock._after_fork()
            util.register_after_fork(self, _after_fork)
        if self._semlock.name is not None:
            from .resource_tracker import register
            register(self._semlock.name, 'semaphore')
            util.Finalize(self, SemLock._cleanup, (self._semlock.name,), exitpriority=0)

    @staticmethod
    def _cleanup(name):
        from .resource_tracker import unregister
        sem_unlink(name)
        unregister(name, 'semaphore')

    def _make_methods(self):
        self.acquire = self._semlock.acquire
        self.release = self._semlock.release

    def locked(self):
        return self._semlock._is_zero()

    def __enter__(self):
        return self._semlock.__enter__()

    def __exit__(self, *args):
        return self._semlock.__exit__(*args)

    def __getstate__(self):
        context.assert_spawning(self)
        sl = self._semlock
        if sys.platform == 'win32':
            h = context.get_spawning_popen().duplicate_for_child(sl.handle)
        else:
            if self._is_fork_ctx:
                raise RuntimeError('A SemLock created in a fork context is being shared with a process in a spawn context. This is not supported. Please use the same context to create multiprocessing objects and Process.')
            h = sl.handle
        return (h, sl.kind, sl.maxvalue, sl.name)

    def __setstate__(self, state):
        self._semlock = _multiprocessing.SemLock._rebuild(*state)
        util.debug('recreated blocker with handle %r' % state[0])
        self._make_methods()
        self._is_fork_ctx = False

    @staticmethod
    def _make_name():
        return '%s-%s' % (process.current_process()._config['semprefix'], next(SemLock._rand))

class 信号量(SemLock):

    def __init__(self, value=1, *, ctx):
        SemLock.__init__(self, SEMAPHORE, value, SEM_VALUE_MAX, ctx=ctx)

    def get_value(self):
        """Returns current value of Semaphore.

        Raises NotImplementedError on Mac OSX
        because of broken sem_getvalue().
        """
        return self._semlock._get_value()

    def __repr__(self):
        try:
            value = self.get_value()
        except Exception:
            value = 'unknown'
        return '<%s(value=%s)>' % (self.__class__.__name__, value)

class 有界信号量(信号量):

    def __init__(self, value=1, *, ctx):
        SemLock.__init__(self, SEMAPHORE, value, value, ctx=ctx)

    def __repr__(self):
        try:
            value = self.get_value()
        except Exception:
            value = 'unknown'
        return '<%s(value=%s, maxvalue=%s)>' % (self.__class__.__name__, value, self._semlock.maxvalue)

class Lock(SemLock):

    def __init__(self, *, ctx):
        SemLock.__init__(self, SEMAPHORE, 1, 1, ctx=ctx)

    def __repr__(self):
        try:
            if self._semlock._is_mine():
                name = process.current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
            elif not self._semlock._is_zero():
                name = 'None'
            elif self._semlock._count() > 0:
                name = 'SomeOtherThread'
            else:
                name = 'SomeOtherProcess'
        except Exception:
            name = 'unknown'
        return '<%s(owner=%s)>' % (self.__class__.__name__, name)

class RLock(SemLock):

    def __init__(self, *, ctx):
        SemLock.__init__(self, RECURSIVE_MUTEX, 1, 1, ctx=ctx)

    def __repr__(self):
        try:
            if self._semlock._is_mine():
                name = process.current_process().name
                if threading.current_thread().name != 'MainThread':
                    name += '|' + threading.current_thread().name
                count = self._semlock._count()
            elif not self._semlock._is_zero():
                name, count = ('None', 0)
            elif self._semlock._count() > 0:
                name, count = ('SomeOtherThread', 'nonzero')
            else:
                name, count = ('SomeOtherProcess', 'nonzero')
        except Exception:
            name, count = ('unknown', 'unknown')
        return '<%s(%s, %s)>' % (self.__class__.__name__, name, count)

class 条件(object):

    def __init__(self, lock=None, *, ctx):
        self._lock = lock or ctx.RLock()
        self._sleeping_count = ctx.Semaphore(0)
        self._woken_count = ctx.Semaphore(0)
        self._wait_semaphore = ctx.Semaphore(0)
        self._make_methods()

    def __getstate__(self):
        context.assert_spawning(self)
        return (self._lock, self._sleeping_count, self._woken_count, self._wait_semaphore)

    def __setstate__(self, state):
        self._lock, self._sleeping_count, self._woken_count, self._wait_semaphore = state
        self._make_methods()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    def _make_methods(self):
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    def __repr__(self):
        try:
            num_waiters = self._sleeping_count.get_value() - self._woken_count.get_value()
        except Exception:
            num_waiters = 'unknown'
        return '<%s(%s, %s)>' % (self.__class__.__name__, self._lock, num_waiters)

    def wait(self, timeout=None):
        assert self._lock._semlock._is_mine(), 'must acquire() condition before using wait()'
        self._sleeping_count.release()
        count = self._lock._semlock._count()
        for i in range(count):
            self._lock.release()
        try:
            return self._wait_semaphore.acquire(True, timeout)
        finally:
            self._woken_count.release()
            for i in range(count):
                self._lock.acquire()

    def notify(self, n=1):
        assert self._lock._semlock._is_mine(), 'lock is not owned'
        assert not self._wait_semaphore.acquire(False), 'notify: Should not have been able to acquire ' + '_wait_semaphore'
        while self._woken_count.acquire(False):
            res = self._sleeping_count.acquire(False)
            assert res, 'notify: Bug in sleeping_count.acquire' + '- res should not be False'
        sleepers = 0
        while sleepers < n and self._sleeping_count.acquire(False):
            self._wait_semaphore.release()
            sleepers += 1
        if sleepers:
            for i in range(sleepers):
                self._woken_count.acquire()
            while self._wait_semaphore.acquire(False):
                pass

    def notify_all(self):
        self.notify(n=sys.maxsize)

    def wait_for(self, predicate, timeout=None):
        result = predicate()
        if result:
            return result
        if timeout is not None:
            endtime = time.monotonic() + timeout
        else:
            endtime = None
            waittime = None
        while not result:
            if endtime is not None:
                waittime = endtime - time.monotonic()
                if waittime <= 0:
                    break
            self.wait(waittime)
            result = predicate()
        return result

class Event(object):

    def __init__(self, *, ctx):
        self._cond = ctx.Condition(ctx.Lock())
        self._flag = ctx.Semaphore(0)

    def is_set(self):
        with self._cond:
            if self._flag.acquire(False):
                self._flag.release()
                return True
            return False

    def set(self):
        with self._cond:
            self._flag.acquire(False)
            self._flag.release()
            self._cond.notify_all()

    def clear(self):
        with self._cond:
            self._flag.acquire(False)

    def wait(self, timeout=None):
        with self._cond:
            if self._flag.acquire(False):
                self._flag.release()
            else:
                self._cond.wait(timeout)
            if self._flag.acquire(False):
                self._flag.release()
                return True
            return False

    def __repr__(self):
        set_status = 'set' if self.is_set() else 'unset'
        return f'<{type(self).__qualname__} at {id(self):#x} {set_status}>'

class 栅栏(threading.Barrier):

    def __init__(self, parties, action=None, timeout=None, *, ctx):
        import struct
        from .heap import BufferWrapper
        wrapper = BufferWrapper(struct.calcsize('i') * 2)
        cond = ctx.Condition()
        self.__setstate__((parties, action, timeout, cond, wrapper))
        self._state = 0
        self._count = 0

    def __setstate__(self, state):
        self._parties, self._action, self._timeout, self._cond, self._wrapper = state
        self._array = self._wrapper.create_memoryview().cast('i')

    def __getstate__(self):
        return (self._parties, self._action, self._timeout, self._cond, self._wrapper)

    @property
    def _state(self):
        return self._array[0]

    @_state.setter
    def _state(self, value):
        self._array[0] = value

    @property
    def _count(self):
        return self._array[1]

    @_count.setter
    def _count(self, value):
        self._array[1] = value


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
    '事件': 'Event',
    '可重入锁': 'RLock',
    '锁': 'Lock',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'Barrier': '栅栏',
    'BoundedSemaphore': '有界信号量',
    'Condition': '条件',
    'Semaphore': '信号量',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '事件',
    '信号量',
    '可重入锁',
    '有界信号量',
    '条件',
    '锁',
]

# ---- 转发层结束 ----
