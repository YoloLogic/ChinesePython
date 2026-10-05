# -*- coding: utf-8 -*-
"""日志.config —— 汉语库（由 tools/汉化库.py 从 Lib/logging/config.py 机械生成，**不要手改**）。

英文库 Lib/logging.config.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py logging
"""


"""
Configuration functions for the logging package for Python. The core package
is based on PEP 282 and comments thereto in comp.lang.python, and influenced
by Apache's log4j system.

Copyright (C) 2001-2022 Vinay Sajip. All Rights Reserved.

To use, simply 'import logging' and log away!
"""
_英文原名表 = {'BaseConfigurator': '配置器基类', 'ConvertingDict': '转换字典', 'ConvertingList': '转换列表', 'ConvertingMixin': '转换混入', 'ConvertingTuple': '转换元组', 'DEFAULT_LOGGING_CONFIG_PORT': '默认日志配置端口', 'DictConfigurator': '字典配置器', 'IDENTIFIER': '标识符', 'RESET_ERROR': '重置错误', 'dictConfig': '按字典配置', 'dictConfigClass': '字典配置器类', 'fileConfig': '读文件配置', 'listen': '监听配置', 'stopListening': '停止监听', 'valid_ident': '合法标识符吗'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
import errno
import functools
import io
import 日志
import 日志.handlers
import os
import queue
import re
import socket
import struct
import threading
import traceback
from socketserver import ThreadingTCPServer, StreamRequestHandler
默认日志配置端口 = 9030
重置错误 = errno.ECONNRESET
_listener = None

def 读文件配置(fname, defaults=None, disable_existing_loggers=True, encoding=None):
    """
    Read the logging configuration from a ConfigParser-format file.

    This can be called several times from an application, allowing an end user
    the ability to select from various pre-canned configurations (if the
    developer provides a mechanism to present the choices and load the chosen
    configuration).
    """
    import configparser
    if isinstance(fname, str):
        if not os.path.exists(fname):
            raise FileNotFoundError(f"{fname} doesn't exist")
        elif not os.path.getsize(fname):
            raise RuntimeError(f'{fname} is an empty file')
    if isinstance(fname, configparser.RawConfigParser):
        cp = fname
    else:
        try:
            cp = configparser.ConfigParser(defaults)
            if hasattr(fname, 'readline'):
                cp.read_file(fname)
            else:
                encoding = io.text_encoding(encoding)
                cp.read(fname, encoding=encoding)
        except configparser.ParsingError as e:
            raise RuntimeError(f'{fname} is invalid: {e}')
    formatters = _create_formatters(cp)
    with 日志._lock:
        _clearExistingHandlers()
        handlers = _install_handlers(cp, formatters)
        _install_loggers(cp, handlers, disable_existing_loggers)

def _resolve(name):
    """Resolve a dotted name to a global object."""
    name = name.split('.')
    used = name.pop(0)
    found = __import__(used)
    for n in name:
        used = used + '.' + n
        try:
            found = getattr(found, n)
        except AttributeError:
            __import__(used)
            found = getattr(found, n)
    return found

def _strip_spaces(alist):
    return map(str.strip, alist)

def _create_formatters(cp):
    """Create and return formatters"""
    flist = cp['formatters']['keys']
    if not len(flist):
        return {}
    flist = flist.split(',')
    flist = _strip_spaces(flist)
    formatters = {}
    for form in flist:
        sectname = 'formatter_%s' % form
        fs = cp.get(sectname, 'format', raw=True, fallback=None)
        dfs = cp.get(sectname, 'datefmt', raw=True, fallback=None)
        stl = cp.get(sectname, 'style', raw=True, fallback='%')
        defaults = cp.get(sectname, 'defaults', raw=True, fallback=None)
        c = 日志.Formatter
        class_name = cp[sectname].get('class')
        if class_name:
            c = _resolve(class_name)
        if defaults is not None:
            defaults = eval(defaults, vars(日志))
            f = c(fs, dfs, stl, defaults=defaults)
        else:
            f = c(fs, dfs, stl)
        formatters[form] = f
    return formatters

def _install_handlers(cp, formatters):
    """Install and return handlers"""
    hlist = cp['handlers']['keys']
    if not len(hlist):
        return {}
    hlist = hlist.split(',')
    hlist = _strip_spaces(hlist)
    handlers = {}
    fixups = []
    for hand in hlist:
        section = cp['handler_%s' % hand]
        klass = section['class']
        fmt = section.get('formatter', '')
        try:
            klass = eval(klass, vars(日志))
        except (AttributeError, NameError):
            klass = _resolve(klass)
        args = section.get('args', '()')
        args = eval(args, vars(日志))
        kwargs = section.get('kwargs', '{}')
        kwargs = eval(kwargs, vars(日志))
        h = klass(*args, **kwargs)
        h.name = hand
        if 'level' in section:
            level = section['level']
            h.setLevel(level)
        if len(fmt):
            h.setFormatter(formatters[fmt])
        if issubclass(klass, 日志.handlers.MemoryHandler):
            target = section.get('target', '')
            if len(target):
                fixups.append((h, target))
        handlers[hand] = h
    for h, t in fixups:
        h.setTarget(handlers[t])
    return handlers

def _handle_existing_loggers(existing, child_loggers, disable_existing):
    """
    When (re)configuring logging, handle loggers which were in the previous
    configuration but are not in the new configuration. There's no point
    deleting them as other threads may continue to hold references to them;
    and by disabling them, you stop them doing any logging.

    However, don't disable children of named loggers, as that's probably not
    what was intended by the user. Also, allow existing loggers to NOT be
    disabled if disable_existing is false.
    """
    root = 日志.root
    for log in existing:
        logger = root.manager.loggerDict[log]
        if log in child_loggers:
            if not isinstance(logger, 日志.PlaceHolder):
                logger.setLevel(日志.NOTSET)
                logger.handlers = []
                logger.propagate = True
        else:
            logger.disabled = disable_existing

def _install_loggers(cp, handlers, disable_existing):
    """Create and install loggers"""
    llist = cp['loggers']['keys']
    llist = llist.split(',')
    llist = list(_strip_spaces(llist))
    llist.remove('root')
    section = cp['logger_root']
    root = 日志.root
    log = root
    if 'level' in section:
        level = section['level']
        log.setLevel(level)
    for h in root.handlers[:]:
        root.removeHandler(h)
    hlist = section['handlers']
    if len(hlist):
        hlist = hlist.split(',')
        hlist = _strip_spaces(hlist)
        for hand in hlist:
            log.addHandler(handlers[hand])
    existing = list(root.manager.loggerDict.keys())
    existing.sort()
    child_loggers = []
    for log in llist:
        section = cp['logger_%s' % log]
        qn = section['qualname']
        propagate = section.getint('propagate', fallback=1)
        logger = 日志.getLogger(qn)
        if qn in existing:
            i = existing.index(qn) + 1
            prefixed = qn + '.'
            pflen = len(prefixed)
            num_existing = len(existing)
            while i < num_existing:
                if existing[i][:pflen] == prefixed:
                    child_loggers.append(existing[i])
                i += 1
            existing.remove(qn)
        if 'level' in section:
            level = section['level']
            logger.setLevel(level)
        for h in logger.handlers[:]:
            logger.removeHandler(h)
        logger.propagate = propagate
        logger.disabled = 0
        hlist = section['handlers']
        if len(hlist):
            hlist = hlist.split(',')
            hlist = _strip_spaces(hlist)
            for hand in hlist:
                logger.addHandler(handlers[hand])
    _handle_existing_loggers(existing, child_loggers, disable_existing)

def _clearExistingHandlers():
    """Clear and close existing handlers"""
    日志._handlers.clear()
    日志.shutdown(日志._handlerList[:])
    del 日志._handlerList[:]
标识符 = re.compile('^[a-z_][a-z0-9_]*$', re.I)

def 合法标识符吗(s):
    m = 标识符.match(s)
    if not m:
        raise ValueError('Not a valid Python identifier: %r' % s)
    return True

class 转换混入(object):
    """For ConvertingXXX's, this mixin class provides common functions"""

    def convert_with_key(self, key, value, replace=True):
        result = self.configurator.convert(value)
        if value is not result:
            if replace:
                self[key] = result
            if type(result) in (转换字典, 转换列表, 转换元组):
                result.parent = self
                result.key = key
        return result

    def convert(self, value):
        result = self.configurator.convert(value)
        if value is not result:
            if type(result) in (转换字典, 转换列表, 转换元组):
                result.parent = self
        return result

class 转换字典(dict, 转换混入):
    """A converting dictionary wrapper."""

    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        return self.convert_with_key(key, value)

    def get(self, key, default=None):
        value = dict.get(self, key, default)
        return self.convert_with_key(key, value)

    def pop(self, key, default=None):
        value = dict.pop(self, key, default)
        return self.convert_with_key(key, value, replace=False)

class 转换列表(list, 转换混入):
    """A converting list wrapper."""

    def __getitem__(self, key):
        value = list.__getitem__(self, key)
        return self.convert_with_key(key, value)

    def pop(self, idx=-1):
        value = list.pop(self, idx)
        return self.convert(value)

class 转换元组(tuple, 转换混入):
    """A converting tuple wrapper."""

    def __getitem__(self, key):
        value = tuple.__getitem__(self, key)
        return self.convert_with_key(key, value, replace=False)

class 配置器基类(object):
    """
    The configurator base class which defines some useful defaults.
    """
    CONVERT_PATTERN = re.compile('^(?P<prefix>[a-z]+)://(?P<suffix>.*)$')
    WORD_PATTERN = re.compile('^\\s*(\\w+)\\s*')
    DOT_PATTERN = re.compile('^\\.\\s*(\\w+)\\s*')
    INDEX_PATTERN = re.compile('^\\[([^\\[\\]]*)\\]\\s*')
    DIGIT_PATTERN = re.compile('^\\d+$')
    value_converters = {'ext': 'ext_convert', 'cfg': 'cfg_convert'}
    importer = staticmethod(__import__)

    def __init__(self, config):
        self.config = 转换字典(config)
        self.config.configurator = self

    def resolve(self, s):
        """
        Resolve strings to objects using standard import and attribute
        syntax.
        """
        name = s.split('.')
        used = name.pop(0)
        try:
            found = self.importer(used)
            for frag in name:
                used += '.' + frag
                try:
                    found = getattr(found, frag)
                except AttributeError:
                    self.importer(used)
                    found = getattr(found, frag)
            return found
        except ImportError as e:
            v = ValueError('Cannot resolve %r: %s' % (s, e))
            raise v from e

    def ext_convert(self, value):
        """Default converter for the ext:// protocol."""
        return self.resolve(value)

    def cfg_convert(self, value):
        """Default converter for the cfg:// protocol."""
        rest = value
        m = self.WORD_PATTERN.match(rest)
        if m is None:
            raise ValueError('Unable to convert %r' % value)
        else:
            rest = rest[m.end():]
            d = self.config[m.groups()[0]]
            while rest:
                m = self.DOT_PATTERN.match(rest)
                if m:
                    d = d[m.groups()[0]]
                else:
                    m = self.INDEX_PATTERN.match(rest)
                    if m:
                        idx = m.groups()[0]
                        if not self.DIGIT_PATTERN.match(idx):
                            d = d[idx]
                        else:
                            try:
                                n = int(idx)
                                d = d[n]
                            except TypeError:
                                d = d[idx]
                if m:
                    rest = rest[m.end():]
                else:
                    raise ValueError('Unable to convert %r at %r' % (value, rest))
        return d

    def convert(self, value):
        """
        Convert values to an appropriate type. dicts, lists and tuples are
        replaced by their converting alternatives. Strings are checked to
        see if they have a conversion format and are converted if they do.
        """
        if not isinstance(value, 转换字典) and isinstance(value, dict):
            value = 转换字典(value)
            value.configurator = self
        elif not isinstance(value, 转换列表) and isinstance(value, list):
            value = 转换列表(value)
            value.configurator = self
        elif not isinstance(value, 转换元组) and isinstance(value, tuple) and (not hasattr(value, '_fields')):
            value = 转换元组(value)
            value.configurator = self
        elif isinstance(value, str):
            m = self.CONVERT_PATTERN.match(value)
            if m:
                d = m.groupdict()
                prefix = d['prefix']
                converter = self.value_converters.get(prefix, None)
                if converter:
                    suffix = d['suffix']
                    converter = getattr(self, converter)
                    value = converter(suffix)
        return value

    def configure_custom(self, config):
        """Configure an object with a user-supplied factory."""
        c = config.pop('()')
        if not callable(c):
            c = self.resolve(c)
        kwargs = {k: config[k] for k in config if k != '.' and 合法标识符吗(k)}
        result = c(**kwargs)
        props = config.pop('.', None)
        if props:
            for name, value in props.items():
                setattr(result, name, value)
        return result

    def as_tuple(self, value):
        """Utility function which converts lists to tuples."""
        if isinstance(value, list):
            value = tuple(value)
        return value

def _is_queue_like_object(obj):
    """Check that *obj* implements the Queue API."""
    if isinstance(obj, (queue.Queue, queue.SimpleQueue)):
        return True
    from multiprocessing.queues import Queue as MPQueue
    if isinstance(obj, MPQueue):
        return True
    minimal_queue_interface = ['put_nowait', 'get']
    return all((callable(getattr(obj, method, None)) for method in minimal_queue_interface))

class 字典配置器(配置器基类):
    """
    Configure logging using a dictionary-like object to describe the
    configuration.
    """

    def configure(self):
        """Do the configuration."""
        config = self.config
        if 'version' not in config:
            raise ValueError("dictionary doesn't specify a version")
        if config['version'] != 1:
            raise ValueError('Unsupported version: %s' % config['version'])
        incremental = config.pop('incremental', False)
        EMPTY_DICT = {}
        with 日志._lock:
            if incremental:
                handlers = config.get('handlers', EMPTY_DICT)
                for name in handlers:
                    if name not in 日志._handlers:
                        raise ValueError('No handler found with name %r' % name)
                    else:
                        try:
                            handler = 日志._handlers[name]
                            handler_config = handlers[name]
                            level = handler_config.get('level', None)
                            if level:
                                handler.setLevel(日志._checkLevel(level))
                        except Exception as e:
                            raise ValueError('Unable to configure handler %r' % name) from e
                loggers = config.get('loggers', EMPTY_DICT)
                for name in loggers:
                    try:
                        self.configure_logger(name, loggers[name], True)
                    except Exception as e:
                        raise ValueError('Unable to configure logger %r' % name) from e
                root = config.get('root', None)
                if root:
                    try:
                        self.configure_root(root, True)
                    except Exception as e:
                        raise ValueError('Unable to configure root logger') from e
            else:
                disable_existing = config.pop('disable_existing_loggers', True)
                _clearExistingHandlers()
                formatters = config.get('formatters', EMPTY_DICT)
                for name in formatters:
                    try:
                        formatters[name] = self.configure_formatter(formatters[name])
                    except Exception as e:
                        raise ValueError('Unable to configure formatter %r' % name) from e
                filters = config.get('filters', EMPTY_DICT)
                for name in filters:
                    try:
                        filters[name] = self.configure_filter(filters[name])
                    except Exception as e:
                        raise ValueError('Unable to configure filter %r' % name) from e
                handlers = config.get('handlers', EMPTY_DICT)
                deferred = []
                for name in sorted(handlers):
                    try:
                        handler = self.configure_handler(handlers[name])
                        handler.name = name
                        handlers[name] = handler
                    except Exception as e:
                        if ' not configured yet' in str(e.__cause__):
                            deferred.append(name)
                        else:
                            raise ValueError('Unable to configure handler %r' % name) from e
                for name in deferred:
                    try:
                        handler = self.configure_handler(handlers[name])
                        handler.name = name
                        handlers[name] = handler
                    except Exception as e:
                        raise ValueError('Unable to configure handler %r' % name) from e
                root = 日志.root
                existing = list(root.manager.loggerDict.keys())
                existing.sort()
                child_loggers = []
                loggers = config.get('loggers', EMPTY_DICT)
                for name in loggers:
                    if name in existing:
                        i = existing.index(name) + 1
                        prefixed = name + '.'
                        pflen = len(prefixed)
                        num_existing = len(existing)
                        while i < num_existing:
                            if existing[i][:pflen] == prefixed:
                                child_loggers.append(existing[i])
                            i += 1
                        existing.remove(name)
                    try:
                        self.configure_logger(name, loggers[name])
                    except Exception as e:
                        raise ValueError('Unable to configure logger %r' % name) from e
                _handle_existing_loggers(existing, child_loggers, disable_existing)
                root = config.get('root', None)
                if root:
                    try:
                        self.configure_root(root)
                    except Exception as e:
                        raise ValueError('Unable to configure root logger') from e

    def configure_formatter(self, config):
        """Configure a formatter from a dictionary."""
        if '()' in config:
            factory = config['()']
            try:
                result = self.configure_custom(config)
            except TypeError as te:
                if "'format'" not in str(te):
                    raise
                config['fmt'] = config.pop('format')
                config['()'] = factory
                result = self.configure_custom(config)
        else:
            fmt = config.get('format', None)
            dfmt = config.get('datefmt', None)
            style = config.get('style', '%')
            cname = config.get('class', None)
            defaults = config.get('defaults', None)
            if not cname:
                c = 日志.Formatter
            else:
                c = _resolve(cname)
            kwargs = {}
            if defaults is not None:
                kwargs['defaults'] = defaults
            if 'validate' in config:
                result = c(fmt, dfmt, style, config['validate'], **kwargs)
            else:
                result = c(fmt, dfmt, style, **kwargs)
        return result

    def configure_filter(self, config):
        """Configure a filter from a dictionary."""
        if '()' in config:
            result = self.configure_custom(config)
        else:
            name = config.get('name', '')
            result = 日志.Filter(name)
        return result

    def add_filters(self, filterer, filters):
        """Add filters to a filterer from a list of names."""
        for f in filters:
            try:
                if callable(f) or callable(getattr(f, 'filter', None)):
                    filter_ = f
                else:
                    filter_ = self.config['filters'][f]
                filterer.addFilter(filter_)
            except Exception as e:
                raise ValueError('Unable to add filter %r' % f) from e

    def _configure_queue_handler(self, klass, **kwargs):
        if 'queue' in kwargs:
            q = kwargs.pop('queue')
        else:
            q = queue.Queue()
        rhl = kwargs.pop('respect_handler_level', False)
        lklass = kwargs.pop('listener', 日志.handlers.QueueListener)
        handlers = kwargs.pop('handlers', [])
        listener = lklass(q, *handlers, respect_handler_level=rhl)
        handler = klass(q, **kwargs)
        handler.listener = listener
        return handler

    def configure_handler(self, config):
        """Configure a handler from a dictionary."""
        config_copy = dict(config)
        formatter = config.pop('formatter', None)
        if formatter:
            try:
                formatter = self.config['formatters'][formatter]
            except Exception as e:
                raise ValueError('Unable to set formatter %r' % formatter) from e
        level = config.pop('level', None)
        filters = config.pop('filters', None)
        if '()' in config:
            c = config.pop('()')
            if not callable(c):
                c = self.resolve(c)
            factory = c
        else:
            cname = config.pop('class')
            if callable(cname):
                klass = cname
            else:
                klass = self.resolve(cname)
            if issubclass(klass, 日志.handlers.MemoryHandler):
                if 'flushLevel' in config:
                    config['flushLevel'] = 日志._checkLevel(config['flushLevel'])
                if 'target' in config:
                    try:
                        tn = config['target']
                        th = self.config['handlers'][tn]
                        if not isinstance(th, 日志.Handler):
                            config.update(config_copy)
                            raise TypeError('target not configured yet')
                        config['target'] = th
                    except Exception as e:
                        raise ValueError('Unable to set target handler %r' % tn) from e
            elif issubclass(klass, 日志.handlers.QueueHandler):
                if 'queue' in config:
                    qspec = config['queue']
                    if isinstance(qspec, str):
                        q = self.resolve(qspec)
                        if not callable(q):
                            raise TypeError('Invalid queue specifier %r' % qspec)
                        config['queue'] = q()
                    elif isinstance(qspec, dict):
                        if '()' not in qspec:
                            raise TypeError('Invalid queue specifier %r' % qspec)
                        config['queue'] = self.configure_custom(dict(qspec))
                    elif not _is_queue_like_object(qspec):
                        raise TypeError('Invalid queue specifier %r' % qspec)
                if 'listener' in config:
                    lspec = config['listener']
                    if isinstance(lspec, type):
                        if not issubclass(lspec, 日志.handlers.QueueListener):
                            raise TypeError('Invalid listener specifier %r' % lspec)
                    else:
                        if isinstance(lspec, str):
                            listener = self.resolve(lspec)
                            if isinstance(listener, type) and (not issubclass(listener, 日志.handlers.QueueListener)):
                                raise TypeError('Invalid listener specifier %r' % lspec)
                        elif isinstance(lspec, dict):
                            if '()' not in lspec:
                                raise TypeError('Invalid listener specifier %r' % lspec)
                            listener = self.configure_custom(dict(lspec))
                        else:
                            raise TypeError('Invalid listener specifier %r' % lspec)
                        if not callable(listener):
                            raise TypeError('Invalid listener specifier %r' % lspec)
                        config['listener'] = listener
                if 'handlers' in config:
                    hlist = []
                    try:
                        for hn in config['handlers']:
                            h = self.config['handlers'][hn]
                            if not isinstance(h, 日志.Handler):
                                config.update(config_copy)
                                raise TypeError('Required handler %r is not configured yet' % hn)
                            hlist.append(h)
                    except Exception as e:
                        raise ValueError('Unable to set required handler %r' % hn) from e
                    config['handlers'] = hlist
            elif issubclass(klass, 日志.handlers.SMTPHandler) and 'mailhost' in config:
                config['mailhost'] = self.as_tuple(config['mailhost'])
            elif issubclass(klass, 日志.handlers.SysLogHandler) and 'address' in config:
                config['address'] = self.as_tuple(config['address'])
            if issubclass(klass, 日志.handlers.QueueHandler):
                factory = functools.partial(self._configure_queue_handler, klass)
            else:
                factory = klass
        kwargs = {k: config[k] for k in config if k != '.' and 合法标识符吗(k)}
        try:
            result = factory(**kwargs)
        except TypeError as te:
            if "'stream'" not in str(te):
                raise
            kwargs['strm'] = kwargs.pop('stream')
            result = factory(**kwargs)
            import warnings
            warnings.warn("Support for custom logging handlers with the 'strm' argument is deprecated and scheduled for removal in Python 3.16. Define handlers with the 'stream' argument instead.", DeprecationWarning, stacklevel=2)
        if formatter:
            result.setFormatter(formatter)
        if level is not None:
            result.setLevel(日志._checkLevel(level))
        if filters:
            self.add_filters(result, filters)
        props = config.pop('.', None)
        if props:
            for name, value in props.items():
                setattr(result, name, value)
        return result

    def add_handlers(self, logger, handlers):
        """Add handlers to a logger from a list of names."""
        for h in handlers:
            try:
                logger.addHandler(self.config['handlers'][h])
            except Exception as e:
                raise ValueError('Unable to add handler %r' % h) from e

    def common_logger_config(self, logger, config, incremental=False):
        """
        Perform configuration which is common to root and non-root loggers.
        """
        level = config.get('level', None)
        if level is not None:
            logger.setLevel(日志._checkLevel(level))
        if not incremental:
            for h in logger.handlers[:]:
                logger.removeHandler(h)
            handlers = config.get('handlers', None)
            if handlers:
                self.add_handlers(logger, handlers)
            filters = config.get('filters', None)
            if filters:
                self.add_filters(logger, filters)

    def configure_logger(self, name, config, incremental=False):
        """Configure a non-root logger from a dictionary."""
        logger = 日志.getLogger(name)
        self.common_logger_config(logger, config, incremental)
        logger.disabled = False
        propagate = config.get('propagate', None)
        if propagate is not None:
            logger.propagate = propagate

    def configure_root(self, config, incremental=False):
        """Configure a root logger from a dictionary."""
        root = 日志.getLogger()
        self.common_logger_config(root, config, incremental)
字典配置器类 = 字典配置器

def 按字典配置(config):
    """Configure logging using a dictionary."""
    字典配置器类(config).configure()

def 监听配置(port=默认日志配置端口, verify=None):
    """
    Start up a socket server on the specified port, and listen for new
    configurations.

    These will be sent as a file suitable for processing by fileConfig().
    Returns a Thread object on which you can call start() to start the server,
    and which you can join() when appropriate. To stop the server, call
    stopListening().

    Use the ``verify`` argument to verify any bytes received across the wire
    from a client. If specified, it should be a callable which receives a
    single argument - the bytes of configuration data received across the
    network - and it should return either ``None``, to indicate that the
    passed in bytes could not be verified and should be discarded, or a
    byte string which is then passed to the configuration machinery as
    normal. Note that you can return transformed bytes, e.g. by decrypting
    the bytes passed in.
    """

    class ConfigStreamHandler(StreamRequestHandler):
        """
        Handler for a logging configuration request.

        It expects a completely new logging configuration and uses fileConfig
        to install it.
        """

        def handle(self):
            """
            Handle a request.

            Each request is expected to be a 4-byte length, packed using
            struct.pack(">L", n), followed by the config file.
            Uses fileConfig() to do the grunt work.
            """
            try:
                conn = self.connection
                chunk = conn.recv(4)
                if len(chunk) == 4:
                    slen = struct.unpack('>L', chunk)[0]
                    chunk = self.connection.recv(slen)
                    while len(chunk) < slen:
                        chunk = chunk + conn.recv(slen - len(chunk))
                    if self.server.verify is not None:
                        chunk = self.server.verify(chunk)
                    if chunk is not None:
                        chunk = chunk.decode('utf-8')
                        try:
                            import json
                            d = json.loads(chunk)
                            assert isinstance(d, dict)
                            按字典配置(d)
                        except Exception:
                            file = io.StringIO(chunk)
                            try:
                                读文件配置(file)
                            except Exception:
                                traceback.print_exc()
                    if self.server.ready:
                        self.server.ready.set()
            except OSError as e:
                if e.errno != 重置错误:
                    raise

    class ConfigSocketReceiver(ThreadingTCPServer):
        """
        A simple TCP socket-based logging config receiver.
        """
        allow_reuse_address = True
        allow_reuse_port = False

        def __init__(self, host='localhost', port=默认日志配置端口, handler=None, ready=None, verify=None):
            try:
                infos = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
            except OSError:
                pass
            else:
                if not any((info[0] == socket.AF_INET for info in infos)):
                    self.address_family = infos[0][0]
            ThreadingTCPServer.__init__(self, (host, port), handler)
            with 日志._lock:
                self.abort = 0
            self.timeout = 1
            self.ready = ready
            self.verify = verify

        def serve_until_stopped(self):
            import select
            abort = 0
            while not abort:
                rd, wr, ex = select.select([self.socket.fileno()], [], [], self.timeout)
                if rd:
                    self.handle_request()
                with 日志._lock:
                    abort = self.abort
            self.server_close()

    class Server(threading.Thread):

        def __init__(self, rcvr, hdlr, port, verify):
            super(Server, self).__init__()
            self.rcvr = rcvr
            self.hdlr = hdlr
            self.port = port
            self.verify = verify
            self.ready = threading.Event()

        def run(self):
            try:
                server = self.rcvr(port=self.port, handler=self.hdlr, ready=self.ready, verify=self.verify)
            except BaseException:
                self.ready.set()
                raise
            if self.port == 0:
                self.port = server.server_address[1]
            self.ready.set()
            global _listener
            with 日志._lock:
                _listener = server
            server.serve_until_stopped()
    return Server(ConfigSocketReceiver, ConfigStreamHandler, port, verify)

def 停止监听():
    """
    Stop the listening server which was created with a call to listen().
    """
    global _listener
    with 日志._lock:
        if _listener:
            _listener.abort = 1
            _listener = None


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'BaseConfigurator': '配置器基类',
    'ConvertingDict': '转换字典',
    'ConvertingList': '转换列表',
    'ConvertingMixin': '转换混入',
    'ConvertingTuple': '转换元组',
    'DEFAULT_LOGGING_CONFIG_PORT': '默认日志配置端口',
    'DictConfigurator': '字典配置器',
    'IDENTIFIER': '标识符',
    'RESET_ERROR': '重置错误',
    'dictConfig': '按字典配置',
    'dictConfigClass': '字典配置器类',
    'fileConfig': '读文件配置',
    'listen': '监听配置',
    'stopListening': '停止监听',
    'valid_ident': '合法标识符吗',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# ---- 转发层结束 ----
