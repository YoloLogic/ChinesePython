# -*- coding: utf-8 -*-
"""多进程.connection —— 汉语库（由 tools/汉化库.py 从 Lib/multiprocessing/connection.py 机械生成，**不要手改**）。

英文库 Lib/multiprocessing.connection.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py multiprocessing
"""


_英文原名表 = {'Client': '客户端', 'Connection': '连接', 'ConnectionWrapper': '连接包装', 'Listener': '监听器', 'SocketClient': '套接字客户端', 'SocketListener': '套接字监听器', 'XmlClient': 'XML客户端', 'XmlListener': 'XML监听器', 'address_type': '地址类型', 'answer_challenge': '应答挑战', 'arbitrary_address': '任意地址', 'deliver_challenge': '发送挑战'}

def __getattr__(名字):
    中 = _英文原名表.get(名字)
    if 中 is not None and 中 in globals():
        return globals()[中]
    raise AttributeError(名字)
__all__ = ['Client', 'Listener', 'Pipe', 'wait']
import errno
import io
import itertools
import os
import sys
import socket
import struct
import time
from . import util
from . import AuthenticationError, BufferTooShort
from .context import reduction
_ForkingPickler = reduction.ForkingPickler
try:
    import _multiprocessing
    import _winapi
    from _winapi import WAIT_OBJECT_0, WAIT_ABANDONED_0, WAIT_TIMEOUT, INFINITE
except ImportError:
    if sys.platform == 'win32':
        raise
    _winapi = None
BUFSIZE = 64 * 1024
CONNECTION_TIMEOUT = 20.0
_mmap_counter = itertools.count()
_MAX_PIPE_ATTEMPTS = 100
default_family = 'AF_INET'
families = ['AF_INET']
if hasattr(socket, 'AF_UNIX'):
    default_family = 'AF_UNIX'
    families += ['AF_UNIX']
if sys.platform == 'win32':
    default_family = 'AF_PIPE'
    families += ['AF_PIPE']

def _init_timeout(timeout=CONNECTION_TIMEOUT):
    return time.monotonic() + timeout

def _check_timeout(t):
    return time.monotonic() > t

def 任意地址(family):
    """
    Return an arbitrary free address for the given family
    """
    if family == 'AF_INET':
        return ('localhost', 0)
    elif family == 'AF_UNIX':
        return os.path.join(util.get_temp_dir(), f'sock-{os.urandom(6).hex()}')
    elif family == 'AF_PIPE':
        return '\\\\.\\pipe\\pyc-%d-%d-%s' % (os.getpid(), next(_mmap_counter), os.urandom(8).hex())
    else:
        raise ValueError('unrecognized family')

def _validate_family(family):
    """
    Checks if the family is valid for the current environment.
    """
    if sys.platform != 'win32' and family == 'AF_PIPE':
        raise ValueError('Family %s is not recognized.' % family)
    if sys.platform == 'win32' and family == 'AF_UNIX':
        if not hasattr(socket, family):
            raise ValueError('Family %s is not recognized.' % family)

def 地址类型(address):
    """
    Return the types of the address

    This can be 'AF_INET', 'AF_UNIX', or 'AF_PIPE'
    """
    if type(address) == tuple:
        return 'AF_INET'
    elif type(address) is str and address.startswith('\\\\'):
        return 'AF_PIPE'
    elif type(address) is str or util.is_abstract_socket_namespace(address):
        return 'AF_UNIX'
    else:
        raise ValueError('address type of %r unrecognized' % address)

