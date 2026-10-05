# -*- coding: utf-8 -*-
"""结构体 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`struct`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["struct"]`，然后：

    python tools\汉化包装层.py struct

可逆性：删这个文件 + 删词表那一段，英文 `struct` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import struct as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
结构体类型 = __英文模块.Struct
算大小 = __英文模块.calcsize
错误 = __英文模块.error
迭代解包 = __英文模块.iter_unpack
打包 = __英文模块.pack
打包进缓冲区 = __英文模块.pack_into
解包 = __英文模块.unpack
从缓冲区解包 = __英文模块.unpack_from

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
Struct = __英文模块.Struct
calcsize = __英文模块.calcsize
error = __英文模块.error
iter_unpack = __英文模块.iter_unpack
pack = __英文模块.pack
pack_into = __英文模块.pack_into
unpack = __英文模块.unpack
unpack_from = __英文模块.unpack_from

__all__ = [
    'Struct',
    'calcsize',
    'error',
    'iter_unpack',
    'pack',
    'pack_into',
    'unpack',
    'unpack_from',
    '结构体类型',
    '算大小',
    '错误',
    '迭代解包',
    '打包',
    '打包进缓冲区',
    '解包',
    '从缓冲区解包',
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
