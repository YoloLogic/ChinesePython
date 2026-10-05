# -*- coding: utf-8 -*-
"""多线程 —— 汉语库（由 tools/汉化库.py 从 Lib/threading.py 机械生成，**不要手改**）。

英文库 Lib/threading.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 多线程
"""


"""Thread module emulating a subset of Java's threading model."""
_英文原名表 = {'Barrier': '栅栏', 'BoundedSemaphore': '有界信号量', 'BrokenBarrierError': '栅栏破损错误', 'Condition': '条件', 'Event': '事件', 'Lock': '锁', 'RLock': '可重入锁', 'Semaphore': '信号量', 'TIMEOUT_MAX': '超时上限', 'Thread': '线程', 'ThreadError': '线程错误', 'Timer': '定时器', 'active_count': '活动线程数', 'current_thread': '当前线程', 'get_ident': '取线程标识', 'get_native_id': '取本机线程号', 'getprofile': '取性能钩子', 'gettrace': '取跟踪钩子', 'main_thread': '主线程', 'setprofile': '设性能钩子', 'setprofile_all_threads': '设全线程性能钩子', 'settrace': '设跟踪钩子', 'settrace_all_threads': '设全线程跟踪钩子'}

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
import os as _os
import sys as _sys
import _thread
import _contextvars
from time import monotonic as _time
from _weakrefset import WeakSet
from itertools import count as _count
try:
    from _collections import deque as _deque
except ImportError:
    from collections import deque as _deque
