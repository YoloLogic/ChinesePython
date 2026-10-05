# -*- coding: utf-8 -*-
"""WSGI参考.WSGI类型 —— 汉语库（由 tools/汉化库.py 从 Lib/wsgiref/types.py 机械生成，**不要手改**）。

英文库 Lib/wsgiref.types.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py wsgiref
"""


"""WSGI-related types for static type checking"""
from collections.abc import Callable, Iterable, Iterator
from types import TracebackType
from typing import Any, Protocol, TypeAlias
__all__ = ['StartResponse', 'WSGIEnvironment', 'WSGIApplication', 'InputStream', 'ErrorStream', 'FileWrapper']
_ExcInfo: TypeAlias = tuple[type[BaseException], BaseException, TracebackType]
_OptExcInfo: TypeAlias = _ExcInfo | tuple[None, None, None]

class StartResponse(Protocol):
    """start_response() callable as defined in PEP 3333"""

    def __call__(self, status: str, headers: list[tuple[str, str]], exc_info: _OptExcInfo | None=..., /) -> Callable[[bytes], object]:
        ...
WSGIEnvironment: TypeAlias = dict[str, Any]
WSGIApplication: TypeAlias = Callable[[WSGIEnvironment, StartResponse], Iterable[bytes]]

class InputStream(Protocol):
    """WSGI input stream as defined in PEP 3333"""

    def read(self, size: int=..., /) -> bytes:
        ...

    def readline(self, size: int=..., /) -> bytes:
        ...

    def readlines(self, hint: int=..., /) -> list[bytes]:
        ...

    def __iter__(self) -> Iterator[bytes]:
        ...

class ErrorStream(Protocol):
    """WSGI error stream as defined in PEP 3333"""

    def flush(self) -> object:
        ...

    def write(self, s: str, /) -> object:
        ...

    def writelines(self, seq: list[str], /) -> object:
        ...

class _Readable(Protocol):

    def read(self, size: int=..., /) -> bytes:
        ...

class FileWrapper(Protocol):
    """WSGI file wrapper as defined in PEP 3333"""

    def __call__(self, file: _Readable, block_size: int=..., /) -> Iterable[bytes]:
        ...


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# ---- 转发层结束 ----
