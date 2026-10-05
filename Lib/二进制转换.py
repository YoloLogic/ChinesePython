# -*- coding: utf-8 -*-
"""二进制转换 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`binascii`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["binascii"]`，然后：

    python tools\汉化包装层.py binascii

可逆性：删这个文件 + 删词表那一段，英文 `binascii` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import binascii as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
错误 = __英文模块.Error
数据不完整 = __英文模块.Incomplete
base64转二进制 = __英文模块.a2b_base64
十六进制转二进制 = __英文模块.a2b_hex
QP转二进制 = __英文模块.a2b_qp
UU转二进制 = __英文模块.a2b_uu
二进制转base64 = __英文模块.b2a_base64
二进制转十六进制 = __英文模块.b2a_hex
二进制转QP = __英文模块.b2a_qp
二进制转UU = __英文模块.b2a_uu
crc32校验 = __英文模块.crc32
hqx校验 = __英文模块.crc_hqx
转十六进制串 = __英文模块.hexlify
十六进制串还原 = __英文模块.unhexlify

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
Error = __英文模块.Error
Incomplete = __英文模块.Incomplete
a2b_base64 = __英文模块.a2b_base64
a2b_hex = __英文模块.a2b_hex
a2b_qp = __英文模块.a2b_qp
a2b_uu = __英文模块.a2b_uu
b2a_base64 = __英文模块.b2a_base64
b2a_hex = __英文模块.b2a_hex
b2a_qp = __英文模块.b2a_qp
b2a_uu = __英文模块.b2a_uu
crc32 = __英文模块.crc32
crc_hqx = __英文模块.crc_hqx
hexlify = __英文模块.hexlify
unhexlify = __英文模块.unhexlify

__all__ = [
    'Error',
    'Incomplete',
    'a2b_base64',
    'a2b_hex',
    'a2b_qp',
    'a2b_uu',
    'b2a_base64',
    'b2a_hex',
    'b2a_qp',
    'b2a_uu',
    'crc32',
    'crc_hqx',
    'hexlify',
    'unhexlify',
    '错误',
    '数据不完整',
    'base64转二进制',
    '十六进制转二进制',
    'QP转二进制',
    'UU转二进制',
    '二进制转base64',
    '二进制转十六进制',
    '二进制转QP',
    '二进制转UU',
    'crc32校验',
    'hqx校验',
    '转十六进制串',
    '十六进制串还原',
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
