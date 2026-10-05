# -*- coding: utf-8 -*-
"""日志.__init__ —— 汉语库（由 tools/汉化库.py 从 Lib/logging/__init__.py 机械生成，**不要手改**）。

英文库 Lib/logging.__init__.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py logging
"""


"""
Logging package for Python. Based on PEP 282 and comments thereto in
comp.lang.python.

Copyright (C) 2001-2022 Vinay Sajip. All Rights Reserved.

To use, simply 'import logging' and log away!
"""
_英文原名表 = {'BASIC_FORMAT': '基本格式', 'BufferingFormatter': '缓冲格式化器', 'CRITICAL': '严重级别', 'DEBUG': '调试级别', 'ERROR': '错误级别', 'FATAL': '致命级别', 'FileHandler': '文件处理器', 'Filter': '过滤器', 'Filterer': '可过滤基类', 'Formatter': '格式化器', 'Handler': '处理器', 'INFO': '信息级别', 'LogRecord': '日志记录', 'Logger': '日志器', 'LoggerAdapter': '日志适配器', 'Manager': '管理器', 'NOTSET': '未设置', 'NullHandler': '空处理器', 'PercentStyle': '百分号风格', 'PlaceHolder': '占位处理器', 'RootLogger': '根日志器', 'StrFormatStyle': '大括号风格', 'StreamHandler': '流处理器', 'StringTemplateStyle': '模板风格', 'WARN': '警告级别旧名', 'WARNING': '警告级别', 'addLevelName': '加级别名字', 'captureWarnings': '捕获警告', 'critical': '严重', 'currentframe': '当前帧', 'debug': '调试', 'disable': '停用级别', 'error': '错误', 'exception': '异常', 'fatal': '致命', 'getHandlerByName': '按名字取处理器', 'getHandlerNames': '取处理器名字表', 'getLevelName': '取级别名字', 'getLevelNamesMapping': '取级别名字表', 'getLogRecordFactory': '取日志记录工厂', 'getLogger': '取日志器', 'getLoggerClass': '取日志器类', 'info': '信息', 'makeLogRecord': '造日志记录', 'root': '根', 'setLogRecordFactory': '设日志记录工厂', 'setLoggerClass': '设日志器类', 'shutdown': '关闭', 'warn': '警告旧名', 'warning': '警告'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
_实例属性全表 = {}
_反表 = {}

def _装类转发(_类, _对, _属性=None):
    if getattr(_类, '__module__', None) != __name__:
        return
    for _英, _中 in _对.items():
        if _中 in _类.__dict__:
            setattr(_类, _英, _类.__dict__[_中])
    if _属性:
        _实例属性全表.update(_属性)
        _反表.update({_中: _英 for _英, _中 in _属性.items()})
        for _英, _中 in _属性.items():
            if _英 not in _类.__dict__ and _中 in _类.__dict__:
                setattr(_类, _英, _类.__dict__[_中])
        if '__getattr__' not in _类.__dict__:

            def _取(self, _名, _对=_实例属性全表, _反=_反表):
                if _名 in _对:
                    try:
                        return object.__getattribute__(self, _对[_名])
                    except AttributeError:
                        pass
                    try:
                        return object.__getattribute__(self, _名)
                    except AttributeError:
                        pass
                if _名 in _反:
                    try:
                        return object.__getattribute__(self, _反[_名])
                    except AttributeError:
                        pass
                raise AttributeError(_名)
            try:
                _类.__getattr__ = _取
            except TypeError:
                return
        if not [_基 for _基 in _类.__mro__ if _基 is not object and '__setattr__' in _基.__dict__ and (not getattr(_基.__dict__['__setattr__'], '_中文转发钩子', False))]:

            def _设(self, _名, _值, _对=_实例属性全表, _反=_反表):
                _英 = _名 if _名 in _对 else _反.get(_名)
                if _英 is None:
                    object.__setattr__(self, _名, _值)
                    return
                _中 = _对[_英]
                _成 = False
                for _名2 in (_中, _英):
                    try:
                        object.__setattr__(self, _名2, _值)
                        _成 = True
                    except AttributeError:
                        pass
                if not _成:
                    raise AttributeError(_名)
            _设._中文转发钩子 = True
            try:
                _类.__setattr__ = _设
            except TypeError:
                return
import sys, os, time, io, re, traceback, warnings, weakref, collections.abc
from types import GenericAlias
from string import Template
from string import Formatter as StrFormatter
__all__ = ['BASIC_FORMAT', 'BufferingFormatter', 'CRITICAL', 'DEBUG', 'ERROR', 'FATAL', 'FileHandler', 'Filter', 'Formatter', 'Handler', 'INFO', 'LogRecord', 'Logger', 'LoggerAdapter', 'NOTSET', 'NullHandler', 'StreamHandler', 'WARN', 'WARNING', 'addLevelName', 'basicConfig', 'captureWarnings', 'critical', 'debug', 'disable', 'error', 'exception', 'fatal', 'getLevelName', 'getLogger', 'getLoggerClass', 'info', 'log', 'makeLogRecord', 'setLoggerClass', 'shutdown', 'warn', 'warning', 'getLogRecordFactory', 'setLogRecordFactory', 'lastResort', 'raiseExceptions', 'getLevelNamesMapping', 'getHandlerByName', 'getHandlerNames']
import threading
__author__ = 'Vinay Sajip <vinay_sajip@red-dove.com>'
__status__ = 'production'
__version__ = '0.5.1.2'
__date__ = '07 February 2010'
_startTime = time.time_ns()
raiseExceptions = True
logThreads = True
logMultiprocessing = True
logProcesses = True
logAsyncioTasks = True
严重级别 = 50
致命级别 = 严重级别
错误级别 = 40
警告级别 = 30
警告级别旧名 = 警告级别
信息级别 = 20
调试级别 = 10
未设置 = 0
_levelToName = {严重级别: 'CRITICAL', 错误级别: 'ERROR', 警告级别: 'WARNING', 信息级别: 'INFO', 调试级别: 'DEBUG', 未设置: 'NOTSET'}
_nameToLevel = {'CRITICAL': 严重级别, 'FATAL': 致命级别, 'ERROR': 错误级别, 'WARN': 警告级别, 'WARNING': 警告级别, 'INFO': 信息级别, 'DEBUG': 调试级别, 'NOTSET': 未设置}

def 取级别名字表():
    return _nameToLevel.copy()

def 取级别名字(level):
    """
    Return the textual or numeric representation of logging level 'level'.

    If the level is one of the predefined levels (CRITICAL, ERROR, WARNING,
    INFO, DEBUG) then you get the corresponding string. If you have
    associated levels with names using addLevelName then the name you have
    associated with 'level' is returned.

    If a numeric value corresponding to one of the defined levels is passed
    in, the corresponding string representation is returned.

    If a string representation of the level is passed in, the corresponding
    numeric value is returned.

    If no matching numeric or string value is passed in, the string
    'Level %s' % level is returned.
    """
    result = _levelToName.get(level)
    if result is not None:
        return result
    result = _nameToLevel.get(level)
    if result is not None:
        return result
    return 'Level %s' % level

def 加级别名字(level, levelName):
    """
    Associate 'levelName' with 'level'.

    This is used when converting levels to text during message formatting.
    """
    with _lock:
        _levelToName[level] = levelName
        _nameToLevel[levelName] = level
if hasattr(sys, '_getframe'):
    当前帧 = lambda: sys._getframe(1)
else:

    def 当前帧():
        """Return the frame object for the caller's stack frame."""
        try:
            raise Exception
        except Exception as exc:
            return exc.__traceback__.tb_frame.f_back
_srcfile = os.path.normcase(加级别名字.__code__.co_filename)

def _is_internal_frame(frame):
    """Signal whether the frame is a CPython or logging module internal."""
    filename = os.path.normcase(frame.f_code.co_filename)
    return filename == _srcfile or ('importlib' in filename and '_bootstrap' in filename)

def _checkLevel(level):
    if isinstance(level, int):
        rv = level
    elif str(level) == level:
        if level not in _nameToLevel:
            raise ValueError('Unknown level: %r' % level)
        rv = _nameToLevel[level]
    else:
        raise TypeError('Level not an integer or a valid string: %r' % (level,))
    return rv
_lock = threading.RLock()

def _prepareFork():
    """
    Prepare to fork a new child process by acquiring the module-level lock.

    This should be used in conjunction with _afterFork().
    """
    try:
        _lock.acquire()
    except BaseException:
        _lock.release()
        raise

def _afterFork():
    """
    After a new child process has been forked, release the module-level lock.

    This should be used in conjunction with _prepareFork().
    """
    _lock.release()
if not hasattr(os, 'register_at_fork'):

    def _register_at_fork_reinit_lock(instance):
        pass
else:
    _at_fork_reinit_lock_weakset = weakref.WeakSet()

    def _register_at_fork_reinit_lock(instance):
        with _lock:
            _at_fork_reinit_lock_weakset.add(instance)

    def _after_at_fork_child_reinit_locks():
        for handler in _at_fork_reinit_lock_weakset:
            handler._at_fork_reinit()
        _lock._at_fork_reinit()
    os.register_at_fork(before=_prepareFork, after_in_child=_after_at_fork_child_reinit_locks, after_in_parent=_afterFork)

class 日志记录(object):
    """
    A LogRecord instance represents an event being logged.

    LogRecord instances are created every time something is logged. They
    contain all the information pertinent to the event being logged. The
    main information passed in is in msg and args, which are combined
    using str(msg) % args to create the message field of the record. The
    record also includes information such as when the record was created,
    the source line where the logging call was made, and any exception
    information to be logged.
    """

    def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None, **kwargs):
        """
        Initialize a logging record with interesting information.
        """
        ct = time.time_ns()
        self.name = name
        self.msg = msg
        if args and len(args) == 1 and isinstance(args[0], collections.abc.Mapping) and args[0]:
            args = args[0]
        self.args = args
        self.levelname = 取级别名字(level)
        self.levelno = level
        self.pathname = pathname
        try:
            self.filename = os.path.basename(pathname)
            self.module = os.path.splitext(self.filename)[0]
        except (TypeError, ValueError, AttributeError):
            self.filename = pathname
            self.module = 'Unknown module'
        self.exc_info = exc_info
        self.exc_text = None
        self.stack_info = sinfo
        self.lineno = lineno
        self.funcName = func
        self.created = ct / 1000000000.0
        self.msecs = ct % 1000000000 // 1000000 + 0.0
        if self.msecs == 999.0 and int(self.created) != ct // 1000000000:
            self.msecs = 0.0
        self.relativeCreated = (ct - _startTime) / 1000000.0
        if logThreads:
            self.thread = threading.get_ident()
            self.threadName = threading.current_thread().name
        else:
            self.thread = None
            self.threadName = None
        if not logMultiprocessing:
            self.processName = None
        else:
            self.processName = 'MainProcess'
            mp = sys.modules.get('multiprocessing')
            if mp is not None:
                try:
                    self.processName = mp.current_process().name
                except Exception:
                    pass
        if logProcesses and hasattr(os, 'getpid'):
            self.process = os.getpid()
        else:
            self.process = None
        self.taskName = None
        if logAsyncioTasks:
            asyncio = sys.modules.get('asyncio')
            if asyncio:
                try:
                    self.taskName = asyncio.current_task().get_name()
                except Exception:
                    pass

    def __repr__(self):
        return '<LogRecord: %s, %s, %s, %s, "%s">' % (self.name, self.levelno, self.pathname, self.lineno, self.msg)

    def 取消息(self):
        """
        Return the message for this LogRecord.

        Return the message for this LogRecord after merging any user-supplied
        arguments with the message.
        """
        msg = str(self.msg)
        if self.args:
            msg = msg % self.args
        return msg
