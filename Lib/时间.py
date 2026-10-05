# -*- coding: utf-8 -*-
"""时间 —— 由 `tools\汉化包装层.py` **机械生成**，别手改。

英文模块：`time`（纯 C 扩展，没有 `.py` 源码可深拷贝 —— 走**机制 4：包装层**）。
改名字 = 改 `tools\库词表.py` 里的 `包装层["time"]`，然后：

    python tools\汉化包装层.py time

可逆性：删这个文件 + 删词表那一段，英文 `time` 一个字节没动。
守卫：`tools\汉化包装层.py --check`（生成物跟词表一致）、
      `tools\查库名字.py`（每个中文名真的存在、且跟英文名**是同一个对象**）、
      `tools\跑官方测试_汉语库.py`（官方测试原样跑在这个壳上）。

**中文名是别名，不是副本** —— 所以 `isinstance` / `except` / `is` 这些跟身份有关的
判据全都成立（跟机制 3 同一个道理，只是这里整模块一起给）。
"""


import time as __英文模块

# 中文名 -> 英文名：**同一个对象**（不是复制一份）。
# 名字顺序按英文名排，生成物才是确定的。
夏令时区 = __英文模块.altzone
转时间串 = __英文模块.asctime
转日期串 = __英文模块.ctime
夏令时标志 = __英文模块.daylight
取时钟信息 = __英文模块.get_clock_info
UTC时间 = __英文模块.gmtime
本地时间 = __英文模块.localtime
转时间戳 = __英文模块.mktime
单调时钟 = __英文模块.monotonic
单调时钟纳秒 = __英文模块.monotonic_ns
性能计数器 = __英文模块.perf_counter
性能计数器纳秒 = __英文模块.perf_counter_ns
进程时间 = __英文模块.process_time
进程时间纳秒 = __英文模块.process_time_ns
休眠 = __英文模块.sleep
格式化时间 = __英文模块.strftime
解析时间 = __英文模块.strptime
时间结构体 = __英文模块.struct_time
线程时间 = __英文模块.thread_time
线程时间纳秒 = __英文模块.thread_time_ns
时间戳 = __英文模块.time
时间戳纳秒 = __英文模块.time_ns
时区 = __英文模块.timezone
时区名 = __英文模块.tzname

# 英文原名一个都不能少：显式再绑一遍（壳自己的 `vars()` 里也看得见）。
altzone = __英文模块.altzone
asctime = __英文模块.asctime
ctime = __英文模块.ctime
daylight = __英文模块.daylight
get_clock_info = __英文模块.get_clock_info
gmtime = __英文模块.gmtime
localtime = __英文模块.localtime
mktime = __英文模块.mktime
monotonic = __英文模块.monotonic
monotonic_ns = __英文模块.monotonic_ns
perf_counter = __英文模块.perf_counter
perf_counter_ns = __英文模块.perf_counter_ns
process_time = __英文模块.process_time
process_time_ns = __英文模块.process_time_ns
sleep = __英文模块.sleep
strftime = __英文模块.strftime
strptime = __英文模块.strptime
struct_time = __英文模块.struct_time
thread_time = __英文模块.thread_time
thread_time_ns = __英文模块.thread_time_ns
time = __英文模块.time
time_ns = __英文模块.time_ns
timezone = __英文模块.timezone
tzname = __英文模块.tzname

__all__ = [
    'altzone',
    'asctime',
    'ctime',
    'daylight',
    'get_clock_info',
    'gmtime',
    'localtime',
    'mktime',
    'monotonic',
    'monotonic_ns',
    'perf_counter',
    'perf_counter_ns',
    'process_time',
    'process_time_ns',
    'sleep',
    'strftime',
    'strptime',
    'struct_time',
    'thread_time',
    'thread_time_ns',
    'time',
    'time_ns',
    'timezone',
    'tzname',
    '夏令时区',
    '转时间串',
    '转日期串',
    '夏令时标志',
    '取时钟信息',
    'UTC时间',
    '本地时间',
    '转时间戳',
    '单调时钟',
    '单调时钟纳秒',
    '性能计数器',
    '性能计数器纳秒',
    '进程时间',
    '进程时间纳秒',
    '休眠',
    '格式化时间',
    '解析时间',
    '时间结构体',
    '线程时间',
    '线程时间纳秒',
    '时间戳',
    '时间戳纳秒',
    '时区',
    '时区名',
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
