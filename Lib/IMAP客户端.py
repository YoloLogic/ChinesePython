# -*- coding: utf-8 -*-
"""IMAP客户端 —— 汉语库（由 tools/汉化库.py 从 Lib/imaplib.py 机械生成，**不要手改**）。

英文库 Lib/imaplib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py IMAP客户端
"""


"""IMAP4 client.

Based on RFC 3501.

Public class:           IMAP4
Public variable:        Debug
Public functions:       Internaldate2tuple
                        Int2AP
                        ParseFlags
                        Time2Internaldate
"""
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
__version__ = '2.60'
import binascii, errno, random, re, socket, subprocess, sys, time, calendar
from datetime import datetime, timezone, timedelta
from io import DEFAULT_BUFFER_SIZE
try:
    import ssl
    支持SSL = True
except ImportError:
    支持SSL = False
__all__ = ['IMAP4', 'IMAP4_stream', 'Internaldate2tuple', 'Int2AP', 'ParseFlags', 'Time2Internaldate']
回车换行 = b'\r\n'
Debug = 0
IMAP4端口 = 143
IMAP4安全端口 = 993
允许的版本 = ('IMAP4REV1', 'IMAP4')
_MAXLINE = 1000000
命令表 = {'APPEND': ('AUTH', 'SELECTED'), 'AUTHENTICATE': ('NONAUTH',), 'CAPABILITY': ('NONAUTH', 'AUTH', 'SELECTED', 'LOGOUT'), 'CHECK': ('SELECTED',), 'CLOSE': ('SELECTED',), 'COPY': ('SELECTED',), 'CREATE': ('AUTH', 'SELECTED'), 'DELETE': ('AUTH', 'SELECTED'), 'DELETEACL': ('AUTH', 'SELECTED'), 'ENABLE': ('AUTH',), 'EXAMINE': ('AUTH', 'SELECTED'), 'EXPUNGE': ('SELECTED',), 'FETCH': ('SELECTED',), 'GETACL': ('AUTH', 'SELECTED'), 'GETANNOTATION': ('AUTH', 'SELECTED'), 'GETQUOTA': ('AUTH', 'SELECTED'), 'GETQUOTAROOT': ('AUTH', 'SELECTED'), 'IDLE': ('AUTH', 'SELECTED'), 'MYRIGHTS': ('AUTH', 'SELECTED'), 'LIST': ('AUTH', 'SELECTED'), 'LOGIN': ('NONAUTH',), 'LOGOUT': ('NONAUTH', 'AUTH', 'SELECTED', 'LOGOUT'), 'LSUB': ('AUTH', 'SELECTED'), 'MOVE': ('SELECTED',), 'NAMESPACE': ('AUTH', 'SELECTED'), 'NOOP': ('NONAUTH', 'AUTH', 'SELECTED', 'LOGOUT'), 'PARTIAL': ('SELECTED',), 'PROXYAUTH': ('AUTH',), 'RENAME': ('AUTH', 'SELECTED'), 'SEARCH': ('SELECTED',), 'SELECT': ('AUTH', 'SELECTED'), 'SETACL': ('AUTH', 'SELECTED'), 'SETANNOTATION': ('AUTH', 'SELECTED'), 'SETQUOTA': ('AUTH', 'SELECTED'), 'SORT': ('SELECTED',), 'STARTTLS': ('NONAUTH',), 'STATUS': ('AUTH', 'SELECTED'), 'STORE': ('SELECTED',), 'SUBSCRIBE': ('AUTH', 'SELECTED'), 'THREAD': ('SELECTED',), 'UID': ('SELECTED',), 'UNSUBSCRIBE': ('AUTH', 'SELECTED'), 'UNSELECT': ('SELECTED',)}
继续响应 = re.compile(b'\\+( (?P<data>.*))?')
标志 = re.compile(b'.*FLAGS \\((?P<flags>[^\\)]*)\\)')
内部日期 = re.compile(b'.*INTERNALDATE "(?P<day>[ 0123][0-9])-(?P<mon>[A-Z][a-z][a-z])-(?P<year>[0-9][0-9][0-9][0-9]) (?P<hour>[0-9][0-9]):(?P<min>[0-9][0-9]):(?P<sec>[0-9][0-9]) (?P<zonen>[-+])(?P<zoneh>[0-9][0-9])(?P<zonem>[0-9][0-9])"')
字面量 = re.compile(b'.*{(?P<size>\\d+)}$', re.ASCII)
映射回车换行 = re.compile(b'\\r\\n|\\r|\\n')
响应码 = re.compile(b'\\[(?P<type>[A-Z-]+)( (?P<data>.*))?\\]')
无标签响应 = re.compile(b'\\* (?P<type>[A-Z-]+)( (?P<data>.*))?')
无标签状态 = re.compile(b'\\* (?P<data>\\d+) (?P<type>[A-Z-]+)( (?P<data2>.*))?', re.ASCII)
_Literal = b'.*{(?P<size>\\d+)}$'
_Untagged_status = b'\\* (?P<data>\\d+) (?P<type>[A-Z-]+)( (?P<data2>.*))?'
_control_chars = re.compile(b'[\x00\r\n]')
_non_astring_char = re.compile(b'[(){ \\x00-\\x1f\\x7f-\\xff%*\\\\"]')
_non_list_char = re.compile(b'[(){ \\x00-\\x1f\\x7f-\\xff\\\\"]')
_quoted = re.compile(b'"(?:[^"\\\\]|\\\\.)*+"')

def _paren_depth(data, depth=0):
    data = _quoted.sub(b'', data)
    return depth + data.count(b'(') - data.count(b')')

