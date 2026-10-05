# -*- coding: utf-8 -*-
"""弱引用 —— 汉语库（由 tools/汉化库.py 从 Lib/weakref.py 机械生成，**不要手改**）。

英文库 Lib/weakref.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 弱引用
"""


"""Weak reference support for Python.

This module is an implementation of PEP 205:

https://peps.python.org/pep-0205/
"""
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
from _weakref import getweakrefcount, getweakrefs, ref, proxy, CallableProxyType, ProxyType, ReferenceType, _remove_dead_weakref
from _weakrefset import WeakSet
import _collections_abc
import sys
import itertools
ProxyTypes = (ProxyType, CallableProxyType)
__all__ = ['ref', 'proxy', 'getweakrefcount', 'getweakrefs', 'WeakKeyDictionary', 'ReferenceType', 'ProxyType', 'CallableProxyType', 'ProxyTypes', 'WeakValueDictionary', 'WeakSet', 'WeakMethod', 'finalize']
_collections_abc.MutableSet.register(WeakSet)

class WeakMethod(ref):
    """
    A custom `weakref.ref` subclass which simulates a weak reference to
    a bound method, working around the lifetime problem of bound methods.
    """
    __slots__ = ('_func_ref', '_meth_type', '_alive', '__weakref__')

    def __new__(cls, meth, callback=None):
        try:
            obj = meth.__self__
            func = meth.__func__
        except AttributeError:
            raise TypeError('argument should be a bound method, not {}'.format(type(meth))) from None

        def _cb(arg):
            self = self_wr()
            if self._alive:
                self._alive = False
                if callback is not None:
                    callback(self)
        self = ref.__new__(cls, obj, _cb)
        self._func_ref = ref(func, _cb)
        self._meth_type = type(meth)
        self._alive = True
        self_wr = ref(self)
        return self

    def __call__(self):
        obj = super().__call__()
        func = self._func_ref()
        if obj is None or func is None:
            return None
        return self._meth_type(func, obj)

    def __eq__(self, other):
        if isinstance(other, WeakMethod):
            if not self._alive or not other._alive:
                return self is other
            return ref.__eq__(self, other) and self._func_ref == other._func_ref
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, WeakMethod):
            if not self._alive or not other._alive:
                return self is not other
            return ref.__ne__(self, other) or self._func_ref != other._func_ref
        return NotImplemented
    __hash__ = ref.__hash__

class WeakValueDictionary(_collections_abc.MutableMapping):
    """Mapping class that references values weakly.

    Entries in the dictionary will be discarded when no strong
    reference to the value exists anymore
    """

    def __init__(self, other=(), /, **kw):

        def remove(wr, selfref=ref(self), _atomic_removal=_remove_dead_weakref):
            self = selfref()
            if self is not None:
                _atomic_removal(self.data, wr.key)
        self._remove = remove
        self.data = {}
        self.update(other, **kw)

    def __getitem__(self, key):
        o = self.data[key]()
        if o is None:
            raise KeyError(key)
        else:
            return o

    def __delitem__(self, key):
        del self.data[key]

    def __len__(self):
        return len(self.data)

    def __contains__(self, key):
        try:
            o = self.data[key]()
        except KeyError:
            return False
        return o is not None

    def __repr__(self):
        return '<%s at %#x>' % (self.__class__.__name__, id(self))

    def __setitem__(self, key, value):
        self.data[key] = KeyedRef(value, self._remove, key)

    def copy(self):
        new = WeakValueDictionary()
        for key, wr in self.data.copy().items():
            o = wr()
            if o is not None:
                new[key] = o
        return new
    __copy__ = copy

    def __deepcopy__(self, memo):
        from copy import deepcopy
        new = self.__class__()
        for key, wr in self.data.copy().items():
            o = wr()
            if o is not None:
                new[deepcopy(key, memo)] = o
        return new

    def get(self, key, default=None):
        try:
            wr = self.data[key]
        except KeyError:
            return default
        else:
            o = wr()
            if o is None:
                return default
            else:
                return o

    def items(self):
        for k, wr in self.data.copy().items():
            v = wr()
            if v is not None:
                yield (k, v)

    def keys(self):
        for k, wr in self.data.copy().items():
            if wr() is not None:
                yield k
    __iter__ = keys

    def 迭代值弱引用(self):
        """Return an iterator that yields the weak references to the values.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.

        """
        yield from self.data.copy().values()

    def values(self):
        for wr in self.data.copy().values():
            obj = wr()
            if obj is not None:
                yield obj

    def popitem(self):
        while True:
            key, wr = self.data.popitem()
            o = wr()
            if o is not None:
                return (key, o)

    def pop(self, key, *args):
        try:
            o = self.data.pop(key)()
        except KeyError:
            o = None
        if o is None:
            if args:
                return args[0]
            else:
                raise KeyError(key)
        else:
            return o

    def setdefault(self, key, default=None):
        try:
            o = self.data[key]()
        except KeyError:
            o = None
        if o is None:
            self.data[key] = KeyedRef(default, self._remove, key)
            return default
        else:
            return o

    def update(self, other=None, /, **kwargs):
        d = self.data
        if other is not None:
            if not hasattr(other, 'items'):
                other = dict(other)
            for key, o in other.items():
                d[key] = KeyedRef(o, self._remove, key)
        for key, o in kwargs.items():
            d[key] = KeyedRef(o, self._remove, key)

    def 取值弱引用表(self):
        """Return a list of weak references to the values.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the values around longer than needed.

        """
        return list(self.data.copy().values())

    def __ior__(self, other):
        self.update(other)
        return self

    def __or__(self, other):
        if isinstance(other, _collections_abc.Mapping):
            c = self.copy()
            c.update(other)
            return c
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, _collections_abc.Mapping):
            c = self.__class__()
            c.update(other)
            c.update(self)
            return c
        return NotImplemented
