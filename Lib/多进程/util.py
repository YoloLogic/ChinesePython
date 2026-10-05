# -*- coding: utf-8 -*-
"""多进程.util —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/util.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.util.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Finalize': '终结器', 'ForkAwareLocal': '感知分叉局部', 'ForkAwareThreadLock': '感知分叉线程锁', 'close_fds': '关闭描述符', 'get_logger': '取日志器', 'get_temp_dir': '取临时目录', 'is_exiting': '正在退出吗', 'log_to_stderr': '记到标准错误', 'register_after_fork': '注册分叉后钩子', 'spawnv_passfds': '派生并传描述符'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import os
import itertools
import sys
import weakref
import atexit
import threading
from subprocess import _args_from_interpreter_flags
from . import process
__all__ = ['sub_debug', 'debug', 'info', 'sub_warning', 'warn', 'get_logger', 'log_to_stderr', 'get_temp_dir', 'register_after_fork', 'is_exiting', 'Finalize', 'ForkAwareThreadLock', 'ForkAwareLocal', 'close_all_fds_except', 'SUBDEBUG', 'SUBWARNING']
NOTSET = 0
SUBDEBUG = 5
DEBUG = 10
INFO = 20
SUBWARNING = 25
WARNING = 30
LOGGER_NAME = 'multiprocessing'
DEFAULT_LOGGING_FORMAT = '[%(levelname)s/%(processName)s] %(message)s'
_logger = None
_log_to_stderr = False

def sub_debug(msg, *args):
    if _logger:
        _logger.log(SUBDEBUG, msg, *args, stacklevel=2)

def debug(msg, *args):
    if _logger:
        _logger.log(DEBUG, msg, *args, stacklevel=2)

def info(msg, *args):
    if _logger:
        _logger.log(INFO, msg, *args, stacklevel=2)

def warn(msg, *args):
    if _logger:
        _logger.log(WARNING, msg, *args, stacklevel=2)

def sub_warning(msg, *args):
    if _logger:
        _logger.log(SUBWARNING, msg, *args, stacklevel=2)

def 取日志器():
    """
    Returns logger used by multiprocessing
    """
    global _logger
    import logging
    with logging._lock:
        if not _logger:
            _logger = logging.getLogger(LOGGER_NAME)
            _logger.propagate = 0
            if hasattr(atexit, 'unregister'):
                atexit.unregister(_exit_function)
                atexit.register(_exit_function)
            else:
                atexit._exithandlers.remove((_exit_function, (), {}))
                atexit._exithandlers.append((_exit_function, (), {}))
    return _logger

def 记到标准错误(level=None):
    """
    Turn on logging and add a handler which prints to stderr
    """
    global _log_to_stderr
    import logging
    logger = 取日志器()
    formatter = logging.Formatter(DEFAULT_LOGGING_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if level:
        logger.setLevel(level)
    _log_to_stderr = True
    return _logger

def _platform_supports_abstract_sockets():
    return sys.platform in ('linux', 'android')

def is_abstract_socket_namespace(address):
    if not address:
        return False
    if isinstance(address, bytes):
        return address[0] == 0
    elif isinstance(address, str):
        return address[0] == '\x00'
    raise TypeError(f'address type of {address!r} unrecognized')
abstract_sockets_supported = _platform_supports_abstract_sockets()
if sys.platform == 'linux':
    _SUN_PATH_MAX = 108
elif sys.platform.startswith(('openbsd', 'freebsd')):
    _SUN_PATH_MAX = 104
else:
    _SUN_PATH_MAX = None if os.name == 'nt' else 92

def _remove_temp_dir(rmtree, tempdir):
    rmtree(tempdir)
    current_process = process.current_process()
    if current_process is not None:
        current_process._config['tempdir'] = None

def _get_base_temp_dir(tempfile):
    """Get a temporary directory where socket files will be created.

    To prevent additional imports, pass a pre-imported 'tempfile' module.
    """
    if os.name == 'nt':
        return None
    base_tempdir = tempfile.gettempdir()
    sun_path_len = len(base_tempdir) + 14 + 14
    if sun_path_len < _SUN_PATH_MAX:
        return base_tempdir
    dirlist = ['/tmp', '/var/tmp', '/usr/tmp']
    try:
        base_system_tempdir = tempfile._get_default_tempdir(dirlist)
    except FileNotFoundError:
        warn('Process-wide temporary directory %s will not be usable for creating socket files and no usable system-wide temporary directory was found in %s', base_tempdir, dirlist)
        return base_tempdir
    warn('Ignoring user-defined temporary directory: %s', base_tempdir)
    assert len(base_system_tempdir) + 14 + 14 < _SUN_PATH_MAX
    return base_system_tempdir

def 取临时目录():
    tempdir = process.current_process()._config.get('tempdir')
    if tempdir is None:
        import shutil, tempfile
        base_tempdir = _get_base_temp_dir(tempfile)
        tempdir = tempfile.mkdtemp(prefix='pymp-', dir=base_tempdir)
        info('created temp directory %s', tempdir)
        终结器(None, _remove_temp_dir, args=(shutil.rmtree, tempdir), exitpriority=-100)
        process.current_process()._config['tempdir'] = tempdir
    return tempdir
_afterfork_registry = weakref.WeakValueDictionary()
_afterfork_counter = itertools.count()

def _run_after_forkers():
    items = list(_afterfork_registry.items())
    items.sort()
    for (index, ident, func), obj in items:
        try:
            func(obj)
        except Exception as e:
            info('after forker raised exception %s', e)

def 注册分叉后钩子(obj, func):
    _afterfork_registry[next(_afterfork_counter), id(obj), func] = obj
_finalizer_registry = {}
_finalizer_counter = itertools.count()

class 终结器(object):
    """
    Class which supports object finalization using weakrefs
    """

    def __init__(self, obj, callback, args=(), kwargs=None, exitpriority=None):
        if exitpriority is not None and (not isinstance(exitpriority, int)):
            raise TypeError('Exitpriority ({0!r}) must be None or int, not {1!s}'.format(exitpriority, type(exitpriority)))
        if obj is not None:
            self._weakref = weakref.ref(obj, self)
        elif exitpriority is None:
            raise ValueError('Without object, exitpriority cannot be None')
        self._callback = callback
        self._args = args
        self._kwargs = kwargs or {}
        self._key = (exitpriority, next(_finalizer_counter))
        self._pid = os.getpid()
        _finalizer_registry[self._key] = self

    def __call__(self, wr=None, _finalizer_registry=_finalizer_registry, sub_debug=sub_debug, getpid=os.getpid):
        """
        Run the callback unless it has already been called or cancelled
        """
        try:
            del _finalizer_registry[self._key]
        except KeyError:
            sub_debug('finalizer no longer registered')
        else:
            if self._pid != getpid():
                sub_debug('finalizer ignored because different process')
                res = None
            else:
                sub_debug('finalizer calling %s with args %s and kwargs %s', self._callback, self._args, self._kwargs)
                res = self._callback(*self._args, **self._kwargs)
            self._weakref = self._callback = self._args = self._kwargs = self._key = None
            return res

    def cancel(self):
        """
        Cancel finalization of the object
        """
        try:
            del _finalizer_registry[self._key]
        except KeyError:
            pass
        else:
            self._weakref = self._callback = self._args = self._kwargs = self._key = None

    def still_active(self):
        """
        Return whether this finalizer is still waiting to invoke callback
        """
        return self._key in _finalizer_registry

    def __repr__(self):
        try:
            obj = self._weakref()
        except (AttributeError, TypeError):
            obj = None
        if obj is None:
            return '<%s object, dead>' % self.__class__.__name__
        x = '<%s object, callback=%s' % (self.__class__.__name__, getattr(self._callback, '__name__', self._callback))
        if self._args:
            x += ', args=' + str(self._args)
        if self._kwargs:
            x += ', kwargs=' + str(self._kwargs)
        if self._key[0] is not None:
            x += ', exitpriority=' + str(self._key[0])
        return x + '>'

def _run_finalizers(minpriority=None):
    """
    Run all finalizers whose exit priority is not None and at least minpriority

    Finalizers with highest priority are called first; finalizers with
    the same priority will be called in reverse order of creation.
    """
    if _finalizer_registry is None:
        return
    if minpriority is None:
        f = lambda p: p[0] is not None
    else:
        f = lambda p: p[0] is not None and p[0] >= minpriority
    keys = [key for key in list(_finalizer_registry) if f(key)]
    keys.sort(reverse=True)
    for key in keys:
        finalizer = _finalizer_registry.get(key)
        if finalizer is not None:
            sub_debug('calling %s', finalizer)
            try:
                finalizer()
            except Exception:
                import traceback
                traceback.print_exc()
    if minpriority is None:
        _finalizer_registry.clear()

def 正在退出吗():
    """
    Returns true if the process is shutting down
    """
    return _exiting or _exiting is None
_exiting = False

def _exit_function(info=info, debug=debug, _run_finalizers=_run_finalizers, active_children=process.active_children, current_process=process.current_process):
    global _exiting
    if not _exiting:
        _exiting = True
        info('process shutting down')
        debug('running all "atexit" finalizers with priority >= 0')
        _run_finalizers(0)
        if current_process() is not None:
            for p in active_children():
                if p.daemon:
                    info('calling terminate() for daemon %s', p.name)
                    p._popen.terminate()
            for p in active_children():
                info('calling join() for process %s', p.name)
                p.join()
        debug('running the remaining "atexit" finalizers')
        _run_finalizers()
atexit.register(_exit_function)

class 感知分叉线程锁(object):

    def __init__(self):
        self._lock = threading.Lock()
        self.acquire = self._lock.acquire
        self.release = self._lock.release
        注册分叉后钩子(self, 感知分叉线程锁._at_fork_reinit)

    def _at_fork_reinit(self):
        self._lock._at_fork_reinit()

    def __enter__(self):
        return self._lock.__enter__()

    def __exit__(self, *args):
        return self._lock.__exit__(*args)

class 感知分叉局部(threading.local):

    def __init__(self):
        注册分叉后钩子(self, lambda obj: obj.__dict__.clear())

    def __reduce__(self):
        return (type(self), ())
try:
    MAXFD = os.sysconf('SC_OPEN_MAX')
except Exception:
    MAXFD = 256

def close_all_fds_except(fds):
    fds = list(fds) + [-1, MAXFD]
    fds.sort()
    assert fds[-1] == MAXFD, 'fd too large'
    for i in range(len(fds) - 1):
        os.closerange(fds[i] + 1, fds[i + 1])

def _close_stdin():
    if sys.stdin is None:
        return
    try:
        sys.stdin.close()
    except (OSError, ValueError):
        pass
    try:
        fd = os.open(os.devnull, os.O_RDONLY)
        try:
            sys.stdin = open(fd, encoding='utf-8', closefd=False)
        except:
            os.close(fd)
            raise
    except (OSError, ValueError):
        pass

def _flush_std_streams():
    try:
        sys.stdout.flush()
    except (AttributeError, ValueError):
        pass
    try:
        sys.stderr.flush()
    except (AttributeError, ValueError):
        pass

def 派生并传描述符(path, args, passfds):
    import _posixsubprocess
    passfds = tuple(sorted(map(int, passfds)))
    errpipe_read, errpipe_write = os.pipe()
    try:
        return _posixsubprocess.fork_exec(args, [path], True, passfds, None, None, -1, -1, -1, -1, -1, -1, errpipe_read, errpipe_write, False, False, -1, None, None, None, -1, None)
    finally:
        os.close(errpipe_read)
        os.close(errpipe_write)

def 关闭描述符(*fds):
    """Close each file descriptor given as an argument"""
    for fd in fds:
        os.close(fd)

def _cleanup_tests():
    """Cleanup multiprocessing resources when multiprocessing tests
    completed."""
    from test import support
    process._cleanup()
    from 多进程 import forkserver
    forkserver._forkserver._stop()
    from 多进程 import resource_tracker
    resource_tracker._resource_tracker._stop()
    _run_finalizers()
    support.gc_collect()
    support.reap_children()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Finalize': '终结器',
    'ForkAwareLocal': '感知分叉局部',
    'ForkAwareThreadLock': '感知分叉线程锁',
    'close_fds': '关闭描述符',
    'get_logger': '取日志器',
    'get_temp_dir': '取临时目录',
    'is_exiting': '正在退出吗',
    'log_to_stderr': '记到标准错误',
    'register_after_fork': '注册分叉后钩子',
    'spawnv_passfds': '派生并传描述符',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '取临时目录',
    '取日志器',
    '感知分叉局部',
    '感知分叉线程锁',
    '正在退出吗',
    '注册分叉后钩子',
    '终结器',
    '记到标准错误',
])

# ---- 转发层结束 ----