class IMAP4客户端:
    """IMAP4 client class.

    Instantiate with: IMAP4([host[, port[, timeout=None]]])

            host - host's name (default: localhost);
            port - port number (default: standard IMAP4 port).
            timeout - socket timeout (default: None)
                      If timeout is not given or is None,
                      the global default socket timeout is used

    All IMAP4rev1 commands are supported by methods of the same
    name (in lowercase).

    All arguments to commands are converted to strings, except for
    AUTHENTICATE, and the last argument to APPEND which is passed as
    an IMAP4 literal.  If necessary (the string contains any
    non-printing characters or white-space and isn't enclosed with
    either parentheses or double quotes) each string is quoted.
    However, the 'password' argument to the LOGIN command is always
    quoted.  If you want to avoid having an argument string quoted
    (eg: the 'flags' argument to STORE) then enclose the string in
    parentheses (eg: "(\\Deleted)").

    Each command returns a tuple: (type, [data, ...]) where 'type'
    is usually 'OK' or 'NO', and 'data' is either the text from the
    tagged response, or untagged results from command. Each 'data'
    is either a string, or a tuple. If a tuple, then the first part
    is the header of the response, and the second part contains
    the data (ie: 'literal' value).

    Errors raise the exception class <instance>.error("<reason>").
    IMAP4 server errors raise <instance>.abort("<reason>"),
    which is a sub-class of 'error'. Mailbox status changes
    from READ-WRITE to READ-ONLY raise the exception class
    <instance>.readonly("<reason>"), which is a sub-class of 'abort'.

    "error" exceptions imply a program error.
    "abort" exceptions imply the connection should be reset, and
            the command re-tried.
    "readonly" exceptions imply the command should be re-tried.

    Note: to use this module, you must read the RFCs pertaining to the
    IMAP4 protocol, as the semantics of the arguments to each IMAP4
    command are left to the invoker, not to mention the results. Also,
    most IMAP servers implement a sub-set of the commands available here.
    """

    class 错误(Exception):
        pass

    class 中止(错误):
        pass

    class 只读(中止):
        pass

    class _responsetimeout(TimeoutError):
        pass

    def __init__(self, host='', port=IMAP4端口, timeout=None):
        self.debug = Debug
        self.state = 'LOGOUT'
        self.literal = None
        self.tagged_commands = {}
        self.untagged_responses = {}
        self.continuation_response = ''
        self._idle_responses = []
        self._idle_capture = False
        self.is_readonly = False
        self.tagnum = 0
        self._tls_established = False
        self._mode_ascii()
        self._readbuf = []
        self.open(host, port, timeout)
        try:
            self._connect()
        except Exception:
            try:
                self.关闭连接()
            except OSError:
                pass
            raise

    def _mode_ascii(self):
        self.utf8_enabled = False
        self._encoding = 'ascii'
        self.字面量 = re.compile(_Literal, re.ASCII)
        self.无标签状态 = re.compile(_Untagged_status, re.ASCII)

    def _mode_utf8(self):
        self.utf8_enabled = True
        self._encoding = 'utf-8'
        self.字面量 = re.compile(_Literal)
        self.无标签状态 = re.compile(_Untagged_status)

    def _connect(self):
        self.tagpre = 整数转AP(random.randint(4096, 65535))
        self.tagre = re.compile(b'(?P<tag>' + self.tagpre + b'\\d+) (?P<type>[A-Z]+) (?P<data>.*)', re.ASCII)
        if __debug__:
            self._cmd_log_len = 10
            self._cmd_log_idx = 0
            self._cmd_log = {}
            if self.debug >= 1:
                self._mesg('imaplib version %s' % __version__)
                self._mesg('new IMAP4 connection, tag=%s' % self.tagpre)
        self.welcome = self._get_response()
        if 'PREAUTH' in self.untagged_responses:
            self.state = 'AUTH'
        elif 'OK' in self.untagged_responses:
            self.state = 'NONAUTH'
        else:
            greeting = (self.welcome or self.mo.string).decode(self._encoding, 'replace')
            raise self.错误('invalid greeting: ' + greeting)
        self._refresh_capabilities()
        if __debug__:
            if self.debug >= 3:
                self._mesg('CAPABILITIES: %r' % (self.capabilities,))
        for version in 允许的版本:
            if not version in self.capabilities:
                continue
            self.PROTOCOL_VERSION = version
            return
        raise self.错误('server not IMAP4 compliant')

    def __getattr__(self, attr):
        if attr in 命令表:
            return getattr(self, attr.lower())
        raise AttributeError("Unknown IMAP4 command: '%s'" % attr)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.state == 'LOGOUT':
            return
        try:
            self.登出()
        except OSError:
            pass

    def _create_socket(self, timeout):
        if timeout is not None and (not timeout):
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        host = None if not self.host else self.host
        sys.audit('imaplib.open', self, self.host, self.port)
        address = (host, self.port)
        if timeout is not None:
            return socket.create_connection(address, timeout)
        return socket.create_connection(address)

    def open(self, host='', port=IMAP4端口, timeout=None):
        """Setup connection to remote server on "host:port"
            (default: localhost:standard IMAP4 port).
        This connection will be used by the routines:
            read, readline, send, shutdown.
        """
        self.host = host
        self.port = port
        self.sock = self._create_socket(timeout)
        self._file = self.sock.makefile('rb')

    @property
    def file(self):
        import warnings
        warnings.warn('IMAP4.file is unsupported, can cause errors, and may be removed.', RuntimeWarning, stacklevel=2)
        return self._file

    def read(self, size):
        """Read 'size' bytes from remote."""
        parts = []
        while size > 0:
            if len(parts) < len(self._readbuf):
                buf = self._readbuf[len(parts)]
            else:
                try:
                    buf = self.sock.recv(DEFAULT_BUFFER_SIZE)
                except ConnectionError:
                    break
                if not buf:
                    break
                self._readbuf.append(buf)
            if len(buf) >= size:
                parts.append(buf[:size])
                self._readbuf = [buf[size:]] + self._readbuf[len(parts):]
                break
            parts.append(buf)
            size -= len(buf)
        return b''.join(parts)

    def readline(self):
        """Read line from remote."""
        LF = b'\n'
        parts = []
        length = 0
        while length < _MAXLINE:
            if len(parts) < len(self._readbuf):
                buf = self._readbuf[len(parts)]
            else:
                try:
                    buf = self.sock.recv(DEFAULT_BUFFER_SIZE)
                except ConnectionError:
                    break
                if not buf:
                    break
                self._readbuf.append(buf)
            pos = buf.find(LF)
            if pos != -1:
                pos += 1
                parts.append(buf[:pos])
                self._readbuf = [buf[pos:]] + self._readbuf[len(parts):]
                break
            parts.append(buf)
            length += len(buf)
        line = b''.join(parts)
        if len(line) > _MAXLINE:
            raise self.错误('got more than %d bytes' % _MAXLINE)
        return line

    def send(self, data):
        """Send data to remote."""
        sys.audit('imaplib.send', self, data)
        self.sock.sendall(data)

    def 关闭连接(self):
        """Close I/O established in "open"."""
        self._file.close()
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError as exc:
            if exc.errno != errno.ENOTCONN and getattr(exc, 'winerror', 0) != 10022:
                raise
        finally:
            self.sock.close()

    def socket(self):
        """Return socket instance used to connect to IMAP4 server.

        socket = <instance>.socket()
        """
        return self.sock

    def 最近(self):
        """Return most recent 'RECENT' responses if any exist,
        else prompt server for an update using the 'NOOP' command.

        (typ, [data]) = <instance>.recent()

        'data' is None if no new messages,
        else list of RECENT responses, most recent last.
        """
        name = 'RECENT'
        typ, dat = self._untagged_response('OK', [None], name)
        if dat[-1]:
            return (typ, dat)
        typ, dat = self.空操作()
        return self._untagged_response(typ, dat, name)

    def 响应(self, code):
        """Return data for response 'code' if received, or None.

        Old value for response 'code' is cleared.

        (code, [data]) = <instance>.response(code)
        """
        return self._untagged_response(code, [None], code.upper())

    def append(self, mailbox, flags, date_time, message):
        """Append message to named mailbox.

        (typ, [data]) = <instance>.append(mailbox, flags, date_time, message)

                All args except 'message' can be None.
        """
        name = 'APPEND'
        if not mailbox:
            mailbox = 'INBOX'
        if flags:
            flags = self._set_quote(flags)
        else:
            flags = None
        if date_time:
            date_time = 时间转内部日期(date_time)
        else:
            date_time = None
        literal = 映射回车换行.sub(回车换行, message)
        self.literal = literal
        return self._simple_command(name, self._astring(mailbox), flags, date_time)

    def 认证(self, mechanism, authobject):
        """Authenticate command - requires response processing.

        'mechanism' specifies which authentication mechanism is to
        be used - it must appear in <instance>.capabilities in the
        form AUTH=<mechanism>.

        'authobject' must be a callable object:

                data = authobject(response)

        It will be called to process server continuation responses; the
        response argument it is passed will be a bytes.  It should return bytes
        data that will be base64 encoded and sent to the server.  It should
        return None if the client abort response '*' should be sent instead.
        """
        mech = mechanism.upper()
        self.literal = _Authenticator(authobject).process
        typ, dat = self._simple_command('AUTHENTICATE', self._atom(mech))
        if typ != 'OK':
            raise self.错误(dat[-1].decode('utf-8', 'replace'))
        self.state = 'AUTH'
        self._refresh_capabilities()
        return (typ, dat)

    def 能力(self):
        """(typ, [data]) = <instance>.capability()
        Fetch capabilities list from server."""
        name = 'CAPABILITY'
        typ, dat = self._simple_command(name)
        return self._untagged_response(typ, dat, name)

    def 检查(self):
        """Checkpoint mailbox on server.

        (typ, [data]) = <instance>.check()
        """
        return self._simple_command('CHECK')

    def close(self):
        """Close currently selected mailbox.

        Deleted messages are removed from writable mailbox.
        This is the recommended command before 'LOGOUT'.

        (typ, [data]) = <instance>.close()
        """
        try:
            typ, dat = self._simple_command('CLOSE')
        finally:
            self.state = 'AUTH'
        return (typ, dat)

    def copy(self, message_set, new_mailbox):
        """Copy 'message_set' messages onto end of 'new_mailbox'.

        (typ, [data]) = <instance>.copy(message_set, new_mailbox)
        """
        return self._simple_command('COPY', self._sequence_set(message_set), self._astring(new_mailbox))

    def 创建(self, mailbox):
        """Create new mailbox.

        (typ, [data]) = <instance>.create(mailbox)
        """
        return self._simple_command('CREATE', self._astring(mailbox))

    def 删除信箱(self, mailbox):
        """Delete old mailbox.

        (typ, [data]) = <instance>.delete(mailbox)
        """
        return self._simple_command('DELETE', self._astring(mailbox))

    def 删ACL(self, mailbox, who):
        """Delete the ACLs (remove any rights) set for who on mailbox.

        (typ, [data]) = <instance>.deleteacl(mailbox, who)
        """
        return self._simple_command('DELETEACL', self._astring(mailbox), self._astring(who))

    def 启用(self, capability):
        """Send an RFC5161 enable string to the server.

        (typ, [data]) = <instance>.enable(capability)
        """
        if 'ENABLE' not in self.capabilities:
            raise IMAP4客户端.error('Server does not support ENABLE')
        typ, data = self._simple_command('ENABLE', capability)
        if typ == 'OK' and 'UTF8=ACCEPT' in capability.upper():
            self._mode_utf8()
        return (typ, data)

    def 彻底删除(self):
        """Permanently remove deleted items from selected mailbox.

        Generates 'EXPUNGE' response for each deleted message.

        (typ, [data]) = <instance>.expunge()

        'data' is list of 'EXPUNGE'd message numbers in order received.
        """
        name = 'EXPUNGE'
        typ, dat = self._simple_command(name)
        return self._untagged_response(typ, dat, name)

    def 取邮件(self, message_set, message_parts):
        """Fetch (parts of) messages.

        (typ, [data, ...]) = <instance>.fetch(message_set, message_parts)

        'message_parts' should be a string of selected parts
        enclosed in parentheses, eg: "(UID BODY[TEXT])".

        'data' are tuples of message part envelope and data.
        """
        name = 'FETCH'
        typ, dat = self._simple_command(name, self._sequence_set(message_set), self._fetch_parts(message_parts))
        return self._untagged_response(typ, dat, name)

    def 取ACL(self, mailbox):
        """Get the ACLs for a mailbox.

        (typ, [data]) = <instance>.getacl(mailbox)
        """
        typ, dat = self._simple_command('GETACL', self._astring(mailbox))
        return self._untagged_response(typ, dat, 'ACL')

    def 取注解(self, mailbox, entry, attribute):
        """(typ, [data]) = <instance>.getannotation(mailbox, entry, attribute)
        Retrieve ANNOTATIONs."""
        typ, dat = self._simple_command('GETANNOTATION', self._astring(mailbox), entry, attribute)
        return self._untagged_response(typ, dat, 'ANNOTATION')

    def 取配额(self, root):
        """Get the quota root's resource usage and limits.

        Part of the IMAP4 QUOTA extension defined in rfc2087.

        (typ, [data]) = <instance>.getquota(root)
        """
        typ, dat = self._simple_command('GETQUOTA', self._astring(root))
        return self._untagged_response(typ, dat, 'QUOTA')

    def 取配额根(self, mailbox):
        """Get the list of quota roots for the named mailbox.

        (typ, [[QUOTAROOT responses...], [QUOTA responses]]) = <instance>.getquotaroot(mailbox)
        """
        typ, dat = self._simple_command('GETQUOTAROOT', self._astring(mailbox))
        typ, quota = self._untagged_response(typ, dat, 'QUOTA')
        typ, quotaroot = self._untagged_response(typ, dat, 'QUOTAROOT')
        return (typ, [quotaroot, quota])

    def 空闲等待(self, duration=None):
        """Return an iterable IDLE context manager producing untagged responses.
        If the argument is not None, limit iteration to 'duration' seconds.

        with M.idle(duration=29 * 60) as idler:
            for typ, data in idler:
                print(typ, data)

        Note: 'duration' requires a socket connection (not IMAP4_stream).
        """
        return 空闲器(self, duration)

    def list(self, directory='', pattern='*'):
        """List mailbox names in directory matching pattern.

        (typ, [data]) = <instance>.list(directory='', pattern='*')

        'data' is list of LIST responses.
        """
        name = 'LIST'
        typ, dat = self._simple_command(name, self._astring(directory), self._list_mailbox(pattern))
        return self._untagged_response(typ, dat, name)

    def 登录(self, user, password):
        """Identify client using plaintext password.

        (typ, [data]) = <instance>.login(user, password)

        NB: 'password' will be quoted.
        """
        typ, dat = self._simple_command('LOGIN', self._astring(user), self._quote(password))
        if typ != 'OK':
            raise self.错误(dat[-1].decode('UTF-8', 'replace'))
        self.state = 'AUTH'
        self._refresh_capabilities()
        return (typ, dat)

    def CRAMMD5登录(self, user, password):
        """ Force use of CRAM-MD5 authentication.

        (typ, [data]) = <instance>.login_cram_md5(user, password)
        """
        self.user, self.password = (user, password)
        return self.认证('CRAM-MD5', self._CRAM_MD5_AUTH)

    def _CRAM_MD5_AUTH(self, challenge):
        """ Authobject to use with CRAM-MD5 authentication. """
        import hmac
        if isinstance(self.password, str):
            password = self.password.encode('utf-8')
        else:
            password = self.password
        try:
            authcode = hmac.HMAC(password, challenge, 'md5')
        except ValueError:
            raise self.错误('CRAM-MD5 authentication is not supported')
        return f'{self.user} {authcode.hexdigest()}'

    def 登出(self):
        """Shutdown connection to server.

        (typ, [data]) = <instance>.logout()

        Returns server 'BYE' response.
        """
        self.state = 'LOGOUT'
        typ, dat = self._simple_command('LOGOUT')
        self.关闭连接()
        return (typ, dat)

    def 列订阅(self, directory='', pattern='*'):
        """List 'subscribed' mailbox names in directory matching pattern.

        (typ, [data, ...]) = <instance>.lsub(directory='', pattern='*')

        'data' are tuples of message part envelope and data.
        """
        name = 'LSUB'
        typ, dat = self._simple_command(name, self._astring(directory), self._list_mailbox(pattern))
        return self._untagged_response(typ, dat, name)

    def 我的权限(self, mailbox):
        """Show my ACLs for a mailbox (i.e. the rights that I have on mailbox).

        (typ, [data]) = <instance>.myrights(mailbox)
        """
        typ, dat = self._simple_command('MYRIGHTS', self._astring(mailbox))
        return self._untagged_response(typ, dat, 'MYRIGHTS')

    def 命名空间(self):
        """ Returns IMAP namespaces ala rfc2342

        (typ, [data, ...]) = <instance>.namespace()
        """
        name = 'NAMESPACE'
        typ, dat = self._simple_command(name)
        return self._untagged_response(typ, dat, name)

    def 空操作(self):
        """Send NOOP command.

        (typ, [data]) = <instance>.noop()
        """
        if __debug__:
            if self.debug >= 3:
                self._dump_ur(self.untagged_responses)
        return self._simple_command('NOOP')

    def 部分取(self, message_num, message_part, start, length):
        """Fetch truncated part of a message.

        (typ, [data, ...]) = <instance>.partial(message_num, message_part, start, length)

        'data' is tuple of message part envelope and data.
        """
        name = 'PARTIAL'
        typ, dat = self._simple_command(name, message_num, message_part, start, length)
        return self._untagged_response(typ, dat, 'FETCH')

    def 代理认证(self, user):
        """Assume authentication as "user".

        Allows an authorised administrator to proxy into any user's
        mailbox.

        (typ, [data]) = <instance>.proxyauth(user)
        """
        name = 'PROXYAUTH'
        return self._simple_command(name, self._astring(user))

    def 重命名(self, oldmailbox, newmailbox):
        """Rename old mailbox name to new.

        (typ, [data]) = <instance>.rename(oldmailbox, newmailbox)
        """
        return self._simple_command('RENAME', self._astring(oldmailbox), self._astring(newmailbox))

    def 搜索(self, charset, *criteria):
        """Search mailbox for matching messages.

        (typ, [data]) = <instance>.search(charset, criterion, ...)

        'data' is space separated list of matching message numbers.
        If UTF8 is enabled, charset MUST be None.
        """
        name = 'SEARCH'
        if charset is not None:
            if self.utf8_enabled:
                raise IMAP4客户端.error('Non-None charset not valid in UTF8 mode')
            typ, dat = self._simple_command(name, 'CHARSET', self._astring(charset), *criteria)
        else:
            typ, dat = self._simple_command(name, *criteria)
        return self._untagged_response(typ, dat, name)

    def 选择信箱(self, mailbox='INBOX', readonly=False):
        """Select a mailbox.

        Flush all untagged responses.

        (typ, [data]) = <instance>.select(mailbox='INBOX', readonly=False)

        'data' is count of messages in mailbox ('EXISTS' response).

        Mandated responses are ('FLAGS', 'EXISTS', 'RECENT', 'UIDVALIDITY'), so
        other responses should be obtained via <instance>.response('FLAGS') etc.
        """
        self.untagged_responses = {}
        self.is_readonly = readonly
        if readonly:
            name = 'EXAMINE'
        else:
            name = 'SELECT'
        typ, dat = self._simple_command(name, self._astring(mailbox))
        if typ != 'OK':
            self.state = 'AUTH'
            return (typ, dat)
        self.state = 'SELECTED'
        if 'READ-ONLY' in self.untagged_responses and (not readonly):
            if __debug__:
                if self.debug >= 1:
                    self._dump_ur(self.untagged_responses)
            raise self.只读('%r is not writable' % (mailbox,))
        return (typ, self.untagged_responses.get('EXISTS', [None]))

    def 设ACL(self, mailbox, who, what):
        """Set a mailbox acl.

        (typ, [data]) = <instance>.setacl(mailbox, who, what)
        """
        return self._simple_command('SETACL', self._astring(mailbox), self._astring(who), self._astring(what))

    def 设注解(self, mailbox, *args):
        """(typ, [data]) = <instance>.setannotation(mailbox[, entry, attribute]+)
        Set ANNOTATIONs."""
        typ, dat = self._simple_command('SETANNOTATION', self._astring(mailbox), *args)
        return self._untagged_response(typ, dat, 'ANNOTATION')

    def 设配额(self, root, limits):
        """Set the quota root's resource limits.

        (typ, [data]) = <instance>.setquota(root, limits)
        """
        typ, dat = self._simple_command('SETQUOTA', self._astring(root), self._set_quote(limits))
        return self._untagged_response(typ, dat, 'QUOTA')

    def sort(self, sort_criteria, charset, *search_criteria):
        """IMAP4rev1 extension SORT command.

        (typ, [data]) = <instance>.sort(sort_criteria, charset, search_criteria, ...)
        """
        name = 'SORT'
        sort_criteria = self._set_quote(sort_criteria)
        if charset is not None:
            charset = self._astring(charset)
        typ, dat = self._simple_command(name, sort_criteria, charset, *search_criteria)
        return self._untagged_response(typ, dat, name)

    def 启动TLS(self, ssl_context=None):
        name = 'STARTTLS'
        if not 支持SSL:
            raise self.错误('SSL support missing')
        if self._tls_established:
            raise self.中止('TLS session already established')
        if name not in self.capabilities:
            raise self.中止('TLS not supported by server')
        if ssl_context is None:
            ssl_context = ssl._create_stdlib_context()
        typ, dat = self._simple_command(name)
        if typ == 'OK':
            self.sock = ssl_context.wrap_socket(self.sock, server_hostname=self.host)
            self._file = self.sock.makefile('rb')
            self._tls_established = True
            self._get_capabilities()
        else:
            raise self.错误("Couldn't establish TLS session")
        return self._untagged_response(typ, dat, name)

    def 取状态(self, mailbox, names):
        """Request named status conditions for mailbox.

        (typ, [data]) = <instance>.status(mailbox, names)
        """
        name = 'STATUS'
        typ, dat = self._simple_command(name, self._astring(mailbox), self._set_quote(names))
        return self._untagged_response(typ, dat, name)

    def 存储(self, message_set, command, flags):
        """Alters flag dispositions for messages in mailbox.

        (typ, [data]) = <instance>.store(message_set, command, flags)
        """
        flags = self._set_quote(flags)
        typ, dat = self._simple_command('STORE', self._sequence_set(message_set), command, flags)
        return self._untagged_response(typ, dat, 'FETCH')

    def 订阅(self, mailbox):
        """Subscribe to new mailbox.

        (typ, [data]) = <instance>.subscribe(mailbox)
        """
        return self._simple_command('SUBSCRIBE', self._astring(mailbox))

    def 线索搜索(self, threading_algorithm, charset, *search_criteria):
        """IMAPrev1 extension THREAD command.

        (type, [data]) = <instance>.thread(threading_algorithm, charset, search_criteria, ...)
        """
        name = 'THREAD'
        if charset is not None:
            charset = self._astring(charset)
        typ, dat = self._simple_command(name, self._atom(threading_algorithm), charset, *search_criteria)
        return self._untagged_response(typ, dat, name)

    def 唯一标识(self, command, *args):
        """Execute "command arg ..." with messages identified by UID,
                rather than message number.

        (typ, [data]) = <instance>.uid(command, arg1, arg2, ...)

        Returns response appropriate to 'command'.
        """
        command = command.upper()
        if not command in 命令表:
            raise self.错误('Unknown IMAP4 UID command: %r' % (command,))
        if self.state not in 命令表[command]:
            raise self.错误('command %s illegal in state %s, only allowed in states %s' % (command, self.state, ', '.join(命令表[command])))
        name = 'UID'
        if command == 'COPY':
            message_set, new_mailbox = args
            args = (self._sequence_set(message_set), self._astring(new_mailbox))
        elif command == 'FETCH':
            message_set, message_parts = args
            args = (self._sequence_set(message_set), self._fetch_parts(message_parts))
        elif command == 'STORE':
            message_set, op, flags = args
            args = (self._sequence_set(message_set), op, self._set_quote(flags))
        elif command == 'SORT':
            sort_criteria, charset, *search_criteria = args
            if charset is not None:
                charset = self._astring(charset)
            args = (self._set_quote(sort_criteria), charset, *search_criteria)
        elif command == 'THREAD':
            threading_algorithm, charset, *search_criteria = args
            if charset is not None:
                charset = self._astring(charset)
            args = (self._atom(threading_algorithm), charset, *search_criteria)
        typ, dat = self._simple_command(name, self._atom(command), *args)
        if command in ('SEARCH', 'SORT', 'THREAD'):
            name = command
        else:
            name = 'FETCH'
        return self._untagged_response(typ, dat, name)

    def 退订(self, mailbox):
        """Unsubscribe from old mailbox.

        (typ, [data]) = <instance>.unsubscribe(mailbox)
        """
        return self._simple_command('UNSUBSCRIBE', self._astring(mailbox))

    def 取消选择(self):
        """Free server's resources associated with the selected mailbox
        and returns the server to the authenticated state.
        This command performs the same actions as CLOSE, except
        that no messages are permanently removed from the currently
        selected mailbox.

        (typ, [data]) = <instance>.unselect()
        """
        try:
            typ, data = self._simple_command('UNSELECT')
        finally:
            self.state = 'AUTH'
        return (typ, data)

    def X原子(self, name, *args):
        """Allow simple extension commands
                notified by server in CAPABILITY response.

        Assumes command is legal in current state.

        (typ, [data]) = <instance>.xatom(name, arg, ...)

        Returns response appropriate to extension command 'name'.
        """
        name = name.upper()
        if not name in 命令表:
            命令表[name] = (self.state,)
        return self._simple_command(name, *args)

    def _append_untagged(self, typ, dat):
        if dat is None:
            dat = b''
        if self._idle_capture:
            if not self._idle_responses or isinstance(self._idle_responses[-1][1][-1], bytes):
                self._idle_responses.append((typ, [dat]))
            else:
                响应 = self._idle_responses[-1]
                assert 响应[0] == typ
                响应[1].append(dat)
            if __debug__ and self.debug >= 5:
                self._mesg(f'idle: queue untagged {typ} {dat!r}')
            return
        ur = self.untagged_responses
        if __debug__:
            if self.debug >= 5:
                self._mesg('untagged_responses[%s] %s += ["%r"]' % (typ, len(ur.get(typ, '')), dat))
        if typ in ur:
            ur[typ].append(dat)
        else:
            ur[typ] = [dat]

    def _check_bye(self):
        bye = self.untagged_responses.get('BYE')
        if bye:
            raise self.中止(bye[-1].decode(self._encoding, 'replace'))

    def _command(self, name, *args):
        if self.state not in 命令表[name]:
            self.literal = None
            raise self.错误('command %s illegal in state %s, only allowed in states %s' % (name, self.state, ', '.join(命令表[name])))
        for typ in ('OK', 'NO', 'BAD'):
            if typ in self.untagged_responses:
                del self.untagged_responses[typ]
        if 'READ-ONLY' in self.untagged_responses and (not self.is_readonly):
            raise self.只读('mailbox status changed to READ-ONLY')
        tag = self._new_tag()
        name = bytes(name, self._encoding)
        data = tag + b' ' + name
        for arg in args:
            if arg is None:
                continue
            if isinstance(arg, str):
                arg = bytes(arg, self._encoding)
            if _control_chars.search(arg):
                raise ValueError('NUL, CR and LF not allowed in commands')
            data = data + b' ' + arg
        literal = self.literal
        if literal is not None:
            self.literal = None
            if type(literal) is type(self._command):
                literator = literal
            else:
                literator = None
                if self.utf8_enabled:
                    data = data + bytes(' UTF8 (~{%s}' % len(literal), self._encoding)
                    literal = literal + b')'
                else:
                    data = data + bytes(' {%s}' % len(literal), self._encoding)
        if __debug__:
            if self.debug >= 4:
                self._mesg('> %r' % data)
            else:
                self._log('> %r' % data)
        try:
            self.send(data + 回车换行)
        except OSError as val:
            raise self.中止('socket error: %s' % val)
        if literal is None:
            return tag
        while 1:
            while self._get_response():
                if self.tagged_commands[tag]:
                    return tag
            if literator:
                literal = literator(self.continuation_response)
            if __debug__:
                if self.debug >= 4:
                    self._mesg('write literal size %s' % len(literal))
            try:
                self.send(literal)
                self.send(回车换行)
            except OSError as val:
                raise self.中止('socket error: %s' % val)
            if not literator:
                break
        return tag

    def _command_complete(self, name, tag):
        登出 = name == 'LOGOUT'
        if not 登出:
            self._check_bye()
        try:
            typ, data = self._get_tagged_response(tag, expect_bye=登出)
        except self.中止 as val:
            raise self.中止('command: %s => %s' % (name, val))
        except self.错误 as val:
            raise self.错误('command: %s => %s' % (name, val))
        if not 登出:
            self._check_bye()
        if typ == 'BAD':
            raise self.错误('%s command error: %s %s' % (name, typ, data))
        return (typ, data)

    def _get_capabilities(self):
        typ, dat = self.能力()
        if dat == [None]:
            raise self.错误('no CAPABILITY response from server')
        dat = str(dat[-1], self._encoding)
        dat = dat.upper()
        self.capabilities = tuple(dat.split())

    def _refresh_capabilities(self):
        if 'CAPABILITY' in self.untagged_responses:
            dat = self.untagged_responses.pop('CAPABILITY')[-1]
            self.capabilities = tuple(str(dat, self._encoding).upper().split())
        else:
            self._get_capabilities()

    def _get_response(self, start_timeout=False):
        if start_timeout is not False and self.sock:
            assert start_timeout is None or start_timeout > 0
            saved_timeout = self.sock.gettimeout()
            self.sock.settimeout(start_timeout)
            try:
                resp = self._get_line()
            except TimeoutError as err:
                raise self._responsetimeout from err
            finally:
                self.sock.settimeout(saved_timeout)
        else:
            resp = self._get_line()
        while resp == b'':
            resp = self._get_line()
        if self._match(self.tagre, resp):
            tag = self.mo.group('tag')
            if not tag in self.tagged_commands:
                raise self.中止('unexpected tagged response: %r' % resp)
            typ = self.mo.group('type')
            typ = str(typ, self._encoding)
            dat = self.mo.group('data')
            self.tagged_commands[tag] = (typ, [dat])
        else:
            dat2 = None
            if not self._match(无标签响应, resp):
                if self._match(self.无标签状态, resp):
                    dat2 = self.mo.group('data2')
            if self.mo is None:
                if self._match(继续响应, resp):
                    self.continuation_response = self.mo.group('data')
                    return None
                raise self.中止('unexpected response: %r' % resp)
            typ = self.mo.group('type')
            typ = str(typ, self._encoding)
            dat = self.mo.group('data')
            if dat is None:
                dat = b''
            if dat2:
                dat = dat + b' ' + dat2
            depth = 0
            while self._match(self.字面量, dat):
                size = int(self.mo.group('size'))
                if __debug__:
                    if self.debug >= 4:
                        self._mesg('read literal size %s' % size)
                data = self.read(size)
                self._append_untagged(typ, (dat, data))
                depth = _paren_depth(dat, depth)
                dat = self._get_line()
                while dat == b'' and depth > 0:
                    dat = self._get_line()
            self._append_untagged(typ, dat)
        if typ in ('OK', 'NO', 'BAD') and self._match(响应码, dat):
            typ = self.mo.group('type')
            typ = str(typ, self._encoding)
            self._append_untagged(typ, self.mo.group('data'))
        if __debug__:
            if self.debug >= 1 and typ in ('NO', 'BAD', 'BYE'):
                self._mesg('%s response: %r' % (typ, dat))
        return resp

    def _get_tagged_response(self, tag, expect_bye=False):
        while 1:
            result = self.tagged_commands[tag]
            if result is not None:
                del self.tagged_commands[tag]
                return result
            if expect_bye:
                typ = 'BYE'
                bye = self.untagged_responses.pop(typ, None)
                if bye is not None:
                    return (typ, bye)
            self._check_bye()
            try:
                self._get_response()
            except self.中止 as val:
                if __debug__:
                    if self.debug >= 1:
                        self.打印日志()
                raise

    def _get_line(self):
        line = self.readline()
        if not line:
            raise self.中止('socket error: EOF')
        if not line.endswith(b'\r\n'):
            raise self.中止('socket error: unterminated line: %r' % line)
        line = line[:-2]
        if __debug__:
            if self.debug >= 4:
                self._mesg('< %r' % line)
            else:
                self._log('< %r' % line)
        return line

    def _match(self, cre, s):
        self.mo = cre.match(s)
        if __debug__:
            if self.mo is not None and self.debug >= 5:
                self._mesg('\tmatched %r => %r' % (cre.pattern, self.mo.groups()))
        return self.mo is not None

    def _new_tag(self):
        tag = self.tagpre + bytes(str(self.tagnum), self._encoding)
        self.tagnum = self.tagnum + 1
        self.tagged_commands[tag] = None
        return tag

    def _atom(self, arg):
        return arg

    def _sequence_set(self, arg):
        return arg

    def _set_quote(self, arg):
        if arg and arg[0] == '(' and (arg[-1] == ')'):
            return arg
        return '(' + arg + ')'

    def _fetch_parts(self, arg):
        if arg.upper() in ('ALL', 'FULL', 'FAST'):
            return arg
        return self._set_quote(arg)

    def _quote(self, arg):
        if isinstance(arg, str):
            arg = bytes(arg, self._encoding)
        arg = arg.replace(b'\\', b'\\\\')
        arg = arg.replace(b'"', b'\\"')
        return b'"' + arg + b'"'

    def _astring(self, arg):
        if isinstance(arg, str):
            arg = bytes(arg, self._encoding)
        if _quoted.fullmatch(arg):
            return arg
        if arg and _non_astring_char.search(arg) is None:
            return arg
        return self._quote(arg)

    def _list_mailbox(self, arg):
        if isinstance(arg, str):
            arg = bytes(arg, self._encoding)
        if _quoted.fullmatch(arg):
            return arg
        if arg and _non_list_char.search(arg) is None:
            return arg
        return self._quote(arg)

    def _simple_command(self, name, *args):
        return self._command_complete(name, self._command(name, *args))

    def _untagged_response(self, typ, dat, name):
        if typ == 'NO':
            return (typ, dat)
        if not name in self.untagged_responses:
            return (typ, [None])
        data = self.untagged_responses.pop(name)
        if __debug__:
            if self.debug >= 5:
                self._mesg('untagged_responses[%s] => %s' % (name, data))
        return (typ, data)
    if __debug__:

        def _mesg(self, s, secs=None):
            if secs is None:
                secs = time.time()
            tm = time.strftime('%M:%S', time.localtime(secs))
            sys.stderr.write('  %s.%02d %s\n' % (tm, secs * 100 % 100, s))
            sys.stderr.flush()

        def _dump_ur(self, untagged_resp_dict):
            if not untagged_resp_dict:
                return
            items = (f'{key}: {value!r}' for key, value in untagged_resp_dict.items())
            self._mesg('untagged responses dump:' + '\n\t\t'.join(items))

        def _log(self, line):
            self._cmd_log[self._cmd_log_idx] = (line, time.time())
            self._cmd_log_idx += 1
            if self._cmd_log_idx >= self._cmd_log_len:
                self._cmd_log_idx = 0

        def 打印日志(self):
            self._mesg('last %d IMAP4 interactions:' % len(self._cmd_log))
            i, n = (self._cmd_log_idx, self._cmd_log_len)
            while n:
                try:
                    self._mesg(*self._cmd_log[i])
                except:
                    pass
                i += 1
                if i >= self._cmd_log_len:
                    i = 0
                n -= 1