_装类转发(日志记录, {'getMessage': '取消息'}, {'getMessage': '取消息'})
_logRecordFactory = 日志记录

def 设日志记录工厂(factory):
    """
    Set the factory to be used when instantiating a log record.

    :param factory: A callable which will be called to instantiate
    a log record.
    """
    global _logRecordFactory
    _logRecordFactory = factory

def 取日志记录工厂():
    """
    Return the factory to be used when instantiating a log record.
    """
    return _logRecordFactory

def 造日志记录(dict):
    """
    Make a LogRecord whose attributes are defined by the specified dictionary,
    This function is useful for converting a logging event received over
    a socket connection (which is sent as a dictionary) into a LogRecord
    instance.
    """
    rv = _logRecordFactory(None, None, '', 0, '', (), None, None)
    rv.__dict__.update(dict)
    return rv
_str_formatter = StrFormatter()
del StrFormatter

class 百分号风格(object):
    default_format = '%(message)s'
    asctime_format = '%(asctime)s'
    asctime_search = '%(asctime)'
    validation_pattern = re.compile('%\\(\\w+\\)[#0+ -]*(\\*|\\d+)?(\\.(\\*|\\d+))?[diouxefgcrsa%]', re.I)

    def __init__(self, fmt, *, defaults=None):
        self._fmt = fmt or self.default_format
        self._defaults = defaults

    def usesTime(self):
        return self._fmt.find(self.asctime_search) >= 0

    def validate(self):
        """Validate the input format, ensure it matches the correct style"""
        if not self.validation_pattern.search(self._fmt):
            raise ValueError("Invalid format '%s' for '%s' style" % (self._fmt, self.default_format[0]))

    def _format(self, record):
        if (defaults := self._defaults):
            values = defaults | record.__dict__
        else:
            values = record.__dict__
        return self._fmt % values

    def format(self, record):
        try:
            return self._format(record)
        except KeyError as e:
            raise ValueError('Formatting field not found in record: %s' % e)

class 大括号风格(百分号风格):
    default_format = '{message}'
    asctime_format = '{asctime}'
    asctime_search = '{asctime'
    fmt_spec = re.compile('^(.?[<>=^])?[+ -]?#?0?(\\d+|{\\w+})?[,_]?(\\.(\\d+|{\\w+}))?[bcdefgnosx%]?$', re.I)
    field_spec = re.compile('^(\\d+|\\w+)(\\.\\w+|\\[[^]]+\\])*$')

    def _format(self, record):
        if (defaults := self._defaults):
            values = defaults | record.__dict__
        else:
            values = record.__dict__
        return self._fmt.format(**values)

    def validate(self):
        """Validate the input format, ensure it is the correct string formatting style"""
        fields = set()
        try:
            for _, fieldname, spec, conversion in _str_formatter.parse(self._fmt):
                if fieldname:
                    if not self.field_spec.match(fieldname):
                        raise ValueError('invalid field name/expression: %r' % fieldname)
                    fields.add(fieldname)
                if conversion and conversion not in 'rsa':
                    raise ValueError('invalid conversion: %r' % conversion)
                if spec and (not self.fmt_spec.match(spec)):
                    raise ValueError('bad specifier: %r' % spec)
        except ValueError as e:
            raise ValueError('invalid format: %s' % e)
        if not fields:
            raise ValueError('invalid format: no fields')

class 模板风格(百分号风格):
    default_format = '${message}'
    asctime_format = '${asctime}'
    asctime_search = '${asctime}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._tpl = Template(self._fmt)

    def usesTime(self):
        fmt = self._fmt
        return fmt.find('$asctime') >= 0 or fmt.find(self.asctime_search) >= 0

    def validate(self):
        pattern = Template.pattern
        fields = set()
        for m in pattern.finditer(self._fmt):
            d = m.groupdict()
            if d['named']:
                fields.add(d['named'])
            elif d['braced']:
                fields.add(d['braced'])
            elif m.group(0) == '$':
                raise ValueError("invalid format: bare '$' not allowed")
        if not fields:
            raise ValueError('invalid format: no fields')

    def _format(self, record):
        if (defaults := self._defaults):
            values = defaults | record.__dict__
        else:
            values = record.__dict__
        return self._tpl.substitute(**values)
基本格式 = '%(levelname)s:%(name)s:%(message)s'
_STYLES = {'%': (百分号风格, 基本格式), '{': (大括号风格, '{levelname}:{name}:{message}'), '$': (模板风格, '${levelname}:${name}:${message}')}

