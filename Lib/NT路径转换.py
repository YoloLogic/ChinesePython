# -*- coding: utf-8 -*-
"""NT路径转换 —— 汉语库（由 tools/汉化库.py 从 Lib/nturl2path.py 机械生成，**不要手改**）。

英文库 Lib/nturl2path.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py NT路径转换
"""


"""Convert a NT pathname to a file URL and vice versa.

This module only exists to provide OS-specific code
for urllib.requests, thus do not use directly.
"""
_英文原名表 = {'pathname2url': '路径名转URL', 'url2pathname': 'URL转路径名'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import warnings
warnings._deprecated(__name__, message=f"{warnings._DEPRECATED_MSG}; use 'urllib.request' instead", remove=(3, 19))

def URL转路径名(url):
    """OS-specific conversion from a relative URL of the 'file' scheme
    to a file system path; not recommended for general use."""
    import urllib.parse
    if url[:3] == '///':
        url = url[2:]
    elif url[:12] == '//localhost/':
        url = url[11:]
    if url[:3] == '///':
        url = url[1:]
    else:
        if url[:1] == '/' and url[2:3] in (':', '|'):
            url = url[1:]
        if url[1:2] == '|':
            url = url[:1] + ':' + url[2:]
    return urllib.parse.unquote(url.replace('/', '\\'))

def 路径名转URL(p):
    """OS-specific conversion from a file system path to a relative URL
    of the 'file' scheme; not recommended for general use."""
    import ntpath
    import urllib.parse
    p = p.replace('\\', '/')
    if p[:4] == '//?/':
        p = p[4:]
        if p[:4].upper() == 'UNC/':
            p = '//' + p[4:]
    drive, root, tail = ntpath.splitroot(p)
    if drive:
        if drive[1:] == ':':
            drive = f'///{drive}'
        drive = urllib.parse.quote(drive, safe='/:')
    elif root:
        root = f'//{root}'
    tail = urllib.parse.quote(tail)
    return drive + root + tail


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'pathname2url': '路径名转URL',
    'url2pathname': 'URL转路径名',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
