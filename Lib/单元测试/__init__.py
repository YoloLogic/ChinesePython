# -*- coding: utf-8 -*-
"""单元测试.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/unittest/__init__.py 机械生成，**不要手改**）。

英文库 Lib/unittest.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py unittest
"""


"""
Python unit testing framework, based on Erich Gamma's JUnit and Kent Beck's
Smalltalk testing framework (used with permission).

This module contains the core framework classes that form the basis of
specific test cases and suites (TestCase, TestSuite etc.), and also a
text-based utility class for running the tests and reporting the results
 (TextTestRunner).

Simple usage:

    import unittest

    class IntegerArithmeticTestCase(unittest.TestCase):
        def testAdd(self):  # test method names begin with 'test'
            self.assertEqual((1 + 2), 3)
            self.assertEqual(0 + 1, 1)
        def testMultiply(self):
            self.assertEqual((0 * 10), 0)
            self.assertEqual((5 * 8), 40)

    if __name__ == '__main__':
        unittest.main()

Further information is available in the bundled documentation, and from

  http://docs.python.org/library/unittest.html

Copyright (c) 1999-2003 Steve Purcell
Copyright (c) 2003 Python Software Foundation
This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.
"""
__all__ = ['TestResult', 'TestCase', 'IsolatedAsyncioTestCase', 'TestSuite', 'TextTestRunner', 'TestLoader', 'FunctionTestCase', 'main', 'defaultTestLoader', 'SkipTest', 'skip', 'skipIf', 'skipUnless', 'expectedFailure', 'TextTestResult', 'installHandler', 'registerResult', 'removeResult', 'removeHandler', 'addModuleCleanup', 'doModuleCleanups', 'enterModuleContext']
__unittest = True
from .result import 测试结果
from .case import 加模块清理, 测试用例, 函数测试用例, 跳过异常, 跳过用例, 条件跳过, 不满足则跳过, 预期失败, 做模块清理, 进入模块上下文
from .suite import BaseTestSuite, 测试套件
from .loader import 测试加载器, 默认测试加载器
from .main import TestProgram, main
from .runner import 文本测试运行器, 文本测试结果
from .signals import 装处理器, 登记结果, 移除结果, 移除处理器

def __dir__():
    return globals().keys() | {'IsolatedAsyncioTestCase'}

def __getattr__(name):
    if name == 'IsolatedAsyncioTestCase':
        global IsolatedAsyncioTestCase
        from .async_case import IsolatedAsyncioTestCase
        return IsolatedAsyncioTestCase
    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')


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
_模块别名 = {
    'FunctionTestCase': '函数测试用例',
    'SkipTest': '跳过异常',
    'TestCase': '测试用例',
    'TestLoader': '测试加载器',
    'TestResult': '测试结果',
    'TestSuite': '测试套件',
    'TextTestResult': '文本测试结果',
    'TextTestRunner': '文本测试运行器',
    'addModuleCleanup': '加模块清理',
    'defaultTestLoader': '默认测试加载器',
    'doModuleCleanups': '做模块清理',
    'enterModuleContext': '进入模块上下文',
    'expectedFailure': '预期失败',
    'installHandler': '装处理器',
    'registerResult': '登记结果',
    'removeHandler': '移除处理器',
    'removeResult': '移除结果',
    'skip': '跳过用例',
    'skipIf': '条件跳过',
    'skipUnless': '不满足则跳过',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '异步测试用例',
]

# ---- 转发层结束 ----