class 格式化器(object):
    """
    Formatter instances are used to convert a LogRecord to text.

    Formatters need to know how a LogRecord is constructed. They are
    responsible for converting a LogRecord to (usually) a string which can
    be interpreted by either a human or an external system. The base Formatter
    allows a formatting string to be specified. If none is supplied, the
    style-dependent default value, "%(message)s", "{message}", or
    "${message}", is used.

    The Formatter can be initialized with a format string which makes use of
    knowledge of the LogRecord attributes - e.g. the default value mentioned
    above makes use of the fact that the user's message and arguments are pre-
    formatted into a LogRecord's message attribute. Currently, the useful
    attributes in a LogRecord are described by:

    %(name)s            Name of the logger (logging channel)
    %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                        WARNING, ERROR, CRITICAL)
    %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                        "WARNING", "ERROR", "CRITICAL")
    %(pathname)s        Full pathname of the source file where the logging
                        call was issued (if available)
    %(filename)s        Filename portion of pathname
    %(module)s          Module (name portion of filename)
    %(lineno)d          Source line number where the logging call was issued
                        (if available)
    %(funcName)s        Function name
    %(created)f         Time when the LogRecord was created (time.time_ns() / 1e9
                        return value)
    %(asctime)s         Textual time when the LogRecord was created
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          Thread ID (if available)
    %(threadName)s      Thread name (if available)
    %(taskName)s        Task name (if available)
    %(process)d         Process ID (if available)
    %(processName)s     Process name (if available)
    %(message)s         The result of record.getMessage(), computed just as
                        the record is emitted
    """
    converter = time.localtime

    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
        """
        Initialize the formatter with specified format strings.

        Initialize the formatter either with the specified format string, or a
        default as described above. Allow for specialized date formatting with
        the optional datefmt argument. If datefmt is omitted, you get an
        ISO8601-like (or RFC 3339-like) format.

        Use a style parameter of '%', '{' or '$' to specify that you want to
        use one of %-formatting, :meth:`str.format` (``{}``) formatting or
        :class:`string.Template` formatting in your format string.

        .. versionchanged:: 3.2
           Added the ``style`` parameter.
        """
        if style not in _STYLES:
            raise ValueError('Style must be one of: %s' % ','.join(_STYLES.keys()))
        self._style = _STYLES[style][0](fmt, defaults=defaults)
        if validate:
            self._style.validate()
        self._fmt = self._style._fmt
        self.datefmt = datefmt
    default_time_format = '%Y-%m-%d %H:%M:%S'
    default_msec_format = '%s,%03d'

    def formatTime(self, record, datefmt=None):
        """
        Return the creation time of the specified LogRecord as formatted text.

        This method should be called from format() by a formatter which
        wants to make use of a formatted time. This method can be overridden
        in formatters to provide for any specific requirement, but the
        basic behaviour is as follows: if datefmt (a string) is specified,
        it is used with time.strftime() to format the creation time of the
        record. Otherwise, an ISO8601-like (or RFC 3339-like) format is used.
        The resulting string is returned. This function uses a user-configurable
        function to convert the creation time to a tuple. By default,
        time.localtime() is used; to change this for a particular formatter
        instance, set the 'converter' attribute to a function with the same
        signature as time.localtime() or time.gmtime(). To change it for all
        formatters, for example if you want all logging times to be shown in GMT,
        set the 'converter' attribute in the Formatter class.
        """
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = time.strftime(self.default_time_format, ct)
            if self.default_msec_format:
                s = self.default_msec_format % (s, record.msecs)
        return s

    def formatException(self, ei):
        """
        Format and return the specified exception information as a string.

        This default implementation just uses
        traceback.print_exception()
        """
        sio = io.StringIO()
        tb = ei[2]
        traceback.print_exception(ei[0], ei[1], tb, limit=None, file=sio)
        s = sio.getvalue()
        sio.close()
        if s[-1:] == '\n':
            s = s[:-1]
        return s

    def usesTime(self):
        """
        Check if the format uses the creation time of the record.
        """
        return self._style.usesTime()

    def formatMessage(self, record):
        return self._style.format(record)

    def formatStack(self, stack_info):
        """
        This method is provided as an extension point for specialized
        formatting of stack information.

        The input data is a string as returned from a call to
        :func:`traceback.print_stack`, but with the last trailing newline
        removed.

        The base implementation just returns the value passed in.
        """
        return stack_info

    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()
        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)
        s = self.formatMessage(record)
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != '\n':
                s = s + '\n'
            s = s + record.exc_text
        if record.stack_info:
            if s[-1:] != '\n':
                s = s + '\n'
            s = s + self.formatStack(record.stack_info)
        return s
_defaultFormatter = 格式化器()

class 缓冲格式化器(object):
    """
    A formatter suitable for formatting a number of records.
    """

    def __init__(self, linefmt=None):
        """
        Optionally specify a formatter which will be used to format each
        individual record.
        """
        if linefmt:
            self.linefmt = linefmt
        else:
            self.linefmt = _defaultFormatter

    def formatHeader(self, records):
        """
        Return the header string for the specified records.
        """
        return ''

    def formatFooter(self, records):
        """
        Return the footer string for the specified records.
        """
        return ''

    def format(self, records):
        """
        Format the specified records and return the result as a string.
        """
        rv = ''
        if len(records) > 0:
            rv = rv + self.formatHeader(records)
            for record in records:
                rv = rv + self.linefmt.format(record)
            rv = rv + self.formatFooter(records)
        return rv

class 过滤器(object):
    """
    Filter instances are used to perform arbitrary filtering of LogRecords.

    Loggers and Handlers can optionally use Filter instances to filter
    records as desired. The base filter class only allows events which are
    below a certain point in the logger hierarchy. For example, a filter
    initialized with "A.B" will allow events logged by loggers "A.B",
    "A.B.C", "A.B.C.D", "A.B.D" etc. but not "A.BB", "B.A.B" etc. If
    initialized with the empty string, all events are passed.
    """

    def __init__(self, name=''):
        """
        Initialize a filter.

        Initialize with the name of the logger which, together with its
        children, will have its events allowed through the filter. If no
        name is specified, allow every event.
        """
        self.name = name
        self.nlen = len(name)

    def filter(self, record):
        """
        Determine if the specified record is to be logged.

        Returns True if the record should be logged, or False otherwise.
        If deemed appropriate, the record may be modified in-place.
        """
        if self.nlen == 0:
            return True
        elif self.name == record.name:
            return True
        elif record.name.find(self.name, 0, self.nlen) != 0:
            return False
        return record.name[self.nlen] == '.'

class 可过滤基类(object):
    """
    A base class for loggers and handlers which allows them to share
    common code.
    """

    def __init__(self):
        """
        Initialize the list of filters to be an empty list.
        """
        self.filters = []

    def 加过滤器(self, filter):
        """
        Add the specified filter to this handler.
        """
        if not filter in self.filters:
            self.filters.append(filter)

    def 去过滤器(self, filter):
        """
        Remove the specified filter from this handler.
        """
        if filter in self.filters:
            self.filters.remove(filter)

    def filter(self, record):
        """
        Determine if a record is loggable by consulting all the filters.

        The default is to allow the record to be logged; any filter can veto
        this by returning a false value.
        If a filter attached to a handler returns a log record instance,
        then that instance is used in place of the original log record in
        any further processing of the event by that handler.
        If a filter returns any other true value, the original log record
        is used in any further processing of the event by that handler.

        If none of the filters return false values, this method returns
        a log record.
        If any of the filters return a false value, this method returns
        a false value.

        .. versionchanged:: 3.2

           Allow filters to be just callables.

        .. versionchanged:: 3.12
           Allow filters to return a LogRecord instead of
           modifying it in place.
        """
        for f in self.filters:
            if hasattr(f, 'filter'):
                result = f.filter(record)
            else:
                result = f(record)
            if not result:
                return False
            if isinstance(result, 日志记录):
                record = result
        return record
_装类转发(可过滤基类, {'addFilter': '加过滤器', 'removeFilter': '去过滤器'}, {'addFilter': '加过滤器', 'removeFilter': '去过滤器'})
_handlers = weakref.WeakValueDictionary()
_handlerList = []

def _removeHandlerRef(wr):
    """
    Remove a handler reference from the internal cleanup list.
    """
    handlers, lock = (_handlerList, _lock)
    if lock and handlers:
        with lock:
            try:
                handlers.remove(wr)
            except ValueError:
                pass

def _addHandlerRef(handler):
    """
    Add a handler to the internal cleanup list using a weak reference.
    """
    with _lock:
        _handlerList.append(weakref.ref(handler, _removeHandlerRef))

def 按名字取处理器(name):
    """
    Get a handler with the specified *name*, or None if there isn't one with
    that name.
    """
    return _handlers.get(name)

def 取处理器名字表():
    """
    Return all known handler names as an immutable set.
    """
    return frozenset(_handlers)