_装类转发(IMAP4客户端, {'authenticate': '认证', 'capability': '能力', 'check': '检查', 'create': '创建', 'delete': '删除信箱', 'deleteacl': '删ACL', 'enable': '启用', 'expunge': '彻底删除', 'fetch': '取邮件', 'getacl': '取ACL', 'getannotation': '取注解', 'getquota': '取配额', 'getquotaroot': '取配额根', 'idle': '空闲等待', 'login': '登录', 'login_cram_md5': 'CRAMMD5登录', 'logout': '登出', 'lsub': '列订阅', 'myrights': '我的权限', 'namespace': '命名空间', 'noop': '空操作', 'partial': '部分取', 'print_log': '打印日志', 'proxyauth': '代理认证', 'recent': '最近', 'rename': '重命名', 'response': '响应', 'search': '搜索', 'select': '选择信箱', 'setacl': '设ACL', 'setannotation': '设注解', 'setquota': '设配额', 'shutdown': '关闭连接', 'starttls': '启动TLS', 'status': '取状态', 'store': '存储', 'subscribe': '订阅', 'thread': '线索搜索', 'uid': '唯一标识', 'unselect': '取消选择', 'unsubscribe': '退订', 'xatom': 'X原子'}, {'Literal': '字面量', 'Untagged_status': '无标签状态', 'abort': '中止', 'authenticate': '认证', 'capability': '能力', 'check': '检查', 'create': '创建', 'delete': '删除信箱', 'deleteacl': '删ACL', 'enable': '启用', 'error': '错误', 'expunge': '彻底删除', 'fetch': '取邮件', 'getacl': '取ACL', 'getannotation': '取注解', 'getquota': '取配额', 'getquotaroot': '取配额根', 'idle': '空闲等待', 'login': '登录', 'login_cram_md5': 'CRAMMD5登录', 'logout': '登出', 'lsub': '列订阅', 'myrights': '我的权限', 'namespace': '命名空间', 'noop': '空操作', 'partial': '部分取', 'print_log': '打印日志', 'proxyauth': '代理认证', 'readonly': '只读', 'recent': '最近', 'rename': '重命名', 'response': '响应', 'search': '搜索', 'select': '选择信箱', 'setacl': '设ACL', 'setannotation': '设注解', 'setquota': '设配额', 'shutdown': '关闭连接', 'starttls': '启动TLS', 'status': '取状态', 'store': '存储', 'subscribe': '订阅', 'thread': '线索搜索', 'uid': '唯一标识', 'unselect': '取消选择', 'unsubscribe': '退订', 'xatom': 'X原子'})

