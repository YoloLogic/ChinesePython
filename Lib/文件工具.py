# -*- coding: utf-8 -*-
"""文件工具 —— 汉语库（由 tools/汉化库.py 从 Lib/shutil.py 机械生成，**不要手改**）。

英文库 Lib/shutil.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 文件工具
"""


"""Utility functions for copying and archiving files and directory trees.

XXX The functions here don't copy the resource fork or other metadata on Mac.

"""
import os
import sys
import stat
import fnmatch
import collections
import errno
try:
    import zlib
    del zlib
    _ZLIB_SUPPORTED = True
except ImportError:
    _ZLIB_SUPPORTED = False
try:
    import bz2
    del bz2
    _BZ2_SUPPORTED = True
except ImportError:
    _BZ2_SUPPORTED = False
try:
    import lzma
    del lzma
    _LZMA_SUPPORTED = True
except ImportError:
    _LZMA_SUPPORTED = False
try:
    from compression import zstd
    del zstd
    _ZSTD_SUPPORTED = True
except ImportError:
    _ZSTD_SUPPORTED = False
_WINDOWS = os.name == 'nt'
posix = nt = None
if os.name == 'posix':
    import posix
elif _WINDOWS:
    import nt
if sys.platform == 'win32':
    import _winapi
else:
    _winapi = None
复制缓冲大小 = 1024 * 1024 if _WINDOWS else 256 * 1024
_USE_CP_SENDFILE = hasattr(os, 'sendfile') and sys.platform.startswith(('linux', 'android', 'sunos'))
_USE_CP_COPY_FILE_RANGE = hasattr(os, 'copy_file_range')
_HAS_FCOPYFILE = posix and hasattr(posix, '_fcopyfile')
_WIN_DEFAULT_PATHEXT = '.COM;.EXE;.BAT;.CMD;.VBS;.JS;.WS;.MSC'
__all__ = ['copyfileobj', 'copyfile', 'copymode', 'copystat', 'copy', 'copy2', 'copytree', 'move', 'rmtree', 'Error', 'SpecialFileError', 'make_archive', 'get_archive_formats', 'register_archive_format', 'unregister_archive_format', 'get_unpack_formats', 'register_unpack_format', 'unregister_unpack_format', 'unpack_archive', 'ignore_patterns', 'chown', 'which', 'get_terminal_size', 'SameFileError']

class 错误(OSError):
    pass
import shutil as _英文身份源
错误 = _英文身份源.Error

class 同一文件错误(错误):
    """Raised when source and destination are the same file."""
import shutil as _英文身份源
同一文件错误 = _英文身份源.SameFileError

class 特殊文件错误(OSError):
    """Raised when trying to do a kind of operation (e.g. copying) which is
    not supported on a special file (e.g. a named pipe)"""
import shutil as _英文身份源
特殊文件错误 = _英文身份源.SpecialFileError

class 读错误(OSError):
    """Raised when an archive cannot be read"""
import shutil as _英文身份源
读错误 = _英文身份源.ReadError

class 注册表错误(Exception):
    """Raised when a registry operation with the archiving
    and unpacking registries fails"""
import shutil as _英文身份源
注册表错误 = _英文身份源.RegistryError

class _GiveupOnFastCopy(Exception):
    """Raised as a signal to fallback on using raw read()/write()
    file copy when fast-copy functions fail to do so.
    """

def _fastcopy_fcopyfile(fsrc, fdst, flags):
    """Copy a regular file content or metadata by using high-performance
    fcopyfile(3) syscall (macOS).
    """
    try:
        infd = fsrc.fileno()
        outfd = fdst.fileno()
    except Exception as err:
        raise _GiveupOnFastCopy(err)
    try:
        posix._fcopyfile(infd, outfd, flags)
    except OSError as err:
        err.filename = fsrc.name
        err.filename2 = fdst.name
        if err.errno in {errno.EINVAL, errno.ENOTSUP}:
            raise _GiveupOnFastCopy(err)
        else:
            raise err from None

def _determine_linux_fastcopy_blocksize(infd):
    """Determine blocksize for fastcopying on Linux.

    Hopefully the whole file will be copied in a single call.
    The copying itself should be performed in a loop 'till EOF is
    reached (0 return) so a blocksize smaller or bigger than the actual
    file size should not make any difference, also in case the file
    content changes while being copied.
    """
    try:
        blocksize = max(os.fstat(infd).st_size, 2 ** 23)
    except OSError:
        blocksize = 2 ** 27
    if sys.maxsize < 2 ** 32:
        blocksize = min(blocksize, 2 ** 30)
    return blocksize

def _fastcopy_copy_file_range(fsrc, fdst):
    """Copy data from one regular mmap-like fd to another by using
    a high-performance copy_file_range(2) syscall that gives filesystems
    an opportunity to implement the use of reflinks or server-side copy.

    This should work on Linux >= 4.5 only.
    """
    try:
        infd = fsrc.fileno()
        outfd = fdst.fileno()
    except Exception as err:
        raise _GiveupOnFastCopy(err)
    blocksize = _determine_linux_fastcopy_blocksize(infd)
    offset = 0
    while True:
        try:
            n_copied = os.copy_file_range(infd, outfd, blocksize, offset_dst=offset)
        except OSError as err:
            err.filename = fsrc.name
            err.filename2 = fdst.name
            if err.errno == errno.ENOSPC:
                raise err from None
            if offset == 0 and os.lseek(outfd, 0, os.SEEK_CUR) == 0:
                raise _GiveupOnFastCopy(err)
            raise err
        else:
            if n_copied == 0:
                if offset == 0:
                    raise _GiveupOnFastCopy()
                break
            offset += n_copied

def _fastcopy_sendfile(fsrc, fdst):
    """Copy data from one regular mmap-like fd to another by using
    high-performance sendfile(2) syscall.
    This should work on Linux >= 2.6.33, Android and Solaris.
    """
    global _USE_CP_SENDFILE
    try:
        infd = fsrc.fileno()
        outfd = fdst.fileno()
    except Exception as err:
        raise _GiveupOnFastCopy(err)
    blocksize = _determine_linux_fastcopy_blocksize(infd)
    offset = 0
    while True:
        try:
            sent = os.sendfile(outfd, infd, offset, blocksize)
        except OSError as err:
            err.filename = fsrc.name
            err.filename2 = fdst.name
            if err.errno == errno.ENOTSOCK:
                _USE_CP_SENDFILE = False
                raise _GiveupOnFastCopy(err)
            if err.errno == errno.ENOSPC:
                raise err from None
            if offset == 0 and os.lseek(outfd, 0, os.SEEK_CUR) == 0:
                raise _GiveupOnFastCopy(err)
            raise err
        else:
            if sent == 0:
                break
            offset += sent

