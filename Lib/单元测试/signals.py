# -*- coding: utf-8 -*-
"""单元测试.signals —— 汉语库（由 tools/汉化库.py 从 Lib/unittest/signals.py 机械生成，**不要手改**）。

英文库 Lib/unittest.signals.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py unittest
"""


_英文原名表 = {'installHandler': '装处理器', 'registerResult': '登记结果', 'removeHandler': '移除处理器', 'removeResult': '移除结果'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import signal
import weakref
from functools import wraps
__unittest = True

class _InterruptHandler(object):

    def __init__(self, default_handler):
        self.called = False
        self.original_handler = default_handler
        if isinstance(default_handler, int):
            if default_handler == signal.SIG_DFL:
                default_handler = signal.default_int_handler
            elif default_handler == signal.SIG_IGN:

                def default_handler(unused_signum, unused_frame):
                    pass
            else:
                raise TypeError('expected SIGINT signal handler to be signal.SIG_IGN, signal.SIG_DFL, or a callable object')
        self.default_handler = default_handler

    def __call__(self, signum, frame):
        installed_handler = signal.getsignal(signal.SIGINT)
        if installed_handler is not self:
            self.default_handler(signum, frame)
        if self.called:
            self.default_handler(signum, frame)
        self.called = True
        for result in _results.keys():
            result.stop()
_results = weakref.WeakKeyDictionary()

def 登记结果(result):
    _results[result] = 1

def 移除结果(result):
    return bool(_results.pop(result, None))
_interrupt_handler = None

def 装处理器():
    global _interrupt_handler
    if _interrupt_handler is None:
        default_handler = signal.getsignal(signal.SIGINT)
        _interrupt_handler = _InterruptHandler(default_handler)
        signal.signal(signal.SIGINT, _interrupt_handler)

def 移除处理器(method=None):
    if method is not None:

        @wraps(method)
        def inner(*args, **kwargs):
            initial = signal.getsignal(signal.SIGINT)
            移除处理器()
            try:
                return method(*args, **kwargs)
            finally:
                signal.signal(signal.SIGINT, initial)
        return inner
    global _interrupt_handler
    if _interrupt_handler is not None:
        signal.signal(signal.SIGINT, _interrupt_handler.original_handler)


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'installHandler': '装处理器',
    'registerResult': '登记结果',
    'removeHandler': '移除处理器',
    'removeResult': '移除结果',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
