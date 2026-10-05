# -*- coding: utf-8 -*-
"""日志.handlers —— 汉语库（由 tools/汉化库.py 从 Lib/logging/handlers.py 机械生成，**不要手改**）。

英文库 Lib/logging.handlers.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py logging
"""


"""
Additional handlers for the logging package for Python. The core package is
based on PEP 282 and comments thereto in comp.lang.python.

Copyright (C) 2001-2021 Vinay Sajip. All Rights Reserved.

To use, simply 'import logging.handlers' and log away!
"""
_英文原名表 = {'BaseRotatingHandler': '轮转处理基类', 'BufferingHandler': '缓冲处理器', 'DEFAULT_HTTP_LOGGING_PORT': '默认HTTP日志端口', 'DEFAULT_SOAP_LOGGING_PORT': '默认SOAP日志端口', 'DEFAULT_TCP_LOGGING_PORT': '默认TCP日志端口', 'DEFAULT_UDP_LOGGING_PORT': '默认UDP日志端口', 'DatagramHandler': '数据报处理器', 'HTTPHandler': 'HTTP处理器', 'MemoryHandler': '内存处理器', 'NTEventLogHandler': 'NT事件日志处理器', 'QueueHandler': '队列处理器', 'QueueListener': '队列监听器', 'RotatingFileHandler': '按大小轮转文件处理器', 'SMTPHandler': '邮件处理器', 'SYSLOG_TCP_PORT': '系统日志TCP端口', 'SYSLOG_UDP_PORT': '系统日志UDP端口', 'SocketHandler': '套接字处理器', 'SysLogHandler': '系统日志处理器', 'TimedRotatingFileHandler': '按时间轮转文件处理器', 'WatchedFileHandler': '监视文件处理器'}

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
import copy
import io
import 日志
import os
import pickle
import queue
import re
import socket
import struct
import threading
import time
默认TCP日志端口 = 9020
默认UDP日志端口 = 9021
默认HTTP日志端口 = 9022
默认SOAP日志端口 = 9023
系统日志UDP端口 = 514
系统日志TCP端口 = 514
_MIDNIGHT = 24 * 60 * 60

class 轮转处理基类(日志.FileHandler):
    """
    Base class for handlers that rotate log files at a certain point.
    Not meant to be instantiated directly.  Instead, use RotatingFileHandler
    or TimedRotatingFileHandler.
    """
    namer = None
    rotator = None

    def __init__(self, filename, mode, encoding=None, delay=False, errors=None):
        """
        Use the specified filename for streamed logging
        """
        日志.FileHandler.__init__(self, filename, mode=mode, encoding=encoding, delay=delay, errors=errors)
        self.mode = mode
        self.encoding = encoding
        self.errors = errors

    def emit(self, record):
        """
        Emit a record.

        Output the record to the file, catering for rollover as described
        in doRollover().
        """
        try:
            if self.shouldRollover(record):
                self.doRollover()
            日志.FileHandler.emit(self, record)
        except Exception:
            self.handleError(record)

    def rotation_filename(self, default_name):
        """
        Modify the filename of a log file when rotating.

        This is provided so that a custom filename can be provided.

        The default implementation calls the 'namer' attribute of the
        handler, if it's callable, passing the default name to
        it. If the attribute isn't callable (the default is None), the name
        is returned unchanged.

        :param default_name: The default name for the log file.
        """
        if not callable(self.namer):
            result = default_name
        else:
            result = self.namer(default_name)
        return result

    def rotate(self, source, dest):
        """
        When rotating, rotate the current log.

        The default implementation calls the 'rotator' attribute of the
        handler, if it's callable, passing the source and dest arguments to
        it. If the attribute isn't callable (the default is None), the source
        is simply renamed to the destination.

        :param source: The source filename. This is normally the base
                       filename, e.g. 'test.log'
        :param dest:   The destination filename. This is normally
                       what the source is rotated to, e.g. 'test.log.1'.
        """
        if not callable(self.rotator):
            if os.path.exists(source):
                os.rename(source, dest)
        else:
            self.rotator(source, dest)

class 按大小轮转文件处理器(轮转处理基类):
    """
    Handler for logging to a set of files, which switches from one file
    to the next when the current file reaches a certain size.
    """

    def __init__(self, filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=False, errors=None):
        """
        Open the specified file and use it as the stream for logging.

        By default, the file grows indefinitely. You can specify particular
        values of maxBytes and backupCount to allow the file to rollover at
        a predetermined size.

        Rollover occurs whenever the current log file is nearly maxBytes in
        length. If backupCount is >= 1, the system will successively create
        new files with the same pathname as the base file, but with extensions
        ".1", ".2" etc. appended to it. For example, with a backupCount of 5
        and a base file name of "app.log", you would get "app.log",
        "app.log.1", "app.log.2", ... through to "app.log.5". The file being
        written to is always "app.log" - when it gets filled up, it is closed
        and renamed to "app.log.1", and if files "app.log.1", "app.log.2" etc.
        exist, then they are renamed to "app.log.2", "app.log.3" etc.
        respectively.

        If maxBytes is zero, rollover never occurs.
        """
        if maxBytes > 0:
            mode = 'a'
        if 'b' not in mode:
            encoding = io.text_encoding(encoding)
        轮转处理基类.__init__(self, filename, mode, encoding=encoding, delay=delay, errors=errors)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def doRollover(self):
        """
        Do a rollover, as described in __init__().
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = self.rotation_filename('%s.%d' % (self.baseFilename, i))
                dfn = self.rotation_filename('%s.%d' % (self.baseFilename, i + 1))
                if os.path.exists(sfn):
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)
            dfn = self.rotation_filename(self.baseFilename + '.1')
            if os.path.exists(dfn):
                os.remove(dfn)
            self.rotate(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        Basically, see if the supplied record would cause the file to exceed
        the size limit we have.
        """
        if self.stream is None:
            self.stream = self._open()
        if self.maxBytes > 0:
            try:
                pos = self.stream.tell()
            except io.UnsupportedOperation:
                return False
            if not pos:
                return False
            msg = '%s\n' % self.format(record)
            if pos + len(msg) >= self.maxBytes:
                if os.path.exists(self.baseFilename) and (not os.path.isfile(self.baseFilename)):
                    return False
                return True
        return False