def _copyfileobj_readinto(fsrc, fdst, length=复制缓冲大小):
    """readinto()/memoryview() based variant of copyfileobj().
    *fsrc* must support readinto() method and both files must be
    open in binary mode.
    """
    fsrc_readinto = fsrc.readinto
    fdst_write = fdst.write
    with memoryview(bytearray(length)) as mv:
        while True:
            n = fsrc_readinto(mv)
            if not n:
                break
            elif n < length:
                with mv[:n] as smv:
                    fdst_write(smv)
                break
            else:
                fdst_write(mv)

def copyfileobj(fsrc, fdst, length=0):
    """copy data from file-like object fsrc to file-like object fdst"""
    if not length:
        length = 复制缓冲大小
    fsrc_read = fsrc.read
    fdst_write = fdst.write
    while (buf := fsrc_read(length)):
        fdst_write(buf)

def _samefile(src, dst):
    if isinstance(src, os.DirEntry) and hasattr(os.path, 'samestat'):
        try:
            return os.path.samestat(src.stat(), os.stat(dst))
        except OSError:
            return False
    if hasattr(os.path, 'samefile'):
        try:
            return os.path.samefile(src, dst)
        except OSError:
            return False
    return os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst))

def _stat(fn):
    return fn.stat() if isinstance(fn, os.DirEntry) else os.stat(fn)

def _islink(fn):
    return fn.is_symlink() if isinstance(fn, os.DirEntry) else os.path.islink(fn)

def 复制文件(src, dst, *, follow_symlinks=True):
    """Copy data from src to dst in the most efficient way possible.

    If follow_symlinks is not set and src is a symbolic link, a new
    symlink will be created instead of copying the file it points to.

    """
    sys.audit('shutil.copyfile', src, dst)
    if _samefile(src, dst):
        raise 同一文件错误('{!r} and {!r} are the same file'.format(src, dst))
    file_size = 0
    for i, fn in enumerate([src, dst]):
        try:
            st = _stat(fn)
        except OSError:
            pass
        else:
            if stat.S_ISFIFO(st.st_mode):
                fn = fn.path if isinstance(fn, os.DirEntry) else fn
                raise 特殊文件错误('`%s` is a named pipe' % fn)
            if _WINDOWS and i == 0:
                file_size = st.st_size
    if not follow_symlinks and _islink(src):
        os.symlink(os.readlink(src), dst)
    else:
        with open(src, 'rb') as fsrc:
            try:
                with open(dst, 'wb') as fdst:
                    if _HAS_FCOPYFILE:
                        try:
                            _fastcopy_fcopyfile(fsrc, fdst, posix._COPYFILE_DATA)
                            return dst
                        except _GiveupOnFastCopy:
                            pass
                    elif _USE_CP_SENDFILE or _USE_CP_COPY_FILE_RANGE:
                        if _USE_CP_COPY_FILE_RANGE:
                            try:
                                _fastcopy_copy_file_range(fsrc, fdst)
                                return dst
                            except _GiveupOnFastCopy:
                                pass
                        if _USE_CP_SENDFILE:
                            try:
                                _fastcopy_sendfile(fsrc, fdst)
                                return dst
                            except _GiveupOnFastCopy:
                                pass
                    elif _WINDOWS and file_size > 0:
                        _copyfileobj_readinto(fsrc, fdst, min(file_size, 复制缓冲大小))
                        return dst
                    copyfileobj(fsrc, fdst)
            except IsADirectoryError as e:
                if not os.path.exists(dst):
                    raise FileNotFoundError(f'Directory does not exist: {dst}') from e
                else:
                    raise
    return dst

def 复制权限(src, dst, *, follow_symlinks=True):
    """Copy mode bits from src to dst.

    If follow_symlinks is not set, symlinks aren't followed if and only
    if both `src` and `dst` are symlinks.  If `lchmod` isn't available
    (e.g. Linux) this method does nothing.

    """
    sys.audit('shutil.copymode', src, dst)
    if not follow_symlinks and _islink(src) and os.path.islink(dst):
        if hasattr(os, 'lchmod'):
            stat_func, chmod_func = (os.lstat, os.lchmod)
        else:
            return
    else:
        stat_func = _stat
        if os.name == 'nt' and os.path.islink(dst):

            def chmod_func(*args):
                os.chmod(*args, follow_symlinks=True)
        else:
            chmod_func = os.chmod
    st = stat_func(src)
    chmod_func(dst, stat.S_IMODE(st.st_mode))
if hasattr(os, 'listxattr'):

    def _copyxattr(src, dst, *, follow_symlinks=True):
        """Copy extended filesystem attributes from `src` to `dst`.

        Overwrite existing attributes.

        If `follow_symlinks` is false, symlinks won't be followed.

        """
        try:
            names = os.listxattr(src, follow_symlinks=follow_symlinks)
        except OSError as e:
            if e.errno not in (errno.ENOTSUP, errno.ENODATA, errno.EINVAL):
                raise
            return
        for name in names:
            try:
                value = os.getxattr(src, name, follow_symlinks=follow_symlinks)
                os.setxattr(dst, name, value, follow_symlinks=follow_symlinks)
            except OSError as e:
                if e.errno not in (errno.EPERM, errno.ENOTSUP, errno.ENODATA, errno.EINVAL, errno.EACCES):
                    raise
else:

    def _copyxattr(*args, **kwargs):
        pass

