# -*- coding: utf-8 -*-
"""多进程.dummy/connection —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/dummy/connection.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.dummy/connection.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Client': '客户端', 'Connection': '连接', 'Listener': '监听器', 'Pipe': '管道'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['Client', 'Listener', 'Pipe']
from queue import Queue
families = [None]

class 监听器(object):

    def __init__(self, address=None, family=None, backlog=1):
        self._backlog_queue = Queue(backlog)

    def accept(self):
        return 连接(*self._backlog_queue.get())

    def close(self):
        self._backlog_queue = None

    @property
    def address(self):
        return self._backlog_queue

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

def 客户端(address):
    _in, _out = (Queue(), Queue())
    address.put((_out, _in))
    return 连接(_in, _out)

def 管道(duplex=True):
    a, b = (Queue(), Queue())
    return (连接(a, b), 连接(b, a))

class 连接(object):

    def __init__(self, _in, _out):
        self._out = _out
        self._in = _in
        self.send = self.send_bytes = _out.put
        self.recv = self.recv_bytes = _in.get

    def poll(self, timeout=0.0):
        if self._in.qsize() > 0:
            return True
        if timeout <= 0.0:
            return False
        with self._in.not_empty:
            self._in.not_empty.wait(timeout)
        return self._in.qsize() > 0

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'Client': '客户端',
    'Connection': '连接',
    'Listener': '监听器',
    'Pipe': '管道',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '客户端',
    '监听器',
    '管道',
])

# ---- 转发层结束 ----