class 空闲器:
    """Iterable IDLE context manager: start IDLE & produce untagged responses.

    An object of this type is returned by the IMAP4.idle() method.

    Note: The name and structure of this class are subject to change.
    """

    def __init__(self, imap, duration=None):
        if 'IDLE' not in imap.capabilities:
            raise imap.error('Server does not support IMAP4 IDLE')
        if duration is not None and (not imap.sock):
            raise imap.error('duration requires a socket connection')
        self._duration = duration
        self._deadline = None
        self._imap = imap
        self._tag = None
        self._saved_state = None

    def __enter__(self):
        imap = self._imap
        assert not imap._idle_responses
        assert not imap._idle_capture
        if __debug__ and imap.debug >= 4:
            imap._mesg(f'idle start duration={self._duration}')
        imap._idle_capture = True
        try:
            self._tag = imap._command('IDLE')
            while (resp := imap._get_response()):
                if imap.tagged_commands[self._tag]:
                    typ, data = imap.tagged_commands.pop(self._tag)
                    if typ == 'NO':
                        raise imap.error(f'idle denied: {data}')
                    raise imap.abort(f'unexpected status response: {resp}')
            if __debug__ and imap.debug >= 4:
                prompt = imap.continuation_response
                imap._mesg(f'idle continuation prompt: {prompt}')
        except BaseException:
            imap._idle_capture = False
            raise
        if self._duration is not None:
            self._deadline = time.monotonic() + self._duration
        self._saved_state = imap.state
        imap.state = 'IDLING'
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        imap = self._imap
        if __debug__ and imap.debug >= 4:
            imap._mesg('idle done')
        imap.state = self._saved_state
        imap._idle_capture = False
        if (leftovers := len(imap._idle_responses)):
            if __debug__ and imap.debug >= 4:
                imap._mesg(f'idle quit with {leftovers} leftover responses')
            while imap._idle_responses:
                typ, data = imap._idle_responses.pop(0)
                for datum in data:
                    imap._append_untagged(typ, datum)
        try:
            imap.send(b'DONE' + 回车换行)
            取状态, [msg] = imap._command_complete('IDLE', self._tag)
            if __debug__ and imap.debug >= 4:
                imap._mesg(f'idle status: {取状态} {msg!r}')
        except OSError:
            if not exc_type:
                raise
        return False

    def __iter__(self):
        return self

    def _pop(self, timeout, default=('', None)):
        imap = self._imap
        if imap.state != 'IDLING':
            raise imap.error('_pop() only works during IDLE')
        if imap._idle_responses:
            resp = imap._idle_responses.pop(0)
            if __debug__ and imap.debug >= 4:
                imap._mesg(f'idle _pop({timeout}) de-queued {resp[0]}')
            return resp
        if __debug__ and imap.debug >= 4:
            imap._mesg(f'idle _pop({timeout}) reading')
        if timeout is not None:
            if timeout <= 0:
                return default
            timeout = float(timeout)
        try:
            imap._get_response(timeout)
        except IMAP4客户端._responsetimeout:
            if __debug__ and imap.debug >= 4:
                imap._mesg(f'idle _pop({timeout}) done')
            return default
        resp = imap._idle_responses.pop(0)
        if __debug__ and imap.debug >= 4:
            imap._mesg(f'idle _pop({timeout}) read {resp[0]}')
        return resp

    def __next__(self):
        imap = self._imap
        if self._duration is None:
            timeout = None
        else:
            timeout = self._deadline - time.monotonic()
        typ, data = self._pop(timeout)
        if not typ:
            if __debug__ and imap.debug >= 4:
                imap._mesg('idle iterator exhausted')
            raise StopIteration
        return (typ, data)

    def 批量读取(self, interval=0.1):
        """Yield a burst of responses no more than 'interval' seconds apart.

        with M.idle() as idler:
            # get a response and any others following by < 0.1 seconds
            batch = list(idler.burst())
            print(f'processing {len(batch)} responses...')
            print(batch)

        Note: This generator requires a socket connection (not IMAP4_stream).
        """
        if not self._imap.sock:
            raise self._imap.error('burst() requires a socket connection')
        try:
            yield next(self)
        except StopIteration:
            return
        while (响应 := self._pop(interval, None)):
            yield 响应