def 复制状态(src, dst, *, follow_symlinks=True):
    """Copy file metadata

    Copy the permission bits, last access time, last modification time, and
    flags from `src` to `dst`. On Linux, copystat() also copies the "extended
    attributes" where possible. The file contents, owner, and group are
    unaffected. `src` and `dst` are path-like objects or path names given as
    strings.

    If the optional flag `follow_symlinks` is not set, symlinks aren't
    followed if and only if both `src` and `dst` are symlinks.
    """
    sys.audit('shutil.copystat', src, dst)

    def _nop(*args, ns=None, follow_symlinks=None):
        pass
    follow = follow_symlinks or not (_islink(src) and os.path.islink(dst))
    if follow:

        def lookup(name):
            return getattr(os, name, _nop)
    else:

        def lookup(name):
            fn = getattr(os, name, _nop)
            if fn in os.supports_follow_symlinks:
                return fn
            return _nop
    if isinstance(src, os.DirEntry):
        st = src.stat(follow_symlinks=follow)
    else:
        st = lookup('stat')(src, follow_symlinks=follow)
    mode = stat.S_IMODE(st.st_mode)
    lookup('utime')(dst, ns=(st.st_atime_ns, st.st_mtime_ns), follow_symlinks=follow)
    _copyxattr(src, dst, follow_symlinks=follow)
    try:
        lookup('chmod')(dst, mode, follow_symlinks=follow)
    except NotImplementedError:
        pass
    if hasattr(st, 'st_flags'):
        try:
            lookup('chflags')(dst, st.st_flags, follow_symlinks=follow)
        except OSError as why:
            for err in ('EOPNOTSUPP', 'ENOTSUP'):
                if hasattr(errno, err) and why.errno == getattr(errno, err):
                    break
            else:
                raise

def 复制(src, dst, *, follow_symlinks=True):
    """Copy data and mode bits ("cp src dst"). Return the file's destination.

    The destination may be a directory.

    If follow_symlinks is false, symlinks won't be followed. This
    resembles GNU's "cp -P src dst".

    If source and destination are the same file, a SameFileError will be
    raised.

    """
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    复制文件(src, dst, follow_symlinks=follow_symlinks)
    复制权限(src, dst, follow_symlinks=follow_symlinks)
    return dst

def 复制带元数据(src, dst, *, follow_symlinks=True):
    """Copy data and metadata. Return the file's destination.

    Metadata is copied with copystat(). Please see the copystat function
    for more information.

    The destination may be a directory.

    If follow_symlinks is false, symlinks won't be followed. This
    resembles GNU's "cp -P src dst".
    """
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    if hasattr(_winapi, 'CopyFile2'):
        src_ = os.fsdecode(src)
        dst_ = os.fsdecode(dst)
        flags = _winapi.COPY_FILE_ALLOW_DECRYPTED_DESTINATION
        if not follow_symlinks:
            flags |= _winapi.COPY_FILE_COPY_SYMLINK
        try:
            _winapi.CopyFile2(src_, dst_, flags)
            return dst
        except OSError as exc:
            if exc.winerror == _winapi.ERROR_PRIVILEGE_NOT_HELD and (not follow_symlinks):
                pass
            elif exc.winerror == _winapi.ERROR_ACCESS_DENIED:
                pass
            else:
                raise
    复制文件(src, dst, follow_symlinks=follow_symlinks)
    复制状态(src, dst, follow_symlinks=follow_symlinks)
    return dst

def 忽略匹配(*patterns):
    """Function that can be used as copytree() ignore parameter.

    Patterns is a sequence of glob-style patterns
    that are used to exclude files"""

    def _ignore_patterns(path, names):
        ignored_names = []
        for pattern in patterns:
            ignored_names.extend(fnmatch.filter(names, pattern))
        return set(ignored_names)
    return _ignore_patterns

def _copytree(entries, src, dst, symlinks, ignore, copy_function, ignore_dangling_symlinks, dirs_exist_ok=False):
    if ignore is not None:
        ignored_names = ignore(os.fspath(src), [x.name for x in entries])
    else:
        ignored_names = ()
    os.makedirs(dst, exist_ok=dirs_exist_ok)
    errors = []
    use_srcentry = copy_function is 复制带元数据 or copy_function is 复制
    for srcentry in entries:
        if srcentry.name in ignored_names:
            continue
        srcname = os.path.join(src, srcentry.name)
        dstname = os.path.join(dst, srcentry.name)
        srcobj = srcentry if use_srcentry else srcname
        try:
            is_symlink = srcentry.is_symlink()
            if is_symlink and os.name == 'nt':
                lstat = srcentry.stat(follow_symlinks=False)
                if lstat.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT:
                    is_symlink = False
            if is_symlink:
                linkto = os.readlink(srcname)
                if symlinks:
                    os.symlink(linkto, dstname)
                    复制状态(srcobj, dstname, follow_symlinks=not symlinks)
                else:
                    if not os.path.exists(linkto) and ignore_dangling_symlinks:
                        continue
                    if srcentry.is_dir():
                        复制树(srcobj, dstname, symlinks, ignore, copy_function, ignore_dangling_symlinks, dirs_exist_ok)
                    else:
                        copy_function(srcobj, dstname)
            elif srcentry.is_dir():
                复制树(srcobj, dstname, symlinks, ignore, copy_function, ignore_dangling_symlinks, dirs_exist_ok)
            else:
                copy_function(srcobj, dstname)
        except 错误 as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
    try:
        复制状态(src, dst)
    except OSError as why:
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))
    if errors:
        raise 错误(errors)
    return dst

def 复制树(src, dst, symlinks=False, ignore=None, copy_function=复制带元数据, ignore_dangling_symlinks=False, dirs_exist_ok=False):
    """Recursively copy a directory tree and return the destination directory.

    If exception(s) occur, an Error is raised with a list of reasons.

    If the optional symlinks flag is true, symbolic links in the
    source tree result in symbolic links in the destination tree; if
    it is false, the contents of the files pointed to by symbolic
    links are copied. If the file pointed to by the symlink doesn't
    exist, an exception will be added in the list of errors raised in
    an Error exception at the end of the copy process.

    You can set the optional ignore_dangling_symlinks flag to true if you
    want to silence this exception. Notice that this has no effect on
    platforms that don't support os.symlink.

    The optional ignore argument is a callable. If given, it
    is called with the `src` parameter, which is the directory
    being visited by copytree(), and `names` which is the list of
    `src` contents, as returned by os.listdir():

        callable(src, names) -> ignored_names

    Since copytree() is called recursively, the callable will be
    called once for each directory that is copied. It returns a
    list of names relative to the `src` directory that should
    not be copied.

    The optional copy_function argument is a callable that will be used
    to copy each file. It will be called with the source path and the
    destination path as arguments. By default, copy2() is used, but any
    function that supports the same signature (like copy()) can be used.

    If dirs_exist_ok is false (the default) and `dst` already exists, a
    `FileExistsError` is raised. If `dirs_exist_ok` is true, the copying
    operation will continue if it encounters existing directories, and files
    within the `dst` tree will be overwritten by corresponding files from the
    `src` tree.
    """
    sys.audit('shutil.copytree', src, dst)
    with os.scandir(src) as itr:
        entries = list(itr)
    return _copytree(entries=entries, src=src, dst=dst, symlinks=symlinks, ignore=ignore, copy_function=copy_function, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)
