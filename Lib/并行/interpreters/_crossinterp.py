# -*- coding: utf-8 -*-
"""并行.interpreters/_crossinterp —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/interpreters/_crossinterp.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.interpreters/_crossinterp.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


"""Common code between queues and channels."""
_英文原名表 = {'ItemInterpreterDestroyed': '条目解释器已销毁', 'UNBOUND': '未绑定', 'UNBOUND_ERROR': '未绑定错误', 'UNBOUND_REMOVE': '未绑定移除', 'UnboundItem': '未绑定项', 'classonly': '仅限类内', 'resolve_unbound': '解析未绑定', 'serialize_unbound': '序列化未绑定'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)

class 条目解释器已销毁(Exception):
    """Raised when trying to get an item whose interpreter was destroyed."""

class 仅限类内:
    """A non-data descriptor that makes a value only visible on the class.

    This is like the "classmethod" builtin, but does not show up on
    instances of the class.  It may be used as a decorator.
    """

    def __init__(self, value):
        self.value = value
        self.getter = classmethod(value).__get__
        self.name = None

    def __set_name__(self, cls, name):
        if self.name is not None:
            raise TypeError('already used')
        self.name = name

    def __get__(self, obj, cls):
        if obj is not None:
            raise AttributeError(self.name)
        return self.getter(None, cls)

class 未绑定项:
    """Represents a cross-interpreter item no longer bound to an interpreter.

    An item is unbound when the interpreter that added it to the
    cross-interpreter container is destroyed.
    """
    __slots__ = ()

    @仅限类内
    def singleton(cls, kind, module, name='UNBOUND'):
        doc = cls.__doc__
        if doc:
            doc = doc.replace('cross-interpreter container', kind).replace('cross-interpreter', kind)
        subclass = type(f'Unbound{kind.capitalize()}Item', (cls,), {'_MODULE': module, '_NAME': name, '__doc__': doc})
        return object.__new__(subclass)
    _MODULE = __name__
    _NAME = 'UNBOUND'

    def __new__(cls):
        raise Exception(f'use {cls._MODULE}.{cls._NAME}')

    def __repr__(self):
        return f'{self._MODULE}.{self._NAME}'
未绑定 = object.__new__(未绑定项)
未绑定错误 = object()
未绑定移除 = object()
_UNBOUND_CONSTANT_TO_FLAG = {未绑定移除: 1, 未绑定错误: 2, 未绑定: 3}
_UNBOUND_FLAG_TO_CONSTANT = {v: k for k, v in _UNBOUND_CONSTANT_TO_FLAG.items()}

def 序列化未绑定(unbound):
    op = unbound
    try:
        flag = _UNBOUND_CONSTANT_TO_FLAG[op]
    except KeyError:
        raise NotImplementedError(f'unsupported unbound replacement op {op!r}')
    return (flag,)

def 解析未绑定(flag, exctype_destroyed):
    try:
        op = _UNBOUND_FLAG_TO_CONSTANT[flag]
    except KeyError:
        raise NotImplementedError(f'unsupported unbound replacement op {flag!r}')
    if op is 未绑定移除:
        raise NotImplementedError
    elif op is 未绑定错误:
        raise exctype_destroyed("item's original interpreter destroyed")
    elif op is 未绑定:
        return 未绑定
    else:
        raise NotImplementedError(repr(op))


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ItemInterpreterDestroyed': '条目解释器已销毁',
    'UNBOUND': '未绑定',
    'UNBOUND_ERROR': '未绑定错误',
    'UNBOUND_REMOVE': '未绑定移除',
    'UnboundItem': '未绑定项',
    'classonly': '仅限类内',
    'resolve_unbound': '解析未绑定',
    'serialize_unbound': '序列化未绑定',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