_装类转发(空闲器, {'burst': '批量读取'}, {'burst': '批量读取'})
if 支持SSL:

    class IMAP4安全客户端(IMAP4客户端):
        """IMAP4 client class over SSL connection

        Instantiate with: IMAP4_SSL([host[, port[, ssl_context[, timeout=None]]]])

                host - host's name (default: localhost);
                port - port number (default: standard IMAP4 SSL port);
                ssl_context - a SSLContext object that contains your certificate chain
                              and private key (default: None)
                timeout - socket timeout (default: None) If timeout is not given or is None,
                          the global default socket timeout is used

        for more documentation see the docstring of the parent class IMAP4.
        """

        def __init__(self, host='', port=IMAP4安全端口, *, ssl_context=None, timeout=None):
            if ssl_context is None:
                ssl_context = ssl._create_stdlib_context()
            self.ssl_context = ssl_context
            IMAP4客户端.__init__(self, host, port, timeout)

        def _create_socket(self, timeout):
            sock = IMAP4客户端._create_socket(self, timeout)
            return self.ssl_context.wrap_socket(sock, server_hostname=self.host)

        def open(self, host='', port=IMAP4安全端口, timeout=None):
            """Setup connection to remote server on "host:port".
                (default: localhost:standard IMAP4 SSL port).
            This connection will be used by the routines:
                read, readline, send, shutdown.
            """
            IMAP4客户端.open(self, host, port, timeout)
    __all__.append('IMAP4_SSL')

