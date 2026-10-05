# -*- coding: utf-8 -*-
"""并行.futures/_base —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/futures/_base.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.futures/_base.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


_英文原名表 = {'ALL_COMPLETED': '全部完成', 'BrokenExecutor': '执行器损坏错误', 'CANCELLED': '已取消', 'CANCELLED_AND_NOTIFIED': '已取消且已通知', 'CancelledError': '已取消错误', 'DoneAndNotDoneFutures': '完成情况', 'Error': '错误', 'Executor': '执行器', 'FINISHED': '已完成', 'FIRST_COMPLETED': '最先完成', 'FIRST_EXCEPTION': '最先异常', 'Future': '未来对象', 'InvalidStateError': '状态无效错误', 'LOGGER': '日志器', 'PENDING': '未开始', 'RUNNING': '运行中', 'as_completed': '完成即取', 'wait': '等待完成'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
import collections
import logging
import threading
import time
import types
import weakref
from itertools import islice
最先完成 = 'FIRST_COMPLETED'
最先异常 = 'FIRST_EXCEPTION'
全部完成 = 'ALL_COMPLETED'
_AS_COMPLETED = '_AS_COMPLETED'
未开始 = 'PENDING'
运行中 = 'RUNNING'
已取消 = 'CANCELLED'
已取消且已通知 = 'CANCELLED_AND_NOTIFIED'
已完成 = 'FINISHED'
_STATE_TO_DESCRIPTION_MAP = {未开始: 'pending', 运行中: 'running', 已取消: 'cancelled', 已取消且已通知: 'cancelled', 已完成: 'finished'}
日志器 = logging.getLogger('concurrent.futures')

class 错误(Exception):
    """Base class for all future-related exceptions."""
    pass
import concurrent.futures._base as _英文身份源
错误 = _英文身份源.Error

class 已取消错误(错误):
    """The Future was cancelled."""
    pass
import concurrent.futures._base as _英文身份源
已取消错误 = _英文身份源.CancelledError
TimeoutError = TimeoutError

class 状态无效错误(错误):
    """The operation is not allowed in this state."""
    pass
import concurrent.futures._base as _英文身份源
状态无效错误 = _英文身份源.InvalidStateError

class _Waiter(object):
    """Provides the event that wait() and as_completed() block on."""

    def __init__(self):
        self.event = threading.Event()
        self.finished_futures = []

    def add_result(self, future):
        self.finished_futures.append(future)

    def add_exception(self, future):
        self.finished_futures.append(future)

    def add_cancelled(self, future):
        self.finished_futures.append(future)

class _AsCompletedWaiter(_Waiter):
    """Used by as_completed()."""

    def __init__(self):
        super(_AsCompletedWaiter, self).__init__()
        self.lock = threading.Lock()

    def add_result(self, future):
        with self.lock:
            super(_AsCompletedWaiter, self).add_result(future)
            self.event.set()

    def add_exception(self, future):
        with self.lock:
            super(_AsCompletedWaiter, self).add_exception(future)
            self.event.set()

    def add_cancelled(self, future):
        with self.lock:
            super(_AsCompletedWaiter, self).add_cancelled(future)
            self.event.set()

class _FirstCompletedWaiter(_Waiter):
    """Used by wait(return_when=FIRST_COMPLETED)."""

    def add_result(self, future):
        super().add_result(future)
        self.event.set()

    def add_exception(self, future):
        super().add_exception(future)
        self.event.set()

    def add_cancelled(self, future):
        super().add_cancelled(future)
        self.event.set()

class _AllCompletedWaiter(_Waiter):
    """Used by wait(return_when=FIRST_EXCEPTION and ALL_COMPLETED)."""

    def __init__(self, num_pending_calls, stop_on_exception):
        self.num_pending_calls = num_pending_calls
        self.stop_on_exception = stop_on_exception
        self.lock = threading.Lock()
        super().__init__()

    def _decrement_pending_calls(self):
        with self.lock:
            self.num_pending_calls -= 1
            if not self.num_pending_calls:
                self.event.set()

    def add_result(self, future):
        super().add_result(future)
        self._decrement_pending_calls()

    def add_exception(self, future):
        super().add_exception(future)
        if self.stop_on_exception:
            self.event.set()
        else:
            self._decrement_pending_calls()

    def add_cancelled(self, future):
        super().add_cancelled(future)
        self._decrement_pending_calls()

class _AcquireFutures(object):
    """A context manager that does an ordered acquire of Future conditions."""

    def __init__(self, futures):
        self.futures = sorted(futures, key=id)

    def __enter__(self):
        for future in self.futures:
            future._condition.acquire()

    def __exit__(self, *args):
        for future in self.futures:
            future._condition.release()

def _create_and_install_waiters(fs, return_when):
    if return_when == _AS_COMPLETED:
        waiter = _AsCompletedWaiter()
    elif return_when == 最先完成:
        waiter = _FirstCompletedWaiter()
    else:
        pending_count = sum((f._state not in [已取消且已通知, 已完成] for f in fs))
        if return_when == 最先异常:
            waiter = _AllCompletedWaiter(pending_count, stop_on_exception=True)
        elif return_when == 全部完成:
            waiter = _AllCompletedWaiter(pending_count, stop_on_exception=False)
        else:
            raise ValueError('Invalid return condition: %r' % return_when)
    for f in fs:
        f._waiters.append(waiter)
    return waiter

def _yield_finished_futures(fs, waiter, ref_collect):
    """
    Iterate on the list *fs*, yielding finished futures one by one in
    reverse order.
    Before yielding a future, *waiter* is removed from its waiters
    and the future is removed from each set in the collection of sets
    *ref_collect*.

    The aim of this function is to avoid keeping stale references after
    the future is yielded and before the iterator resumes.
    """
    while fs:
        f = fs[-1]
        for futures_set in ref_collect:
            futures_set.remove(f)
        with f._condition:
            f._waiters.remove(waiter)
        del f
        yield fs.pop()

def 完成即取(fs, timeout=None):
    """An iterator over the given futures that yields each as it completes.

    Args:
        fs: The sequence of Futures (possibly created by different
            Executors) to iterate over.
        timeout: The maximum number of seconds to wait.  If None, then
            there is no limit on the wait time.

    Returns:
        An iterator that yields the given Futures as they complete
        (finished or cancelled).  If any given Futures are duplicated,
        they will be returned once.

    Raises:
        TimeoutError: If the entire result iterator could not be generated
            before the given timeout.
    """
    if timeout is not None:
        end_time = timeout + time.monotonic()
    fs = set(fs)
    total_futures = len(fs)
    with _AcquireFutures(fs):
        finished = set((f for f in fs if f._state in [已取消且已通知, 已完成]))
        pending = fs - finished
        waiter = _create_and_install_waiters(fs, _AS_COMPLETED)
    finished = list(finished)
    try:
        yield from _yield_finished_futures(finished, waiter, ref_collect=(fs,))
        while pending:
            if timeout is None:
                wait_timeout = None
            else:
                wait_timeout = end_time - time.monotonic()
                if wait_timeout < 0:
                    raise TimeoutError('%d (of %d) futures unfinished' % (len(pending), total_futures))
            waiter.event.wait(wait_timeout)
            with waiter.lock:
                finished = waiter.finished_futures
                waiter.finished_futures = []
                waiter.event.clear()
            finished.reverse()
            yield from _yield_finished_futures(finished, waiter, ref_collect=(fs, pending))
    finally:
        for f in fs:
            with f._condition:
                f._waiters.remove(waiter)
完成情况 = collections.namedtuple('DoneAndNotDoneFutures', 'done not_done')

def 等待完成(fs, timeout=None, return_when=全部完成):
    """Wait for the futures in the given sequence to complete.

    Args:
        fs: The sequence of Futures (possibly created by different
            Executors) to wait upon.
        timeout: The maximum number of seconds to wait.  If None, then
            there is no limit on the wait time.
        return_when: Indicates when this function should return.
            The options are:

            FIRST_COMPLETED - Return when any future finishes or is
                              cancelled.
            FIRST_EXCEPTION - Return when any future finishes by raising an
                              exception.  If no future raises an exception
                              then it is equivalent to ALL_COMPLETED.
            ALL_COMPLETED -   Return when all futures finish or are
                              cancelled.

    Returns:
        A named 2-tuple of sets. The first set, named 'done', contains the
        futures that completed (is finished or cancelled) before the wait
        completed. The second set, named 'not_done', contains uncompleted
        futures. Duplicate futures given to *fs* are removed and will be
        returned only once.
    """
    fs = set(fs)
    with _AcquireFutures(fs):
        done = {f for f in fs if f._state in [已取消且已通知, 已完成]}
        not_done = fs - done
        if return_when == 最先完成 and done:
            return 完成情况(done, not_done)
        elif return_when == 最先异常 and done:
            if any((f for f in done if not f.cancelled() and f.exception() is not None)):
                return 完成情况(done, not_done)
        if len(done) == len(fs):
            return 完成情况(done, not_done)
        waiter = _create_and_install_waiters(fs, return_when)
    waiter.event.wait(timeout)
    for f in fs:
        with f._condition:
            f._waiters.remove(waiter)
    done.update(waiter.finished_futures)
    return 完成情况(done, fs - done)

def _result_or_cancel(fut, timeout=None):
    try:
        try:
            return fut.result(timeout)
        finally:
            fut.cancel()
    finally:
        del fut

class 未来对象(object):
    """Represents the result of an asynchronous computation."""

    def __init__(self):
        """Initializes the future. Should not be called by clients."""
        self._condition = threading.Condition()
        self._state = 未开始
        self._result = None
        self._exception = None
        self._waiters = []
        self._done_callbacks = []

    def _invoke_callbacks(self):
        for callback in self._done_callbacks:
            try:
                callback(self)
            except Exception:
                日志器.exception('exception calling callback for %r', self)

    def __repr__(self):
        with self._condition:
            if self._state == 已完成:
                if self._exception:
                    return '<%s at %#x state=%s raised %s>' % (self.__class__.__name__, id(self), _STATE_TO_DESCRIPTION_MAP[self._state], self._exception.__class__.__name__)
                else:
                    return '<%s at %#x state=%s returned %s>' % (self.__class__.__name__, id(self), _STATE_TO_DESCRIPTION_MAP[self._state], self._result.__class__.__name__)
            return '<%s at %#x state=%s>' % (self.__class__.__name__, id(self), _STATE_TO_DESCRIPTION_MAP[self._state])

    def cancel(self):
        """Cancel the future if possible.

        Returns True if the future was cancelled, False otherwise. A future
        cannot be cancelled if it is running or has already completed.
        """
        with self._condition:
            if self._state in [运行中, 已完成]:
                return False
            if self._state in [已取消, 已取消且已通知]:
                return True
            self._state = 已取消
            self._condition.notify_all()
        self._invoke_callbacks()
        return True

    def cancelled(self):
        """Return True if the future was cancelled."""
        with self._condition:
            return self._state in [已取消, 已取消且已通知]

    def running(self):
        """Return True if the future is currently executing."""
        with self._condition:
            return self._state == 运行中

    def done(self):
        """Return True if the future was cancelled or finished executing."""
        with self._condition:
            return self._state in [已取消, 已取消且已通知, 已完成]

    def __get_result(self):
        if self._exception is not None:
            try:
                raise self._exception
            finally:
                self = None
        else:
            return self._result

    def add_done_callback(self, fn):
        """Attaches a callable that will be called when the future finishes.

        Args:
            fn: A callable that will be called with this future as its only
                argument when the future completes or is cancelled.  The
                callable will always be called by a thread in the same
                process in which it was added.  If the future has already
                completed or been cancelled then the callable will be
                called immediately.  These callables are called in the
                order that they were added.
        """
        with self._condition:
            if self._state not in [已取消, 已取消且已通知, 已完成]:
                self._done_callbacks.append(fn)
                return
        try:
            fn(self)
        except Exception:
            日志器.exception('exception calling callback for %r', self)

    def result(self, timeout=None):
        """Return the result of the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the result if the
                future isn't done.  If None, then there is no limit on the
                wait time.

        Returns:
            The result of the call that the future represents.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the
                given timeout.
            Exception: If the call raised then that exception will be
                raised.
        """
        try:
            with self._condition:
                if self._state in [已取消, 已取消且已通知]:
                    raise 已取消错误()
                elif self._state == 已完成:
                    return self.__get_result()
                self._condition.wait(timeout)
                if self._state in [已取消, 已取消且已通知]:
                    raise 已取消错误()
                elif self._state == 已完成:
                    return self.__get_result()
                else:
                    raise TimeoutError()
        finally:
            self = None

    def exception(self, timeout=None):
        """Return the exception raised by the call that the future represents.

        Args:
            timeout: The number of seconds to wait for the exception if the
                future isn't done.  If None, then there is no limit on the
                wait time.

        Returns:
            The exception raised by the call that the future represents or
            None if the call completed without raising.

        Raises:
            CancelledError: If the future was cancelled.
            TimeoutError: If the future didn't finish executing before the
                given timeout.
        """
        with self._condition:
            if self._state in [已取消, 已取消且已通知]:
                raise 已取消错误()
            elif self._state == 已完成:
                return self._exception
            self._condition.wait(timeout)
            if self._state in [已取消, 已取消且已通知]:
                raise 已取消错误()
            elif self._state == 已完成:
                return self._exception
            else:
                raise TimeoutError()

    def set_running_or_notify_cancel(self):
        """Mark the future as running or process any cancel notifications.

        Should only be used by Executor implementations and unit tests.

        If the future has been cancelled (cancel() was called and returned
        True) then any threads waiting on the future completing (though
        calls to as_completed() or wait()) are notified and False is
        returned.

        If the future was not cancelled then it is put in the running state
        (future calls to running() will return True) and True is returned.

        This method should be called by Executor implementations before
        executing the work associated with this future. If this method
        returns False then the work should not be executed.

        Returns:
            False if the Future was cancelled, True otherwise.

        Raises:
            RuntimeError: if this method was already called or if
                set_result() or set_exception() was called.
        """
        with self._condition:
            if self._state == 已取消:
                self._state = 已取消且已通知
                for waiter in self._waiters:
                    waiter.add_cancelled(self)
                return False
            elif self._state == 未开始:
                self._state = 运行中
                return True
            else:
                日志器.critical('Future %s in unexpected state: %s', id(self), self._state)
                raise RuntimeError('Future in unexpected state')

    def set_result(self, result):
        """Sets the return value of work associated with the future.

        Should only be used by Executor implementations and unit tests.
        """
        with self._condition:
            if self._state in {已取消, 已取消且已通知, 已完成}:
                raise 状态无效错误('{}: {!r}'.format(self._state, self))
            self._result = result
            self._state = 已完成
            for waiter in self._waiters:
                waiter.add_result(self)
            self._condition.notify_all()
        self._invoke_callbacks()

    def set_exception(self, exception):
        """Sets the result of the future as being the given exception.

        Should only be used by Executor implementations and unit tests.
        """
        with self._condition:
            if self._state in {已取消, 已取消且已通知, 已完成}:
                raise 状态无效错误('{}: {!r}'.format(self._state, self))
            self._exception = exception
            self._state = 已完成
            for waiter in self._waiters:
                waiter.add_exception(self)
            self._condition.notify_all()
        self._invoke_callbacks()
    __class_getitem__ = classmethod(types.GenericAlias)
import concurrent.futures._base as _英文身份源
未来对象 = _英文身份源.Future

class 执行器(object):
    """This is an abstract base class for concrete asynchronous executors."""

    def submit(self, fn, /, *args, **kwargs):
        """Submits a callable to be executed with the given arguments.

        Schedules the callable to be executed as fn(*args, **kwargs) and
        returns a Future instance representing the execution of the
        callable.

        Returns:
            A Future representing the given call.
        """
        raise NotImplementedError()

    def map(self, fn, *iterables, timeout=None, chunksize=1, buffersize=None):
        """Returns an iterator equivalent to map(fn, iter).

        Args:
            fn: A callable that will take as many arguments as there are
                passed iterables.
            timeout: The maximum number of seconds to wait. If None, then
                there is no limit on the wait time.
            chunksize: The size of the chunks the iterable will be broken
                into before being passed to a child process.  This argument
                is only used by ProcessPoolExecutor; it is ignored by
                ThreadPoolExecutor.
            buffersize: The number of submitted tasks whose results have not
                yet been yielded.  If the buffer is full, iteration over the
                iterables pauses until a result is yielded from the buffer.
                If None, all input elements are eagerly collected, and
                a task is submitted for each.

        Returns:
            An iterator equivalent to: map(func, *iterables) but the calls
            may be evaluated out-of-order.

        Raises:
            TimeoutError: If the entire result iterator could not be
                generated before the given timeout.
            Exception: If fn(*args) raises for any values.
        """
        if buffersize is not None and (not isinstance(buffersize, int)):
            raise TypeError('buffersize must be an integer or None')
        if buffersize is not None and buffersize < 1:
            raise ValueError('buffersize must be None or > 0')
        if timeout is not None:
            end_time = timeout + time.monotonic()
        zipped_iterables = zip(*iterables)
        if buffersize:
            fs = collections.deque((self.submit(fn, *args) for args in islice(zipped_iterables, buffersize)))
        else:
            fs = [self.submit(fn, *args) for args in zipped_iterables]
        executor_weakref = weakref.ref(self)

        def result_iterator():
            try:
                fs.reverse()
                while fs:
                    if buffersize and (executor := executor_weakref()) and (args := next(zipped_iterables, None)):
                        fs.appendleft(executor.submit(fn, *args))
                    if timeout is None:
                        yield _result_or_cancel(fs.pop())
                    else:
                        yield _result_or_cancel(fs.pop(), end_time - time.monotonic())
            finally:
                for future in fs:
                    future.cancel()
        return result_iterator()

    def shutdown(self, wait=True, *, cancel_futures=False):
        """Clean-up the resources associated with the Executor.

        It is safe to call this method several times. Otherwise, no other
        methods can be called after this one.

        Args:
            wait: If True then shutdown will not return until all running
                futures have finished executing and the resources used by
                the executor have been reclaimed.
            cancel_futures: If True then shutdown will cancel all pending
                futures. Futures that are completed or running will not be
                cancelled.
        """
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False
import concurrent.futures._base as _英文身份源
执行器 = _英文身份源.Executor

class 执行器损坏错误(RuntimeError):
    """
    Raised when an executor has become non-functional after a severe failure.
    """
import concurrent.futures._base as _英文身份源
执行器损坏错误 = _英文身份源.BrokenExecutor


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

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import concurrent.futures._base as _英文库
执行器损坏错误 = _英文库.BrokenExecutor
已取消错误 = _英文库.CancelledError
错误 = _英文库.Error
执行器 = _英文库.Executor
未来对象 = _英文库.Future
状态无效错误 = _英文库.InvalidStateError
_模块别名 = {
    'ALL_COMPLETED': '全部完成',
    'BrokenExecutor': '执行器损坏错误',
    'CANCELLED': '已取消',
    'CANCELLED_AND_NOTIFIED': '已取消且已通知',
    'CancelledError': '已取消错误',
    'DoneAndNotDoneFutures': '完成情况',
    'Error': '错误',
    'Executor': '执行器',
    'FINISHED': '已完成',
    'FIRST_COMPLETED': '最先完成',
    'FIRST_EXCEPTION': '最先异常',
    'Future': '未来对象',
    'InvalidStateError': '状态无效错误',
    'LOGGER': '日志器',
    'PENDING': '未开始',
    'RUNNING': '运行中',
    'as_completed': '完成即取',
    'wait': '等待完成',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
