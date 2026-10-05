# -*- coding: utf-8 -*-
"""操作系统 —— 汉语库（由 tools/汉化库.py 从 Lib/os.py 机械生成，**不要手改**）。

英文库 Lib/os.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 操作系统
"""


"""OS routines for NT or Posix depending on what system we're on.

This exports:
  - all functions from posix or nt, e.g. unlink, stat, etc.
  - os.path is either posixpath or ntpath
  - os.name is either 'posix' or 'nt'
  - os.curdir is a string representing the current directory (always '.')
  - os.pardir is a string representing the parent directory (always '..')
  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')
  - os.extsep is the extension separator (always '.')
  - os.altsep is the alternate pathname separator (None or '/')
  - os.pathsep is the component separator used in $PATH etc
  - os.linesep is the line separator in text files ('\\n' or '\\r\\n')
  - os.defpath is the default search path for executables
  - os.devnull is the file path of the null device ('/dev/null', etc.)

Programs that import and use 'os' stand a better chance of being
portable between different platforms.  Of course, they must then
only use functions that are defined by all platforms (e.g., unlink
and opendir), and leave all pathname manipulation to os.path
(e.g., split and join).
"""
import abc
import sys
import stat as st
from _collections_abc import _check_methods
GenericAlias = type(list[int])
_names = sys.builtin_module_names
__all__ = ['altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep', 'defpath', 'name', 'path', 'devnull', 'SEEK_SET', 'SEEK_CUR', 'SEEK_END', 'fsencode', 'fsdecode', 'get_exec_path', 'fdopen', 'extsep']

def _exists(name):
    return name in globals()

def _get_exports_list(module):
    try:
        return list(module.__all__)
    except AttributeError:
        return [n for n in dir(module) if n[0] != '_']
if 'posix' in _names:
    name = 'posix'
    linesep = '\n'
    from posix import *
    try:
        from posix import _exit
        __all__.append('_exit')
    except ImportError:
        pass
    import posixpath as path
    try:
        from posix import _have_functions
    except ImportError:
        pass
    try:
        from posix import _create_environ
    except ImportError:
        pass
    import posix
    __all__.extend(_get_exports_list(posix))
    del posix
elif 'nt' in _names:
    name = 'nt'
    linesep = '\r\n'
    from nt import *
    try:
        from nt import _exit
        __all__.append('_exit')
    except ImportError:
        pass
    import ntpath as path
    import nt
    __all__.extend(_get_exports_list(nt))
    del nt
    try:
        from nt import _have_functions
    except ImportError:
        pass
    try:
        from nt import _create_environ
    except ImportError:
        pass
else:
    raise ImportError('no os specific module found')
sys.modules['os.path'] = path
from os.path import curdir, pardir, sep, pathsep, defpath, extsep, altsep, devnull
del _names
if _exists('_have_functions'):
    _globals = globals()

    def _add(str, fn):
        if fn in _globals and str in _have_functions:
            _set.add(_globals[fn])
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    _add('HAVE_FCHMODAT', 'chmod')
    _add('HAVE_FCHOWNAT', 'chown')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_LSTAT', 'lstat')
    _add('HAVE_FUTIMESAT', 'utime')
    _add('HAVE_LINKAT', 'link')
    _add('HAVE_MKDIRAT', 'mkdir')
    _add('HAVE_MKFIFOAT', 'mkfifo')
    _add('HAVE_MKNODAT', 'mknod')
    _add('HAVE_OPENAT', 'open')
    _add('HAVE_READLINKAT', 'readlink')
    _add('HAVE_RENAMEAT', 'rename')
    _add('HAVE_SYMLINKAT', 'symlink')
    _add('HAVE_UNLINKAT', 'unlink')
    _add('HAVE_UNLINKAT', 'rmdir')
    _add('HAVE_UTIMENSAT', 'utime')
    supports_dir_fd = _set
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    supports_effective_ids = _set
    _set = set()
    _add('HAVE_FCHDIR', 'chdir')
    _add('HAVE_FCHMOD', 'chmod')
    _add('MS_WINDOWS', 'chmod')
    _add('HAVE_FCHOWN', 'chown')
    _add('HAVE_FDOPENDIR', 'listdir')
    _add('HAVE_FDOPENDIR', 'scandir')
    _add('HAVE_FEXECVE', 'execve')
    _set.add(stat)
    _add('HAVE_FTRUNCATE', 'truncate')
    _add('HAVE_FUTIMENS', 'utime')
    _add('HAVE_FUTIMES', 'utime')
    _add('HAVE_FPATHCONF', 'pathconf')
    if _exists('statvfs') and _exists('fstatvfs'):
        _add('HAVE_FSTATVFS', 'statvfs')
    supports_fd = _set
    _set = set()
    _add('HAVE_FACCESSAT', 'access')
    _add('HAVE_FCHOWNAT', 'chown')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_LCHFLAGS', 'chflags')
    _add('HAVE_LCHMOD', 'chmod')
    _add('MS_WINDOWS', 'chmod')
    if _exists('lchown'):
        _add('HAVE_LCHOWN', 'chown')
    _add('HAVE_LINKAT', 'link')
    _add('HAVE_LUTIMES', 'utime')
    _add('HAVE_LSTAT', 'stat')
    _add('HAVE_FSTATAT', 'stat')
    _add('HAVE_UTIMENSAT', 'utime')
    _add('MS_WINDOWS', 'stat')
    supports_follow_symlinks = _set
    del _set
    del _have_functions
    del _globals
    del _add