class IMAP4管道客户端(IMAP4客户端):
    """IMAP4 client class over a stream

    Instantiate with: IMAP4_stream(command)

            "command" - a string that can be passed to subprocess.Popen()

    for more documentation see the docstring of the parent class IMAP4.
    """

    def __init__(self, command):
        self.command = command
        IMAP4客户端.__init__(self)

    def open(self, host=None, port=None, timeout=None):
        """Setup a stream connection.
        This connection will be used by the routines:
            read, readline, send, shutdown.
        """
        self.host = None
        self.port = None
        self.sock = None
        self._file = None
        self.process = subprocess.Popen(self.command, bufsize=DEFAULT_BUFFER_SIZE, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True, close_fds=True)
        self.writefile = self.process.stdin
        self.readfile = self.process.stdout

    def read(self, size):
        """Read 'size' bytes from remote."""
        return self.readfile.read(size)

    def readline(self):
        """Read line from remote."""
        return self.readfile.readline()

    def send(self, data):
        """Send data to remote."""
        self.writefile.write(data)
        self.writefile.flush()

    def 关闭连接(self):
        """Close I/O established in "open"."""
        self.readfile.close()
        self.writefile.close()
        self.process.wait()
_装类转发(IMAP4管道客户端, {'shutdown': '关闭连接'}, {'shutdown': '关闭连接'})

