# -*- coding: utf-8 -*-
"""多进程.queues —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/queues.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.queues.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'JoinableQueue': '可汇合队列', 'Queue': '队列', 'SimpleQueue': '简单队列'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['Queue', 'SimpleQueue', 'JoinableQueue']
import sys
import os
import threading
import collections
import time
import types
import weakref
import errno
from queue import Empty, Full
from . import connection
from . import context
_ForkingPickler = context.reduction.ForkingPickler
from .util import debug, info, Finalize, register_after_fork, is_exiting

class 队列(object):

    def __init__(self, maxsize=0, *, ctx):
        if maxsize <= 0:
            from .synchronize import SEM_VALUE_MAX as maxsize
        self._maxsize = maxsize
        self._reader, self._writer = connection.Pipe(duplex=False)
        self._rlock = ctx.Lock()
        self._opid = os.getpid()
        if sys.platform == 'win32':
            self._wlock = None
        else:
            self._wlock = ctx.Lock()
        self._sem = ctx.BoundedSemaphore(maxsize)
        self._ignore_epipe = False
        self._reset()
        if sys.platform != 'win32':
            register_after_fork(self, 队列._after_fork)

    def __getstate__(self):
        context.assert_spawning(self)
        return (self._ignore_epipe, self._maxsize, self._reader, self._writer, self._rlock, self._wlock, self._sem, self._opid)

    def __setstate__(self, state):
        self._ignore_epipe, self._maxsize, self._reader, self._writer, self._rlock, self._wlock, self._sem, self._opid = state
        self._reset()

    def _after_fork(self):
        debug('Queue._after_fork()')
        self._reset(after_fork=True)

    def _reset(self, after_fork=False):
        if after_fork:
            self._notempty._at_fork_reinit()
        else:
            self._notempty = threading.Condition(threading.Lock())
        self._buffer = collections.deque()
        self._thread = None
        self._jointhread = None
        self._joincancelled = False
        self._closed = False
        self._close = None
        self._send_bytes = self._writer.send_bytes
        self._recv_bytes = self._reader.recv_bytes
        self._poll = self._reader.poll

    def put(self, obj, block=True, timeout=None):
        if self._closed:
            raise ValueError(f'Queue {self!r} is closed')
        if not self._sem.acquire(block, timeout):
            raise Full
        with self._notempty:
            if self._thread is None:
                self._start_thread()
            self._buffer.append(obj)
            self._notempty.notify()

    def get(self, block=True, timeout=None):
        if self._closed:
            raise ValueError(f'Queue {self!r} is closed')
        if block and timeout is None:
            with self._rlock:
                res = self._recv_bytes()
            self._sem.release()
        else:
            if block:
                deadline = time.monotonic() + timeout
            if not self._rlock.acquire(block, timeout):
                raise Empty
            try:
                if block:
                    timeout = deadline - time.monotonic()
                    if not self._poll(timeout):
                        raise Empty
                elif not self._poll():
                    raise Empty
                res = self._recv_bytes()
                self._sem.release()
            finally:
                self._rlock.release()
        return _ForkingPickler.loads(res)

    def qsize(self):
        return self._maxsize - self._sem.get_value()

    def empty(self):
        return not self._poll()

    def full(self):
        return self._sem._semlock._is_zero()

    def get_nowait(self):
        return self.get(False)

    def put_nowait(self, obj):
        return self.put(obj, False)

    def close(self):
        self._closed = True
        close = self._close
        if close:
            self._close = None
            close()

    def join_thread(self):
        debug('Queue.join_thread()')
        assert self._closed, 'Queue {0!r} not closed'.format(self)
        if self._jointhread:
            self._jointhread()

    def cancel_join_thread(self):
        debug('Queue.cancel_join_thread()')
        self._joincancelled = True
        try:
            self._jointhread.cancel()
        except AttributeError:
            pass

    def _terminate_broken(self):
        self._reader.close()
        if sys.platform == 'win32':
            self._writer.close()
        self.close()
        self.join_thread()

    def _start_thread(self):
        debug('Queue._start_thread()')
        self._buffer.clear()
        self._thread = threading.Thread(target=队列._feed, args=(self._buffer, self._notempty, self._send_bytes, self._wlock, self._reader.close, self._writer.close, self._ignore_epipe, self._on_queue_feeder_error, self._sem), name='QueueFeederThread', daemon=True)
        try:
            debug('doing self._thread.start()')
            self._thread.start()
            debug('... done self._thread.start()')
        except:
            self._thread = None
            raise
        if not self._joincancelled:
            self._jointhread = Finalize(self._thread, 队列._finalize_join, [weakref.ref(self._thread)], exitpriority=-5)
        self._close = Finalize(self, 队列._finalize_close, [self._buffer, self._notempty], exitpriority=10)

    @staticmethod
    def _finalize_join(twr):
        debug('joining queue thread')
        thread = twr()
        if thread is not None:
            thread.join()
            debug('... queue thread joined')
        else:
            debug('... queue thread already dead')

    @staticmethod
    def _finalize_close(buffer, notempty):
        debug('telling queue thread to quit')
        with notempty:
            buffer.append(_sentinel)
            notempty.notify()

    @staticmethod
    def _feed(buffer, notempty, send_bytes, writelock, reader_close, writer_close, ignore_epipe, onerror, queue_sem):
        debug('starting thread to feed data to pipe')
        nacquire = notempty.acquire
        nrelease = notempty.release
        nwait = notempty.wait
        bpopleft = buffer.popleft
        sentinel = _sentinel
        if sys.platform != 'win32':
            wacquire = writelock.acquire
            wrelease = writelock.release
        else:
            wacquire = None
        while 1:
            try:
                nacquire()
                try:
                    if not buffer:
                        nwait()
                finally:
                    nrelease()
                try:
                    while 1:
                        obj = bpopleft()
                        if obj is sentinel:
                            debug('feeder thread got sentinel -- exiting')
                            reader_close()
                            writer_close()
                            return
                        obj = _ForkingPickler.dumps(obj)
                        if wacquire is None:
                            send_bytes(obj)
                        else:
                            wacquire()
                            try:
                                send_bytes(obj)
                            finally:
                                wrelease()
                except IndexError:
                    pass
            except Exception as e:
                if ignore_epipe and getattr(e, 'errno', 0) == errno.EPIPE:
                    return
                if is_exiting():
                    info('error in queue thread: %s', e)
                    return
                else:
                    queue_sem.release()
                    onerror(e, obj)

    @staticmethod
    def _on_queue_feeder_error(e, obj):
        """
        Private API hook called when feeding data in the background thread
        raises an exception.  For overriding by concurrent.futures.
        """
        import traceback
        traceback.print_exc()
    __class_getitem__ = classmethod(types.GenericAlias)
_sentinel = object()

class 可汇合队列(队列):

    def __init__(self, maxsize=0, *, ctx):
        队列.__init__(self, maxsize, ctx=ctx)
        self._unfinished_tasks = ctx.Semaphore(0)
        self._cond = ctx.Condition()

    def __getstate__(self):
        return 队列.__getstate__(self) + (self._cond, self._unfinished_tasks)

    def __setstate__(self, state):
        队列.__setstate__(self, state[:-2])
        self._cond, self._unfinished_tasks = state[-2:]

    def put(self, obj, block=True, timeout=None):
        if self._closed:
            raise ValueError(f'Queue {self!r} is closed')
        if not self._sem.acquire(block, timeout):
            raise Full
        with self._notempty, self._cond:
            if self._thread is None:
                self._start_thread()
            self._buffer.append(obj)
            self._unfinished_tasks.release()
            self._notempty.notify()

    def task_done(self):
        with self._cond:
            if not self._unfinished_tasks.acquire(False):
                raise ValueError('task_done() called too many times')
            if self._unfinished_tasks._semlock._is_zero():
                self._cond.notify_all()

    def join(self):
        with self._cond:
            if not self._unfinished_tasks._semlock._is_zero():
                self._cond.wait()

class 简单队列(object):

    def __init__(self, *, ctx):
        self._reader, self._writer = connection.Pipe(duplex=False)
        self._rlock = ctx.Lock()
        self._poll = self._reader.poll
        if sys.platform == 'win32':
            self._wlock = None
        else:
            self._wlock = ctx.Lock()

    def close(self):
        self._reader.close()
        self._writer.close()

    def empty(self):
        return not self._poll()

    def __getstate__(self):
        context.assert_spawning(self)
        return (self._reader, self._writer, self._rlock, self._wlock)

    def __setstate__(self, state):
        self._reader, self._writer, self._rlock, self._wlock = state
        self._poll = self._reader.poll

    def get(self):
        with self._rlock:
            res = self._reader.recv_bytes()
        return _ForkingPickler.loads(res)

    def put(self, obj):
        obj = _ForkingPickler.dumps(obj)
        if self._wlock is None:
            self._writer.send_bytes(obj)
        else:
            with self._wlock:
                self._writer.send_bytes(obj)
    __class_getitem__ = classmethod(types.GenericAlias)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'JoinableQueue': '可汇合队列',
    'Queue': '队列',
    'SimpleQueue': '简单队列',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '可汇合队列',
    '简单队列',
    '队列',
])

# ---- 转发层结束 ----