if hasattr(os.stat_result, 'st_file_attributes'):

    def _rmtree_islink(st):
        return stat.S_ISLNK(st.st_mode) or (st.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT and st.st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT)
else:

    def _rmtree_islink(st):
        return stat.S_ISLNK(st.st_mode)

def _rmtree_unsafe(path, dir_fd, onexc):
    if dir_fd is not None:
        raise NotImplementedError('dir_fd unavailable on this platform')
    try:
        st = os.lstat(path)
    except OSError as err:
        onexc(os.lstat, path, err)
        return
    try:
        if _rmtree_islink(st):
            raise OSError('Cannot call rmtree on a symbolic link')
    except OSError as err:
        onexc(os.path.islink, path, err)
        return

    def onerror(err):
        if not isinstance(err, FileNotFoundError):
            onexc(os.scandir, err.filename, err)
    results = os.walk(path, topdown=False, onerror=onerror, followlinks=os._walk_symlinks_as_files)
    for dirpath, dirnames, filenames in results:
        for name in dirnames:
            fullname = os.path.join(dirpath, name)
            try:
                os.rmdir(fullname)
            except FileNotFoundError:
                continue
            except OSError as err:
                onexc(os.rmdir, fullname, err)
        for name in filenames:
            fullname = os.path.join(dirpath, name)
            try:
                os.unlink(fullname)
            except FileNotFoundError:
                continue
            except OSError as err:
                onexc(os.unlink, fullname, err)
    try:
        os.rmdir(path)
    except FileNotFoundError:
        pass
    except OSError as err:
        onexc(os.rmdir, path, err)

def _rmtree_safe_fd(path, dir_fd, onexc):
    if isinstance(path, bytes):
        path = os.fsdecode(path)
    stack = [(os.lstat, dir_fd, path, None)]
    try:
        while stack:
            _rmtree_safe_fd_step(stack, onexc)
    finally:
        while stack:
            func, fd, path, entry = stack.pop()
            if func is not os.close:
                continue
            try:
                os.close(fd)
            except OSError as err:
                onexc(os.close, path, err)

def _rmtree_safe_fd_step(stack, onexc):
    func, dirfd, path, orig_entry = stack.pop()
    name = path if orig_entry is None else orig_entry.name
    try:
        if func is os.close:
            os.close(dirfd)
            return
        if func is os.rmdir:
            os.rmdir(name, dir_fd=dirfd)
            return
        assert func is os.lstat
        if orig_entry is None:
            orig_st = os.lstat(name, dir_fd=dirfd)
        else:
            orig_st = orig_entry.stat(follow_symlinks=False)
        func = os.open
        topfd = os.open(name, os.O_RDONLY | os.O_NONBLOCK, dir_fd=dirfd)
        func = os.path.islink
        try:
            if not os.path.samestat(orig_st, os.fstat(topfd)):
                raise OSError('Cannot call rmtree on a symbolic link')
            stack.append((os.rmdir, dirfd, path, orig_entry))
        finally:
            stack.append((os.close, topfd, path, orig_entry))
        func = os.scandir
        with os.scandir(topfd) as scandir_it:
            entries = list(scandir_it)
        for entry in entries:
            fullname = os.path.join(path, entry.name)
            try:
                if entry.is_dir(follow_symlinks=False):
                    stack.append((os.lstat, topfd, fullname, entry))
                    continue
            except FileNotFoundError:
                continue
            except OSError:
                pass
            try:
                os.unlink(entry.name, dir_fd=topfd)
            except FileNotFoundError:
                continue
            except OSError as err:
                onexc(os.unlink, fullname, err)
    except FileNotFoundError as err:
        if orig_entry is None or func is os.close:
            err.filename = path
            onexc(func, path, err)
    except OSError as err:
        err.filename = path
        onexc(func, path, err)
_use_fd_functions = {os.open, os.stat, os.unlink, os.rmdir} <= os.supports_dir_fd and os.scandir in os.supports_fd and (os.stat in os.supports_follow_symlinks)
_rmtree_impl = _rmtree_safe_fd if _use_fd_functions else _rmtree_unsafe

def 删目录树(path, ignore_errors=False, onerror=None, *, onexc=None, dir_fd=None):
    """Recursively delete a directory tree.

    If dir_fd is not None, it should be a file descriptor open to a directory;
    path will then be relative to that directory.
    dir_fd may not be implemented on your platform.
    If it is unavailable, using it will raise a NotImplementedError.

    If ignore_errors is set, errors are ignored; otherwise, if onexc or
    onerror is set, it is called to handle the error with arguments (func,
    path, exc_info) where func is platform and implementation dependent;
    path is the argument to that function that caused it to fail; and
    the value of exc_info describes the exception. For onexc it is the
    exception instance, and for onerror it is a tuple as returned by
    sys.exc_info().  If ignore_errors is false and both onexc and
    onerror are None, the exception is reraised.

    onerror is deprecated and only remains for backwards compatibility.
    If both onerror and onexc are set, onerror is ignored and onexc is used.
    """
    sys.audit('shutil.rmtree', path, dir_fd)
    if ignore_errors:

        def onexc(*args):
            pass
    elif onerror is None and onexc is None:

        def onexc(*args):
            raise
    elif onexc is None:
        if onerror is None:

            def onexc(*args):
                raise
        else:

            def onexc(*args):
                func, path, exc = args
                if exc is None:
                    exc_info = (None, None, None)
                else:
                    exc_info = (type(exc), exc, exc.__traceback__)
                return onerror(func, path, exc_info)
    _rmtree_impl(path, dir_fd, onexc)
删目录树.avoids_symlink_attacks = _use_fd_functions

