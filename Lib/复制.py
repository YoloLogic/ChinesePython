# -*- coding: utf-8 -*-
"""复制 —— 汉语库（由 tools/汉化库.py 从 Lib/copy.py 机械生成，**不要手改**）。

英文库 Lib/copy.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 复制
"""


"""Generic (shallow and deep) copying operations.

Interface summary:

        import copy

        x = copy.copy(y)                # make a shallow copy of y
        x = copy.deepcopy(y)            # make a deep copy of y
        x = copy.replace(y, a=1, b=2)   # new object with fields replaced, as defined by `__replace__`

For module specific errors, copy.Error is raised.

The difference between shallow and deep copying is only relevant for
compound objects (objects that contain other objects, like lists or
class instances).

- A shallow copy constructs a new compound object and then (to the
  extent possible) inserts *the same objects* into it that the
  original contains.

- A deep copy constructs a new compound object and then, recursively,
  inserts *copies* into it of the objects found in the original.

Two problems often exist with deep copy operations that don't exist
with shallow copy operations:

 a) recursive objects (compound objects that, directly or indirectly,
    contain a reference to themselves) may cause a recursive loop

 b) because deep copy copies *everything* it may copy too much, e.g.
    administrative data structures that should be shared even between
    copies

Python's deep copy operation avoids these problems by:

 a) keeping a table of objects already copied during the current
    copying pass

 b) letting user-defined classes override the copying operation or the
    set of components copied

This version does not copy types like module, class, function, method,
nor stack trace, stack frame, nor file, socket, window, nor any
similar types.

Classes can use the same interfaces to control copying that they use
to control pickling: they can define methods called __getinitargs__(),
__getstate__() and __setstate__().  See the documentation for module
"pickle" for information on these methods.
"""
_英文原名表 = {'Error': '复制错误', 'copy': '复制', 'deepcopy': '深复制', 'replace': '替换'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import types
import weakref
from copyreg import dispatch_table

class 复制错误(Exception):
    pass
error = 复制错误
__all__ = ['Error', 'copy', 'deepcopy', 'replace']

def 复制(x):
    """Shallow copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
    """
    cls = type(x)
    if cls in _copy_atomic_types:
        return x
    if cls in _copy_builtin_containers:
        return cls.copy(x)
    if issubclass(cls, type):
        return x
    copier = getattr(cls, '__copy__', None)
    if copier is not None:
        return copier(x)
    reductor = dispatch_table.get(cls)
    if reductor is not None:
        rv = reductor(x)
    else:
        reductor = getattr(x, '__reduce_ex__', None)
        if reductor is not None:
            rv = reductor(4)
        else:
            reductor = getattr(x, '__reduce__', None)
            if reductor:
                rv = reductor()
            else:
                raise 复制错误('un(shallow)copyable object of type %s' % cls)
    if isinstance(rv, str):
        return x
    return _reconstruct(x, None, *rv)
_copy_atomic_types = {types.NoneType, int, float, bool, complex, str, tuple, bytes, frozenset, type, range, slice, property, types.BuiltinFunctionType, types.EllipsisType, types.NotImplementedType, types.FunctionType, types.CodeType, weakref.ref, super}
_copy_builtin_containers = {list, dict, set, bytearray}

def 深复制(x, memo=None, _nil=[]):
    """Deep copy operation on arbitrary Python objects.

    See the module's __doc__ string for more info.
    """
    cls = type(x)
    if cls in _atomic_types:
        return x
    d = id(x)
    if memo is None:
        memo = {}
    else:
        y = memo.get(d, _nil)
        if y is not _nil:
            return y
    copier = _deepcopy_dispatch.get(cls)
    if copier is not None:
        y = copier(x, memo)
    elif issubclass(cls, type):
        y = x
    else:
        copier = getattr(x, '__deepcopy__', None)
        if copier is not None:
            y = copier(memo)
        else:
            reductor = dispatch_table.get(cls)
            if reductor:
                rv = reductor(x)
            else:
                reductor = getattr(x, '__reduce_ex__', None)
                if reductor is not None:
                    rv = reductor(4)
                else:
                    reductor = getattr(x, '__reduce__', None)
                    if reductor:
                        rv = reductor()
                    else:
                        raise 复制错误('un(deep)copyable object of type %s' % cls)
            if isinstance(rv, str):
                y = x
            else:
                y = _reconstruct(x, memo, *rv)
    if y is not x:
        memo[d] = y
        _keep_alive(x, memo)
    return y
_atomic_types = {types.NoneType, types.EllipsisType, types.NotImplementedType, int, float, bool, complex, bytes, str, types.CodeType, type, range, types.BuiltinFunctionType, types.FunctionType, weakref.ref, property}
_deepcopy_dispatch = d = {}

def _deepcopy_list(x, memo, deepcopy=深复制):
    y = []
    memo[id(x)] = y
    append = y.append
    for a in x:
        append(deepcopy(a, memo))
    return y
d[list] = _deepcopy_list

def _deepcopy_tuple(x, memo, deepcopy=深复制):
    y = [deepcopy(a, memo) for a in x]
    try:
        return memo[id(x)]
    except KeyError:
        pass
    for k, j in zip(x, y):
        if k is not j:
            y = tuple(y)
            break
    else:
        y = x
    return y
d[tuple] = _deepcopy_tuple

def _deepcopy_dict(x, memo, deepcopy=深复制):
    y = {}
    memo[id(x)] = y
    for key, value in x.items():
        y[deepcopy(key, memo)] = deepcopy(value, memo)
    return y
d[dict] = _deepcopy_dict

def _deepcopy_method(x, memo):
    return type(x)(x.__func__, 深复制(x.__self__, memo))
d[types.MethodType] = _deepcopy_method
del d

def _keep_alive(x, memo):
    """Keeps a reference to the object x in the memo.

    Because we remember objects by their id, we have
    to assure that possibly temporary objects are kept
    alive by referencing them.
    We store a reference at the id of the memo, which should
    normally not be used unless someone tries to deepcopy
    the memo itself...
    """
    try:
        memo[id(memo)].append(x)
    except KeyError:
        memo[id(memo)] = [x]

def _reconstruct(x, memo, func, args, state=None, listiter=None, dictiter=None, *, deepcopy=深复制):
    deep = memo is not None
    if deep and args:
        args = (deepcopy(arg, memo) for arg in args)
    y = func(*args)
    if deep:
        memo[id(x)] = y
    if state is not None:
        if deep:
            state = deepcopy(state, memo)
        if hasattr(y, '__setstate__'):
            y.__setstate__(state)
        else:
            if isinstance(state, tuple) and len(state) == 2:
                state, slotstate = state
            else:
                slotstate = None
            if state is not None:
                y.__dict__.update(state)
            if slotstate is not None:
                for key, value in slotstate.items():
                    setattr(y, key, value)
    if listiter is not None:
        if deep:
            for item in listiter:
                item = deepcopy(item, memo)
                y.append(item)
        else:
            for item in listiter:
                y.append(item)
    if dictiter is not None:
        if deep:
            for key, value in dictiter:
                key = deepcopy(key, memo)
                value = deepcopy(value, memo)
                y[key] = value
        else:
            for key, value in dictiter:
                y[key] = value
    return y
del types, weakref

def 替换(obj, /, **changes):
    """Return a new object replacing specified fields with new values.

    This is especially useful for immutable objects, like named tuples or
    frozen dataclasses.
    """
    cls = obj.__class__
    func = getattr(cls, '__replace__', None)
    if func is None:
        raise TypeError(f'replace() does not support {cls.__name__} objects')
    return func(obj, **changes)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Error': '复制错误',
    'copy': '复制',
    'deepcopy': '深复制',
    'replace': '替换',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '复制',
    '复制错误',
    '替换',
    '深复制',
]

# ---- 转发层结束 ----
