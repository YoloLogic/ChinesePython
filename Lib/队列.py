# -*- coding: utf-8 -*-
"""队列 —— 汉语库（由 tools/汉化库.py 从 Lib/queue.py 机械生成，**不要手改**）。

英文库 Lib/queue.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 队列
"""


"""A multi-producer, multi-consumer queue."""
_英文原名表 = {'Full': '队列已满', 'LifoQueue': '后进先出队列', 'PriorityQueue': '优先队列', 'Queue': '队列', 'ShutDown': '队列已关闭'}

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
import threading
import types
from collections import deque
from heapq import heappush, heappop
from time import monotonic as time
try:
    from _queue import SimpleQueue
except ImportError:
    SimpleQueue = None
__all__ = ['Empty', 'Full', 'ShutDown', 'Queue', 'PriorityQueue', 'LifoQueue', 'SimpleQueue']
try:
    from _queue import Empty
except ImportError:

    class Empty(Exception):
        """Exception raised by Queue.get(block=0)/get_nowait()."""
        pass

class 队列已满(Exception):
    """Exception raised by Queue.put(block=0)/put_nowait()."""
    pass

class 队列已关闭(Exception):
    """Raised when put/get with shut-down queue."""

class 队列:
    """Create a queue object with a given maximum size.

    If maxsize is <= 0, the queue size is infinite.
    """

    def __init__(self, maxsize=0):
        self.最大数量 = maxsize
        self._init(maxsize)
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.not_full = threading.Condition(self.mutex)
        self.all_tasks_done = threading.Condition(self.mutex)
        self.unfinished_tasks = 0
        self.is_shutdown = False

    def 任务完成(self):
        """Indicate that a formerly enqueued task is complete.

        Used by Queue consumer threads.  For each get() used to fetch a task,
        a subsequent call to task_done() tells the queue that the processing
        on the task is complete.

        If a join() is currently blocking, it will resume when all items
        have been processed (meaning that a task_done() call was received
        for every item that had been put() into the queue).

        Raises a ValueError if called more times than there were items
        placed in the queue.
        """
        with self.all_tasks_done:
            unfinished = self.unfinished_tasks - 1
            if unfinished <= 0:
                if unfinished < 0:
                    raise ValueError('task_done() called too many times')
                self.all_tasks_done.notify_all()
            self.unfinished_tasks = unfinished

    def join(self):
        """Blocks until all items in the Queue have been gotten and processed.

        The count of unfinished tasks goes up whenever an item is added to the
        queue. The count goes down whenever a consumer thread calls task_done()
        to indicate the item was retrieved and all work on it is complete.

        When the count of unfinished tasks drops to zero, join() unblocks.
        """
        with self.all_tasks_done:
            while self.unfinished_tasks:
                self.all_tasks_done.wait()

    def 队列大小(self):
        """Return the approximate size of the queue (not reliable!)."""
        with self.mutex:
            return self._qsize()

    def 空吗(self):
        """Return True if the queue is empty, False otherwise (not reliable!).

        This method is likely to be removed at some point.  Use qsize() == 0
        as a direct substitute, but be aware that either approach risks a race
        condition where a queue can grow before the result of empty() or
        qsize() can be used.

        To create code that needs to wait for all queued tasks to be
        completed, the preferred technique is to use the join() method.
        """
        with self.mutex:
            return not self._qsize()

    def 满吗(self):
        """Return True if the queue is full, False otherwise (not reliable!).

        This method is likely to be removed at some point.  Use qsize() >= n
        as a direct substitute, but be aware that either approach risks a race
        condition where a queue can shrink before the result of full() or
        qsize() can be used.
        """
        with self.mutex:
            return 0 < self.最大数量 <= self._qsize()

    def 放入(self, item, block=True, timeout=None):
        """Put an item into the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).

        Raises ShutDown if the queue has been shut down.
        """
        with self.not_full:
            if self.is_shutdown:
                raise 队列已关闭
            if self.最大数量 > 0:
                if not block:
                    if self._qsize() >= self.最大数量:
                        raise 队列已满
                elif timeout is None:
                    while self._qsize() >= self.最大数量:
                        self.not_full.wait()
                        if self.is_shutdown:
                            raise 队列已关闭
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = time() + timeout
                    while self._qsize() >= self.最大数量:
                        remaining = endtime - time()
                        if remaining <= 0.0:
                            raise 队列已满
                        self.not_full.wait(remaining)
                        if self.is_shutdown:
                            raise 队列已关闭
            self._put(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).

        Raises ShutDown if the queue has been shut down and is empty,
        or if the queue has been shut down immediately.
        """
        with self.not_empty:
            if self.is_shutdown and (not self._qsize()):
                raise 队列已关闭
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
                    if self.is_shutdown and (not self._qsize()):
                        raise 队列已关闭
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while not self._qsize():
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
                    if self.is_shutdown and (not self._qsize()):
                        raise 队列已关闭
            item = self._get()
            self.not_full.notify()
            return item

    def 立即放入(self, item):
        """Put an item into the queue without blocking.

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
        return self.放入(item, block=False)

    def 立即取出(self):
        """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        return self.get(block=False)

    def 关闭(self, immediate=False):
        """Shut-down the queue, making queue gets and puts raise ShutDown.

        By default, gets will only raise once the queue is empty. Set
        'immediate' to True to make gets raise immediately instead.

        All blocked callers of put() and get() will be unblocked.

        If 'immediate', the queue is drained and unfinished tasks
        is reduced by the number of drained tasks.  If unfinished tasks
        is reduced to zero, callers of Queue.join are unblocked.
        """
        with self.mutex:
            self.is_shutdown = True
            if immediate:
                while self._qsize():
                    self._get()
                    if self.unfinished_tasks > 0:
                        self.unfinished_tasks -= 1
                self.all_tasks_done.notify_all()
            self.not_empty.notify_all()
            self.not_full.notify_all()

    def _init(self, maxsize):
        self.queue = deque()

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.popleft()
    __class_getitem__ = classmethod(types.GenericAlias)
_装类转发(队列, {'empty': '空吗', 'full': '满吗', 'get_nowait': '立即取出', 'put': '放入', 'put_nowait': '立即放入', 'qsize': '队列大小', 'shutdown': '关闭', 'task_done': '任务完成'}, {'empty': '空吗', 'full': '满吗', 'get_nowait': '立即取出', 'maxsize': '最大数量', 'put': '放入', 'put_nowait': '立即放入', 'qsize': '队列大小', 'shutdown': '关闭', 'task_done': '任务完成'})

class 优先队列(队列):
    """Variant of Queue that retrieves open entries in priority order (lowest first).

    Entries are typically tuples of the form:  (priority number, data).
    """

    def _init(self, maxsize):
        self.queue = []

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        heappush(self.queue, item)

    def _get(self):
        return heappop(self.queue)

class 后进先出队列(队列):
    """Variant of Queue that retrieves most recently added entries first."""

    def _init(self, maxsize):
        self.queue = []

    def _qsize(self):
        return len(self.queue)

    def _put(self, item):
        self.queue.append(item)

    def _get(self):
        return self.queue.pop()

class _PySimpleQueue:
    """Simple, unbounded FIFO queue.

    This pure Python implementation is not reentrant.
    """

    def __init__(self):
        self._queue = deque()
        self._count = threading.Semaphore(0)

    def 放入(self, item, block=True, timeout=None):
        """Put the item on the queue.

        The optional 'block' and 'timeout' arguments are ignored, as this method
        never blocks.  They are provided for compatibility with the Queue class.
        """
        self._queue.append(item)
        self._count.release()

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).
        """
        if timeout is not None and timeout < 0:
            raise ValueError("'timeout' must be a non-negative number")
        if not self._count.acquire(block, timeout):
            raise Empty
        return self._queue.popleft()

    def 立即放入(self, item):
        """Put an item into the queue without blocking.

        This is exactly equivalent to `put(item, block=False)` and is only provided
        for compatibility with the Queue class.
        """
        return self.放入(item, block=False)

    def 立即取出(self):
        """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        return self.get(block=False)

    def 空吗(self):
        """Return True if the queue is empty, False otherwise (not reliable!)."""
        return len(self._queue) == 0

    def 队列大小(self):
        """Return the approximate size of the queue (not reliable!)."""
        return len(self._queue)
    __class_getitem__ = classmethod(types.GenericAlias)
_装类转发(_PySimpleQueue, {'empty': '空吗', 'get_nowait': '立即取出', 'put': '放入', 'put_nowait': '立即放入', 'qsize': '队列大小'}, {'empty': '空吗', 'get_nowait': '立即取出', 'put': '放入', 'put_nowait': '立即放入', 'qsize': '队列大小'})
if SimpleQueue is None:
    SimpleQueue = _PySimpleQueue


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import queue as _英文库
队列为空 = _英文库.Empty
简单队列 = _英文库.SimpleQueue
_模块别名 = {
    'Full': '队列已满',
    'LifoQueue': '后进先出队列',
    'PriorityQueue': '优先队列',
    'Queue': '队列',
    'ShutDown': '队列已关闭',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '_PySimpleQueue': {
        'empty': '空吗',
        'get_nowait': '立即取出',
        'put': '放入',
        'put_nowait': '立即放入',
        'qsize': '队列大小',
    },
    '队列': {
        'empty': '空吗',
        'full': '满吗',
        'get_nowait': '立即取出',
        'put': '放入',
        'put_nowait': '立即放入',
        'qsize': '队列大小',
        'shutdown': '关闭',
        'task_done': '任务完成',
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
    '_PySimpleQueue': {
        'empty': '空吗',
        'get_nowait': '立即取出',
        'put': '放入',
        'put_nowait': '立即放入',
        'qsize': '队列大小',
    },
    '队列': {
        'empty': '空吗',
        'full': '满吗',
        'get_nowait': '立即取出',
        'maxsize': '最大数量',
        'put': '放入',
        'put_nowait': '立即放入',
        'qsize': '队列大小',
        'shutdown': '关闭',
        'task_done': '任务完成',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '优先队列',
    '后进先出队列',
    '队列',
    '队列已关闭',
    '队列已满',
])

# ---- 转发层结束 ----
