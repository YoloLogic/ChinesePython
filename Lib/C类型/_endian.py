# -*- coding: utf-8 -*-
"""C类型._endian —— 汉语库（由 tools/汉化库.py 从 Lib/ctypes/_endian.py 机械生成，**不要手改**）。

英文库 Lib/ctypes._endian.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py ctypes
"""


import sys
from C类型 import Array, Structure, Union
_array_type = type(Array)

def _other_endian(typ):
    """Return the type with the 'other' byte order.  Simple types like
    c_int and so on already have __ctype_be__ and __ctype_le__
    attributes which contain the types, for more complicated types
    arrays and structures are supported.
    """
    if hasattr(typ, _OTHER_ENDIAN):
        return getattr(typ, _OTHER_ENDIAN)
    if isinstance(typ, _array_type):
        return _other_endian(typ._type_) * typ._length_
    if issubclass(typ, (Structure, Union)):
        return typ
    raise TypeError('This type does not support other endian: %s' % typ)

class _swapped_meta:

    def __setattr__(self, attrname, value):
        if attrname == '_fields_':
            fields = []
            for desc in value:
                name = desc[0]
                typ = desc[1]
                rest = desc[2:]
                fields.append((name, _other_endian(typ)) + rest)
            value = fields
        super().__setattr__(attrname, value)

class _swapped_struct_meta(_swapped_meta, type(Structure)):
    pass

class _swapped_union_meta(_swapped_meta, type(Union)):
    pass
if sys.byteorder == 'little':
    _OTHER_ENDIAN = '__ctype_be__'
    LittleEndianStructure = Structure

    class BigEndianStructure(Structure, metaclass=_swapped_struct_meta):
        """Structure with big endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None
    LittleEndianUnion = Union

    class BigEndianUnion(Union, metaclass=_swapped_union_meta):
        """Union with big endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None
elif sys.byteorder == 'big':
    _OTHER_ENDIAN = '__ctype_le__'
    BigEndianStructure = Structure

    class LittleEndianStructure(Structure, metaclass=_swapped_struct_meta):
        """Structure with little endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None
    BigEndianUnion = Union

    class LittleEndianUnion(Union, metaclass=_swapped_union_meta):
        """Union with little endian byte order"""
        __slots__ = ()
        _swappedbytes_ = None
else:
    raise RuntimeError('Invalid byteorder')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