SEEK_SET = 0
SEEK_CUR = 1
SEEK_END = 2

def 递归建目录(name, mode=511, exist_ok=False):
    """makedirs(name [, mode=0o777][, exist_ok=False])

    Super-mkdir; create a leaf directory and all intermediate ones.  Works
    like mkdir, except that any intermediate path segment (not just the
    rightmost) will be created if it does not exist.  If the target
    directory already exists, raise an OSError if exist_ok is False.
    Otherwise no exception is raised.  This is recursive.

    """
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    if head and tail and (not path.exists(head)):
        try:
            递归建目录(head, exist_ok=exist_ok)
        except FileExistsError:
            pass
        cdir = curdir
        if isinstance(tail, bytes):
            cdir = bytes(curdir, 'ASCII')
        if tail == cdir:
            return
    try:
        mkdir(name, mode)
    except OSError:
        if not exist_ok or not path.isdir(name):
            raise

def 递归删目录(name):
    """removedirs(name)

    Super-rmdir; remove a leaf directory and all empty intermediate
    ones.  Works like rmdir except that, if the leaf directory is
    successfully removed, directories corresponding to rightmost path
    segments will be pruned away until either the whole path is
    consumed or an error occurs.  Errors during this latter phase are
    ignored -- they generally mean that a directory was not empty.

    """
    rmdir(name)
    head, tail = path.split(name)
    if not tail:
        head, tail = path.split(head)
    while head and tail:
        try:
            rmdir(head)
        except OSError:
            break
        head, tail = path.split(head)

def 重命名交换(old, new):
    """renames(old, new)

    Super-rename; create directories as necessary and delete any left
    empty.  Works like rename, except creation of any intermediate
    directories needed to make the new pathname good is attempted
    first.  After the rename, directories corresponding to rightmost
    path segments of the old name will be pruned until either the
    whole path is consumed or a nonempty directory is found.

    Note: this function can fail with the new directory structure made
    if you lack permissions needed to unlink the leaf directory or
    file.

    """
    head, tail = path.split(new)
    if head and tail and (not path.exists(head)):
        递归建目录(head)
    rename(old, new)
    head, tail = path.split(old)
    if head and tail:
        try:
            递归删目录(head)
        except OSError:
            pass
__all__.extend(['makedirs', 'removedirs', 'renames'])
_walk_symlinks_as_files = object()

def 遍历目录(top, topdown=True, onerror=None, followlinks=False):
    """Directory tree generator.

    For each directory in the directory tree rooted at top (including top
    itself, but excluding '.' and '..'), yields a 3-tuple

        dirpath, dirnames, filenames

    dirpath is a string, the path to the directory.  dirnames is a list of
    the names of the subdirectories in dirpath (including symlinks to
    directories, and excluding '.' and '..').
    filenames is a list of the names of the non-directory files in dirpath.
    Note that the names in the lists are just names, with no path
    components.  To get a full path (which begins with top) to a file or
    directory in dirpath, do os.path.join(dirpath, name).

    If optional arg 'topdown' is true or not specified, the triple for a
    directory is generated before the triples for any of its subdirectories
    (directories are generated top down).  If topdown is false, the triple
    for a directory is generated after the triples for all of its
    subdirectories (directories are generated bottom up).

    When topdown is true, the caller can modify the dirnames list in-place
    (e.g., via del or slice assignment), and walk will only recurse into the
    subdirectories whose names remain in dirnames; this can be used to prune
    the search, or to impose a specific order of visiting.  Modifying
    dirnames when topdown is false has no effect on the behavior of
    os.walk(), since the directories in dirnames have already been generated
    by the time dirnames itself is generated. No matter the value of
    topdown, the list of subdirectories is retrieved before the tuples for
    the directory and its subdirectories are generated.

    By default errors from the os.scandir() call are ignored.  If
    optional arg 'onerror' is specified, it should be a function; it
    will be called with one argument, an OSError instance.  It can
    report the error to continue with the walk, or raise the exception
    to abort the walk.  Note that the filename is available as the
    filename attribute of the exception object.

    By default, os.walk does not follow symbolic links to subdirectories on
    systems that support them.  In order to get this functionality, set the
    optional argument 'followlinks' to true.

    Caution:  if you pass a relative pathname for top, don't change the
    current working directory between resumptions of walk.  walk never
    changes the current directory, and assumes that the client doesn't
    either.

    Example:

    import os
    from os.path import join, getsize
    for root, dirs, files in os.walk('python/Lib/xml'):
        print(root, "consumes ")
        print(sum(getsize(join(root, name)) for name in files), end=" ")
        print("bytes in", len(files), "non-directory files")
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')  # don't visit __pycache__ directories

    """
    sys.audit('os.walk', top, topdown, onerror, followlinks)
    stack = [fspath(top)]
    islink, join = (path.islink, path.join)
    while stack:
        top = stack.pop()
        if isinstance(top, tuple):
            yield top
            continue
        dirs = []
        nondirs = []
        walk_dirs = []
        try:
            with scandir(top) as entries:
                for entry in entries:
                    try:
                        if followlinks is _walk_symlinks_as_files:
                            is_dir = entry.is_dir(follow_symlinks=False) and (not entry.is_junction())
                        else:
                            is_dir = entry.is_dir()
                    except OSError:
                        is_dir = False
                    if is_dir:
                        dirs.append(entry.name)
                    else:
                        nondirs.append(entry.name)
                    if not topdown and is_dir:
                        if followlinks:
                            walk_into = True
                        else:
                            try:
                                is_symlink = entry.is_symlink()
                            except OSError:
                                is_symlink = False
                            walk_into = not is_symlink
                        if walk_into:
                            walk_dirs.append(entry.path)
        except OSError as error:
            if onerror is not None:
                onerror(error)
            continue
        if topdown:
            yield (top, dirs, nondirs)
            for dirname in reversed(dirs):
                new_path = join(top, dirname)
                if followlinks or not islink(new_path):
                    stack.append(new_path)
        else:
            stack.append((top, dirs, nondirs))
            for new_path in reversed(walk_dirs):
                stack.append(new_path)
