# -*- coding: utf-8 -*-
"""单元测试.async_case —— 汉语库（由 tools/汉化库.py 从 Lib/unittest/async_case.py 机械生成，**不要手改**）。

英文库 Lib/unittest.async_case.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py unittest
"""


import asyncio
import contextvars
import inspect
import warnings
from .case import TestCase
__unittest = True

class IsolatedAsyncioTestCase(TestCase):
    loop_factory = None

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        self._asyncioRunner = None
        self._asyncioTestContext = contextvars.copy_context()

    async def asyncSetUp(self):
        pass

    async def asyncTearDown(self):
        pass

    def addAsyncCleanup(self, func, /, *args, **kwargs):
        self.addCleanup(*(func, *args), **kwargs)

    async def enterAsyncContext(self, cm):
        """Enters the supplied asynchronous context manager.

        If successful, also adds its __aexit__ method as a cleanup
        function and returns the result of the __aenter__ method.
        """
        cls = type(cm)
        try:
            enter = cls.__aenter__
            exit = cls.__aexit__
        except AttributeError:
            msg = f"'{cls.__module__}.{cls.__qualname__}' object does not support the asynchronous context manager protocol"
            try:
                cls.__enter__
                cls.__exit__
            except AttributeError:
                pass
            else:
                msg += ' but it supports the context manager protocol. Did you mean to use enterContext()?'
            raise TypeError(msg) from None
        result = await enter(cm)
        self.addAsyncCleanup(exit, cm, None, None, None)
        return result

    def _callSetUp(self):
        self._asyncioRunner.get_loop()
        self._asyncioTestContext.run(self.setUp)
        self._callAsync(self.asyncSetUp)

    def _callTestMethod(self, method):
        result = self._callMaybeAsync(method)
        if result is not None:
            msg = (f'It is deprecated to return a value that is not None from a test case ({method} returned {type(result).__name__!r})',)
            warnings.warn(msg, DeprecationWarning, stacklevel=4)

    def _callTearDown(self):
        self._callAsync(self.asyncTearDown)
        self._asyncioTestContext.run(self.tearDown)

    def _callCleanup(self, function, *args, **kwargs):
        self._callMaybeAsync(function, *args, **kwargs)

    def _callAsync(self, func, /, *args, **kwargs):
        assert self._asyncioRunner is not None, 'asyncio runner is not initialized'
        assert inspect.iscoroutinefunction(func), f'{func!r} is not an async function'
        return self._asyncioRunner.run(func(*args, **kwargs), context=self._asyncioTestContext)

    def _callMaybeAsync(self, func, /, *args, **kwargs):
        assert self._asyncioRunner is not None, 'asyncio runner is not initialized'
        if inspect.iscoroutinefunction(func):
            return self._asyncioRunner.run(func(*args, **kwargs), context=self._asyncioTestContext)
        else:
            return self._asyncioTestContext.run(func, *args, **kwargs)

    def _setupAsyncioRunner(self):
        assert self._asyncioRunner is None, 'asyncio runner is already initialized'
        runner = asyncio.Runner(debug=True, loop_factory=self.loop_factory)
        self._asyncioRunner = runner

    def _tearDownAsyncioRunner(self):
        runner = self._asyncioRunner
        runner.close()

    def run(self, result=None):
        self._setupAsyncioRunner()
        try:
            return super().run(result)
        finally:
            self._tearDownAsyncioRunner()

    def debug(self):
        self._setupAsyncioRunner()
        super().debug()
        self._tearDownAsyncioRunner()

    def __del__(self):
        if self._asyncioRunner is not None:
            self._tearDownAsyncioRunner()


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
    '异步测试用例': 'IsolatedAsyncioTestCase',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})

# ---- 转发层结束 ----