_装类转发(WeakValueDictionary, {'itervaluerefs': '迭代值弱引用', 'valuerefs': '取值弱引用表'}, {'itervaluerefs': '迭代值弱引用', 'valuerefs': '取值弱引用表'})

class KeyedRef(ref):
    """Specialized reference that includes a key corresponding to the value.

    This is used in the WeakValueDictionary to avoid having to create
    a function object for each key stored in the mapping.  A shared
    callback object can use the 'key' attribute of a KeyedRef instead
    of getting a reference to the key from an enclosing scope.

    """
    __slots__ = ('key',)

    def __new__(type, ob, callback, key):
        self = ref.__new__(type, ob, callback)
        self.key = key
        return self

    def __init__(self, ob, callback, key):
        super().__init__(ob, callback)

class WeakKeyDictionary(_collections_abc.MutableMapping):
    """ Mapping class that references keys weakly.

    Entries in the dictionary will be discarded when there is no
    longer a strong reference to the key. This can be used to
    associate additional data with an object owned by other parts of
    an application without adding attributes to those objects. This
    can be especially useful with objects that override attribute
    accesses.
    """

    def __init__(self, dict=None):
        self.data = {}

        def remove(k, selfref=ref(self)):
            self = selfref()
            if self is not None:
                try:
                    del self.data[k]
                except KeyError:
                    pass
        self._remove = remove
        if dict is not None:
            self.update(dict)

    def __delitem__(self, key):
        del self.data[ref(key)]

    def __getitem__(self, key):
        return self.data[ref(key)]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return '<%s at %#x>' % (self.__class__.__name__, id(self))

    def __setitem__(self, key, value):
        self.data[ref(key, self._remove)] = value

    def copy(self):
        new = WeakKeyDictionary()
        for key, value in self.data.copy().items():
            o = key()
            if o is not None:
                new[o] = value
        return new
    __copy__ = copy

    def __deepcopy__(self, memo):
        from copy import deepcopy
        new = self.__class__()
        for key, value in self.data.copy().items():
            o = key()
            if o is not None:
                new[o] = deepcopy(value, memo)
        return new

    def get(self, key, default=None):
        return self.data.get(ref(key), default)

    def __contains__(self, key):
        try:
            wr = ref(key)
        except TypeError:
            return False
        return wr in self.data

    def items(self):
        for wr, value in self.data.copy().items():
            key = wr()
            if key is not None:
                yield (key, value)

    def keys(self):
        for wr in self.data.copy():
            obj = wr()
            if obj is not None:
                yield obj
    __iter__ = keys

    def values(self):
        for wr, value in self.data.copy().items():
            if wr() is not None:
                yield value

    def 取键弱引用表(self):
        """Return a list of weak references to the keys.

        The references are not guaranteed to be 'live' at the time
        they are used, so the result of calling the references needs
        to be checked before being used.  This can be used to avoid
        creating references that will cause the garbage collector to
        keep the keys around longer than needed.

        """
        return list(self.data)

    def popitem(self):
        while True:
            key, value = self.data.popitem()
            o = key()
            if o is not None:
                return (o, value)

    def pop(self, key, *args):
        return self.data.pop(ref(key), *args)

    def setdefault(self, key, default=None):
        return self.data.setdefault(ref(key, self._remove), default)

    def update(self, dict=None, /, **kwargs):
        d = self.data
        if dict is not None:
            if not hasattr(dict, 'items'):
                dict = type({})(dict)
            for key, value in dict.items():
                d[ref(key, self._remove)] = value
        if len(kwargs):
            self.update(kwargs)

    def __ior__(self, other):
        self.update(other)
        return self

    def __or__(self, other):
        if isinstance(other, _collections_abc.Mapping):
            c = self.copy()
            c.update(other)
            return c
        return NotImplemented

    def __ror__(self, other):
        if isinstance(other, _collections_abc.Mapping):
            c = self.__class__()
            c.update(other)
            c.update(self)
            return c
        return NotImplemented
_装类转发(WeakKeyDictionary, {'keyrefs': '取键弱引用表'}, {'keyrefs': '取键弱引用表'})

