# -*- coding: utf-8 -*-
"""多进程.dummy/__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/dummy/__init__.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.dummy/__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Array': '数组', 'DummyProcess': '假进程', 'Manager': '管理器', 'Pool': '进程池', 'Value': '值', 'active_children': '活动子进程', 'freeze_support': '冻结支持', 'shutdown': '关闭'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['Process', 'current_process', 'active_children', 'freeze_support', 'Lock', 'RLock', 'Semaphore', 'BoundedSemaphore', 'Condition', 'Event', 'Barrier', 'Queue', 'Manager', 'Pipe', 'Pool', 'JoinableQueue']
import threading
import sys
import weakref
import array
from .connection import Pipe
from threading import Lock, RLock, Semaphore, BoundedSemaphore
from threading import Event, Condition, Barrier
from queue import Queue

class 假进程(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._pid = None
        self._children = weakref.WeakKeyDictionary()
        self._start_called = False
        self._parent = current_process()

    def start(self):
        if self._parent is not current_process():
            raise RuntimeError('Parent is {0!r} but current_process is {1!r}'.format(self._parent, current_process()))
        self._start_called = True
        if hasattr(self._parent, '_children'):
            self._parent._children[self] = None
        threading.Thread.start(self)

    @property
    def exitcode(self):
        if self._start_called and (not self.is_alive()):
            return 0
        else:
            return None
Process = 假进程
current_process = threading.current_thread
current_process()._children = weakref.WeakKeyDictionary()

def 活动子进程():
    children = current_process()._children
    for p in list(children):
        if not p.is_alive():
            children.pop(p, None)
    return list(children)

def 冻结支持():
    pass

class Namespace(object):

    def __init__(self, /, **kwds):
        self.__dict__.update(kwds)

    def __repr__(self):
        items = list(self.__dict__.items())
        temp = []
        for name, value in items:
            if not name.startswith('_'):
                temp.append('%s=%r' % (name, value))
        temp.sort()
        return '%s(%s)' % (self.__class__.__name__, ', '.join(temp))
dict = dict
list = list

def 数组(typecode, sequence, lock=True):
    return array.array(typecode, sequence)

class 值(object):

    def __init__(self, typecode, value, lock=True):
        self._typecode = typecode
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def __repr__(self):
        return '<%s(%r, %r)>' % (type(self).__name__, self._typecode, self._value)

def 管理器():
    return sys.modules[__name__]

def 关闭():
    pass

def 进程池(processes=None, initializer=None, initargs=()):
    from ..pool import ThreadPool
    return ThreadPool(processes, initializer, initargs)
JoinableQueue = Queue


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
    '命名空间': 'Namespace',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'Array': '数组',
    'DummyProcess': '假进程',
    'Manager': '管理器',
    'Pool': '进程池',
    'Value': '值',
    'active_children': '活动子进程',
    'freeze_support': '冻结支持',
    'shutdown': '关闭',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '冻结支持',
    '命名空间',
    '活动子进程',
    '管理器',
    '进程池',
])

# ---- 转发层结束 ----
