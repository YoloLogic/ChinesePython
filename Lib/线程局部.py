# -*- coding: utf-8 -*-
"""线程局部 —— 汉语库（由 tools/汉化库.py 从 Lib/_threading_local.py 机械生成，**不要手改**）。

英文库 Lib/_threading_local.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 线程局部
"""


"""Thread-local objects.

(Note that this module provides a Python version of the threading.local
 class.  Depending on the version of Python you're using, there may be a
 faster one available.  You should always import the `local` class from
 `threading`.)
"""
_英文原名表 = {'local': '局部'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from weakref import ref
from contextlib import contextmanager
__all__ = ['local']

class _localimpl:
    """A class managing thread-local dicts"""
    __slots__ = ('key', 'dicts', 'localargs', 'locallock', '__weakref__')

    def __init__(self):
        self.key = '_threading_local._localimpl.' + str(id(self))
        self.dicts = {}

    def get_dict(self):
        """Return the dict for the current thread. Raises KeyError if none
        defined."""
        thread = current_thread()
        return self.dicts[id(thread)][1]

    def create_dict(self):
        """Create a new dict for the current thread, and return it."""
        localdict = {}
        key = self.key
        thread = current_thread()
        idt = id(thread)

        def local_deleted(_, key=key):
            thread = wrthread()
            if thread is not None:
                del thread.__dict__[key]

        def thread_deleted(_, idt=idt):
            局部 = wrlocal()
            if 局部 is not None:
                dct = 局部.dicts.pop(idt)
        wrlocal = ref(self, local_deleted)
        wrthread = ref(thread, thread_deleted)
        thread.__dict__[key] = wrlocal
        self.dicts[idt] = (wrthread, localdict)
        return localdict

@contextmanager
def _patch(self):
    impl = object.__getattribute__(self, '_local__impl')
    try:
        dct = impl.get_dict()
    except KeyError:
        dct = impl.create_dict()
        args, kw = impl.localargs
        self.__init__(*args, **kw)
    with impl.locallock:
        object.__setattr__(self, '__dict__', dct)
        yield

class 局部:
    __slots__ = ('_local__impl', '__dict__')

    def __new__(cls, /, *args, **kw):
        if (args or kw) and cls.__init__ is object.__init__:
            raise TypeError('Initialization arguments are not supported')
        self = object.__new__(cls)
        impl = _localimpl()
        impl.localargs = (args, kw)
        impl.locallock = RLock()
        object.__setattr__(self, '_local__impl', impl)
        impl.create_dict()
        return self

    def __getattribute__(self, name):
        with _patch(self):
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name == '__dict__':
            raise AttributeError("%r object attribute '__dict__' is read-only" % self.__class__.__name__)
        with _patch(self):
            return object.__setattr__(self, name, value)

    def __delattr__(self, name):
        if name == '__dict__':
            raise AttributeError("%r object attribute '__dict__' is read-only" % self.__class__.__name__)
        with _patch(self):
            return object.__delattr__(self, name)
from threading import current_thread, RLock


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'local': '局部',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '局部',
])

# ---- 转发层结束 ----
