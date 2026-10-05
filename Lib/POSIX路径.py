# -*- coding: utf-8 -*-
"""POSIX路径 —— 汉语库（由 tools/汉化库.py 从 Lib/posixpath.py 机械生成，**不要手改**）。

英文库 Lib/posixpath.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py POSIX路径
"""


"""Common operations on Posix pathnames.

Instead of importing this module directly, import os and refer to
this module as os.path.  The "os.path" name is an alias for this
module on Posix systems; on other systems (e.g. Windows),
os.path provides the same operations in a manner specific to that
platform, and is an alias to another module (e.g. ntpath).

Some of this can actually be useful on non-Posix systems too, e.g.
for manipulation of the pathname component of URLs.
"""
_英文原名表 = {'abspath': '绝对路径', 'altsep': '备用分隔符', 'basename': '取基本名', 'commonpath': '公共路径', 'curdir': '当前目录', 'defpath': '默认搜索路径', 'devnull': '空设备', 'dirname': '取目录名', 'expanduser': '展开用户目录', 'expandvars': '展开变量', 'extsep': '扩展名分隔符', 'isabs': '是绝对路径吗', 'ismount': '是挂载点吗', 'join': '拼接', 'normcase': '规范化大小写', 'pardir': '父目录', 'pathsep': '路径分隔符', 'realpath': '真实路径', 'relpath': '相对路径', 'sep': '分隔符', 'split': '切分', 'splitdrive': '拆分驱动器', 'splitext': '切分扩展名', 'supports_unicode_filenames': '支持统一码文件名'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
当前目录 = '.'
父目录 = '..'
扩展名分隔符 = '.'
分隔符 = '/'
路径分隔符 = ':'
默认搜索路径 = '/bin:/usr/bin'
备用分隔符 = None
空设备 = '/dev/null'
import errno
import os
import sys
import stat
import genericpath
from genericpath import *
__all__ = ['normcase', 'isabs', 'join', 'splitdrive', 'splitroot', 'split', 'splitext', 'basename', 'dirname', 'commonprefix', 'getsize', 'getmtime', 'getatime', 'getctime', 'islink', 'exists', 'lexists', 'isdir', 'isfile', 'ismount', 'expanduser', 'expandvars', 'normpath', 'abspath', 'samefile', 'sameopenfile', 'samestat', 'curdir', 'pardir', 'sep', 'pathsep', 'defpath', 'altsep', 'extsep', 'devnull', 'realpath', 'supports_unicode_filenames', 'relpath', 'commonpath', 'isjunction', 'isdevdrive', 'ALLOW_MISSING']

def _get_sep(path):
    if isinstance(path, bytes):
        return b'/'
    else:
        return '/'

def 规范化大小写(s):
    """Normalize case of pathname.  Has no effect under Posix"""
    return os.fspath(s)

def 是绝对路径吗(s):
    """Test whether a path is absolute"""
    s = os.fspath(s)
    分隔符 = _get_sep(s)
    return s.startswith(分隔符)

def 拼接(a, *p):
    """Join two or more pathname components, inserting '/' as needed.
    If any component is an absolute path, all previous path components
    will be discarded.  An empty last part will result in a path that
    ends with a separator."""
    a = os.fspath(a)
    分隔符 = _get_sep(a)
    path = a
    try:
        for b in p:
            b = os.fspath(b)
            if b.startswith(分隔符) or not path:
                path = b
            elif path.endswith(分隔符):
                path += b
            else:
                path += 分隔符 + b
    except (TypeError, AttributeError, BytesWarning):
        genericpath._check_arg_types('join', a, *p)
        raise
    return path

def 切分(p):
    """Split a pathname.  Returns tuple "(head, tail)" where "tail" is
    everything after the final slash.  Either part may be empty."""
    p = os.fspath(p)
    分隔符 = _get_sep(p)
    i = p.rfind(分隔符) + 1
    head, tail = (p[:i], p[i:])
    if head and head != 分隔符 * len(head):
        head = head.rstrip(分隔符)
    return (head, tail)

def 切分扩展名(p):
    p = os.fspath(p)
    if isinstance(p, bytes):
        分隔符 = b'/'
        扩展名分隔符 = b'.'
    else:
        分隔符 = '/'
        扩展名分隔符 = '.'
    return genericpath._splitext(p, 分隔符, None, 扩展名分隔符)
切分扩展名.__doc__ = genericpath._splitext.__doc__

def 拆分驱动器(p):
    """Split a pathname into drive and path. On Posix, drive is always
    empty."""
    p = os.fspath(p)
    return (p[:0], p)
try:
    from posix import _path_splitroot_ex as splitroot
except ImportError:

    def splitroot(p):
        """Split a pathname into drive, root and tail.

        The tail contains anything after the root."""
        p = os.fspath(p)
        if isinstance(p, bytes):
            分隔符 = b'/'
            empty = b''
        else:
            分隔符 = '/'
            empty = ''
        if p[:1] != 分隔符:
            return (empty, empty, p)
        elif p[1:2] != 分隔符 or p[2:3] == 分隔符:
            return (empty, 分隔符, p[1:])
        else:
            return (empty, p[:2], p[2:])

def 取基本名(p):
    """Returns the final component of a pathname"""
    p = os.fspath(p)
    分隔符 = _get_sep(p)
    i = p.rfind(分隔符) + 1
    return p[i:]

def 取目录名(p):
    """Returns the directory component of a pathname"""
    p = os.fspath(p)
    分隔符 = _get_sep(p)
    i = p.rfind(分隔符) + 1
    head = p[:i]
    if head and head != 分隔符 * len(head):
        head = head.rstrip(分隔符)
    return head

def 是挂载点吗(path):
    """Test whether a path is a mount point"""
    try:
        s1 = os.lstat(path)
    except (OSError, ValueError):
        return False
    else:
        if stat.S_ISLNK(s1.st_mode):
            return False
    path = os.fspath(path)
    if isinstance(path, bytes):
        parent = 拼接(path, b'..')
    else:
        parent = 拼接(path, '..')
    try:
        s2 = os.lstat(parent)
    except OSError:
        parent = 真实路径(parent)
        try:
            s2 = os.lstat(parent)
        except OSError:
            return False
    return s1.st_dev != s2.st_dev or s1.st_ino == s2.st_ino

def 展开用户目录(path):
    """Expand ~ and ~user constructions.  If user or $HOME is unknown,
    do nothing."""
    path = os.fspath(path)
    if isinstance(path, bytes):
        tilde = b'~'
    else:
        tilde = '~'
    if not path.startswith(tilde):
        return path
    分隔符 = _get_sep(path)
    i = path.find(分隔符, 1)
    if i < 0:
        i = len(path)
    if i == 1:
        if 'HOME' not in os.environ:
            try:
                import pwd
            except ImportError:
                return path
            try:
                userhome = pwd.getpwuid(os.getuid()).pw_dir
            except KeyError:
                return path
        else:
            userhome = os.environ['HOME']
    else:
        try:
            import pwd
        except ImportError:
            return path
        name = path[1:i]
        if isinstance(name, bytes):
            name = os.fsdecode(name)
        try:
            pwent = pwd.getpwnam(name)
        except KeyError:
            return path
        userhome = pwent.pw_dir
    if userhome is None and sys.platform == 'vxworks':
        return path
    if isinstance(path, bytes):
        userhome = os.fsencode(userhome)
    userhome = userhome.rstrip(分隔符)
    return userhome + path[i:] or 分隔符
_varpattern = '\\$(\\w+|\\{[^}]*\\}?)'
_varsub = None
_varsubb = None

def 展开变量(path):
    """Expand shell variables of form $var and ${var}.  Unknown variables
    are left unchanged."""
    path = os.fspath(path)
    global _varsub, _varsubb
    if isinstance(path, bytes):
        if b'$' not in path:
            return path
        if not _varsubb:
            import re
            _varsubb = re.compile(_varpattern.encode(), re.ASCII).sub
        sub = _varsubb
        start = b'{'
        end = b'}'
        environ = getattr(os, 'environb', None)
    else:
        if '$' not in path:
            return path
        if not _varsub:
            import re
            _varsub = re.compile(_varpattern, re.ASCII).sub
        sub = _varsub
        start = '{'
        end = '}'
        environ = os.environ

    def repl(m):
        name = m[1]
        if name.startswith(start):
            if not name.endswith(end):
                return m[0]
            name = name[1:-1]
        try:
            if environ is None:
                value = os.fsencode(os.environ[os.fsdecode(name)])
            else:
                value = environ[name]
        except KeyError:
            return m[0]
        else:
            return value
    return sub(repl, path)
try:
    from posix import _path_normpath as normpath
except ImportError:

    def normpath(path):
        """Normalize path, eliminating double slashes, etc."""
        path = os.fspath(path)
        if isinstance(path, bytes):
            分隔符 = b'/'
            dot = b'.'
            dotdot = b'..'
        else:
            分隔符 = '/'
            dot = '.'
            dotdot = '..'
        if not path:
            return dot
        _, initial_slashes, path = splitroot(path)
        comps = path.split(分隔符)
        new_comps = []
        for comp in comps:
            if not comp or comp == dot:
                continue
            if comp != dotdot or (not initial_slashes and (not new_comps)) or (new_comps and new_comps[-1] == dotdot):
                new_comps.append(comp)
            elif new_comps:
                new_comps.pop()
        comps = new_comps
        path = initial_slashes + 分隔符.join(comps)
        return path or dot

def 绝对路径(path):
    """Return an absolute path."""
    path = os.fspath(path)
    if isinstance(path, bytes):
        if not path.startswith(b'/'):
            path = 拼接(os.getcwdb(), path)
    elif not path.startswith('/'):
        path = 拼接(os.getcwd(), path)
    return normpath(path)

def 真实路径(filename, *, strict=False):
    """Return the canonical path of the specified filename, eliminating any
symbolic links encountered in the path."""
    filename = os.fspath(filename)
    if isinstance(filename, bytes):
        分隔符 = b'/'
        当前目录 = b'.'
        父目录 = b'..'
        getcwd = os.getcwdb
    else:
        分隔符 = '/'
        当前目录 = '.'
        父目录 = '..'
        getcwd = os.getcwd
    if strict is ALLOW_MISSING:
        ignored_error = FileNotFoundError
        strict = True
    elif strict:
        ignored_error = ()
    else:
        ignored_error = OSError
    lstat = os.lstat
    readlink = os.readlink
    maxlinks = None
    rest = filename.split(分隔符)[::-1]
    part_count = len(rest)
    path = 分隔符 if filename.startswith(分隔符) else getcwd()
    seen = {}
    link_count = 0
    while part_count:
        name = rest.pop()
        if name is None:
            seen[rest.pop()] = path
            continue
        part_count -= 1
        if not name or name == 当前目录:
            continue
        if name == 父目录:
            path = path[:path.rindex(分隔符)] or 分隔符
            continue
        if path == 分隔符:
            newpath = path + name
        else:
            newpath = path + 分隔符 + name
        try:
            st_mode = lstat(newpath).st_mode
            if not stat.S_ISLNK(st_mode):
                if strict and part_count and (not stat.S_ISDIR(st_mode)):
                    raise OSError(errno.ENOTDIR, os.strerror(errno.ENOTDIR), newpath)
                path = newpath
                continue
            elif maxlinks is not None:
                link_count += 1
                if link_count > maxlinks:
                    if strict:
                        raise OSError(errno.ELOOP, os.strerror(errno.ELOOP), newpath)
                    path = newpath
                    continue
            elif newpath in seen:
                path = seen[newpath]
                if path is not None:
                    continue
                if strict:
                    raise OSError(errno.ELOOP, os.strerror(errno.ELOOP), newpath)
                path = newpath
                continue
            target = readlink(newpath)
        except ignored_error:
            pass
        else:
            if target.startswith(分隔符):
                path = 分隔符
            if maxlinks is None:
                seen[newpath] = None
                rest.append(newpath)
                rest.append(None)
            target_parts = target.split(分隔符)[::-1]
            rest.extend(target_parts)
            part_count += len(target_parts)
            continue
        path = newpath
    return path
支持统一码文件名 = sys.platform == 'darwin'

def 相对路径(path, start=None):
    """Return a relative version of a path"""
    path = os.fspath(path)
    if not path:
        raise ValueError('no path specified')
    if isinstance(path, bytes):
        当前目录 = b'.'
        分隔符 = b'/'
        父目录 = b'..'
    else:
        当前目录 = '.'
        分隔符 = '/'
        父目录 = '..'
    if start is None:
        start = 当前目录
    else:
        start = os.fspath(start)
    try:
        start_tail = 绝对路径(start).lstrip(分隔符)
        path_tail = 绝对路径(path).lstrip(分隔符)
        start_list = start_tail.split(分隔符) if start_tail else []
        path_list = path_tail.split(分隔符) if path_tail else []
        i = len(commonprefix([start_list, path_list]))
        rel_list = [父目录] * (len(start_list) - i) + path_list[i:]
        if not rel_list:
            return 当前目录
        return 分隔符.join(rel_list)
    except (TypeError, AttributeError, BytesWarning, DeprecationWarning):
        genericpath._check_arg_types('relpath', path, start)
        raise

def 公共路径(paths):
    """Given a sequence of path names, returns the longest common sub-path."""
    paths = tuple(map(os.fspath, paths))
    if not paths:
        raise ValueError('commonpath() arg is an empty sequence')
    if isinstance(paths[0], bytes):
        分隔符 = b'/'
        当前目录 = b'.'
    else:
        分隔符 = '/'
        当前目录 = '.'
    try:
        split_paths = [path.split(分隔符) for path in paths]
        try:
            是绝对路径吗, = {p.startswith(分隔符) for p in paths}
        except ValueError:
            raise ValueError("Can't mix absolute and relative paths") from None
        split_paths = [[c for c in s if c and c != 当前目录] for s in split_paths]
        s1 = min(split_paths)
        s2 = max(split_paths)
        common = s1
        for i, c in enumerate(s1):
            if c != s2[i]:
                common = s1[:i]
                break
        prefix = 分隔符 if 是绝对路径吗 else 分隔符[:0]
        return prefix + 分隔符.join(common)
    except (TypeError, AttributeError):
        genericpath._check_arg_types('commonpath', *paths)
        raise


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 本模块别名：词表里有、但规则不让改定义的名字（内置名最典型，比如 `open`）
_本模块别名 = {
    '拆分根': 'splitroot',
    '规范化路径': 'normpath',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import posixpath as _英文库
允许缺失 = _英文库.ALLOW_MISSING
公共前缀 = _英文库.commonprefix
存在吗 = _英文库.exists
取访问时间 = _英文库.getatime
取创建时间 = _英文库.getctime
取修改时间 = _英文库.getmtime
取大小 = _英文库.getsize
是开发盘吗 = _英文库.isdevdrive
是目录吗 = _英文库.isdir
是文件吗 = _英文库.isfile
是联接吗 = _英文库.isjunction
是链接吗 = _英文库.islink
不跟随存在吗 = _英文库.lexists
同文件吗 = _英文库.samefile
同打开文件吗 = _英文库.sameopenfile
同状态吗 = _英文库.samestat
_模块别名 = {
    'abspath': '绝对路径',
    'altsep': '备用分隔符',
    'basename': '取基本名',
    'commonpath': '公共路径',
    'curdir': '当前目录',
    'defpath': '默认搜索路径',
    'devnull': '空设备',
    'dirname': '取目录名',
    'expanduser': '展开用户目录',
    'expandvars': '展开变量',
    'extsep': '扩展名分隔符',
    'isabs': '是绝对路径吗',
    'ismount': '是挂载点吗',
    'join': '拼接',
    'normcase': '规范化大小写',
    'pardir': '父目录',
    'pathsep': '路径分隔符',
    'realpath': '真实路径',
    'relpath': '相对路径',
    'sep': '分隔符',
    'split': '切分',
    'splitdrive': '拆分驱动器',
    'splitext': '切分扩展名',
    'supports_unicode_filenames': '支持统一码文件名',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '公共路径',
    '分隔符',
    '切分',
    '切分扩展名',
    '取基本名',
    '取目录名',
    '备用分隔符',
    '展开变量',
    '展开用户目录',
    '当前目录',
    '扩展名分隔符',
    '拆分根',
    '拆分驱动器',
    '拼接',
    '支持统一码文件名',
    '是挂载点吗',
    '是绝对路径吗',
    '父目录',
    '相对路径',
    '真实路径',
    '空设备',
    '绝对路径',
    '规范化大小写',
    '规范化路径',
    '路径分隔符',
    '默认搜索路径',
]

# ---- 转发层结束 ----
