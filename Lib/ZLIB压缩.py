# -*- coding: utf-8 -*-
"""ZLIB压缩 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`zlib`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["zlib"]`，然后：

    python tools\汉化包装层.py zlib

可逆性：删这个文件 + 删词表那一段，英文 `zlib` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import zlib as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
DEFLATE方法 = __英文模块.DEFLATED
默认缓冲区大小 = __英文模块.DEF_BUF_SIZE
默认内存级别 = __英文模块.DEF_MEM_LEVEL
最大窗口位数 = __英文模块.MAX_WBITS
ZLIBNG版本 = __英文模块.ZLIBNG_VERSION
ZLIB运行时版本 = __英文模块.ZLIB_RUNTIME_VERSION
ZLIB版本 = __英文模块.ZLIB_VERSION
最佳压缩 = __英文模块.Z_BEST_COMPRESSION
最快速度 = __英文模块.Z_BEST_SPEED
块刷新 = __英文模块.Z_BLOCK
默认压缩级别 = __英文模块.Z_DEFAULT_COMPRESSION
默认策略 = __英文模块.Z_DEFAULT_STRATEGY
过滤策略 = __英文模块.Z_FILTERED
结束 = __英文模块.Z_FINISH
固定霍夫曼 = __英文模块.Z_FIXED
完全刷新 = __英文模块.Z_FULL_FLUSH
仅霍夫曼 = __英文模块.Z_HUFFMAN_ONLY
不压缩 = __英文模块.Z_NO_COMPRESSION
不刷新 = __英文模块.Z_NO_FLUSH
部分刷新 = __英文模块.Z_PARTIAL_FLUSH
行程编码策略 = __英文模块.Z_RLE
同步刷新 = __英文模块.Z_SYNC_FLUSH
允许树块 = __英文模块.Z_TREES
adler32校验 = __英文模块.adler32
压缩 = __英文模块.compress
压缩对象 = __英文模块.compressobj
crc32校验 = __英文模块.crc32
解压 = __英文模块.decompress
解压对象 = __英文模块.decompressobj
错误 = __英文模块.error

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
DEFLATED = __英文模块.DEFLATED
DEF_BUF_SIZE = __英文模块.DEF_BUF_SIZE
DEF_MEM_LEVEL = __英文模块.DEF_MEM_LEVEL
MAX_WBITS = __英文模块.MAX_WBITS
ZLIBNG_VERSION = __英文模块.ZLIBNG_VERSION
ZLIB_RUNTIME_VERSION = __英文模块.ZLIB_RUNTIME_VERSION
ZLIB_VERSION = __英文模块.ZLIB_VERSION
Z_BEST_COMPRESSION = __英文模块.Z_BEST_COMPRESSION
Z_BEST_SPEED = __英文模块.Z_BEST_SPEED
Z_BLOCK = __英文模块.Z_BLOCK
Z_DEFAULT_COMPRESSION = __英文模块.Z_DEFAULT_COMPRESSION
Z_DEFAULT_STRATEGY = __英文模块.Z_DEFAULT_STRATEGY
Z_FILTERED = __英文模块.Z_FILTERED
Z_FINISH = __英文模块.Z_FINISH
Z_FIXED = __英文模块.Z_FIXED
Z_FULL_FLUSH = __英文模块.Z_FULL_FLUSH
Z_HUFFMAN_ONLY = __英文模块.Z_HUFFMAN_ONLY
Z_NO_COMPRESSION = __英文模块.Z_NO_COMPRESSION
Z_NO_FLUSH = __英文模块.Z_NO_FLUSH
Z_PARTIAL_FLUSH = __英文模块.Z_PARTIAL_FLUSH
Z_RLE = __英文模块.Z_RLE
Z_SYNC_FLUSH = __英文模块.Z_SYNC_FLUSH
Z_TREES = __英文模块.Z_TREES
adler32 = __英文模块.adler32
compress = __英文模块.compress
compressobj = __英文模块.compressobj
crc32 = __英文模块.crc32
decompress = __英文模块.decompress
decompressobj = __英文模块.decompressobj
error = __英文模块.error

__all__ = [
    'DEFLATED',
    'DEF_BUF_SIZE',
    'DEF_MEM_LEVEL',
    'MAX_WBITS',
    'ZLIBNG_VERSION',
    'ZLIB_RUNTIME_VERSION',
    'ZLIB_VERSION',
    'Z_BEST_COMPRESSION',
    'Z_BEST_SPEED',
    'Z_BLOCK',
    'Z_DEFAULT_COMPRESSION',
    'Z_DEFAULT_STRATEGY',
    'Z_FILTERED',
    'Z_FINISH',
    'Z_FIXED',
    'Z_FULL_FLUSH',
    'Z_HUFFMAN_ONLY',
    'Z_NO_COMPRESSION',
    'Z_NO_FLUSH',
    'Z_PARTIAL_FLUSH',
    'Z_RLE',
    'Z_SYNC_FLUSH',
    'Z_TREES',
    'adler32',
    'compress',
    'compressobj',
    'crc32',
    'decompress',
    'decompressobj',
    'error',
    'DEFLATE方法',
    '默认缓冲区大小',
    '默认内存级别',
    '最大窗口位数',
    'ZLIBNG版本',
    'ZLIB运行时版本',
    'ZLIB版本',
    '最佳压缩',
    '最快速度',
    '块刷新',
    '默认压缩级别',
    '默认策略',
    '过滤策略',
    '结束',
    '固定霍夫曼',
    '完全刷新',
    '仅霍夫曼',
    '不压缩',
    '不刷新',
    '部分刷新',
    '行程编码策略',
    '同步刷新',
    '允许树块',
    'adler32校验',
    '压缩',
    '压缩对象',
    'crc32校验',
    '解压',
    '解压对象',
    '错误',
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
