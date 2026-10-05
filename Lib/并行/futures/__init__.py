# -*- coding: utf-8 -*-
"""并行.futures/__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/concurrent/futures/__init__.py 机械生成，**不要手改**）。

英文库 Lib/concurrent.futures/__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py concurrent
"""


"""Execute computations asynchronously using threads or processes."""
__author__ = 'Brian Quinlan (brian@sweetapp.com)'
from 并行.futures._base import 最先完成, 最先异常, 全部完成, 已取消错误, TimeoutError, 状态无效错误, 执行器损坏错误, 未来对象, 执行器, 等待完成, 完成即取
__all__ = ['FIRST_COMPLETED', 'FIRST_EXCEPTION', 'ALL_COMPLETED', 'CancelledError', 'TimeoutError', 'InvalidStateError', 'BrokenExecutor', 'Future', 'Executor', 'wait', 'as_completed', 'ProcessPoolExecutor', 'ThreadPoolExecutor']
try:
    import _interpreters
except ImportError:
    _interpreters = None
if _interpreters:
    __all__.append('InterpreterPoolExecutor')

def __dir__():
    return __all__ + ['__author__', '__doc__']

def __getattr__(name):
    global ProcessPoolExecutor, ThreadPoolExecutor, InterpreterPoolExecutor
    if name == 'ProcessPoolExecutor':
        from .process import ProcessPoolExecutor
        return ProcessPoolExecutor
    if name == 'ThreadPoolExecutor':
        from .thread import ThreadPoolExecutor
        return ThreadPoolExecutor
    if _interpreters and name == 'InterpreterPoolExecutor':
        from .interpreter import InterpreterPoolExecutor
        return InterpreterPoolExecutor
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
    '解释器池执行器': 'InterpreterPoolExecutor',
    '超时错误': 'TimeoutError',
    '进程池执行器': 'ProcessPoolExecutor',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})

# 懒别名（D-151）：这些名字是模块级 `__getattr__` 懒加载的，上面那次 `globals()` 抓不到它们。
# 中文名转成英文名后交给原来那个 `__getattr__`（PEP 562）。
_懒别名 = {
    '线程池执行器': 'ThreadPoolExecutor',
    '解释器池执行器': 'InterpreterPoolExecutor',
    '进程池执行器': 'ProcessPoolExecutor',
}
if _懒别名 and '__getattr__' in globals():
    _原取属性 = globals()['__getattr__']
    def __getattr__(名字):
        return _原取属性(_懒别名.get(名字, 名字))
_模块别名 = {
    'ALL_COMPLETED': '全部完成',
    'BrokenExecutor': '执行器损坏错误',
    'CancelledError': '已取消错误',
    'Executor': '执行器',
    'FIRST_COMPLETED': '最先完成',
    'FIRST_EXCEPTION': '最先异常',
    'Future': '未来对象',
    'InvalidStateError': '状态无效错误',
    'as_completed': '完成即取',
    'wait': '等待完成',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '解释器池执行器',
    '超时错误',
    '进程池执行器',
]

# ---- 转发层结束 ----
