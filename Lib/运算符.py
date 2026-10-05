# -*- coding: utf-8 -*-
"""运算符 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`operator`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["operator"]`，然后：

    python tools\汉化包装层.py operator

可逆性：删这个文件 + 删词表那一段，英文 `operator` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import operator as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
绝对值 = __英文模块.abs
加 = __英文模块.add
按位与 = __英文模块.and_
取属性器 = __英文模块.attrgetter
调用 = __英文模块.call
连接 = __英文模块.concat
包含 = __英文模块.contains
计数 = __英文模块.countOf
删项 = __英文模块.delitem
等于 = __英文模块.eq
整除 = __英文模块.floordiv
大于等于 = __英文模块.ge
取项 = __英文模块.getitem
大于 = __英文模块.gt
原地加 = __英文模块.iadd
原地按位与 = __英文模块.iand
原地连接 = __英文模块.iconcat
原地整除 = __英文模块.ifloordiv
原地左移 = __英文模块.ilshift
原地矩阵乘 = __英文模块.imatmul
原地取模 = __英文模块.imod
原地乘 = __英文模块.imul
取索引 = __英文模块.index
索引查找 = __英文模块.indexOf
按位取反旧名 = __英文模块.inv
按位取反 = __英文模块.invert
原地按位或 = __英文模块.ior
原地幂 = __英文模块.ipow
原地右移 = __英文模块.irshift
是同一对象 = __英文模块.is_
是None = __英文模块.is_none
不是同一对象 = __英文模块.is_not
不是None = __英文模块.is_not_none
原地减 = __英文模块.isub
取项器 = __英文模块.itemgetter
原地真除 = __英文模块.itruediv
原地按位异或 = __英文模块.ixor
小于等于 = __英文模块.le
长度提示 = __英文模块.length_hint
左移 = __英文模块.lshift
小于 = __英文模块.lt
矩阵乘 = __英文模块.matmul
调方法器 = __英文模块.methodcaller
取模 = __英文模块.mod
乘 = __英文模块.mul
不等于 = __英文模块.ne
取负 = __英文模块.neg
逻辑非 = __英文模块.not_
按位或 = __英文模块.or_
取正 = __英文模块.pos
幂 = __英文模块.pow
右移 = __英文模块.rshift
设项 = __英文模块.setitem
减 = __英文模块.sub
真除 = __英文模块.truediv
真伪 = __英文模块.truth
按位异或 = __英文模块.xor

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
abs = __英文模块.abs
add = __英文模块.add
and_ = __英文模块.and_
attrgetter = __英文模块.attrgetter
call = __英文模块.call
concat = __英文模块.concat
contains = __英文模块.contains
countOf = __英文模块.countOf
delitem = __英文模块.delitem
eq = __英文模块.eq
floordiv = __英文模块.floordiv
ge = __英文模块.ge
getitem = __英文模块.getitem
gt = __英文模块.gt
iadd = __英文模块.iadd
iand = __英文模块.iand
iconcat = __英文模块.iconcat
ifloordiv = __英文模块.ifloordiv
ilshift = __英文模块.ilshift
imatmul = __英文模块.imatmul
imod = __英文模块.imod
imul = __英文模块.imul
index = __英文模块.index
indexOf = __英文模块.indexOf
inv = __英文模块.inv
invert = __英文模块.invert
ior = __英文模块.ior
ipow = __英文模块.ipow
irshift = __英文模块.irshift
is_ = __英文模块.is_
is_none = __英文模块.is_none
is_not = __英文模块.is_not
is_not_none = __英文模块.is_not_none
isub = __英文模块.isub
itemgetter = __英文模块.itemgetter
itruediv = __英文模块.itruediv
ixor = __英文模块.ixor
le = __英文模块.le
length_hint = __英文模块.length_hint
lshift = __英文模块.lshift
lt = __英文模块.lt
matmul = __英文模块.matmul
methodcaller = __英文模块.methodcaller
mod = __英文模块.mod
mul = __英文模块.mul
ne = __英文模块.ne
neg = __英文模块.neg
not_ = __英文模块.not_
or_ = __英文模块.or_
pos = __英文模块.pos
pow = __英文模块.pow
rshift = __英文模块.rshift
setitem = __英文模块.setitem
sub = __英文模块.sub
truediv = __英文模块.truediv
truth = __英文模块.truth
xor = __英文模块.xor

__all__ = [
    'abs',
    'add',
    'and_',
    'attrgetter',
    'call',
    'concat',
    'contains',
    'countOf',
    'delitem',
    'eq',
    'floordiv',
    'ge',
    'getitem',
    'gt',
    'iadd',
    'iand',
    'iconcat',
    'ifloordiv',
    'ilshift',
    'imatmul',
    'imod',
    'imul',
    'index',
    'indexOf',
    'inv',
    'invert',
    'ior',
    'ipow',
    'irshift',
    'is_',
    'is_none',
    'is_not',
    'is_not_none',
    'isub',
    'itemgetter',
    'itruediv',
    'ixor',
    'le',
    'length_hint',
    'lshift',
    'lt',
    'matmul',
    'methodcaller',
    'mod',
    'mul',
    'ne',
    'neg',
    'not_',
    'or_',
    'pos',
    'pow',
    'rshift',
    'setitem',
    'sub',
    'truediv',
    'truth',
    'xor',
    '绝对值',
    '加',
    '按位与',
    '取属性器',
    '调用',
    '连接',
    '包含',
    '计数',
    '删项',
    '等于',
    '整除',
    '大于等于',
    '取项',
    '大于',
    '原地加',
    '原地按位与',
    '原地连接',
    '原地整除',
    '原地左移',
    '原地矩阵乘',
    '原地取模',
    '原地乘',
    '取索引',
    '索引查找',
    '按位取反旧名',
    '按位取反',
    '原地按位或',
    '原地幂',
    '原地右移',
    '是同一对象',
    '是None',
    '不是同一对象',
    '不是None',
    '原地减',
    '取项器',
    '原地真除',
    '原地按位异或',
    '小于等于',
    '长度提示',
    '左移',
    '小于',
    '矩阵乘',
    '调方法器',
    '取模',
    '乘',
    '不等于',
    '取负',
    '逻辑非',
    '按位或',
    '取正',
    '幂',
    '右移',
    '设项',
    '减',
    '真除',
    '真伪',
    '按位异或',
]


def __getattr__(名):
    """兜底转发：没在这儿显式列出来的名字（含私有名）照样到得了 C 那边。

    为什么必须有：硬约束是「英文原名一个都不能少」，而 C 模块的内部名
    我们没法一个个预料 —— 官方测试碰得到的、`dir(zlib)` 里有的一切，
    靠这一条全部兜住（PEP 562 的模块级 `__getattr__`）。
    """
    return getattr(__英文模块, 名)


def __dir__():
    # `dir()` 两边都算上：Shell 补全 / 官方那种按 `dir()` 算的判据都看得见。
    # ⚠ **壳自己的辅助函数不列**（D-147）：官方 `test_signal.test_functions_module_attr`
    #   会遍历 `dir()`，要求每个「非内置函数」的 `__module__` 是英文模块名 ——
    #   壳里的 `__getattr__`/`__dir__` 是 Python 函数、`__module__` 是汉语模块名
    #   ⇒ 列出来就挂（实测）。
    return sorted((set(globals()) | set(dir(__英文模块)))
                  - {"__getattr__", "__dir__", "__英文模块"})
