# -*- coding: utf-8 -*-
"""异步IO —— 由 `tools\汉化库.py` 机械生成的**薄壳**（D-182），别手改。

英文模块：`asyncio`（**不深拷贝**：中文名是**别名**，跟英文名指向同一个对象）
为什么：asyncio 的核心被 _asyncio C 加速、内部耦合极深：深拷贝会造出第二套 Task/Future/事件循环，实测 test_events 卡死、全包约 503 个失败；薄壳只有一个世界

⚠ 薄壳 = **包级名字 + 子模块名都指向英文那份同一个对象**（D-183）：
  * `globals().update(英文公开名)` + `__path__ = 英文.__path__`
  * 子模块**先真导入一遍再挂到 `sys.modules[汉语名.子模块]`** —— 少了这一句，
    `import 异步IO.子模块` 会**再加载一份**：两个类对象（`isinstance` 挂），
    导入机械出现两套状态（官方 `test_importlib` 实测 138 条失败）。
"""

import importlib as __导入工具
import sys as __系统
import asyncio as __英文

for _子 in ('base_events', 'base_futures', 'base_subprocess', 'base_tasks', 'constants', 'coroutines', 'events', 'exceptions', 'format_helpers', 'futures', 'graph', 'locks', 'log', 'mixins', 'proactor_events', 'protocols', 'queues', 'runners', 'selector_events', 'sslproto', 'staggered', 'streams', 'subprocess', 'taskgroups', 'tasks', 'threads', 'timeouts', 'tools', 'transports', 'trsock', 'unix_events', 'windows_events', 'windows_utils'):
    try:
        __系统.modules["异步IO." + _子] = __导入工具.import_module("asyncio." + _子)
    except ImportError:
        pass      # 平台相关子模块（如 Windows 上的 asyncio.unix_events）

globals().update({_名: _值 for _名, _值 in vars(__英文).items() if not _名.startswith("__")})
__path__ = __英文.__path__

_别名对 = (('AbstractEventLoop', '抽象事件循环'), ('AbstractServer', '抽象服务器'), ('Barrier', '栅栏'), ('BaseEventLoop', '基础事件循环'), ('BaseProtocol', '基础协议'), ('BaseTransport', '基础传输'), ('BoundedSemaphore', '有界信号量'), ('BrokenBarrierError', '栅栏破损错误'), ('BufferedProtocol', '缓冲协议'), ('CancelledError', '已取消错误'), ('Condition', '条件变量'), ('DatagramProtocol', '数据报协议'), ('DatagramTransport', '数据报传输'), ('Event', '事件'), ('Future', '期物'), ('Handle', '句柄'), ('IncompleteReadError', '读不完整错误'), ('InvalidStateError', '无效状态错误'), ('IocpProactor', '完成端口前摄'), ('LifoQueue', '后进先出队列'), ('LimitOverrunError', '超限错误'), ('Lock', '互斥锁'), ('PriorityQueue', '优先队列'), ('ProactorEventLoop', '前摄器循环'), ('Protocol', '协议'), ('Queue', '队列'), ('QueueEmpty', '队列空'), ('QueueFull', '队列满'), ('QueueShutDown', '队列已关闭'), ('ReadTransport', '读传输'), ('Runner', '运行器'), ('SelectorEventLoop', '选择器循环'), ('Semaphore', '信号量'), ('SendfileNotAvailableError', '发文件不可用'), ('Server', '服务器'), ('StreamReader', '流读取器'), ('StreamReaderProtocol', '流读取协议'), ('StreamWriter', '流写入器'), ('SubprocessProtocol', '子进程协议'), ('SubprocessTransport', '子进程传输'), ('Task', '任务'), ('TaskGroup', '任务组'), ('Timeout', '限时器'), ('TimerHandle', '定时句柄'), ('Transport', '传输'), ('WriteTransport', '写传输'), ('abort', '中止'), ('acquire', '获取'), ('as_completed', '完成即取'), ('at_eof', '到末尾了吗'), ('can_write_eof', '能写结束吗'), ('capture_call_graph', '捕获调用图'), ('clear', '清除'), ('close', '关闭'), ('create_subprocess_exec', '造子进程'), ('create_subprocess_shell', '造外壳子进程'), ('create_task', '造任务'), ('drain', '冲刷'), ('eager_task_factory', '急切任务工厂'), ('empty', '是空的吗'), ('ensure_future', '确保期物'), ('expired', '已超时'), ('feed_data', '喂数据'), ('feed_eof', '喂结束'), ('format_call_graph', '格式化调用图'), ('full', '是满的吗'), ('gather', '收集'), ('get', '取出'), ('get_event_loop_policy', '取循环策略'), ('get_extra_info', '取附加信息'), ('get_loop', '取循环'), ('get_nowait', '不等待取出'), ('is_closing', '正在关闭吗'), ('is_set', '已设置吗'), ('iscoroutine', '是协程吗'), ('iscoroutinefunction', '是协程函数吗'), ('isfuture', '是期物吗'), ('join', '等待清空'), ('locked', '已锁定吗'), ('new_event_loop', '新事件循环'), ('notify', '通知一个'), ('notify_all', '通知全部'), ('print_call_graph', '打印调用图'), ('put', '放入'), ('put_nowait', '不等待放入'), ('qsize', '取大小'), ('read', '读取'), ('readexactly', '精确读取'), ('readline', '读一行'), ('readuntil', '读到为止'), ('release', '释放'), ('reschedule', '重排'), ('reset', '重置'), ('run', '运行'), ('run_coroutine_threadsafe', '跨线程跑协程'), ('set', '设置'), ('set_event_loop', '设事件循环'), ('set_event_loop_policy', '设循环策略'), ('set_exception', '设异常'), ('set_transport', '设传输'), ('shield', '保护'), ('shutdown', '关闭'), ('sleep', '休眠'), ('task_done', '任务完成'), ('to_thread', '在线程跑'), ('wait', '等待完成'), ('wait_closed', '等待关闭'), ('wait_for', '限时等待'), ('when', '何时'), ('wrap_future', '包装期物'), ('write', '写入'), ('write_eof', '写结束'), ('writelines', '写多行'))
for _英, _中 in _别名对:
    if hasattr(__英文, _英):
        globals()[_中] = getattr(__英文, _英)

__all__ = tuple(list(getattr(__英文, "__all__", [])) +
               [_中 for _英, _中 in _别名对 if _中 in globals()])


def __getattr__(名):
    """兜底转发：没显式起中文名的（含私有名）照样到得了英文那边。"""
    return getattr(__英文, 名)


def __dir__():
    return sorted(set(globals()) | set(dir(__英文)))
