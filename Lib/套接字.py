# -*- coding: utf-8 -*-
"""套接字 —— 汉语库（由 tools/汉化库.py 从 Lib/socket.py 机械生成，**不要手改**）。

英文库 Lib/socket.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 套接字
"""


"""This module provides socket operations and some related functions.
On Unix, it supports IP (Internet Protocol) and Unix domain sockets.
On other systems, it only supports IP. Functions specific for a
socket are available as methods of the socket object.

Functions:

socket() -- create a new socket object
socketpair() -- create a pair of new socket objects [*]
fromfd() -- create a socket object from an open file descriptor [*]
send_fds() -- Send file descriptor to the socket.
recv_fds() -- Receive file descriptors from the socket.
fromshare() -- create a socket object from data received from socket.share() [*]
gethostname() -- return the current hostname
gethostbyname() -- map a hostname to its IP number
gethostbyaddr() -- map an IP number or hostname to DNS info
getservbyname() -- map a service name and a protocol name to a port number
getprotobyname() -- map a protocol name (e.g. 'tcp') to a number
ntohs(), ntohl() -- convert 16, 32 bit int from network to host byte order
htons(), htonl() -- convert 16, 32 bit int from host to network byte order
inet_aton() -- convert IP addr string (123.45.67.89) to 32-bit packed format
inet_ntoa() -- convert 32-bit packed format IP to string (123.45.67.89)
socket.getdefaulttimeout() -- get the default timeout value
socket.setdefaulttimeout() -- set the default timeout value
create_connection() -- connects to an address, with an optional timeout and
                       optional source address.
create_server() -- create a TCP socket and bind it to a specified address.

 [*] not available on all platforms!

Special objects:

SocketType -- type object for socket objects
error -- exception raised for I/O errors
has_ipv6 -- boolean value indicating if IPv6 is supported

IntEnum constants:

AF_INET, AF_UNIX -- socket domains (first argument to socket() call)
SOCK_STREAM, SOCK_DGRAM, SOCK_RAW -- socket types (second argument)

Integer constants:

Many other constants may be defined; these may be used in calls to
the setsockopt() and getsockopt() methods.
"""
_英文原名表 = {'SocketIO': '套接字IO', 'create_connection': '建连接', 'create_server': '建服务器', 'fromfd': '从文件描述符', 'getfqdn': '取全限定域名', 'has_dualstack_ipv6': '有双栈IPv6吗'}

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
import _socket
from _socket import *
import io
import os
import sys
from enum import IntEnum, IntFlag
try:
    import errno
except ImportError:
    errno = None
EBADF = getattr(errno, 'EBADF', 9)
EAGAIN = getattr(errno, 'EAGAIN', 11)
EWOULDBLOCK = getattr(errno, 'EWOULDBLOCK', 11)
__all__ = ['fromfd', 'getfqdn', 'create_connection', 'create_server', 'has_dualstack_ipv6', 'AddressFamily', 'SocketKind']
__all__.extend(os._get_exports_list(_socket))
IntEnum._convert_('AddressFamily', __name__, lambda C: C.isupper() and C.startswith('AF_'))
IntEnum._convert_('SocketKind', __name__, lambda C: C.isupper() and C.startswith('SOCK_'))
IntFlag._convert_('MsgFlag', __name__, lambda C: C.isupper() and C.startswith('MSG_'))
IntFlag._convert_('AddressInfo', __name__, lambda C: C.isupper() and C.startswith('AI_'))
_LOCALHOST = '127.0.0.1'
_LOCALHOST_V6 = '::1'

def _intenum_converter(value, enum_klass):
    """Convert a numeric family value to an IntEnum member.

    If it's not a known member, return the numeric value itself.
    """
    try:
        return enum_klass(value)
    except ValueError:
        return value
