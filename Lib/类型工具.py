# -*- coding: utf-8 -*-
"""类型工具 —— 汉语库（由 tools/汉化库.py 从 Lib/types.py 机械生成，**不要手改**）。

英文库 Lib/types.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 类型工具
"""


"""
Define names for built-in types that aren't directly accessible as a builtin.
"""
_英文原名表 = {'DynamicClassAttribute': '动态类属性', 'coroutine': '协程', 'get_original_bases': '取原始基类', 'new_class': '新建类', 'prepare_class': '准备类', 'resolve_bases': '解析基类'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
try:
    from _types import *
except ImportError:
    import sys

    def _f():
        pass
    FunctionType = type(_f)
    LambdaType = type(lambda: None)
    CodeType = type(_f.__code__)
    MappingProxyType = type(type.__dict__)
    SimpleNamespace = type(sys.implementation)

    def _cell_factory():
        a = 1

        def f():
            nonlocal a
        return f.__closure__[0]
    CellType = type(_cell_factory())

    def _g():
        yield 1
    GeneratorType = type(_g())

    async def _c():
        pass
    _c = _c()
    CoroutineType = type(_c)
    _c.close()

    async def _ag():
        yield
    _ag = _ag()
    AsyncGeneratorType = type(_ag)

    class _C:

        def _m(self):
            pass
    MethodType = type(_C()._m)
    BuiltinFunctionType = type(len)
    BuiltinMethodType = type([].append)
    WrapperDescriptorType = type(object.__init__)
    MethodWrapperType = type(object().__str__)
    MethodDescriptorType = type(str.join)
    ClassMethodDescriptorType = type(dict.__dict__['fromkeys'])
    ModuleType = type(sys)
    try:
        raise TypeError
    except TypeError as exc:
        TracebackType = type(exc.__traceback__)
        FrameType = type(exc.__traceback__.tb_frame)
    GetSetDescriptorType = type(FunctionType.__code__)
    MemberDescriptorType = type(FunctionType.__globals__)
    GenericAlias = type(list[int])
    UnionType = type(int | str)
    EllipsisType = type(Ellipsis)
    NoneType = type(None)
    NotImplementedType = type(NotImplemented)
    del sys, _f, _g, _C, _c, _ag, _cell_factory

def 新建类(name, bases=(), kwds=None, exec_body=None):
    """Create a class object dynamically using the appropriate metaclass."""
    resolved_bases = 解析基类(bases)
    meta, ns, kwds = 准备类(name, resolved_bases, kwds)
    if exec_body is not None:
        exec_body(ns)
    if resolved_bases is not bases:
        ns['__orig_bases__'] = bases
    return meta(name, resolved_bases, ns, **kwds)

def 解析基类(bases):
    """Resolve MRO entries dynamically as specified by PEP 560."""
    new_bases = list(bases)
    updated = False
    shift = 0
    for i, base in enumerate(bases):
        if isinstance(base, type):
            continue
        if not hasattr(base, '__mro_entries__'):
            continue
        new_base = base.__mro_entries__(bases)
        updated = True
        if not isinstance(new_base, tuple):
            raise TypeError('__mro_entries__ must return a tuple')
        else:
            new_bases[i + shift:i + shift + 1] = new_base
            shift += len(new_base) - 1
    if not updated:
        return bases
    return tuple(new_bases)

def 准备类(name, bases=(), kwds=None):
    """Call the __prepare__ method of the appropriate metaclass.

    Returns (metaclass, namespace, kwds) as a 3-tuple

    *metaclass* is the appropriate metaclass
    *namespace* is the prepared class namespace
    *kwds* is an updated copy of the passed in kwds argument with any
    'metaclass' entry removed. If no kwds argument is passed in, this will
    be an empty dict.
    """
    if kwds is None:
        kwds = {}
    else:
        kwds = dict(kwds)
    if 'metaclass' in kwds:
        meta = kwds.pop('metaclass')
    elif bases:
        meta = type(bases[0])
    else:
        meta = type
    if isinstance(meta, type):
        meta = _calculate_meta(meta, bases)
    if hasattr(meta, '__prepare__'):
        ns = meta.__prepare__(name, bases, **kwds)
    else:
        ns = {}
    return (meta, ns, kwds)

def _calculate_meta(meta, bases):
    """Calculate the most derived metaclass."""
    winner = meta
    for base in bases:
        base_meta = type(base)
        if issubclass(winner, base_meta):
            continue
        if issubclass(base_meta, winner):
            winner = base_meta
            continue
        raise TypeError('metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases')
    return winner

def 取原始基类(cls, /):
    """Return the class's "original" bases prior to modification by `__mro_entries__`.

    Examples::

        from typing import TypeVar, Generic, NamedTuple, TypedDict

        T = TypeVar("T")
        class Foo(Generic[T]): ...
        class Bar(Foo[int], float): ...
        class Baz(list[str]): ...
        Eggs = NamedTuple("Eggs", [("a", int), ("b", str)])
        Spam = TypedDict("Spam", {"a": int, "b": str})

        assert get_original_bases(Bar) == (Foo[int], float)
        assert get_original_bases(Baz) == (list[str],)
        assert get_original_bases(Eggs) == (NamedTuple,)
        assert get_original_bases(Spam) == (TypedDict,)
        assert get_original_bases(int) == (object,)
    """
    try:
        return cls.__dict__.get('__orig_bases__', cls.__bases__)
    except AttributeError:
        raise TypeError(f'Expected an instance of type, not {type(cls).__name__!r}') from None

class 动态类属性:
    """Route attribute access on a class to __getattr__.

    This is a descriptor, used to define attributes that act differently
    when accessed through an instance and through a class.  Instance access
    remains normal, but access to an attribute through a class will be
    routed to the class's __getattr__ method; this is done by raising
    AttributeError.

    This allows one to have properties active on an instance, and have
    virtual attributes on the class with the same name.  (Enum used this
    between Python versions 3.4 - 3.9 .)

    Subclass from this to use a different method of accessing virtual
    attributes and still be treated properly by the inspect module.  (Enum
    uses this since Python 3.10 .)

    """

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or fget.__doc__
        self.overwrite_doc = doc is None
        self.__isabstractmethod__ = bool(getattr(fget, '__isabstractmethod__', False))

    def __get__(self, instance, ownerclass=None):
        if instance is None:
            if self.__isabstractmethod__:
                return self
            raise AttributeError()
        elif self.fget is None:
            raise AttributeError('unreadable attribute')
        return self.fget(instance)

    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)

    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)

    def getter(self, fget):
        fdoc = fget.__doc__ if self.overwrite_doc else None
        result = type(self)(fget, self.fset, self.fdel, fdoc or self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def setter(self, fset):
        result = type(self)(self.fget, fset, self.fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

    def deleter(self, fdel):
        result = type(self)(self.fget, self.fset, fdel, self.__doc__)
        result.overwrite_doc = self.overwrite_doc
        return result

class _GeneratorWrapper:

    def __init__(self, gen):
        self.__wrapped = gen
        self.__isgen = gen.__class__ is GeneratorType
        self.__name__ = getattr(gen, '__name__', None)
        self.__qualname__ = getattr(gen, '__qualname__', None)

    def send(self, val):
        return self.__wrapped.send(val)

    def throw(self, tp, *rest):
        return self.__wrapped.throw(tp, *rest)

    def close(self):
        return self.__wrapped.close()

    @property
    def gi_code(self):
        return self.__wrapped.gi_code

    @property
    def gi_frame(self):
        return self.__wrapped.gi_frame

    @property
    def gi_running(self):
        return self.__wrapped.gi_running

    @property
    def gi_yieldfrom(self):
        return self.__wrapped.gi_yieldfrom

    @property
    def gi_suspended(self):
        return self.__wrapped.gi_suspended
    cr_code = gi_code
    cr_frame = gi_frame
    cr_running = gi_running
    cr_await = gi_yieldfrom
    cr_suspended = gi_suspended

    def __next__(self):
        return next(self.__wrapped)

    def __iter__(self):
        if self.__isgen:
            return self.__wrapped
        return self
    __await__ = __iter__

def 协程(func):
    """Convert regular generator function to a coroutine."""
    if not callable(func):
        raise TypeError('types.coroutine() expects a callable')
    if func.__class__ is FunctionType and getattr(func, '__code__', None).__class__ is CodeType:
        co_flags = func.__code__.co_flags
        if co_flags & 384:
            return func
        if co_flags & 32:
            co = func.__code__
            func.__code__ = co.replace(co_flags=co.co_flags | 256)
            return func
    import functools
    import _collections_abc

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        coro = func(*args, **kwargs)
        if coro.__class__ is CoroutineType or (coro.__class__ is GeneratorType and coro.gi_code.co_flags & 256):
            return coro
        if isinstance(coro, _collections_abc.Generator) and (not isinstance(coro, _collections_abc.Coroutine)):
            return _GeneratorWrapper(coro)
        return coro
    return wrapped
__all__ = [n for n in globals() if not n.startswith('_')]


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'DynamicClassAttribute': '动态类属性',
    'coroutine': '协程',
    'get_original_bases': '取原始基类',
    'new_class': '新建类',
    'prepare_class': '准备类',
    'resolve_bases': '解析基类',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