__all__.append('walk')
if {open, stat} <= supports_dir_fd and {scandir, stat} <= supports_fd:

    def fwalk(top='.', topdown=True, onerror=None, *, follow_symlinks=False, dir_fd=None):
        """Directory tree generator.

        This behaves exactly like walk(), except that it yields a 4-tuple

            dirpath, dirnames, filenames, dirfd

        `dirpath`, `dirnames` and `filenames` are identical to walk() output,
        and `dirfd` is a file descriptor referring to the directory `dirpath`.

        The advantage of fwalk() over walk() is that it's safe against symlink
        races (when follow_symlinks is False).

        If dir_fd is not None, it should be a file descriptor open to
        a directory, and top should be relative; top will then be relative to
        that directory.  (dir_fd is always supported for fwalk.)

        Caution:
        Since fwalk() yields file descriptors, those are only valid until the
        next iteration step, so you should dup() them if you want to keep them
        for a longer period.

        Example:

        import os
        for root, dirs, files, rootfd in os.fwalk('python/Lib/xml'):
            print(root, "consumes", end="")
            print(sum(os.stat(name, dir_fd=rootfd).st_size for name in files),
                  end="")
            print("bytes in", len(files), "non-directory files")
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')  # don't visit __pycache__ directories
        """
        sys.audit('os.fwalk', top, topdown, onerror, follow_symlinks, dir_fd)
        top = fspath(top)
        stack = [(_fwalk_walk, (True, dir_fd, top, top, None))]
        isbytes = isinstance(top, bytes)
        try:
            while stack:
                yield from _fwalk(stack, isbytes, topdown, onerror, follow_symlinks)
        finally:
            while stack:
                action, value = stack.pop()
                if action == _fwalk_close:
                    close(value)
    _fwalk_walk = 0
    _fwalk_yield = 1
    _fwalk_close = 2

    def _fwalk(stack, isbytes, topdown, onerror, follow_symlinks):
        action, value = stack.pop()
        if action == _fwalk_close:
            close(value)
            return
        elif action == _fwalk_yield:
            yield value
            return
        assert action == _fwalk_walk
        isroot, dirfd, toppath, topname, entry = value
        try:
            if not follow_symlinks:
                if entry is None:
                    orig_st = stat(topname, follow_symlinks=False, dir_fd=dirfd)
                else:
                    orig_st = entry.stat(follow_symlinks=False)
            topfd = open(topname, O_RDONLY | O_NONBLOCK, dir_fd=dirfd)
        except OSError as err:
            if isroot:
                raise
            if onerror is not None:
                onerror(err)
            return
        stack.append((_fwalk_close, topfd))
        if not follow_symlinks:
            if isroot and (not st.S_ISDIR(orig_st.st_mode)):
                return
            if not path.samestat(orig_st, stat(topfd)):
                return
        scandir_it = scandir(topfd)
        dirs = []
        nondirs = []
        entries = None if topdown or follow_symlinks else []
        for entry in scandir_it:
            name = entry.name
            if isbytes:
                name = 编码路径(name)
            try:
                if entry.is_dir():
                    dirs.append(name)
                    if entries is not None:
                        entries.append(entry)
                else:
                    nondirs.append(name)
            except OSError:
                try:
                    if entry.is_symlink():
                        nondirs.append(name)
                except OSError:
                    pass
        if topdown:
            yield (toppath, dirs, nondirs, topfd)
        else:
            stack.append((_fwalk_yield, (toppath, dirs, nondirs, topfd)))
        toppath = path.join(toppath, toppath[:0])
        if entries is None:
            stack.extend(((_fwalk_walk, (False, topfd, toppath + name, name, None)) for name in dirs[::-1]))
        else:
            stack.extend(((_fwalk_walk, (False, topfd, toppath + name, name, entry)) for name, entry in zip(dirs[::-1], entries[::-1])))
    __all__.append('fwalk')

