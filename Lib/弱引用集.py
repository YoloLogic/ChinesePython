# -*- coding: utf-8 -*-
"""弱引用集 —— 汉语库（由 tools/汉化库.py 从 Lib/_weakrefset.py 机械生成，**不要手改**）。

英文库 Lib/_weakrefset.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 弱引用集
"""


_英文原名表 = {'WeakSet': '弱集合'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from _weakref import ref
from types import GenericAlias
__all__ = ['WeakSet']

class 弱集合:

    def __init__(self, data=None):
        self.data = set()

        def _remove(item, selfref=ref(self)):
            self = selfref()
            if self is not None:
                self.data.discard(item)
        self._remove = _remove
        if data is not None:
            self.update(data)

    def __iter__(self):
        for itemref in self.data.copy():
            item = itemref()
            if item is not None:
                yield item

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        try:
            wr = ref(item)
        except TypeError:
            return False
        return wr in self.data

    def __reduce__(self):
        return (self.__class__, (list(self),), self.__getstate__())

    def add(self, item):
        self.data.add(ref(item, self._remove))

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def pop(self):
        while True:
            try:
                itemref = self.data.pop()
            except KeyError:
                raise KeyError('pop from empty WeakSet') from None
            item = itemref()
            if item is not None:
                return item

    def remove(self, item):
        self.data.remove(ref(item))

    def discard(self, item):
        self.data.discard(ref(item))

    def update(self, other):
        for element in other:
            self.add(element)

    def __ior__(self, other):
        self.update(other)
        return self

    def difference(self, other):
        newset = self.copy()
        newset.difference_update(other)
        return newset
    __sub__ = difference

    def difference_update(self, other):
        self.__isub__(other)

    def __isub__(self, other):
        if self is other:
            self.data.clear()
        else:
            self.data.difference_update((ref(item) for item in other))
        return self

    def intersection(self, other):
        return self.__class__((item for item in other if item in self))
    __and__ = intersection

    def intersection_update(self, other):
        self.__iand__(other)

    def __iand__(self, other):
        self.data.intersection_update((ref(item) for item in other))
        return self

    def issubset(self, other):
        return self.data.issubset((ref(item) for item in other))
    __le__ = issubset

    def __lt__(self, other):
        return self.data < set(map(ref, other))

    def issuperset(self, other):
        return self.data.issuperset((ref(item) for item in other))
    __ge__ = issuperset

    def __gt__(self, other):
        return self.data > set(map(ref, other))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.data == set(map(ref, other))

    def symmetric_difference(self, other):
        newset = self.copy()
        newset.symmetric_difference_update(other)
        return newset
    __xor__ = symmetric_difference

    def symmetric_difference_update(self, other):
        self.__ixor__(other)

    def __ixor__(self, other):
        if self is other:
            self.data.clear()
        else:
            self.data.symmetric_difference_update((ref(item, self._remove) for item in other))
        return self

    def union(self, other):
        return self.__class__((e for s in (self, other) for e in s))
    __or__ = union

    def isdisjoint(self, other):
        return len(self.intersection(other)) == 0

    def __repr__(self):
        return repr(self.data)
    __class_getitem__ = classmethod(GenericAlias)
import _weakrefset as _英文身份源
弱集合 = _英文身份源.WeakSet


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import _weakrefset as _英文库
弱集合 = _英文库.WeakSet
_模块别名 = {
    'WeakSet': '弱集合',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '弱集合',
])

# ---- 转发层结束 ----
