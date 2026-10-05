# -*- coding: utf-8 -*-
"""SQLite数据库.dbapi2 —— 汉语库（由 tools/汉化库.py 从 Lib/sqlite3/dbapi2.py 机械生成，**不要手改**）。

英文库 Lib/sqlite3.dbapi2.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py sqlite3
"""


_英文原名表 = {'Binary': '二进制', 'Date': '日期', 'DateFromTicks': '时间戳转日期', 'Time': '时间', 'TimeFromTicks': '时间戳转时间', 'Timestamp': '时间戳', 'TimestampFromTicks': '时间戳转时间戳', 'apilevel': 'API级别', 'paramstyle': '参数风格', 'sqlite_version_info': 'SQLite版本信息'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import datetime
import time
import collections.abc
from _sqlite3 import *
参数风格 = 'qmark'
API级别 = '2.0'
日期 = datetime.date
时间 = datetime.time
时间戳 = datetime.datetime

def 时间戳转日期(ticks):
    return 日期(*time.localtime(ticks)[:3])

def 时间戳转时间(ticks):
    return 时间(*time.localtime(ticks)[3:6])

def 时间戳转时间戳(ticks):
    return 时间戳(*time.localtime(ticks)[:6])
SQLite版本信息 = tuple([int(x) for x in sqlite_version.split('.')])
二进制 = memoryview
collections.abc.Sequence.register(Row)

def register_adapters_and_converters():
    from warnings import warn
    msg = 'The default {what} is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes'

    def adapt_date(val):
        warn(msg.format(what='date adapter'), DeprecationWarning, stacklevel=2)
        return val.isoformat()

    def adapt_datetime(val):
        warn(msg.format(what='datetime adapter'), DeprecationWarning, stacklevel=2)
        return val.isoformat(' ')

    def convert_date(val):
        warn(msg.format(what='date converter'), DeprecationWarning, stacklevel=2)
        return datetime.date(*map(int, val.split(b'-')))

    def convert_timestamp(val):
        warn(msg.format(what='timestamp converter'), DeprecationWarning, stacklevel=2)
        datepart, timepart = val.split(b' ')
        year, month, day = map(int, datepart.split(b'-'))
        timepart_full = timepart.split(b'.')
        hours, minutes, seconds = map(int, timepart_full[0].split(b':'))
        if len(timepart_full) == 2:
            microseconds = int('{:0<6.6}'.format(timepart_full[1].decode()))
        else:
            microseconds = 0
        val = datetime.datetime(year, month, day, hours, minutes, seconds, microseconds)
        return val
    register_adapter(datetime.date, adapt_date)
    register_adapter(datetime.datetime, adapt_datetime)
    register_converter('date', convert_date)
    register_converter('timestamp', convert_timestamp)
register_adapters_and_converters()
del register_adapters_and_converters


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import sqlite3.dbapi2 as _英文库
二进制大对象 = _英文库.Blob
连接 = _英文库.Connection
游标 = _英文库.Cursor
数据错误 = _英文库.DataError
数据库操作错误 = _英文库.DatabaseError
数据库错误 = _英文库.Error
完整性错误 = _英文库.IntegrityError
接口错误 = _英文库.InterfaceError
内部错误 = _英文库.InternalError
旧式事务控制 = _英文库.LEGACY_TRANSACTION_CONTROL
不支持错误 = _英文库.NotSupportedError
操作错误 = _英文库.OperationalError
解析列名 = _英文库.PARSE_COLNAMES
解析声明类型 = _英文库.PARSE_DECLTYPES
准备协议 = _英文库.PrepareProtocol
编程错误 = _英文库.ProgrammingError
行 = _英文库.Row
警告 = _英文库.Warning
适配 = _英文库.adapt
补全语句 = _英文库.complete_statement
连接数据库 = _英文库.connect
启用回调回溯 = _英文库.enable_callback_tracebacks
注册适配器 = _英文库.register_adapter
注册转换器 = _英文库.register_converter
SQLite版本 = _英文库.sqlite_version
线程安全级别 = _英文库.threadsafety
_模块别名 = {
    'Binary': '二进制',
    'Date': '日期',
    'DateFromTicks': '时间戳转日期',
    'Time': '时间',
    'TimeFromTicks': '时间戳转时间',
    'Timestamp': '时间戳',
    'TimestampFromTicks': '时间戳转时间戳',
    'apilevel': 'API级别',
    'paramstyle': '参数风格',
    'sqlite_version_info': 'SQLite版本信息',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