class 处理器(可过滤基类):
    """
    Handler instances dispatch logging events to specific destinations.

    The base handler class. Acts as a placeholder which defines the Handler
    interface. Handlers can optionally use Formatter instances to format
    records as desired. By default, no formatter is specified; in this case,
    the 'raw' message as determined by record.message is logged.
    """

    def __init__(self, level=未设置):
        """
        Initializes the instance - basically setting the formatter to None
        and the filter list to empty.
        """
        可过滤基类.__init__(self)
        self._name = None
        self.level = _checkLevel(level)
        self.formatter = None
        self._closed = False
        _addHandlerRef(self)
        self.createLock()

    def get_name(self):
        return self._name

    def set_name(self, name):
        with _lock:
            if self._name in _handlers:
                del _handlers[self._name]
            self._name = name
            if name:
                _handlers[name] = self
    name = property(get_name, set_name)

    def createLock(self):
        """
        Acquire a thread lock for serializing access to the underlying I/O.
        """
        self.lock = threading.RLock()
        _register_at_fork_reinit_lock(self)

    def _at_fork_reinit(self):
        self.lock._at_fork_reinit()

    def acquire(self):
        """
        Acquire the I/O thread lock.
        """
        if self.lock:
            self.lock.acquire()

    def release(self):
        """
        Release the I/O thread lock.
        """
        if self.lock:
            self.lock.release()

    def 设级别(self, level):
        """
        Set the logging level of this handler.  level must be an int or a str.
        """
        self.level = _checkLevel(level)

    def format(self, record):
        """
        Format the specified record.

        If a formatter is set, use it. Otherwise, use the default formatter
        for the module.
        """
        if self.formatter:
            fmt = self.formatter
        else:
            fmt = _defaultFormatter
        return fmt.format(record)

    def emit(self, record):
        """
        Do whatever it takes to actually log the specified logging record.

        This version is intended to be implemented by subclasses and so
        raises a NotImplementedError.
        """
        raise NotImplementedError('emit must be implemented by Handler subclasses')

    def handle(self, record):
        """
        Conditionally emit the specified logging record.

        Emission depends on filters which may have been added to the handler.
        Wrap the actual emission of the record with acquisition/release of
        the I/O thread lock.

        Returns an instance of the log record that was emitted
        if it passed all filters, otherwise a false value is returned.
        """
        rv = self.filter(record)
        if isinstance(rv, 日志记录):
            record = rv
        if rv:
            with self.lock:
                self.emit(record)
        return rv

    def 设格式化器(self, fmt):
        """
        Set the formatter for this handler.
        """
        self.formatter = fmt

    def flush(self):
        """
        Ensure all logging output has been flushed.

        This version does nothing and is intended to be implemented by
        subclasses.
        """
        pass

    def close(self):
        """
        Tidy up any resources used by the handler.

        This version removes the handler from an internal map of handlers,
        _handlers, which is used for handler lookup by name. Subclasses
        should ensure that this gets called from overridden close()
        methods.
        """
        with _lock:
            self._closed = True
            if self._name and self._name in _handlers:
                del _handlers[self._name]

    def handleError(self, record):
        """
        Handle errors which occur during an emit() call.

        This method should be called from handlers when an exception is
        encountered during an emit() call. If raiseExceptions is false,
        exceptions get silently ignored. This is what is mostly wanted
        for a logging system - most users will not care about errors in
        the logging system, they are more interested in application errors.
        You could, however, replace this with a custom handler if you wish.
        The record which was being processed is passed in to this method.
        """
        if raiseExceptions and sys.stderr:
            exc = sys.exception()
            try:
                sys.stderr.write('--- Logging error ---\n')
                traceback.print_exception(exc, limit=None, file=sys.stderr)
                sys.stderr.write('Call stack:\n')
                frame = exc.__traceback__.tb_frame
                while frame and os.path.dirname(frame.f_code.co_filename) == __path__[0]:
                    frame = frame.f_back
                if frame:
                    traceback.print_stack(frame, file=sys.stderr)
                else:
                    sys.stderr.write('Logged from file %s, line %s\n' % (record.filename, record.lineno))
                try:
                    sys.stderr.write('Message: %r\nArguments: %s\n' % (record.msg, record.args))
                except RecursionError:
                    raise
                except Exception:
                    sys.stderr.write('Unable to print the message and arguments - possible formatting error.\nUse the traceback above to help find the error.\n')
            except OSError:
                pass
            finally:
                del exc

    def __repr__(self):
        level = 取级别名字(self.level)
        return '<%s (%s)>' % (self.__class__.__name__, level)
_装类转发(处理器, {'setFormatter': '设格式化器', 'setLevel': '设级别'}, {'setFormatter': '设格式化器', 'setLevel': '设级别'})

class 流处理器(处理器):
    """
    A handler class which writes logging records, appropriately formatted,
    to a stream. Note that this class does not close the stream, as
    sys.stdout or sys.stderr may be used.
    """
    terminator = '\n'

    def __init__(self, stream=None):
        """
        Initialize the handler.

        If stream is not specified, sys.stderr is used.
        """
        处理器.__init__(self)
        if stream is None:
            stream = sys.stderr
        self.stream = stream

    def flush(self):
        """
        Flushes the stream.
        """
        with self.lock:
            if self.stream and hasattr(self.stream, 'flush'):
                self.stream.flush()

    def emit(self, record):
        """
        Emit a record.

        If a formatter is specified, it is used to format the record.
        The record is then written to the stream with a trailing newline.  If
        exception information is present, it is formatted using
        traceback.print_exception and appended to the stream.  If the stream
        has an 'encoding' attribute, it is used to determine how to do the
        output to the stream.
        """
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg + self.terminator)
            self.flush()
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)

    def setStream(self, stream):
        """
        Sets the StreamHandler's stream to the specified value,
        if it is different.

        Returns the old stream, if the stream was changed, or None
        if it wasn't.
        """
        if stream is self.stream:
            result = None
        else:
            result = self.stream
            with self.lock:
                self.flush()
                self.stream = stream
        return result

    def __repr__(self):
        level = 取级别名字(self.level)
        name = getattr(self.stream, 'name', '')
        name = str(name)
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)
    __class_getitem__ = classmethod(GenericAlias)

class 文件处理器(流处理器):
    """
    A handler class which writes formatted logging records to disk files.
    """

    def __init__(self, filename, mode='a', encoding=None, delay=False, errors=None):
        """
        Open the specified file and use it as the stream for logging.
        """
        filename = os.fspath(filename)
        self.baseFilename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        if 'b' not in mode:
            self.encoding = io.text_encoding(encoding)
        self.errors = errors
        self.delay = delay
        self._builtin_open = open
        if delay:
            处理器.__init__(self)
            self.stream = None
        else:
            流处理器.__init__(self, self._open())

    def close(self):
        """
        Closes the stream.
        """
        with self.lock:
            try:
                if self.stream:
                    try:
                        self.flush()
                    finally:
                        stream = self.stream
                        self.stream = None
                        if hasattr(stream, 'close'):
                            stream.close()
            finally:
                流处理器.close(self)

    def _open(self):
        """
        Open the current base file with the (original) mode and encoding.
        Return the resulting stream.
        """
        open_func = self._builtin_open
        return open_func(self.baseFilename, self.mode, encoding=self.encoding, errors=self.errors)

    def emit(self, record):
        """
        Emit a record.

        If the stream was not opened because 'delay' was specified in the
        constructor, open it before calling the superclass's emit.

        If stream is not open, current mode is 'w' and `_closed=True`, record
        will not be emitted (see Issue #42378).
        """
        if self.stream is None:
            if self.mode != 'w' or not self._closed:
                self.stream = self._open()
        if self.stream:
            流处理器.emit(self, record)

    def __repr__(self):
        level = 取级别名字(self.level)
        return '<%s %s (%s)>' % (self.__class__.__name__, self.baseFilename, level)

class _StderrHandler(流处理器):
    """
    This class is like a StreamHandler using sys.stderr, but always uses
    whatever sys.stderr is currently set to rather than the value of
    sys.stderr at handler construction time.
    """

    def __init__(self, level=未设置):
        """
        Initialize the handler.
        """
        处理器.__init__(self, level)

    @property
    def stream(self):
        return sys.stderr
_defaultLastResort = _StderrHandler(警告级别)
lastResort = _defaultLastResort

class 占位处理器(object):
    """
    PlaceHolder instances are used in the Manager logger hierarchy to take
    the place of nodes for which no loggers have been defined. This class is
    intended for internal use only and not as part of the public API.
    """

    def __init__(self, alogger):
        """
        Initialize with the specified logger being a child of this placeholder.
        """
        self.loggerMap = {alogger: None}

    def append(self, alogger):
        """
        Add the specified logger as a child of this placeholder.
        """
        if alogger not in self.loggerMap:
            self.loggerMap[alogger] = None

def 设日志器类(klass):
    """
    Set the class to be used when instantiating a logger. The class should
    define __init__() such that only a name argument is required, and the
    __init__() should call Logger.__init__()
    """
    if klass != 日志器:
        if not issubclass(klass, 日志器):
            raise TypeError('logger not derived from logging.Logger: ' + klass.__name__)
    global _loggerClass
    _loggerClass = klass

def 取日志器类():
    """
    Return the class to be used when instantiating a logger.
    """
    return _loggerClass