if sys.platform.lower().startswith('win'):
    errorTab = {6: 'Specified event object handle is invalid.', 8: 'Insufficient memory available.', 87: 'One or more parameters are invalid.', 995: 'Overlapped operation aborted.', 996: 'Overlapped I/O event object not in signaled state.', 997: 'Overlapped operation will complete later.', 10004: 'The operation was interrupted.', 10009: 'A bad file handle was passed.', 10013: 'Permission denied.', 10014: 'A fault occurred on the network??', 10022: 'An invalid operation was attempted.', 10024: 'Too many open files.', 10035: 'The socket operation would block.', 10036: 'A blocking operation is already in progress.', 10037: 'Operation already in progress.', 10038: 'Socket operation on nonsocket.', 10039: 'Destination address required.', 10040: 'Message too long.', 10041: 'Protocol wrong type for socket.', 10042: 'Bad protocol option.', 10043: 'Protocol not supported.', 10044: 'Socket type not supported.', 10045: 'Operation not supported.', 10046: 'Protocol family not supported.', 10047: 'Address family not supported by protocol family.', 10048: 'The network address is in use.', 10049: 'Cannot assign requested address.', 10050: 'Network is down.', 10051: 'Network is unreachable.', 10052: 'Network dropped connection on reset.', 10053: 'Software caused connection abort.', 10054: 'The connection has been reset.', 10055: 'No buffer space available.', 10056: 'Socket is already connected.', 10057: 'Socket is not connected.', 10058: 'The network has been shut down.', 10059: 'Too many references.', 10060: 'The operation timed out.', 10061: 'Connection refused.', 10062: 'Cannot translate name.', 10063: 'The name is too long.', 10064: 'The host is down.', 10065: 'The host is unreachable.', 10066: 'Directory not empty.', 10067: 'Too many processes.', 10068: 'User quota exceeded.', 10069: 'Disk quota exceeded.', 10070: 'Stale file handle reference.', 10071: 'Item is remote.', 10091: 'Network subsystem is unavailable.', 10092: 'Winsock.dll version out of range.', 10093: 'Successful WSAStartup not yet performed.', 10101: 'Graceful shutdown in progress.', 10102: 'No more results from WSALookupServiceNext.', 10103: 'Call has been canceled.', 10104: 'Procedure call table is invalid.', 10105: 'Service provider is invalid.', 10106: 'Service provider failed to initialize.', 10107: 'System call failure.', 10108: 'Service not found.', 10109: 'Class type not found.', 10110: 'No more results from WSALookupServiceNext.', 10111: 'Call was canceled.', 10112: 'Database query was refused.', 11001: 'Host not found.', 11002: 'Nonauthoritative host not found.', 11003: 'This is a nonrecoverable error.', 11004: 'Valid name, no data record requested type.', 11005: 'QoS receivers.', 11006: 'QoS senders.', 11007: 'No QoS senders.', 11008: 'QoS no receivers.', 11009: 'QoS request confirmed.', 11010: 'QoS admission error.', 11011: 'QoS policy failure.', 11012: 'QoS bad style.', 11013: 'QoS bad object.', 11014: 'QoS traffic control error.', 11015: 'QoS generic error.', 11016: 'QoS service type error.', 11017: 'QoS flowspec error.', 11018: 'Invalid QoS provider buffer.', 11019: 'Invalid QoS filter style.', 11020: 'Invalid QoS filter style.', 11021: 'Incorrect QoS filter count.', 11022: 'Invalid QoS object length.', 11023: 'Incorrect QoS flow count.', 11024: 'Unrecognized QoS object.', 11025: 'Invalid QoS policy object.', 11026: 'Invalid QoS flow descriptor.', 11027: 'Invalid QoS provider-specific flowspec.', 11028: 'Invalid QoS provider-specific filterspec.', 11029: 'Invalid QoS shape discard mode object.', 11030: 'Invalid QoS shaping rate object.', 11031: 'Reserved policy QoS element type.'}
    __all__.append('errorTab')

class _GiveupOnSendfile(Exception):
    pass