def 执行l(file, *args):
    """execl(file, *args)

    Execute the executable file with argument list args, replacing the
    current process. """
    execv(file, args)

def 执行le(file, *args):
    """execle(file, *args, env)

    Execute the executable file with argument list args and
    environment env, replacing the current process. """
    env = args[-1]
    execve(file, args[:-1], env)

def 执行lp(file, *args):
    """execlp(file, *args)

    Execute the executable file (which is searched for along $PATH)
    with argument list args, replacing the current process. """
    执行vp(file, args)

def 执行lpe(file, *args):
    """execlpe(file, *args, env)

    Execute the executable file (which is searched for along $PATH)
    with argument list args and environment env, replacing the current
    process. """
    env = args[-1]
    执行vpe(file, args[:-1], env)

def 执行vp(file, args):
    """execvp(file, args)

    Execute the executable file (which is searched for along $PATH)
    with argument list args, replacing the current process.
    args may be a list or tuple of strings. """
    _execvpe(file, args)

def 执行vpe(file, args, env):
    """execvpe(file, args, env)

    Execute the executable file (which is searched for along $PATH)
    with argument list args and environment env, replacing the
    current process.
    args may be a list or tuple of strings. """
    _execvpe(file, args, env)
__all__.extend(['execl', 'execle', 'execlp', 'execlpe', 'execvp', 'execvpe'])

def _execvpe(file, args, env=None):
    if env is not None:
        exec_func = execve
        argrest = (args, env)
    else:
        exec_func = execv
        argrest = (args,)
        env = environ
    if path.dirname(file):
        exec_func(file, *argrest)
        return
    saved_exc = None
    path_list = 取执行路径(env)
    if name != 'nt':
        file = 编码路径(file)
        path_list = map(编码路径, path_list)
    for dir in path_list:
        fullname = path.join(dir, file)
        try:
            exec_func(fullname, *argrest)
        except (FileNotFoundError, NotADirectoryError) as e:
            last_exc = e
        except OSError as e:
            last_exc = e
            if saved_exc is None:
                saved_exc = e
    if saved_exc is not None:
        raise saved_exc
    raise last_exc

def 取执行路径(env=None):
    """Returns the sequence of directories that will be searched for the
    named executable (similar to a shell) when launching a process.

    *env* must be an environment variable dict or None.  If *env* is None,
    os.environ will be used.
    """
    import warnings
    if env is None:
        env = environ
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', BytesWarning)
        try:
            path_list = env.get('PATH')
        except TypeError:
            path_list = None
        if supports_bytes_environ:
            try:
                path_listb = env[b'PATH']
            except (KeyError, TypeError):
                pass
            else:
                if path_list is not None:
                    raise ValueError("env cannot contain 'PATH' and b'PATH' keys")
                path_list = path_listb
            if path_list is not None and isinstance(path_list, bytes):
                path_list = 解码路径(path_list)
    if path_list is None:
        path_list = defpath
    return path_list.split(pathsep)
from _collections_abc import MutableMapping, Mapping

class _Environ(MutableMapping):

    def __init__(self, data, encodekey, decodekey, encodevalue, decodevalue):
        self.encodekey = encodekey
        self.decodekey = decodekey
        self.encodevalue = encodevalue
        self.decodevalue = decodevalue
        self._data = data

    def __getitem__(self, key):
        try:
            value = self._data[self.encodekey(key)]
        except KeyError:
            raise KeyError(key) from None
        return self.decodevalue(value)

    def __setitem__(self, key, value):
        key = self.encodekey(key)
        value = self.encodevalue(value)
        putenv(key, value)
        self._data[key] = value

    def __delitem__(self, key):
        encodedkey = self.encodekey(key)
        unsetenv(encodedkey)
        try:
            del self._data[encodedkey]
        except KeyError:
            raise KeyError(key) from None

    def __iter__(self):
        keys = list(self._data)
        for key in keys:
            yield self.decodekey(key)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        formatted_items = ', '.join((f'{self.decodekey(key)!r}: {self.decodevalue(value)!r}' for key, value in self._data.items()))
        return f'environ({{{formatted_items}}})'

    def copy(self):
        return dict(self)

    def setdefault(self, key, value):
        if key not in self:
            self[key] = value
        return self[key]

    def __ior__(self, other):
        self.update(other)
        return self

    def __or__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        new = dict(self)
        new.update(other)
        return new

    def __ror__(self, other):
        if not isinstance(other, Mapping):
            return NotImplemented
        new = dict(other)
        new.update(self)
        return new