class _ConnectionBase:
    _handle = None

    def __init__(self, handle, readable=True, writable=True):
        handle = handle.__index__()
        if handle < 0:
            raise ValueError('invalid handle')
        if not readable and (not writable):
            raise ValueError('at least one of `readable` and `writable` must be True')
        self._handle = handle
        self._readable = readable
        self._writable = writable

    def __del__(self):
        if self._handle is not None:
            self._close()

    def _check_closed(self):
        if self._handle is None:
            raise OSError('handle is closed')

    def _check_readable(self):
        if not self._readable:
            raise OSError('connection is write-only')

    def _check_writable(self):
        if not self._writable:
            raise OSError('connection is read-only')

    def _bad_message_length(self):
        if self._writable:
            self._readable = False
        else:
            self.close()
        raise OSError('bad message length')

    @property
    def closed(self):
        """True if the connection is closed"""
        return self._handle is None

    @property
    def readable(self):
        """True if the connection is readable"""
        return self._readable

    @property
    def writable(self):
        """True if the connection is writable"""
        return self._writable

    def fileno(self):
        """File descriptor or handle of the connection"""
        self._check_closed()
        return self._handle

    def close(self):
        """Close the connection"""
        if self._handle is not None:
            try:
                self._close()
            finally:
                self._handle = None

    def _detach(self):
        """Stop managing the underlying file descriptor or handle."""
        self._handle = None

    def send_bytes(self, buf, offset=0, size=None):
        """Send the bytes data from a bytes-like object"""
        self._check_closed()
        self._check_writable()
        m = memoryview(buf)
        if m.itemsize > 1:
            m = m.cast('B')
        n = m.nbytes
        if offset < 0:
            raise ValueError('offset is negative')
        if n < offset:
            raise ValueError('buffer length < offset')
        if size is None:
            size = n - offset
        elif size < 0:
            raise ValueError('size is negative')
        elif offset + size > n:
            raise ValueError('buffer length < offset + size')
        self._send_bytes(m[offset:offset + size])

    def send(self, obj):
        """Send a (picklable) object"""
        self._check_closed()
        self._check_writable()
        self._send_bytes(_ForkingPickler.dumps(obj))

    def recv_bytes(self, maxlength=None):
        """
        Receive bytes data as a bytes object.
        """
        self._check_closed()
        self._check_readable()
        if maxlength is not None and maxlength < 0:
            raise ValueError('negative maxlength')
        buf = self._recv_bytes(maxlength)
        if buf is None:
            self._bad_message_length()
        return buf.getvalue()

    def recv_bytes_into(self, buf, offset=0):
        """
        Receive bytes data into a writeable bytes-like object.
        Return the number of bytes read.
        """
        self._check_closed()
        self._check_readable()
        with memoryview(buf) as m:
            itemsize = m.itemsize
            bytesize = itemsize * len(m)
            if offset < 0:
                raise ValueError('negative offset')
            elif offset > bytesize:
                raise ValueError('offset too large')
            result = self._recv_bytes()
            size = result.tell()
            if bytesize < offset + size:
                raise BufferTooShort(result.getvalue())
            result.seek(0)
            result.readinto(m[offset // itemsize:(offset + size) // itemsize])
            return size

    def recv(self):
        """Receive a (picklable) object"""
        self._check_closed()
        self._check_readable()
        buf = self._recv_bytes()
        return _ForkingPickler.loads(buf.getbuffer())

    def poll(self, timeout=0.0):
        """Whether there is any input available to be read"""
        self._check_closed()
        self._check_readable()
        return self._poll(timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()
if _winapi:

    class PipeConnection(_ConnectionBase):
        """
        Connection class based on a Windows named pipe.
        Overlapped I/O is used, so the handles must have been created
        with FILE_FLAG_OVERLAPPED.
        """
        _got_empty_message = False
        _send_ov = None

        def _close(self, _CloseHandle=_winapi.CloseHandle):
            ov = self._send_ov
            if ov is not None:
                ov.cancel()
            _CloseHandle(self._handle)

        def _send_bytes(self, buf):
            if self._send_ov is not None:
                raise ValueError('concurrent send_bytes() calls are not supported')
            ov, err = _winapi.WriteFile(self._handle, buf, overlapped=True)
            self._send_ov = ov
            try:
                if err == _winapi.ERROR_IO_PENDING:
                    waitres = _winapi.WaitForMultipleObjects([ov.event], False, INFINITE)
                    assert waitres == WAIT_OBJECT_0
            except:
                ov.cancel()
                raise
            finally:
                self._send_ov = None
                nwritten, err = ov.GetOverlappedResult(True)
            if err == _winapi.ERROR_OPERATION_ABORTED:
                raise OSError(errno.EPIPE, 'handle is closed')
            assert err == 0
            assert nwritten == len(buf)

        def _recv_bytes(self, maxsize=None):
            if self._got_empty_message:
                self._got_empty_message = False
                return io.BytesIO()
            else:
                bsize = 128 if maxsize is None else min(maxsize, 128)
                try:
                    ov, err = _winapi.ReadFile(self._handle, bsize, overlapped=True)
                    sentinel = object()
                    return_value = sentinel
                    try:
                        try:
                            if err == _winapi.ERROR_IO_PENDING:
                                waitres = _winapi.WaitForMultipleObjects([ov.event], False, INFINITE)
                                assert waitres == WAIT_OBJECT_0
                        except:
                            ov.cancel()
                            raise
                        finally:
                            nread, err = ov.GetOverlappedResult(True)
                            if err == 0:
                                f = io.BytesIO()
                                f.write(ov.getbuffer())
                                return_value = f
                            elif err == _winapi.ERROR_MORE_DATA:
                                return_value = self._get_more_data(ov, maxsize)
                    except:
                        if return_value is sentinel:
                            raise
                    if return_value is not sentinel:
                        return return_value
                except OSError as e:
                    if e.winerror == _winapi.ERROR_BROKEN_PIPE:
                        raise EOFError
                    else:
                        raise
            raise RuntimeError("shouldn't get here; expected KeyboardInterrupt")

        def _poll(self, timeout):
            if self._got_empty_message or _winapi.PeekNamedPipe(self._handle)[0] != 0:
                return True
            return bool(wait([self], timeout))

        def _get_more_data(self, ov, maxsize):
            buf = ov.getbuffer()
            f = io.BytesIO()
            f.write(buf)
            left = _winapi.PeekNamedPipe(self._handle)[1]
            assert left > 0
            if maxsize is not None and len(buf) + left > maxsize:
                self._bad_message_length()
            ov, err = _winapi.ReadFile(self._handle, left, overlapped=True)
            rbytes, err = ov.GetOverlappedResult(True)
            assert err == 0
            assert rbytes == left
            f.write(ov.getbuffer())
            return f

class 连接(_ConnectionBase):
    """
    Connection class based on an arbitrary file descriptor (Unix only), or
    a socket handle (Windows).
    """
    if _winapi:

        def _close(self, _close=_multiprocessing.closesocket):
            _close(self._handle)
        _write = _multiprocessing.send
        _read = _multiprocessing.recv
    else:

        def _close(self, _close=os.close):
            _close(self._handle)
        _write = os.write
        _read = os.read

    def _send(self, buf, write=_write):
        remaining = len(buf)
        while True:
            n = write(self._handle, buf)
            remaining -= n
            if remaining == 0:
                break
            buf = buf[n:]

    def _recv(self, size, read=_read):
        buf = io.BytesIO()
        handle = self._handle
        remaining = size
        while remaining > 0:
            to_read = min(BUFSIZE, remaining)
            chunk = read(handle, to_read)
            n = len(chunk)
            if n == 0:
                if remaining == size:
                    raise EOFError
                else:
                    raise OSError('got end of file during message')
            buf.write(chunk)
            remaining -= n
        return buf

    def _send_bytes(self, buf):
        n = len(buf)
        if n > 2147483647:
            pre_header = struct.pack('!i', -1)
            header = struct.pack('!Q', n)
            self._send(pre_header)
            self._send(header)
            self._send(buf)
        else:
            header = struct.pack('!i', n)
            if n > 16384:
                self._send(header)
                self._send(buf)
            else:
                self._send(header + buf)

    def _recv_bytes(self, maxsize=None):
        buf = self._recv(4)
        size, = struct.unpack('!i', buf.getvalue())
        if size == -1:
            buf = self._recv(8)
            size, = struct.unpack('!Q', buf.getvalue())
        if maxsize is not None and size > maxsize:
            return None
        return self._recv(size)

    def _poll(self, timeout):
        r = wait([self], timeout)
        return bool(r)

class 监听器(object):
    """
    Returns a listener object.

    This is a wrapper for a bound socket which is 'listening' for
    connections, or for a Windows named pipe.
    """

    def __init__(self, address=None, family=None, backlog=1, authkey=None):
        family = family or (address and 地址类型(address)) or default_family
        _validate_family(family)
        if authkey is not None and (not isinstance(authkey, bytes)):
            raise TypeError('authkey should be a byte string')
        if family == 'AF_PIPE':
            if address:
                self._listener = PipeListener(address, backlog)
            else:
                for attempts in itertools.count():
                    address = 任意地址(family)
                    try:
                        self._listener = PipeListener(address, backlog)
                        break
                    except OSError as e:
                        if attempts >= _MAX_PIPE_ATTEMPTS:
                            raise
                        if e.winerror not in (_winapi.ERROR_PIPE_BUSY, _winapi.ERROR_ACCESS_DENIED):
                            raise
        else:
            address = address or 任意地址(family)
            self._listener = 套接字监听器(address, family, backlog)
        self._authkey = authkey

    def accept(self):
        """
        Accept a connection on the bound socket or named pipe of `self`.

        Returns a `Connection` object.
        """
        if self._listener is None:
            raise OSError('listener is closed')
        c = self._listener.accept()
        if self._authkey is not None:
            发送挑战(c, self._authkey)
            应答挑战(c, self._authkey)
        return c

    def close(self):
        """
        Close the bound socket or named pipe of `self`.
        """
        listener = self._listener
        if listener is not None:
            self._listener = None
            listener.close()

    @property
    def address(self):
        return self._listener._address

    @property
    def last_accepted(self):
        return self._listener._last_accepted

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

def 客户端(address, family=None, authkey=None):
    """
    Returns a connection to the address of a `Listener`
    """
    family = family or 地址类型(address)
    _validate_family(family)
    if family == 'AF_PIPE':
        c = PipeClient(address)
    else:
        c = 套接字客户端(address)
    if authkey is not None and (not isinstance(authkey, bytes)):
        raise TypeError('authkey should be a byte string')
    if authkey is not None:
        应答挑战(c, authkey)
        发送挑战(c, authkey)
    return c
if sys.platform != 'win32':

    def Pipe(duplex=True):
        """
        Returns pair of connection objects at either end of a pipe
        """
        if duplex:
            s1, s2 = socket.socketpair()
            s1.setblocking(True)
            s2.setblocking(True)
            c1 = 连接(s1.detach())
            c2 = 连接(s2.detach())
        else:
            fd1, fd2 = os.pipe()
            c1 = 连接(fd1, writable=False)
            c2 = 连接(fd2, readable=False)
        return (c1, c2)
else:

    def Pipe(duplex=True):
        """
        Returns pair of connection objects at either end of a pipe
        """
        if duplex:
            openmode = _winapi.PIPE_ACCESS_DUPLEX
            access = _winapi.GENERIC_READ | _winapi.GENERIC_WRITE
            obsize, ibsize = (BUFSIZE, BUFSIZE)
        else:
            openmode = _winapi.PIPE_ACCESS_INBOUND
            access = _winapi.GENERIC_WRITE
            obsize, ibsize = (0, BUFSIZE)
        for attempts in itertools.count():
            address = 任意地址('AF_PIPE')
            try:
                h1 = _winapi.CreateNamedPipe(address, openmode | _winapi.FILE_FLAG_OVERLAPPED | _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, 1, obsize, ibsize, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)
                break
            except OSError as e:
                if attempts >= _MAX_PIPE_ATTEMPTS:
                    raise
                if e.winerror not in (_winapi.ERROR_PIPE_BUSY, _winapi.ERROR_ACCESS_DENIED):
                    raise
        h2 = _winapi.CreateFile(address, access, 0, _winapi.NULL, _winapi.OPEN_EXISTING, _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL)
        _winapi.SetNamedPipeHandleState(h2, _winapi.PIPE_READMODE_MESSAGE, None, None)
        overlapped = _winapi.ConnectNamedPipe(h1, overlapped=True)
        _, err = overlapped.GetOverlappedResult(True)
        assert err == 0
        c1 = PipeConnection(h1, writable=duplex)
        c2 = PipeConnection(h2, readable=duplex)
        return (c1, c2)

class 套接字监听器(object):
    """
    Representation of a socket which is bound to an address and listening
    """

    def __init__(self, address, family, backlog=1):
        self._socket = socket.socket(getattr(socket, family))
        try:
            if os.name == 'posix':
                self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setblocking(True)
            self._socket.bind(address)
            self._socket.listen(backlog)
            self._address = self._socket.getsockname()
        except OSError:
            self._socket.close()
            raise
        self._family = family
        self._last_accepted = None
        if family == 'AF_UNIX' and (not util.is_abstract_socket_namespace(address)):
            self._unlink = util.Finalize(self, os.unlink, args=(address,), exitpriority=0)
        else:
            self._unlink = None

    def accept(self):
        s, self._last_accepted = self._socket.accept()
        s.setblocking(True)
        return 连接(s.detach())

    def close(self):
        try:
            self._socket.close()
        finally:
            unlink = self._unlink
            if unlink is not None:
                self._unlink = None
                unlink()

def 套接字客户端(address):
    """
    Return a connection object connected to the socket given by `address`
    """
    family = 地址类型(address)
    with socket.socket(getattr(socket, family)) as s:
        s.setblocking(True)
        s.connect(address)
        return 连接(s.detach())
if sys.platform == 'win32':

    class PipeListener(object):
        """
        Representation of a named pipe
        """

        def __init__(self, address, backlog=None):
            self._address = address
            self._handle_queue = [self._new_handle(first=True)]
            self._last_accepted = None
            util.sub_debug('listener created with address=%r', self._address)
            self.close = util.Finalize(self, PipeListener._finalize_pipe_listener, args=(self._handle_queue, self._address), exitpriority=0)

        def _new_handle(self, first=False):
            flags = _winapi.PIPE_ACCESS_DUPLEX | _winapi.FILE_FLAG_OVERLAPPED
            if first:
                flags |= _winapi.FILE_FLAG_FIRST_PIPE_INSTANCE
            return _winapi.CreateNamedPipe(self._address, flags, _winapi.PIPE_TYPE_MESSAGE | _winapi.PIPE_READMODE_MESSAGE | _winapi.PIPE_WAIT, _winapi.PIPE_UNLIMITED_INSTANCES, BUFSIZE, BUFSIZE, _winapi.NMPWAIT_WAIT_FOREVER, _winapi.NULL)

        def accept(self):
            self._handle_queue.append(self._new_handle())
            handle = self._handle_queue.pop(0)
            try:
                ov = _winapi.ConnectNamedPipe(handle, overlapped=True)
            except OSError as e:
                if e.winerror != _winapi.ERROR_NO_DATA:
                    raise
            else:
                try:
                    res = _winapi.WaitForMultipleObjects([ov.event], False, INFINITE)
                except:
                    ov.cancel()
                    _winapi.CloseHandle(handle)
                    raise
                finally:
                    _, err = ov.GetOverlappedResult(True)
                    assert err == 0
            return PipeConnection(handle)

        @staticmethod
        def _finalize_pipe_listener(queue, address):
            util.sub_debug('closing listener with address=%r', address)
            for handle in queue:
                _winapi.CloseHandle(handle)

    def PipeClient(address):
        """
        Return a connection object connected to the pipe given by `address`
        """
        t = _init_timeout()
        while 1:
            try:
                _winapi.WaitNamedPipe(address, 1000)
                h = _winapi.CreateFile(address, _winapi.GENERIC_READ | _winapi.GENERIC_WRITE, 0, _winapi.NULL, _winapi.OPEN_EXISTING, _winapi.FILE_FLAG_OVERLAPPED, _winapi.NULL)
            except OSError as e:
                if e.winerror not in (_winapi.ERROR_SEM_TIMEOUT, _winapi.ERROR_PIPE_BUSY) or _check_timeout(t):
                    raise
            else:
                break
        else:
            raise
        _winapi.SetNamedPipeHandleState(h, _winapi.PIPE_READMODE_MESSAGE, None, None)
        return PipeConnection(h)
MESSAGE_LENGTH = 40
_CHALLENGE = b'#CHALLENGE#'
_WELCOME = b'#WELCOME#'
_FAILURE = b'#FAILURE#'
_ALLOWED_DIGESTS = frozenset({b'md5', b'sha256', b'sha384', b'sha3_256', b'sha3_384'})
_MAX_DIGEST_LEN = max((len(_) for _ in _ALLOWED_DIGESTS))
_MD5ONLY_MESSAGE_LENGTH = 20
_MD5_DIGEST_LEN = 16
_LEGACY_LENGTHS = (_MD5ONLY_MESSAGE_LENGTH, _MD5_DIGEST_LEN)

def _get_digest_name_and_payload(message):
    """Returns a digest name and the payload for a response hash.

    If a legacy protocol is detected based on the message length
    or contents the digest name returned will be empty to indicate
    legacy mode where MD5 and no digest prefix should be sent.
    """
    if len(message) in _LEGACY_LENGTHS:
        return ('', message)
    if message.startswith(b'{') and (curly := message.find(b'}', 1, _MAX_DIGEST_LEN + 2)) > 0:
        digest = message[1:curly]
        if digest in _ALLOWED_DIGESTS:
            payload = message[curly + 1:]
            return (digest.decode('ascii'), payload)
    raise AuthenticationError(f'unsupported message length, missing digest prefix, or unsupported digest: message={message!r}')

def _create_response(authkey, message):
    """Create a MAC based on authkey and message

    The MAC algorithm defaults to HMAC-MD5, unless MD5 is not available or
    the message has a '{digest_name}' prefix. For legacy HMAC-MD5, the response
    is the raw MAC, otherwise the response is prefixed with '{digest_name}',
    e.g. b'{sha256}abcdefg...'

    Note: The MAC protects the entire message including the digest_name prefix.
    """
    import hmac
    digest_name = _get_digest_name_and_payload(message)[0]
    if not digest_name:
        try:
            return hmac.new(authkey, message, 'md5').digest()
        except ValueError:
            digest_name = 'sha256'
    response = hmac.new(authkey, message, digest_name).digest()
    return b'{%s}%s' % (digest_name.encode('ascii'), response)

def _verify_challenge(authkey, message, response):
    """Verify MAC challenge

    If our message did not include a digest_name prefix, the client is allowed
    to select a stronger digest_name from _ALLOWED_DIGESTS.

    In case our message is prefixed, a client cannot downgrade to a weaker
    algorithm, because the MAC is calculated over the entire message
    including the '{digest_name}' prefix.
    """
    import hmac
    response_digest, response_mac = _get_digest_name_and_payload(response)
    response_digest = response_digest or 'md5'
    try:
        expected = hmac.new(authkey, message, response_digest).digest()
    except ValueError:
        raise AuthenticationError(f'response_digest={response_digest!r} unsupported')
    if len(expected) != len(response_mac):
        raise AuthenticationError(f'expected {response_digest!r} of length {len(expected)} got {len(response_mac)}')
    if not hmac.compare_digest(expected, response_mac):
        raise AuthenticationError('digest received was wrong')

def 发送挑战(connection, authkey: bytes, digest_name='sha256'):
    if not isinstance(authkey, bytes):
        raise ValueError('Authkey must be bytes, not {0!s}'.format(type(authkey)))
    assert MESSAGE_LENGTH > _MD5ONLY_MESSAGE_LENGTH, 'protocol constraint'
    message = os.urandom(MESSAGE_LENGTH)
    message = b'{%s}%s' % (digest_name.encode('ascii'), message)
    connection.send_bytes(_CHALLENGE + message)
    response = connection.recv_bytes(256)
    try:
        _verify_challenge(authkey, message, response)
    except AuthenticationError:
        connection.send_bytes(_FAILURE)
        raise
    else:
        connection.send_bytes(_WELCOME)

def 应答挑战(connection, authkey: bytes):
    if not isinstance(authkey, bytes):
        raise ValueError('Authkey must be bytes, not {0!s}'.format(type(authkey)))
    message = connection.recv_bytes(256)
    if not message.startswith(_CHALLENGE):
        raise AuthenticationError(f'Protocol error, expected challenge: message={message!r}')
    message = message[len(_CHALLENGE):]
    if len(message) < _MD5ONLY_MESSAGE_LENGTH:
        raise AuthenticationError(f'challenge too short: {len(message)} bytes')
    digest = _create_response(authkey, message)
    connection.send_bytes(digest)
    response = connection.recv_bytes(256)
    if response != _WELCOME:
        raise AuthenticationError('digest sent was rejected')

class 连接包装(object):

    def __init__(self, conn, dumps, loads):
        self._conn = conn
        self._dumps = dumps
        self._loads = loads
        for attr in ('fileno', 'close', 'poll', 'recv_bytes', 'send_bytes'):
            obj = getattr(conn, attr)
            setattr(self, attr, obj)

    def send(self, obj):
        s = self._dumps(obj)
        self._conn.send_bytes(s)

    def recv(self):
        s = self._conn.recv_bytes()
        return self._loads(s)

def _xml_dumps(obj):
    return xmlrpclib.dumps((obj,), None, None, None, 1).encode('utf-8')

def _xml_loads(s):
    (obj,), method = xmlrpclib.loads(s.decode('utf-8'))
    return obj

class XML监听器(监听器):

    def accept(self):
        global xmlrpclib
        import xmlrpc.client as xmlrpclib
        obj = 监听器.accept(self)
        return 连接包装(obj, _xml_dumps, _xml_loads)

def XML客户端(*args, **kwds):
    global xmlrpclib
    import xmlrpc.client as xmlrpclib
    return 连接包装(客户端(*args, **kwds), _xml_dumps, _xml_loads)
if sys.platform == 'win32':

    def _exhaustive_wait(handles, timeout):
        L = list(handles)
        ready = []
        if len(L) > 60:
            try:
                res = _winapi.BatchedWaitForMultipleObjects(L, False, timeout)
            except TimeoutError:
                return []
            ready.extend((L[i] for i in res))
            if res:
                L = [h for i, h in enumerate(L) if i > res[0] & i not in res]
            timeout = 0
        while L:
            short_L = L[:60] if len(L) > 60 else L
            res = _winapi.WaitForMultipleObjects(short_L, False, timeout)
            if res == WAIT_TIMEOUT:
                break
            elif WAIT_OBJECT_0 <= res < WAIT_OBJECT_0 + len(L):
                res -= WAIT_OBJECT_0
            elif WAIT_ABANDONED_0 <= res < WAIT_ABANDONED_0 + len(L):
                res -= WAIT_ABANDONED_0
            else:
                raise RuntimeError('Should not get here')
            ready.append(L[res])
            L = L[res + 1:]
            timeout = 0
        return ready
    _ready_errors = {_winapi.ERROR_BROKEN_PIPE, _winapi.ERROR_NETNAME_DELETED}

    def wait(object_list, timeout=None):
        """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
        if timeout is None:
            timeout = INFINITE
        elif timeout < 0:
            timeout = 0
        else:
            timeout = int(timeout * 1000 + 0.5)
        object_list = list(object_list)
        waithandle_to_obj = {}
        ov_list = []
        ready_objects = set()
        ready_handles = set()
        try:
            for o in object_list:
                try:
                    fileno = getattr(o, 'fileno')
                except AttributeError:
                    waithandle_to_obj[o.__index__()] = o
                else:
                    try:
                        ov, err = _winapi.ReadFile(fileno(), 0, True)
                    except OSError as e:
                        ov, err = (None, e.winerror)
                        if err not in _ready_errors:
                            raise
                    if err == _winapi.ERROR_IO_PENDING:
                        ov_list.append(ov)
                        waithandle_to_obj[ov.event] = o
                    else:
                        if ov and sys.getwindowsversion()[:2] >= (6, 2):
                            try:
                                _, err = ov.GetOverlappedResult(False)
                            except OSError as e:
                                err = e.winerror
                            if not err and hasattr(o, '_got_empty_message'):
                                o._got_empty_message = True
                        ready_objects.add(o)
                        timeout = 0
            ready_handles = _exhaustive_wait(waithandle_to_obj.keys(), timeout)
        finally:
            for ov in ov_list:
                ov.cancel()
            for ov in ov_list:
                try:
                    _, err = ov.GetOverlappedResult(True)
                except OSError as e:
                    err = e.winerror
                    if err not in _ready_errors:
                        raise
                if err != _winapi.ERROR_OPERATION_ABORTED:
                    o = waithandle_to_obj[ov.event]
                    ready_objects.add(o)
                    if err == 0:
                        if hasattr(o, '_got_empty_message'):
                            o._got_empty_message = True
        ready_objects.update((waithandle_to_obj[h] for h in ready_handles))
        return [o for o in object_list if o in ready_objects]
else:
    import selectors
    if hasattr(selectors, 'PollSelector'):
        _WaitSelector = selectors.PollSelector
    else:
        _WaitSelector = selectors.SelectSelector

    def wait(object_list, timeout=None):
        """
        Wait till an object in object_list is ready/readable.

        Returns list of those objects in object_list which are ready/readable.
        """
        with _WaitSelector() as selector:
            for obj in object_list:
                selector.register(obj, selectors.EVENT_READ)
            if timeout is not None:
                deadline = time.monotonic() + timeout
            while True:
                ready = selector.select(timeout)
                if ready:
                    return [key.fileobj for key, events in ready]
                elif timeout is not None:
                    timeout = deadline - time.monotonic()
                    if timeout < 0:
                        return ready
if sys.platform == 'win32':

    def reduce_connection(conn):
        handle = conn.fileno()
        with socket.fromfd(handle, socket.AF_INET, socket.SOCK_STREAM) as s:
            from . import resource_sharer
            ds = resource_sharer.DupSocket(s)
            return (rebuild_connection, (ds, conn.readable, conn.writable))

    def rebuild_connection(ds, readable, writable):
        sock = ds.detach()
        return 连接(sock.detach(), readable, writable)
    reduction.register(连接, reduce_connection)

    def reduce_pipe_connection(conn):
        access = (_winapi.FILE_GENERIC_READ if conn.readable else 0) | (_winapi.FILE_GENERIC_WRITE if conn.writable else 0)
        dh = reduction.DupHandle(conn.fileno(), access)
        return (rebuild_pipe_connection, (dh, conn.readable, conn.writable))

    def rebuild_pipe_connection(dh, readable, writable):
        handle = dh.detach()
        return PipeConnection(handle, readable, writable)
    reduction.register(PipeConnection, reduce_pipe_connection)
else:

    def reduce_connection(conn):
        df = reduction.DupFd(conn.fileno())
        return (rebuild_connection, (df, conn.readable, conn.writable))

    def rebuild_connection(df, readable, writable):
        fd = df.detach()
        return 连接(fd, readable, writable)
    reduction.register(连接, reduce_connection)


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
    'ConnectionWrapper': '连接包装',
    'Listener': '监听器',
    'SocketClient': '套接字客户端',
    'SocketListener': '套接字监听器',
    'XmlClient': 'XML客户端',
    'XmlListener': 'XML监听器',
    'address_type': '地址类型',
    'answer_challenge': '应答挑战',
    'arbitrary_address': '任意地址',
    'deliver_challenge': '发送挑战',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    '客户端',
    '监听器',
])

# ---- 转发层结束 ----
