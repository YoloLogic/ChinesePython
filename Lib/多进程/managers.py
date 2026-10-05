# -*- coding: utf-8 -*-
"""多进程.managers —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/managers.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.managers.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


__all__ = ['BaseManager', 'SyncManager', 'BaseProxy', 'Token']
import sys
import threading
import signal
import array
import collections.abc
import queue
import time
import types
import os
from os import getpid
from traceback import format_exc
from . import connection
from .context import reduction, get_spawning_popen, ProcessError
from . import pool
from . import process
from . import util
from . import get_context
try:
    from . import shared_memory
except ImportError:
    HAS_SHMEM = False
else:
    HAS_SHMEM = True
    __all__.append('SharedMemoryManager')

def 归约数组(a):
    return (array.array, (a.typecode, a.tobytes()))
reduction.register(array.array, 归约数组)
view_types = [type(getattr({}, name)()) for name in ('items', 'keys', 'values')]

def 重建为列表(obj):
    return (list, (list(obj),))
for view_type in view_types:
    reduction.register(view_type, 重建为列表)
del view_type, view_types

class 令牌(object):
    """
    Type to uniquely identify a shared object
    """
    __slots__ = ('typeid', 'address', 'id')

    def __init__(self, typeid, address, id):
        self.typeid, self.address, self.id = (typeid, address, id)

    def __getstate__(self):
        return (self.typeid, self.address, self.id)

    def __setstate__(self, state):
        self.typeid, self.address, self.id = state

    def __repr__(self):
        return '%s(typeid=%r, address=%r, id=%r)' % (self.__class__.__name__, self.typeid, self.address, self.id)

def 分派(c, id, methodname, args=(), kwds={}):
    """
    Send a message to manager using connection `c` and return response
    """
    c.send((id, methodname, args, kwds))
    kind, result = c.recv()
    if kind == '#RETURN':
        return result
    try:
        raise 转成错误(kind, result)
    finally:
        del result

def 转成错误(kind, result):
    if kind == '#ERROR':
        return result
    elif kind in ('#TRACEBACK', '#UNSERIALIZABLE'):
        if not isinstance(result, str):
            raise TypeError("Result {0!r} (kind '{1}') type is {2}, not str".format(result, kind, type(result)))
        if kind == '#UNSERIALIZABLE':
            return 远端错误('Unserializable message: %s\n' % result)
        else:
            return 远端错误(result)
    else:
        return ValueError('Unrecognized message type {!r}'.format(kind))

class 远端错误(Exception):

    def __str__(self):
        return '\n' + '-' * 75 + '\n' + str(self.args[0]) + '-' * 75

def 全部方法(obj):
    """
    Return a list of names of methods of `obj`
    """
    temp = []
    for name in dir(obj):
        func = getattr(obj, name)
        if callable(func):
            temp.append(name)
    return temp

def 公开方法(obj):
    """
    Return a list of names of methods of `obj` which do not start with '_'
    """
    return [name for name in 全部方法(obj) if name[0] != '_']

class 服务器(object):
    """
    Server class which runs in a process controlled by a manager object
    """
    public = ['shutdown', 'create', 'accept_connection', 'get_methods', 'debug_info', 'number_of_objects', 'dummy', 'incref', 'decref']

    def __init__(self, registry, address, authkey, serializer):
        if not isinstance(authkey, bytes):
            raise TypeError('Authkey {0!r} is type {1!s}, not bytes'.format(authkey, type(authkey)))
        self.registry = registry
        self.authkey = process.AuthenticationString(authkey)
        Listener, Client = listener_client[serializer]
        self.listener = Listener(address=address, backlog=128)
        self.address = self.listener.address
        self.id_to_obj = {'0': (None, ())}
        self.id_to_refcount = {}
        self.id_to_local_proxy_obj = {}
        self.mutex = threading.Lock()

    def serve_forever(self):
        """
        Run the server forever
        """
        self.stop_event = threading.Event()
        process.current_process()._manager_server = self
        try:
            accepter = threading.Thread(target=self.accepter)
            accepter.daemon = True
            accepter.start()
            try:
                while not self.stop_event.is_set():
                    self.stop_event.wait(1)
            except (KeyboardInterrupt, SystemExit):
                pass
        finally:
            if sys.stdout != sys.__stdout__:
                util.debug('resetting stdout, stderr')
                sys.stdout = sys.__stdout__
                sys.stderr = sys.__stderr__
            sys.exit(0)

    def accepter(self):
        while True:
            try:
                c = self.listener.accept()
            except OSError:
                continue
            t = threading.Thread(target=self.handle_request, args=(c,))
            t.daemon = True
            t.start()

    def _handle_request(self, c):
        request = None
        try:
            connection.deliver_challenge(c, self.authkey)
            connection.answer_challenge(c, self.authkey)
            request = c.recv()
            ignore, funcname, args, kwds = request
            assert funcname in self.public, '%r unrecognized' % funcname
            func = getattr(self, funcname)
        except Exception:
            msg = ('#TRACEBACK', format_exc())
        else:
            try:
                result = func(c, *args, **kwds)
            except Exception:
                msg = ('#TRACEBACK', format_exc())
            else:
                msg = ('#RETURN', result)
        try:
            c.send(msg)
        except Exception as e:
            try:
                c.send(('#TRACEBACK', format_exc()))
            except Exception:
                pass
            util.info('Failure to send message: %r', msg)
            util.info(' ... request was %r', request)
            util.info(' ... exception was %r', e)

    def handle_request(self, conn):
        """
        Handle a new connection
        """
        try:
            self._handle_request(conn)
        except SystemExit:
            pass
        finally:
            conn.close()

    def serve_client(self, conn):
        """
        Handle requests from the proxies in a particular process/thread
        """
        util.debug('starting server thread to service %r', threading.current_thread().name)
        recv = conn.recv
        send = conn.send
        id_to_obj = self.id_to_obj
        while not self.stop_event.is_set():
            try:
                methodname = obj = None
                request = recv()
                ident, methodname, args, kwds = request
                try:
                    obj, exposed, gettypeid = id_to_obj[ident]
                except KeyError as ke:
                    try:
                        obj, exposed, gettypeid = self.id_to_local_proxy_obj[ident]
                    except KeyError:
                        raise ke
                if methodname not in exposed:
                    raise AttributeError('method %r of %r object is not in exposed=%r' % (methodname, type(obj), exposed))
                function = getattr(obj, methodname)
                try:
                    res = function(*args, **kwds)
                except Exception as e:
                    msg = ('#ERROR', e)
                else:
                    typeid = gettypeid and gettypeid.get(methodname, None)
                    if typeid:
                        rident, rexposed = self.create(conn, typeid, res)
                        token = 令牌(typeid, self.address, rident)
                        msg = ('#PROXY', (rexposed, token))
                    else:
                        msg = ('#RETURN', res)
            except AttributeError:
                if methodname is None:
                    msg = ('#TRACEBACK', format_exc())
                else:
                    try:
                        fallback_func = self.fallback_mapping[methodname]
                        result = fallback_func(self, conn, ident, obj, *args, **kwds)
                        msg = ('#RETURN', result)
                    except Exception:
                        msg = ('#TRACEBACK', format_exc())
            except EOFError:
                util.debug('got EOF -- exiting thread serving %r', threading.current_thread().name)
                sys.exit(0)
            except Exception:
                msg = ('#TRACEBACK', format_exc())
            try:
                try:
                    send(msg)
                except Exception:
                    send(('#UNSERIALIZABLE', format_exc()))
            except Exception as e:
                util.info('exception in thread serving %r', threading.current_thread().name)
                util.info(' ... message was %r', msg)
                util.info(' ... exception was %r', e)
                conn.close()
                sys.exit(1)

    def fallback_getvalue(self, conn, ident, obj):
        return obj

    def fallback_str(self, conn, ident, obj):
        return str(obj)

    def fallback_repr(self, conn, ident, obj):
        return repr(obj)
    fallback_mapping = {'__str__': fallback_str, '__repr__': fallback_repr, '#GETVALUE': fallback_getvalue}

    def dummy(self, c):
        pass

    def debug_info(self, c):
        """
        Return some info --- useful to spot problems with refcounting
        """
        with self.mutex:
            result = []
            keys = list(self.id_to_refcount.keys())
            keys.sort()
            for ident in keys:
                if ident != '0':
                    result.append('  %s:       refcount=%s\n    %s' % (ident, self.id_to_refcount[ident], str(self.id_to_obj[ident][0])[:75]))
            return '\n'.join(result)

    def number_of_objects(self, c):
        """
        Number of shared objects
        """
        return len(self.id_to_refcount)

    def shutdown(self, c):
        """
        Shutdown this process
        """
        try:
            util.debug('manager received shutdown message')
            c.send(('#RETURN', None))
        except:
            import traceback
            traceback.print_exc()
        finally:
            self.stop_event.set()

    def create(self, c, typeid, /, *args, **kwds):
        """
        Create a new shared object and return its id
        """
        with self.mutex:
            callable, exposed, method_to_typeid, proxytype = self.registry[typeid]
            if callable is None:
                if kwds or len(args) != 1:
                    raise ValueError('Without callable, must have one non-keyword argument')
                obj = args[0]
            else:
                obj = callable(*args, **kwds)
            if exposed is None:
                exposed = 公开方法(obj)
            if method_to_typeid is not None:
                if not isinstance(method_to_typeid, dict):
                    raise TypeError('Method_to_typeid {0!r}: type {1!s}, not dict'.format(method_to_typeid, type(method_to_typeid)))
                exposed = list(exposed) + list(method_to_typeid)
            ident = '%x' % id(obj)
            util.debug('%r callable returned object with id %r', typeid, ident)
            self.id_to_obj[ident] = (obj, set(exposed), method_to_typeid)
            if ident not in self.id_to_refcount:
                self.id_to_refcount[ident] = 0
        self.incref(c, ident)
        return (ident, tuple(exposed))

    def get_methods(self, c, token):
        """
        Return the methods of the shared object indicated by token
        """
        return tuple(self.id_to_obj[token.id][1])

    def accept_connection(self, c, name):
        """
        Spawn a new thread to serve this connection
        """
        threading.current_thread().name = name
        c.send(('#RETURN', None))
        self.serve_client(c)

    def incref(self, c, ident):
        with self.mutex:
            try:
                self.id_to_refcount[ident] += 1
            except KeyError as ke:
                if ident in self.id_to_local_proxy_obj:
                    self.id_to_refcount[ident] = 1
                    self.id_to_obj[ident] = self.id_to_local_proxy_obj[ident]
                    util.debug('Server re-enabled tracking & INCREF %r', ident)
                else:
                    raise ke

    def decref(self, c, ident):
        if ident not in self.id_to_refcount and ident in self.id_to_local_proxy_obj:
            util.debug('Server DECREF skipping %r', ident)
            return
        with self.mutex:
            if self.id_to_refcount[ident] <= 0:
                raise AssertionError('Id {0!s} ({1!r}) has refcount {2:n}, not 1+'.format(ident, self.id_to_obj[ident], self.id_to_refcount[ident]))
            self.id_to_refcount[ident] -= 1
            if self.id_to_refcount[ident] == 0:
                del self.id_to_refcount[ident]
        if ident not in self.id_to_refcount:
            self.id_to_obj[ident] = (None, (), None)
            util.debug('disposing of obj with id %r', ident)
            with self.mutex:
                del self.id_to_obj[ident]

class 状态(object):
    __slots__ = ['value']
    INITIAL = 0
    STARTED = 1
    SHUTDOWN = 2
listener_client = {'pickle': (connection.Listener, connection.Client), 'xmlrpclib': (connection.XmlListener, connection.XmlClient)}

class 管理器基类(object):
    """
    Base class for managers
    """
    _registry = {}
    _Server = 服务器

    def __init__(self, address=None, authkey=None, serializer='pickle', ctx=None, *, shutdown_timeout=1.0):
        if authkey is None:
            authkey = process.current_process().authkey
        self._address = address
        self._authkey = process.AuthenticationString(authkey)
        self._state = 状态()
        self._state.value = 状态.INITIAL
        self._serializer = serializer
        self._Listener, self._Client = listener_client[serializer]
        self._ctx = ctx or get_context()
        self._shutdown_timeout = shutdown_timeout

    def get_server(self):
        """
        Return server object with serve_forever() method and address attribute
        """
        if self._state.value != 状态.INITIAL:
            if self._state.value == 状态.STARTED:
                raise ProcessError('Already started server')
            elif self._state.value == 状态.SHUTDOWN:
                raise ProcessError('Manager has shut down')
            else:
                raise ProcessError('Unknown state {!r}'.format(self._state.value))
        return 服务器(self._registry, self._address, self._authkey, self._serializer)

    def connect(self):
        """
        Connect manager object to the server process
        """
        Listener, Client = listener_client[self._serializer]
        conn = Client(self._address, authkey=self._authkey)
        分派(conn, None, 'dummy')
        self._state.value = 状态.STARTED

    def start(self, initializer=None, initargs=()):
        """
        Spawn a server process for this manager object
        """
        if self._state.value != 状态.INITIAL:
            if self._state.value == 状态.STARTED:
                raise ProcessError('Already started server')
            elif self._state.value == 状态.SHUTDOWN:
                raise ProcessError('Manager has shut down')
            else:
                raise ProcessError('Unknown state {!r}'.format(self._state.value))
        if initializer is not None and (not callable(initializer)):
            raise TypeError('initializer must be a callable')
        reader, writer = connection.Pipe(duplex=False)
        self._process = self._ctx.Process(target=type(self)._run_server, args=(self._registry, self._address, self._authkey, self._serializer, writer, initializer, initargs))
        ident = ':'.join((str(i) for i in self._process._identity))
        self._process.name = type(self).__name__ + '-' + ident
        self._process.start()
        writer.close()
        self._address = reader.recv()
        reader.close()
        self._state.value = 状态.STARTED
        self.shutdown = util.Finalize(self, type(self)._finalize_manager, args=(self._process, self._address, self._authkey, self._state, self._Client, self._shutdown_timeout), exitpriority=0)

    @classmethod
    def _run_server(cls, registry, address, authkey, serializer, writer, initializer=None, initargs=()):
        """
        Create a server, report its address and run it
        """
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        if initializer is not None:
            initializer(*initargs)
        server = cls._Server(registry, address, authkey, serializer)
        writer.send(server.address)
        writer.close()
        util.info('manager serving at %r', server.address)
        server.serve_forever()

    def _create(self, typeid, /, *args, **kwds):
        """
        Create a new shared object; return the token and exposed tuple
        """
        assert self._state.value == 状态.STARTED, 'server not yet started'
        conn = self._Client(self._address, authkey=self._authkey)
        try:
            id, exposed = 分派(conn, None, 'create', (typeid,) + args, kwds)
        finally:
            conn.close()
        return (令牌(typeid, self._address, id), exposed)

    def join(self, timeout=None):
        """
        Join the manager process (if it has been spawned)
        """
        if self._process is not None:
            self._process.join(timeout)
            if not self._process.is_alive():
                self._process = None

    def _debug_info(self):
        """
        Return some info about the servers shared objects and connections
        """
        conn = self._Client(self._address, authkey=self._authkey)
        try:
            return 分派(conn, None, 'debug_info')
        finally:
            conn.close()

    def _number_of_objects(self):
        """
        Return the number of shared objects
        """
        conn = self._Client(self._address, authkey=self._authkey)
        try:
            return 分派(conn, None, 'number_of_objects')
        finally:
            conn.close()

    def __enter__(self):
        if self._state.value == 状态.INITIAL:
            self.start()
        if self._state.value != 状态.STARTED:
            if self._state.value == 状态.INITIAL:
                raise ProcessError('Unable to start server')
            elif self._state.value == 状态.SHUTDOWN:
                raise ProcessError('Manager has shut down')
            else:
                raise ProcessError('Unknown state {!r}'.format(self._state.value))
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    @staticmethod
    def _finalize_manager(process, address, authkey, state, _Client, shutdown_timeout):
        """
        Shutdown the manager process; will be registered as a finalizer
        """
        if process.is_alive():
            util.info('sending shutdown message to manager')
            try:
                conn = _Client(address, authkey=authkey)
                try:
                    分派(conn, None, 'shutdown')
                finally:
                    conn.close()
            except Exception:
                pass
            process.join(timeout=shutdown_timeout)
            if process.is_alive():
                util.info('manager still alive')
                if hasattr(process, 'terminate'):
                    util.info('trying to `terminate()` manager process')
                    process.terminate()
                    process.join(timeout=shutdown_timeout)
                    if process.is_alive():
                        util.info('manager still alive after terminate')
                        process.kill()
                        process.join()
        state.value = 状态.SHUTDOWN
        try:
            del BaseProxy._address_to_local[address]
        except KeyError:
            pass

    @property
    def address(self):
        return self._address

    @classmethod
    def register(cls, typeid, callable=None, proxytype=None, exposed=None, method_to_typeid=None, create_method=True):
        """
        Register a typeid with the manager type
        """
        if '_registry' not in cls.__dict__:
            cls._registry = cls._registry.copy()
        if proxytype is None:
            proxytype = 自动代理
        exposed = exposed or getattr(proxytype, '_exposed_', None)
        method_to_typeid = method_to_typeid or getattr(proxytype, '_method_to_typeid_', None)
        if method_to_typeid:
            for key, value in list(method_to_typeid.items()):
                assert type(key) is str, '%r is not a string' % key
                assert type(value) is str, '%r is not a string' % value
        cls._registry[typeid] = (callable, exposed, method_to_typeid, proxytype)
        if create_method:

            def temp(self, /, *args, **kwds):
                util.debug('requesting creation of a shared %r object', typeid)
                token, exp = self._create(typeid, *args, **kwds)
                proxy = proxytype(token, self._serializer, manager=self, authkey=self._authkey, exposed=exp)
                conn = self._Client(token.address, authkey=self._authkey)
                分派(conn, None, 'decref', (token.id,))
                return proxy
            temp.__name__ = typeid
            setattr(cls, typeid, temp)

class 进程局部集合(set):

    def __init__(self):
        util.register_after_fork(self, lambda obj: obj.clear())

    def __reduce__(self):
        return (type(self), ())

class BaseProxy(object):
    """
    A base for proxies of shared objects
    """
    _address_to_local = {}
    _mutex = util.ForkAwareThreadLock()
    _next_serial = 1

    def __init__(self, token, serializer, manager=None, authkey=None, exposed=None, incref=True, manager_owned=False):
        with BaseProxy._mutex:
            tls_serials = BaseProxy._address_to_local.get(token.address, None)
            if tls_serials is None:
                tls_serials = (util.ForkAwareLocal(), 进程局部集合())
                BaseProxy._address_to_local[token.address] = tls_serials
            self._serial = BaseProxy._next_serial
            BaseProxy._next_serial += 1
        self._tls = tls_serials[0]
        self._all_serials = tls_serials[1]
        self._token = token
        self._id = self._token.id
        self._manager = manager
        self._serializer = serializer
        self._Client = listener_client[serializer][1]
        self._owned_by_manager = manager_owned
        if authkey is not None:
            self._authkey = process.AuthenticationString(authkey)
        elif self._manager is not None:
            self._authkey = self._manager._authkey
        else:
            self._authkey = process.current_process().authkey
        if incref:
            self._incref()
        util.register_after_fork(self, BaseProxy._after_fork)

    def _connect(self):
        util.debug('making connection to manager')
        name = process.current_process().name
        if threading.current_thread().name != 'MainThread':
            name += '|' + threading.current_thread().name
        conn = self._Client(self._token.address, authkey=self._authkey)
        分派(conn, None, 'accept_connection', (name,))
        self._tls.connection = conn

    def _callmethod(self, methodname, args=(), kwds={}):
        """
        Try to call a method of the referent and return a copy of the result
        """
        try:
            conn = self._tls.connection
        except AttributeError:
            util.debug('thread %r does not own a connection', threading.current_thread().name)
            self._connect()
            conn = self._tls.connection
        conn.send((self._id, methodname, args, kwds))
        kind, result = conn.recv()
        if kind == '#RETURN':
            return result
        elif kind == '#PROXY':
            exposed, token = result
            proxytype = self._manager._registry[token.typeid][-1]
            token.address = self._token.address
            proxy = proxytype(token, self._serializer, manager=self._manager, authkey=self._authkey, exposed=exposed)
            conn = self._Client(token.address, authkey=self._authkey)
            分派(conn, None, 'decref', (token.id,))
            return proxy
        try:
            raise 转成错误(kind, result)
        finally:
            del result

    def _getvalue(self):
        """
        Get a copy of the value of the referent
        """
        return self._callmethod('#GETVALUE')

    def _incref(self):
        if self._owned_by_manager:
            util.debug('owned_by_manager skipped INCREF of %r', self._token.id)
            return
        conn = self._Client(self._token.address, authkey=self._authkey)
        分派(conn, None, 'incref', (self._id,))
        util.debug('INCREF %r', self._token.id)
        self._all_serials.add(self._serial)
        state = self._manager and self._manager._state
        self._close = util.Finalize(self, BaseProxy._decref, args=(self._token, self._serial, self._authkey, state, self._tls, self._all_serials, self._Client), exitpriority=10)

    @staticmethod
    def _decref(token, serial, authkey, state, tls, idset, _Client):
        idset.discard(serial)
        if state is None or state.value == 状态.STARTED:
            try:
                util.debug('DECREF %r', token.id)
                conn = _Client(token.address, authkey=authkey)
                分派(conn, None, 'decref', (token.id,))
            except Exception as e:
                util.debug('... decref failed %s', e)
        else:
            util.debug('DECREF %r -- manager already shutdown', token.id)
        if not idset and hasattr(tls, 'connection'):
            util.debug('thread %r has no more proxies so closing conn', threading.current_thread().name)
            tls.connection.close()
            del tls.connection

    def _after_fork(self):
        self._manager = None
        try:
            self._incref()
        except Exception as e:
            util.info('incref failed: %s' % e)

    def __reduce__(self):
        kwds = {}
        if get_spawning_popen() is not None:
            kwds['authkey'] = self._authkey
        if getattr(self, '_isauto', False):
            kwds['exposed'] = self._exposed_
            return (重建代理, (自动代理, self._token, self._serializer, kwds))
        else:
            return (重建代理, (type(self), self._token, self._serializer, kwds))

    def __deepcopy__(self, memo):
        return self._getvalue()

    def __repr__(self):
        return '<%s object, typeid %r at %#x>' % (type(self).__name__, self._token.typeid, id(self))

    def __str__(self):
        """
        Return representation of the referent (or a fall-back if that fails)
        """
        try:
            return self._callmethod('__repr__')
        except Exception:
            return repr(self)[:-1] + "; '__str__()' failed>"

def 重建代理(func, token, serializer, kwds):
    """
    Function used for unpickling proxy objects.
    """
    server = getattr(process.current_process(), '_manager_server', None)
    if server and server.address == token.address:
        util.debug('Rebuild a proxy owned by manager, token=%r', token)
        kwds['manager_owned'] = True
        if token.id not in server.id_to_local_proxy_obj:
            server.id_to_local_proxy_obj[token.id] = server.id_to_obj[token.id]
    incref = kwds.pop('incref', True) and (not getattr(process.current_process(), '_inheriting', False))
    return func(token, serializer, incref=incref, **kwds)

def 造代理类型(name, exposed, _cache={}):
    """
    Return a proxy type whose methods are given by `exposed`
    """
    exposed = tuple(exposed)
    try:
        return _cache[name, exposed]
    except KeyError:
        pass
    dic = {}
    for meth in exposed:
        exec('def %s(self, /, *args, **kwds):\n        return self._callmethod(%r, args, kwds)' % (meth, meth), dic)
    ProxyType = type(name, (BaseProxy,), dic)
    ProxyType._exposed_ = exposed
    _cache[name, exposed] = ProxyType
    return ProxyType

def 自动代理(token, serializer, manager=None, authkey=None, exposed=None, incref=True, manager_owned=False):
    """
    Return an auto-proxy for `token`
    """
    _Client = listener_client[serializer][1]
    if exposed is None:
        conn = _Client(token.address, authkey=authkey)
        try:
            exposed = 分派(conn, None, 'get_methods', (token,))
        finally:
            conn.close()
    if authkey is None and manager is not None:
        authkey = manager._authkey
    if authkey is None:
        authkey = process.current_process().authkey
    ProxyType = 造代理类型('AutoProxy[%s]' % token.typeid, exposed)
    proxy = ProxyType(token, serializer, manager=manager, authkey=authkey, incref=incref, manager_owned=manager_owned)
    proxy._isauto = True
    return proxy

class Namespace(object):

    def __init__(self, /, **kwds):
        self.__dict__.update(kwds)

    def __repr__(self):
        items = list(self.__dict__.items())
        temp = []
        for name, value in items:
            if not name.startswith('_'):
                temp.append('%s=%r' % (name, value))
        temp.sort()
        return '%s(%s)' % (self.__class__.__name__, ', '.join(temp))

class 值(object):

    def __init__(self, typecode, value, lock=True):
        self._typecode = typecode
        self._value = value

    def get(self):
        return self._value

    def set(self, value):
        self._value = value

    def __repr__(self):
        return '%s(%r, %r)' % (type(self).__name__, self._typecode, self._value)
    value = property(get, set)

def 数组(typecode, sequence, lock=True):
    return array.array(typecode, sequence)

class IteratorProxy(BaseProxy):
    _exposed_ = ('__next__', 'send', 'throw', 'close')

    def __iter__(self):
        return self

    def __next__(self, *args):
        return self._callmethod('__next__', args)

    def send(self, *args):
        return self._callmethod('send', args)

    def throw(self, *args):
        return self._callmethod('throw', args)

    def close(self, *args):
        return self._callmethod('close', args)

class AcquirerProxy(BaseProxy):
    _exposed_ = ('acquire', 'release', 'locked')

    def acquire(self, blocking=True, timeout=None):
        args = (blocking,) if timeout is None else (blocking, timeout)
        return self._callmethod('acquire', args)

    def release(self):
        return self._callmethod('release')

    def locked(self):
        return self._callmethod('locked')

    def __enter__(self):
        return self._callmethod('acquire')

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._callmethod('release')

class ConditionProxy(AcquirerProxy):
    _exposed_ = ('acquire', 'release', 'locked', 'wait', 'notify', 'notify_all')

    def wait(self, timeout=None):
        return self._callmethod('wait', (timeout,))

    def notify(self, n=1):
        return self._callmethod('notify', (n,))

    def notify_all(self):
        return self._callmethod('notify_all')

    def wait_for(self, predicate, timeout=None):
        result = predicate()
        if result:
            return result
        if timeout is not None:
            endtime = time.monotonic() + timeout
        else:
            endtime = None
            waittime = None
        while not result:
            if endtime is not None:
                waittime = endtime - time.monotonic()
                if waittime <= 0:
                    break
            self.wait(waittime)
            result = predicate()
        return result

class EventProxy(BaseProxy):
    _exposed_ = ('is_set', 'set', 'clear', 'wait')

    def is_set(self):
        return self._callmethod('is_set')

    def set(self):
        return self._callmethod('set')

    def clear(self):
        return self._callmethod('clear')

    def wait(self, timeout=None):
        return self._callmethod('wait', (timeout,))

class BarrierProxy(BaseProxy):
    _exposed_ = ('__getattribute__', 'wait', 'abort', 'reset')

    def wait(self, timeout=None):
        return self._callmethod('wait', (timeout,))

    def abort(self):
        return self._callmethod('abort')

    def reset(self):
        return self._callmethod('reset')

    @property
    def parties(self):
        return self._callmethod('__getattribute__', ('parties',))

    @property
    def n_waiting(self):
        return self._callmethod('__getattribute__', ('n_waiting',))

    @property
    def broken(self):
        return self._callmethod('__getattribute__', ('broken',))

class NamespaceProxy(BaseProxy):
    _exposed_ = ('__getattribute__', '__setattr__', '__delattr__')

    def __getattr__(self, key):
        if key[0] == '_':
            return object.__getattribute__(self, key)
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('__getattribute__', (key,))

    def __setattr__(self, key, value):
        if key[0] == '_':
            return object.__setattr__(self, key, value)
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('__setattr__', (key, value))

    def __delattr__(self, key):
        if key[0] == '_':
            return object.__delattr__(self, key)
        callmethod = object.__getattribute__(self, '_callmethod')
        return callmethod('__delattr__', (key,))

class ValueProxy(BaseProxy):
    _exposed_ = ('get', 'set')

    def get(self):
        return self._callmethod('get')

    def set(self, value):
        return self._callmethod('set', (value,))
    value = property(get, set)
    __class_getitem__ = classmethod(types.GenericAlias)
BaseListProxy = 造代理类型('BaseListProxy', ('__add__', '__contains__', '__delitem__', '__getitem__', '__imul__', '__len__', '__mul__', '__reversed__', '__rmul__', '__setitem__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort'))

class ListProxy(BaseListProxy):

    def __iadd__(self, value):
        self._callmethod('extend', (value,))
        return self

    def __imul__(self, value):
        self._callmethod('__imul__', (value,))
        return self
    __class_getitem__ = classmethod(types.GenericAlias)
collections.abc.MutableSequence.register(BaseListProxy)
_BaseDictProxy = 造代理类型('_BaseDictProxy', ('__contains__', '__delitem__', '__getitem__', '__ior__', '__iter__', '__len__', '__or__', '__reversed__', '__ror__', '__setitem__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values'))
_BaseDictProxy._method_to_typeid_ = {'__iter__': 'Iterator'}

class DictProxy(_BaseDictProxy):

    def __ior__(self, value):
        self._callmethod('__ior__', (value,))
        return self
    __class_getitem__ = classmethod(types.GenericAlias)
collections.abc.MutableMapping.register(_BaseDictProxy)
_BaseSetProxy = 造代理类型('_BaseSetProxy', ('__and__', '__class_getitem__', '__contains__', '__iand__', '__ior__', '__isub__', '__iter__', '__ixor__', '__len__', '__or__', '__rand__', '__ror__', '__rsub__', '__rxor__', '__sub__', '__xor__', '__ge__', '__gt__', '__le__', '__lt__', 'add', 'clear', 'copy', 'difference', 'difference_update', 'discard', 'intersection', 'intersection_update', 'isdisjoint', 'issubset', 'issuperset', 'pop', 'remove', 'symmetric_difference', 'symmetric_difference_update', 'union', 'update'))

class SetProxy(_BaseSetProxy):

    def __ior__(self, value):
        self._callmethod('__ior__', (value,))
        return self

    def __iand__(self, value):
        self._callmethod('__iand__', (value,))
        return self

    def __ixor__(self, value):
        self._callmethod('__ixor__', (value,))
        return self

    def __isub__(self, value):
        self._callmethod('__isub__', (value,))
        return self
    __class_getitem__ = classmethod(types.GenericAlias)
collections.abc.MutableMapping.register(_BaseSetProxy)
ArrayProxy = 造代理类型('ArrayProxy', ('__len__', '__getitem__', '__setitem__'))
BasePoolProxy = 造代理类型('PoolProxy', ('apply', 'apply_async', 'close', 'imap', 'imap_unordered', 'join', 'map', 'map_async', 'starmap', 'starmap_async', 'terminate'))
BasePoolProxy._method_to_typeid_ = {'apply_async': 'AsyncResult', 'map_async': 'AsyncResult', 'starmap_async': 'AsyncResult', 'imap': 'Iterator', 'imap_unordered': 'Iterator'}

class PoolProxy(BasePoolProxy):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

class 同步管理器(管理器基类):
    """
    Subclass of `BaseManager` which supports a number of shared object types.

    The types registered are those intended for the synchronization
    of threads, plus `dict`, `list` and `Namespace`.

    The `multiprocessing.Manager()` function creates started instances of
    this class.
    """
同步管理器.register('Queue', queue.Queue)
同步管理器.register('JoinableQueue', queue.Queue)
同步管理器.register('Event', threading.Event, EventProxy)
同步管理器.register('Lock', threading.Lock, AcquirerProxy)
同步管理器.register('RLock', threading.RLock, AcquirerProxy)
同步管理器.register('Semaphore', threading.Semaphore, AcquirerProxy)
同步管理器.register('BoundedSemaphore', threading.BoundedSemaphore, AcquirerProxy)
同步管理器.register('Condition', threading.Condition, ConditionProxy)
同步管理器.register('Barrier', threading.Barrier, BarrierProxy)
同步管理器.register('Pool', pool.Pool, PoolProxy)
同步管理器.register('list', list, ListProxy)
同步管理器.register('dict', dict, DictProxy)
同步管理器.register('set', set, SetProxy)
同步管理器.register('Value', 值, ValueProxy)
同步管理器.register('Array', 数组, ArrayProxy)
同步管理器.register('Namespace', Namespace, NamespaceProxy)
同步管理器.register('Iterator', proxytype=IteratorProxy, create_method=False)
同步管理器.register('AsyncResult', create_method=False)
if HAS_SHMEM:

    class _SharedMemoryTracker:
        """Manages one or more shared memory segments."""

        def __init__(self, name, segment_names=None):
            self.shared_memory_context_name = name
            self.segment_names = [] if segment_names is None else segment_names

        def register_segment(self, segment_name):
            """Adds the supplied shared memory block name to tracker."""
            util.debug(f'Register segment {segment_name!r} in pid {getpid()}')
            self.segment_names.append(segment_name)

        def destroy_segment(self, segment_name):
            """Calls unlink() on the shared memory block with the supplied name
            and removes it from the list of blocks being tracked."""
            util.debug(f'Destroy segment {segment_name!r} in pid {getpid()}')
            self.segment_names.remove(segment_name)
            segment = shared_memory.SharedMemory(segment_name)
            segment.close()
            segment.unlink()

        def unlink(self):
            """Calls destroy_segment() on all tracked shared memory blocks."""
            for segment_name in self.segment_names[:]:
                self.destroy_segment(segment_name)

        def __del__(self):
            util.debug(f'Call {self.__class__.__name__}.__del__ in {getpid()}')
            self.unlink()

        def __getstate__(self):
            return (self.shared_memory_context_name, self.segment_names)

        def __setstate__(self, state):
            self.__init__(*state)

    class SharedMemoryServer(服务器):
        public = 服务器.public + ['track_segment', 'release_segment', 'list_segments']

        def __init__(self, *args, **kwargs):
            服务器.__init__(self, *args, **kwargs)
            address = self.address
            if isinstance(address, bytes):
                address = os.fsdecode(address)
            self.shared_memory_context = _SharedMemoryTracker(f'shm_{address}_{getpid()}')
            util.debug(f'SharedMemoryServer started by pid {getpid()}')

        def create(self, c, typeid, /, *args, **kwargs):
            """Create a new distributed-shared object (not backed by a shared
            memory block) and return its id to be used in a Proxy Object."""
            if hasattr(self.registry[typeid][-1], '_shared_memory_proxy'):
                kwargs['shared_memory_context'] = self.shared_memory_context
            return 服务器.create(self, c, typeid, *args, **kwargs)

        def shutdown(self, c):
            """Call unlink() on all tracked shared memory, terminate the Server."""
            self.shared_memory_context.unlink()
            return 服务器.shutdown(self, c)

        def track_segment(self, c, segment_name):
            """Adds the supplied shared memory block name to Server's tracker."""
            self.shared_memory_context.register_segment(segment_name)

        def release_segment(self, c, segment_name):
            """Calls unlink() on the shared memory block with the supplied name
            and removes it from the tracker instance inside the Server."""
            self.shared_memory_context.destroy_segment(segment_name)

        def list_segments(self, c):
            """Returns a list of names of shared memory blocks that the Server
            is currently tracking."""
            return self.shared_memory_context.segment_names

    class SharedMemoryManager(管理器基类):
        """Like SyncManager but uses SharedMemoryServer instead of Server.

        It provides methods for creating and returning SharedMemory instances
        and for creating a list-like object (ShareableList) backed by shared
        memory.  It also provides methods that create and return Proxy Objects
        that support synchronization across processes (i.e. multi-process-safe
        locks and semaphores).
        """
        _Server = SharedMemoryServer

        def __init__(self, *args, **kwargs):
            if os.name == 'posix':
                from . import resource_tracker
                resource_tracker.ensure_running()
            管理器基类.__init__(self, *args, **kwargs)
            util.debug(f'{self.__class__.__name__} created by pid {getpid()}')

        def __del__(self):
            util.debug(f'{self.__class__.__name__}.__del__ by pid {getpid()}')

        def get_server(self):
            """Better than monkeypatching for now; merge into Server ultimately"""
            if self._state.value != 状态.INITIAL:
                if self._state.value == 状态.STARTED:
                    raise ProcessError('Already started SharedMemoryServer')
                elif self._state.value == 状态.SHUTDOWN:
                    raise ProcessError('SharedMemoryManager has shut down')
                else:
                    raise ProcessError('Unknown state {!r}'.format(self._state.value))
            return self._Server(self._registry, self._address, self._authkey, self._serializer)

        def SharedMemory(self, size):
            """Returns a new SharedMemory instance with the specified size in
            bytes, to be tracked by the manager."""
            with self._Client(self._address, authkey=self._authkey) as conn:
                sms = shared_memory.SharedMemory(None, create=True, size=size)
                try:
                    分派(conn, None, 'track_segment', (sms.name,))
                except BaseException as e:
                    sms.unlink()
                    raise e
            return sms

        def ShareableList(self, sequence):
            """Returns a new ShareableList instance populated with the values
            from the input sequence, to be tracked by the manager."""
            with self._Client(self._address, authkey=self._authkey) as conn:
                sl = shared_memory.ShareableList(sequence)
                try:
                    分派(conn, None, 'track_segment', (sl.shm.name,))
                except BaseException as e:
                    sl.shm.unlink()
                    raise e
            return sl


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
    '事件代理': 'EventProxy',
    '代理基类': 'BaseProxy',
    '值代理': 'ValueProxy',
    '列表代理': 'ListProxy',
    '命名空间': 'Namespace',
    '命名空间代理': 'NamespaceProxy',
    '字典代理': 'DictProxy',
    '条件代理': 'ConditionProxy',
    '栅栏代理': 'BarrierProxy',
    '获取器代理': 'AcquirerProxy',
    '进程池代理': 'PoolProxy',
    '迭代器代理': 'IteratorProxy',
    '集合代理': 'SetProxy',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'Array': '数组',
    'AutoProxy': '自动代理',
    'BaseManager': '管理器基类',
    'MakeProxyType': '造代理类型',
    'ProcessLocalSet': '进程局部集合',
    'RebuildProxy': '重建代理',
    'RemoteError': '远端错误',
    'Server': '服务器',
    'State': '状态',
    'SyncManager': '同步管理器',
    'Token': '令牌',
    'Value': '值',
    'all_methods': '全部方法',
    'convert_to_error': '转成错误',
    'dispatch': '分派',
    'public_methods': '公开方法',
    'rebuild_as_list': '重建为列表',
    'reduce_array': '归约数组',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '事件代理',
    '代理基类',
    '令牌',
    '值代理',
    '列表代理',
    '同步管理器',
    '命名空间',
    '命名空间代理',
    '字典代理',
    '条件代理',
    '栅栏代理',
    '管理器基类',
    '获取器代理',
    '进程池代理',
    '迭代器代理',
    '集合代理',
])

# ---- 转发层结束 ----
