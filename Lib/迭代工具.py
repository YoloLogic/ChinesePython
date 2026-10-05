# -*- coding: utf-8 -*-
"""迭代工具 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`itertools`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["itertools"]`，然后：

    python tools\汉化包装层.py itertools

可逆性：删这个文件 + 删词表那一段，英文 `itertools` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import itertools as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
累积 = __英文模块.accumulate
分批 = __英文模块.batched
串联 = __英文模块.chain
组合 = __英文模块.combinations
可重复组合 = __英文模块.combinations_with_replacement
筛选 = __英文模块.compress
计数 = __英文模块.count
循环 = __英文模块.cycle
条件丢弃 = __英文模块.dropwhile
过滤假值 = __英文模块.filterfalse
分组 = __英文模块.groupby
切片 = __英文模块.islice
相邻对 = __英文模块.pairwise
排列 = __英文模块.permutations
笛卡尔积 = __英文模块.product
重复 = __英文模块.repeat
解包映射 = __英文模块.starmap
条件取用 = __英文模块.takewhile
分流 = __英文模块.tee
最长拉链 = __英文模块.zip_longest

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
accumulate = __英文模块.accumulate
batched = __英文模块.batched
chain = __英文模块.chain
combinations = __英文模块.combinations
combinations_with_replacement = __英文模块.combinations_with_replacement
compress = __英文模块.compress
count = __英文模块.count
cycle = __英文模块.cycle
dropwhile = __英文模块.dropwhile
filterfalse = __英文模块.filterfalse
groupby = __英文模块.groupby
islice = __英文模块.islice
pairwise = __英文模块.pairwise
permutations = __英文模块.permutations
product = __英文模块.product
repeat = __英文模块.repeat
starmap = __英文模块.starmap
takewhile = __英文模块.takewhile
tee = __英文模块.tee
zip_longest = __英文模块.zip_longest

__all__ = [
    'accumulate',
    'batched',
    'chain',
    'combinations',
    'combinations_with_replacement',
    'compress',
    'count',
    'cycle',
    'dropwhile',
    'filterfalse',
    'groupby',
    'islice',
    'pairwise',
    'permutations',
    'product',
    'repeat',
    'starmap',
    'takewhile',
    'tee',
    'zip_longest',
    '累积',
    '分批',
    '串联',
    '组合',
    '可重复组合',
    '筛选',
    '计数',
    '循环',
    '条件丢弃',
    '过滤假值',
    '分组',
    '切片',
    '相邻对',
    '排列',
    '笛卡尔积',
    '重复',
    '解包映射',
    '条件取用',
    '分流',
    '最长拉链',
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
