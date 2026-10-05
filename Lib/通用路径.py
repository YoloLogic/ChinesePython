# -*- coding: utf-8 -*-
"""通用路径 —— 汉语库（由 tools/汉化库.py 从 Lib/genericpath.py 机械生成，**不要手改**）。

英文库 Lib/genericpath.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 通用路径
"""


"""
Path operations common to more than one OS
Do not use directly.  The OS specific modules import the appropriate
functions from this module themselves.
"""
_英文原名表 = {'ALLOW_MISSING': '允许缺失', 'commonprefix': '公共前缀', 'exists': '存在吗', 'getatime': '取访问时间', 'getctime': '取创建时间', 'getmtime': '取修改时间', 'getsize': '取大小', 'isdevdrive': '是开发盘吗', 'isdir': '是目录吗', 'isfile': '是文件吗', 'isjunction': '是联接吗', 'islink': '是链接吗', 'lexists': '不跟随存在吗', 'samefile': '同文件吗', 'sameopenfile': '同打开文件吗', 'samestat': '同状态吗'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import os
import stat
__all__ = ['commonprefix', 'exists', 'getatime', 'getctime', 'getmtime', 'getsize', 'isdevdrive', 'isdir', 'isfile', 'isjunction', 'islink', 'lexists', 'samefile', 'sameopenfile', 'samestat', 'ALLOW_MISSING']

def 存在吗(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except (OSError, ValueError):
        return False
    return True

def 不跟随存在吗(path):
    """Test whether a path exists.  Returns True for broken symbolic links"""
    try:
        os.lstat(path)
    except (OSError, ValueError):
        return False
    return True

def 是文件吗(path):
    """Test whether a path is a regular file"""
    try:
        st = os.stat(path)
    except (OSError, ValueError):
        return False
    return stat.S_ISREG(st.st_mode)

def 是目录吗(s):
    """Return true if the pathname refers to an existing directory."""
    try:
        st = os.stat(s)
    except (OSError, ValueError):
        return False
    return stat.S_ISDIR(st.st_mode)

def 是链接吗(path):
    """Test whether a path is a symbolic link"""
    try:
        st = os.lstat(path)
    except (OSError, ValueError, AttributeError):
        return False
    return stat.S_ISLNK(st.st_mode)

def 是联接吗(path):
    """Test whether a path is a junction
    Junctions are not supported on the current platform"""
    os.fspath(path)
    return False

def 是开发盘吗(path):
    """Determines whether the specified path is on a Windows Dev Drive.
    Dev Drives are not supported on the current platform"""
    os.fspath(path)
    return False

def 取大小(filename):
    """Return the size of a file, reported by os.stat()."""
    return os.stat(filename).st_size

def 取修改时间(filename):
    """Return the last modification time of a file, reported by os.stat()."""
    return os.stat(filename).st_mtime

def 取访问时间(filename):
    """Return the last access time of a file, reported by os.stat()."""
    return os.stat(filename).st_atime

def 取创建时间(filename):
    """Return the metadata change time of a file, reported by os.stat()."""
    return os.stat(filename).st_ctime

def 公共前缀(m):
    """Given a list of pathnames, returns the longest common leading component"""
    if not m:
        return ''
    if not isinstance(m[0], (list, tuple)):
        m = tuple(map(os.fspath, m))
    s1 = min(m)
    s2 = max(m)
    for i, c in enumerate(s1):
        if c != s2[i]:
            return s1[:i]
    return s1

def 同状态吗(s1, s2):
    """Test whether two stat buffers reference the same file"""
    return s1.st_ino == s2.st_ino and s1.st_dev == s2.st_dev

def 同文件吗(f1, f2):
    """Test whether two pathnames reference the same actual file or directory

    This is determined by the device number and i-node number and
    raises an exception if an os.stat() call on either pathname fails.
    """
    s1 = os.stat(f1)
    s2 = os.stat(f2)
    return 同状态吗(s1, s2)

def 同打开文件吗(fp1, fp2):
    """Test whether two open file objects reference the same file"""
    s1 = os.fstat(fp1)
    s2 = os.fstat(fp2)
    return 同状态吗(s1, s2)

def _splitext(p, sep, altsep, extsep):
    """Split the extension from a pathname.

    Extension is everything from the last dot to the end, ignoring
    leading dots.  Returns "(root, ext)"; ext may be empty."""
    sepIndex = p.rfind(sep)
    if altsep:
        altsepIndex = p.rfind(altsep)
        sepIndex = max(sepIndex, altsepIndex)
    dotIndex = p.rfind(extsep)
    if dotIndex > sepIndex:
        filenameIndex = sepIndex + 1
        while filenameIndex < dotIndex:
            if p[filenameIndex:filenameIndex + 1] != extsep:
                return (p[:dotIndex], p[dotIndex:])
            filenameIndex += 1
    return (p, p[:0])

def _check_arg_types(funcname, *args):
    hasstr = hasbytes = False
    for s in args:
        if isinstance(s, str):
            hasstr = True
        elif isinstance(s, bytes):
            hasbytes = True
        else:
            raise TypeError(f'{funcname}() argument must be str, bytes, or os.PathLike object, not {s.__class__.__name__!r}') from None
    if hasstr and hasbytes:
        raise TypeError("Can't mix strings and bytes in path components") from None

@object.__new__
class 允许缺失:
    """Special value for use in realpath()."""

    def __repr__(self):
        return 'os.path.ALLOW_MISSING'

    def __reduce__(self):
        return self.__class__.__name__


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'ALLOW_MISSING': '允许缺失',
    'commonprefix': '公共前缀',
    'exists': '存在吗',
    'getatime': '取访问时间',
    'getctime': '取创建时间',
    'getmtime': '取修改时间',
    'getsize': '取大小',
    'isdevdrive': '是开发盘吗',
    'isdir': '是目录吗',
    'isfile': '是文件吗',
    'isjunction': '是联接吗',
    'islink': '是链接吗',
    'lexists': '不跟随存在吗',
    'samefile': '同文件吗',
    'sameopenfile': '同打开文件吗',
    'samestat': '同状态吗',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '不跟随存在吗',
    '允许缺失',
    '公共前缀',
    '取修改时间',
    '取创建时间',
    '取大小',
    '取访问时间',
    '同打开文件吗',
    '同文件吗',
    '同状态吗',
    '存在吗',
    '是开发盘吗',
    '是文件吗',
    '是目录吗',
    '是联接吗',
    '是链接吗',
])

# ---- 转发层结束 ----