def _create_environ_mapping():
    if name == 'nt':

        def check_str(value):
            if not isinstance(value, str):
                raise TypeError('str expected, not %s' % type(value).__name__)
            return value
        encode = check_str
        decode = str

        def encodekey(key):
            return encode(key).upper()
        data = {}
        for key, value in environ.items():
            data[encodekey(key)] = value
    else:
        encoding = sys.getfilesystemencoding()

        def encode(value):
            if not isinstance(value, str):
                raise TypeError('str expected, not %s' % type(value).__name__)
            return value.encode(encoding, 'surrogateescape')

        def decode(value):
            return value.decode(encoding, 'surrogateescape')
        encodekey = encode
        data = environ
    return _Environ(data, encodekey, decode, encode, decode)
environ = _create_environ_mapping()
del _create_environ_mapping
if _exists('_create_environ'):

    def 重载环境():
        data = _create_environ()
        if name == 'nt':
            encodekey = environ.encodekey
            data = {encodekey(key): value for key, value in data.items()}
        env_data = environ._data
        env_data.clear()
        env_data.update(data)
    __all__.append('reload_environ')

def 取环境变量(key, default=None):
    """Get an environment variable, return None if it doesn't exist.
    The optional second argument can specify an alternate default.
    key, default and the result are str."""
    return environ.get(key, default)
supports_bytes_environ = name != 'nt'
__all__.extend(('getenv', 'supports_bytes_environ'))
if supports_bytes_environ:

    def _check_bytes(value):
        if not isinstance(value, bytes):
            raise TypeError('bytes expected, not %s' % type(value).__name__)
        return value
    environb = _Environ(environ._data, _check_bytes, bytes, _check_bytes, bytes)
    del _check_bytes

    def getenvb(key, default=None):
        """Get an environment variable, return None if it doesn't exist.
        The optional second argument can specify an alternate default.
        key, default and the result are bytes."""
        return environb.get(key, default)
    __all__.extend(('environb', 'getenvb'))

def _fscodec():
    encoding = sys.getfilesystemencoding()
    errors = sys.getfilesystemencodeerrors()

    def 编码路径(filename):
        """Encode filename (an os.PathLike, bytes, or str) to the filesystem
        encoding with 'surrogateescape' error handler, return bytes unchanged.
        On Windows, use 'strict' error handler if the file system encoding is
        'mbcs' (which is the default encoding).
        """
        filename = fspath(filename)
        if isinstance(filename, str):
            return filename.encode(encoding, errors)
        else:
            return filename

    def 解码路径(filename):
        """Decode filename (an os.PathLike, bytes, or str) from the filesystem
        encoding with 'surrogateescape' error handler, return str unchanged. On
        Windows, use 'strict' error handler if the file system encoding is
        'mbcs' (which is the default encoding).
        """
        filename = fspath(filename)
        if isinstance(filename, bytes):
            return filename.decode(encoding, errors)
        else:
            return filename
    return (编码路径, 解码路径)
编码路径, 解码路径 = _fscodec()
del _fscodec
if _exists('fork') and (not _exists('spawnv')) and _exists('execv'):
    P_WAIT = 0
    P_NOWAIT = P_NOWAITO = 1
    __all__.extend(['P_WAIT', 'P_NOWAIT', 'P_NOWAITO'])

    def _spawnvef(mode, file, args, env, func):
        if not isinstance(args, (tuple, list)):
            raise TypeError('argv must be a tuple or a list')
        if not args or not args[0]:
            raise ValueError('argv first element cannot be empty')
        pid = fork()
        if not pid:
            try:
                if env is None:
                    func(file, args)
                else:
                    func(file, args, env)
            except:
                _exit(127)
        else:
            if mode == P_NOWAIT:
                return pid
            while 1:
                wpid, sts = waitpid(pid, 0)
                if WIFSTOPPED(sts):
                    continue
                return waitstatus_to_exitcode(sts)

    def spawnv(mode, file, args):
        """spawnv(mode, file, args) -> integer

Execute file with arguments from args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        return _spawnvef(mode, file, args, None, execv)

    def spawnve(mode, file, args, env):
        """spawnve(mode, file, args, env) -> integer