class finalize:
    """Class for finalization of weakrefable objects

    finalize(obj, func, *args, **kwargs) returns a callable finalizer
    object which will be called when obj is garbage collected. The
    first time the finalizer is called it evaluates func(*arg, **kwargs)
    and returns the result. After this the finalizer is dead, and
    calling it just returns None.

    When the program exits any remaining finalizers for which the
    atexit attribute is true will be run in reverse order of creation.
    By default atexit is true.
    """
    __slots__ = ()
    _registry = {}
    _shutdown = False
    _index_iter = itertools.count()
    _dirty = False
    _registered_with_atexit = False

    class _Info:
        __slots__ = ('weakref', 'func', 'args', 'kwargs', 'atexit', 'index')

    def __init__(self, obj, func, /, *args, **kwargs):
        if not self._registered_with_atexit:
            import atexit
            atexit.register(self._exitfunc)
            finalize._registered_with_atexit = True
        info = self._Info()
        info.weakref = ref(obj, self)
        info.func = func
        info.args = args
        info.kwargs = kwargs or None
        info.atexit = True
        info.index = next(self._index_iter)
        self._registry[self] = info
        finalize._dirty = True

    def __call__(self, _=None):
        """If alive then mark as dead and return func(*args, **kwargs);
        otherwise return None"""
        info = self._registry.pop(self, None)
        if info and (not self._shutdown):
            return info.func(*info.args, **info.kwargs or {})

    def 分离(self):
        """If alive then mark as dead and return (obj, func, args, kwargs);
        otherwise return None"""
        info = self._registry.get(self)
        obj = info and info.weakref()
        if obj is not None and self._registry.pop(self, None):
            return (obj, info.func, info.args, info.kwargs or {})

    def 窥视(self):
        """If alive then return (obj, func, args, kwargs);
        otherwise return None"""
        info = self._registry.get(self)
        obj = info and info.weakref()
        if obj is not None:
            return (obj, info.func, info.args, info.kwargs or {})

    @property
    def 存活吗(self):
        """Whether finalizer is alive"""
        return self in self._registry

    @property
    def atexit(self):
        """Whether finalizer should be called at exit"""
        info = self._registry.get(self)
        return bool(info) and info.atexit

    @atexit.setter
    def atexit(self, value):
        info = self._registry.get(self)
        if info:
            info.atexit = bool(value)

    def __repr__(self):
        info = self._registry.get(self)
        obj = info and info.weakref()
        if obj is None:
            return '<%s object at %#x; dead>' % (type(self).__name__, id(self))
        else:
            return '<%s object at %#x; for %r at %#x>' % (type(self).__name__, id(self), type(obj).__name__, id(obj))

    @classmethod
    def _select_for_exit(cls):
        L = [(f, i) for f, i in cls._registry.items() if i.atexit]
        L.sort(key=lambda item: item[1].index)
        return [f for f, i in L]

    @classmethod
    def _exitfunc(cls):
        reenable_gc = False
        try:
            if cls._registry:
                import gc
                if gc.isenabled():
                    reenable_gc = True
                    gc.disable()
                pending = None
                while True:
                    if pending is None or finalize._dirty:
                        pending = cls._select_for_exit()
                        finalize._dirty = False
                    if not pending:
                        break
                    f = pending.pop()
                    try:
                        f()
                    except Exception:
                        sys.excepthook(*sys.exc_info())
                    assert f not in cls._registry
        finally:
            finalize._shutdown = True
            if reenable_gc:
                gc.enable()
_装类转发(finalize, {'alive': '存活吗', 'detach': '分离', 'peek': '窥视'}, {'alive': '存活吗', 'detach': '分离', 'peek': '窥视'})


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
    '代理类型组': 'ProxyTypes',
    '弱值字典': 'WeakValueDictionary',
    '弱方法': 'WeakMethod',
    '弱键字典': 'WeakKeyDictionary',
    '终结器': 'finalize',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import weakref as _英文库
可调用代理类型 = _英文库.CallableProxyType
代理类型 = _英文库.ProxyType
弱引用类型 = _英文库.ReferenceType
弱集合 = _英文库.WeakSet
取弱引用数 = _英文库.getweakrefcount
取弱引用表 = _英文库.getweakrefs
代理 = _英文库.proxy
弱引用 = _英文库.ref

_成员别名 = {
    'WeakKeyDictionary': {
        'keyrefs': '取键弱引用表',
    },
    'WeakValueDictionary': {
        'itervaluerefs': '迭代值弱引用',
        'valuerefs': '取值弱引用表',
    },
    'finalize': {
        'alive': '存活吗',
        'detach': '分离',
        'peek': '窥视',
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
    'WeakKeyDictionary': {
        'keyrefs': '取键弱引用表',
    },
    'WeakValueDictionary': {
        'itervaluerefs': '迭代值弱引用',
        'valuerefs': '取值弱引用表',
    },
    'finalize': {
        'alive': '存活吗',
        'detach': '分离',
        'peek': '窥视',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '代理类型组',
    '弱值字典',
    '弱方法',
    '弱键字典',
    '终结器',
])

# ---- 转发层结束 ----
