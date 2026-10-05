# -*- coding: utf-8 -*-
"""信号 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`signal`（整层建在 `from _signal import *` + `_IntEnum._convert_` **运行时造枚举**上—— 改名会让 `_convert_` 扫不到，只能整模块走**身份别名**（机制 3 的整模块版））。
改名字 = 改 `tools\库词表.py` 里的 `包装层["signal"]`，然后：

    python tools\汉化包装层.py signal

可逆性：删这个文件 + 删词表那一段，英文 `signal` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import signal as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
控制台BREAK事件 = __英文模块.CTRL_BREAK_EVENT
控制台C事件 = __英文模块.CTRL_C_EVENT
处理器 = __英文模块.Handlers
信号个数 = __英文模块.NSIG
中止信号 = __英文模块.SIGABRT
中断键信号 = __英文模块.SIGBREAK
浮点异常信号 = __英文模块.SIGFPE
非法指令信号 = __英文模块.SIGILL
中断信号 = __英文模块.SIGINT
段错误信号 = __英文模块.SIGSEGV
终止信号 = __英文模块.SIGTERM
默认处理 = __英文模块.SIG_DFL
忽略信号 = __英文模块.SIG_IGN
信号集合 = __英文模块.Signals
默认中断处理器 = __英文模块.default_int_handler
取处理器 = __英文模块.getsignal
抛信号 = __英文模块.raise_signal
设唤醒描述符 = __英文模块.set_wakeup_fd
注册处理器 = __英文模块.signal
信号说明 = __英文模块.strsignal
有效信号集 = __英文模块.valid_signals

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
CTRL_BREAK_EVENT = __英文模块.CTRL_BREAK_EVENT
CTRL_C_EVENT = __英文模块.CTRL_C_EVENT
Handlers = __英文模块.Handlers
NSIG = __英文模块.NSIG
SIGABRT = __英文模块.SIGABRT
SIGBREAK = __英文模块.SIGBREAK
SIGFPE = __英文模块.SIGFPE
SIGILL = __英文模块.SIGILL
SIGINT = __英文模块.SIGINT
SIGSEGV = __英文模块.SIGSEGV
SIGTERM = __英文模块.SIGTERM
SIG_DFL = __英文模块.SIG_DFL
SIG_IGN = __英文模块.SIG_IGN
Signals = __英文模块.Signals
default_int_handler = __英文模块.default_int_handler
getsignal = __英文模块.getsignal
raise_signal = __英文模块.raise_signal
set_wakeup_fd = __英文模块.set_wakeup_fd
signal = __英文模块.signal
strsignal = __英文模块.strsignal
valid_signals = __英文模块.valid_signals

__all__ = [
    'CTRL_BREAK_EVENT',
    'CTRL_C_EVENT',
    'Handlers',
    'NSIG',
    'SIGABRT',
    'SIGBREAK',
    'SIGFPE',
    'SIGILL',
    'SIGINT',
    'SIGSEGV',
    'SIGTERM',
    'SIG_DFL',
    'SIG_IGN',
    'Signals',
    'default_int_handler',
    'getsignal',
    'raise_signal',
    'set_wakeup_fd',
    'signal',
    'strsignal',
    'valid_signals',
    '控制台BREAK事件',
    '控制台C事件',
    '处理器',
    '信号个数',
    '中止信号',
    '中断键信号',
    '浮点异常信号',
    '非法指令信号',
    '中断信号',
    '段错误信号',
    '终止信号',
    '默认处理',
    '忽略信号',
    '信号集合',
    '默认中断处理器',
    '取处理器',
    '抛信号',
    '设唤醒描述符',
    '注册处理器',
    '信号说明',
    '有效信号集',
]


def __getattr__(名):
    """兜底转发：没在这儿显式列出来的名字（含私有名）照样到得了 C 那边。

    为什么必须有：硬约束是「英文原名一个都不能少」，而 C 模块的内部名
    我们没法一个个预料 —— 官方测试碰得到的、`dir(zlib)` 里有的一切，
    靠这一条全部兜住（PEP 562 的模块级 `__getattr__`）。
    """
    return getattr(__英文模块, 名)


def __dir__():
    # `dir()` 两边都算上：Shell 补全 / 官方那种按 `dir()` 算的判据都看得见。
    # ⚠ **壳自己的辅助函数不列**（D-147）：官方 `test_signal.test_functions_module_attr`
    #   会遍历 `dir()`，要求每个「非内置函数」的 `__module__` 是英文模块名 ——
    #   壳里的 `__getattr__`/`__dir__` 是 Python 函数、`__module__` 是汉语模块名
    #   ⇒ 列出来就挂（实测）。
    return sorted((set(globals()) | set(dir(__英文模块)))
                  - {"__getattr__", "__dir__", "__英文模块"})