class socket(_socket.socket):
    """A subclass of _socket.socket adding the makefile() method."""
    __slots__ = ['__weakref__', '_io_refs', '_closed']

    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        if fileno is None:
            if family == -1:
                family = AF_INET
            if type == -1:
                type = SOCK_STREAM
            if proto == -1:
                proto = 0
        _socket.socket.__init__(self, family, type, proto, fileno)
        self._io_refs = 0
        self._closed = False

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if not self._closed:
            self.close()

    def __repr__(self):
        """Wrap __repr__() to reveal the real class name and socket
        address(es).
        """
        closed = getattr(self, '_closed', False)
        s = '<%s.%s%s fd=%i, family=%s, type=%s, proto=%i' % (self.__class__.__module__, self.__class__.__qualname__, ' [closed]' if closed else '', self.fileno(), self.family, self.type, self.proto)
        if not closed:
            try:
                laddr = self.getsockname()
                if laddr:
                    s += ', laddr=%s' % str(laddr)
            except (error, AttributeError):
                pass
            try:
                raddr = self.getpeername()
                if raddr:
                    s += ', raddr=%s' % str(raddr)
            except (error, AttributeError):
                pass
        s += '>'
        return s

    def __getstate__(self):
        raise TypeError(f'cannot pickle {self.__class__.__name__!r} object')

    def dup(self):
        """dup() -> socket object

        Duplicate the socket. Return a new socket object connected to the same
        system resource. The new socket is non-inheritable.
        """
        fd = dup(self.fileno())
        sock = self.__class__(self.family, self.type, self.proto, fileno=fd)
        sock.settimeout(self.gettimeout())
        return sock

    def accept(self):
        """accept() -> (socket object, address info)

        Wait for an incoming connection.  Return a new socket
        representing the connection, and the address of the client.
        For IP sockets, the address info is a pair (hostaddr, port).
        """
        fd, addr = self._accept()
        sock = socket(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return (sock, addr)

    def makefile(self, mode='r', buffering=None, *, encoding=None, errors=None, newline=None):
        """makefile(...) -> an I/O stream connected to the socket

        The arguments are as for io.open() after the filename, except the only
        supported mode values are 'r' (default), 'w', 'b', or a combination of
        those.
        """
        if not set(mode) <= {'r', 'w', 'b'}:
            raise ValueError('invalid mode %r (only r, w, b allowed)' % (mode,))
        writing = 'w' in mode
        reading = 'r' in mode or not writing
        assert reading or writing
        binary = 'b' in mode
        rawmode = ''
        if reading:
            rawmode += 'r'
        if writing:
            rawmode += 'w'
        raw = 套接字IO(self, rawmode)
        self._io_refs += 1
        if buffering is None:
            buffering = -1
        if buffering < 0:
            buffering = io.DEFAULT_BUFFER_SIZE
        if buffering == 0:
            if not binary:
                raise ValueError('unbuffered streams must be binary')
            return raw
        if reading and writing:
            buffer = io.BufferedRWPair(raw, raw, buffering)
        elif reading:
            buffer = io.BufferedReader(raw, buffering)
        else:
            assert writing
            buffer = io.BufferedWriter(raw, buffering)
        if binary:
            return buffer
        encoding = io.text_encoding(encoding)
        text = io.TextIOWrapper(buffer, encoding, errors, newline)
        text.mode = mode
        return text
    if hasattr(os, 'sendfile'):

        def _sendfile_use_sendfile(self, file, offset=0, count=None):
            import selectors
            self._check_sendfile_params(file, offset, count)
            sockno = self.fileno()
            try:
                fileno = file.fileno()
            except (AttributeError, io.UnsupportedOperation) as err:
                raise _GiveupOnSendfile(err)
            try:
                fsize = os.fstat(fileno).st_size
            except OSError as err:
                raise _GiveupOnSendfile(err)
            if not fsize:
                return 0
            blocksize = min(count or fsize, 2 ** 30)
            timeout = self.gettimeout()
            if timeout == 0:
                raise ValueError('non-blocking sockets are not supported')
            if hasattr(selectors, 'PollSelector'):
                selector = selectors.PollSelector()
            else:
                selector = selectors.SelectSelector()
            selector.register(sockno, selectors.EVENT_WRITE)
            total_sent = 0
            selector_select = selector.select
            os_sendfile = os.sendfile
            try:
                while True:
                    if timeout and (not selector_select(timeout)):
                        raise TimeoutError('timed out')
                    if count:
                        blocksize = min(count - total_sent, blocksize)
                        if blocksize <= 0:
                            break
                    try:
                        sent = os_sendfile(sockno, fileno, offset, blocksize)
                    except BlockingIOError:
                        if not timeout:
                            selector_select()
                        continue
                    except OSError as err:
                        if total_sent == 0:
                            raise _GiveupOnSendfile(err)
                        raise err from None
                    else:
                        if sent == 0:
                            break
                        offset += sent
                        total_sent += sent
                return total_sent
            finally:
                if total_sent > 0 and hasattr(file, 'seek'):
                    file.seek(offset)
    else:

        def _sendfile_use_sendfile(self, file, offset=0, count=None):
            raise _GiveupOnSendfile('os.sendfile() not available on this platform')

    def _sendfile_use_send(self, file, offset=0, count=None):
        self._check_sendfile_params(file, offset, count)
        if self.gettimeout() == 0:
            raise ValueError('non-blocking sockets are not supported')
        if offset:
            file.seek(offset)
        blocksize = min(count, 8192) if count else 8192
        total_sent = 0
        file_read = file.read
        sock_send = self.send
        try:
            while True:
                if count:
                    blocksize = min(count - total_sent, blocksize)
                    if blocksize <= 0:
                        break
                data = memoryview(file_read(blocksize))
                if not data:
                    break
                while True:
                    try:
                        sent = sock_send(data)
                    except BlockingIOError:
                        continue
                    else:
                        total_sent += sent
                        if sent < len(data):
                            data = data[sent:]
                        else:
                            break
            return total_sent
        finally:
            if total_sent > 0 and hasattr(file, 'seek'):
                file.seek(offset + total_sent)

    def _check_sendfile_params(self, file, offset, count):
        if 'b' not in getattr(file, 'mode', 'b'):
            raise ValueError('file should be opened in binary mode')
        if not self.type & SOCK_STREAM:
            raise ValueError('only SOCK_STREAM type sockets are supported')
        if count is not None:
            if not isinstance(count, int):
                raise TypeError('count must be a positive integer (got {!r})'.format(count))
            if count <= 0:
                raise ValueError('count must be a positive integer (got {!r})'.format(count))

    def sendfile(self, file, offset=0, count=None):
        """sendfile(file[, offset[, count]]) -> sent

        Send a file until EOF is reached by using high-performance
        os.sendfile() and return the total number of bytes which
        were sent.
        *file* must be a regular file object opened in binary mode.
        If os.sendfile() is not available (e.g. Windows) or file is
        not a regular file socket.send() will be used instead.
        *offset* tells from where to start reading the file.
        If specified, *count* is the total number of bytes to transmit
        as opposed to sending the file until EOF is reached.
        File position is updated on return or also in case of error in
        which case file.tell() can be used to figure out the number of
        bytes which were sent.
        The socket must be of SOCK_STREAM type.
        Non-blocking sockets are not supported.
        """
        try:
            return self._sendfile_use_sendfile(file, offset, count)
        except _GiveupOnSendfile:
            return self._sendfile_use_send(file, offset, count)

    def _decref_socketios(self):
        if self._io_refs > 0:
            self._io_refs -= 1
        if self._closed:
            self.close()

    def _real_close(self, _ss=_socket.socket):
        _ss.close(self)

    def close(self):
        self._closed = True
        if self._io_refs <= 0:
            self._real_close()

    def detach(self):
        """detach() -> file descriptor

        Close the socket object without closing the underlying file descriptor.
        The object cannot be used after this call, but the file descriptor
        can be reused for other purposes.  The file descriptor is returned.
        """
        self._closed = True
        return super().detach()

    @property
    def family(self):
        """Read-only access to the address family for this socket.
        """
        return _intenum_converter(super().family, AddressFamily)

    @property
    def type(self):
        """Read-only access to the socket type.
        """
        return _intenum_converter(super().type, SocketKind)
    if os.name == 'nt':

        def get_inheritable(self):
            return os.get_handle_inheritable(self.fileno())

        def set_inheritable(self, inheritable):
            os.set_handle_inheritable(self.fileno(), inheritable)
    else:

        def get_inheritable(self):
            return os.get_inheritable(self.fileno())

        def set_inheritable(self, inheritable):
            os.set_inheritable(self.fileno(), inheritable)
    get_inheritable.__doc__ = 'Get the inheritable flag of the socket'
    set_inheritable.__doc__ = 'Set the inheritable flag of the socket'
_装类转发(socket, {'close': '关闭', 'dup': '复制'}, {'close': '关闭', 'dup': '复制'})

def 从文件描述符(fd, family, type, proto=0):
    """ fromfd(fd, family, type[, proto]) -> socket object

    Create a socket object from a duplicate of the given file
    descriptor.  The remaining arguments are the same as for socket().
    """
    nfd = dup(fd)
    return socket(family, type, proto, nfd)
if hasattr(_socket.socket, 'sendmsg'):

    def send_fds(sock, buffers, fds, flags=0, address=None):
        """ send_fds(sock, buffers, fds[, flags[, address]]) -> integer

        Send the list of file descriptors fds over an AF_UNIX socket.
        """
        import array
        return sock.sendmsg(buffers, [(_socket.SOL_SOCKET, _socket.SCM_RIGHTS, array.array('i', fds))])
    __all__.append('send_fds')
if hasattr(_socket.socket, 'recvmsg'):

    def recv_fds(sock, bufsize, maxfds, flags=0):
        """ recv_fds(sock, bufsize, maxfds[, flags]) -> (data, list of file
        descriptors, msg_flags, address)

        Receive up to maxfds file descriptors returning the message
        data and a list containing the descriptors.
        """
        import array
        fds = array.array('i')
        msg, ancdata, flags, addr = sock.recvmsg(bufsize, _socket.CMSG_LEN(maxfds * fds.itemsize))
        for cmsg_level, cmsg_type, cmsg_data in ancdata:
            if cmsg_level == _socket.SOL_SOCKET and cmsg_type == _socket.SCM_RIGHTS:
                fds.frombytes(cmsg_data[:len(cmsg_data) - len(cmsg_data) % fds.itemsize])
        return (msg, list(fds), flags, addr)
    __all__.append('recv_fds')
if hasattr(_socket.socket, 'share'):

    def fromshare(info):
        """ fromshare(info) -> socket object

        Create a socket object from the bytes object returned by
        socket.share(pid).
        """
        return socket(0, 0, 0, info)
    __all__.append('fromshare')

def _fallback_socketpair(family=AF_INET, type=SOCK_STREAM, proto=0):
    if family == AF_INET:
        host = _LOCALHOST
    elif family == AF_INET6:
        host = _LOCALHOST_V6
    else:
        raise ValueError('Only AF_INET and AF_INET6 socket address families are supported')
    if type != SOCK_STREAM:
        raise ValueError('Only SOCK_STREAM socket type is supported')
    if proto != 0:
        raise ValueError('Only protocol zero is supported')
    lsock = socket(family, type, proto)
    try:
        lsock.bind((host, 0))
        lsock.listen()
        addr, port = lsock.getsockname()[:2]
        csock = socket(family, type, proto)
        try:
            csock.setblocking(False)
            try:
                csock.connect((addr, port))
            except (BlockingIOError, InterruptedError):
                pass
            csock.setblocking(True)
            ssock, _ = lsock.accept()
        except:
            csock.close()
            raise
    finally:
        lsock.close()
    if sys.platform != 'wasi':
        try:
            if ssock.getsockname() != csock.getpeername() or csock.getsockname() != ssock.getpeername():
                raise ConnectionError('Unexpected peer connection')
        except:
            ssock.close()
            csock.close()
            raise
    return (ssock, csock)
if hasattr(_socket, 'socketpair'):

    def socketpair(family=None, type=SOCK_STREAM, proto=0):
        if family is None:
            try:
                family = AF_UNIX
            except NameError:
                family = AF_INET
        a, b = _socket.socketpair(family, type, proto)
        a = socket(family, type, proto, a.detach())
        b = socket(family, type, proto, b.detach())
        return (a, b)
else:
    socketpair = _fallback_socketpair
    __all__.append('socketpair')
socketpair.__doc__ = 'socketpair([family[, type[, proto]]]) -> (socket object, socket object)\nCreate a pair of socket objects from the sockets returned by the platform\nsocketpair() function.\nThe arguments are the same as for socket() except the default family is AF_UNIX\nif defined on the platform; otherwise, the default is AF_INET.\n'
_blocking_errnos = {EAGAIN, EWOULDBLOCK}

class 套接字IO(io.RawIOBase):
    """Raw I/O implementation for stream sockets.

    This class supports the makefile() method on sockets.  It provides
    the raw I/O interface on top of a socket object.
    """

    def __init__(self, sock, mode):
        if mode not in ('r', 'w', 'rw', 'rb', 'wb', 'rwb'):
            raise ValueError('invalid mode: %r' % mode)
        io.RawIOBase.__init__(self)
        self._sock = sock
        if 'b' not in mode:
            mode += 'b'
        self._mode = mode
        self._reading = 'r' in mode
        self._writing = 'w' in mode
        self._timeout_occurred = False

    def readinto(self, b):
        """Read up to len(b) bytes into the writable buffer *b* and return
        the number of bytes read.  If the socket is non-blocking and no bytes
        are available, None is returned.

        If *b* is non-empty, a 0 return value indicates that the connection
        was shutdown at the other end.
        """
        self._checkClosed()
        self._checkReadable()
        if self._timeout_occurred:
            raise OSError('cannot read from timed out object')
        try:
            return self._sock.recv_into(b)
        except timeout:
            self._timeout_occurred = True
            raise
        except error as e:
            if e.errno in _blocking_errnos:
                return None
            raise

    def write(self, b):
        """Write the given bytes or bytearray object *b* to the socket
        and return the number of bytes written.  This can be less than
        len(b) if not all data could be written.  If the socket is
        non-blocking and no bytes could be written None is returned.
        """
        self._checkClosed()
        self._checkWritable()
        try:
            return self._sock.send(b)
        except error as e:
            if e.errno in _blocking_errnos:
                return None
            raise

    def readable(self):
        """True if the SocketIO is open for reading.
        """
        if self.closed:
            raise ValueError('I/O operation on closed socket.')
        return self._reading

    def writable(self):
        """True if the SocketIO is open for writing.
        """
        if self.closed:
            raise ValueError('I/O operation on closed socket.')
        return self._writing

    def seekable(self):
        """True if the SocketIO is open for seeking.
        """
        if self.closed:
            raise ValueError('I/O operation on closed socket.')
        return super().seekable()

    def fileno(self):
        """Return the file descriptor of the underlying socket.
        """
        self._checkClosed()
        return self._sock.fileno()

    @property
    def name(self):
        if not self.closed:
            return self.fileno()
        else:
            return -1

    @property
    def mode(self):
        return self._mode

    def close(self):
        """Close the SocketIO object.  This doesn't close the underlying
        socket, except if all references to it have disappeared.
        """
        if self.closed:
            return
        io.RawIOBase.close(self)
        self._sock._decref_socketios()
        self._sock = None
_装类转发(套接字IO, {'close': '关闭'}, {'close': '关闭'})

def 取全限定域名(name=''):
    """Get fully qualified domain name from name.

    An empty argument is interpreted as meaning the local host.

    First the hostname returned by gethostbyaddr() is checked, then
    possibly existing aliases. In case no FQDN is available and `name`
    was given, it is returned unchanged. If `name` was empty, '0.0.0.0' or '::',
    hostname from gethostname() is returned.
    """
    name = name.strip()
    if not name or name in ('0.0.0.0', '::'):
        name = gethostname()
    try:
        hostname, aliases, ipaddrs = gethostbyaddr(name)
    except error:
        pass
    else:
        aliases.insert(0, hostname)
        for name in aliases:
            if '.' in name:
                break
        else:
            name = hostname
    return name
_GLOBAL_DEFAULT_TIMEOUT = object()

def 建连接(address, timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None, *, all_errors=False):
    """Connect to *address* and return the socket object.

    Convenience function.  Connect to *address* (a 2-tuple ``(host,
    port)``) and return the socket object.  Passing the optional
    *timeout* parameter will set the timeout on the socket instance
    before attempting to connect.  If no *timeout* is supplied, the
    global default timeout setting returned by :func:`getdefaulttimeout`
    is used.  If *source_address* is set it must be a tuple of (host, port)
    for the socket to bind as a source address before making the connection.
    A host of '' or port 0 tells the OS to use the default. When a connection
    cannot be created, raises the last error if *all_errors* is False,
    and an ExceptionGroup of all errors if *all_errors* is True.
    """
    host, port = address
    exceptions = []
    for res in getaddrinfo(host, port, 0, SOCK_STREAM):
        af, socktype, proto, canonname, sa = res
        sock = None
        try:
            sock = socket(af, socktype, proto)
            if timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                sock.settimeout(timeout)
            if source_address:
                sock.bind(source_address)
            sock.connect(sa)
            exceptions.clear()
            return sock
        except error as exc:
            if not all_errors:
                exceptions.clear()
            exceptions.append(exc)
            if sock is not None:
                sock.close()
    if len(exceptions):
        try:
            if not all_errors:
                raise exceptions[0]
            raise ExceptionGroup('create_connection failed', exceptions)
        finally:
            exceptions.clear()
    else:
        raise error('getaddrinfo returns an empty list')

def 有双栈IPv6吗():
    """Return True if the platform supports creating a SOCK_STREAM socket
    which can handle both AF_INET and AF_INET6 (IPv4 / IPv6) connections.
    """
    if not has_ipv6 or not hasattr(_socket, 'IPPROTO_IPV6') or (not hasattr(_socket, 'IPV6_V6ONLY')):
        return False
    try:
        with socket(AF_INET6, SOCK_STREAM) as sock:
            sock.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 0)
            return sock.getsockopt(IPPROTO_IPV6, IPV6_V6ONLY) == 0
    except error:
        return False