__all__ = ['get_ident', 'active_count', 'Condition', 'current_thread', 'enumerate', 'main_thread', 'TIMEOUT_MAX', 'Event', 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Thread', 'Barrier', 'BrokenBarrierError', 'Timer', 'ThreadError', 'setprofile', 'settrace', 'local', 'stack_size', 'excepthook', 'ExceptHookArgs', 'gettrace', 'getprofile', 'setprofile_all_threads', 'settrace_all_threads']
_start_joinable_thread = _thread.start_joinable_thread
_daemon_threads_allowed = _thread.daemon_threads_allowed
_allocate_lock = _thread.allocate_lock
_LockType = _thread.LockType
_thread_shutdown = _thread._shutdown
_make_thread_handle = _thread._make_thread_handle
_ThreadHandle = _thread._ThreadHandle
取线程标识 = _thread.get_ident
_get_main_thread_ident = _thread._get_main_thread_ident
_is_main_interpreter = _thread._is_main_interpreter
try:
    取本机线程号 = _thread.get_native_id
    _HAVE_THREAD_NATIVE_ID = True
    __all__.append('get_native_id')
except AttributeError:
    _HAVE_THREAD_NATIVE_ID = False
try:
    _set_name = _thread.set_name
except AttributeError:
    _set_name = None
线程错误 = _thread.error
try:
    _CRLock = _thread.RLock
except AttributeError:
    _CRLock = None
超时上限 = _thread.TIMEOUT_MAX
del _thread
try:
    from _thread import _local as local
except ImportError:
    from _threading_local import local
_profile_hook = None
_trace_hook = None

def 设性能钩子(func):
    """Set a profile function for all threads started from the threading module.

    The func will be passed to sys.setprofile() for each thread, before its
    run() method is called.
    """
    global _profile_hook
    _profile_hook = func

def 设全线程性能钩子(func):
    """Set a profile function for all threads started from the threading module
    and all Python threads that are currently executing.

    The func will be passed to sys.setprofile() for each thread, before its
    run() method is called.
    """
    设性能钩子(func)
    _sys._setprofileallthreads(func)

def 取性能钩子():
    """Get the profiler function as set by threading.setprofile()."""
    return _profile_hook

def 设跟踪钩子(func):
    """Set a trace function for all threads started from the threading module.

    The func will be passed to sys.settrace() for each thread, before its run()
    method is called.
    """
    global _trace_hook
    _trace_hook = func

def 设全线程跟踪钩子(func):
    """Set a trace function for all threads started from the threading module
    and all Python threads that are currently executing.

    The func will be passed to sys.settrace() for each thread, before its run()
    method is called.
    """
    设跟踪钩子(func)
    _sys._settraceallthreads(func)

def 取跟踪钩子():
    """Get the trace function as set by threading.settrace()."""
    return _trace_hook
锁 = _LockType

def 可重入锁(*args, **kwargs):
    """Factory function that returns a new reentrant lock.

    A reentrant lock must be released by the thread that acquired it. Once a
    thread has acquired a reentrant lock, the same thread may acquire it again
    without blocking; the thread must release it once for each time it has
    acquired it.

    """
    if args or kwargs:
        import warnings
        warnings.warn('Passing arguments to RLock is deprecated and will be removed in 3.15', DeprecationWarning, stacklevel=2)
    if _CRLock is None:
        return _PyRLock(*args, **kwargs)
    return _CRLock(*args, **kwargs)

class _RLock:
    """This class implements reentrant lock objects.

    A reentrant lock must be released by the thread that acquired it. Once a
    thread has acquired a reentrant lock, the same thread may acquire it
    again without blocking; the thread must release it once for each time it
    has acquired it.

    """

    def __init__(self):
        self._block = _allocate_lock()
        self._owner = None
        self._count = 0

    def __repr__(self):
        owner = self._owner
        try:
            owner = _active[owner].name
        except KeyError:
            pass
        return '<%s %s.%s object owner=%r count=%d at %s>' % ('locked' if self.locked() else 'unlocked', self.__class__.__module__, self.__class__.__qualname__, owner, self._count, hex(id(self)))

    def _at_fork_reinit(self):
        self._block._at_fork_reinit()
        self._owner = None
        self._count = 0

    def acquire(self, blocking=True, timeout=-1):
        """Acquire a lock, blocking or non-blocking.

        When invoked without arguments: if this thread already owns the lock,
        increment the recursion level by one, and return immediately. Otherwise,
        if another thread owns the lock, block until the lock is unlocked. Once
        the lock is unlocked (not owned by any thread), then grab ownership, set
        the recursion level to one, and return. If more than one thread is
        blocked waiting until the lock is unlocked, only one at a time will be
        able to grab ownership of the lock. There is no return value in this
        case.

        When invoked with the blocking argument set to true, do the same thing
        as when called without arguments, and return true.

        When invoked with the blocking argument set to false, do not block. If a
        call without an argument would block, return false immediately;
        otherwise, do the same thing as when called without arguments, and
        return true.

        When invoked with the floating-point timeout argument set to a positive
        value, block for at most the number of seconds specified by timeout
        and as long as the lock cannot be acquired.  Return true if the lock has
        been acquired, false if the timeout has elapsed.

        """
        me = 取线程标识()
        if self._owner == me:
            self._count += 1
            return 1
        rc = self._block.acquire(blocking, timeout)
        if rc:
            self._owner = me
            self._count = 1
        return rc
    __enter__ = acquire

    def release(self):
        """Release a lock, decrementing the recursion level.

        If after the decrement it is zero, reset the lock to unlocked (not owned
        by any thread), and if any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed. If after
        the decrement the recursion level is still nonzero, the lock remains
        locked and owned by the calling thread.

        Only call this method when the calling thread owns the lock. A
        RuntimeError is raised if this method is called when the lock is
        unlocked.

        There is no return value.

        """
        if self._owner != 取线程标识():
            raise RuntimeError('cannot release un-acquired lock')
        self._count = count = self._count - 1
        if not count:
            self._owner = None
            self._block.release()

    def __exit__(self, t, v, tb):
        self.release()

    def locked(self):
        """Return whether this object is locked."""
        return self._block.locked()

    def _acquire_restore(self, state):
        self._block.acquire()
        self._count, self._owner = state

    def _release_save(self):
        if self._count == 0:
            raise RuntimeError('cannot release un-acquired lock')
        count = self._count
        self._count = 0
        owner = self._owner
        self._owner = None
        self._block.release()
        return (count, owner)

    def _is_owned(self):
        return self._owner == 取线程标识()

    def _recursion_count(self):
        if self._owner != 取线程标识():
            return 0
        return self._count
_PyRLock = _RLock

class 条件:
    """Class that implements a condition variable.

    A condition variable allows one or more threads to wait until they are
    notified by another thread.

    If the lock argument is given and not None, it must be a Lock or RLock
    object, and it is used as the underlying lock. Otherwise, a new RLock object
    is created and used as the underlying lock.

    """

    def __init__(self, lock=None):
        if lock is None:
            lock = 可重入锁()
        self._lock = lock
        self.acquire = lock.acquire
        self.release = lock.release
        self.locked = lock.locked
        if hasattr(lock, '_release_save'):
            self._release_save = lock._release_save
        if hasattr(lock, '_acquire_restore'):
            self._acquire_restore = lock._acquire_restore
        if hasattr(lock, '_is_owned'):
            self._is_owned = lock._is_owned
        self._waiters = _deque()

    def _at_fork_reinit(self):
        self._lock._at_fork_reinit()
        self._waiters.clear()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    def __repr__(self):
        return '<Condition(%s, %d)>' % (self._lock, len(self._waiters))

    def _release_save(self):
        self._lock.release()

    def _acquire_restore(self, x):
        self._lock.acquire()

    def _is_owned(self):
        if self._lock.acquire(False):
            self._lock.release()
            return False
        else:
            return True

    def 等候(self, timeout=None):
        """Wait until notified or until a timeout occurs.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method releases the underlying lock, and then blocks until it is
        awakened by a notify() or notify_all() call for the same condition
        variable in another thread, or until the optional timeout occurs. Once
        awakened or timed out, it re-acquires the lock and returns.

        When the timeout argument is present and not None, it should be a
        floating-point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        When the underlying lock is an RLock, it is not released using its
        release() method, since this may not actually unlock the lock when it
        was acquired multiple times recursively. Instead, an internal interface
        of the RLock class is used, which really unlocks it even when it has
        been recursively acquired several times. Another internal interface is
        then used to restore the recursion level when the lock is reacquired.

        """
        if not self._is_owned():
            raise RuntimeError('cannot wait on un-acquired lock')
        waiter = _allocate_lock()
        waiter.acquire()
        self._waiters.append(waiter)
        saved_state = self._release_save()
        gotit = False
        try:
            if timeout is None:
                waiter.acquire()
                gotit = True
            elif timeout > 0:
                gotit = waiter.acquire(True, timeout)
            else:
                gotit = waiter.acquire(False)
            return gotit
        finally:
            self._acquire_restore(saved_state)
            if not gotit:
                try:
                    self._waiters.remove(waiter)
                except ValueError:
                    pass

    def 等候直到(self, predicate, timeout=None):
        """Wait until a condition evaluates to True.

        predicate should be a callable which result will be interpreted as a
        boolean value.  A timeout may be provided giving the maximum time to
        wait.

        """
        endtime = None
        waittime = timeout
        result = predicate()
        while not result:
            if waittime is not None:
                if endtime is None:
                    endtime = _time() + waittime
                else:
                    waittime = endtime - _time()
                    if waittime <= 0:
                        break
            self.等候(waittime)
            result = predicate()
        return result

    def 通知(self, n=1):
        """Wake up one or more threads waiting on this condition, if any.

        If the calling thread has not acquired the lock when this method is
        called, a RuntimeError is raised.

        This method wakes up at most n of the threads waiting for the condition
        variable; it is a no-op if no threads are waiting.

        """
        if not self._is_owned():
            raise RuntimeError('cannot notify on un-acquired lock')
        waiters = self._waiters
        while waiters and n > 0:
            waiter = waiters[0]
            try:
                waiter.release()
            except RuntimeError:
                pass
            else:
                n -= 1
            try:
                waiters.remove(waiter)
            except ValueError:
                pass

    def 通知全部(self):
        """Wake up all threads waiting on this condition.

        If the calling thread has not acquired the lock when this method
        is called, a RuntimeError is raised.

        """
        self.通知(len(self._waiters))

    def notifyAll(self):
        """Wake up all threads waiting on this condition.

        This method is deprecated, use notify_all() instead.

        """
        import warnings
        warnings.warn('notifyAll() is deprecated, use notify_all() instead', DeprecationWarning, stacklevel=2)
        self.通知全部()
_装类转发(条件, {'notify': '通知', 'notify_all': '通知全部', 'wait': '等候', 'wait_for': '等候直到'}, {'notify': '通知', 'notify_all': '通知全部', 'wait': '等候', 'wait_for': '等候直到'})

class 信号量:
    """This class implements semaphore objects.

    Semaphores manage a counter representing the number of release() calls minus
    the number of acquire() calls, plus an initial value. The acquire() method
    blocks if necessary until it can return without making the counter
    negative. If not given, value defaults to 1.

    """

    def __init__(self, value=1):
        if value < 0:
            raise ValueError('semaphore initial value must be >= 0')
        self._cond = 条件(锁())
        self._value = value

    def __repr__(self):
        cls = self.__class__
        return f'<{cls.__module__}.{cls.__qualname__} at {id(self):#x}: value={self._value}>'

    def acquire(self, blocking=True, timeout=None):
        """Acquire a semaphore, decrementing the internal counter by one.

        When invoked without arguments: if the internal counter is larger than
        zero on entry, decrement it by one and return immediately. If it is zero
        on entry, block, waiting until some other thread has called release() to
        make it larger than zero. This is done with proper interlocking so that
        if multiple acquire() calls are blocked, release() will wake exactly one
        of them up. The implementation may pick one at random, so the order in
        which blocked threads are awakened should not be relied on. There is no
        return value in this case.

        When invoked with blocking set to true, do the same thing as when called
        without arguments, and return true.

        When invoked with blocking set to false, do not block. If a call without
        an argument would block, return false immediately; otherwise, do the
        same thing as when called without arguments, and return true.

        When invoked with a timeout other than None, it will block for at
        most timeout seconds.  If acquire does not complete successfully in
        that interval, return false.  Return true otherwise.

        """
        if not blocking and timeout is not None:
            raise ValueError("can't specify timeout for non-blocking acquire")
        rc = False
        endtime = None
        with self._cond:
            while self._value == 0:
                if not blocking:
                    break
                if timeout is not None:
                    if endtime is None:
                        endtime = _time() + timeout
                    else:
                        timeout = endtime - _time()
                        if timeout <= 0:
                            break
                self._cond.wait(timeout)
            else:
                self._value -= 1
                rc = True
        return rc
    __enter__ = acquire

    def release(self, n=1):
        """Release a semaphore, incrementing the internal counter by one or more.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        """
        if n < 1:
            raise ValueError('n must be one or more')
        with self._cond:
            self._value += n
            self._cond.notify(n)

    def __exit__(self, t, v, tb):
        self.release()

class 有界信号量(信号量):
    """Implements a bounded semaphore.

    A bounded semaphore checks to make sure its current value doesn't exceed its
    initial value. If it does, ValueError is raised. In most situations
    semaphores are used to guard resources with limited capacity.

    If the semaphore is released too many times it's a sign of a bug. If not
    given, value defaults to 1.

    Like regular semaphores, bounded semaphores manage a counter representing
    the number of release() calls minus the number of acquire() calls, plus an
    initial value. The acquire() method blocks if necessary until it can return
    without making the counter negative. If not given, value defaults to 1.

    """

    def __init__(self, value=1):
        super().__init__(value)
        self._initial_value = value

    def __repr__(self):
        cls = self.__class__
        return f'<{cls.__module__}.{cls.__qualname__} at {id(self):#x}: value={self._value}/{self._initial_value}>'

    def release(self, n=1):
        """Release a semaphore, incrementing the internal counter by one or more.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        If the number of releases exceeds the number of acquires,
        raise a ValueError.

        """
        if n < 1:
            raise ValueError('n must be one or more')
        with self._cond:
            if self._value + n > self._initial_value:
                raise ValueError('Semaphore released too many times')
            self._value += n
            self._cond.notify(n)

class 事件:
    """Class implementing event objects.

    Events manage a flag that can be set to true with the set() method and reset
    to false with the clear() method. The wait() method blocks until the flag is
    true.  The flag is initially false.

    """

    def __init__(self):
        self._cond = 条件(锁())
        self._flag = False

    def __repr__(self):
        cls = self.__class__
        status = 'set' if self._flag else 'unset'
        return f'<{cls.__module__}.{cls.__qualname__} at {id(self):#x}: {status}>'

    def _at_fork_reinit(self):
        self._cond._at_fork_reinit()

    def 已置位(self):
        """Return true if and only if the internal flag is true."""
        return self._flag

    def isSet(self):
        """Return true if and only if the internal flag is true.

        This method is deprecated, use is_set() instead.

        """
        import warnings
        warnings.warn('isSet() is deprecated, use is_set() instead', DeprecationWarning, stacklevel=2)
        return self.已置位()

    def set(self):
        """Set the internal flag to true.

        All threads waiting for it to become true are awakened. Threads
        that call wait() once the flag is true will not block at all.

        """
        with self._cond:
            self._flag = True
            self._cond.notify_all()

    def clear(self):
        """Reset the internal flag to false.

        Subsequently, threads calling wait() will block until set() is called to
        set the internal flag to true again.

        """
        with self._cond:
            self._flag = False

    def 等候(self, timeout=None):
        """Block until the internal flag is true.

        If the internal flag is true on entry, return immediately. Otherwise,
        block until another thread calls set() to set the flag to true, or until
        the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating-point number specifying a timeout for the operation in seconds
        (or fractions thereof).

        This method returns the internal flag on exit, so it will always return
        ``True`` except if a timeout is given and the operation times out, when
        it will return ``False``.

        """
        with self._cond:
            signaled = self._flag
            if not signaled:
                signaled = self._cond.wait(timeout)
            return signaled
_装类转发(事件, {'is_set': '已置位', 'wait': '等候'}, {'is_set': '已置位', 'wait': '等候'})

class 栅栏:
    """Implements a Barrier.

    Useful for synchronizing a fixed number of threads at known synchronization
    points.  Threads block on 'wait()' and are simultaneously awoken once they
    have all made that call.

    """

    def __init__(self, parties, action=None, timeout=None):
        """Create a barrier, initialised to 'parties' threads.

        'action' is a callable which, when supplied, will be called by one of
        the threads after they have all entered the barrier and just prior to
        releasing them all. If a 'timeout' is provided, it is used as the
        default for all subsequent 'wait()' calls.

        """
        if parties < 1:
            raise ValueError('parties must be >= 1')
        self._cond = 条件(锁())
        self._action = action
        self._timeout = timeout
        self._parties = parties
        self._state = 0
        self._count = 0

    def __repr__(self):
        cls = self.__class__
        if self.已破损:
            return f'<{cls.__module__}.{cls.__qualname__} at {id(self):#x}: broken>'
        return f'<{cls.__module__}.{cls.__qualname__} at {id(self):#x}: waiters={self.等候数}/{self.参与数}>'

    def 等候(self, timeout=None):
        """Wait for the barrier.

        When the specified number of threads have started waiting, they are all
        simultaneously awoken. If an 'action' was provided for the barrier, one
        of the threads will have executed that callback prior to returning.
        Returns an individual index number from 0 to 'parties-1'.

        """
        if timeout is None:
            timeout = self._timeout
        with self._cond:
            self._enter()
            index = self._count
            self._count += 1
            try:
                if index + 1 == self._parties:
                    self._release()
                else:
                    self._wait(timeout)
                return index
            finally:
                self._count -= 1
                self._exit()

    def _enter(self):
        while self._state in (-1, 1):
            self._cond.wait()
        if self._state < 0:
            raise 栅栏破损错误
        assert self._state == 0

    def _release(self):
        try:
            if self._action:
                self._action()
            self._state = 1
            self._cond.notify_all()
        except:
            self._break()
            raise

    def _wait(self, timeout):
        if not self._cond.wait_for(lambda: self._state != 0, timeout):
            self._break()
            raise 栅栏破损错误
        if self._state < 0:
            raise 栅栏破损错误
        assert self._state == 1

    def _exit(self):
        if self._count == 0:
            if self._state in (-1, 1):
                self._state = 0
                self._cond.notify_all()

    def 重置(self):
        """Reset the barrier to the initial state.

        Any threads currently waiting will get the BrokenBarrier exception
        raised.

        """
        with self._cond:
            if self._count > 0:
                if self._state == 0:
                    self._state = -1
                elif self._state == -2:
                    self._state = -1
            else:
                self._state = 0
            self._cond.notify_all()

    def 中止(self):
        """Place the barrier into a 'broken' state.

        Useful in case of error.  Any currently waiting threads and threads
        attempting to 'wait()' will have BrokenBarrierError raised.

        """
        with self._cond:
            self._break()

    def _break(self):
        self._state = -2
        self._cond.notify_all()

    @property
    def 参与数(self):
        """Return the number of threads required to trip the barrier."""
        return self._parties

    @property
    def 等候数(self):
        """Return the number of threads currently waiting at the barrier."""
        if self._state == 0:
            return self._count
        return 0

    @property
    def 已破损(self):
        """Return True if the barrier is in a broken state."""
        return self._state == -2
_装类转发(栅栏, {'abort': '中止', 'broken': '已破损', 'n_waiting': '等候数', 'parties': '参与数', 'reset': '重置', 'wait': '等候'}, {'abort': '中止', 'broken': '已破损', 'n_waiting': '等候数', 'parties': '参与数', 'reset': '重置', 'wait': '等候'})

class 栅栏破损错误(RuntimeError):
    pass
_counter = _count(1).__next__

def _newname(name_template):
    return name_template % _counter()
_active_limbo_lock = 可重入锁()
_active = {}
_limbo = {}
_dangling = WeakSet()

class 线程:
    """A class that represents a thread of control.

    This class can be safely subclassed in a limited fashion. There are two ways
    to specify the activity: by passing a callable object to the constructor, or
    by overriding the run() method in a subclass.

    """
    _initialized = False

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None, context=None):
        """This constructor should always be called with keyword arguments. Arguments are:

        *group* should be None; reserved for future extension when a ThreadGroup
        class is implemented.

        *target* is the callable object to be invoked by the run()
        method. Defaults to None, meaning nothing is called.

        *name* is the thread name. By default, a unique name is constructed of
        the form "Thread-N" where N is a small decimal number.

        *args* is a list or tuple of arguments for the target invocation. Defaults to ().

        *kwargs* is a dictionary of keyword arguments for the target
        invocation. Defaults to {}.

        *context* is the contextvars.Context value to use for the thread.
        The default value is None, which means to check
        sys.flags.thread_inherit_context.  If that flag is true, use a copy
        of the context of the caller.  If false, use an empty context.  To
        explicitly start with an empty context, pass a new instance of
        contextvars.Context().  To explicitly start with a copy of the current
        context, pass the value from contextvars.copy_context().

        If a subclass overrides the constructor, it must make sure to invoke
        the base class constructor (Thread.__init__()) before doing anything
        else to the thread.

        """
        assert group is None, 'group argument must be None for now'
        if kwargs is None:
            kwargs = {}
        if name:
            name = str(name)
        else:
            name = _newname('Thread-%d')
            if target is not None:
                try:
                    target_name = target.__name__
                    name += f' ({target_name})'
                except AttributeError:
                    pass
        self._target = target
        self._name = name
        self._args = args
        self._kwargs = kwargs
        if daemon is not None:
            if daemon and (not _daemon_threads_allowed()):
                raise RuntimeError('daemon threads are disabled in this (sub)interpreter')
            self._daemonic = daemon
        else:
            self._daemonic = 当前线程().daemon
        self._context = context
        self._ident = None
        if _HAVE_THREAD_NATIVE_ID:
            self._native_id = None
        self._os_thread_handle = _ThreadHandle()
        self._started = 事件()
        self._initialized = True
        self._stderr = _sys.stderr
        self._invoke_excepthook = _make_invoke_excepthook()
        _dangling.add(self)

    def _after_fork(self, new_ident=None):
        self._started._at_fork_reinit()
        if new_ident is not None:
            self._ident = new_ident
            assert self._os_thread_handle.ident == new_ident
            if _HAVE_THREAD_NATIVE_ID:
                self._set_native_id()
        else:
            pass

    def __repr__(self):
        assert self._initialized, 'Thread.__init__() was not called'
        status = 'initial'
        if self._started.is_set():
            status = 'started'
        if self._os_thread_handle.is_done():
            status = 'stopped'
        if self._daemonic:
            status += ' daemon'
        if self._ident is not None:
            status += ' %s' % self._ident
        return '<%s(%s, %s)>' % (self.__class__.__name__, self._name, status)

    def 启动(self):
        """Start the thread's activity.

        It must be called at most once per thread object. It arranges for the
        object's run() method to be invoked in a separate thread of control.

        This method will raise a RuntimeError if called more than once on the
        same thread object.

        """
        if not self._initialized:
            raise RuntimeError('thread.__init__() not called')
        if self._started.is_set():
            raise RuntimeError('threads can only be started once')
        with _active_limbo_lock:
            _limbo[self] = self
        if self._context is None:
            if _sys.flags.thread_inherit_context:
                self._context = _contextvars.copy_context()
            else:
                self._context = _contextvars.Context()
        try:
            _start_joinable_thread(self._bootstrap, handle=self._os_thread_handle, daemon=self.守护)
        except Exception:
            with _active_limbo_lock:
                del _limbo[self]
            raise
        self._started.wait()

    def run(self):
        """Method representing the thread's activity.

        You may override this method in a subclass. The standard run() method
        invokes the callable object passed to the object's constructor as the
        target argument, if any, with sequential and keyword arguments taken
        from the args and kwargs arguments, respectively.

        """
        try:
            if self._target is not None:
                self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

    def _bootstrap(self):
        try:
            self._bootstrap_inner()
        except:
            if self._daemonic and _sys is None:
                return
            raise

    def _set_ident(self):
        self._ident = 取线程标识()
    if _HAVE_THREAD_NATIVE_ID:

        def _set_native_id(self):
            self._native_id = 取本机线程号()

    def _set_os_name(self):
        if _set_name is None or not self._name:
            return
        try:
            _set_name(self._name)
        except OSError:
            pass

    def _bootstrap_inner(self):
        try:
            self._set_ident()
            if _HAVE_THREAD_NATIVE_ID:
                self._set_native_id()
            self._set_os_name()
            self._started.set()
            with _active_limbo_lock:
                _active[self._ident] = self
                del _limbo[self]
            if _trace_hook:
                _sys.settrace(_trace_hook)
            if _profile_hook:
                _sys.setprofile(_profile_hook)
            try:
                self._context.run(self.run)
            except:
                self._invoke_excepthook(self)
        finally:
            self._delete()

    def _delete(self):
        """Remove current thread from the dict of currently running threads."""
        with _active_limbo_lock:
            del _active[取线程标识()]

    def join(self, timeout=None):
        """Wait until the thread terminates.

        This blocks the calling thread until the thread whose join() method is
        called terminates -- either normally or through an unhandled exception
        or until the optional timeout occurs.

        When the timeout argument is present and not None, it should be a
        floating-point number specifying a timeout for the operation in seconds
        (or fractions thereof). As join() always returns None, you must call
        is_alive() after join() to decide whether a timeout happened -- if the
        thread is still alive, the join() call timed out.

        When the timeout argument is not present or None, the operation will
        block until the thread terminates.

        A thread can be join()ed many times.

        join() raises a RuntimeError if an attempt is made to join the current
        thread as that would cause a deadlock. It is also an error to join() a
        thread before it has been started and attempts to do so raises the same
        exception.

        """
        if not self._initialized:
            raise RuntimeError('Thread.__init__() not called')
        if not self._started.is_set():
            raise RuntimeError('cannot join thread before it is started')
        if self is 当前线程():
            raise RuntimeError('cannot join current thread')
        if timeout is not None:
            timeout = max(timeout, 0)
        self._os_thread_handle.join(timeout)

    @property
    def 名字(self):
        """A string used for identification purposes only.

        It has no semantics. Multiple threads may be given the same name. The
        initial name is set by the constructor.

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._name

    @名字.setter
    def 名字(self, name):
        assert self._initialized, 'Thread.__init__() not called'
        self._name = str(name)
        if 取线程标识() == self._ident:
            self._set_os_name()

    @property
    def 标识(self):
        """Thread identifier of this thread or None if it has not been started.

        This is a nonzero integer. See the get_ident() function. Thread
        identifiers may be recycled when a thread exits and another thread is
        created. The identifier is available even after the thread has exited.

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._ident
    if _HAVE_THREAD_NATIVE_ID:

        @property
        def 本机线程号(self):
            """Native integral thread ID of this thread, or None if it has not been started.

            This is a non-negative integer. See the get_native_id() function.
            This represents the Thread ID as reported by the kernel.

            """
            assert self._initialized, 'Thread.__init__() not called'
            return self._native_id

    def 存活吗(self):
        """Return whether the thread is alive.

        This method returns True just before the run() method starts until just
        after the run() method terminates. See also the module function
        enumerate().

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._started.is_set() and (not self._os_thread_handle.is_done())

    @property
    def 守护(self):
        """A boolean value indicating whether this thread is a daemon thread.

        This must be set before start() is called, otherwise RuntimeError is
        raised. Its initial value is inherited from the creating thread; the
        main thread is not a daemon thread and therefore all threads created in
        the main thread default to daemon = False.

        The entire Python program exits when only daemon threads are left.

        """
        assert self._initialized, 'Thread.__init__() not called'
        return self._daemonic

    @守护.setter
    def 守护(self, daemonic):
        if not self._initialized:
            raise RuntimeError('Thread.__init__() not called')
        if daemonic and (not _daemon_threads_allowed()):
            raise RuntimeError('daemon threads are disabled in this interpreter')
        if self._started.is_set():
            raise RuntimeError('cannot set daemon status of active thread')
        self._daemonic = daemonic

    def isDaemon(self):
        """Return whether this thread is a daemon.

        This method is deprecated, use the daemon attribute instead.

        """
        import warnings
        warnings.warn('isDaemon() is deprecated, get the daemon attribute instead', DeprecationWarning, stacklevel=2)
        return self.守护

    def setDaemon(self, daemonic):
        """Set whether this thread is a daemon.

        This method is deprecated, use the .daemon property instead.

        """
        import warnings
        warnings.warn('setDaemon() is deprecated, set the daemon attribute instead', DeprecationWarning, stacklevel=2)
        self.守护 = daemonic

    def getName(self):
        """Return a string used for identification purposes only.

        This method is deprecated, use the name attribute instead.

        """
        import warnings
        warnings.warn('getName() is deprecated, get the name attribute instead', DeprecationWarning, stacklevel=2)
        return self.名字

    def setName(self, name):
        """Set the name string for this thread.

        This method is deprecated, use the name attribute instead.

        """
        import warnings
        warnings.warn('setName() is deprecated, set the name attribute instead', DeprecationWarning, stacklevel=2)
        self.名字 = name
_装类转发(线程, {'daemon': '守护', 'ident': '标识', 'is_alive': '存活吗', 'name': '名字', 'native_id': '本机线程号', 'start': '启动'}, {'daemon': '守护', 'ident': '标识', 'is_alive': '存活吗', 'name': '名字', 'native_id': '本机线程号', 'start': '启动'})
try:
    from _thread import _excepthook as excepthook, _ExceptHookArgs as ExceptHookArgs
except ImportError:
    from traceback import print_exception as _print_exception
    from collections import namedtuple
    _ExceptHookArgs = namedtuple('ExceptHookArgs', 'exc_type exc_value exc_traceback thread')

    def ExceptHookArgs(args):
        return _ExceptHookArgs(*args)

    def excepthook(args, /):
        """
        Handle uncaught Thread.run() exception.
        """
        if args.exc_type == SystemExit:
            return
        if _sys is not None and _sys.stderr is not None:
            stderr = _sys.stderr
        elif args.thread is not None:
            stderr = args.thread._stderr
            if stderr is None:
                return
        else:
            return
        if args.thread is not None:
            名字 = args.thread.name
        else:
            名字 = 取线程标识()
        print(f'Exception in thread {名字}:', file=stderr, flush=True)
        _print_exception(args.exc_type, args.exc_value, args.exc_traceback, file=stderr)
        stderr.flush()
__excepthook__ = excepthook

def _make_invoke_excepthook():
    old_excepthook = excepthook
    old_sys_excepthook = _sys.excepthook
    if old_excepthook is None:
        raise RuntimeError('threading.excepthook is None')
    if old_sys_excepthook is None:
        raise RuntimeError('sys.excepthook is None')
    sys_exc_info = _sys.exc_info
    local_print = print
    local_sys = _sys

    def invoke_excepthook(thread):
        global excepthook
        try:
            hook = excepthook
            if hook is None:
                hook = old_excepthook
            args = ExceptHookArgs([*sys_exc_info(), thread])
            hook(args)
        except Exception as exc:
            exc.__suppress_context__ = True
            del exc
            if local_sys is not None and local_sys.stderr is not None:
                stderr = local_sys.stderr
            else:
                stderr = thread._stderr
            local_print('Exception in threading.excepthook:', file=stderr, flush=True)
            if local_sys is not None and local_sys.excepthook is not None:
                sys_excepthook = local_sys.excepthook
            else:
                sys_excepthook = old_sys_excepthook
            sys_excepthook(*sys_exc_info())
        finally:
            args = None
    return invoke_excepthook

class 定时器(线程):
    """Call a function after a specified number of seconds:

            t = Timer(30.0, f, args=None, kwargs=None)
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting

    """

    def __init__(self, interval, function, args=None, kwargs=None):
        线程.__init__(self)
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.finished = 事件()

    def 取消(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def run(self):
        self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()
_装类转发(定时器, {'cancel': '取消'}, {'cancel': '取消'})

class _MainThread(线程):

    def __init__(self):
        线程.__init__(self, name='MainThread', daemon=False)
        self._started.set()
        self._ident = _get_main_thread_ident()
        self._os_thread_handle = _make_thread_handle(self._ident)
        if _HAVE_THREAD_NATIVE_ID:
            self._set_native_id()
        with _active_limbo_lock:
            _active[self._ident] = self
_thread_local_info = local()

class _DeleteDummyThreadOnDel:
    """
    Helper class to remove a dummy thread from threading._active on __del__.
    """

    def __init__(self, dummy_thread):
        self._dummy_thread = dummy_thread
        self._tident = dummy_thread.ident
        _thread_local_info._track_dummy_thread_ref = self

    def __del__(self, _active_limbo_lock=_active_limbo_lock, _active=_active):
        with _active_limbo_lock:
            if _active.get(self._tident) is self._dummy_thread:
                _active.pop(self._tident, None)

class _DummyThread(线程):

    def __init__(self):
        线程.__init__(self, name=_newname('Dummy-%d'), daemon=_daemon_threads_allowed())
        self._started.set()
        self._set_ident()
        self._os_thread_handle = _make_thread_handle(self._ident)
        if _HAVE_THREAD_NATIVE_ID:
            self._set_native_id()
        with _active_limbo_lock:
            _active[self._ident] = self
        _DeleteDummyThreadOnDel(self)

    def 存活吗(self):
        if not self._os_thread_handle.is_done() and self._started.is_set():
            return True
        raise RuntimeError('thread is not alive')

    def join(self, timeout=None):
        raise RuntimeError('cannot join a dummy thread')

    def _after_fork(self, new_ident=None):
        if new_ident is not None:
            self.__class__ = _MainThread
            self._name = 'MainThread'
            self._daemonic = False
        线程._after_fork(self, new_ident=new_ident)
_装类转发(_DummyThread, {'is_alive': '存活吗'}, {'is_alive': '存活吗'})

def 当前线程():
    """Return the current Thread object, corresponding to the caller's thread of control.

    If the caller's thread of control was not created through the threading
    module, a dummy thread object with limited functionality is returned.

    """
    try:
        return _active[取线程标识()]
    except KeyError:
        return _DummyThread()

def currentThread():
    """Return the current Thread object, corresponding to the caller's thread of control.

    This function is deprecated, use current_thread() instead.

    """
    import warnings
    warnings.warn('currentThread() is deprecated, use current_thread() instead', DeprecationWarning, stacklevel=2)
    return 当前线程()

def 活动线程数():
    """Return the number of Thread objects currently alive.

    The returned count is equal to the length of the list returned by
    enumerate().

    """
    with _active_limbo_lock:
        return len(_active) + len(_limbo)

def activeCount():
    """Return the number of Thread objects currently alive.

    This function is deprecated, use active_count() instead.

    """
    import warnings
    warnings.warn('activeCount() is deprecated, use active_count() instead', DeprecationWarning, stacklevel=2)
    return 活动线程数()

def _enumerate():
    return list(_active.values()) + list(_limbo.values())

def enumerate():
    """Return a list of all Thread objects currently alive.

    The list includes daemonic threads, dummy thread objects created by
    current_thread(), and the main thread. It excludes terminated threads and
    threads that have not yet been started.

    """
    with _active_limbo_lock:
        return list(_active.values()) + list(_limbo.values())
_threading_atexits = []
_SHUTTING_DOWN = False

def _register_atexit(func, *arg, **kwargs):
    """CPython internal: register *func* to be called before joining threads.

    The registered *func* is called with its arguments just before all
    non-daemon threads are joined in `_shutdown()`. It provides a similar
    purpose to `atexit.register()`, but its functions are called prior to
    threading shutdown instead of interpreter shutdown.

    For similarity to atexit, the registered functions are called in reverse.
    """
    if _SHUTTING_DOWN:
        raise RuntimeError("can't register atexit after shutdown")
    _threading_atexits.append(lambda: func(*arg, **kwargs))
from _thread import stack_size
_main_thread = _MainThread()

def _shutdown():
    """
    Wait until the Python thread state of all non-daemon threads get deleted.
    """
    if _main_thread._os_thread_handle.is_done() and _is_main_interpreter():
        return
    global _SHUTTING_DOWN
    _SHUTTING_DOWN = True
    for atexit_call in reversed(_threading_atexits):
        atexit_call()
    if _is_main_interpreter():
        _main_thread._os_thread_handle._set_done()
    _thread_shutdown()

def 主线程():
    """Return the main thread object.

    In normal conditions, the main thread is the thread from which the
    Python interpreter was started.
    """
    return _main_thread

def _after_fork():
    """
    Cleanup threading module state that should not exist after a fork.
    """
    global _active_limbo_lock, _main_thread
    _active_limbo_lock = 可重入锁()
    new_active = {}
    try:
        current = _active[取线程标识()]
    except KeyError:
        current = _MainThread()
    _main_thread = current
    with _active_limbo_lock:
        threads = set(_enumerate())
        threads.update(_dangling)
        for thread in threads:
            if thread is current:
                标识 = 取线程标识()
                thread._after_fork(new_ident=标识)
                new_active[标识] = thread
            else:
                thread._after_fork()
        _limbo.clear()
        _active.clear()
        _active.update(new_active)
        assert len(_active) == 1
if hasattr(_os, 'register_at_fork'):
    _os.register_at_fork(after_in_child=_after_fork)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Barrier': '栅栏',
    'BoundedSemaphore': '有界信号量',
    'BrokenBarrierError': '栅栏破损错误',
    'Condition': '条件',
    'Event': '事件',
    'Lock': '锁',
    'RLock': '可重入锁',
    'Semaphore': '信号量',
    'TIMEOUT_MAX': '超时上限',
    'Thread': '线程',
    'ThreadError': '线程错误',
    'Timer': '定时器',
    'active_count': '活动线程数',
    'current_thread': '当前线程',
    'get_ident': '取线程标识',
    'get_native_id': '取本机线程号',
    'getprofile': '取性能钩子',
    'gettrace': '取跟踪钩子',
    'main_thread': '主线程',
    'setprofile': '设性能钩子',
    'setprofile_all_threads': '设全线程性能钩子',
    'settrace': '设跟踪钩子',
    'settrace_all_threads': '设全线程跟踪钩子',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '_DummyThread': {
        'is_alive': '存活吗',
    },
    '事件': {
        'is_set': '已置位',
        'wait': '等候',
    },
    '定时器': {
        'cancel': '取消',
    },
    '条件': {
        'notify': '通知',
        'notify_all': '通知全部',
        'wait': '等候',
        'wait_for': '等候直到',
    },
    '栅栏': {
        'abort': '中止',
        'broken': '已破损',
        'n_waiting': '等候数',
        'parties': '参与数',
        'reset': '重置',
        'wait': '等候',
    },
    '线程': {
        'daemon': '守护',
        'ident': '标识',
        'is_alive': '存活吗',
        'name': '名字',
        'native_id': '本机线程号',
        'start': '启动',
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
    '_DummyThread': {
        'is_alive': '存活吗',
    },
    '事件': {
        'is_set': '已置位',
        'wait': '等候',
    },
    '定时器': {
        'cancel': '取消',
    },
    '条件': {
        'notify': '通知',
        'notify_all': '通知全部',
        'wait': '等候',
        'wait_for': '等候直到',
    },
    '栅栏': {
        'abort': '中止',
        'broken': '已破损',
        'n_waiting': '等候数',
        'parties': '参与数',
        'reset': '重置',
        'wait': '等候',
    },
    '线程': {
        'daemon': '守护',
        'ident': '标识',
        'is_alive': '存活吗',
        'name': '名字',
        'native_id': '本机线程号',
        'start': '启动',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '主线程',
    '事件',
    '信号量',
    '取性能钩子',
    '取本机线程号',
    '取线程标识',
    '取跟踪钩子',
    '可重入锁',
    '定时器',
    '当前线程',
    '有界信号量',
    '条件',
    '栅栏',
    '栅栏破损错误',
    '活动线程数',
    '线程',
    '线程错误',
    '设全线程性能钩子',
    '设全线程跟踪钩子',
    '设性能钩子',
    '设跟踪钩子',
    '超时上限',
    '锁',
]

# ---- 转发层结束 ----
