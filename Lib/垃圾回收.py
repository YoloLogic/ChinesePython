# -*- coding: utf-8 -*-
"""垃圾回收 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`gc`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["gc"]`，然后：

    python tools\汉化包装层.py gc

可逆性：删这个文件 + 删词表那一段，英文 `gc` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import gc as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
调试可回收 = __英文模块.DEBUG_COLLECTABLE
调试泄漏 = __英文模块.DEBUG_LEAK
调试全部保留 = __英文模块.DEBUG_SAVEALL
调试统计 = __英文模块.DEBUG_STATS
调试不可回收 = __英文模块.DEBUG_UNCOLLECTABLE
回调表 = __英文模块.callbacks
回收 = __英文模块.collect
停用 = __英文模块.disable
启用 = __英文模块.enable
冻结 = __英文模块.freeze
垃圾表 = __英文模块.garbage
取计数 = __英文模块.get_count
取调试标志 = __英文模块.get_debug
取冻结数 = __英文模块.get_freeze_count
取对象表 = __英文模块.get_objects
取被引用者 = __英文模块.get_referents
取引用者 = __英文模块.get_referrers
取统计 = __英文模块.get_stats
取阈值 = __英文模块.get_threshold
已终结吗 = __英文模块.is_finalized
被跟踪吗 = __英文模块.is_tracked
已启用吗 = __英文模块.isenabled
设调试标志 = __英文模块.set_debug
设阈值 = __英文模块.set_threshold
解冻 = __英文模块.unfreeze

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
DEBUG_COLLECTABLE = __英文模块.DEBUG_COLLECTABLE
DEBUG_LEAK = __英文模块.DEBUG_LEAK
DEBUG_SAVEALL = __英文模块.DEBUG_SAVEALL
DEBUG_STATS = __英文模块.DEBUG_STATS
DEBUG_UNCOLLECTABLE = __英文模块.DEBUG_UNCOLLECTABLE
callbacks = __英文模块.callbacks
collect = __英文模块.collect
disable = __英文模块.disable
enable = __英文模块.enable
freeze = __英文模块.freeze
garbage = __英文模块.garbage
get_count = __英文模块.get_count
get_debug = __英文模块.get_debug
get_freeze_count = __英文模块.get_freeze_count
get_objects = __英文模块.get_objects
get_referents = __英文模块.get_referents
get_referrers = __英文模块.get_referrers
get_stats = __英文模块.get_stats
get_threshold = __英文模块.get_threshold
is_finalized = __英文模块.is_finalized
is_tracked = __英文模块.is_tracked
isenabled = __英文模块.isenabled
set_debug = __英文模块.set_debug
set_threshold = __英文模块.set_threshold
unfreeze = __英文模块.unfreeze

__all__ = [
    'DEBUG_COLLECTABLE',
    'DEBUG_LEAK',
    'DEBUG_SAVEALL',
    'DEBUG_STATS',
    'DEBUG_UNCOLLECTABLE',
    'callbacks',
    'collect',
    'disable',
    'enable',
    'freeze',
    'garbage',
    'get_count',
    'get_debug',
    'get_freeze_count',
    'get_objects',
    'get_referents',
    'get_referrers',
    'get_stats',
    'get_threshold',
    'is_finalized',
    'is_tracked',
    'isenabled',
    'set_debug',
    'set_threshold',
    'unfreeze',
    '调试可回收',
    '调试泄漏',
    '调试全部保留',
    '调试统计',
    '调试不可回收',
    '回调表',
    '回收',
    '停用',
    '启用',
    '冻结',
    '垃圾表',
    '取计数',
    '取调试标志',
    '取冻结数',
    '取对象表',
    '取被引用者',
    '取引用者',
    '取统计',
    '取阈值',
    '已终结吗',
    '被跟踪吗',
    '已启用吗',
    '设调试标志',
    '设阈值',
    '解冻',
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