Execute file with arguments from args in a subprocess with the
specified environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        return _spawnvef(mode, file, args, env, execve)

    def spawnvp(mode, file, args):
        """spawnvp(mode, file, args) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        return _spawnvef(mode, file, args, None, 执行vp)

    def spawnvpe(mode, file, args, env):
        """spawnvpe(mode, file, args, env) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        return _spawnvef(mode, file, args, env, 执行vpe)
    __all__.extend(['spawnv', 'spawnve', 'spawnvp', 'spawnvpe'])
if _exists('spawnv'):

    def 派生l(mode, file, *args):
        """spawnl(mode, file, *args) -> integer

Execute file with arguments from args in a subprocess.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        return spawnv(mode, file, args)

    def 派生le(mode, file, *args):
        """spawnle(mode, file, *args, env) -> integer

Execute file with arguments from args in a subprocess with the
supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        env = args[-1]
        return spawnve(mode, file, args[:-1], env)
    __all__.extend(['spawnl', 'spawnle'])
if _exists('spawnvp'):

    def spawnlp(mode, file, *args):
        """spawnlp(mode, file, *args) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        return spawnvp(mode, file, args)

    def spawnlpe(mode, file, *args):
        """spawnlpe(mode, file, *args, env) -> integer

Execute file (which is looked for along $PATH) with arguments from
args in a subprocess with the supplied environment.
If mode == P_NOWAIT return the pid of the process.
If mode == P_WAIT return the process's exit code if it exits normally;
otherwise return -SIG, where SIG is the signal that killed it. """
        env = args[-1]
        return spawnvpe(mode, file, args[:-1], env)
    __all__.extend(['spawnlp', 'spawnlpe'])
if sys.platform != 'vxworks':

    def 管道执行(cmd, mode='r', buffering=-1):
        if not isinstance(cmd, str):
            raise TypeError('invalid cmd type (%s, expected string)' % type(cmd))
        if mode not in ('r', 'w'):
            raise ValueError('invalid mode %r' % mode)
        if buffering == 0 or buffering is None:
            raise ValueError('popen() does not support unbuffered streams')
        import subprocess
        if mode == 'r':
            proc = subprocess.Popen(cmd, shell=True, text=True, stdout=subprocess.PIPE, bufsize=buffering)
            return _wrap_close(proc.stdout, proc)
        else:
            proc = subprocess.Popen(cmd, shell=True, text=True, stdin=subprocess.PIPE, bufsize=buffering)
            return _wrap_close(proc.stdin, proc)

    class _wrap_close:

        def __init__(self, stream, proc):
            self._stream = stream
            self._proc = proc

        def close(self):
            self._stream.close()
            returncode = self._proc.wait()
            if returncode == 0:
                return None
            if name == 'nt':
                return returncode
            else:
                return returncode << 8

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()

        def __getattr__(self, name):
            return getattr(self._stream, name)

        def __iter__(self):
            return iter(self._stream)
    __all__.append('popen')

def 从描述符打开(fd, mode='r', buffering=-1, encoding=None, *args, **kwargs):
    if not isinstance(fd, int):
        raise TypeError('invalid fd type (%s, expected integer)' % type(fd))
    import io
    if 'b' not in mode:
        encoding = io.text_encoding(encoding)
    return io.open(fd, mode, buffering, encoding, *args, **kwargs)

def _fspath(path):
    """Return the path representation of a path-like object.

    If str or bytes is passed in, it is returned unchanged. Otherwise the
    os.PathLike interface is used to get the path representation. If the
    path representation is not str or bytes, TypeError is raised. If the
    provided path is not str, bytes, or os.PathLike, TypeError is raised.
    """
    if isinstance(path, (str, bytes)):
        return path
    path_type = type(path)
    try:
        path_repr = path_type.__fspath__(path)
    except AttributeError:
        if hasattr(path_type, '__fspath__'):
            raise
        else:
            raise TypeError('expected str, bytes or os.PathLike object, not ' + path_type.__name__)
    except TypeError:
        if path_type.__fspath__ is None:
            raise TypeError('expected str, bytes or os.PathLike object, not ' + path_type.__name__) from None
        else:
            raise
    if isinstance(path_repr, (str, bytes)):
        return path_repr
    else:
        raise TypeError('expected {}.__fspath__() to return str or bytes, not {}'.format(path_type.__name__, type(path_repr).__name__))
if not _exists('fspath'):
    fspath = _fspath
    fspath.__name__ = 'fspath'

class 路径类(abc.ABC):
    """Abstract base class for implementing the file system path protocol."""
    __slots__ = ()

    @abc.abstractmethod
    def __fspath__(self):
        """Return the file system path representation of the object."""
        raise NotImplementedError

    @classmethod
    def __subclasshook__(cls, subclass):
        if cls is 路径类:
            return _check_methods(subclass, '__fspath__')
        return NotImplemented
    __class_getitem__ = classmethod(GenericAlias)
if name == 'nt':

    class _AddedDllDirectory:

        def __init__(self, path, cookie, remove_dll_directory):
            self.path = path
            self._cookie = cookie
            self._remove_dll_directory = remove_dll_directory

        def close(self):
            self._remove_dll_directory(self._cookie)
            self.path = None

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.close()

        def __repr__(self):
            if self.path:
                return '<AddedDllDirectory({!r})>'.format(self.path)
            return '<AddedDllDirectory()>'

    def 添加DLL目录(path):
        """Add a path to the DLL search path.

        This search path is used when resolving dependencies for imported
        extension modules (the module itself is resolved through sys.path),
        and also by ctypes.

        Remove the directory by calling close() on the returned object or
        using it in a with statement.
        """
        import nt
        cookie = nt._add_dll_directory(path)
        return _AddedDllDirectory(path, cookie, nt._remove_dll_directory)
if _exists('sched_getaffinity') and sys._get_cpu_count_config() < 0:

    def process_cpu_count():
        """
        Get the number of CPUs of the current process.

        Return the number of logical CPUs usable by the calling thread of the
        current process. Return None if indeterminable.
        """
        return len(sched_getaffinity(0))
else:
    process_cpu_count = cpu_count


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
    'CPU数': 'cpu_count',
    '上级目录': 'pardir',
    '临时文件上限': 'TMP_MAX',
    '关闭': 'close',
    '关闭区间': 'closerange',
    '写': 'write',
    '分隔符': 'sep',
    '切换目录': 'chdir',
    '列出卷': 'listvolumes',
    '列出挂载点': 'listmounts',
    '列出目录': 'listdir',
    '列出驱动器': 'listdrives',
    '删文件': 'unlink',
    '删环境变量': 'unsetenv',
    '删目录': 'rmdir',
    '删除文件': 'remove',
    '取当前目录': 'getcwd',
    '取当前目录字节': 'getcwdb',
    '取文件状态': 'fstat',
    '取时间': 'times',
    '取父进程号': 'getppid',
    '取状态': 'stat',
    '取登录名': 'getlogin',
    '取终端大小': 'get_terminal_size',
    '取路径': 'fspath',
    '取进程号': 'getpid',
    '取链接状态': 'lstat',
    '取阻塞模式': 'get_blocking',
    '句柄可继承吗': 'get_handle_inheritable',
    '可写': 'W_OK',
    '可执行': 'X_OK',
    '可访问吗': 'access',
    '可读': 'R_OK',
    '同步到磁盘': 'fsync',
    '名字': 'name',
    '启动文件': 'startfile',
    '备用分隔符': 'altsep',
    '复制描述符': 'dup',
    '复制描述符到': 'dup2',
    '存在性': 'F_OK',
    '定位当前位置': 'SEEK_CUR',
    '定位末尾': 'SEEK_END',
    '定位起点': 'SEEK_SET',
    '建目录': 'mkdir',
    '建硬链接': 'link',
    '建符号链接': 'symlink',
    '建管道': 'pipe',
    '异常终止': 'abort',
    '当前目录': 'curdir',
    '截断': 'truncate',
    '截断文件': 'ftruncate',
    '打开': 'open',
    '打开不继承': 'O_NOINHERIT',
    '打开临时': 'O_TEMPORARY',
    '打开二进制': 'O_BINARY',
    '打开创建': 'O_CREAT',
    '打开只写': 'O_WRONLY',
    '打开只读': 'O_RDONLY',
    '打开尾接': 'O_APPEND',
    '打开截断': 'O_TRUNC',
    '打开文本': 'O_TEXT',
    '打开独占': 'O_EXCL',
    '打开短命': 'O_SHORT_LIVED',
    '打开读写': 'O_RDWR',
    '打开随机访问': 'O_RANDOM',
    '打开顺序访问': 'O_SEQUENTIAL',
    '执行v': 'execv',
    '执行ve': 'execve',
    '执行命令': 'system',
    '扩展名分隔符': 'extsep',
    '扫描目录': 'scandir',
    '描述符可继承吗': 'get_inheritable',
    '支持字节环境吗': 'supports_bytes_environ',
    '支持描述符': 'supports_fd',
    '支持有效标识': 'supports_effective_ids',
    '支持目录描述符': 'supports_dir_fd',
    '支持跟随符号链接': 'supports_follow_symlinks',
    '改文件权限': 'fchmod',
    '改权限': 'chmod',
    '改链接权限': 'lchmod',
    '文件系统状态结果': 'statvfs_result',
    '时间结果': 'times_result',
    '是终端吗': 'isatty',
    '替换文件': 'replace',
    '正常退出码': 'EX_OK',
    '派生v': 'spawnv',
    '派生ve': 'spawnve',
    '派生不等待': 'P_NOWAIT',
    '派生不等待覆盖': 'P_NOWAITO',
    '派生分离': 'P_DETACH',
    '派生等待': 'P_WAIT',
    '派生覆盖': 'P_OVERLAY',
    '状态结果': 'stat_result',
    '环境': 'environ',
    '目录项': 'DirEntry',
    '移动读写位置': 'lseek',
    '空设备': 'devnull',
    '等待子进程': 'waitpid',
    '等待状态转退出码': 'waitstatus_to_exitcode',
    '系统信息结果': 'uname_result',
    '系统错误': 'error',
    '终止进程': 'kill',
    '终端大小': 'terminal_size',
    '行分隔符': 'linesep',
    '设句柄可继承': 'set_handle_inheritable',
    '设备编码': 'device_encoding',
    '设描述符可继承': 'set_inheritable',
    '设时间': 'utime',
    '设权限掩码': 'umask',
    '设环境变量': 'putenv',
    '设阻塞模式': 'set_blocking',
    '读': 'read',
    '读入缓冲': 'readinto',
    '读链接': 'readlink',
    '路径': 'path',
    '路径分隔符': 'pathsep',
    '进程CPU数': 'process_cpu_count',
    '重命名': 'rename',
    '错误描述': 'strerror',
    '随机字节': 'urandom',
    '默认搜索路径': 'defpath',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'PathLike': '路径类',
    'add_dll_directory': '添加DLL目录',
    'execl': '执行l',
    'execle': '执行le',
    'execlp': '执行lp',
    'execlpe': '执行lpe',
    'execvp': '执行vp',
    'execvpe': '执行vpe',
    'fdopen': '从描述符打开',
    'fsdecode': '解码路径',
    'fsencode': '编码路径',
    'get_exec_path': '取执行路径',
    'getenv': '取环境变量',
    'makedirs': '递归建目录',
    'popen': '管道执行',
    'reload_environ': '重载环境',
    'removedirs': '递归删目录',
    'renames': '重命名交换',
    'spawnl': '派生l',
    'spawnle': '派生le',
    'walk': '遍历目录',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    'CPU数',
    '上级目录',
    '临时文件上限',
    '从描述符打开',
    '关闭',
    '关闭区间',
    '写',
    '分隔符',
    '切换目录',
    '列出卷',
    '列出挂载点',
    '列出目录',
    '列出驱动器',
    '删文件',
    '删环境变量',
    '删目录',
    '删除文件',
    '取当前目录',
    '取当前目录字节',
    '取执行路径',
    '取文件状态',
    '取时间',
    '取父进程号',
    '取状态',
    '取环境变量',
    '取登录名',
    '取终端大小',
    '取路径',
    '取进程号',
    '取链接状态',
    '取阻塞模式',
    '句柄可继承吗',
    '可写',
    '可执行',
    '可访问吗',
    '可读',
    '同步到磁盘',
    '名字',
    '启动文件',
    '备用分隔符',
    '复制描述符',
    '复制描述符到',
    '存在性',
    '定位当前位置',
    '定位末尾',
    '定位起点',
    '建目录',
    '建硬链接',
    '建符号链接',
    '建管道',
    '异常终止',
    '当前目录',
    '截断',
    '截断文件',
    '打开',
    '打开不继承',
    '打开临时',
    '打开二进制',
    '打开创建',
    '打开只写',
    '打开只读',
    '打开尾接',
    '打开截断',
    '打开文本',
    '打开独占',
    '打开短命',
    '打开读写',
    '打开随机访问',
    '打开顺序访问',
    '执行l',
    '执行le',
    '执行lp',
    '执行lpe',
    '执行v',
    '执行ve',
    '执行vp',
    '执行vpe',
    '执行命令',
    '扩展名分隔符',
    '扫描目录',
    '描述符可继承吗',
    '支持字节环境吗',
    '支持描述符',
    '支持有效标识',
    '支持目录描述符',
    '支持跟随符号链接',
    '改文件权限',
    '改权限',
    '改链接权限',
    '文件系统状态结果',
    '时间结果',
    '是终端吗',
    '替换文件',
    '正常退出码',
    '派生l',
    '派生le',
    '派生v',
    '派生ve',
    '派生不等待',
    '派生不等待覆盖',
    '派生分离',
    '派生等待',
    '派生覆盖',
    '状态结果',
    '环境',
    '目录项',
    '移动读写位置',
    '空设备',
    '等待子进程',
    '等待状态转退出码',
    '管道执行',
    '系统信息结果',
    '系统错误',
    '终止进程',
    '终端大小',
    '编码路径',
    '行分隔符',
    '解码路径',
    '设句柄可继承',
    '设备编码',
    '设描述符可继承',
    '设时间',
    '设权限掩码',
    '设环境变量',
    '设阻塞模式',
    '读',
    '读入缓冲',
    '读链接',
    '路径',
    '路径分隔符',
    '进程CPU数',
    '递归删目录',
    '递归建目录',
    '遍历目录',
    '重命名',
    '重命名交换',
    '重载环境',
    '错误描述',
    '随机字节',
    '默认搜索路径',
]

# ---- 转发层结束 ----
