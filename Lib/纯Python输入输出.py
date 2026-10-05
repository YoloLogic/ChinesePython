# -*- coding: utf-8 -*-
"""纯Python输入输出 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`_pyio`（`io` 的纯 Python 实现；官方 `test_io` 的 Py* 那一半测它 —— 必须跟 `输入输出` **同时**换上、用同一套中文名（D-143））。
改名字 = 改 `tools\库词表.py` 里的 `包装层["_pyio"]`，然后：

    python tools\汉化包装层.py _pyio

可逆性：删这个文件 + 删词表那一段，英文 `_pyio` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import _pyio as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
阻塞IO错误 = __英文模块.BlockingIOError
缓冲IO基础 = __英文模块.BufferedIOBase
缓冲读写对 = __英文模块.BufferedRWPair
缓冲随机访问 = __英文模块.BufferedRandom
缓冲读取器 = __英文模块.BufferedReader
缓冲写入器 = __英文模块.BufferedWriter
字节流IO = __英文模块.BytesIO
默认缓冲大小 = __英文模块.DEFAULT_BUFFER_SIZE
文件IO = __英文模块.FileIO
IO基础 = __英文模块.IOBase
增量换行解码器 = __英文模块.IncrementalNewlineDecoder
原始IO基础 = __英文模块.RawIOBase
读取器 = __英文模块.Reader
定位当前位置 = __英文模块.SEEK_CUR
定位末尾 = __英文模块.SEEK_END
定位起点 = __英文模块.SEEK_SET
字符串IO = __英文模块.StringIO
文本IO基础 = __英文模块.TextIOBase
文本IO包装器 = __英文模块.TextIOWrapper
不支持的操作 = __英文模块.UnsupportedOperation
写入器 = __英文模块.Writer
打开 = __英文模块.open
打开代码文件 = __英文模块.open_code
文本编码 = __英文模块.text_encoding

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
BlockingIOError = __英文模块.BlockingIOError
BufferedIOBase = __英文模块.BufferedIOBase
BufferedRWPair = __英文模块.BufferedRWPair
BufferedRandom = __英文模块.BufferedRandom
BufferedReader = __英文模块.BufferedReader
BufferedWriter = __英文模块.BufferedWriter
BytesIO = __英文模块.BytesIO
DEFAULT_BUFFER_SIZE = __英文模块.DEFAULT_BUFFER_SIZE
FileIO = __英文模块.FileIO
IOBase = __英文模块.IOBase
IncrementalNewlineDecoder = __英文模块.IncrementalNewlineDecoder
RawIOBase = __英文模块.RawIOBase
Reader = __英文模块.Reader
SEEK_CUR = __英文模块.SEEK_CUR
SEEK_END = __英文模块.SEEK_END
SEEK_SET = __英文模块.SEEK_SET
StringIO = __英文模块.StringIO
TextIOBase = __英文模块.TextIOBase
TextIOWrapper = __英文模块.TextIOWrapper
UnsupportedOperation = __英文模块.UnsupportedOperation
Writer = __英文模块.Writer
open = __英文模块.open
open_code = __英文模块.open_code
text_encoding = __英文模块.text_encoding

__all__ = [
    'BlockingIOError',
    'BufferedIOBase',
    'BufferedRWPair',
    'BufferedRandom',
    'BufferedReader',
    'BufferedWriter',
    'BytesIO',
    'DEFAULT_BUFFER_SIZE',
    'FileIO',
    'IOBase',
    'IncrementalNewlineDecoder',
    'RawIOBase',
    'Reader',
    'SEEK_CUR',
    'SEEK_END',
    'SEEK_SET',
    'StringIO',
    'TextIOBase',
    'TextIOWrapper',
    'UnsupportedOperation',
    'Writer',
    'open',
    'open_code',
    'text_encoding',
    '缓冲IO基础',
    '缓冲读写对',
    '缓冲随机访问',
    '缓冲读取器',
    '缓冲写入器',
    '字节流IO',
    '默认缓冲大小',
    '文件IO',
    'IO基础',
    '增量换行解码器',
    '原始IO基础',
    '读取器',
    '定位当前位置',
    '定位末尾',
    '定位起点',
    '字符串IO',
    '文本IO基础',
    '文本IO包装器',
    '不支持的操作',
    '写入器',
    '打开',
    '文本编码',
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
