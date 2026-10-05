# -*- coding: utf-8 -*-
"""并行.futures/interpreter —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/futures/interpreter.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.futures/interpreter.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


"""Implements InterpreterPoolExecutor."""
_英文原名表 = {'BrokenInterpreterPool': '解释器池损坏错误', 'WorkerContext': '工作者上下文', 'do_call': '调用一次'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
from 并行 import interpreters
import sys
from . import thread as _thread
import traceback

def 调用一次(results, func, args, kwargs):
    try:
        return func(*args, **kwargs)
    except BaseException as exc:
        try:
            results.put(exc)
        except interpreters.NotShareableError:
            print('exception is not shareable:', file=sys.stderr)
            traceback.print_exception(exc)
            results.put(None)
        raise

class 工作者上下文(_thread.WorkerContext):

    @classmethod
    def prepare(cls, initializer, initargs):

        def resolve_task(fn, args, kwargs):
            if isinstance(fn, str):
                raise TypeError('scripts not supported')
            else:
                task = (fn, args, kwargs)
            return task
        if initializer is not None:
            try:
                initdata = resolve_task(initializer, initargs, {})
            except ValueError:
                if isinstance(initializer, str) and initargs:
                    raise ValueError(f'an initializer script does not take args, got {initargs!r}')
                raise
        else:
            initdata = None

        def create_context():
            return cls(initdata)
        return (create_context, resolve_task)

    def __init__(self, initdata):
        self.initdata = initdata
        self.interp = None
        self.results = None

    def __del__(self):
        if self.interp is not None:
            self.finalize()

    def initialize(self):
        assert self.interp is None, self.interp
        self.interp = interpreters.create()
        try:
            maxsize = 0
            self.results = interpreters.create_queue(maxsize)
            if self.initdata:
                self.run(self.initdata)
        except BaseException:
            self.finalize()
            raise

    def finalize(self):
        interp = self.interp
        results = self.results
        self.results = None
        self.interp = None
        if results is not None:
            del results
        if interp is not None:
            interp.close()

    def run(self, task):
        try:
            return self.interp.call(调用一次, self.results, *task)
        except interpreters.ExecutionFailed as wrapper:
            exc = self.results.get()
            if exc is None:
                raise
            raise exc from wrapper

class 解释器池损坏错误(_thread.BrokenThreadPool):
    """
    Raised when a worker thread in an InterpreterPoolExecutor failed initializing.
    """

class InterpreterPoolExecutor(_thread.ThreadPoolExecutor):
    BROKEN = 解释器池损坏错误

    @classmethod
    def prepare_context(cls, initializer, initargs):
        return 工作者上下文.prepare(initializer, initargs)

    def __init__(self, max_workers=None, thread_name_prefix='', initializer=None, initargs=()):
        """Initializes a new InterpreterPoolExecutor instance.

        Args:
            max_workers: The maximum number of interpreters that can be used
                to execute the given calls.
            thread_name_prefix: An optional name prefix to give our threads.
            initializer: A callable or script used to initialize
                each worker interpreter.
            initargs: A tuple of arguments to pass to the initializer.
        """
        thread_name_prefix = thread_name_prefix or f'InterpreterPoolExecutor-{self._counter()}'
        super().__init__(max_workers, thread_name_prefix, initializer, initargs)


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
    '解释器池执行器': 'InterpreterPoolExecutor',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'BrokenInterpreterPool': '解释器池损坏错误',
    'WorkerContext': '工作者上下文',
    'do_call': '调用一次',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