def _basename(path):
    """A basename() variant which first strips the trailing slash, if present.
    Thus we always get the last component of the path, even for directories.

    path: Union[PathLike, str]

    e.g.
    >>> os.path.basename('/bar/foo')
    'foo'
    >>> os.path.basename('/bar/foo/')
    ''
    >>> _basename('/bar/foo/')
    'foo'
    """
    path = os.fspath(path)
    sep = os.path.sep + (os.path.altsep or '')
    return os.path.basename(path.rstrip(sep))

def 移动(src, dst, copy_function=复制带元数据):
    """Recursively move a file or directory to another location. This is
    similar to the Unix "mv" command. Return the file or directory's
    destination.

    If dst is an existing directory or a symlink to a directory, then src is
    moved inside that directory. The destination path in that directory must
    not already exist.

    If dst already exists but is not a directory, it may be overwritten
    depending on os.rename() semantics.

    os.rename() is preferably used if the source and destination are on the
    same filesystem. In case os.rename() fails due to OSError (e.g. the user
    has write permission to *dst* file but not to its parent directory),
    this method falls back to using *copy_function* silently.
    Symlinks are also recreated under the new name if os.rename() fails
    because of cross filesystem renames.

    It's recommended to use os.rename() if atomic move is strictly required.

    The optional `copy_function` argument is a callable that will be used
    to copy the source or it will be delegated to `copytree`.
    By default, copy2() is used, but any function that supports the same
    signature (like copy()) can be used.

    A lot more could be done here...  A look at a mv.c shows a lot of
    the issues this implementation glosses over.

    """
    sys.audit('shutil.move', src, dst)
    real_dst = dst
    if os.path.isdir(dst):
        if _samefile(src, dst) and (not os.path.islink(src)):
            os.rename(src, dst)
            return
        real_dst = os.path.join(dst, _basename(src))
        if os.path.exists(real_dst):
            raise 错误("Destination path '%s' already exists" % real_dst)
    try:
        os.rename(src, real_dst)
    except OSError:
        if os.path.islink(src):
            linkto = os.readlink(src)
            os.symlink(linkto, real_dst)
            os.unlink(src)
        elif os.path.isdir(src):
            if _destinsrc(src, dst):
                raise 错误("Cannot move a directory '%s' into itself '%s'." % (src, dst))
            if _is_immutable(src) or (not os.access(src, os.W_OK) and os.listdir(src) and (sys.platform == 'darwin')):
                raise PermissionError("Cannot move the non-empty directory '%s': Lacking write permission to '%s'." % (src, src))
            复制树(src, real_dst, copy_function=copy_function, symlinks=True)
            删目录树(src)
        else:
            copy_function(src, real_dst)
            os.unlink(src)
    return real_dst

def _destinsrc(src, dst):
    src = os.path.realpath(src)
    dst = os.path.realpath(dst)
    if not src.endswith(os.path.sep):
        src += os.path.sep
    if not dst.endswith(os.path.sep):
        dst += os.path.sep
    return dst.startswith(src)

def _is_immutable(src):
    st = _stat(src)
    immutable_states = [stat.UF_IMMUTABLE, stat.SF_IMMUTABLE]
    return hasattr(st, 'st_flags') and st.st_flags in immutable_states

def _get_gid(name):
    """Returns a gid, given a group name."""
    if name is None:
        return None
    try:
        from grp import getgrnam
    except ImportError:
        return None
    try:
        result = getgrnam(name)
    except KeyError:
        result = None
    if result is not None:
        return result[2]
    return None

def _get_uid(name):
    """Returns an uid, given a user name."""
    if name is None:
        return None
    try:
        from pwd import getpwnam
    except ImportError:
        return None
    try:
        result = getpwnam(name)
    except KeyError:
        result = None
    if result is not None:
        return result[2]
    return None

def _make_tarball(base_name, base_dir, compress='gzip', verbose=0, dry_run=0, owner=None, group=None, logger=None, root_dir=None):
    """Create a (possibly compressed) tar file from all the files under
    'base_dir'.

    'compress' must be "gzip" (the default), "bzip2", "xz", "zst", or None.

    'owner' and 'group' can be used to define an owner and a group for the
    archive that is being built. If not provided, the current owner and group
    will be used.

    The output tar file will be named 'base_name' +  ".tar", possibly plus
    the appropriate compression extension (".gz", ".bz2", ".xz", or ".zst").

    Returns the output filename.
    """
    if compress is None:
        tar_compression = ''
    elif _ZLIB_SUPPORTED and compress == 'gzip':
        tar_compression = 'gz'
    elif _BZ2_SUPPORTED and compress == 'bzip2':
        tar_compression = 'bz2'
    elif _LZMA_SUPPORTED and compress == 'xz':
        tar_compression = 'xz'
    elif _ZSTD_SUPPORTED and compress == 'zst':
        tar_compression = 'zst'
    else:
        raise ValueError("bad value for 'compress', or compression format not supported : {0}".format(compress))
    import tarfile
    compress_ext = '.' + tar_compression if compress else ''
    archive_name = base_name + '.tar' + compress_ext
    archive_dir = os.path.dirname(archive_name)
    if archive_dir and (not os.path.exists(archive_dir)):
        if logger is not None:
            logger.info('creating %s', archive_dir)
        if not dry_run:
            os.makedirs(archive_dir)
    if logger is not None:
        logger.info('Creating tar archive')
    uid = _get_uid(owner)
    gid = _get_gid(group)

    def _set_uid_gid(tarinfo):
        if gid is not None:
            tarinfo.gid = gid
            tarinfo.gname = group
        if uid is not None:
            tarinfo.uid = uid
            tarinfo.uname = owner
        return tarinfo
    if not dry_run:
        tar = tarfile.open(archive_name, 'w|%s' % tar_compression)
        arcname = base_dir
        if root_dir is not None:
            base_dir = os.path.join(root_dir, base_dir)
        try:
            tar.add(base_dir, arcname, filter=_set_uid_gid)
        finally:
            tar.close()
    if root_dir is not None:
        archive_name = os.path.abspath(archive_name)
    return archive_name

