# -*- coding: utf-8 -*-
"""路径库.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/pathlib/__init__.py 机械生成，**不要手改**）。

英文库 Lib/pathlib.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py pathlib
"""


"""Object-oriented filesystem paths.

This module provides classes to represent abstract paths and concrete
paths with operations that have semantics appropriate for different
operating systems.
"""
_英文原名表 = {'Path': '路径', 'PosixPath': 'POSIX路径', 'PurePath': '纯路径', 'PurePosixPath': '纯POSIX路径', 'PureWindowsPath': '纯Windows路径', 'UnsupportedOperation': '不支持的操作', 'WindowsPath': 'Windows路径'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import io
import ntpath
import operator
import os
import posixpath
import sys
from errno import *
from glob import _StringGlobber, _no_recurse_symlinks
from itertools import chain
from stat import S_ISDIR, S_ISREG, S_ISSOCK, S_ISBLK, S_ISCHR, S_ISFIFO
from _collections_abc import Sequence
try:
    import pwd
except ImportError:
    pwd = None
try:
    import grp
except ImportError:
    grp = None
from 路径库._os import PathInfo, DirEntryInfo, ensure_different_files, ensure_distinct_paths, copyfile2, copyfileobj, magic_open, copy_info
__all__ = ['UnsupportedOperation', 'PurePath', 'PurePosixPath', 'PureWindowsPath', 'Path', 'PosixPath', 'WindowsPath']

class 不支持的操作(NotImplementedError):
    """An exception that is raised when an unsupported operation is attempted.
    """
    pass
import pathlib as _英文身份源
不支持的操作 = _英文身份源.UnsupportedOperation

class _PathParents(Sequence):
    """This object provides sequence-like access to the logical ancestors
    of a path.  Don't try to construct it yourself."""
    __slots__ = ('_path', '_drv', '_root', '_tail')

    def __init__(self, path):
        self._path = path
        self._drv = path.drive
        self._root = path.root
        self._tail = path._tail

    def __len__(self):
        return len(self._tail)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return tuple((self[i] for i in range(*idx.indices(len(self)))))
        if idx >= len(self) or idx < -len(self):
            raise IndexError(idx)
        if idx < 0:
            idx += len(self)
        return self._path._from_parsed_parts(self._drv, self._root, self._tail[:-idx - 1])

    def __repr__(self):
        return '<{}.parents>'.format(type(self._path).__name__)

class 纯路径:
    """Base class for manipulating paths without I/O.

    PurePath represents a filesystem path and offers operations which
    don't imply any actual filesystem I/O.  Depending on your system,
    instantiating a PurePath will return either a PurePosixPath or a
    PureWindowsPath object.  You can also instantiate either of these classes
    directly, regardless of your system.
    """
    __slots__ = ('_raw_paths', '_drv', '_root', '_tail_cached', '_str', '_str_normcase_cached', '_parts_normcase_cached', '_hash')
    parser = os.path

    def __new__(cls, *args, **kwargs):
        """Construct a PurePath from one or several strings and or existing
        PurePath objects.  The strings and path objects are combined so as
        to yield a canonicalized path, which is incorporated into the
        new PurePath object.
        """
        if cls is 纯路径:
            cls = 纯Windows路径 if os.name == 'nt' else 纯POSIX路径
        return object.__new__(cls)

    def __init__(self, *args):
        paths = []
        for arg in args:
            if isinstance(arg, 纯路径):
                if arg.parser is not self.parser:
                    paths.append(arg.as_posix())
                else:
                    paths.extend(arg._raw_paths)
            else:
                try:
                    path = os.fspath(arg)
                except TypeError:
                    path = arg
                if not isinstance(path, str):
                    raise TypeError(f'argument should be a str or an os.PathLike object where __fspath__ returns a str, not {type(path).__name__!r}')
                paths.append(path)
        self._raw_paths = paths

    def with_segments(self, *pathsegments):
        """Construct a new path object from any number of path-like objects.
        Subclasses may override this method to customize how new path objects
        are created from methods like `iterdir()`.
        """
        return type(self)(*pathsegments)

    def 拼路径(self, *pathsegments):
        """Combine this path with one or several arguments, and return a
        new path representing either a subpath (if all arguments are relative
        paths) or a totally different path (if one of the arguments is
        anchored).
        """
        return self.with_segments(self, *pathsegments)

    def __truediv__(self, key):
        try:
            return self.with_segments(self, key)
        except TypeError:
            return NotImplemented

    def __rtruediv__(self, key):
        try:
            return self.with_segments(key, self)
        except TypeError:
            return NotImplemented

    def __reduce__(self):
        return (self.__class__, tuple(self._raw_paths))

    def __repr__(self):
        return '{}({!r})'.format(self.__class__.__name__, self.转POSIX())

    def __fspath__(self):
        return str(self)

    def __bytes__(self):
        """Return the bytes representation of the path.  This is only
        recommended to use under Unix."""
        return os.fsencode(self)

    @property
    def _str_normcase(self):
        try:
            return self._str_normcase_cached
        except AttributeError:
            if self.parser is posixpath:
                self._str_normcase_cached = str(self)
            else:
                self._str_normcase_cached = str(self).lower()
            return self._str_normcase_cached

    def __hash__(self):
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(self._str_normcase)
            return self._hash

    def __eq__(self, other):
        if not isinstance(other, 纯路径):
            return NotImplemented
        return self._str_normcase == other._str_normcase and self.parser is other.parser

    @property
    def _parts_normcase(self):
        try:
            return self._parts_normcase_cached
        except AttributeError:
            self._parts_normcase_cached = self._str_normcase.split(self.parser.sep)
            return self._parts_normcase_cached

    def __lt__(self, other):
        if not isinstance(other, 纯路径) or self.parser is not other.parser:
            return NotImplemented
        return self._parts_normcase < other._parts_normcase

    def __le__(self, other):
        if not isinstance(other, 纯路径) or self.parser is not other.parser:
            return NotImplemented
        return self._parts_normcase <= other._parts_normcase

    def __gt__(self, other):
        if not isinstance(other, 纯路径) or self.parser is not other.parser:
            return NotImplemented
        return self._parts_normcase > other._parts_normcase

    def __ge__(self, other):
        if not isinstance(other, 纯路径) or self.parser is not other.parser:
            return NotImplemented
        return self._parts_normcase >= other._parts_normcase

    def __str__(self):
        """Return the string representation of the path, suitable for
        passing to system calls."""
        try:
            return self._str
        except AttributeError:
            self._str = self._format_parsed_parts(self.盘符, self.根, self._tail) or '.'
            return self._str

    @classmethod
    def _format_parsed_parts(cls, drv, root, tail):
        if drv or root:
            return drv + root + cls.parser.sep.join(tail)
        elif tail and cls.parser.splitdrive(tail[0])[0]:
            tail = ['.'] + tail
        return cls.parser.sep.join(tail)

    def _from_parsed_parts(self, drv, root, tail):
        path = self._from_parsed_string(self._format_parsed_parts(drv, root, tail))
        path._drv = drv
        path._root = root
        path._tail_cached = tail
        return path

    def _from_parsed_string(self, path_str):
        path = self.with_segments(path_str)
        path._str = path_str or '.'
        return path

    @classmethod
    def _parse_path(cls, path):
        if not path:
            return ('', '', [])
        sep = cls.parser.sep
        altsep = cls.parser.altsep
        if altsep:
            path = path.replace(altsep, sep)
        drv, 根, rel = cls.parser.splitroot(path)
        if not 根 and drv.startswith(sep) and (not drv.endswith(sep)):
            drv_parts = drv.split(sep)
            if len(drv_parts) == 4 and drv_parts[2] not in '?.':
                根 = sep
            elif len(drv_parts) == 6:
                根 = sep
        return (drv, 根, [x for x in rel.split(sep) if x and x != '.'])

    @classmethod
    def _parse_pattern(cls, pattern):
        """Parse a glob pattern to a list of parts. This is much like
        _parse_path, except:

        - Rather than normalizing and returning the drive and root, we raise
          NotImplementedError if either are present.
        - If the path has no real parts, we raise ValueError.
        - If the path ends in a slash, then a final empty part is added.
        """
        drv, 根, rel = cls.parser.splitroot(pattern)
        if 根 or drv:
            raise NotImplementedError('Non-relative patterns are unsupported')
        sep = cls.parser.sep
        altsep = cls.parser.altsep
        if altsep:
            rel = rel.replace(altsep, sep)
        分片 = [x for x in rel.split(sep) if x and x != '.']
        if not 分片:
            raise ValueError(f'Unacceptable pattern: {str(pattern)!r}')
        elif rel.endswith(sep):
            分片.append('')
        return 分片

    def 转POSIX(self):
        """Return the string representation of the path with forward (/)
        slashes."""
        return str(self).replace(self.parser.sep, '/')

    @property
    def _raw_path(self):
        paths = self._raw_paths
        if len(paths) == 1:
            return paths[0]
        elif paths:
            return self.parser.join(*paths)
        else:
            return ''

    @property
    def 盘符(self):
        """The drive prefix (letter or UNC path), if any."""
        try:
            return self._drv
        except AttributeError:
            self._drv, self._root, self._tail_cached = self._parse_path(self._raw_path)
            return self._drv

    @property
    def 根(self):
        """The root of the path, if any."""
        try:
            return self._root
        except AttributeError:
            self._drv, self._root, self._tail_cached = self._parse_path(self._raw_path)
            return self._root

    @property
    def _tail(self):
        try:
            return self._tail_cached
        except AttributeError:
            self._drv, self._root, self._tail_cached = self._parse_path(self._raw_path)
            return self._tail_cached

    @property
    def 锚点(self):
        """The concatenation of the drive and root, or ''."""
        return self.盘符 + self.根

    @property
    def 分片(self):
        """An object providing sequence-like access to the
        components in the filesystem path."""
        if self.盘符 or self.根:
            return (self.盘符 + self.根,) + tuple(self._tail)
        else:
            return tuple(self._tail)

    @property
    def 父目录(self):
        """The logical parent of the path."""
        drv = self.盘符
        根 = self.根
        tail = self._tail
        if not tail:
            return self
        return self._from_parsed_parts(drv, 根, tail[:-1])

    @property
    def 各级父目录(self):
        """A sequence of this path's logical parents."""
        return _PathParents(self)

    @property
    def 名字(self):
        """The final path component, if any."""
        tail = self._tail
        if not tail:
            return ''
        return tail[-1]

    def 换名字(self, name):
        """Return a new path with the file name changed."""
        p = self.parser
        if not name or p.sep in name or (p.altsep and p.altsep in name) or (name == '.'):
            raise ValueError(f'Invalid name {name!r}')
        tail = self._tail.copy()
        if not tail:
            raise ValueError(f'{self!r} has an empty name')
        tail[-1] = name
        return self._from_parsed_parts(self.盘符, self.根, tail)

    def 换主干名(self, stem):
        """Return a new path with the stem changed."""
        后缀 = self.后缀
        if not 后缀:
            return self.换名字(stem)
        elif not stem:
            raise ValueError(f'{self!r} has a non-empty suffix')
        else:
            return self.换名字(stem + 后缀)

    def 换后缀(self, suffix):
        """Return a new path with the file suffix changed.  If the path
        has no suffix, add given suffix.  If the given suffix is an empty
        string, remove the suffix from the path.
        """
        主干名 = self.主干名
        if not 主干名:
            raise ValueError(f'{self!r} has an empty name')
        elif suffix and (not suffix.startswith('.')):
            raise ValueError(f'Invalid suffix {suffix!r}')
        else:
            return self.换名字(主干名 + suffix)

    @property
    def 主干名(self):
        """The final path component, minus its last suffix."""
        名字 = self.名字
        i = 名字.rfind('.')
        if i != -1:
            主干名 = 名字[:i]
            if 主干名.lstrip('.'):
                return 主干名
        return 名字

    @property
    def 后缀(self):
        """
        The final component's last suffix, if any.

        This includes the leading period. For example: '.txt'
        """
        名字 = self.名字.lstrip('.')
        i = 名字.rfind('.')
        if i != -1:
            return 名字[i:]
        return ''

    @property
    def 后缀们(self):
        """
        A list of the final component's suffixes, if any.

        These include the leading periods. For example: ['.tar', '.gz']
        """
        return ['.' + ext for ext in self.名字.lstrip('.').split('.')[1:]]

    def 相对路径(self, other, *, walk_up=False):
        """Return the relative path to another path identified by the passed
        arguments.  If the operation is not possible (because this is not
        related to the other path), raise ValueError.

        The *walk_up* parameter controls whether `..` may be used to resolve
        the path.
        """
        if not hasattr(other, 'with_segments'):
            other = self.with_segments(other)
        for step, path in enumerate(chain([other], other.parents)):
            if path == self or path in self.各级父目录:
                break
            elif not walk_up:
                raise ValueError(f'{str(self)!r} is not in the subpath of {str(other)!r}')
            elif path.name == '..':
                raise ValueError(f"'..' segment in {str(other)!r} cannot be walked")
        else:
            raise ValueError(f'{str(self)!r} and {str(other)!r} have different anchors')
        分片 = ['..'] * step + self._tail[len(path._tail):]
        return self._from_parsed_parts('', '', 分片)

    def 相对于吗(self, other):
        """Return True if the path is relative to another path or False.
        """
        if not hasattr(other, 'with_segments'):
            other = self.with_segments(other)
        return other == self or other in self.各级父目录

    def 是绝对路径吗(self):
        """True if the path is absolute (has both a root and, if applicable,
        a drive)."""
        if self.parser is posixpath:
            for path in self._raw_paths:
                if path.startswith('/'):
                    return True
            return False
        return self.parser.isabs(self)

    def 是保留名吗(self):
        """Return True if the path contains one of the special names reserved
        by the system, if any."""
        import warnings
        msg = 'pathlib.PurePath.is_reserved() is deprecated and scheduled for removal in Python 3.15. Use os.path.isreserved() to detect reserved paths on Windows.'
        warnings._deprecated('pathlib.PurePath.is_reserved', msg, remove=(3, 15))
        if self.parser is ntpath:
            return self.parser.isreserved(self)
        return False

    def 转URI(self):
        """Return the path as a URI."""
        import warnings
        msg = 'pathlib.PurePath.as_uri() is deprecated and scheduled for removal in Python 3.19. Use pathlib.Path.as_uri().'
        warnings._deprecated('pathlib.PurePath.as_uri', msg, remove=(3, 19))
        if not self.是绝对路径吗():
            raise ValueError("relative path can't be expressed as a file URI")
        盘符 = self.盘符
        if len(盘符) == 2 and 盘符[1] == ':':
            prefix = 'file:///' + 盘符
            path = self.转POSIX()[2:]
        elif 盘符:
            prefix = 'file:'
            path = self.转POSIX()
        else:
            prefix = 'file://'
            path = str(self)
        from urllib.parse import quote_from_bytes
        return prefix + quote_from_bytes(os.fsencode(path))

    def 完全匹配(self, pattern, *, case_sensitive=None):
        """
        Return True if this path matches the given glob-style pattern. The
        pattern is matched against the entire path.
        """
        if not hasattr(pattern, 'with_segments'):
            pattern = self.with_segments(pattern)
        if case_sensitive is None:
            case_sensitive = self.parser is posixpath
        path = str(self) if self.分片 else ''
        pattern = str(pattern) if pattern.parts else ''
        globber = _StringGlobber(self.parser.sep, case_sensitive, recursive=True)
        return globber.compile(pattern)(path) is not None

    def 匹配(self, path_pattern, *, case_sensitive=None):
        """
        Return True if this path matches the given pattern. If the pattern is
        relative, matching is done from the right; otherwise, the entire path
        is matched. The recursive wildcard '**' is *not* supported by this
        method.
        """
        if not hasattr(path_pattern, 'with_segments'):
            path_pattern = self.with_segments(path_pattern)
        if case_sensitive is None:
            case_sensitive = self.parser is posixpath
        path_parts = self.分片[::-1]
        pattern_parts = path_pattern.parts[::-1]
        if not pattern_parts:
            raise ValueError('empty pattern')
        if len(path_parts) < len(pattern_parts):
            return False
        if len(path_parts) > len(pattern_parts) and path_pattern.anchor:
            return False
        globber = _StringGlobber(self.parser.sep, case_sensitive)
        for path_part, pattern_part in zip(path_parts, pattern_parts):
            匹配 = globber.compile(pattern_part)
            if 匹配(path_part) is None:
                return False
        return True
_装类转发(纯路径, {'anchor': '锚点', 'as_posix': '转POSIX', 'as_uri': '转URI', 'drive': '盘符', 'full_match': '完全匹配', 'is_absolute': '是绝对路径吗', 'is_relative_to': '相对于吗', 'is_reserved': '是保留名吗', 'joinpath': '拼路径', 'match': '匹配', 'name': '名字', 'parent': '父目录', 'parents': '各级父目录', 'parts': '分片', 'relative_to': '相对路径', 'root': '根', 'stem': '主干名', 'suffix': '后缀', 'suffixes': '后缀们', 'with_name': '换名字', 'with_stem': '换主干名', 'with_suffix': '换后缀'}, {'anchor': '锚点', 'as_posix': '转POSIX', 'as_uri': '转URI', 'drive': '盘符', 'full_match': '完全匹配', 'is_absolute': '是绝对路径吗', 'is_relative_to': '相对于吗', 'is_reserved': '是保留名吗', 'joinpath': '拼路径', 'match': '匹配', 'name': '名字', 'parent': '父目录', 'parents': '各级父目录', 'parts': '分片', 'relative_to': '相对路径', 'root': '根', 'stem': '主干名', 'suffix': '后缀', 'suffixes': '后缀们', 'with_name': '换名字', 'with_stem': '换主干名', 'with_suffix': '换后缀'})
os.PathLike.register(纯路径)

class 纯POSIX路径(纯路径):
    """PurePath subclass for non-Windows systems.

    On a POSIX system, instantiating a PurePath should return this object.
    However, you can also instantiate it directly on any system.
    """
    parser = posixpath
    __slots__ = ()

class 纯Windows路径(纯路径):
    """PurePath subclass for Windows systems.

    On a Windows system, instantiating a PurePath should return this object.
    However, you can also instantiate it directly on any system.
    """
    parser = ntpath
    __slots__ = ()

class 路径(纯路径):
    """PurePath subclass that can make system calls.

    Path represents a filesystem path but unlike PurePath, also offers
    methods to do system calls on path objects. Depending on your system,
    instantiating a Path will return either a PosixPath or a WindowsPath
    object. You can also instantiate a PosixPath or WindowsPath directly,
    but cannot instantiate a WindowsPath on a POSIX system or vice versa.
    """
    __slots__ = ('_info',)

    def __new__(cls, *args, **kwargs):
        if cls is 路径:
            cls = Windows路径 if os.name == 'nt' else POSIX路径
        return object.__new__(cls)

    @property
    def info(self):
        """
        A PathInfo object that exposes the file type and other file attributes
        of this path.
        """
        try:
            return self._info
        except AttributeError:
            self._info = PathInfo(self)
            return self._info

    def 取状态(self, *, follow_symlinks=True):
        """
        Return the result of the stat() system call on this path, like
        os.stat() does.
        """
        return os.stat(self, follow_symlinks=follow_symlinks)

    def 取软链状态(self):
        """
        Like stat(), except if the path points to a symlink, the symlink's
        status information is returned, rather than its target's.
        """
        return os.lstat(self)

    def 存在吗(self, *, follow_symlinks=True):
        """
        Whether this path exists.

        This method normally follows symlinks; to check whether a symlink exists,
        add the argument follow_symlinks=False.
        """
        if follow_symlinks:
            return os.path.exists(self)
        return os.path.lexists(self)

    def 是目录吗(self, *, follow_symlinks=True):
        """
        Whether this path is a directory.
        """
        if follow_symlinks:
            return os.path.isdir(self)
        try:
            return S_ISDIR(self.取状态(follow_symlinks=follow_symlinks).st_mode)
        except (OSError, ValueError):
            return False

    def 是文件吗(self, *, follow_symlinks=True):
        """
        Whether this path is a regular file (also True for symlinks pointing
        to regular files).
        """
        if follow_symlinks:
            return os.path.isfile(self)
        try:
            return S_ISREG(self.取状态(follow_symlinks=follow_symlinks).st_mode)
        except (OSError, ValueError):
            return False

    def 是挂载点吗(self):
        """
        Check if this path is a mount point
        """
        return os.path.ismount(self)

    def 是软链吗(self):
        """
        Whether this path is a symbolic link.
        """
        return os.path.islink(self)

    def 是联接点吗(self):
        """
        Whether this path is a junction.
        """
        return os.path.isjunction(self)

    def 是块设备吗(self):
        """
        Whether this path is a block device.
        """
        try:
            return S_ISBLK(self.取状态().st_mode)
        except (OSError, ValueError):
            return False

    def 是字符设备吗(self):
        """
        Whether this path is a character device.
        """
        try:
            return S_ISCHR(self.取状态().st_mode)
        except (OSError, ValueError):
            return False

    def 是FIFO吗(self):
        """
        Whether this path is a FIFO.
        """
        try:
            return S_ISFIFO(self.取状态().st_mode)
        except (OSError, ValueError):
            return False

    def 是套接字吗(self):
        """
        Whether this path is a socket.
        """
        try:
            return S_ISSOCK(self.取状态().st_mode)
        except (OSError, ValueError):
            return False

    def 同一文件吗(self, other_path):
        """Return whether other_path is the same or not as this file
        (as returned by os.path.samefile()).
        """
        st = self.取状态()
        try:
            other_st = other_path.stat()
        except AttributeError:
            other_st = self.with_segments(other_path).stat()
        return st.st_ino == other_st.st_ino and st.st_dev == other_st.st_dev

    def open(self, mode='r', buffering=-1, encoding=None, errors=None, newline=None):
        """
        Open the file pointed to by this path and return a file object, as
        the built-in open() function does.
        """
        if 'b' not in mode:
            encoding = io.text_encoding(encoding)
        return io.open(self, mode, buffering, encoding, errors, newline)

    def 读字节(self):
        """
        Open the file in bytes mode, read it, and close the file.
        """
        with self.open(mode='rb', buffering=0) as f:
            return f.read()

    def 读文本(self, encoding=None, errors=None, newline=None):
        """
        Open the file in text mode, read it, and close the file.
        """
        encoding = io.text_encoding(encoding)
        with self.open(mode='r', encoding=encoding, errors=errors, newline=newline) as f:
            return f.read()

    def 写字节(self, data):
        """
        Open the file in bytes mode, write to it, and close the file.
        """
        view = memoryview(data)
        with self.open(mode='wb') as f:
            return f.write(view)

    def 写文本(self, data, encoding=None, errors=None, newline=None):
        """
        Open the file in text mode, write to it, and close the file.
        """
        encoding = io.text_encoding(encoding)
        if not isinstance(data, str):
            raise TypeError('data must be str, not %s' % data.__class__.__name__)
        with self.open(mode='w', encoding=encoding, errors=errors, newline=newline) as f:
            return f.write(data)
    _remove_leading_dot = operator.itemgetter(slice(2, None))
    _remove_trailing_slash = operator.itemgetter(slice(-1))

    def _filter_trailing_slash(self, paths):
        sep = self.parser.sep
        anchor_len = len(self.锚点)
        for path_str in paths:
            if len(path_str) > anchor_len and path_str[-1] == sep:
                path_str = path_str[:-1]
            yield path_str

    def _from_dir_entry(self, dir_entry, path_str):
        path = self.with_segments(path_str)
        path._str = path_str
        path._info = DirEntryInfo(dir_entry)
        return path

    def 迭代目录(self):
        """Yield path objects of the directory contents.

        The children are yielded in arbitrary order, and the
        special entries '.' and '..' are not included.
        """
        root_dir = str(self)
        with os.scandir(root_dir) as scandir_it:
            entries = list(scandir_it)
        if root_dir == '.':
            return (self._from_dir_entry(e, e.name) for e in entries)
        else:
            return (self._from_dir_entry(e, e.path) for e in entries)

    def 通配(self, pattern, *, case_sensitive=None, recurse_symlinks=False):
        """Iterate over this subtree and yield all existing files (of any
        kind, including directories) matching the given relative pattern.
        """
        sys.audit('pathlib.Path.glob', self, pattern)
        if case_sensitive is None:
            case_sensitive = self.parser is posixpath
            case_pedantic = False
        else:
            case_pedantic = True
        分片 = self._parse_pattern(pattern)
        recursive = True if recurse_symlinks else _no_recurse_symlinks
        globber = _StringGlobber(self.parser.sep, case_sensitive, case_pedantic, recursive)
        select = globber.selector(分片[::-1])
        根 = str(self)
        paths = select(self.parser.join(根, ''))
        if 根 == '.':
            paths = map(self._remove_leading_dot, paths)
        if 分片[-1] == '':
            paths = map(self._remove_trailing_slash, paths)
        elif 分片[-1] == '**':
            paths = self._filter_trailing_slash(paths)
        paths = map(self._from_parsed_string, paths)
        return paths

    def 递归通配(self, pattern, *, case_sensitive=None, recurse_symlinks=False):
        """Recursively yield all existing files (of any kind, including
        directories) matching the given relative pattern, anywhere in
        this subtree.
        """
        sys.audit('pathlib.Path.rglob', self, pattern)
        pattern = self.parser.join('**', pattern)
        return self.通配(pattern, case_sensitive=case_sensitive, recurse_symlinks=recurse_symlinks)

    def 遍历(self, top_down=True, on_error=None, follow_symlinks=False):
        """Walk the directory tree from this directory, similar to os.walk()."""
        sys.audit('pathlib.Path.walk', self, on_error, follow_symlinks)
        root_dir = str(self)
        if not follow_symlinks:
            follow_symlinks = os._walk_symlinks_as_files
        results = os.walk(root_dir, top_down, on_error, follow_symlinks)
        for path_str, dirnames, filenames in results:
            if root_dir == '.':
                path_str = path_str[2:]
            yield (self._from_parsed_string(path_str), dirnames, filenames)

    def 绝对化(self):
        """Return an absolute version of this path
        No normalization or symlink resolution is performed.

        Use resolve() to resolve symlinks and remove '..' segments.
        """
        if self.是绝对路径吗():
            return self
        if self.根:
            盘符 = os.path.splitroot(os.getcwd())[0]
            return self._from_parsed_parts(盘符, self.根, self._tail)
        if self.盘符:
            当前目录 = os.path.abspath(self.盘符)
        else:
            当前目录 = os.getcwd()
        if not self._tail:
            return self._from_parsed_string(当前目录)
        盘符, 根, rel = os.path.splitroot(当前目录)
        if not rel:
            return self._from_parsed_parts(盘符, 根, self._tail)
        tail = rel.split(self.parser.sep)
        tail.extend(self._tail)
        return self._from_parsed_parts(盘符, 根, tail)

    @classmethod
    def 当前目录(cls):
        """Return a new path pointing to the current working directory."""
        当前目录 = os.getcwd()
        path = cls(当前目录)
        path._str = 当前目录
        return path

    def 解析(self, strict=False):
        """
        Make the path absolute, resolving all symlinks on the way and also
        normalizing it.
        """
        return self.with_segments(os.path.realpath(self, strict=strict))
    if pwd:

        def 属主(self, *, follow_symlinks=True):
            """
            Return the login name of the file owner.
            """
            uid = self.取状态(follow_symlinks=follow_symlinks).st_uid
            return pwd.getpwuid(uid).pw_name
    else:

        def 属主(self, *, follow_symlinks=True):
            """
            Return the login name of the file owner.
            """
            f = f'{type(self).__name__}.owner()'
            raise 不支持的操作(f'{f} is unsupported on this system')
    if grp:

        def 属组(self, *, follow_symlinks=True):
            """
            Return the group name of the file gid.
            """
            gid = self.取状态(follow_symlinks=follow_symlinks).st_gid
            return grp.getgrgid(gid).gr_name
    else:

        def 属组(self, *, follow_symlinks=True):
            """
            Return the group name of the file gid.
            """
            f = f'{type(self).__name__}.group()'
            raise 不支持的操作(f'{f} is unsupported on this system')
    if hasattr(os, 'readlink'):

        def 读软链(self):
            """
            Return the path to which the symbolic link points.
            """
            return self.with_segments(os.readlink(self))
    else:

        def 读软链(self):
            """
            Return the path to which the symbolic link points.
            """
            f = f'{type(self).__name__}.readlink()'
            raise 不支持的操作(f'{f} is unsupported on this system')

    def 触碰(self, mode=438, exist_ok=True):
        """
        Create this file with the given access mode, if it doesn't exist.
        """
        if exist_ok:
            try:
                os.utime(self, None)
            except OSError:
                pass
            else:
                return
        flags = os.O_CREAT | os.O_WRONLY
        if not exist_ok:
            flags |= os.O_EXCL
        fd = os.open(self, flags, mode)
        os.close(fd)

    def 建目录(self, mode=511, parents=False, exist_ok=False):
        """
        Create a new directory at this given path.
        """
        try:
            os.mkdir(self, mode)
        except FileNotFoundError:
            if not parents or self.父目录 == self:
                raise
            self.父目录.mkdir(parents=True, exist_ok=True)
            self.建目录(mode, parents=False, exist_ok=exist_ok)
        except OSError:
            if not exist_ok or not self.是目录吗():
                raise

    def 改权限(self, mode, *, follow_symlinks=True):
        """
        Change the permissions of the path, like os.chmod().
        """
        os.chmod(self, mode, follow_symlinks=follow_symlinks)

    def lchmod(self, mode):
        """
        Like chmod(), except if the path points to a symlink, the symlink's
        permissions are changed, rather than its target's.
        """
        self.改权限(mode, follow_symlinks=False)

    def 删文件(self, missing_ok=False):
        """
        Remove this file or link.
        If the path is a directory, use rmdir() instead.
        """
        try:
            os.unlink(self)
        except FileNotFoundError:
            if not missing_ok:
                raise

    def 删目录(self):
        """
        Remove this directory.  The directory must be empty.
        """
        os.rmdir(self)

    def _delete(self):
        """
        Delete this file or directory (including all sub-directories).
        """
        if self.是软链吗() or self.是联接点吗():
            self.删文件()
        elif self.是目录吗():
            import shutil
            shutil.rmtree(self)
        else:
            self.删文件()

    def 改名(self, target):
        """
        Rename this path to the target path.

        The target path may be absolute or relative. Relative paths are
        interpreted relative to the current working directory, *not* the
        directory of the Path object.

        Returns the new Path instance pointing to the target path.
        """
        os.rename(self, target)
        if not hasattr(target, 'with_segments'):
            target = self.with_segments(target)
        return target

    def replace(self, target):
        """
        Rename this path to the target path, overwriting if that path exists.

        The target path may be absolute or relative. Relative paths are
        interpreted relative to the current working directory, *not* the
        directory of the Path object.

        Returns the new Path instance pointing to the target path.
        """
        os.replace(self, target)
        if not hasattr(target, 'with_segments'):
            target = self.with_segments(target)
        return target

    def copy(self, target, **kwargs):
        """
        Recursively copy this file or directory tree to the given destination.
        """
        if not hasattr(target, 'with_segments'):
            target = self.with_segments(target)
        ensure_distinct_paths(self, target)
        target._copy_from(self, **kwargs)
        return target.joinpath()

    def copy_into(self, target_dir, **kwargs):
        """
        Copy this file or directory tree into the given existing directory.
        """
        名字 = self.名字
        if not 名字:
            raise ValueError(f'{self!r} has an empty name')
        elif hasattr(target_dir, 'with_segments'):
            target = target_dir / 名字
        else:
            target = self.with_segments(target_dir, 名字)
        return self.copy(target, **kwargs)

    def _copy_from(self, source, follow_symlinks=True, preserve_metadata=False):
        """
        Recursively copy the given path to this path.
        """
        if not follow_symlinks and source.info.is_symlink():
            self._copy_from_symlink(source, preserve_metadata)
        elif source.info.is_dir():
            children = source.iterdir()
            os.mkdir(self)
            for child in children:
                self.拼路径(child.name)._copy_from(child, follow_symlinks, preserve_metadata)
            if preserve_metadata:
                copy_info(source.info, self)
        else:
            self._copy_from_file(source, preserve_metadata)

    def _copy_from_file(self, source, preserve_metadata=False):
        ensure_different_files(source, self)
        with magic_open(source, 'rb') as source_f:
            with open(self, 'wb') as target_f:
                copyfileobj(source_f, target_f)
        if preserve_metadata:
            copy_info(source.info, self)
    if copyfile2:
        _copy_from_file_fallback = _copy_from_file

        def _copy_from_file(self, source, preserve_metadata=False):
            try:
                source = os.fspath(source)
            except TypeError:
                pass
            else:
                copyfile2(source, str(self))
                return
            self._copy_from_file_fallback(source, preserve_metadata)
    if os.name == 'nt':

        def _copy_from_symlink(self, source, preserve_metadata=False):
            os.symlink(str(source.readlink()), self, source.info.is_dir())
            if preserve_metadata:
                copy_info(source.info, self, follow_symlinks=False)
    else:

        def _copy_from_symlink(self, source, preserve_metadata=False):
            os.symlink(str(source.readlink()), self)
            if preserve_metadata:
                copy_info(source.info, self, follow_symlinks=False)

    def move(self, target):
        """
        Recursively move this file or directory tree to the given destination.
        """
        try:
            target = self.with_segments(target)
        except TypeError:
            pass
        else:
            ensure_different_files(self, target)
            try:
                os.replace(self, target)
            except OSError as err:
                if err.errno != EXDEV:
                    raise
            else:
                return target.joinpath()
        target = self.copy(target, follow_symlinks=False, preserve_metadata=True)
        self._delete()
        return target

    def move_into(self, target_dir):
        """
        Move this file or directory tree into the given existing directory.
        """
        名字 = self.名字
        if not 名字:
            raise ValueError(f'{self!r} has an empty name')
        elif hasattr(target_dir, 'with_segments'):
            target = target_dir / 名字
        else:
            target = self.with_segments(target_dir, 名字)
        return self.move(target)
    if hasattr(os, 'symlink'):

        def 建软链(self, target, target_is_directory=False):
            """
            Make this path a symlink pointing to the target path.
            Note the order of arguments (link, target) is the reverse of os.symlink.
            """
            os.symlink(target, self, target_is_directory)
    else:

        def 建软链(self, target, target_is_directory=False):
            """
            Make this path a symlink pointing to the target path.
            Note the order of arguments (link, target) is the reverse of os.symlink.
            """
            f = f'{type(self).__name__}.symlink_to()'
            raise 不支持的操作(f'{f} is unsupported on this system')
    if hasattr(os, 'link'):

        def 建硬链(self, target):
            """
            Make this path a hard link pointing to the same file as *target*.

            Note the order of arguments (self, target) is the reverse of os.link's.
            """
            os.link(target, self)
    else:

        def 建硬链(self, target):
            """
            Make this path a hard link pointing to the same file as *target*.

            Note the order of arguments (self, target) is the reverse of os.link's.
            """
            f = f'{type(self).__name__}.hardlink_to()'
            raise 不支持的操作(f'{f} is unsupported on this system')

    def 展开用户目录(self):
        """ Return a new path with expanded ~ and ~user constructs
        (as returned by os.path.expanduser)
        """
        if not (self.盘符 or self.根) and self._tail and (self._tail[0][:1] == '~'):
            homedir = os.path.expanduser(self._tail[0])
            if homedir[:1] == '~':
                raise RuntimeError('Could not determine home directory.')
            drv, 根, tail = self._parse_path(homedir)
            return self._from_parsed_parts(drv, 根, tail + self._tail[1:])
        return self

    @classmethod
    def 家目录(cls):
        """Return a new path pointing to expanduser('~').
        """
        homedir = os.path.expanduser('~')
        if homedir == '~':
            raise RuntimeError('Could not determine home directory.')
        return cls(homedir)

    def 转URI(self):
        """Return the path as a URI."""
        if not self.是绝对路径吗():
            raise ValueError("relative paths can't be expressed as file URIs")
        from urllib.request import pathname2url
        return pathname2url(str(self), add_scheme=True)

    @classmethod
    def from_uri(cls, uri):
        """Return a new path from the given 'file' URI."""
        from urllib.error import URLError
        from urllib.request import url2pathname
        try:
            path = cls(url2pathname(uri, require_scheme=True))
        except URLError as exc:
            raise ValueError(exc.reason) from None
        if not path.is_absolute():
            raise ValueError(f'URI is not absolute: {uri!r}')
        return path
_装类转发(路径, {'absolute': '绝对化', 'as_uri': '转URI', 'chmod': '改权限', 'cwd': '当前目录', 'exists': '存在吗', 'expanduser': '展开用户目录', 'glob': '通配', 'group': '属组', 'hardlink_to': '建硬链', 'home': '家目录', 'is_block_device': '是块设备吗', 'is_char_device': '是字符设备吗', 'is_dir': '是目录吗', 'is_fifo': '是FIFO吗', 'is_file': '是文件吗', 'is_junction': '是联接点吗', 'is_mount': '是挂载点吗', 'is_socket': '是套接字吗', 'is_symlink': '是软链吗', 'iterdir': '迭代目录', 'lstat': '取软链状态', 'mkdir': '建目录', 'owner': '属主', 'read_bytes': '读字节', 'read_text': '读文本', 'readlink': '读软链', 'rename': '改名', 'resolve': '解析', 'rglob': '递归通配', 'rmdir': '删目录', 'samefile': '同一文件吗', 'stat': '取状态', 'symlink_to': '建软链', 'touch': '触碰', 'unlink': '删文件', 'walk': '遍历', 'write_bytes': '写字节', 'write_text': '写文本'}, {'absolute': '绝对化', 'anchor': '锚点', 'as_uri': '转URI', 'chmod': '改权限', 'cwd': '当前目录', 'drive': '盘符', 'exists': '存在吗', 'expanduser': '展开用户目录', 'glob': '通配', 'group': '属组', 'hardlink_to': '建硬链', 'home': '家目录', 'is_absolute': '是绝对路径吗', 'is_block_device': '是块设备吗', 'is_char_device': '是字符设备吗', 'is_dir': '是目录吗', 'is_fifo': '是FIFO吗', 'is_file': '是文件吗', 'is_junction': '是联接点吗', 'is_mount': '是挂载点吗', 'is_socket': '是套接字吗', 'is_symlink': '是软链吗', 'iterdir': '迭代目录', 'joinpath': '拼路径', 'lstat': '取软链状态', 'mkdir': '建目录', 'name': '名字', 'owner': '属主', 'parent': '父目录', 'read_bytes': '读字节', 'read_text': '读文本', 'readlink': '读软链', 'rename': '改名', 'resolve': '解析', 'rglob': '递归通配', 'rmdir': '删目录', 'root': '根', 'samefile': '同一文件吗', 'stat': '取状态', 'symlink_to': '建软链', 'touch': '触碰', 'unlink': '删文件', 'walk': '遍历', 'write_bytes': '写字节', 'write_text': '写文本'})

class POSIX路径(路径, 纯POSIX路径):
    """Path subclass for non-Windows systems.

    On a POSIX system, instantiating a Path should return this object.
    """
    __slots__ = ()
    if os.name == 'nt':

        def __new__(cls, *args, **kwargs):
            raise 不支持的操作(f'cannot instantiate {cls.__name__!r} on your system')

class Windows路径(路径, 纯Windows路径):
    """Path subclass for Windows systems.

    On a Windows system, instantiating a Path should return this object.
    """
    __slots__ = ()
    if os.name != 'nt':

        def __new__(cls, *args, **kwargs):
            raise 不支持的操作(f'cannot instantiate {cls.__name__!r} on your system')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 子模块的英文名也留着（照「英文原名一个都不能少」）：
# `JSON解析.decoder` 跟 `JSON解析.解码模块` 是**同一个模块对象**。
from . import 路径类型 as types

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import pathlib as _英文库
不支持的操作 = _英文库.UnsupportedOperation
_模块别名 = {
    'Path': '路径',
    'PosixPath': 'POSIX路径',
    'PurePath': '纯路径',
    'PurePosixPath': '纯POSIX路径',
    'PureWindowsPath': '纯Windows路径',
    'UnsupportedOperation': '不支持的操作',
    'WindowsPath': 'Windows路径',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '纯路径': {
        'anchor': '锚点',
        'as_posix': '转POSIX',
        'as_uri': '转URI',
        'drive': '盘符',
        'full_match': '完全匹配',
        'is_absolute': '是绝对路径吗',
        'is_relative_to': '相对于吗',
        'is_reserved': '是保留名吗',
        'joinpath': '拼路径',
        'match': '匹配',
        'name': '名字',
        'parent': '父目录',
        'parents': '各级父目录',
        'parts': '分片',
        'relative_to': '相对路径',
        'root': '根',
        'stem': '主干名',
        'suffix': '后缀',
        'suffixes': '后缀们',
        'with_name': '换名字',
        'with_stem': '换主干名',
        'with_suffix': '换后缀',
    },
    '路径': {
        'absolute': '绝对化',
        'as_uri': '转URI',
        'chmod': '改权限',
        'cwd': '当前目录',
        'exists': '存在吗',
        'expanduser': '展开用户目录',
        'glob': '通配',
        'group': '属组',
        'hardlink_to': '建硬链',
        'home': '家目录',
        'is_block_device': '是块设备吗',
        'is_char_device': '是字符设备吗',
        'is_dir': '是目录吗',
        'is_fifo': '是FIFO吗',
        'is_file': '是文件吗',
        'is_junction': '是联接点吗',
        'is_mount': '是挂载点吗',
        'is_socket': '是套接字吗',
        'is_symlink': '是软链吗',
        'iterdir': '迭代目录',
        'lstat': '取软链状态',
        'mkdir': '建目录',
        'owner': '属主',
        'read_bytes': '读字节',
        'read_text': '读文本',
        'readlink': '读软链',
        'rename': '改名',
        'resolve': '解析',
        'rglob': '递归通配',
        'rmdir': '删目录',
        'samefile': '同一文件吗',
        'stat': '取状态',
        'symlink_to': '建软链',
        'touch': '触碰',
        'unlink': '删文件',
        'walk': '遍历',
        'write_bytes': '写字节',
        'write_text': '写文本',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '纯路径': {
        'anchor': '锚点',
        'as_posix': '转POSIX',
        'as_uri': '转URI',
        'drive': '盘符',
        'full_match': '完全匹配',
        'is_absolute': '是绝对路径吗',
        'is_relative_to': '相对于吗',
        'is_reserved': '是保留名吗',
        'joinpath': '拼路径',
        'match': '匹配',
        'name': '名字',
        'parent': '父目录',
        'parents': '各级父目录',
        'parts': '分片',
        'relative_to': '相对路径',
        'root': '根',
        'stem': '主干名',
        'suffix': '后缀',
        'suffixes': '后缀们',
        'with_name': '换名字',
        'with_stem': '换主干名',
        'with_suffix': '换后缀',
    },
    '路径': {
        'absolute': '绝对化',
        'anchor': '锚点',
        'as_uri': '转URI',
        'chmod': '改权限',
        'cwd': '当前目录',
        'drive': '盘符',
        'exists': '存在吗',
        'expanduser': '展开用户目录',
        'glob': '通配',
        'group': '属组',
        'hardlink_to': '建硬链',
        'home': '家目录',
        'is_absolute': '是绝对路径吗',
        'is_block_device': '是块设备吗',
        'is_char_device': '是字符设备吗',
        'is_dir': '是目录吗',
        'is_fifo': '是FIFO吗',
        'is_file': '是文件吗',
        'is_junction': '是联接点吗',
        'is_mount': '是挂载点吗',
        'is_socket': '是套接字吗',
        'is_symlink': '是软链吗',
        'iterdir': '迭代目录',
        'joinpath': '拼路径',
        'lstat': '取软链状态',
        'mkdir': '建目录',
        'name': '名字',
        'owner': '属主',
        'parent': '父目录',
        'read_bytes': '读字节',
        'read_text': '读文本',
        'readlink': '读软链',
        'rename': '改名',
        'resolve': '解析',
        'rglob': '递归通配',
        'rmdir': '删目录',
        'root': '根',
        'samefile': '同一文件吗',
        'stat': '取状态',
        'symlink_to': '建软链',
        'touch': '触碰',
        'unlink': '删文件',
        'walk': '遍历',
        'write_bytes': '写字节',
        'write_text': '写文本',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'POSIX路径',
    'Windows路径',
    '不支持的操作',
    '纯POSIX路径',
    '纯Windows路径',
    '纯路径',
    '路径',
]

# ---- 转发层结束 ----
