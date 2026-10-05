# -*- coding: utf-8 -*-
"""事件调度 —— 汉语库（由 tools/汉化库.py 从 Lib/sched.py 机械生成，**不要手改**）。

英文库 Lib/sched.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 事件调度
"""


"""A generally useful event scheduler class.

Each instance of this class manages its own queue.
No multi-threading is implied; you are supposed to hack that
yourself, or use a single instance per application.

Each instance is parametrized with two functions, one that is
supposed to return the current time, one that is supposed to
implement a delay.  You can implement real-time scheduling by
substituting time and sleep from built-in module time, or you can
implement simulated time by writing your own functions.  This can
also be used to integrate scheduling with STDWIN events; the delay
function is allowed to modify the queue.  Time can be expressed as
integers or floating-point numbers, as long as it is consistent.

Events are specified by tuples (time, priority, action, argument, kwargs).
As in UNIX, lower priority numbers mean higher priority; in this
way the queue can be maintained as a priority queue.  Execution of the
event means calling the action function, passing it the argument
sequence in "argument" (remember that in Python, multiple function
arguments are be packed in a sequence) and keyword parameters in "kwargs".
The action function may be an instance method so it
has another way to reference private data (besides global variables).
"""
_英文原名表 = {'Event': '事件', 'scheduler': '调度器'}

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
import time
import heapq
from collections import namedtuple
from itertools import count
import threading
from time import monotonic as _time
__all__ = ['scheduler']
事件 = namedtuple('Event', 'time, priority, sequence, action, argument, kwargs')
事件.time.__doc__ = 'Numeric type compatible with the return value of the\ntimefunc function passed to the constructor.'
事件.priority.__doc__ = 'Events scheduled for the same time will be executed\nin the order of their priority.'
事件.sequence.__doc__ = 'A continually increasing sequence number that\n    separates events if time and priority are equal.'
事件.action.__doc__ = 'Executing the event means executing\naction(*argument, **kwargs)'
事件.argument.__doc__ = 'argument is a sequence holding the positional\narguments for the action.'
事件.kwargs.__doc__ = 'kwargs is a dictionary holding the keyword\narguments for the action.'
_sentinel = object()

class 调度器:

    def __init__(self, timefunc=_time, delayfunc=time.sleep):
        """Initialize a new instance, passing the time and delay
        functions"""
        self._queue = []
        self._lock = threading.RLock()
        self.timefunc = timefunc
        self.延迟函数 = delayfunc
        self._sequence_generator = count()

    def 定时进入(self, time, priority, action, argument=(), kwargs=_sentinel):
        """Enter a new event in the queue at an absolute time.

        Returns an ID for the event which can be used to remove it,
        if necessary.

        """
        if kwargs is _sentinel:
            kwargs = {}
        with self._lock:
            event = 事件(time, priority, next(self._sequence_generator), action, argument, kwargs)
            heapq.heappush(self._queue, event)
        return event

    def 延后进入(self, delay, priority, action, argument=(), kwargs=_sentinel):
        """A variant that specifies the time as a relative time.

        This is actually the more commonly used interface.

        """
        time = self.timefunc() + delay
        return self.定时进入(time, priority, action, argument, kwargs)

    def 取消(self, event):
        """Remove an event from the queue.

        This must be presented the ID as returned by enter().
        If the event is not in the queue, this raises ValueError.

        """
        with self._lock:
            self._queue.remove(event)
            heapq.heapify(self._queue)

    def 空了吗(self):
        """Check whether the queue is empty."""
        with self._lock:
            return not self._queue

    def 运行(self, blocking=True):
        """Execute events until the queue is empty.
        If blocking is False executes the scheduled events due to
        expire soonest (if any) and then return the deadline of the
        next scheduled call in the scheduler.

        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        restarted.

        It is legal for both the delay function and the action
        function to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.

        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.

        """
        lock = self._lock
        q = self._queue
        延迟函数 = self.延迟函数
        timefunc = self.timefunc
        pop = heapq.heappop
        while True:
            with lock:
                if not q:
                    break
                time, priority, sequence, action, argument, kwargs = q[0]
                now = timefunc()
                if time > now:
                    delay = True
                else:
                    delay = False
                    pop(q)
            if delay:
                if not blocking:
                    return time - now
                延迟函数(time - now)
            else:
                action(*argument, **kwargs)
                延迟函数(0)

    @property
    def 队列(self):
        """An ordered list of upcoming events.

        Events are named tuples with fields for:
            time, priority, action, arguments, kwargs

        """
        with self._lock:
            events = self._queue[:]
        return list(map(heapq.heappop, [events] * len(events)))
_装类转发(调度器, {'cancel': '取消', 'empty': '空了吗', 'enter': '延后进入', 'enterabs': '定时进入', 'queue': '队列', 'run': '运行'}, {'cancel': '取消', 'delayfunc': '延迟函数', 'empty': '空了吗', 'enter': '延后进入', 'enterabs': '定时进入', 'queue': '队列', 'run': '运行'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Event': '事件',
    'scheduler': '调度器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '调度器': {
        'cancel': '取消',
        'empty': '空了吗',
        'enter': '延后进入',
        'enterabs': '定时进入',
        'queue': '队列',
        'run': '运行',
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
    '调度器': {
        'cancel': '取消',
        'delayfunc': '延迟函数',
        'empty': '空了吗',
        'enter': '延后进入',
        'enterabs': '定时进入',
        'queue': '队列',
        'run': '运行',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '调度器',
])

# ---- 转发层结束 ----