def 建服务器(address, *, family=AF_INET, backlog=None, reuse_port=False, dualstack_ipv6=False):
    """Convenience function which creates a SOCK_STREAM type socket
    bound to *address* (a 2-tuple (host, port)) and return the socket
    object.

    *family* should be either AF_INET or AF_INET6.
    *backlog* is the queue size passed to socket.listen().
    *reuse_port* dictates whether to use the SO_REUSEPORT socket option.
    *dualstack_ipv6*: if true and the platform supports it, it will
    create an AF_INET6 socket able to accept both IPv4 or IPv6
    connections. When false it will explicitly disable this option on
    platforms that enable it by default (e.g. Linux).

    >>> with create_server(('', 8000)) as server:
    ...     while True:
    ...         conn, addr = server.accept()
    ...         # handle new connection
    """
    if reuse_port and (not hasattr(_socket, 'SO_REUSEPORT')):
        raise ValueError('SO_REUSEPORT not supported on this platform')
    if dualstack_ipv6:
        if not 有双栈IPv6吗():
            raise ValueError('dualstack_ipv6 not supported on this platform')
        if family != AF_INET6:
            raise ValueError('dualstack_ipv6 requires AF_INET6 family')
    sock = socket(family, SOCK_STREAM)
    try:
        if os.name not in ('nt', 'cygwin') and hasattr(_socket, 'SO_REUSEADDR'):
            try:
                sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            except error:
                pass
        if reuse_port and family in (AF_INET, AF_INET6):
            sock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
        if has_ipv6 and family == AF_INET6:
            if dualstack_ipv6:
                sock.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 0)
            elif hasattr(_socket, 'IPV6_V6ONLY') and hasattr(_socket, 'IPPROTO_IPV6'):
                sock.setsockopt(IPPROTO_IPV6, IPV6_V6ONLY, 1)
        try:
            sock.bind(address)
        except error as err:
            msg = '%s (while attempting to bind on address %r)' % (err.strerror, address)
            raise error(err.errno, msg) from None
        if backlog is None:
            sock.listen()
        else:
            sock.listen(backlog)
        return sock
    except error:
        sock.close()
        raise

def getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    """Resolve host and port into list of address info entries.

    Translate the host/port argument into a sequence of 5-tuples that contain
    all the necessary arguments for creating a socket connected to that service.
    host is a domain name, a string representation of an IPv4/v6 address or
    None. port is a string service name such as 'http', a numeric port number or
    None. By passing None as the value of host and port, you can pass NULL to
    the underlying C API.

    The family, type and proto arguments can be optionally specified in order to
    narrow the list of addresses returned. Passing zero as a value for each of
    these arguments selects the full range of results.
    """
    addrlist = []
    for res in _socket.getaddrinfo(host, port, family, type, proto, flags):
        af, socktype, proto, canonname, sa = res
        addrlist.append((_intenum_converter(af, AddressFamily), _intenum_converter(socktype, SocketKind), proto, canonname, sa))
    return addrlist


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
    '取地址信息': 'getaddrinfo',
    '套接字': 'socket',
    '套接字对': 'socketpair',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})

# 身份别名层：这些名字跟英文库是**同一个对象**（类型身份参与语义，只能别名）
import socket as _英文库
地址族_APPLETALK = _英文库.AF_APPLETALK
蓝牙地址族 = _英文库.AF_BLUETOOTH
地址族_DECnet = _英文库.AF_DECnet
地址族_HYPERV = _英文库.AF_HYPERV
互联网地址族 = _英文库.AF_INET
互联网v6地址族 = _英文库.AF_INET6
地址族_IPX = _英文库.AF_IPX
红外地址族 = _英文库.AF_IRDA
链路地址族 = _英文库.AF_LINK
地址族_SNA = _英文库.AF_SNA
未指定地址族 = _英文库.AF_UNSPEC
按地址配置 = _英文库.AI_ADDRCONFIG
全部地址 = _英文库.AI_ALL
取规范名 = _英文库.AI_CANONNAME
数字主机 = _英文库.AI_NUMERICHOST
数字服务 = _英文库.AI_NUMERICSERV
被动模式 = _英文库.AI_PASSIVE
v4映射 = _英文库.AI_V4MAPPED
地址族 = _英文库.AddressFamily
地址信息 = _英文库.AddressInfo
再次尝试 = _英文库.EAGAIN
稍后重试 = _英文库.EAI_AGAIN
标志无效 = _英文库.EAI_BADFLAGS
名字服务失败 = _英文库.EAI_FAIL
地址族不支持 = _英文库.EAI_FAMILY
内存不足 = _英文库.EAI_MEMORY
无数据 = _英文库.EAI_NODATA
名字无效 = _英文库.EAI_NONAME
服务无效 = _英文库.EAI_SERVICE
套接字类型不支持 = _英文库.EAI_SOCKTYPE
坏描述符 = _英文库.EBADF
会阻塞 = _英文库.EWOULDBLOCK
全主机组 = _英文库.INADDR_ALLHOSTS_GROUP
任意地址 = _英文库.INADDR_ANY
广播地址 = _英文库.INADDR_BROADCAST
回环地址 = _英文库.INADDR_LOOPBACK
最大本地组 = _英文库.INADDR_MAX_LOCAL_GROUP
无效地址 = _英文库.INADDR_NONE
未指定地址组 = _英文库.INADDR_UNSPEC_GROUP
保留端口 = _英文库.IPPORT_RESERVED
用户保留端口 = _英文库.IPPORT_USERRESERVED
协议_AH = _英文库.IPPROTO_AH
协议_CBT = _英文库.IPPROTO_CBT
协议_目的选项 = _英文库.IPPROTO_DSTOPTS
协议_EGP = _英文库.IPPROTO_EGP
协议_ESP = _英文库.IPPROTO_ESP
协议_分片 = _英文库.IPPROTO_FRAGMENT
协议_GGP = _英文库.IPPROTO_GGP
协议_逐跳选项 = _英文库.IPPROTO_HOPOPTS
协议_ICLFXBM = _英文库.IPPROTO_ICLFXBM
协议_ICMP = _英文库.IPPROTO_ICMP
协议_ICMPv6 = _英文库.IPPROTO_ICMPV6
协议_IDP = _英文库.IPPROTO_IDP
协议_IGMP = _英文库.IPPROTO_IGMP
协议_IGP = _英文库.IPPROTO_IGP
协议_IP = _英文库.IPPROTO_IP
协议_IPv4 = _英文库.IPPROTO_IPV4
协议_IPv6 = _英文库.IPPROTO_IPV6
协议_L2TP = _英文库.IPPROTO_L2TP
协议_MAX = _英文库.IPPROTO_MAX
协议_ND = _英文库.IPPROTO_ND
协议_无 = _英文库.IPPROTO_NONE
协议_PGM = _英文库.IPPROTO_PGM
协议_PIM = _英文库.IPPROTO_PIM
协议_PUP = _英文库.IPPROTO_PUP
协议_RAW = _英文库.IPPROTO_RAW
协议_RDP = _英文库.IPPROTO_RDP
协议_路由 = _英文库.IPPROTO_ROUTING
协议_SCTP = _英文库.IPPROTO_SCTP
协议_ST = _英文库.IPPROTO_ST
协议_TCP = _英文库.IPPROTO_TCP
协议_UDP = _英文库.IPPROTO_UDP
IPv6选项_CHECKSUM = _英文库.IPV6_CHECKSUM
IPv6选项_DONTFRAG = _英文库.IPV6_DONTFRAG
IPv6选项_HOPLIMIT = _英文库.IPV6_HOPLIMIT
IPv6选项_HOPOPTS = _英文库.IPV6_HOPOPTS
IPv6选项_JOIN_GROUP = _英文库.IPV6_JOIN_GROUP
IPv6选项_LEAVE_GROUP = _英文库.IPV6_LEAVE_GROUP
IPv6选项_MULTICAST_HOPS = _英文库.IPV6_MULTICAST_HOPS
IPv6选项_MULTICAST_IF = _英文库.IPV6_MULTICAST_IF
IPv6选项_MULTICAST_LOOP = _英文库.IPV6_MULTICAST_LOOP
IPv6选项_PKTINFO = _英文库.IPV6_PKTINFO
IPv6选项_RECVERR = _英文库.IPV6_RECVERR
IPv6选项_RECVRTHDR = _英文库.IPV6_RECVRTHDR
IPv6选项_RECVTCLASS = _英文库.IPV6_RECVTCLASS
IPv6选项_RTHDR = _英文库.IPV6_RTHDR
IPv6选项_TCLASS = _英文库.IPV6_TCLASS
IPv6选项_UNICAST_HOPS = _英文库.IPV6_UNICAST_HOPS
IPv6选项_V6ONLY = _英文库.IPV6_V6ONLY
IP选项_ADD_MEMBERSHIP = _英文库.IP_ADD_MEMBERSHIP
IP选项_ADD_SOURCE_MEMBERSHIP = _英文库.IP_ADD_SOURCE_MEMBERSHIP
IP选项_BLOCK_SOURCE = _英文库.IP_BLOCK_SOURCE
IP选项_DROP_MEMBERSHIP = _英文库.IP_DROP_MEMBERSHIP
IP选项_DROP_SOURCE_MEMBERSHIP = _英文库.IP_DROP_SOURCE_MEMBERSHIP
IP选项_HDRINCL = _英文库.IP_HDRINCL
IP选项_MULTICAST_IF = _英文库.IP_MULTICAST_IF
IP选项_MULTICAST_LOOP = _英文库.IP_MULTICAST_LOOP
IP选项_MULTICAST_TTL = _英文库.IP_MULTICAST_TTL
IP选项_OPTIONS = _英文库.IP_OPTIONS
IP选项_PKTINFO = _英文库.IP_PKTINFO
IP选项_RECVDSTADDR = _英文库.IP_RECVDSTADDR
IP选项_RECVERR = _英文库.IP_RECVERR
IP选项_RECVTOS = _英文库.IP_RECVTOS
IP选项_RECVTTL = _英文库.IP_RECVTTL
IP选项_TOS = _英文库.IP_TOS
IP选项_TTL = _英文库.IP_TTL
IP选项_UNBLOCK_SOURCE = _英文库.IP_UNBLOCK_SOURCE
广播消息 = _英文库.MSG_BCAST
控制截断 = _英文库.MSG_CTRUNC
不走路由 = _英文库.MSG_DONTROUTE
错误队列 = _英文库.MSG_ERRQUEUE
多播消息 = _英文库.MSG_MCAST
带外 = _英文库.MSG_OOB
窥探 = _英文库.MSG_PEEK
截断 = _英文库.MSG_TRUNC
等到满 = _英文库.MSG_WAITALL
消息标志 = _英文库.MsgFlag
数据报服务 = _英文库.NI_DGRAM
最大主机名长 = _英文库.NI_MAXHOST
最大服务名长 = _英文库.NI_MAXSERV
名字必需 = _英文库.NI_NAMEREQD
不取全限定 = _英文库.NI_NOFQDN
数字主机名 = _英文库.NI_NUMERICHOST
数字服务名 = _英文库.NI_NUMERICSERV
关闭读 = _英文库.SHUT_RD
关闭读写 = _英文库.SHUT_RDWR
关闭写 = _英文库.SHUT_WR
数据报套接字 = _英文库.SOCK_DGRAM
原始套接字 = _英文库.SOCK_RAW
可靠数据报套接字 = _英文库.SOCK_RDM
顺序包套接字 = _英文库.SOCK_SEQPACKET
流式套接字 = _英文库.SOCK_STREAM
层_IP = _英文库.SOL_IP
层_RFCOMM = _英文库.SOL_RFCOMM
套接字层 = _英文库.SOL_SOCKET
层_TCP = _英文库.SOL_TCP
层_UDP = _英文库.SOL_UDP
最大连接数 = _英文库.SOMAXCONN
已监听 = _英文库.SO_ACCEPTCONN
允许广播 = _英文库.SO_BROADCAST
蓝牙加密 = _英文库.SO_BTH_ENCRYPT
蓝牙MTU = _英文库.SO_BTH_MTU
蓝牙MTU最大 = _英文库.SO_BTH_MTU_MAX
蓝牙MTU最小 = _英文库.SO_BTH_MTU_MIN
调试 = _英文库.SO_DEBUG
不走路由 = _英文库.SO_DONTROUTE
取错误 = _英文库.SO_ERROR
独占地址 = _英文库.SO_EXCLUSIVEADDRUSE
保持连接 = _英文库.SO_KEEPALIVE
延迟关闭 = _英文库.SO_LINGER
带外内联 = _英文库.SO_OOBINLINE
原始目的地址 = _英文库.SO_ORIGINAL_DST
接收缓冲 = _英文库.SO_RCVBUF
接收低水位 = _英文库.SO_RCVLOWAT
接收超时 = _英文库.SO_RCVTIMEO
地址可重用 = _英文库.SO_REUSEADDR
发送缓冲 = _英文库.SO_SNDBUF
发送低水位 = _英文库.SO_SNDLOWAT
发送超时 = _英文库.SO_SNDTIMEO
取类型 = _英文库.SO_TYPE
环回可用 = _英文库.SO_USELOOPBACK
套接字类型 = _英文库.SocketKind
快速打开 = _英文库.TCP_FASTOPEN
保活次数 = _英文库.TCP_KEEPCNT
保活空闲 = _英文库.TCP_KEEPIDLE
保活间隔 = _英文库.TCP_KEEPINTVL
最大段长 = _英文库.TCP_MAXSEG
不延迟 = _英文库.TCP_NODELAY
快速确认 = _英文库.TCP_QUICKACK
关闭 = _英文库.close
复制 = _英文库.dup
套接字错误 = _英文库.error
地址信息错误 = _英文库.gaierror
取默认超时 = _英文库.getdefaulttimeout
按地址取主机 = _英文库.gethostbyaddr
按名取主机 = _英文库.gethostbyname
按名取主机扩展 = _英文库.gethostbyname_ex
取主机名 = _英文库.gethostname
取名字信息 = _英文库.getnameinfo
按名取协议 = _英文库.getprotobyname
按名取服务 = _英文库.getservbyname
按端口取服务 = _英文库.getservbyport
有IPv6吗 = _英文库.has_ipv6
主机名错误 = _英文库.herror
主机转网络长 = _英文库.htonl
主机转网络短 = _英文库.htons
索引转接口名 = _英文库.if_indextoname
接口名索引 = _英文库.if_nameindex
接口名转索引 = _英文库.if_nametoindex
点分转网络序 = _英文库.inet_aton
网络序转点分 = _英文库.inet_ntoa
打包转点分 = _英文库.inet_ntop
点分转打包 = _英文库.inet_pton
网络转主机长 = _英文库.ntohl
网络转主机短 = _英文库.ntohs
设默认超时 = _英文库.setdefaulttimeout
超时 = _英文库.timeout
_模块别名 = {
    'SocketIO': '套接字IO',
    'create_connection': '建连接',
    'create_server': '建服务器',
    'fromfd': '从文件描述符',
    'getfqdn': '取全限定域名',
    'has_dualstack_ipv6': '有双栈IPv6吗',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'socket': {
        'close': '关闭',
        'dup': '复制',
    },
    '套接字IO': {
        'close': '关闭',
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
    'socket': {
        'close': '关闭',
        'dup': '复制',
    },
    '套接字IO': {
        'close': '关闭',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '从文件描述符',
    '取全限定域名',
    '取地址信息',
    '套接字',
    '套接字对',
    '建服务器',
    '建连接',
    '有双栈IPv6吗',
])

# ---- 转发层结束 ----