class 管理器(object):
    """
    There is [under normal circumstances] just one Manager instance, which
    holds the hierarchy of loggers.
    """

    def __init__(self, rootnode):
        """
        Initialize the manager with the root node of the logger hierarchy.
        """
        self.根 = rootnode
        self.停用级别 = 0
        self.emittedNoHandlerWarning = False
        self.loggerDict = {}
        self.loggerClass = None
        self.logRecordFactory = None

    @property
    def 停用级别(self):
        return self._disable

    @停用级别.setter
    def 停用级别(self, value):
        self._disable = _checkLevel(value)

    def 取日志器(self, name):
        """
        Get a logger with the specified name (channel name), creating it
        if it doesn't yet exist. This name is a dot-separated hierarchical
        name, such as "a", "a.b", "a.b.c" or similar.

        If a PlaceHolder existed for the specified name [i.e. the logger
        didn't exist but a child of it did], replace it with the created
        logger and fix up the parent/child references which pointed to the
        placeholder to now point to the logger.
        """
        rv = None
        if not isinstance(name, str):
            raise TypeError('A logger name must be a string')
        with _lock:
            if name in self.loggerDict:
                rv = self.loggerDict[name]
                if isinstance(rv, 占位处理器):
                    ph = rv
                    rv = (self.loggerClass or _loggerClass)(name)
                    rv.manager = self
                    self.loggerDict[name] = rv
                    self._fixupChildren(ph, rv)
                    self._fixupParents(rv)
            else:
                rv = (self.loggerClass or _loggerClass)(name)
                rv.manager = self
                self.loggerDict[name] = rv
                self._fixupParents(rv)
        return rv

    def 设日志器类(self, klass):
        """
        Set the class to be used when instantiating a logger with this Manager.
        """
        if klass != 日志器:
            if not issubclass(klass, 日志器):
                raise TypeError('logger not derived from logging.Logger: ' + klass.__name__)
        self.loggerClass = klass

    def 设日志记录工厂(self, factory):
        """
        Set the factory to be used when instantiating a log record with this
        Manager.
        """
        self.logRecordFactory = factory

    def _fixupParents(self, alogger):
        """
        Ensure that there are either loggers or placeholders all the way
        from the specified logger to the root of the logger hierarchy.
        """
        name = alogger.name
        i = name.rfind('.')
        rv = None
        while i > 0 and (not rv):
            substr = name[:i]
            if substr not in self.loggerDict:
                self.loggerDict[substr] = 占位处理器(alogger)
            else:
                obj = self.loggerDict[substr]
                if isinstance(obj, 日志器):
                    rv = obj
                else:
                    assert isinstance(obj, 占位处理器)
                    obj.append(alogger)
            i = name.rfind('.', 0, i - 1)
        if not rv:
            rv = self.根
        alogger.parent = rv

    def _fixupChildren(self, ph, alogger):
        """
        Ensure that children of the placeholder ph are connected to the
        specified logger.
        """
        name = alogger.name
        namelen = len(name)
        for c in ph.loggerMap.keys():
            if c.parent.name[:namelen] != name:
                alogger.parent = c.parent
                c.parent = alogger

    def _clear_cache(self):
        """
        Clear the cache for all loggers in loggerDict
        Called when level changes are made
        """
        with _lock:
            for logger in self.loggerDict.values():
                if isinstance(logger, 日志器):
                    logger._cache.clear()
            self.根._cache.clear()
_装类转发(管理器, {'disable': '停用级别', 'getLogger': '取日志器', 'setLogRecordFactory': '设日志记录工厂', 'setLoggerClass': '设日志器类'}, {'disable': '停用级别', 'getLogger': '取日志器', 'root': '根', 'setLogRecordFactory': '设日志记录工厂', 'setLoggerClass': '设日志器类'})

