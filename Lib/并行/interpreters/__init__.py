# -*- coding: utf-8 -*-
"""并行.interpreters/__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/interpreters/__init__.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.interpreters/__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


"""Subinterpreters High Level Module."""
_英文原名表 = {'Interpreter': '解释器', 'create': '创建', 'get_current': '取当前', 'get_main': '取主', 'list_all': '列出全部'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import threading
import weakref
import _interpreters
from _interpreters import InterpreterError, InterpreterNotFoundError, NotShareableError, is_shareable
from ._queues import create as create_queue, Queue, QueueEmpty, QueueFull
__all__ = ['get_current', 'get_main', 'create', 'list_all', 'is_shareable', 'Interpreter', 'InterpreterError', 'InterpreterNotFoundError', 'ExecutionFailed', 'NotShareableError', 'create_queue', 'Queue', 'QueueEmpty', 'QueueFull']
_EXEC_FAILURE_STR = '\n{superstr}\n\nUncaught in the interpreter:\n\n{formatted}\n'.strip()

class ExecutionFailed(InterpreterError):
    """An unhandled exception happened during execution.

    This is raised from Interpreter.exec() and Interpreter.call().
    """

    def __init__(self, excinfo):
        msg = excinfo.formatted
        if not msg:
            if excinfo.type and excinfo.msg:
                msg = f'{excinfo.type.__name__}: {excinfo.msg}'
            else:
                msg = excinfo.type.__name__ or excinfo.msg
        super().__init__(msg)
        self.excinfo = excinfo

    def __str__(self):
        try:
            formatted = self.excinfo.errdisplay
        except Exception:
            return super().__str__()
        else:
            return _EXEC_FAILURE_STR.format(superstr=super().__str__(), formatted=formatted)

def 创建():
    """Return a new (idle) Python interpreter."""
    id = _interpreters.create(reqrefs=True)
    return 解释器(id, _ownsref=True)

def 列出全部():
    """Return all existing interpreters."""
    return [解释器(id, _whence=whence) for id, whence in _interpreters.list_all(require_ready=True)]

def 取当前():
    """Return the currently running interpreter."""
    id, whence = _interpreters.get_current()
    return 解释器(id, _whence=whence)

def 取主():
    """Return the main interpreter."""
    id, whence = _interpreters.get_main()
    assert whence == _interpreters.WHENCE_RUNTIME, repr(whence)
    return 解释器(id, _whence=whence)
_known = weakref.WeakValueDictionary()

class 解释器:
    """A single Python interpreter.

    Attributes:

    "id" - the unique process-global ID number for the interpreter
    "whence" - indicates where the interpreter was created

    If the interpreter wasn't created by this module
    then any method that modifies the interpreter will fail,
    i.e. .close(), .prepare_main(), .exec(), and .call()
    """
    _WHENCE_TO_STR = {_interpreters.WHENCE_UNKNOWN: 'unknown', _interpreters.WHENCE_RUNTIME: 'runtime init', _interpreters.WHENCE_LEGACY_CAPI: 'legacy C-API', _interpreters.WHENCE_CAPI: 'C-API', _interpreters.WHENCE_XI: 'cross-interpreter C-API', _interpreters.WHENCE_STDLIB: '_interpreters module'}

    def __new__(cls, id, /, _whence=None, _ownsref=None):
        if not isinstance(id, int):
            raise TypeError(f'id must be an int, got {id!r}')
        id = int(id)
        if _whence is None:
            if _ownsref:
                _whence = _interpreters.WHENCE_STDLIB
            else:
                _whence = _interpreters.whence(id)
        assert _whence in cls._WHENCE_TO_STR, repr(_whence)
        if _ownsref is None:
            _ownsref = _whence == _interpreters.WHENCE_STDLIB
        try:
            self = _known[id]
            assert hasattr(self, '_ownsref')
        except KeyError:
            self = super().__new__(cls)
            _known[id] = self
            self._id = id
            self._whence = _whence
            self._ownsref = _ownsref
            if _ownsref:
                _interpreters.incref(id)
        return self

    def __repr__(self):
        return f'{type(self).__name__}({self.id})'

    def __hash__(self):
        return hash(self._id)

    def __del__(self):
        self._decref()

    def __reduce__(self):
        return (type(self), (self._id,))

    def _decref(self, *, InterpreterNotFoundError=InterpreterNotFoundError, _interp_decref=_interpreters.decref):
        if not self._ownsref:
            return
        self._ownsref = False
        try:
            _interp_decref(self._id)
        except InterpreterNotFoundError:
            pass

    @property
    def id(self):
        return self._id

    @property
    def whence(self):
        return self._WHENCE_TO_STR[self._whence]

    def is_running(self):
        """Return whether or not the identified interpreter is running."""
        return _interpreters.is_running(self._id)

    def close(self):
        """Finalize and destroy the interpreter.

        Attempting to destroy the current interpreter results
        in an InterpreterError.
        """
        return _interpreters.destroy(self._id, restrict=True)

    def prepare_main(self, ns=None, /, **kwargs):
        """Bind the given values into the interpreter's __main__.

        The values must be shareable.
        """
        ns = dict(ns, **kwargs) if ns is not None else kwargs
        _interpreters.set___main___attrs(self._id, ns, restrict=True)

    def exec(self, code, /):
        """Run the given source code in the interpreter.

        This is essentially the same as calling the builtin "exec"
        with this interpreter, using the __dict__ of its __main__
        module as both globals and locals.

        There is no return value.

        If the code raises an unhandled exception then an ExecutionFailed
        exception is raised, which summarizes the unhandled exception.
        The actual exception is discarded because objects cannot be
        shared between interpreters.

        This blocks the current Python thread until done.  During
        that time, the previous interpreter is allowed to run
        in other threads.
        """
        excinfo = _interpreters.exec(self._id, code, restrict=True)
        if excinfo is not None:
            raise ExecutionFailed(excinfo)

    def _call(self, callable, args, kwargs):
        res, excinfo = _interpreters.call(self._id, callable, args, kwargs, restrict=True)
        if excinfo is not None:
            raise ExecutionFailed(excinfo)
        return res

    def call(self, callable, /, *args, **kwargs):
        """Call the object in the interpreter with given args/kwargs.

        Nearly all callables, args, kwargs, and return values are
        supported.  All "shareable" objects are supported, as are
        "stateless" functions (meaning non-closures that do not use
        any globals).  This method will fall back to pickle.

        If the callable raises an exception then the error display
        (including full traceback) is sent back between the interpreters
        and an ExecutionFailed exception is raised, much like what
        happens with Interpreter.exec().
        """
        return self._call(callable, args, kwargs)

    def call_in_thread(self, callable, /, *args, **kwargs):
        """Return a new thread that calls the object in the interpreter.

        The return value and any raised exception are discarded.
        """
        t = threading.Thread(target=self._call, args=(callable, args, kwargs))
        t.start()
        return t


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
    '执行失败错误': 'ExecutionFailed',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'Interpreter': '解释器',
    'create': '创建',
    'get_current': '取当前',
    'get_main': '取主',
    'list_all': '列出全部',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '列出全部',
    '创建',
    '取主',
    '取当前',
    '执行失败错误',
    '解释器',
])

# ---- 转发层结束 ----
