# -*- coding: utf-8 -*-
"""多进程.sharedctypes —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/sharedctypes.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.sharedctypes.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Array': '数组', 'RawArray': '原始数组', 'RawValue': '原始值', 'Synchronized': '已同步', 'SynchronizedArray': '同步数组', 'SynchronizedBase': '同步基类', 'SynchronizedString': '同步字符串', 'Value': '值', 'make_property': '造属性', 'synchronized': '同步化'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import ctypes
import weakref
from . import heap
from . import get_context
from .context import reduction, assert_spawning
_ForkingPickler = reduction.ForkingPickler
__all__ = ['RawValue', 'RawArray', 'Value', 'Array', 'copy', 'synchronized']
typecode_to_type = {'c': ctypes.c_char, 'u': ctypes.c_wchar, 'b': ctypes.c_byte, 'B': ctypes.c_ubyte, 'h': ctypes.c_short, 'H': ctypes.c_ushort, 'i': ctypes.c_int, 'I': ctypes.c_uint, 'l': ctypes.c_long, 'L': ctypes.c_ulong, 'q': ctypes.c_longlong, 'Q': ctypes.c_ulonglong, 'f': ctypes.c_float, 'd': ctypes.c_double}

def _new_value(type_):
    size = ctypes.sizeof(type_)
    wrapper = heap.BufferWrapper(size)
    return rebuild_ctype(type_, wrapper, None)

def 原始值(typecode_or_type, *args):
    """
    Returns a ctypes object allocated from shared memory
    """
    type_ = typecode_to_type.get(typecode_or_type, typecode_or_type)
    obj = _new_value(type_)
    ctypes.memset(ctypes.addressof(obj), 0, ctypes.sizeof(obj))
    obj.__init__(*args)
    return obj

def 原始数组(typecode_or_type, size_or_initializer):
    """
    Returns a ctypes array allocated from shared memory
    """
    type_ = typecode_to_type.get(typecode_or_type, typecode_or_type)
    if isinstance(size_or_initializer, int):
        type_ = type_ * size_or_initializer
        obj = _new_value(type_)
        ctypes.memset(ctypes.addressof(obj), 0, ctypes.sizeof(obj))
        return obj
    else:
        type_ = type_ * len(size_or_initializer)
        result = _new_value(type_)
        result.__init__(*size_or_initializer)
        return result

def 值(typecode_or_type, *args, lock=True, ctx=None):
    """
    Return a synchronization wrapper for a Value
    """
    obj = 原始值(typecode_or_type, *args)
    if lock is False:
        return obj
    if lock in (True, None):
        ctx = ctx or get_context()
        lock = ctx.RLock()
    if not hasattr(lock, 'acquire'):
        raise AttributeError("%r has no method 'acquire'" % lock)
    return 同步化(obj, lock, ctx=ctx)

def 数组(typecode_or_type, size_or_initializer, *, lock=True, ctx=None):
    """
    Return a synchronization wrapper for a RawArray
    """
    obj = 原始数组(typecode_or_type, size_or_initializer)
    if lock is False:
        return obj
    if lock in (True, None):
        ctx = ctx or get_context()
        lock = ctx.RLock()
    if not hasattr(lock, 'acquire'):
        raise AttributeError("%r has no method 'acquire'" % lock)
    return 同步化(obj, lock, ctx=ctx)

def copy(obj):
    new_obj = _new_value(type(obj))
    ctypes.pointer(new_obj)[0] = obj
    return new_obj

def 同步化(obj, lock=None, ctx=None):
    assert not isinstance(obj, 同步基类), 'object already synchronized'
    ctx = ctx or get_context()
    if isinstance(obj, ctypes._SimpleCData):
        return 已同步(obj, lock, ctx)
    elif isinstance(obj, ctypes.Array):
        if obj._type_ is ctypes.c_char:
            return 同步字符串(obj, lock, ctx)
        return 同步数组(obj, lock, ctx)
    else:
        cls = type(obj)
        try:
            scls = class_cache[cls]
        except KeyError:
            names = [field[0] for field in cls._fields_]
            d = {name: 造属性(name) for name in names}
            classname = 'Synchronized' + cls.__name__
            scls = class_cache[cls] = type(classname, (同步基类,), d)
        return scls(obj, lock, ctx)

def reduce_ctype(obj):
    assert_spawning(obj)
    if isinstance(obj, ctypes.Array):
        return (rebuild_ctype, (obj._type_, obj._wrapper, obj._length_))
    else:
        return (rebuild_ctype, (type(obj), obj._wrapper, None))

def rebuild_ctype(type_, wrapper, length):
    if length is not None:
        type_ = type_ * length
    _ForkingPickler.register(type_, reduce_ctype)
    buf = wrapper.create_memoryview()
    obj = type_.from_buffer(buf)
    obj._wrapper = wrapper
    return obj

def 造属性(name):
    try:
        return prop_cache[name]
    except KeyError:
        d = {}
        exec(template % ((name,) * 7), d)
        prop_cache[name] = d[name]
        return d[name]
template = '\ndef get%s(self):\n    self.acquire()\n    try:\n        return self._obj.%s\n    finally:\n        self.release()\ndef set%s(self, value):\n    self.acquire()\n    try:\n        self._obj.%s = value\n    finally:\n        self.release()\n%s = property(get%s, set%s)\n'
prop_cache = {}
class_cache = weakref.WeakKeyDictionary()

class 同步基类(object):

    def __init__(self, obj, lock=None, ctx=None):
        self._obj = obj
        if lock:
            self._lock = lock
        else:
            ctx = ctx or get_context(force=True)
            self._lock = ctx.RLock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

    def __reduce__(self):
        assert_spawning(self)
        return (同步化, (self._obj, self._lock))

    def get_obj(self):
        return self._obj

    def get_lock(self):
        return self._lock

    def __repr__(self):
        return '<%s wrapper for %s>' % (type(self).__name__, self._obj)

class 已同步(同步基类):
    value = 造属性('value')

class 同步数组(同步基类):

    def __len__(self):
        return len(self._obj)

    def __getitem__(self, i):
        with self:
            return self._obj[i]

    def __setitem__(self, i, value):
        with self:
            self._obj[i] = value

    def __getslice__(self, start, stop):
        with self:
            return self._obj[start:stop]

    def __setslice__(self, start, stop, values):
        with self:
            self._obj[start:stop] = values

class 同步字符串(同步数组):
    value = 造属性('value')
    raw = 造属性('raw')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Array': '数组',
    'RawArray': '原始数组',
    'RawValue': '原始值',
    'Synchronized': '已同步',
    'SynchronizedArray': '同步数组',
    'SynchronizedBase': '同步基类',
    'SynchronizedString': '同步字符串',
    'Value': '值',
    'make_property': '造属性',
    'synchronized': '同步化',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '值',
    '原始值',
    '原始数组',
    '同步化',
    '数组',
])

# ---- 转发层结束 ----