class 日志器(可过滤基类):
    """
    Instances of the Logger class represent a single logging channel. A
    "logging channel" indicates an area of an application. Exactly how an
    "area" is defined is up to the application developer. Since an
    application can have any number of areas, logging channels are identified
    by a unique string. Application areas can be nested (e.g. an area
    of "input processing" might include sub-areas "read CSV files", "read
    XLS files" and "read Gnumeric files"). To cater for this natural nesting,
    channel names are organized into a namespace hierarchy where levels are
    separated by periods, much like the Java or Python package namespace. So
    in the instance given above, channel names might be "input" for the upper
    level, and "input.csv", "input.xls" and "input.gnu" for the sub-levels.
    There is no arbitrary limit to the depth of nesting.
    """

    def __init__(self, name, level=未设置):
        """
        Initialize the logger with a name and an optional level.
        """
        可过滤基类.__init__(self)
        self.name = name
        self.level = _checkLevel(level)
        self.parent = None
        self.propagate = True
        self.handlers = []
        self.disabled = False
        self._cache = {}

    def 设级别(self, level):
        """
        Set the logging level of this logger.  level must be an int or a str.
        """
        self.level = _checkLevel(level)
        self.manager._clear_cache()

    def 调试(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'DEBUG'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.debug("Houston, we have a %s", "thorny problem", exc_info=True)
        """
        if self.对该级别启用吗(调试级别):
            self._log(调试级别, msg, args, **kwargs)

    def 信息(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'INFO'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "notable problem", exc_info=True)
        """
        if self.对该级别启用吗(信息级别):
            self._log(信息级别, msg, args, **kwargs)

    def 警告(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'WARNING'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.warning("Houston, we have a %s", "bit of a problem", exc_info=True)
        """
        if self.对该级别启用吗(警告级别):
            self._log(警告级别, msg, args, **kwargs)

    def 警告旧名(self, msg, *args, **kwargs):
        warnings.warn("The 'warn' method is deprecated, use 'warning' instead", DeprecationWarning, 2)
        self.警告(msg, *args, **kwargs)

    def 错误(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'ERROR'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.error("Houston, we have a %s", "major problem", exc_info=True)
        """
        if self.对该级别启用吗(错误级别):
            self._log(错误级别, msg, args, **kwargs)

    def 异常(self, msg, *args, exc_info=True, **kwargs):
        """
        Convenience method for logging an ERROR with exception information.
        """
        self.错误(msg, *args, exc_info=exc_info, **kwargs)

    def 严重(self, msg, *args, **kwargs):
        """
        Log 'msg % args' with severity 'CRITICAL'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.critical("Houston, we have a %s", "major disaster", exc_info=True)
        """
        if self.对该级别启用吗(严重级别):
            self._log(严重级别, msg, args, **kwargs)

    def 致命(self, msg, *args, **kwargs):
        """
        Don't use this method, use critical() instead.
        """
        self.严重(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """
        Log 'msg % args' with the integer severity 'level'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.log(level, "We have a %s", "mysterious problem", exc_info=True)
        """
        if not isinstance(level, int):
            if raiseExceptions:
                raise TypeError('level must be an integer')
            else:
                return
        if self.对该级别启用吗(level):
            self._log(level, msg, args, **kwargs)

    def findCaller(self, stack_info=False, stacklevel=1):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = 当前帧()
        if f is None:
            return ('(unknown file)', 0, '(unknown function)', None)
        while stacklevel > 0:
            next_f = f.f_back
            if next_f is None:
                break
            f = next_f
            if not _is_internal_frame(f):
                stacklevel -= 1
        co = f.f_code
        sinfo = None
        if stack_info:
            with io.StringIO() as sio:
                sio.write('Stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
        return (co.co_filename, f.f_lineno, co.co_name, sinfo)

    def makeRecord(self, name, level, fn, lno, msg, args, exc_info, func=None, extra=None, sinfo=None):
        """
        A factory method which can be overridden in subclasses to create
        specialized LogRecords.
        """
        rv = _logRecordFactory(name, level, fn, lno, msg, args, exc_info, func, sinfo)
        if extra is not None:
            for key in extra:
                if key in ['message', 'asctime'] or key in rv.__dict__:
                    raise KeyError('Attempt to overwrite %r in LogRecord' % key)
                rv.__dict__[key] = extra[key]
        return rv

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        sinfo = None
        if _srcfile:
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info, stacklevel)
            except ValueError:
                fn, lno, func = ('(unknown file)', 0, '(unknown function)')
        else:
            fn, lno, func = ('(unknown file)', 0, '(unknown function)')
        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)
        self.handle(record)

    def handle(self, record):
        """
        Call the handlers for the specified record.

        This method is used for unpickled records received from a socket, as
        well as those created locally. Logger-level filtering is applied.
        """
        if self.disabled:
            return
        maybe_record = self.filter(record)
        if not maybe_record:
            return
        if isinstance(maybe_record, 日志记录):
            record = maybe_record
        self.callHandlers(record)

    def addHandler(self, hdlr):
        """
        Add the specified handler to this logger.
        """
        with _lock:
            if not hdlr in self.handlers:
                self.handlers.append(hdlr)

    def removeHandler(self, hdlr):
        """
        Remove the specified handler from this logger.
        """
        with _lock:
            if hdlr in self.handlers:
                handlers = self.handlers.copy()
                handlers.remove(hdlr)
                self.handlers = handlers

    def hasHandlers(self):
        """
        See if this logger has any handlers configured.

        Loop through all handlers for this logger and its parents in the
        logger hierarchy. Return True if a handler was found, else False.
        Stop searching up the hierarchy whenever a logger with the "propagate"
        attribute set to zero is found - that will be the last logger which
        is checked for the existence of handlers.
        """
        c = self
        rv = False
        while c:
            if c.handlers:
                rv = True
                break
            if not c.propagate:
                break
            else:
                c = c.parent
        return rv

    def callHandlers(self, record):
        """
        Pass a record to all relevant handlers.

        Loop through all handlers for this logger and its parents in the
        logger hierarchy. If no handler was found, output a one-off error
        message to sys.stderr. Stop searching up the hierarchy whenever a
        logger with the "propagate" attribute set to zero is found - that
        will be the last logger whose handlers are called.
        """
        c = self
        found = 0
        while c:
            for hdlr in c.handlers:
                found = found + 1
                if record.levelno >= hdlr.level:
                    hdlr.handle(record)
            if not c.propagate:
                c = None
            else:
                c = c.parent
        if found == 0:
            if lastResort:
                if record.levelno >= lastResort.level:
                    lastResort.handle(record)
            elif raiseExceptions and (not self.manager.emittedNoHandlerWarning):
                sys.stderr.write('No handlers could be found for logger "%s"\n' % self.name)
                self.manager.emittedNoHandlerWarning = True

    def 取有效级别(self):
        """
        Get the effective level for this logger.

        Loop through this logger and its parents in the logger hierarchy,
        looking for a non-zero logging level. Return the first one found.
        """
        logger = self
        while logger:
            if logger.level:
                return logger.level
            logger = logger.parent
        return 未设置

    def 对该级别启用吗(self, level):
        """
        Is this logger enabled for level 'level'?
        """
        if self.disabled:
            return False
        try:
            return self._cache[level]
        except KeyError:
            with _lock:
                if self.manager.disable >= level:
                    is_enabled = self._cache[level] = False
                else:
                    is_enabled = self._cache[level] = level >= self.取有效级别()
            return is_enabled

    def 取子日志器(self, suffix):
        """
        Get a logger which is a descendant to this one.

        This is a convenience method, such that

        logging.getLogger('abc').getChild('def.ghi')

        is the same as

        logging.getLogger('abc.def.ghi')

        It's useful, for example, when the parent logger is named using
        __name__ rather than a literal string.
        """
        if self.根 is not self:
            suffix = '.'.join((self.name, suffix))
        return self.manager.getLogger(suffix)

    def getChildren(self):

        def _hierlevel(logger):
            if logger is logger.manager.root:
                return 0
            return 1 + logger.name.count('.')
        d = self.manager.loggerDict
        with _lock:
            return set((item for item in d.values() if isinstance(item, 日志器) and item.parent is self and (_hierlevel(item) == 1 + _hierlevel(item.parent))))

    def __repr__(self):
        level = 取级别名字(self.取有效级别())
        return '<%s %s (%s)>' % (self.__class__.__name__, self.name, level)

    def __reduce__(self):
        if 取日志器(self.name) is not self:
            import pickle
            raise pickle.PicklingError('logger cannot be pickled')
        return (取日志器, (self.name,))
_装类转发(日志器, {'critical': '严重', 'debug': '调试', 'error': '错误', 'exception': '异常', 'fatal': '致命', 'getChild': '取子日志器', 'getEffectiveLevel': '取有效级别', 'info': '信息', 'isEnabledFor': '对该级别启用吗', 'setLevel': '设级别', 'warn': '警告旧名', 'warning': '警告'}, {'critical': '严重', 'debug': '调试', 'error': '错误', 'exception': '异常', 'fatal': '致命', 'getChild': '取子日志器', 'getEffectiveLevel': '取有效级别', 'info': '信息', 'isEnabledFor': '对该级别启用吗', 'root': '根', 'setLevel': '设级别', 'warn': '警告旧名', 'warning': '警告'})

class 根日志器(日志器):
    """
    A root logger is not that different to any other logger, except that
    it must have a logging level and there is only one instance of it in
    the hierarchy.
    """

    def __init__(self, level):
        """
        Initialize the logger with the name "root".
        """
        日志器.__init__(self, 'root', level)

    def __reduce__(self):
        return (取日志器, ())
_loggerClass = 日志器

class 日志适配器(object):
    """
    An adapter for loggers which makes it easier to specify contextual
    information in logging output.
    """

    def __init__(self, logger, extra=None, merge_extra=False):
        """
        Initialize the adapter with a logger and an optional dict-like object
        which provides contextual information. This constructor signature
        allows easy stacking of LoggerAdapters, if so desired.

        You can effectively pass keyword arguments as shown in the
        following example:

        adapter = LoggerAdapter(someLogger, dict(p1=v1, p2="v2"))

        By default, LoggerAdapter objects will drop the "extra" argument
        passed on the individual log calls to use its own instead.

        Initializing it with merge_extra=True will instead merge both
        maps when logging, the individual call extra taking precedence
        over the LoggerAdapter instance extra

        .. versionchanged:: 3.13
           The *merge_extra* argument was added.
        """
        self.logger = logger
        self.extra = extra
        self.merge_extra = merge_extra

    def process(self, msg, kwargs):
        """
        Process the logging message and keyword arguments passed in to
        a logging call to insert contextual information. You can either
        manipulate the message itself, the keyword args or both. Return
        the message and kwargs modified (or not) to suit your needs.

        Normally, you'll only need to override this one method in a
        LoggerAdapter subclass for your specific needs.
        """
        if self.merge_extra and kwargs.get('extra') is not None:
            if self.extra is not None:
                kwargs['extra'] = {**self.extra, **kwargs['extra']}
        else:
            kwargs['extra'] = self.extra
        return (msg, kwargs)

    def 调试(self, msg, *args, **kwargs):
        """
        Delegate a debug call to the underlying logger.
        """
        self.log(调试级别, msg, *args, **kwargs)

    def 信息(self, msg, *args, **kwargs):
        """
        Delegate an info call to the underlying logger.
        """
        self.log(信息级别, msg, *args, **kwargs)

    def 警告(self, msg, *args, **kwargs):
        """
        Delegate a warning call to the underlying logger.
        """
        self.log(警告级别, msg, *args, **kwargs)

    def 警告旧名(self, msg, *args, **kwargs):
        warnings.warn("The 'warn' method is deprecated, use 'warning' instead", DeprecationWarning, 2)
        self.警告(msg, *args, **kwargs)

    def 错误(self, msg, *args, **kwargs):
        """
        Delegate an error call to the underlying logger.
        """
        self.log(错误级别, msg, *args, **kwargs)

    def 异常(self, msg, *args, exc_info=True, **kwargs):
        """
        Delegate an exception call to the underlying logger.
        """
        self.log(错误级别, msg, *args, exc_info=exc_info, **kwargs)

    def 严重(self, msg, *args, **kwargs):
        """
        Delegate a critical call to the underlying logger.
        """
        self.log(严重级别, msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        """
        Delegate a log call to the underlying logger, after adding
        contextual information from this adapter instance.
        """
        if self.对该级别启用吗(level):
            msg, kwargs = self.process(msg, kwargs)
            self.logger.log(level, msg, *args, **kwargs)

    def 对该级别启用吗(self, level):
        """
        Is this logger enabled for level 'level'?
        """
        return self.logger.isEnabledFor(level)

    def 设级别(self, level):
        """
        Set the specified level on the underlying logger.
        """
        self.logger.setLevel(level)

    def 取有效级别(self):
        """
        Get the effective level for the underlying logger.
        """
        return self.logger.getEffectiveLevel()

    def hasHandlers(self):
        """
        See if the underlying logger has any handlers.
        """
        return self.logger.hasHandlers()

    def _log(self, level, msg, args, **kwargs):
        """
        Low-level log implementation, proxied to allow nested logger adapters.
        """
        return self.logger._log(level, msg, args, **kwargs)

    @property
    def manager(self):
        return self.logger.manager

    @manager.setter
    def manager(self, value):
        self.logger.manager = value

    @property
    def name(self):
        return self.logger.name

    def __repr__(self):
        logger = self.logger
        level = 取级别名字(logger.getEffectiveLevel())
        return '<%s %s (%s)>' % (self.__class__.__name__, logger.name, level)
    __class_getitem__ = classmethod(GenericAlias)
_装类转发(日志适配器, {'critical': '严重', 'debug': '调试', 'error': '错误', 'exception': '异常', 'getEffectiveLevel': '取有效级别', 'info': '信息', 'isEnabledFor': '对该级别启用吗', 'setLevel': '设级别', 'warn': '警告旧名', 'warning': '警告'}, {'critical': '严重', 'debug': '调试', 'error': '错误', 'exception': '异常', 'getEffectiveLevel': '取有效级别', 'info': '信息', 'isEnabledFor': '对该级别启用吗', 'setLevel': '设级别', 'warn': '警告旧名', 'warning': '警告'})
根 = 根日志器(警告级别)
日志器.root = 根
日志器.manager = 管理器(日志器.root)

def basicConfig(**kwargs):
    """
    Do basic configuration for the logging system.

    This function does nothing if the root logger already has handlers
    configured, unless the keyword argument *force* is set to ``True``.
    It is a convenience method intended for use by simple scripts
    to do one-shot configuration of the logging package.

    The default behaviour is to create a StreamHandler which writes to
    sys.stderr, set a formatter using the BASIC_FORMAT format string, and
    add the handler to the root logger.

    A number of optional keyword arguments may be specified, which can alter
    the default behaviour.

    filename  Specifies that a FileHandler be created, using the specified
              filename, rather than a StreamHandler.
    filemode  Specifies the mode to open the file, if filename is specified
              (if filemode is unspecified, it defaults to 'a').
    format    Use the specified format string for the handler.
    datefmt   Use the specified date/time format.
    style     If a format string is specified, use this to specify the
              type of format string (possible values '%', '{', '$', for
              %-formatting, :meth:`str.format` and :class:`string.Template`
              - defaults to '%').
    level     Set the root logger level to the specified level.
    stream    Use the specified stream to initialize the StreamHandler. Note
              that this argument is incompatible with 'filename' - if both
              are present, 'stream' is ignored.
    handlers  If specified, this should be an iterable of already created
              handlers, which will be added to the root logger. Any handler
              in the list which does not have a formatter assigned will be
              assigned the formatter created in this function.
    force     If this keyword  is specified as true, any existing handlers
              attached to the root logger are removed and closed, before
              carrying out the configuration as specified by the other
              arguments.
    encoding  If specified together with a filename, this encoding is passed to
              the created FileHandler, causing it to be used when the file is
              opened.
    errors    If specified together with a filename, this value is passed to the
              created FileHandler, causing it to be used when the file is
              opened in text mode. If not specified, the default value is
              `backslashreplace`.

    Note that you could specify a stream created using open(filename, mode)
    rather than passing the filename and mode in. However, it should be
    remembered that StreamHandler does not close its stream (since it may be
    using sys.stdout or sys.stderr), whereas FileHandler closes its stream
    when the handler is closed.

    .. versionchanged:: 3.2
       Added the ``style`` parameter.

    .. versionchanged:: 3.3
       Added the ``handlers`` parameter. A ``ValueError`` is now thrown for
       incompatible arguments (e.g. ``handlers`` specified together with
       ``filename``/``filemode``, or ``filename``/``filemode`` specified
       together with ``stream``, or ``handlers`` specified together with
       ``stream``.

    .. versionchanged:: 3.8
       Added the ``force`` parameter.

    .. versionchanged:: 3.9
       Added the ``encoding`` and ``errors`` parameters.
    """
    with _lock:
        force = kwargs.pop('force', False)
        encoding = kwargs.pop('encoding', None)
        errors = kwargs.pop('errors', 'backslashreplace')
        if force:
            for h in 根.handlers[:]:
                根.removeHandler(h)
                h.close()
        if len(根.handlers) == 0:
            handlers = kwargs.pop('handlers', None)
            if handlers is None:
                if 'stream' in kwargs and 'filename' in kwargs:
                    raise ValueError("'stream' and 'filename' should not be specified together")
            elif 'stream' in kwargs or 'filename' in kwargs:
                raise ValueError("'stream' or 'filename' should not be specified together with 'handlers'")
            if handlers is None:
                filename = kwargs.pop('filename', None)
                mode = kwargs.pop('filemode', 'a')
                if filename:
                    if 'b' in mode:
                        errors = None
                    else:
                        encoding = io.text_encoding(encoding)
                    h = 文件处理器(filename, mode, encoding=encoding, errors=errors)
                else:
                    stream = kwargs.pop('stream', None)
                    h = 流处理器(stream)
                handlers = [h]
            dfs = kwargs.pop('datefmt', None)
            style = kwargs.pop('style', '%')
            if style not in _STYLES:
                raise ValueError('Style must be one of: %s' % ','.join(_STYLES.keys()))
            fs = kwargs.pop('format', _STYLES[style][1])
            fmt = 格式化器(fs, dfs, style)
            for h in handlers:
                if h.formatter is None:
                    h.setFormatter(fmt)
                根.addHandler(h)
            level = kwargs.pop('level', None)
            if level is not None:
                根.setLevel(level)
            if kwargs:
                keys = ', '.join(kwargs.keys())
                raise ValueError('Unrecognised argument(s): %s' % keys)

def 取日志器(name=None):
    """
    Return a logger with the specified name, creating it if necessary.

    If no name is specified, return the root logger.
    """
    if not name or (isinstance(name, str) and name == 根.name):
        return 根
    return 日志器.manager.getLogger(name)

def 严重(msg, *args, **kwargs):
    """
    Log a message with severity 'CRITICAL' on the root logger. If the logger
    has no handlers, call basicConfig() to add a console handler with a
    pre-defined format.
    """
    if len(根.handlers) == 0:
        basicConfig()
    根.critical(msg, *args, **kwargs)

def 致命(msg, *args, **kwargs):
    """
    Don't use this function, use critical() instead.
    """
    严重(msg, *args, **kwargs)

def 错误(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    if len(根.handlers) == 0:
        basicConfig()
    根.error(msg, *args, **kwargs)

def 异常(msg, *args, exc_info=True, **kwargs):
    """
    Log a message with severity 'ERROR' on the root logger, with exception
    information. If the logger has no handlers, basicConfig() is called to add
    a console handler with a pre-defined format.
    """
    错误(msg, *args, exc_info=exc_info, **kwargs)

def 警告(msg, *args, **kwargs):
    """
    Log a message with severity 'WARNING' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    if len(根.handlers) == 0:
        basicConfig()
    根.warning(msg, *args, **kwargs)

def 警告旧名(msg, *args, **kwargs):
    warnings.warn("The 'warn' function is deprecated, use 'warning' instead", DeprecationWarning, 2)
    警告(msg, *args, **kwargs)

def 信息(msg, *args, **kwargs):
    """
    Log a message with severity 'INFO' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    if len(根.handlers) == 0:
        basicConfig()
    根.info(msg, *args, **kwargs)

def 调试(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the root logger. If the logger has
    no handlers, call basicConfig() to add a console handler with a pre-defined
    format.
    """
    if len(根.handlers) == 0:
        basicConfig()
    根.debug(msg, *args, **kwargs)

def log(level, msg, *args, **kwargs):
    """
    Log 'msg % args' with the integer severity 'level' on the root logger. If
    the logger has no handlers, call basicConfig() to add a console handler
    with a pre-defined format.
    """
    if len(根.handlers) == 0:
        basicConfig()
    根.log(level, msg, *args, **kwargs)

def 停用级别(level=严重级别):
    """
    Disable all logging calls of severity 'level' and below.
    """
    根.manager.disable = level
    根.manager._clear_cache()

def 关闭(handlerList=_handlerList):
    """
    Perform any cleanup actions in the logging system (e.g. flushing
    buffers).

    Should be called at application exit.
    """
    for wr in reversed(handlerList[:]):
        try:
            h = wr()
            if h:
                try:
                    h.acquire()
                    if getattr(h, 'flushOnClose', True):
                        h.flush()
                    h.close()
                except (OSError, ValueError):
                    pass
                finally:
                    h.release()
        except:
            if raiseExceptions:
                raise
import atexit
atexit.register(关闭)

class 空处理器(处理器):
    """
    This handler does nothing. It's intended to be used to avoid the
    "No handlers could be found for logger XXX" one-off warning. This is
    important for library code, which may contain code to log events. If a user
    of the library does not configure logging, the one-off warning might be
    produced; to avoid this, the library developer simply needs to instantiate
    a NullHandler and add it to the top-level logger of the library module or
    package.
    """

    def handle(self, record):
        """Stub."""

    def emit(self, record):
        """Stub."""

    def createLock(self):
        self.lock = None

    def _at_fork_reinit(self):
        pass
_warnings_showwarning = None

def _showwarning(message, category, filename, lineno, file=None, line=None):
    """
    Implementation of showwarnings which redirects to logging, which will first
    check to see if the file parameter is None. If a file is specified, it will
    delegate to the original warnings implementation of showwarning. Otherwise,
    it will call warnings.formatwarning and will log the resulting string to a
    warnings logger named "py.warnings" with level logging.WARNING.
    """
    if file is not None:
        if _warnings_showwarning is not None:
            _warnings_showwarning(message, category, filename, lineno, file, line)
    else:
        s = warnings.formatwarning(message, category, filename, lineno, line)
        logger = 取日志器('py.warnings')
        if not logger.handlers:
            logger.addHandler(空处理器())
        logger.warning(str(s))

def 捕获警告(capture):
    """
    If capture is true, redirect all warnings to the logging package.
    If capture is False, ensure that warnings are not redirected to logging
    but to their original destinations.
    """
    global _warnings_showwarning
    if capture:
        if _warnings_showwarning is None:
            _warnings_showwarning = warnings.showwarning
            warnings.showwarning = _showwarning
    elif _warnings_showwarning is not None:
        warnings.showwarning = _warnings_showwarning
        _warnings_showwarning = None


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BASIC_FORMAT': '基本格式',
    'BufferingFormatter': '缓冲格式化器',
    'CRITICAL': '严重级别',
    'DEBUG': '调试级别',
    'ERROR': '错误级别',
    'FATAL': '致命级别',
    'FileHandler': '文件处理器',
    'Filter': '过滤器',
    'Filterer': '可过滤基类',
    'Formatter': '格式化器',
    'Handler': '处理器',
    'INFO': '信息级别',
    'LogRecord': '日志记录',
    'Logger': '日志器',
    'LoggerAdapter': '日志适配器',
    'Manager': '管理器',
    'NOTSET': '未设置',
    'NullHandler': '空处理器',
    'PercentStyle': '百分号风格',
    'PlaceHolder': '占位处理器',
    'RootLogger': '根日志器',
    'StrFormatStyle': '大括号风格',
    'StreamHandler': '流处理器',
    'StringTemplateStyle': '模板风格',
    'WARN': '警告级别旧名',
    'WARNING': '警告级别',
    'addLevelName': '加级别名字',
    'captureWarnings': '捕获警告',
    'critical': '严重',
    'currentframe': '当前帧',
    'debug': '调试',
    'disable': '停用级别',
    'error': '错误',
    'exception': '异常',
    'fatal': '致命',
    'getHandlerByName': '按名字取处理器',
    'getHandlerNames': '取处理器名字表',
    'getLevelName': '取级别名字',
    'getLevelNamesMapping': '取级别名字表',
    'getLogRecordFactory': '取日志记录工厂',
    'getLogger': '取日志器',
    'getLoggerClass': '取日志器类',
    'info': '信息',
    'makeLogRecord': '造日志记录',
    'root': '根',
    'setLogRecordFactory': '设日志记录工厂',
    'setLoggerClass': '设日志器类',
    'shutdown': '关闭',
    'warn': '警告旧名',
    'warning': '警告',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '可过滤基类': {
        'addFilter': '加过滤器',
        'removeFilter': '去过滤器',
    },
    '处理器': {
        'setFormatter': '设格式化器',
        'setLevel': '设级别',
    },
    '日志器': {
        'critical': '严重',
        'debug': '调试',
        'error': '错误',
        'exception': '异常',
        'fatal': '致命',
        'getChild': '取子日志器',
        'getEffectiveLevel': '取有效级别',
        'info': '信息',
        'isEnabledFor': '对该级别启用吗',
        'setLevel': '设级别',
        'warn': '警告旧名',
        'warning': '警告',
    },
    '日志记录': {
        'getMessage': '取消息',
    },
    '日志适配器': {
        'critical': '严重',
        'debug': '调试',
        'error': '错误',
        'exception': '异常',
        'getEffectiveLevel': '取有效级别',
        'info': '信息',
        'isEnabledFor': '对该级别启用吗',
        'setLevel': '设级别',
        'warn': '警告旧名',
        'warning': '警告',
    },
    '管理器': {
        'disable': '停用级别',
        'getLogger': '取日志器',
        'setLogRecordFactory': '设日志记录工厂',
        'setLoggerClass': '设日志器类',
    },
}
_转发跳过 = []
_无 = object()    # 哨兵：类属性**值就是 None** 时 ≠ 「没找到」（D-126 修的真 bug）
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # ★必须从 __dict__ 拿**描述符本体**，不能用 getattr(类, 名)：
        #   getattr 会把 classmethod/staticmethod/property **绑到本类上**，
        #   再挂成别名之后，**子类**调用拿到的还是绑死在本类的那个 ——
        #   DummyFraction.from_number(...) 会返回基类实例
        #   （fractions 的 testFromNumber_subclass 就是这么挂的，见 D-035）。
        _原 = _类.__dict__.get(_中, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _中 in _基.__dict__:
                    _原 = _基.__dict__[_中]
                    break
        if _原 is _无:
            _转发跳过.append((_类名, _英, _中))
            continue
        setattr(_类, _英, _原)

# 中文成员名的兜底（D-125 起，D-126 推广到全部类）：上面主循环只认「中文名在类里」，
#   找不到就跳过 —— 可中文名**本来就不在类里**有两种情况：① 类名走了身份别名
#   （机制 3），指向英文那个对象；② 改名被规则挡下（那个名字是 import 进来的）。
#   实测 `注解库.前向引用('X').求值()`、`选择器.select选择器.选择` 都是 AttributeError。
#   这里反过来挂：从英文名取**描述符本体**，把中文名加上去。只加描述符别名，
#   **不装钩子**（英文类协议不改，照 D-070）；C 类型不可变、setattr 抛 TypeError 就跳过
#   （C 类型的方法名归机制 1 的方法名表管）。
for _类名, _对 in _成员别名.items():
    _类 = globals().get(_类名)
    if _类 is None:
        continue
    for _英, _中 in _对.items():
        # 中文名已经在类里（改名成功）⇒ 没事，主循环已把英文名补回去了。
        if _中 in _类.__dict__ or any(_中 in _基.__dict__ for _基 in _类.__mro__):
            continue
        _原 = _类.__dict__.get(_英, _无)
        if _原 is _无:
            for _基 in _类.__mro__:
                if _英 in _基.__dict__:
                    _原 = _基.__dict__[_英]
                    break
        if _原 is None:
            _转发跳过.append((_类名, _英, _中))
            continue
        try:
            setattr(_类, _中, _原)
        except TypeError:
            continue    # C 类型不可变挂不上；主循环已经记过一笔，不重复记
        if (_类名, _英, _中) in _转发跳过:
            _转发跳过.remove((_类名, _英, _中))

# 实例属性：两个方向都翻（英文名 <-> 中文名）。
# **逻辑只有一份**，在 `_装类转发` 里 —— 每个类定义紧后面已经装过一次
# （照 D-040），这里是文件末尾的兜底，幂等。
_实例属性 = {
    '可过滤基类': {
        'addFilter': '加过滤器',
        'removeFilter': '去过滤器',
    },
    '处理器': {
        'setFormatter': '设格式化器',
        'setLevel': '设级别',
    },
    '日志器': {
        'critical': '严重',
        'debug': '调试',
        'error': '错误',
        'exception': '异常',
        'fatal': '致命',
        'getChild': '取子日志器',
        'getEffectiveLevel': '取有效级别',
        'info': '信息',
        'isEnabledFor': '对该级别启用吗',
        'root': '根',
        'setLevel': '设级别',
        'warn': '警告旧名',
        'warning': '警告',
    },
    '日志记录': {
        'getMessage': '取消息',
    },
    '日志适配器': {
        'critical': '严重',
        'debug': '调试',
        'error': '错误',
        'exception': '异常',
        'getEffectiveLevel': '取有效级别',
        'info': '信息',
        'isEnabledFor': '对该级别启用吗',
        'setLevel': '设级别',
        'warn': '警告旧名',
        'warning': '警告',
    },
    '管理器': {
        'disable': '停用级别',
        'getLogger': '取日志器',
        'root': '根',
        'setLogRecordFactory': '设日志记录工厂',
        'setLoggerClass': '设日志器类',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = list(__all__) + [
    '严重',
    '严重级别',
    '信息',
    '信息级别',
    '停用级别',
    '关闭',
    '加级别名字',
    '取处理器名字表',
    '取日志器',
    '取日志器类',
    '取日志记录工厂',
    '取级别名字',
    '取级别名字表',
    '基本格式',
    '处理器',
    '异常',
    '按名字取处理器',
    '捕获警告',
    '文件处理器',
    '日志器',
    '日志记录',
    '日志适配器',
    '未设置',
    '格式化器',
    '流处理器',
    '空处理器',
    '缓冲格式化器',
    '致命',
    '致命级别',
    '警告',
    '警告旧名',
    '警告级别',
    '警告级别旧名',
    '设日志器类',
    '设日志记录工厂',
    '调试',
    '调试级别',
    '过滤器',
    '造日志记录',
    '错误',
    '错误级别',
]

# ---- 转发层结束 ----