class 按时间轮转文件处理器(轮转处理基类):
    """
    Handler for logging to a file, rotating the log file at certain timed
    intervals.

    If backupCount is > 0, when rollover is done, no more than backupCount
    files are kept - the oldest ones are deleted.
    """

    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None, errors=None):
        encoding = io.text_encoding(encoding)
        轮转处理基类.__init__(self, filename, 'a', encoding=encoding, delay=delay, errors=errors)
        self.when = when.upper()
        self.backupCount = backupCount
        self.utc = utc
        self.atTime = atTime
        if self.when == 'S':
            self.interval = 1
            self.suffix = '%Y-%m-%d_%H-%M-%S'
            extMatch = '(?<!\\d)\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}-\\d{2}(?!\\d)'
        elif self.when == 'M':
            self.interval = 60
            self.suffix = '%Y-%m-%d_%H-%M'
            extMatch = '(?<!\\d)\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}(?!\\d)'
        elif self.when == 'H':
            self.interval = 60 * 60
            self.suffix = '%Y-%m-%d_%H'
            extMatch = '(?<!\\d)\\d{4}-\\d{2}-\\d{2}_\\d{2}(?!\\d)'
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.interval = 60 * 60 * 24
            self.suffix = '%Y-%m-%d'
            extMatch = '(?<!\\d)\\d{4}-\\d{2}-\\d{2}(?!\\d)'
        elif self.when.startswith('W'):
            self.interval = 60 * 60 * 24 * 7
            if len(self.when) != 2:
                raise ValueError('You must specify a day for weekly rollover from 0 to 6 (0 is Monday): %s' % self.when)
            if self.when[1] < '0' or self.when[1] > '6':
                raise ValueError('Invalid day specified for weekly rollover: %s' % self.when)
            self.dayOfWeek = int(self.when[1])
            self.suffix = '%Y-%m-%d'
            extMatch = '(?<!\\d)\\d{4}-\\d{2}-\\d{2}(?!\\d)'
        else:
            raise ValueError('Invalid rollover interval specified: %s' % self.when)
        self.extMatch = re.compile(extMatch, re.ASCII)
        self.interval = self.interval * interval
        filename = self.baseFilename
        if os.path.exists(filename):
            t = int(os.stat(filename).st_mtime)
        else:
            t = int(time.time())
        self.rolloverAt = self.computeRollover(t)

    def computeRollover(self, currentTime):
        """
        Work out the rollover time based on the specified time.
        """
        result = currentTime + self.interval
        if self.when == 'MIDNIGHT' or self.when.startswith('W'):
            if self.utc:
                t = time.gmtime(currentTime)
            else:
                t = time.localtime(currentTime)
            currentHour = t[3]
            currentMinute = t[4]
            currentSecond = t[5]
            currentDay = t[6]
            if self.atTime is None:
                rotate_ts = _MIDNIGHT
            else:
                rotate_ts = (self.atTime.hour * 60 + self.atTime.minute) * 60 + self.atTime.second
            r = rotate_ts - ((currentHour * 60 + currentMinute) * 60 + currentSecond)
            if r <= 0:
                r += _MIDNIGHT
                currentDay = (currentDay + 1) % 7
            result = currentTime + r
            if self.when.startswith('W'):
                day = currentDay
                if day != self.dayOfWeek:
                    if day < self.dayOfWeek:
                        daysToWait = self.dayOfWeek - day
                    else:
                        daysToWait = 6 - day + self.dayOfWeek + 1
                    result += daysToWait * _MIDNIGHT
                result += self.interval - _MIDNIGHT * 7
            else:
                result += self.interval - _MIDNIGHT
            if not self.utc:
                dstNow = t[-1]
                dstAtRollover = time.localtime(result)[-1]
                if dstNow != dstAtRollover:
                    if not dstNow:
                        addend = -3600
                        if not time.localtime(result - 3600)[-1]:
                            addend = 0
                    else:
                        addend = 3600
                    result += addend
        return result

    def shouldRollover(self, record):
        """
        Determine if rollover should occur.

        record is not used, as we are just comparing times, but it is needed so
        the method signatures are the same
        """
        t = int(time.time())
        if t >= self.rolloverAt:
            if os.path.exists(self.baseFilename) and (not os.path.isfile(self.baseFilename)):
                self.rolloverAt = self.computeRollover(t)
                return False
            return True
        return False

    def getFilesToDelete(self):
        """
        Determine the files to delete when rolling over.

        More specific than the earlier method, which just used glob.glob().
        """
        dirName, baseName = os.path.split(self.baseFilename)
        fileNames = os.listdir(dirName)
        result = []
        if self.namer is None:
            prefix = baseName + '.'
            plen = len(prefix)
            for fileName in fileNames:
                if fileName[:plen] == prefix:
                    suffix = fileName[plen:]
                    if self.extMatch.fullmatch(suffix):
                        result.append(os.path.join(dirName, fileName))
        else:
            for fileName in fileNames:
                m = self.extMatch.search(fileName)
                while m:
                    dfn = self.namer(self.baseFilename + '.' + m[0])
                    if os.path.basename(dfn) == fileName:
                        result.append(os.path.join(dirName, fileName))
                        break
                    m = self.extMatch.search(fileName, m.start() + 1)
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """
        currentTime = int(time.time())
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstNow = time.localtime(currentTime)[-1]
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t + addend)
        dfn = self.rotation_filename(self.baseFilename + '.' + time.strftime(self.suffix, timeTuple))
        if os.path.exists(dfn):
            return
        if self.stream:
            self.stream.close()
            self.stream = None
        self.rotate(self.baseFilename, dfn)
        if self.backupCount > 0:
            for s in self.getFilesToDelete():
                os.remove(s)
        if not self.delay:
            self.stream = self._open()
        self.rolloverAt = self.computeRollover(currentTime)

class 监视文件处理器(日志.FileHandler):
    """
    A handler for logging to a file, which watches the file
    to see if it has changed while in use. This can happen because of
    usage of programs such as newsyslog and logrotate which perform
    log file rotation. This handler, intended for use under Unix,
    watches the file to see if it has changed since the last emit.
    (A file has changed if its device or inode have changed.)
    If it has changed, the old file stream is closed, and the file
    opened to get a new stream.

    This handler is not appropriate for use under Windows, because
    under Windows open files cannot be moved or renamed - logging
    opens the files with exclusive locks - and so there is no need
    for such a handler.

    This handler is based on a suggestion and patch by Chad J.
    Schroeder.
    """

    def __init__(self, filename, mode='a', encoding=None, delay=False, errors=None):
        if 'b' not in mode:
            encoding = io.text_encoding(encoding)
        日志.FileHandler.__init__(self, filename, mode=mode, encoding=encoding, delay=delay, errors=errors)
        self.dev, self.ino = (-1, -1)
        self._statstream()

    def _statstream(self):
        if self.stream is None:
            return
        sres = os.fstat(self.stream.fileno())
        self.dev = sres.st_dev
        self.ino = sres.st_ino

    def reopenIfNeeded(self):
        """
        Reopen log file if needed.

        Checks if the underlying file has changed, and if it
        has, close the old stream and reopen the file to get the
        current stream.
        """
        if self.stream is None:
            return
        try:
            sres = os.stat(self.baseFilename)
            reopen = sres.st_dev != self.dev or sres.st_ino != self.ino
        except FileNotFoundError:
            reopen = True
        if not reopen:
            return
        self.stream.flush()
        self.stream.close()
        self.stream = None
        self.stream = self._open()
        self._statstream()

    def emit(self, record):
        """
        Emit a record.

        If underlying file has changed, reopen the file before emitting the
        record to it.
        """
        self.reopenIfNeeded()
        日志.FileHandler.emit(self, record)

class 套接字处理器(日志.Handler):
    """
    A handler class which writes logging records, in pickle format, to
    a streaming socket. The socket is kept open across logging calls.
    If the peer resets it, an attempt is made to reconnect on the next call.
    The pickle which is sent is that of the LogRecord's attribute dictionary
    (__dict__), so that the receiver does not need to have the logging module
    installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.
    """

    def __init__(self, host, port):
        """
        Initializes the handler with a specific host address and port.

        When the attribute *closeOnError* is set to True - if a socket error
        occurs, the socket is silently closed and then reopened on the next
        logging call.
        """
        日志.Handler.__init__(self)
        self.host = host
        self.port = port
        if port is None:
            self.address = host
        else:
            self.address = (host, port)
        self.sock = None
        self.closeOnError = False
        self.retryTime = None
        self.retryStart = 1.0
        self.retryMax = 30.0
        self.retryFactor = 2.0

    def makeSocket(self, timeout=1):
        """
        A factory method which allows subclasses to define the precise
        type of socket they want.
        """
        if self.port is not None:
            result = socket.create_connection(self.address, timeout=timeout)
        else:
            result = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            result.settimeout(timeout)
            try:
                result.connect(self.address)
            except OSError:
                result.close()
                raise
        return result

    def createSocket(self):
        """
        Try to create a socket, using an exponential backoff with
        a max retry time. Thanks to Robert Olson for the original patch
        (SF #815911) which has been slightly refactored.
        """
        now = time.time()
        if self.retryTime is None:
            attempt = True
        else:
            attempt = now >= self.retryTime
        if attempt:
            try:
                self.sock = self.makeSocket()
                self.retryTime = None
            except OSError:
                if self.retryTime is None:
                    self.retryPeriod = self.retryStart
                else:
                    self.retryPeriod = self.retryPeriod * self.retryFactor
                    if self.retryPeriod > self.retryMax:
                        self.retryPeriod = self.retryMax
                self.retryTime = now + self.retryPeriod

    def send(self, s):
        """
        Send a pickled string to the socket.

        This function allows for partial sends which can happen when the
        network is busy.
        """
        if self.sock is None:
            self.createSocket()
        if self.sock:
            try:
                self.sock.sendall(s)
            except OSError:
                self.sock.close()
                self.sock = None

    def makePickle(self, record):
        """
        Pickles the record in binary format with a length prefix, and
        returns it ready for transmission across the socket.
        """
        ei = record.exc_info
        if ei:
            dummy = self.format(record)
        d = dict(record.__dict__)
        d['msg'] = record.getMessage()
        d['args'] = None
        d['exc_info'] = None
        d.pop('message', None)
        s = pickle.dumps(d, 1)
        slen = struct.pack('>L', len(s))
        return slen + s

    def handleError(self, record):
        """
        Handle an error during logging.

        An error has occurred during logging. Most likely cause -
        connection lost. Close the socket so that we can retry on the
        next event.
        """
        if self.closeOnError and self.sock:
            self.sock.close()
            self.sock = None
        else:
            日志.Handler.handleError(self, record)

    def emit(self, record):
        """
        Emit a record.

        Pickles the record and writes it to the socket in binary format.
        If there is an error with the socket, silently drop the packet.
        If there was a problem with the socket, re-establishes the
        socket.
        """
        try:
            s = self.makePickle(record)
            self.send(s)
        except Exception:
            self.handleError(record)

    def close(self):
        """
        Closes the socket.
        """
        with self.lock:
            sock = self.sock
            if sock:
                self.sock = None
                sock.close()
            日志.Handler.close(self)

class 数据报处理器(套接字处理器):
    """
    A handler class which writes logging records, in pickle format, to
    a datagram socket.  The pickle which is sent is that of the LogRecord's
    attribute dictionary (__dict__), so that the receiver does not need to
    have the logging module installed in order to process the logging event.

    To unpickle the record at the receiving end into a LogRecord, use the
    makeLogRecord function.

    """

    def __init__(self, host, port):
        """
        Initializes the handler with a specific host address and port.
        """
        套接字处理器.__init__(self, host, port)
        self.closeOnError = False

    def makeSocket(self):
        """
        The factory method of SocketHandler is here overridden to create
        a UDP socket (SOCK_DGRAM).
        """
        if self.port is None:
            family = socket.AF_UNIX
        else:
            family = socket.AF_INET
        s = socket.socket(family, socket.SOCK_DGRAM)
        return s

    def send(self, s):
        """
        Send a pickled string to a socket.

        This function no longer allows for partial sends which can happen
        when the network is busy - UDP does not guarantee delivery and
        can deliver packets out of sequence.
        """
        if self.sock is None:
            self.createSocket()
        self.sock.sendto(s, self.address)

class 系统日志处理器(日志.Handler):
    """
    A handler class which sends formatted logging records to a syslog
    server. Based on Sam Rushing's syslog module:
    http://www.nightmare.com/squirl/python-ext/misc/syslog.py
    Contributed by Nicolas Untz (after which minor refactoring changes
    have been made).
    """
    LOG_EMERG = 0
    LOG_ALERT = 1
    LOG_CRIT = 2
    LOG_ERR = 3
    LOG_WARNING = 4
    LOG_NOTICE = 5
    LOG_INFO = 6
    LOG_DEBUG = 7
    LOG_KERN = 0
    LOG_USER = 1
    LOG_MAIL = 2
    LOG_DAEMON = 3
    LOG_AUTH = 4
    LOG_SYSLOG = 5
    LOG_LPR = 6
    LOG_NEWS = 7
    LOG_UUCP = 8
    LOG_CRON = 9
    LOG_AUTHPRIV = 10
    LOG_FTP = 11
    LOG_NTP = 12
    LOG_SECURITY = 13
    LOG_CONSOLE = 14
    LOG_SOLCRON = 15
    LOG_LOCAL0 = 16
    LOG_LOCAL1 = 17
    LOG_LOCAL2 = 18
    LOG_LOCAL3 = 19
    LOG_LOCAL4 = 20
    LOG_LOCAL5 = 21
    LOG_LOCAL6 = 22
    LOG_LOCAL7 = 23
    priority_names = {'alert': LOG_ALERT, 'crit': LOG_CRIT, 'critical': LOG_CRIT, 'debug': LOG_DEBUG, 'emerg': LOG_EMERG, 'err': LOG_ERR, 'error': LOG_ERR, 'info': LOG_INFO, 'notice': LOG_NOTICE, 'panic': LOG_EMERG, 'warn': LOG_WARNING, 'warning': LOG_WARNING}
    facility_names = {'auth': LOG_AUTH, 'authpriv': LOG_AUTHPRIV, 'console': LOG_CONSOLE, 'cron': LOG_CRON, 'daemon': LOG_DAEMON, 'ftp': LOG_FTP, 'kern': LOG_KERN, 'lpr': LOG_LPR, 'mail': LOG_MAIL, 'news': LOG_NEWS, 'ntp': LOG_NTP, 'security': LOG_SECURITY, 'solaris-cron': LOG_SOLCRON, 'syslog': LOG_SYSLOG, 'user': LOG_USER, 'uucp': LOG_UUCP, 'local0': LOG_LOCAL0, 'local1': LOG_LOCAL1, 'local2': LOG_LOCAL2, 'local3': LOG_LOCAL3, 'local4': LOG_LOCAL4, 'local5': LOG_LOCAL5, 'local6': LOG_LOCAL6, 'local7': LOG_LOCAL7}
    priority_map = {'DEBUG': 'debug', 'INFO': 'info', 'WARNING': 'warning', 'ERROR': 'error', 'CRITICAL': 'critical'}

    def __init__(self, address=('localhost', 系统日志UDP端口), facility=LOG_USER, socktype=None, timeout=None):
        """
        Initialize a handler.

        If address is specified as a string, a UNIX socket is used. To log to a
        local syslogd, "SysLogHandler(address="/dev/log")" can be used.
        If facility is not specified, LOG_USER is used. If socktype is
        specified as socket.SOCK_DGRAM or socket.SOCK_STREAM, that specific
        socket type will be used. For Unix sockets, you can also specify a
        socktype of None, in which case socket.SOCK_DGRAM will be used, falling
        back to socket.SOCK_STREAM.
        """
        日志.Handler.__init__(self)
        self.address = address
        self.facility = facility
        self.socktype = socktype
        self.timeout = timeout
        self.socket = None
        self.createSocket()

    def _connect_unixsocket(self, address):
        use_socktype = self.socktype
        if use_socktype is None:
            use_socktype = socket.SOCK_DGRAM
        self.socket = socket.socket(socket.AF_UNIX, use_socktype)
        try:
            self.socket.connect(address)
            self.socktype = use_socktype
        except OSError:
            self.socket.close()
            if self.socktype is not None:
                raise
            use_socktype = socket.SOCK_STREAM
            self.socket = socket.socket(socket.AF_UNIX, use_socktype)
            try:
                self.socket.connect(address)
                self.socktype = use_socktype
            except OSError:
                self.socket.close()
                raise

    def createSocket(self):
        """
        Try to create a socket and, if it's not a datagram socket, connect it
        to the other end. This method is called during handler initialization,
        but it's not regarded as an error if the other end isn't listening yet
        --- the method will be called again when emitting an event,
        if there is no socket at that point.
        """
        address = self.address
        socktype = self.socktype
        if isinstance(address, str):
            self.unixsocket = True
            try:
                self._connect_unixsocket(address)
            except OSError:
                pass
        else:
            self.unixsocket = False
            if socktype is None:
                socktype = socket.SOCK_DGRAM
            host, port = address
            ress = socket.getaddrinfo(host, port, 0, socktype)
            if not ress:
                raise OSError('getaddrinfo returns an empty list')
            for res in ress:
                af, socktype, proto, _, sa = res
                err = sock = None
                try:
                    sock = socket.socket(af, socktype, proto)
                    if self.timeout:
                        sock.settimeout(self.timeout)
                    if socktype == socket.SOCK_STREAM:
                        sock.connect(sa)
                    break
                except OSError as exc:
                    err = exc
                    if sock is not None:
                        sock.close()
            if err is not None:
                raise err
            self.socket = sock
            self.socktype = socktype

    def encodePriority(self, facility, priority):
        """
        Encode the facility and priority. You can pass in strings or
        integers - if strings are passed, the facility_names and
        priority_names mapping dictionaries are used to convert them to
        integers.
        """
        if isinstance(facility, str):
            facility = self.facility_names[facility]
        if isinstance(priority, str):
            priority = self.priority_names[priority]
        return facility << 3 | priority

    def close(self):
        """
        Closes the socket.
        """
        with self.lock:
            sock = self.socket
            if sock:
                self.socket = None
                sock.close()
            日志.Handler.close(self)

    def mapPriority(self, levelName):
        """
        Map a logging level name to a key in the priority_names map.
        This is useful in two scenarios: when custom levels are being
        used, and in the case where you can't do a straightforward
        mapping by lowercasing the logging level name because of locale-
        specific issues (see SF #1524081).
        """
        return self.priority_map.get(levelName, 'warning')
    ident = ''
    append_nul = True

    def emit(self, record):
        """
        Emit a record.

        The record is formatted, and then sent to the syslog server. If
        exception information is present, it is NOT sent to the server.
        """
        try:
            msg = self.format(record)
            if self.ident:
                msg = self.ident + msg
            if self.append_nul:
                msg += '\x00'
            prio = '<%d>' % self.encodePriority(self.facility, self.mapPriority(record.levelname))
            prio = prio.encode('utf-8')
            msg = msg.encode('utf-8')
            msg = prio + msg
            if not self.socket:
                self.createSocket()
            if self.unixsocket:
                try:
                    self.socket.send(msg)
                except OSError:
                    self.socket.close()
                    self._connect_unixsocket(self.address)
                    self.socket.send(msg)
            elif self.socktype == socket.SOCK_DGRAM:
                self.socket.sendto(msg, self.address)
            else:
                self.socket.sendall(msg)
        except Exception:
            self.handleError(record)

class 邮件处理器(日志.Handler):
    """
    A handler class which sends an SMTP email for each logging event.
    """

    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None, timeout=5.0):
        """
        Initialize the handler.

        Initialize the instance with the from and to addresses and subject
        line of the email. To specify a non-standard SMTP port, use the
        (host, port) tuple format for the mailhost argument. To specify
        authentication credentials, supply a (username, password) tuple
        for the credentials argument. To specify the use of a secure
        protocol (TLS), pass in a tuple for the secure argument. This will
        only be used when authentication credentials are supplied. The tuple
        will be either an empty tuple, or a single-value tuple with the name
        of a keyfile, or a 2-value tuple with the names of the keyfile and
        certificate file. (This tuple is passed to the
        `ssl.SSLContext.load_cert_chain` method).
        A timeout in seconds can be specified for the SMTP connection (the
        default is one second).
        """
        日志.Handler.__init__(self)
        if isinstance(mailhost, (list, tuple)):
            self.mailhost, self.mailport = mailhost
        else:
            self.mailhost, self.mailport = (mailhost, None)
        if isinstance(credentials, (list, tuple)):
            self.username, self.password = credentials
        else:
            self.username = None
        self.fromaddr = fromaddr
        if isinstance(toaddrs, str):
            toaddrs = [toaddrs]
        self.toaddrs = toaddrs
        self.subject = subject
        self.secure = secure
        self.timeout = timeout

    def getSubject(self, record):
        """
        Determine the subject for the email.

        If you want to specify a subject line which is record-dependent,
        override this method.
        """
        return self.subject

    def emit(self, record):
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            import smtplib
            from email.message import EmailMessage
            import email.utils
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port, timeout=self.timeout)
            msg = EmailMessage()
            msg['From'] = self.fromaddr
            msg['To'] = ','.join(self.toaddrs)
            msg['Subject'] = self.getSubject(record)
            msg['Date'] = email.utils.localtime()
            msg.set_content(self.format(record))
            if self.username:
                if self.secure is not None:
                    import ssl
                    try:
                        keyfile = self.secure[0]
                    except IndexError:
                        keyfile = None
                    try:
                        certfile = self.secure[1]
                    except IndexError:
                        certfile = None
                    context = ssl._create_stdlib_context(certfile=certfile, keyfile=keyfile)
                    smtp.ehlo()
                    smtp.starttls(context=context)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.send_message(msg)
            smtp.quit()
        except Exception:
            self.handleError(record)

class NT事件日志处理器(日志.Handler):
    """
    A handler class which sends events to the NT Event Log. Adds a
    registry entry for the specified application name. If no dllname is
    provided, win32service.pyd (which contains some basic message
    placeholders) is used. Note that use of these placeholders will make
    your event logs big, as the entire message source is held in the log.
    If you want slimmer logs, you have to pass in the name of your own DLL
    which contains the message definitions you want to use in the event log.
    """

    def __init__(self, appname, dllname=None, logtype='Application'):
        日志.Handler.__init__(self)
        try:
            import win32evtlogutil, win32evtlog
            self.appname = appname
            self._welu = win32evtlogutil
            if not dllname:
                dllname = os.path.split(self._welu.__file__)
                dllname = os.path.split(dllname[0])
                dllname = os.path.join(dllname[0], 'win32service.pyd')
            self.dllname = dllname
            self.logtype = logtype
            try:
                self._welu.AddSourceToRegistry(appname, dllname, logtype)
            except Exception as e:
                if getattr(e, 'winerror', None) != 5:
                    raise
            self.deftype = win32evtlog.EVENTLOG_ERROR_TYPE
            self.typemap = {日志.DEBUG: win32evtlog.EVENTLOG_INFORMATION_TYPE, 日志.INFO: win32evtlog.EVENTLOG_INFORMATION_TYPE, 日志.WARNING: win32evtlog.EVENTLOG_WARNING_TYPE, 日志.ERROR: win32evtlog.EVENTLOG_ERROR_TYPE, 日志.CRITICAL: win32evtlog.EVENTLOG_ERROR_TYPE}
        except ImportError:
            print('The Python Win32 extensions for NT (service, event logging) appear not to be available.')
            self._welu = None

    def getMessageID(self, record):
        """
        Return the message ID for the event record. If you are using your
        own messages, you could do this by having the msg passed to the
        logger being an ID rather than a formatting string. Then, in here,
        you could use a dictionary lookup to get the message ID. This
        version returns 1, which is the base message ID in win32service.pyd.
        """
        return 1

    def getEventCategory(self, record):
        """
        Return the event category for the record.

        Override this if you want to specify your own categories. This version
        returns 0.
        """
        return 0

    def getEventType(self, record):
        """
        Return the event type for the record.

        Override this if you want to specify your own types. This version does
        a mapping using the handler's typemap attribute, which is set up in
        __init__() to a dictionary which contains mappings for DEBUG, INFO,
        WARNING, ERROR and CRITICAL. If you are using your own levels you will
        either need to override this method or place a suitable dictionary in
        the handler's typemap attribute.
        """
        return self.typemap.get(record.levelno, self.deftype)

    def emit(self, record):
        """
        Emit a record.

        Determine the message ID, event category and event type. Then
        log the message in the NT event log.
        """
        if self._welu:
            try:
                id = self.getMessageID(record)
                cat = self.getEventCategory(record)
                type = self.getEventType(record)
                msg = self.format(record)
                self._welu.ReportEvent(self.appname, id, cat, type, [msg])
            except Exception:
                self.handleError(record)

    def close(self):
        """
        Clean up this handler.

        You can remove the application name from the registry as a
        source of event log entries. However, if you do this, you will
        not be able to see the events as you intended in the Event Log
        Viewer - it needs to be able to access the registry to get the
        DLL name.
        """
        日志.Handler.close(self)

class HTTP处理器(日志.Handler):
    """
    A class which sends records to a web server, using either GET or
    POST semantics.
    """

    def __init__(self, host, url, method='GET', secure=False, credentials=None, context=None):
        """
        Initialize the instance with the host, the request URL, and the method
        ("GET" or "POST")
        """
        日志.Handler.__init__(self)
        method = method.upper()
        if method not in ['GET', 'POST']:
            raise ValueError('method must be GET or POST')
        if not secure and context is not None:
            raise ValueError('context parameter only makes sense with secure=True')
        self.host = host
        self.url = url
        self.method = method
        self.secure = secure
        self.credentials = credentials
        self.context = context

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz Glasner.
        """
        return record.__dict__

    def getConnection(self, host, secure):
        """
        get a HTTP[S]Connection.

        Override when a custom connection is required, for example if
        there is a proxy.
        """
        import http.client
        if secure:
            connection = http.client.HTTPSConnection(host, context=self.context)
        else:
            connection = http.client.HTTPConnection(host)
        return connection

    def emit(self, record):
        """
        Emit a record.

        Send the record to the web server as a percent-encoded dictionary
        """
        try:
            import urllib.parse
            host = self.host
            h = self.getConnection(host, self.secure)
            url = self.url
            data = urllib.parse.urlencode(self.mapLogRecord(record))
            if self.method == 'GET':
                if url.find('?') >= 0:
                    sep = '&'
                else:
                    sep = '?'
                url = url + '%c%s' % (sep, data)
            h.putrequest(self.method, url)
            i = host.find(':')
            if i >= 0:
                host = host[:i]
            if self.method == 'POST':
                h.putheader('Content-type', 'application/x-www-form-urlencoded')
                h.putheader('Content-length', str(len(data)))
            if self.credentials:
                import base64
                s = ('%s:%s' % self.credentials).encode('utf-8')
                s = 'Basic ' + base64.b64encode(s).strip().decode('ascii')
                h.putheader('Authorization', s)
            h.endheaders()
            if self.method == 'POST':
                h.send(data.encode('utf-8'))
            h.getresponse()
        except Exception:
            self.handleError(record)

class 缓冲处理器(日志.Handler):
    """
  A handler class which buffers logging records in memory. Whenever each
  record is added to the buffer, a check is made to see if the buffer should
  be flushed. If it should, then flush() is expected to do what's needed.
    """

    def __init__(self, capacity):
        """
        Initialize the handler with the buffer size.
        """
        日志.Handler.__init__(self)
        self.capacity = capacity
        self.buffer = []

    def shouldFlush(self, record):
        """
        Should the handler flush its buffer?

        Returns true if the buffer is up to capacity. This method can be
        overridden to implement custom flushing strategies.
        """
        return len(self.buffer) >= self.capacity

    def emit(self, record):
        """
        Emit a record.

        Append the record. If shouldFlush() tells us to, call flush() to process
        the buffer.
        """
        self.buffer.append(record)
        if self.shouldFlush(record):
            self.flush()

    def flush(self):
        """
        Override to implement custom flushing behaviour.

        This version just zaps the buffer to empty.
        """
        with self.lock:
            self.buffer.clear()

    def close(self):
        """
        Close the handler.

        This version just flushes and chains to the parent class' close().
        """
        try:
            self.flush()
        finally:
            日志.Handler.close(self)

class 内存处理器(缓冲处理器):
    """
    A handler class which buffers logging records in memory, periodically
    flushing them to a target handler. Flushing occurs whenever the buffer
    is full, or when an event of a certain severity or greater is seen.
    """

    def __init__(self, capacity, flushLevel=日志.ERROR, target=None, flushOnClose=True):
        """
        Initialize the handler with the buffer size, the level at which
        flushing should occur and an optional target.

        Note that without a target being set either here or via setTarget(),
        a MemoryHandler is no use to anyone!

        The ``flushOnClose`` argument is ``True`` for backward compatibility
        reasons - the old behaviour is that when the handler is closed, the
        buffer is flushed, even if the flush level hasn't been exceeded nor the
        capacity exceeded. To prevent this, set ``flushOnClose`` to ``False``.
        """
        缓冲处理器.__init__(self, capacity)
        self.flushLevel = flushLevel
        self.target = target
        self.flushOnClose = flushOnClose

    def shouldFlush(self, record):
        """
        Check for buffer full or a record at the flushLevel or higher.
        """
        return len(self.buffer) >= self.capacity or record.levelno >= self.flushLevel

    def setTarget(self, target):
        """
        Set the target handler for this handler.
        """
        with self.lock:
            self.target = target

    def flush(self):
        """
        For a MemoryHandler, flushing means just sending the buffered
        records to the target, if there is one. Override if you want
        different behaviour.

        The record buffer is only cleared if a target has been set.
        """
        with self.lock:
            if self.target:
                for record in self.buffer:
                    self.target.handle(record)
                self.buffer.clear()

    def close(self):
        """
        Flush, if appropriately configured, set the target to None and lose the
        buffer.
        """
        try:
            if self.flushOnClose:
                self.flush()
        finally:
            with self.lock:
                self.target = None
                缓冲处理器.close(self)

class 队列处理器(日志.Handler):
    """
    This handler sends events to a queue. Typically, it would be used together
    with a multiprocessing Queue to centralise logging to file in one process
    (in a multi-process application), so as to avoid file write contention
    between processes.

    This code is new in Python 3.2, but this class can be copy pasted into
    user code for use with earlier Python versions.
    """

    def __init__(self, queue):
        """
        Initialise an instance, using the passed queue.
        """
        日志.Handler.__init__(self)
        self.queue = queue
        self.listener = None

    def 入队(self, record):
        """
        Enqueue a record.

        The base implementation uses put_nowait. You may want to override
        this method if you want to use blocking, timeouts or custom queue
        implementations.
        """
        self.queue.put_nowait(record)

    def prepare(self, record):
        """
        Prepare a record for queuing. The object returned by this method is
        enqueued.

        The base implementation formats the record to merge the message and
        arguments, and removes unpickleable items from the record in-place.
        Specifically, it overwrites the record's `msg` and
        `message` attributes with the merged message (obtained by
        calling the handler's `format` method), and sets the `args`,
        `exc_info` and `exc_text` attributes to None.

        You might want to override this method if you want to convert
        the record to a dict or JSON string, or send a modified copy
        of the record while leaving the original intact.
        """
        msg = self.format(record)
        record = copy.copy(record)
        record.message = msg
        record.msg = msg
        record.args = None
        record.exc_info = None
        record.exc_text = None
        record.stack_info = None
        return record

    def emit(self, record):
        """
        Emit a record.

        Writes the LogRecord to the queue, preparing it for pickling first.
        """
        try:
            self.入队(self.prepare(record))
        except Exception:
            self.handleError(record)
_装类转发(队列处理器, {'enqueue': '入队'}, {'enqueue': '入队'})

class 队列监听器(object):
    """
    This class implements an internal threaded listener which watches for
    LogRecords being added to a queue, removes them and passes them to a
    list of handlers for processing.
    """
    _sentinel = None

    def __init__(self, queue, *handlers, respect_handler_level=False):
        """
        Initialise an instance with the specified queue and
        handlers.
        """
        self.queue = queue
        self.handlers = handlers
        self._thread = None
        self.respect_handler_level = respect_handler_level

    def __enter__(self):
        """
        For use as a context manager. Starts the listener.
        """
        self.启动()
        return self

    def __exit__(self, *args):
        """
        For use as a context manager. Stops the listener.
        """
        self.停止()

    def 出队(self, block):
        """
        Dequeue a record and return it, optionally blocking.

        The base implementation uses get. You may want to override this method
        if you want to use timeouts or work with custom queue implementations.
        """
        return self.queue.get(block)

    def 启动(self):
        """
        Start the listener.

        This starts up a background thread to monitor the queue for
        LogRecords to process.
        """
        if self._thread is not None:
            raise RuntimeError('Listener already started')
        self._thread = t = threading.Thread(target=self._monitor)
        t.daemon = True
        t.start()

    def prepare(self, record):
        """
        Prepare a record for handling.

        This method just returns the passed-in record. You may want to
        override this method if you need to do any custom marshalling or
        manipulation of the record before passing it to the handlers.
        """
        return record

    def handle(self, record):
        """
        Handle a record.

        This just loops through the handlers offering them the record
        to handle.
        """
        record = self.prepare(record)
        for handler in self.handlers:
            if not self.respect_handler_level:
                process = True
            else:
                process = record.levelno >= handler.level
            if process:
                handler.handle(record)

    def _monitor(self):
        """
        Monitor the queue for records, and ask the handler
        to deal with them.

        This method runs on a separate, internal thread.
        The thread will terminate if it sees a sentinel object in the queue.
        """
        q = self.queue
        has_task_done = hasattr(q, 'task_done')
        while True:
            try:
                record = self.出队(True)
                if record is self._sentinel:
                    if has_task_done:
                        q.task_done()
                    break
                self.handle(record)
                if has_task_done:
                    q.task_done()
            except queue.Empty:
                break

    def enqueue_sentinel(self):
        """
        This is used to enqueue the sentinel record.

        The base implementation uses put_nowait. You may want to override this
        method if you want to use timeouts or work with custom queue
        implementations.
        """
        self.queue.put_nowait(self._sentinel)

    def 停止(self):
        """
        Stop the listener.

        This asks the thread to terminate, and then waits for it to do so.
        Note that if you don't call this before your application exits, there
        may be some records still left on the queue, which won't be processed.
        """
        if self._thread:
            self.enqueue_sentinel()
            self._thread.join()
            self._thread = None
_装类转发(队列监听器, {'dequeue': '出队', 'start': '启动', 'stop': '停止'}, {'dequeue': '出队', 'start': '启动', 'stop': '停止'})


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseRotatingHandler': '轮转处理基类',
    'BufferingHandler': '缓冲处理器',
    'DEFAULT_HTTP_LOGGING_PORT': '默认HTTP日志端口',
    'DEFAULT_SOAP_LOGGING_PORT': '默认SOAP日志端口',
    'DEFAULT_TCP_LOGGING_PORT': '默认TCP日志端口',
    'DEFAULT_UDP_LOGGING_PORT': '默认UDP日志端口',
    'DatagramHandler': '数据报处理器',
    'HTTPHandler': 'HTTP处理器',
    'MemoryHandler': '内存处理器',
    'NTEventLogHandler': 'NT事件日志处理器',
    'QueueHandler': '队列处理器',
    'QueueListener': '队列监听器',
    'RotatingFileHandler': '按大小轮转文件处理器',
    'SMTPHandler': '邮件处理器',
    'SYSLOG_TCP_PORT': '系统日志TCP端口',
    'SYSLOG_UDP_PORT': '系统日志UDP端口',
    'SocketHandler': '套接字处理器',
    'SysLogHandler': '系统日志处理器',
    'TimedRotatingFileHandler': '按时间轮转文件处理器',
    'WatchedFileHandler': '监视文件处理器',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    '队列处理器': {
        'enqueue': '入队',
    },
    '队列监听器': {
        'dequeue': '出队',
        'start': '启动',
        'stop': '停止',
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
    '队列处理器': {
        'enqueue': '入队',
    },
    '队列监听器': {
        'dequeue': '出队',
        'start': '启动',
        'stop': '停止',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# ---- 转发层结束 ----
