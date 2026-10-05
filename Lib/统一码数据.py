# -*- coding: utf-8 -*-
"""统一码数据 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`unicodedata`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["unicodedata"]`，然后：

    python tools\汉化包装层.py unicodedata

可逆性：删这个文件 + 删词表那一段，英文 `unicodedata` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import unicodedata as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
统一码数据库 = __英文模块.UCD
双向类别 = __英文模块.bidirectional
类别 = __英文模块.category
组合类 = __英文模块.combining
十进制值 = __英文模块.decimal
分解 = __英文模块.decomposition
数字值 = __英文模块.digit
东亚宽度 = __英文模块.east_asian_width
已规范化吗 = __英文模块.is_normalized
反查 = __英文模块.lookup
镜像吗 = __英文模块.mirrored
名字 = __英文模块.name
规范化 = __英文模块.normalize
数值 = __英文模块.numeric
统一码数据库3_2_0 = __英文模块.ucd_3_2_0
统一码数据版本 = __英文模块.unidata_version

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
UCD = __英文模块.UCD
bidirectional = __英文模块.bidirectional
category = __英文模块.category
combining = __英文模块.combining
decimal = __英文模块.decimal
decomposition = __英文模块.decomposition
digit = __英文模块.digit
east_asian_width = __英文模块.east_asian_width
is_normalized = __英文模块.is_normalized
lookup = __英文模块.lookup
mirrored = __英文模块.mirrored
name = __英文模块.name
normalize = __英文模块.normalize
numeric = __英文模块.numeric
ucd_3_2_0 = __英文模块.ucd_3_2_0
unidata_version = __英文模块.unidata_version

__all__ = [
    'UCD',
    'bidirectional',
    'category',
    'combining',
    'decimal',
    'decomposition',
    'digit',
    'east_asian_width',
    'is_normalized',
    'lookup',
    'mirrored',
    'name',
    'normalize',
    'numeric',
    'ucd_3_2_0',
    'unidata_version',
    '统一码数据库',
    '双向类别',
    '类别',
    '组合类',
    '十进制值',
    '分解',
    '数字值',
    '东亚宽度',
    '已规范化吗',
    '反查',
    '镜像吗',
    '名字',
    '规范化',
    '数值',
    '统一码数据库3_2_0',
    '统一码数据版本',
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