def _make_zipfile(base_name, base_dir, verbose=0, dry_run=0, logger=None, owner=None, group=None, root_dir=None):
    """Create a zip file from all the files under 'base_dir'.

    The output zip file will be named 'base_name' + ".zip".  Returns the
    name of the output zip file.
    """
    import zipfile
    zip_filename = base_name + '.zip'
    archive_dir = os.path.dirname(base_name)
    if archive_dir and (not os.path.exists(archive_dir)):
        if logger is not None:
            logger.info('creating %s', archive_dir)
        if not dry_run:
            os.makedirs(archive_dir)
    if logger is not None:
        logger.info("creating '%s' and adding '%s' to it", zip_filename, base_dir)
    if not dry_run:
        with zipfile.ZipFile(zip_filename, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            arcname = os.path.normpath(base_dir)
            if root_dir is not None:
                base_dir = os.path.join(root_dir, base_dir)
            base_dir = os.path.normpath(base_dir)
            if arcname != os.curdir:
                zf.write(base_dir, arcname)
                if logger is not None:
                    logger.info("adding '%s'", base_dir)
            for dirpath, dirnames, filenames in os.walk(base_dir):
                arcdirpath = dirpath
                if root_dir is not None:
                    arcdirpath = os.path.relpath(arcdirpath, root_dir)
                arcdirpath = os.path.normpath(arcdirpath)
                for name in sorted(dirnames):
                    path = os.path.join(dirpath, name)
                    arcname = os.path.join(arcdirpath, name)
                    zf.write(path, arcname)
                    if logger is not None:
                        logger.info("adding '%s'", path)
                for name in filenames:
                    path = os.path.join(dirpath, name)
                    path = os.path.normpath(path)
                    if os.path.isfile(path):
                        arcname = os.path.join(arcdirpath, name)
                        zf.write(path, arcname)
                        if logger is not None:
                            logger.info("adding '%s'", path)
    if root_dir is not None:
        zip_filename = os.path.abspath(zip_filename)
    return zip_filename
_make_tarball.supports_root_dir = True
_make_zipfile.supports_root_dir = True
_ARCHIVE_FORMATS = {'tar': (_make_tarball, [('compress', None)], 'uncompressed tar file')}
if _ZLIB_SUPPORTED:
    _ARCHIVE_FORMATS['gztar'] = (_make_tarball, [('compress', 'gzip')], "gzip'ed tar-file")
    _ARCHIVE_FORMATS['zip'] = (_make_zipfile, [], 'ZIP file')
if _BZ2_SUPPORTED:
    _ARCHIVE_FORMATS['bztar'] = (_make_tarball, [('compress', 'bzip2')], "bzip2'ed tar-file")
if _LZMA_SUPPORTED:
    _ARCHIVE_FORMATS['xztar'] = (_make_tarball, [('compress', 'xz')], "xz'ed tar-file")
if _ZSTD_SUPPORTED:
    _ARCHIVE_FORMATS['zstdtar'] = (_make_tarball, [('compress', 'zst')], "zstd'ed tar-file")

def 取归档格式():
    """Returns a list of supported formats for archiving and unarchiving.

    Each element of the returned sequence is a tuple (name, description)
    """
    formats = [(name, registry[2]) for name, registry in _ARCHIVE_FORMATS.items()]
    formats.sort()
    return formats

def 登记归档格式(name, function, extra_args=None, description=''):
    """Registers an archive format.

    name is the name of the format. function is the callable that will be
    used to create archives. If provided, extra_args is a sequence of
    (name, value) tuples that will be passed as arguments to the callable.
    description can be provided to describe the format, and will be returned
    by the get_archive_formats() function.
    """
    if extra_args is None:
        extra_args = []
    if not callable(function):
        raise TypeError('The %s object is not callable' % function)
    if not isinstance(extra_args, (tuple, list)):
        raise TypeError('extra_args needs to be a sequence')
    for element in extra_args:
        if not isinstance(element, (tuple, list)) or len(element) != 2:
            raise TypeError('extra_args elements are : (arg_name, value)')
    _ARCHIVE_FORMATS[name] = (function, extra_args, description)

def 注销归档格式(name):
    del _ARCHIVE_FORMATS[name]

def 造归档(base_name, format, root_dir=None, base_dir=None, verbose=0, dry_run=0, owner=None, group=None, logger=None):
    """Create an archive file (eg. zip or tar).

    'base_name' is the name of the file to create, minus any format-specific
    extension; 'format' is the archive format: one of "zip", "tar", "gztar",
    "bztar", "xztar", or "zstdtar".  Or any other registered format.

    'root_dir' is a directory that will be the root directory of the
    archive; ie. we typically chdir into 'root_dir' before creating the
    archive.  'base_dir' is the directory where we start archiving from;
    ie. 'base_dir' will be the common prefix of all files and
    directories in the archive.  'root_dir' and 'base_dir' both default
    to the current directory.  Returns the name of the archive file.

    'owner' and 'group' are used when creating a tar archive. By default,
    uses the current owner and group.
    """
    sys.audit('shutil.make_archive', base_name, format, root_dir, base_dir)
    try:
        format_info = _ARCHIVE_FORMATS[format]
    except KeyError:
        raise ValueError("unknown archive format '%s'" % format) from None
    kwargs = {'dry_run': dry_run, 'logger': logger, 'owner': owner, 'group': group}
    func = format_info[0]
    for arg, val in format_info[1]:
        kwargs[arg] = val
    if base_dir is None:
        base_dir = os.curdir
    supports_root_dir = getattr(func, 'supports_root_dir', False)
    save_cwd = None
    if root_dir is not None:
        stmd = os.stat(root_dir).st_mode
        if not stat.S_ISDIR(stmd):
            raise NotADirectoryError(errno.ENOTDIR, 'Not a directory', root_dir)
        if supports_root_dir:
            base_name = os.fspath(base_name)
            kwargs['root_dir'] = root_dir
        else:
            save_cwd = os.getcwd()
            if logger is not None:
                logger.debug("changing into '%s'", root_dir)
            base_name = os.path.abspath(base_name)
            if not dry_run:
                os.chdir(root_dir)
    try:
        filename = func(base_name, base_dir, **kwargs)
    finally:
        if save_cwd is not None:
            if logger is not None:
                logger.debug("changing back to '%s'", save_cwd)
            os.chdir(save_cwd)
    return filename

def 取解包格式():
    """Returns a list of supported formats for unpacking.

    Each element of the returned sequence is a tuple
    (name, extensions, description)
    """
    formats = [(name, info[0], info[3]) for name, info in _UNPACK_FORMATS.items()]
    formats.sort()
    return formats

def _check_unpack_options(extensions, function, extra_args):
    """Checks what gets registered as an unpacker."""
    existing_extensions = {}
    for name, info in _UNPACK_FORMATS.items():
        for ext in info[0]:
            existing_extensions[ext] = name
    for extension in extensions:
        if extension in existing_extensions:
            msg = '%s is already registered for "%s"'
            raise 注册表错误(msg % (extension, existing_extensions[extension]))
    if not callable(function):
        raise TypeError('The registered function must be a callable')

def 登记解包格式(name, extensions, function, extra_args=None, description=''):
    """Registers an unpack format.

    `name` is the name of the format. `extensions` is a list of extensions
    corresponding to the format.

    `function` is the callable that will be
    used to unpack archives. The callable will receive archives to unpack.
    If it's unable to handle an archive, it needs to raise a ReadError
    exception.

    If provided, `extra_args` is a sequence of
    (name, value) tuples that will be passed as arguments to the callable.
    description can be provided to describe the format, and will be returned
    by the get_unpack_formats() function.
    """
    if extra_args is None:
        extra_args = []
    _check_unpack_options(extensions, function, extra_args)
    _UNPACK_FORMATS[name] = (extensions, function, extra_args, description)

def 注销解包格式(name):
    """Removes the pack format from the registry."""
    del _UNPACK_FORMATS[name]

def _ensure_directory(path):
    """Ensure that the parent directory of `path` exists"""
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

def _unpack_zipfile(filename, extract_dir):
    """Unpack zip `filename` to `extract_dir`
    """
    import zipfile
    if not zipfile.is_zipfile(filename):
        raise 读错误('%s is not a zip file' % filename)
    with zipfile.ZipFile(filename) as zip:
        zip._ignore_invalid_names = True
        zip.extractall(extract_dir)

def _unpack_tarfile(filename, extract_dir, *, filter=None):
    """Unpack tar/tar.gz/tar.bz2/tar.xz/tar.zst `filename` to `extract_dir`
    """
    import tarfile
    try:
        tarobj = tarfile.open(filename)
    except tarfile.TarError:
        raise 读错误('%s is not a compressed or uncompressed tar file' % filename)
    try:
        tarobj.extractall(extract_dir, filter=filter)
    finally:
        tarobj.close()
_UNPACK_FORMATS = {'tar': (['.tar'], _unpack_tarfile, [], 'uncompressed tar file'), 'zip': (['.zip'], _unpack_zipfile, [], 'ZIP file')}
if _ZLIB_SUPPORTED:
    _UNPACK_FORMATS['gztar'] = (['.tar.gz', '.tgz'], _unpack_tarfile, [], "gzip'ed tar-file")
if _BZ2_SUPPORTED:
    _UNPACK_FORMATS['bztar'] = (['.tar.bz2', '.tbz2'], _unpack_tarfile, [], "bzip2'ed tar-file")
if _LZMA_SUPPORTED:
    _UNPACK_FORMATS['xztar'] = (['.tar.xz', '.txz'], _unpack_tarfile, [], "xz'ed tar-file")
if _ZSTD_SUPPORTED:
    _UNPACK_FORMATS['zstdtar'] = (['.tar.zst', '.tzst'], _unpack_tarfile, [], "zstd'ed tar-file")

def _find_unpack_format(filename):
    for name, info in _UNPACK_FORMATS.items():
        for extension in info[0]:
            if filename.endswith(extension):
                return name
    return None

def 解归档(filename, extract_dir=None, format=None, *, filter=None):
    """Unpack an archive.

    `filename` is the name of the archive.

    `extract_dir` is the name of the target directory, where the archive
    is unpacked. If not provided, the current working directory is used.

    `format` is the archive format: one of "zip", "tar", "gztar", "bztar",
    "xztar", or "zstdtar".  Or any other registered format.  If not provided,
    unpack_archive will use the filename extension and see if an unpacker
    was registered for that extension.

    In case none is found, a ValueError is raised.

    If `filter` is given, it is passed to the underlying
    extraction function.
    """
    sys.audit('shutil.unpack_archive', filename, extract_dir, format)
    if extract_dir is None:
        extract_dir = os.getcwd()
    extract_dir = os.fspath(extract_dir)
    filename = os.fspath(filename)
    if filter is None:
        filter_kwargs = {}
    else:
        filter_kwargs = {'filter': filter}
    if format is not None:
        try:
            format_info = _UNPACK_FORMATS[format]
        except KeyError:
            raise ValueError("Unknown unpack format '{0}'".format(format)) from None
        func = format_info[1]
        func(filename, extract_dir, **dict(format_info[2]), **filter_kwargs)
    else:
        format = _find_unpack_format(filename)
        if format is None:
            raise 读错误("Unknown archive format '{0}'".format(filename))
        func = _UNPACK_FORMATS[format][1]
        kwargs = dict(_UNPACK_FORMATS[format][2]) | filter_kwargs
        func(filename, extract_dir, **kwargs)
if hasattr(os, 'statvfs'):
    __all__.append('disk_usage')
    _ntuple_diskusage = collections.namedtuple('usage', 'total used free')
    _ntuple_diskusage.total.__doc__ = 'Total space in bytes'
    _ntuple_diskusage.used.__doc__ = 'Used space in bytes'
    _ntuple_diskusage.free.__doc__ = 'Free space in bytes'

    def 磁盘用量(path):
        """Return disk usage statistics about the given path.

        Returned value is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)
elif _WINDOWS:
    __all__.append('disk_usage')
    _ntuple_diskusage = collections.namedtuple('usage', 'total used free')

    def 磁盘用量(path):
        """Return disk usage statistics about the given path.

        Returned values is a named tuple with attributes 'total', 'used' and
        'free', which are the amount of total, used and free space, in bytes.
        """
        total, free = nt._getdiskusage(path)
        used = total - free
        return _ntuple_diskusage(total, used, free)

def 改属主(path, user=None, group=None, *, dir_fd=None, follow_symlinks=True):
    """Change owner user and group of the given path.

    user and group can be the uid/gid or the user/group names, and in that case,
    they are converted to their respective uid/gid.

    If dir_fd is set, it should be an open file descriptor to the directory to
    be used as the root of *path* if it is relative.

    If follow_symlinks is set to False and the last element of the path is a
    symbolic link, chown will modify the link itself and not the file being
    referenced by the link.
    """
    sys.audit('shutil.chown', path, user, group)
    if user is None and group is None:
        raise ValueError('user and/or group must be set')
    _user = user
    _group = group
    if user is None:
        _user = -1
    elif isinstance(user, str):
        _user = _get_uid(user)
        if _user is None:
            raise LookupError('no such user: {!r}'.format(user))
    if group is None:
        _group = -1
    elif not isinstance(group, int):
        _group = _get_gid(group)
        if _group is None:
            raise LookupError('no such group: {!r}'.format(group))
    os.chown(path, _user, _group, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

def 取终端大小(fallback=(80, 24)):
    """Get the size of the terminal window.

    For each of the two dimensions, the environment variable, COLUMNS
    and LINES respectively, is checked. If the variable is defined and
    the value is a positive integer, it is used.

    When COLUMNS or LINES is not defined, which is the common case,
    the terminal connected to sys.__stdout__ is queried
    by invoking os.get_terminal_size.

    If the terminal size cannot be successfully queried, either because
    the system doesn't support querying, or because we are not
    connected to a terminal, the value given in fallback parameter
    is used. Fallback defaults to (80, 24) which is the default
    size used by many terminal emulators.

    The value returned is a named tuple of type os.terminal_size.
    """
    try:
        columns = int(os.environ['COLUMNS'])
    except (KeyError, ValueError):
        columns = 0
    try:
        lines = int(os.environ['LINES'])
    except (KeyError, ValueError):
        lines = 0
    if columns <= 0 or lines <= 0:
        try:
            size = os.get_terminal_size(sys.__stdout__.fileno())
        except (AttributeError, ValueError, OSError):
            size = os.terminal_size(fallback)
        if columns <= 0:
            columns = size.columns or fallback[0]
        if lines <= 0:
            lines = size.lines or fallback[1]
    return os.terminal_size((columns, lines))

def _access_check(fn, mode):
    return os.path.exists(fn) and os.access(fn, mode) and (not os.path.isdir(fn))

def _win_path_needs_curdir(cmd, mode):
    """
    On Windows, we can use NeedCurrentDirectoryForExePath to figure out
    if we should add the cwd to PATH when searching for executables if
    the mode is executable.
    """
    return not mode & os.X_OK or _winapi.NeedCurrentDirectoryForExePath(os.fsdecode(cmd))

def 找可执行文件(cmd, mode=os.F_OK | os.X_OK, path=None):
    """Given a command, mode, and a PATH string, return the path which
    conforms to the given mode on the PATH, or None if there is no such
    file.

    `mode` defaults to os.F_OK | os.X_OK. `path` defaults to the result
    of os.environ.get("PATH"), or can be overridden with a custom search
    path.

    """
    use_bytes = isinstance(cmd, bytes)
    dirname, cmd = os.path.split(cmd)
    if dirname:
        path = [dirname]
    else:
        if path is None:
            path = os.environ.get('PATH', None)
            if path is None:
                try:
                    path = os.confstr('CS_PATH')
                except (AttributeError, ValueError):
                    path = os.defpath
        if not path:
            return None
        if use_bytes:
            path = os.fsencode(path)
            path = path.split(os.fsencode(os.pathsep))
        else:
            path = os.fsdecode(path)
            path = path.split(os.pathsep)
        if sys.platform == 'win32' and _win_path_needs_curdir(cmd, mode):
            curdir = os.curdir
            if use_bytes:
                curdir = os.fsencode(curdir)
            path.insert(0, curdir)
    if sys.platform == 'win32':
        pathext_source = os.getenv('PATHEXT') or _WIN_DEFAULT_PATHEXT
        pathext = pathext_source.split(os.pathsep)
        pathext = [ext.rstrip('.') for ext in pathext if ext]
        if use_bytes:
            pathext = [os.fsencode(ext) for ext in pathext]
        files = [cmd + ext for ext in pathext]
        normcmd = cmd.upper()
        if not mode & os.X_OK or any((normcmd.endswith(ext.upper()) for ext in pathext)):
            files.insert(0, cmd)
    else:
        files = [cmd]
    seen = set()
    for dir in path:
        normdir = os.path.normcase(dir)
        if normdir not in seen:
            seen.add(normdir)
            for thefile in files:
                name = os.path.join(dir, thefile)
                if _access_check(name, mode):
                    return name
    return None

def __getattr__(name):
    if name == 'ExecError':
        import warnings
        warnings._deprecated('shutil.ExecError', f"{warnings._DEPRECATED_MSG}; it isn't raised by any shutil function.", remove=(3, 16))
        return RuntimeError
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import shutil as _英文库
错误 = _英文库.Error
读错误 = _英文库.ReadError
注册表错误 = _英文库.RegistryError
同一文件错误 = _英文库.SameFileError
特殊文件错误 = _英文库.SpecialFileError
_模块别名 = {
    'COPY_BUFSIZE': '复制缓冲大小',
    'Error': '错误',
    'ReadError': '读错误',
    'RegistryError': '注册表错误',
    'SameFileError': '同一文件错误',
    'SpecialFileError': '特殊文件错误',
    'chown': '改属主',
    'copy': '复制',
    'copy2': '复制带元数据',
    'copyfile': '复制文件',
    'copymode': '复制权限',
    'copystat': '复制状态',
    'copytree': '复制树',
    'disk_usage': '磁盘用量',
    'get_archive_formats': '取归档格式',
    'get_terminal_size': '取终端大小',
    'get_unpack_formats': '取解包格式',
    'ignore_patterns': '忽略匹配',
    'make_archive': '造归档',
    'move': '移动',
    'register_archive_format': '登记归档格式',
    'register_unpack_format': '登记解包格式',
    'rmtree': '删目录树',
    'unpack_archive': '解归档',
    'unregister_archive_format': '注销归档格式',
    'unregister_unpack_format': '注销解包格式',
    'which': '找可执行文件',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '删目录树',
    '取归档格式',
    '取终端大小',
    '取解包格式',
    '同一文件错误',
    '复制',
    '复制带元数据',
    '复制文件',
    '复制权限',
    '复制树',
    '复制状态',
    '忽略匹配',
    '找可执行文件',
    '改属主',
    '注销归档格式',
    '注销解包格式',
    '特殊文件错误',
    '登记归档格式',
    '登记解包格式',
    '磁盘用量',
    '移动',
    '解归档',
    '造归档',
    '错误',
])

# ---- 转发层结束 ----
