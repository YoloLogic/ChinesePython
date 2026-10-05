# -*- coding: utf-8 -*-
"""通配文件 —— 汉语库（由 tools/汉化库.py 从 Lib/glob.py 机械生成，**不要手改**）。

英文库 Lib/glob.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 通配文件
"""


"""Filename globbing utility."""
_英文原名表 = {'escape': '转义', 'glob': '通配', 'has_magic': '有通配符吗', 'iglob': '迭代通配', 'magic_check': '通配检查', 'magic_check_bytes': '通配检查字节'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import contextlib
import os
import re
import fnmatch
import functools
import itertools
import operator
import stat
import sys
__all__ = ['glob', 'iglob', 'escape', 'translate']

def 通配(pathname, *, root_dir=None, dir_fd=None, recursive=False, include_hidden=False):
    """Return a list of paths matching a `pathname` pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. Unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns by default.

    The order of the returned list is undefined. Sort it if you need a
    particular order.

    If `root_dir` is not None, it should be a path-like object specifying
    the root directory for searching.  It has the same effect as changing
    the current directory before calling it (without actually changing it).
    If pathname is relative, the result will contain paths relative to
    `root_dir`.

    If `dir_fd` is not None, it should be a file descriptor referring to a
    directory, and paths will then be relative to that directory.

    If `include_hidden` is true, wildcards can match path segments beginning
    with a dot ('.').

    If `recursive` is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    return list(迭代通配(pathname, root_dir=root_dir, dir_fd=dir_fd, recursive=recursive, include_hidden=include_hidden))

def 迭代通配(pathname, *, root_dir=None, dir_fd=None, recursive=False, include_hidden=False):
    """Return an iterator which yields the paths matching a `pathname` pattern.

    The pattern may contain simple shell-style wildcards a la
    fnmatch. However, unlike fnmatch, filenames starting with a
    dot are special cases that are not matched by '*' and '?'
    patterns.

    The order of the returned paths is undefined. Sort them if you need a
    particular order.

    If `root_dir` is not None, it should be a path-like object specifying
    the root directory for searching.  It has the same effect as changing
    the current directory before calling it (without actually changing it).
    If pathname is relative, the result will contain paths relative to
    `root_dir`.

    If `dir_fd` is not None, it should be a file descriptor referring to a
    directory, and paths will then be relative to that directory.

    If `include_hidden` is true, wildcards can match path segments beginning
    with a dot ('.').

    If `recursive` is true, the pattern '**' will match any files and
    zero or more directories and subdirectories.
    """
    sys.audit('glob.glob', pathname, recursive)
    sys.audit('glob.glob/2', pathname, recursive, root_dir, dir_fd)
    if root_dir is not None:
        root_dir = os.fspath(root_dir)
    else:
        root_dir = pathname[:0]
    it = _iglob(pathname, root_dir, dir_fd, recursive, False, include_hidden=include_hidden)
    if not pathname or (recursive and _isrecursive(pathname[:2])):
        try:
            s = next(it)
            if s:
                it = itertools.chain((s,), it)
        except StopIteration:
            pass
    return it

def _iglob(pathname, root_dir, dir_fd, recursive, dironly, include_hidden=False):
    dirname, basename = os.path.split(pathname)
    if not 有通配符吗(pathname):
        assert not dironly
        if basename:
            if _lexists(_join(root_dir, pathname), dir_fd):
                yield pathname
        elif _isdir(_join(root_dir, dirname), dir_fd):
            yield pathname
        return
    if not dirname:
        if recursive and _isrecursive(basename):
            yield from _glob2(root_dir, basename, dir_fd, dironly, include_hidden=include_hidden)
        else:
            yield from _glob1(root_dir, basename, dir_fd, dironly, include_hidden=include_hidden)
        return
    if dirname != pathname and 有通配符吗(dirname):
        dirs = _iglob(dirname, root_dir, dir_fd, recursive, True, include_hidden=include_hidden)
    else:
        dirs = [dirname]
    if 有通配符吗(basename):
        if recursive and _isrecursive(basename):
            glob_in_dir = _glob2
        else:
            glob_in_dir = _glob1
    else:
        glob_in_dir = _glob0
    for dirname in dirs:
        for name in glob_in_dir(_join(root_dir, dirname), basename, dir_fd, dironly, include_hidden=include_hidden):
            yield os.path.join(dirname, name)

def _glob1(dirname, pattern, dir_fd, dironly, include_hidden=False):
    names = _listdir(dirname, dir_fd, dironly)
    if not (include_hidden or _ishidden(pattern)):
        names = (x for x in names if not _ishidden(x))
    return fnmatch.filter(names, pattern)

def _glob0(dirname, basename, dir_fd, dironly, include_hidden=False):
    if basename:
        if _lexists(_join(dirname, basename), dir_fd):
            return [basename]
    elif _isdir(dirname, dir_fd):
        return [basename]
    return []
_deprecated_function_message = '{name} is deprecated and will be removed in Python {remove}. Use glob.glob and pass a directory to its root_dir argument instead.'

def glob0(dirname, pattern):
    import warnings
    warnings._deprecated('glob.glob0', _deprecated_function_message, remove=(3, 15))
    return _glob0(dirname, pattern, None, False)

def glob1(dirname, pattern):
    import warnings
    warnings._deprecated('glob.glob1', _deprecated_function_message, remove=(3, 15))
    return _glob1(dirname, pattern, None, False)

def _glob2(dirname, pattern, dir_fd, dironly, include_hidden=False):
    assert _isrecursive(pattern)
    if not dirname or _isdir(dirname, dir_fd):
        yield pattern[:0]
    yield from _rlistdir(dirname, dir_fd, dironly, include_hidden=include_hidden)

def _iterdir(dirname, dir_fd, dironly):
    try:
        fd = None
        fsencode = None
        if dir_fd is not None:
            if dirname:
                fd = arg = os.open(dirname, _dir_open_flags, dir_fd=dir_fd)
            else:
                arg = dir_fd
            if isinstance(dirname, bytes):
                fsencode = os.fsencode
        elif dirname:
            arg = dirname
        elif isinstance(dirname, bytes):
            arg = bytes(os.curdir, 'ASCII')
        else:
            arg = os.curdir
        try:
            with os.scandir(arg) as it:
                for entry in it:
                    try:
                        if not dironly or entry.is_dir():
                            if fsencode is not None:
                                yield fsencode(entry.name)
                            else:
                                yield entry.name
                    except OSError:
                        pass
        finally:
            if fd is not None:
                os.close(fd)
    except OSError:
        return

def _listdir(dirname, dir_fd, dironly):
    with contextlib.closing(_iterdir(dirname, dir_fd, dironly)) as it:
        return list(it)

def _rlistdir(dirname, dir_fd, dironly, include_hidden=False):
    names = _listdir(dirname, dir_fd, dironly)
    for x in names:
        if include_hidden or not _ishidden(x):
            yield x
            path = _join(dirname, x) if dirname else x
            for y in _rlistdir(path, dir_fd, dironly, include_hidden=include_hidden):
                yield _join(x, y)

def _lexists(pathname, dir_fd):
    if dir_fd is None:
        return os.path.lexists(pathname)
    try:
        os.lstat(pathname, dir_fd=dir_fd)
    except (OSError, ValueError):
        return False
    else:
        return True

def _isdir(pathname, dir_fd):
    if dir_fd is None:
        return os.path.isdir(pathname)
    try:
        st = os.stat(pathname, dir_fd=dir_fd)
    except (OSError, ValueError):
        return False
    else:
        return stat.S_ISDIR(st.st_mode)

def _join(dirname, basename):
    if not dirname or not basename:
        return dirname or basename
    return os.path.join(dirname, basename)
通配检查 = re.compile('([*?[])')
通配检查字节 = re.compile(b'([*?[])')

def 有通配符吗(s):
    if isinstance(s, bytes):
        match = 通配检查字节.search(s)
    else:
        match = 通配检查.search(s)
    return match is not None

def _ishidden(path):
    return path[0] in ('.', b'.'[0])

def _isrecursive(pattern):
    if isinstance(pattern, bytes):
        return pattern == b'**'
    else:
        return pattern == '**'

def 转义(pathname):
    """Escape all special characters.
    """
    drive, pathname = os.path.splitdrive(pathname)
    if isinstance(pathname, bytes):
        pathname = 通配检查字节.sub(b'[\\1]', pathname)
    else:
        pathname = 通配检查.sub('[\\1]', pathname)
    return drive + pathname
_special_parts = ('', '.', '..')
_dir_open_flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0)
_no_recurse_symlinks = object()

def translate(pat, *, recursive=False, include_hidden=False, seps=None):
    """Translate a pathname with shell wildcards to a regular expression.

    If `recursive` is true, the pattern segment '**' will match any number
    of path segments.

    If `include_hidden` is true, wildcards can match path segments beginning
    with a dot ('.').

    If a sequence of separator characters is given to `seps`, they will be
    used to split the pattern into segments and match path separators.  If
    not given, os.path.sep and os.path.altsep (where available) are used.
    """
    if not seps:
        if os.path.altsep:
            seps = (os.path.sep, os.path.altsep)
        else:
            seps = os.path.sep
    escaped_seps = ''.join(map(re.escape, seps))
    any_sep = f'[{escaped_seps}]' if len(seps) > 1 else escaped_seps
    not_sep = f'[^{escaped_seps}]'
    if include_hidden:
        one_last_segment = f'{not_sep}+'
        one_segment = f'{one_last_segment}{any_sep}'
        any_segments = f'(?:.+{any_sep})?'
        any_last_segments = '.*'
    else:
        one_last_segment = f'[^{escaped_seps}.]{not_sep}*'
        one_segment = f'{one_last_segment}{any_sep}'
        any_segments = f'(?:{one_segment})*'
        any_last_segments = f'{any_segments}(?:{one_last_segment})?'
    results = []
    parts = re.split(any_sep, pat)
    last_part_idx = len(parts) - 1
    for idx, part in enumerate(parts):
        if part == '*':
            results.append(one_segment if idx < last_part_idx else one_last_segment)
        elif recursive and part == '**':
            if idx < last_part_idx:
                if parts[idx + 1] != '**':
                    results.append(any_segments)
            else:
                results.append(any_last_segments)
        else:
            if part:
                if not include_hidden and part[0] in '*?':
                    results.append('(?!\\.)')
                results.extend(fnmatch._translate(part, f'{not_sep}*', not_sep)[0])
            if idx < last_part_idx:
                results.append(any_sep)
    res = ''.join(results)
    return f'(?s:{res})\\z'

@functools.lru_cache(maxsize=512)
def _compile_pattern(pat, seps, case_sensitive, recursive=True):
    """Compile given glob pattern to a re.Pattern object (observing case
    sensitivity)."""
    flags = re.NOFLAG if case_sensitive else re.IGNORECASE
    regex = translate(pat, recursive=recursive, include_hidden=True, seps=seps)
    return re.compile(regex, flags=flags).match

class _GlobberBase:
    """Abstract class providing shell-style pattern matching and globbing.
    """

    def __init__(self, sep, case_sensitive, case_pedantic=False, recursive=False):
        self.sep = sep
        self.case_sensitive = case_sensitive
        self.case_pedantic = case_pedantic
        self.recursive = recursive

    @staticmethod
    def lexists(path):
        """Implements os.path.lexists().
        """
        raise NotImplementedError

    @staticmethod
    def scandir(path):
        """Like os.scandir(), but generates (entry, name, path) tuples.
        """
        raise NotImplementedError

    @staticmethod
    def concat_path(path, text):
        """Implements path concatenation.
        """
        raise NotImplementedError

    def compile(self, pat, altsep=None):
        seps = (self.sep, altsep) if altsep else self.sep
        return _compile_pattern(pat, seps, self.case_sensitive, self.recursive)

    def selector(self, parts):
        """Returns a function that selects from a given path, walking and
        filtering according to the glob-style pattern parts in *parts*.
        """
        if not parts:
            return self.select_exists
        part = parts.pop()
        if self.recursive and part == '**':
            selector = self.recursive_selector
        elif part in _special_parts:
            selector = self.special_selector
        elif not self.case_pedantic and 通配检查.search(part) is None:
            selector = self.literal_selector
        else:
            selector = self.wildcard_selector
        return selector(part, parts)

    def special_selector(self, part, parts):
        """Returns a function that selects special children of the given path.
        """
        if parts:
            part += self.sep
        select_next = self.selector(parts)

        def select_special(path, exists=False):
            path = self.concat_path(path, part)
            return select_next(path, exists)
        return select_special

    def literal_selector(self, part, parts):
        """Returns a function that selects a literal descendant of a path.
        """
        while parts and 通配检查.search(parts[-1]) is None:
            part += self.sep + parts.pop()
        if parts:
            part += self.sep
        select_next = self.selector(parts)

        def select_literal(path, exists=False):
            path = self.concat_path(path, part)
            return select_next(path, exists=False)
        return select_literal

    def wildcard_selector(self, part, parts):
        """Returns a function that selects direct children of a given path,
        filtering by pattern.
        """
        match = None if part == '*' else self.compile(part)
        dir_only = bool(parts)
        if dir_only:
            select_next = self.selector(parts)

        def select_wildcard(path, exists=False):
            try:
                entries = self.scandir(path)
            except OSError:
                pass
            else:
                for entry, entry_name, entry_path in entries:
                    if match is None or match(entry_name):
                        if dir_only:
                            try:
                                if not entry.is_dir():
                                    continue
                            except OSError:
                                continue
                            entry_path = self.concat_path(entry_path, self.sep)
                            yield from select_next(entry_path, exists=True)
                        else:
                            yield entry_path
        return select_wildcard

    def recursive_selector(self, part, parts):
        """Returns a function that selects a given path and all its children,
        recursively, filtering by pattern.
        """
        while parts and parts[-1] == '**':
            parts.pop()
        follow_symlinks = self.recursive is not _no_recurse_symlinks
        if follow_symlinks:
            while parts and parts[-1] not in _special_parts:
                part += self.sep + parts.pop()
        match = None if part == '**' else self.compile(part)
        dir_only = bool(parts)
        select_next = self.selector(parts)

        def select_recursive(path, exists=False):
            match_pos = len(str(path))
            if match is None or match(str(path), match_pos):
                yield from select_next(path, exists)
            stack = [path]
            while stack:
                yield from select_recursive_step(stack, match_pos)

        def select_recursive_step(stack, match_pos):
            path = stack.pop()
            try:
                entries = self.scandir(path)
            except OSError:
                pass
            else:
                for entry, _entry_name, entry_path in entries:
                    is_dir = False
                    try:
                        if entry.is_dir(follow_symlinks=follow_symlinks):
                            is_dir = True
                    except OSError:
                        pass
                    if is_dir or not dir_only:
                        entry_path_str = str(entry_path)
                        if dir_only:
                            entry_path = self.concat_path(entry_path, self.sep)
                        if match is None or match(entry_path_str, match_pos):
                            if dir_only:
                                yield from select_next(entry_path, exists=True)
                            else:
                                yield entry_path
                        if is_dir:
                            stack.append(entry_path)
        return select_recursive

    def select_exists(self, path, exists=False):
        """Yields the given path, if it exists.
        """
        if exists:
            yield path
        elif self.lexists(path):
            yield path

class _StringGlobber(_GlobberBase):
    """Provides shell-style pattern matching and globbing for string paths.
    """
    lexists = staticmethod(os.path.lexists)
    concat_path = operator.add

    @staticmethod
    def scandir(path):
        with os.scandir(path) as scandir_it:
            entries = list(scandir_it)
        return ((entry, entry.name, entry.path) for entry in entries)

class _PathGlobber(_GlobberBase):
    """Provides shell-style pattern matching and globbing for pathlib paths.
    """

    @staticmethod
    def lexists(path):
        return path.info.exists(follow_symlinks=False)

    @staticmethod
    def scandir(path):
        return ((child.info, child.name, child) for child in path.iterdir())

    @staticmethod
    def concat_path(path, text):
        return path.with_segments(str(path) + text)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'escape': '转义',
    'glob': '通配',
    'has_magic': '有通配符吗',
    'iglob': '迭代通配',
    'magic_check': '通配检查',
    'magic_check_bytes': '通配检查字节',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '转义',
    '迭代通配',
    '通配',
]

# ---- 转发层结束 ----
