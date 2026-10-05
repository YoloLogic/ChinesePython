# -*- coding: utf-8 -*-
"""内存映射文件 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`mmap`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["mmap"]`，然后：

    python tools\汉化包装层.py mmap

可逆性：删这个文件 + 删词表那一段，英文 `mmap` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import mmap as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
写时复制 = __英文模块.ACCESS_COPY
默认访问 = __英文模块.ACCESS_DEFAULT
只读 = __英文模块.ACCESS_READ
读写 = __英文模块.ACCESS_WRITE
分配粒度 = __英文模块.ALLOCATIONGRANULARITY
页大小 = __英文模块.PAGESIZE
错误 = __英文模块.error
内存映射 = __英文模块.mmap

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
ACCESS_COPY = __英文模块.ACCESS_COPY
ACCESS_DEFAULT = __英文模块.ACCESS_DEFAULT
ACCESS_READ = __英文模块.ACCESS_READ
ACCESS_WRITE = __英文模块.ACCESS_WRITE
ALLOCATIONGRANULARITY = __英文模块.ALLOCATIONGRANULARITY
PAGESIZE = __英文模块.PAGESIZE
error = __英文模块.error
mmap = __英文模块.mmap

__all__ = [
    'ACCESS_COPY',
    'ACCESS_DEFAULT',
    'ACCESS_READ',
    'ACCESS_WRITE',
    'ALLOCATIONGRANULARITY',
    'PAGESIZE',
    'error',
    'mmap',
    '写时复制',
    '默认访问',
    '只读',
    '读写',
    '分配粒度',
    '页大小',
    '错误',
    '内存映射',
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