class _Authenticator:
    """Private class to provide en/decoding
            for base64-based authentication conversation.
    """

    def __init__(self, mechinst):
        self.mech = mechinst

    def process(self, data):
        ret = self.mech(self.decode(data))
        if ret is None:
            return b'*'
        return self.encode(ret)

    def encode(self, inp):
        oup = b''
        if isinstance(inp, str):
            inp = inp.encode('utf-8')
        while inp:
            if len(inp) > 48:
                t = inp[:48]
                inp = inp[48:]
            else:
                t = inp
                inp = b''
            e = binascii.b2a_base64(t)
            if e:
                oup = oup + e[:-1]
        return oup

    def decode(self, inp):
        if not inp:
            return b''
        return binascii.a2b_base64(inp)
月份 = ' Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split(' ')
月转数字 = {s.encode(): n + 1 for n, s in enumerate(月份[1:])}

def 内部日期转元组(resp):
    """Parse an IMAP4 INTERNALDATE string.

    Return corresponding local time.  The return value is a
    time.struct_time tuple or None if the string has wrong format.
    """
    mo = 内部日期.match(resp)
    if not mo:
        return None
    mon = 月转数字[mo.group('mon')]
    zonen = mo.group('zonen')
    day = int(mo.group('day'))
    year = int(mo.group('year'))
    hour = int(mo.group('hour'))
    min = int(mo.group('min'))
    sec = int(mo.group('sec'))
    zoneh = int(mo.group('zoneh'))
    zonem = int(mo.group('zonem'))
    zone = (zoneh * 60 + zonem) * 60
    if zonen == b'-':
        zone = -zone
    tt = (year, mon, day, hour, min, sec, -1, -1, -1)
    utc = calendar.timegm(tt) - zone
    return time.localtime(utc)

def 整数转AP(num):
    """Convert integer to A-P string representation."""
    val = b''
    AP = b'ABCDEFGHIJKLMNOP'
    num = int(abs(num))
    while num:
        num, mod = divmod(num, 16)
        val = AP[mod:mod + 1] + val
    return val

def 解析标志(resp):
    """Convert IMAP4 flags response to python tuple."""
    mo = 标志.match(resp)
    if not mo:
        return ()
    return tuple(mo.group('flags').split())

def 时间转内部日期(date_time):
    """Convert date_time to IMAP4 INTERNALDATE representation.

    Return string in form: '"DD-Mmm-YYYY HH:MM:SS +HHMM"'.  The
    date_time argument can be a number (int or float) representing
    seconds since epoch (as returned by time.time()), a 9-tuple
    representing local time, an instance of time.struct_time (as
    returned by time.localtime()), an aware datetime instance or a
    double-quoted string.  In the last case, it is assumed to already
    be in the correct format.
    """
    if isinstance(date_time, (int, float)):
        dt = datetime.fromtimestamp(date_time, timezone.utc).astimezone()
    elif isinstance(date_time, tuple):
        gmtoff = getattr(date_time, 'tm_gmtoff', None)
        if gmtoff is None:
            if time.daylight:
                dst = date_time[8]
                if dst == -1:
                    dst = time.localtime(time.mktime(date_time))[8]
                gmtoff = -(time.timezone, time.altzone)[dst]
            else:
                gmtoff = -time.timezone
        delta = timedelta(seconds=gmtoff)
        dt = datetime(*date_time[:6], tzinfo=timezone(delta))
    elif isinstance(date_time, datetime):
        if date_time.tzinfo is None:
            raise ValueError('date_time must be aware')
        dt = date_time
    elif isinstance(date_time, str) and (date_time[0], date_time[-1]) == ('"', '"'):
        return date_time
    else:
        raise ValueError('date_time not of a known type')
    fmt = '"%d-{}-%Y %H:%M:%S %z"'.format(月份[dt.month])
    return dt.strftime(fmt)
