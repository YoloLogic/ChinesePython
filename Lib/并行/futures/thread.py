# -*- coding: utf-8 -*-
"""并行.futures/thread —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/futures/thread.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.futures/thread.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


"""Implements ThreadPoolExecutor."""
_英文原名表 = {'BrokenThreadPool': '线程池损坏错误', 'ThreadPoolExecutor': '线程池执行器', 'WorkerContext': '工作者上下文'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
from 并行.futures import _base
import itertools
import queue
import threading
import types
import weakref
import os
_threads_queues = weakref.WeakKeyDictionary()
_shutdown = False
_global_shutdown_lock = threading.Lock()

def _python_exit():
    global _shutdown
    with _global_shutdown_lock:
        _shutdown = True
    items = list(_threads_queues.items())
    for t, q in items:
        q.put(None)
    for t, q in items:
        t.join()
threading._register_atexit(_python_exit)
if hasattr(os, 'register_at_fork'):
    os.register_at_fork(before=_global_shutdown_lock.acquire, after_in_child=_global_shutdown_lock._at_fork_reinit, after_in_parent=_global_shutdown_lock.release)
    os.register_at_fork(after_in_child=_threads_queues.clear)

class 工作者上下文:

    @classmethod
    def prepare(cls, initializer, initargs):
        if initializer is not None:
            if not callable(initializer):
                raise TypeError('initializer must be a callable')

        def create_context():
            return cls(initializer, initargs)

        def resolve_task(fn, args, kwargs):
            return (fn, args, kwargs)
        return (create_context, resolve_task)

    def __init__(self, initializer, initargs):
        self.initializer = initializer
        self.initargs = initargs

    def initialize(self):
        if self.initializer is not None:
            self.initializer(*self.initargs)

    def finalize(self):
        pass

    def run(self, task):
        fn, args, kwargs = task
        return fn(*args, **kwargs)

class _WorkItem:

    def __init__(self, future, task):
        self.future = future
        self.task = task

    def run(self, ctx):
        if not self.future.set_running_or_notify_cancel():
            return
        try:
            result = ctx.run(self.task)
        except BaseException as exc:
            self.future.set_exception(exc)
            self = None
        else:
            self.future.set_result(result)
    __class_getitem__ = classmethod(types.GenericAlias)

def _worker(executor_reference, ctx, work_queue):
    try:
        ctx.initialize()
    except BaseException:
        _base.LOGGER.critical('Exception in initializer:', exc_info=True)
        executor = executor_reference()
        if executor is not None:
            executor._initializer_failed()
        return
    try:
        while True:
            try:
                work_item = work_queue.get_nowait()
            except queue.Empty:
                executor = executor_reference()
                if executor is not None:
                    executor._idle_semaphore.release()
                del executor
                work_item = work_queue.get(block=True)
            if work_item is not None:
                work_item.run(ctx)
                del work_item
                continue
            executor = executor_reference()
            if _shutdown or executor is None or executor._shutdown:
                if executor is not None:
                    executor._shutdown = True
                work_queue.put(None)
                return
            del executor
    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)
    finally:
        ctx.finalize()

class 线程池损坏错误(_base.BrokenExecutor):
    """
    Raised when a worker thread in a ThreadPoolExecutor failed initializing.
    """

class 线程池执行器(_base.Executor):
    BROKEN = 线程池损坏错误
    _counter = itertools.count().__next__

    @classmethod
    def prepare_context(cls, initializer, initargs):
        return 工作者上下文.prepare(initializer, initargs)

    def __init__(self, max_workers=None, thread_name_prefix='', initializer=None, initargs=(), **ctxkwargs):
        """Initializes a new ThreadPoolExecutor instance.

        Args:
            max_workers: The maximum number of threads that can be used to
                execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: A callable used to initialize worker threads.
            initargs: A tuple of arguments to pass to the initializer.
            ctxkwargs: Additional arguments to cls.prepare_context().
        """
        if max_workers is None:
            max_workers = min(32, (os.process_cpu_count() or 1) + 4)
        if max_workers <= 0:
            raise ValueError('max_workers must be greater than 0')
        self._create_worker_context, self._resolve_work_item_task = type(self).prepare_context(initializer, initargs, **ctxkwargs)
        self._max_workers = max_workers
        self._work_queue = queue.SimpleQueue()
        self._idle_semaphore = threading.Semaphore(0)
        self._threads = set()
        self._broken = False
        self._shutdown = False
        self._shutdown_lock = threading.Lock()
        self._thread_name_prefix = thread_name_prefix or 'ThreadPoolExecutor-%d' % self._counter()

    def submit(self, fn, /, *args, **kwargs):
        with self._shutdown_lock, _global_shutdown_lock:
            if self._broken:
                raise self.BROKEN(self._broken)
            if self._shutdown:
                raise RuntimeError('cannot schedule new futures after shutdown')
            if _shutdown:
                raise RuntimeError('cannot schedule new futures after interpreter shutdown')
            f = _base.Future()
            task = self._resolve_work_item_task(fn, args, kwargs)
            w = _WorkItem(f, task)
            self._work_queue.put(w)
            self._adjust_thread_count()
            return f
    submit.__doc__ = _base.Executor.submit.__doc__

    def _adjust_thread_count(self):
        if self._idle_semaphore.acquire(timeout=0):
            return

        def weakref_cb(_, q=self._work_queue):
            q.put(None)
        num_threads = len(self._threads)
        if num_threads < self._max_workers:
            thread_name = '%s_%d' % (self._thread_name_prefix or self, num_threads)
            t = threading.Thread(name=thread_name, target=_worker, args=(weakref.ref(self, weakref_cb), self._create_worker_context(), self._work_queue))
            t.start()
            self._threads.add(t)
            _threads_queues[t] = self._work_queue

    def _initializer_failed(self):
        with self._shutdown_lock:
            self._broken = 'A thread initializer failed, the thread pool is not usable anymore'
            while True:
                try:
                    work_item = self._work_queue.get_nowait()
                except queue.Empty:
                    break
                if work_item is not None:
                    work_item.future.set_exception(self.BROKEN(self._broken))

    def shutdown(self, wait=True, *, cancel_futures=False):
        with self._shutdown_lock:
            self._shutdown = True
            if cancel_futures:
                while True:
                    try:
                        work_item = self._work_queue.get_nowait()
                    except queue.Empty:
                        break
                    if work_item is not None:
                        work_item.future.cancel()
            self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()
    shutdown.__doc__ = _base.Executor.shutdown.__doc__
import concurrent.futures.thread as _英文身份源
线程池执行器 = _英文身份源.ThreadPoolExecutor


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import concurrent.futures.thread as _英文库
线程池执行器 = _英文库.ThreadPoolExecutor
_模块别名 = {
    'BrokenThreadPool': '线程池损坏错误',
    'ThreadPoolExecutor': '线程池执行器',
    'WorkerContext': '工作者上下文',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
