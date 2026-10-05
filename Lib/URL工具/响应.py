# -*- coding: utf-8 -*-
"""URL工具.响应 —— 汉语库（由 tools/汉化库.py 从 Lib/urllib/response.py 机械生成，**不要手改**）。

英文库 Lib/urllib.response.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py urllib
"""


"""Response classes used by urllib.

The base class, addbase, defines a minimal file-like interface,
including read() and readline().  The typical response object is an
addinfourl instance, which defines an info() method that returns
headers and a geturl() method that returns the url.
"""
_英文原名表 = {'addbase': '加基址', 'addclosehook': '加关闭钩子', 'addinfo': '加信息', 'addinfourl': '带信息的URL响应'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import tempfile
__all__ = ['addbase', 'addclosehook', 'addinfo', 'addinfourl']

class 加基址(tempfile._TemporaryFileWrapper):
    """Base class for addinfo and addclosehook. Is a good idea for garbage collection."""

    def __init__(self, fp):
        super(加基址, self).__init__(fp, '<urllib response>', delete=False)
        self.fp = fp

    def __repr__(self):
        return '<%s at %r whose fp = %r>' % (self.__class__.__name__, id(self), self.file)

    def __enter__(self):
        if self.fp.closed:
            raise ValueError('I/O operation on closed file')
        return self

    def __exit__(self, type, value, traceback):
        self.close()

class 加关闭钩子(加基址):
    """Class to add a close hook to an open file."""

    def __init__(self, fp, closehook, *hookargs):
        super(加关闭钩子, self).__init__(fp)
        self.closehook = closehook
        self.hookargs = hookargs

    def close(self):
        try:
            closehook = self.closehook
            hookargs = self.hookargs
            if closehook:
                self.closehook = None
                self.hookargs = None
                closehook(*hookargs)
        finally:
            super(加关闭钩子, self).close()

class 加信息(加基址):
    """class to add an info() method to an open file."""

    def __init__(self, fp, headers):
        super(加信息, self).__init__(fp)
        self.headers = headers

    def info(self):
        return self.headers

class 带信息的URL响应(加信息):
    """class to add info() and geturl() methods to an open file."""

    def __init__(self, fp, headers, url, code=None):
        super(带信息的URL响应, self).__init__(fp, headers)
        self.url = url
        self.code = code

    @property
    def status(self):
        return self.code

    def getcode(self):
        return self.code

    def geturl(self):
        return self.url


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'addbase': '加基址',
    'addclosehook': '加关闭钩子',
    'addinfo': '加信息',
    'addinfourl': '带信息的URL响应',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '加信息',
    '加关闭钩子',
    '加基址',
    '带信息的URL响应',
]

# ---- 转发层结束 ----