if __name__ == '__main__':
    import getopt, getpass
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'd:s:')
    except getopt.error as val:
        optlist, args = ((), ())
    stream_command = None
    for opt, val in optlist:
        if opt == '-d':
            Debug = int(val)
        elif opt == '-s':
            stream_command = val
            if not args:
                args = (stream_command,)
    if not args:
        args = ('',)
    host = args[0]
    USER = getpass.getuser()
    PASSWD = getpass.getpass('IMAP password for %s on %s: ' % (USER, host or 'localhost'))
    test_mesg = 'From: %(user)s@localhost%(lf)sSubject: IMAP4 test%(lf)s%(lf)sdata...%(lf)s' % {'user': USER, 'lf': '\n'}
    test_seq1 = (('login', (USER, PASSWD)), ('create', ('/tmp/xxx 1',)), ('rename', ('/tmp/xxx 1', '/tmp/yyy')), ('CREATE', ('/tmp/yyz 2',)), ('append', ('/tmp/yyz 2', None, None, test_mesg)), ('list', ('/tmp', 'yy*')), ('select', ('/tmp/yyz 2',)), ('search', (None, 'SUBJECT', 'test')), ('fetch', ('1', '(FLAGS INTERNALDATE RFC822)')), ('store', ('1', 'FLAGS', '(\\Deleted)')), ('namespace', ()), ('expunge', ()), ('recent', ()), ('close', ()))
    test_seq2 = (('select', ()), ('response', ('UIDVALIDITY',)), ('uid', ('SEARCH', 'ALL')), ('response', ('EXISTS',)), ('append', (None, None, None, test_mesg)), ('recent', ()), ('logout', ()))

    def run(cmd, args):
        M._mesg('%s %s' % (cmd, args))
        typ, dat = getattr(M, cmd)(*args)
        M._mesg('%s => %s %s' % (cmd, typ, dat))
        if typ == 'NO':
            raise dat[0]
        return dat
    try:
        if stream_command:
            M = IMAP4管道客户端(stream_command)
        else:
            M = IMAP4客户端(host)
        if M.state == 'AUTH':
            test_seq1 = test_seq1[1:]
        M._mesg('PROTOCOL_VERSION = %s' % M.PROTOCOL_VERSION)
        M._mesg('CAPABILITIES = %r' % (M.capabilities,))
        for cmd, args in test_seq1:
            run(cmd, args)
        for ml in run('list', ('/tmp/', 'yy%')):
            mo = re.match('.*"([^"]+)"$', ml)
            if mo:
                path = mo.group(1)
            else:
                path = ml.split()[-1]
            run('delete', (path,))
        for cmd, args in test_seq2:
            dat = run(cmd, args)
            if (cmd, args) != ('uid', ('SEARCH', 'ALL')):
                continue
            唯一标识 = dat[-1].split()
            if not 唯一标识:
                continue
            run('uid', ('FETCH', '%s' % 唯一标识[-1], '(FLAGS INTERNALDATE RFC822.SIZE RFC822.HEADER RFC822.TEXT)'))
        print('\nAll tests OK.')
    except:
        print('\nTests failed.')
        if not Debug:
            print('\nIf you would like to see debugging output,\ntry: %s -d5\n' % sys.argv[0])
        raise


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'AllowedVersions': '允许的版本',
    'CRLF': '回车换行',
    'Commands': '命令表',
    'Continuation': '继续响应',
    'Flags': '标志',
    'HAVE_SSL': '支持SSL',
    'IMAP4': 'IMAP4客户端',
    'IMAP4_PORT': 'IMAP4端口',
    'IMAP4_SSL': 'IMAP4安全客户端',
    'IMAP4_SSL_PORT': 'IMAP4安全端口',
    'IMAP4_stream': 'IMAP4管道客户端',
    'Idler': '空闲器',
    'Int2AP': '整数转AP',
    'InternalDate': '内部日期',
    'Internaldate2tuple': '内部日期转元组',
    'Literal': '字面量',
    'MapCRLF': '映射回车换行',
    'Mon2num': '月转数字',
    'Months': '月份',
    'ParseFlags': '解析标志',
    'Response_code': '响应码',
    'Time2Internaldate': '时间转内部日期',
    'Untagged_response': '无标签响应',
    'Untagged_status': '无标签状态',
    'uid': '唯一标识',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'IMAP4客户端': {
        'authenticate': '认证',
        'capability': '能力',
        'check': '检查',
        'create': '创建',
        'delete': '删除信箱',
        'deleteacl': '删ACL',
        'enable': '启用',
        'expunge': '彻底删除',
        'fetch': '取邮件',
        'getacl': '取ACL',
        'getannotation': '取注解',
        'getquota': '取配额',
        'getquotaroot': '取配额根',
        'idle': '空闲等待',
        'login': '登录',
        'login_cram_md5': 'CRAMMD5登录',
        'logout': '登出',
        'lsub': '列订阅',
        'myrights': '我的权限',
        'namespace': '命名空间',
        'noop': '空操作',
        'partial': '部分取',
        'print_log': '打印日志',
        'proxyauth': '代理认证',
        'recent': '最近',
        'rename': '重命名',
        'response': '响应',
        'search': '搜索',
        'select': '选择信箱',
        'setacl': '设ACL',
        'setannotation': '设注解',
        'setquota': '设配额',
        'shutdown': '关闭连接',
        'starttls': '启动TLS',
        'status': '取状态',
        'store': '存储',
        'subscribe': '订阅',
        'thread': '线索搜索',
        'uid': '唯一标识',
        'unselect': '取消选择',
        'unsubscribe': '退订',
        'xatom': 'X原子',
    },
    'IMAP4管道客户端': {
        'shutdown': '关闭连接',
    },
    '空闲器': {
        'burst': '批量读取',
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
    'IMAP4客户端': {
        'Literal': '字面量',
        'Untagged_status': '无标签状态',
        'abort': '中止',
        'authenticate': '认证',
        'capability': '能力',
        'check': '检查',
        'create': '创建',
        'delete': '删除信箱',
        'deleteacl': '删ACL',
        'enable': '启用',
        'error': '错误',
        'expunge': '彻底删除',
        'fetch': '取邮件',
        'getacl': '取ACL',
        'getannotation': '取注解',
        'getquota': '取配额',
        'getquotaroot': '取配额根',
        'idle': '空闲等待',
        'login': '登录',
        'login_cram_md5': 'CRAMMD5登录',
        'logout': '登出',
        'lsub': '列订阅',
        'myrights': '我的权限',
        'namespace': '命名空间',
        'noop': '空操作',
        'partial': '部分取',
        'print_log': '打印日志',
        'proxyauth': '代理认证',
        'readonly': '只读',
        'recent': '最近',
        'rename': '重命名',
        'response': '响应',
        'search': '搜索',
        'select': '选择信箱',
        'setacl': '设ACL',
        'setannotation': '设注解',
        'setquota': '设配额',
        'shutdown': '关闭连接',
        'starttls': '启动TLS',
        'status': '取状态',
        'store': '存储',
        'subscribe': '订阅',
        'thread': '线索搜索',
        'uid': '唯一标识',
        'unselect': '取消选择',
        'unsubscribe': '退订',
        'xatom': 'X原子',
    },
    'IMAP4管道客户端': {
        'shutdown': '关闭连接',
    },
    '空闲器': {
        'burst': '批量读取',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'IMAP4安全客户端',
    'IMAP4客户端',
    'IMAP4管道客户端',
    '内部日期转元组',
    '整数转AP',
    '时间转内部日期',
    '解析标志',
])

# ---- 转发层结束 ----
