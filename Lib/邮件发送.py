# -*- coding: utf-8 -*-
"""邮件发送 —— 汉语库（由 tools/汉化库.py 从 Lib/smtplib.py 机械生成，**不要手改**）。

英文库 Lib/smtplib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py 邮件发送
"""


"""SMTP/ESMTP client class.

This should follow RFC 821 (SMTP), RFC 1869 (ESMTP), RFC 2554 (SMTP
Authentication) and RFC 2487 (Secure SMTP over TLS).

Notes:

Please remember, when doing ESMTP, that the names of the SMTP service
extensions are NOT the same thing as the option keywords for the RCPT
and MAIL commands!

Example:

  >>> import smtplib
  >>> s=smtplib.SMTP("localhost")
  >>> print(s.help())
  This is Sendmail version 8.8.4
  Topics:
      HELO    EHLO    MAIL    RCPT    DATA
      RSET    NOOP    QUIT    HELP    VRFY
      EXPN    VERB    ETRN    DSN
  For more info use "HELP <topic>".
  To report bugs in the implementation send email to
      sendmail-bugs@sendmail.org.
  For local information send email to Postmaster at your site.
  End of HELP info
  >>> s.putcmd("vrfy","someone@here")
  >>> s.getreply()
  (250, "Somebody OverHere <somebody@here.my.org>")
  >>> s.quit()
"""
_英文原名表 = {'CRLF': '回车换行', 'LMTP': 'LMTP客户端', 'LMTP_PORT': 'LMTP端口', 'OLDSTYLE_AUTH': '旧式认证', 'SMTP': 'SMTP客户端', 'SMTPAuthenticationError': 'SMTP认证错误', 'SMTPConnectError': 'SMTP连接错误', 'SMTPDataError': 'SMTP数据错误', 'SMTPException': 'SMTP异常', 'SMTPHeloError': 'SMTP问候错误', 'SMTPNotSupportedError': 'SMTP不支持错误', 'SMTPRecipientsRefused': 'SMTP收件人被拒', 'SMTPResponseException': 'SMTP响应异常', 'SMTPSenderRefused': 'SMTP发件人被拒', 'SMTPServerDisconnected': 'SMTP服务器断开', 'SMTP_PORT': 'SMTP端口', 'SMTP_SSL': 'SMTP安全客户端', 'SMTP_SSL_PORT': 'SMTP安全端口', 'bCRLF': '字节回车换行', 'quoteaddr': '引用地址', 'quotedata': '引用数据'}

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
import socket
import io
import re
import email.utils
import email.message
import email.generator
import base64
import hmac
import copy
import datetime
import sys
from email.base64mime import body_encode as encode_base64
__all__ = ['SMTPException', 'SMTPNotSupportedError', 'SMTPServerDisconnected', 'SMTPResponseException', 'SMTPSenderRefused', 'SMTPRecipientsRefused', 'SMTPDataError', 'SMTPConnectError', 'SMTPHeloError', 'SMTPAuthenticationError', 'quoteaddr', 'quotedata', 'SMTP']
SMTP端口 = 25
SMTP安全端口 = 465
回车换行 = '\r\n'
字节回车换行 = b'\r\n'
_MAXLINE = 8192
_MAXCHALLENGE = 5
旧式认证 = re.compile('auth=(.*)', re.I)

class SMTP异常(OSError):
    """Base class for all exceptions raised by this module."""

class SMTP不支持错误(SMTP异常):
    """The command or option is not supported by the SMTP server.

    This exception is raised when an attempt is made to run a command or a
    command with an option which is not supported by the server.
    """

class SMTP服务器断开(SMTP异常):
    """Not connected to any SMTP server.

    This exception is raised when the server unexpectedly disconnects,
    or when an attempt is made to use the SMTP instance before
    connecting it to a server.
    """

class SMTP响应异常(SMTP异常):
    """Base class for all exceptions that include an SMTP error code.

    These exceptions are generated in some instances when the SMTP
    server returns an error code.  The error code is stored in the
    `smtp_code' attribute of the error, and the `smtp_error' attribute
    is set to the error message.
    """

    def __init__(self, code, msg):
        self.smtp_code = code
        self.smtp_error = msg
        self.args = (code, msg)

class SMTP发件人被拒(SMTP响应异常):
    """Sender address refused.

    In addition to the attributes set by on all SMTPResponseException
    exceptions, this sets 'sender' to the string that the SMTP refused.
    """

    def __init__(self, code, msg, sender):
        self.smtp_code = code
        self.smtp_error = msg
        self.sender = sender
        self.args = (code, msg, sender)

class SMTP收件人被拒(SMTP异常):
    """All recipient addresses refused.

    The errors for each recipient are accessible through the attribute
    'recipients', which is a dictionary of exactly the same sort as
    SMTP.sendmail() returns.
    """

    def __init__(self, recipients):
        self.recipients = recipients
        self.args = (recipients,)

class SMTP数据错误(SMTP响应异常):
    """The SMTP server didn't accept the data."""

class SMTP连接错误(SMTP响应异常):
    """Error during connection establishment."""

class SMTP问候错误(SMTP响应异常):
    """The server refused our HELO reply."""

class SMTP认证错误(SMTP响应异常):
    """Authentication error.

    Most probably the server didn't accept the username/password
    combination provided.
    """

def 引用地址(addrstring):
    """Quote a subset of the email addresses defined by RFC 821.

    Should be able to handle anything email.utils.parseaddr can handle.
    """
    displayname, addr = email.utils.parseaddr(addrstring)
    if (displayname, addr) == ('', ''):
        if addrstring.strip().startswith('<'):
            return addrstring
        return '<%s>' % addrstring
    return '<%s>' % addr

def _addr_only(addrstring):
    displayname, addr = email.utils.parseaddr(addrstring)
    if (displayname, addr) == ('', ''):
        return addrstring
    return addr

def 引用数据(data):
    """Quote data for email.

    Double leading '.', and change Unix newline '\\n', or Mac '\\r' into
    internet CRLF end-of-line.
    """
    return re.sub('(?m)^\\.', '..', re.sub('(?:\\r\\n|\\n|\\r(?!\\n))', 回车换行, data))

def _quote_periods(bindata):
    return re.sub(b'(?m)^\\.', b'..', bindata)

def _fix_eols(data):
    return re.sub('(?:\\r\\n|\\n|\\r(?!\\n))', 回车换行, data)
try:
    hmac.digest(b'', b'', 'md5')
except ValueError:
    _have_cram_md5_support = False
else:
    _have_cram_md5_support = True
try:
    import ssl
except ImportError:
    _have_ssl = False
else:
    _have_ssl = True

class SMTP客户端:
    """This class manages a connection to an SMTP or ESMTP server.
    SMTP Objects:
        SMTP objects have the following attributes:
            helo_resp
                This is the message given by the server in response to the
                most recent HELO command.

            ehlo_resp
                This is the message given by the server in response to the
                most recent EHLO command. This is usually multiline.

            does_esmtp
                This is a True value _after you do an EHLO command_, if the
                server supports ESMTP.

            esmtp_features
                This is a dictionary, which, if the server supports ESMTP,
                will _after you do an EHLO command_, contain the names of the
                SMTP service extensions this server supports, and their
                parameters (if any).

                Note, all extension names are mapped to lower case in the
                dictionary.

        See each method's docstrings for details.  In general, there is a
        method of the same name to perform each SMTP command.  There is also a
        method called 'sendmail' that will do an entire mail transaction.
        """
    debuglevel = 0
    sock = None
    file = None
    helo_resp = None
    ehlo_msg = 'ehlo'
    ehlo_resp = None
    does_esmtp = False
    default_port = SMTP端口

    def __init__(self, host='', port=0, local_hostname=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None):
        """Initialize a new instance.

        If specified, `host` is the name of the remote host to which to
        connect.  If specified, `port` specifies the port to which to connect.
        By default, smtplib.SMTP_PORT is used.  If a host is specified the
        connect method is called, and if it returns anything other than a
        success code an SMTPConnectError is raised.  If specified,
        `local_hostname` is used as the FQDN of the local host in the HELO/EHLO
        command.  Otherwise, the local hostname is found using
        socket.getfqdn(). The `source_address` parameter takes a 2-tuple (host,
        port) for the socket to bind to as its source address before
        connecting. If the host is '' and port is 0, the OS default behavior
        will be used.

        """
        self.timeout = timeout
        self.esmtp_features = {}
        self.command_encoding = 'ascii'
        self.source_address = source_address
        self._auth_challenge_count = 0
        if host:
            code, msg = self.连接(host, port)
            if code != 220:
                self.close()
                raise SMTP连接错误(code, msg)
        if local_hostname is not None:
            self.local_hostname = local_hostname
        else:
            fqdn = socket.getfqdn()
            if '.' in fqdn:
                self.local_hostname = fqdn
            else:
                addr = '127.0.0.1'
                try:
                    addr = socket.gethostbyname(socket.gethostname())
                except socket.gaierror:
                    pass
                self.local_hostname = '[%s]' % addr

    def __enter__(self):
        return self

    def __exit__(self, *args):
        try:
            code, message = self.执行命令('QUIT')
            if code != 221:
                raise SMTP响应异常(code, message)
        except SMTP服务器断开:
            pass
        finally:
            self.close()

    def 设调试级别(self, debuglevel):
        """Set the debug output level.

        A non-false value results in debug messages for connection and for all
        messages sent to and received from the server.

        """
        self.debuglevel = debuglevel

    def _print_debug(self, *args):
        if self.debuglevel > 1:
            print(datetime.datetime.now().time(), *args, file=sys.stderr)
        else:
            print(*args, file=sys.stderr)

    def _get_socket(self, host, port, timeout):
        if timeout is not None and (not timeout):
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        if self.debuglevel > 0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socket.create_connection((host, port), timeout, self.source_address)

    def 连接(self, host='localhost', port=0, source_address=None):
        """Connect to a host on a given port.

        If the hostname ends with a colon (':') followed by a number, and
        there is no port specified, that suffix will be stripped off and the
        number interpreted as the port number to use.

        Note: This method is automatically invoked by __init__, if a host is
        specified during instantiation.

        """
        if source_address:
            self.source_address = source_address
        if not port and host.find(':') == host.rfind(':'):
            i = host.rfind(':')
            if i >= 0:
                host, port = (host[:i], host[i + 1:])
                try:
                    port = int(port)
                except ValueError:
                    raise OSError('nonnumeric port')
        self._host = host
        if not port:
            port = self.default_port
        sys.audit('smtplib.connect', self, host, port)
        self.sock = self._get_socket(host, port, self.timeout)
        self.file = None
        code, msg = self.取响应()
        if self.debuglevel > 0:
            self._print_debug('connect:', repr(msg))
        return (code, msg)

    def send(self, s):
        """Send 's' to the server."""
        if self.debuglevel > 0:
            self._print_debug('send:', repr(s))
        if self.sock:
            if isinstance(s, str):
                s = s.encode(self.command_encoding)
            sys.audit('smtplib.send', self, s)
            try:
                self.sock.sendall(s)
            except OSError:
                self.close()
                raise SMTP服务器断开('Server not connected')
        else:
            raise SMTP服务器断开('please run connect() first')

    def 发送命令(self, cmd, args=''):
        """Send a command to the server."""
        if args == '':
            s = cmd
        else:
            s = f'{cmd} {args}'
        if '\r' in s or '\n' in s:
            s = s.replace('\n', '\\n').replace('\r', '\\r')
            raise ValueError(f'command and arguments contain prohibited newline characters: {s}')
        self.send(f'{s}{回车换行}')

    def 取响应(self):
        """Get a reply from the server.

        Returns a tuple consisting of:

          - server response code (e.g. '250', or such, if all goes well)
            Note: returns -1 if it can't read response code.

          - server response string corresponding to response code (multiline
            responses are converted to a single, multiline string).

        Raises SMTPServerDisconnected if end-of-file is reached.
        """
        resp = []
        if self.file is None:
            self.file = self.sock.makefile('rb')
        while 1:
            try:
                line = self.file.readline(_MAXLINE + 1)
            except OSError as e:
                self.close()
                raise SMTP服务器断开('Connection unexpectedly closed: ' + str(e))
            if not line:
                self.close()
                raise SMTP服务器断开('Connection unexpectedly closed')
            if self.debuglevel > 0:
                self._print_debug('reply:', repr(line))
            if len(line) > _MAXLINE:
                self.close()
                raise SMTP响应异常(500, 'Line too long.')
            resp.append(line[4:].strip(b' \t\r\n'))
            code = line[:3]
            try:
                errcode = int(code)
            except ValueError:
                errcode = -1
                break
            if line[3:4] != b'-':
                break
        errmsg = b'\n'.join(resp)
        if self.debuglevel > 0:
            self._print_debug('reply: retcode (%s); Msg: %a' % (errcode, errmsg))
        return (errcode, errmsg)

    def 执行命令(self, cmd, args=''):
        """Send a command, and return its response code."""
        self.发送命令(cmd, args)
        return self.取响应()

    def 问候(self, name=''):
        """SMTP 'helo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        """
        self.发送命令('helo', name or self.local_hostname)
        code, msg = self.取响应()
        self.helo_resp = msg
        return (code, msg)

    def 扩展问候(self, name=''):
        """ SMTP 'ehlo' command.
        Hostname to send for this command defaults to the FQDN of the local
        host.
        """
        self.esmtp_features = {}
        self.发送命令(self.ehlo_msg, name or self.local_hostname)
        code, msg = self.取响应()
        if code == -1 and len(msg) == 0:
            self.close()
            raise SMTP服务器断开('Server not connected')
        self.ehlo_resp = msg
        if code != 250:
            return (code, msg)
        self.does_esmtp = True
        assert isinstance(self.ehlo_resp, bytes), repr(self.ehlo_resp)
        resp = self.ehlo_resp.decode('latin-1').split('\n')
        del resp[0]
        for each in resp:
            auth_match = 旧式认证.match(each)
            if auth_match:
                self.esmtp_features['auth'] = self.esmtp_features.get('auth', '') + ' ' + auth_match.groups(0)[0]
                continue
            m = re.match('(?P<feature>[A-Za-z0-9][A-Za-z0-9\\-]*) ?', each)
            if m:
                feature = m.group('feature').lower()
                params = m.string[m.end('feature'):].strip()
                if feature == 'auth':
                    self.esmtp_features[feature] = self.esmtp_features.get(feature, '') + ' ' + params
                else:
                    self.esmtp_features[feature] = params
        return (code, msg)

    def 有扩展吗(self, opt):
        """Does the server support a given SMTP service extension?"""
        return opt.lower() in self.esmtp_features

    def help(self, args=''):
        """SMTP 'help' command.
        Returns help text from server."""
        self.发送命令('help', args)
        return self.取响应()[1]

    def 重置会话(self):
        """SMTP 'rset' command -- resets session."""
        self.command_encoding = 'ascii'
        return self.执行命令('rset')

    def _rset(self):
        """Internal 'rset' command which ignores any SMTPServerDisconnected error.

        Used internally in the library, since the server disconnected error
        should appear to the application when the *next* command is issued, if
        we are doing an internal "safety" reset.
        """
        try:
            self.重置会话()
        except SMTP服务器断开:
            pass

    def 空操作(self):
        """SMTP 'noop' command -- doesn't do anything :>"""
        return self.执行命令('noop')

    def 发件人(self, sender, options=()):
        """SMTP 'mail' command -- begins mail xfer session.

        This method may raise the following exceptions:

         SMTPNotSupportedError  The options parameter includes 'SMTPUTF8'
                                but the SMTPUTF8 extension is not supported by
                                the server.
        """
        optionlist = ''
        if options and self.does_esmtp:
            if any((x.lower() == 'smtputf8' for x in options)):
                if self.有扩展吗('smtputf8'):
                    self.command_encoding = 'utf-8'
                else:
                    raise SMTP不支持错误('SMTPUTF8 not supported by server')
            optionlist = ' ' + ' '.join(options)
        self.发送命令('mail', 'from:%s%s' % (引用地址(sender), optionlist))
        return self.取响应()

    def 收件人(self, recip, options=()):
        """SMTP 'rcpt' command -- indicates 1 recipient for this mail."""
        optionlist = ''
        if options and self.does_esmtp:
            optionlist = ' ' + ' '.join(options)
        self.发送命令('rcpt', 'to:%s%s' % (引用地址(recip), optionlist))
        return self.取响应()

    def 数据(self, msg):
        """SMTP 'DATA' command -- sends message data to server.

        Automatically quotes lines beginning with a period per rfc821.
        Raises SMTPDataError if there is an unexpected reply to the
        DATA command; the return value from this method is the final
        response code received when the all data is sent.  If msg
        is a string, lone '\\r' and '\\n' characters are converted to
        '\\r\\n' characters.  If msg is bytes, it is transmitted as is.
        """
        self.发送命令('data')
        code, repl = self.取响应()
        if self.debuglevel > 0:
            self._print_debug('data:', (code, repl))
        if code != 354:
            raise SMTP数据错误(code, repl)
        else:
            if isinstance(msg, str):
                msg = _fix_eols(msg).encode('ascii')
            q = _quote_periods(msg)
            if q[-2:] != 字节回车换行:
                q = q + 字节回车换行
            q = q + b'.' + 字节回车换行
            self.send(q)
            code, msg = self.取响应()
            if self.debuglevel > 0:
                self._print_debug('data:', (code, msg))
            return (code, msg)

    def 校验地址(self, address):
        """SMTP 'verify' command -- checks for address validity."""
        self.发送命令('vrfy', _addr_only(address))
        return self.取响应()
    vrfy = 校验地址

    def 展开邮件组(self, address):
        """SMTP 'expn' command -- expands a mailing list."""
        self.发送命令('expn', _addr_only(address))
        return self.取响应()

    def 需要时问候(self):
        """Call self.ehlo() and/or self.helo() if needed.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
        """
        if self.helo_resp is None and self.ehlo_resp is None:
            if not 200 <= self.扩展问候()[0] <= 299:
                code, resp = self.问候()
                if not 200 <= code <= 299:
                    raise SMTP问候错误(code, resp)

    def 认证(self, mechanism, authobject, *, initial_response_ok=True):
        """Authentication command - requires response processing.

        'mechanism' specifies which authentication mechanism is to
        be used - the valid values are those listed in the 'auth'
        element of 'esmtp_features'.

        'authobject' must be a callable object taking a single argument:

                data = authobject(challenge)

        It will be called to process the server's challenge response; the
        challenge argument it is passed will be a bytes.  It should return
        an ASCII string that will be base64 encoded and sent to the server.

        Keyword arguments:
            - initial_response_ok: Allow sending the RFC 4954 initial-response
              to the AUTH command, if the authentication methods supports it.
        """
        mechanism = mechanism.upper()
        initial_response = authobject() if initial_response_ok else None
        if initial_response is not None:
            response = encode_base64(initial_response.encode('ascii'), eol='')
            code, resp = self.执行命令('AUTH', mechanism + ' ' + response)
            self._auth_challenge_count = 1
        else:
            code, resp = self.执行命令('AUTH', mechanism)
            self._auth_challenge_count = 0
        while code == 334:
            self._auth_challenge_count += 1
            challenge = base64.decodebytes(resp)
            response = encode_base64(authobject(challenge).encode('ascii'), eol='')
            code, resp = self.执行命令(response)
            if self._auth_challenge_count > _MAXCHALLENGE:
                raise SMTP异常('Server AUTH mechanism infinite loop. Last response: ' + repr((code, resp)))
        if code in (235, 503):
            return (code, resp)
        raise SMTP认证错误(code, resp)

    def CRAMMD5认证(self, challenge=None):
        """ Authobject to use with CRAM-MD5 authentication. Requires self.user
        and self.password to be set."""
        if challenge is None:
            return None
        if not _have_cram_md5_support:
            raise SMTP异常('CRAM-MD5 is not supported')
        password = self.password.encode('ascii')
        authcode = hmac.HMAC(password, challenge, 'md5')
        return f'{self.user} {authcode.hexdigest()}'

    def 明文认证(self, challenge=None):
        """ Authobject to use with PLAIN authentication. Requires self.user and
        self.password to be set."""
        return '\x00%s\x00%s' % (self.user, self.password)

    def 登录认证(self, challenge=None):
        """ Authobject to use with LOGIN authentication. Requires self.user and
        self.password to be set."""
        if challenge is None or self._auth_challenge_count < 2:
            return self.user
        else:
            return self.password

    def 登录(self, user, password, *, initial_response_ok=True):
        """Log in on an SMTP server that requires authentication.

        The arguments are:
            - user:         The user name to authenticate with.
            - password:     The password for the authentication.

        Keyword arguments:
            - initial_response_ok: Allow sending the RFC 4954 initial-response
              to the AUTH command, if the authentication methods supports it.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        This method will return normally if the authentication was successful.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
         SMTPAuthenticationError  The server didn't accept the username/
                                  password combination.
         SMTPNotSupportedError    The AUTH command is not supported by the
                                  server.
         SMTPException            No suitable authentication method was
                                  found.
        """
        self.需要时问候()
        if not self.有扩展吗('auth'):
            raise SMTP不支持错误('SMTP AUTH extension not supported by server.')
        advertised_authlist = self.esmtp_features['auth'].split()
        if _have_cram_md5_support:
            preferred_auths = ['CRAM-MD5', 'PLAIN', 'LOGIN']
        else:
            preferred_auths = ['PLAIN', 'LOGIN']
        authlist = [认证 for 认证 in preferred_auths if 认证 in advertised_authlist]
        if not authlist:
            raise SMTP异常('No suitable authentication method found.')
        self.user, self.password = (user, password)
        for authmethod in authlist:
            method_name = 'auth_' + authmethod.lower().replace('-', '_')
            try:
                code, resp = self.认证(authmethod, getattr(self, method_name), initial_response_ok=initial_response_ok)
                if code in (235, 503):
                    return (code, resp)
            except SMTP认证错误 as e:
                last_exception = e
        raise last_exception

    def 启动TLS(self, *, context=None):
        """Puts the connection to the SMTP server into TLS mode.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.

        If the server supports TLS, this will encrypt the rest of the SMTP
        session. If you provide the context parameter,
        the identity of the SMTP server and client can be checked. This,
        however, depends on whether the socket module really checks the
        certificates.

        This method may raise the following exceptions:

         SMTPHeloError            The server didn't reply properly to
                                  the helo greeting.
        """
        self.需要时问候()
        if not self.有扩展吗('starttls'):
            raise SMTP不支持错误('STARTTLS extension not supported by server.')
        resp, reply = self.执行命令('STARTTLS')
        if resp == 220:
            if not _have_ssl:
                raise RuntimeError('No SSL support included in this Python')
            if context is None:
                context = ssl._create_stdlib_context()
            self.sock = context.wrap_socket(self.sock, server_hostname=self._host)
            self.file = None
            self.helo_resp = None
            self.ehlo_resp = None
            self.esmtp_features = {}
            self.does_esmtp = False
        else:
            raise SMTP响应异常(resp, reply)
        return (resp, reply)

    def 发邮件(self, from_addr, to_addrs, msg, mail_options=(), rcpt_options=()):
        """This command performs an entire mail transaction.

        The arguments are:
            - from_addr    : The address sending this mail.
            - to_addrs     : A list of addresses to send this mail to.  A bare
                             string will be treated as a list with 1 address.
            - msg          : The message to send.
            - mail_options : List of ESMTP options (such as 8bitmime) for the
                             mail command.
            - rcpt_options : List of ESMTP options (such as DSN commands) for
                             all the rcpt commands.

        msg may be a string containing characters in the ASCII range, or a byte
        string.  A string is encoded to bytes using the ascii codec, and lone
        \\r and \\n characters are converted to \\r\\n characters.

        If there has been no previous EHLO or HELO command this session, this
        method tries ESMTP EHLO first.  If the server does ESMTP, message size
        and each of the specified options will be passed to it.  If EHLO
        fails, HELO will be tried and ESMTP options suppressed.

        This method will return normally if the mail is accepted for at least
        one recipient.  It returns a dictionary, with one entry for each
        recipient that was refused.  Each entry contains a tuple of the SMTP
        error code and the accompanying error message sent by the server.

        This method may raise the following exceptions:

         SMTPHeloError          The server didn't reply properly to
                                the helo greeting.
         SMTPRecipientsRefused  The server rejected ALL recipients
                                (no mail was sent).
         SMTPSenderRefused      The server didn't accept the from_addr.
         SMTPDataError          The server replied with an unexpected
                                error code (other than a refusal of
                                a recipient).
         SMTPNotSupportedError  The mail_options parameter includes 'SMTPUTF8'
                                but the SMTPUTF8 extension is not supported by
                                the server.

        Note: the connection will be open even after an exception is raised.

        Example:

         >>> import smtplib
         >>> s=smtplib.SMTP("localhost")
         >>> tolist=["one@one.org","two@two.org","three@three.org","four@four.org"]
         >>> msg = '''\\
         ... From: Me@my.org
         ... Subject: testin'...
         ...
         ... This is a test '''
         >>> s.sendmail("me@my.org",tolist,msg)
         { "three@three.org" : ( 550 ,"User unknown" ) }
         >>> s.quit()

        In the above example, the message was accepted for delivery to three
        of the four addresses, and one was rejected, with the error code
        550.  If all addresses are accepted, then the method will return an
        empty dictionary.

        """
        self.需要时问候()
        esmtp_opts = []
        if isinstance(msg, str):
            msg = _fix_eols(msg).encode('ascii')
        if self.does_esmtp:
            if self.有扩展吗('size'):
                esmtp_opts.append('size=%d' % len(msg))
            for option in mail_options:
                esmtp_opts.append(option)
        code, resp = self.发件人(from_addr, esmtp_opts)
        if code != 250:
            if code == 421:
                self.close()
            else:
                self._rset()
            raise SMTP发件人被拒(code, resp, from_addr)
        senderrs = {}
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        for each in to_addrs:
            code, resp = self.收件人(each, rcpt_options)
            if code != 250 and code != 251:
                senderrs[each] = (code, resp)
            if code == 421:
                self.close()
                raise SMTP收件人被拒(senderrs)
        if len(senderrs) == len(to_addrs):
            self._rset()
            raise SMTP收件人被拒(senderrs)
        code, resp = self.数据(msg)
        if code != 250:
            if code == 421:
                self.close()
            else:
                self._rset()
            raise SMTP数据错误(code, resp)
        return senderrs

    def 发消息(self, msg, from_addr=None, to_addrs=None, mail_options=(), rcpt_options=()):
        """Converts message to a bytestring and passes it to sendmail.

        The arguments are as for sendmail, except that msg is an
        email.message.Message object.  If from_addr is None or to_addrs is
        None, these arguments are taken from the headers of the Message as
        described in RFC 5322 (a ValueError is raised if there is more than
        one set of 'Resent-' headers).  Regardless of the values of from_addr and
        to_addr, any Bcc field (or Resent-Bcc field, when the Message is a
        resent) of the Message object won't be transmitted.  The Message
        object is then serialized using email.generator.BytesGenerator and
        sendmail is called to transmit the message.  If the sender or any of
        the recipient addresses contain non-ASCII and the server advertises the
        SMTPUTF8 capability, the policy is cloned with utf8 set to True for the
        serialization, and SMTPUTF8 and BODY=8BITMIME are asserted on the send.
        If the server does not support SMTPUTF8, an SMTPNotSupported error is
        raised.  Otherwise the generator is called without modifying the
        policy.

        """
        self.需要时问候()
        resent = msg.get_all('Resent-Date')
        if resent is None:
            header_prefix = ''
        elif len(resent) == 1:
            header_prefix = 'Resent-'
        else:
            raise ValueError("message has more than one 'Resent-' header block")
        if from_addr is None:
            from_addr = msg[header_prefix + 'Sender'] if header_prefix + 'Sender' in msg else msg[header_prefix + 'From']
            from_addr = email.utils.getaddresses([from_addr])[0][1]
        if to_addrs is None:
            addr_fields = [f for f in (msg[header_prefix + 'To'], msg[header_prefix + 'Bcc'], msg[header_prefix + 'Cc']) if f is not None]
            to_addrs = [a[1] for a in email.utils.getaddresses(addr_fields)]
        msg_copy = copy.copy(msg)
        del msg_copy['Bcc']
        del msg_copy['Resent-Bcc']
        international = False
        try:
            ''.join([from_addr, *to_addrs]).encode('ascii')
        except UnicodeEncodeError:
            if not self.有扩展吗('smtputf8'):
                raise SMTP不支持错误('One or more source or delivery addresses require internationalized email support, but the server does not advertise the required SMTPUTF8 capability')
            international = True
        with io.BytesIO() as bytesmsg:
            if international:
                g = email.generator.BytesGenerator(bytesmsg, policy=msg.policy.clone(utf8=True))
                mail_options = (*mail_options, 'SMTPUTF8', 'BODY=8BITMIME')
            else:
                g = email.generator.BytesGenerator(bytesmsg)
            g.flatten(msg_copy, linesep='\r\n')
            flatmsg = bytesmsg.getvalue()
        return self.发邮件(from_addr, to_addrs, flatmsg, mail_options, rcpt_options)

    def close(self):
        """Close the connection to the SMTP server."""
        try:
            file = self.file
            self.file = None
            if file:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock:
                sock.close()

    def quit(self):
        """Terminate the SMTP session."""
        res = self.执行命令('quit')
        self.ehlo_resp = self.helo_resp = None
        self.esmtp_features = {}
        self.does_esmtp = False
        self.close()
        return res
_装类转发(SMTP客户端, {'auth': '认证', 'auth_cram_md5': 'CRAMMD5认证', 'auth_login': '登录认证', 'auth_plain': '明文认证', 'connect': '连接', 'data': '数据', 'docmd': '执行命令', 'ehlo': '扩展问候', 'ehlo_or_helo_if_needed': '需要时问候', 'expn': '展开邮件组', 'getreply': '取响应', 'has_extn': '有扩展吗', 'helo': '问候', 'login': '登录', 'mail': '发件人', 'noop': '空操作', 'putcmd': '发送命令', 'rcpt': '收件人', 'rset': '重置会话', 'send_message': '发消息', 'sendmail': '发邮件', 'set_debuglevel': '设调试级别', 'starttls': '启动TLS', 'verify': '校验地址'}, {'auth': '认证', 'auth_cram_md5': 'CRAMMD5认证', 'auth_login': '登录认证', 'auth_plain': '明文认证', 'connect': '连接', 'data': '数据', 'docmd': '执行命令', 'ehlo': '扩展问候', 'ehlo_or_helo_if_needed': '需要时问候', 'expn': '展开邮件组', 'getreply': '取响应', 'has_extn': '有扩展吗', 'helo': '问候', 'login': '登录', 'mail': '发件人', 'noop': '空操作', 'putcmd': '发送命令', 'rcpt': '收件人', 'rset': '重置会话', 'send_message': '发消息', 'sendmail': '发邮件', 'set_debuglevel': '设调试级别', 'starttls': '启动TLS', 'verify': '校验地址'})
if _have_ssl:

    class SMTP安全客户端(SMTP客户端):
        """ This is a subclass derived from SMTP that connects over an SSL
        encrypted socket (to use this class you need a socket module that was
        compiled with SSL support). If host is not specified, '' (the local
        host) is used. If port is omitted, the standard SMTP-over-SSL port
        (465) is used.  local_hostname and source_address have the same meaning
        as they do in the SMTP class.  context also optional, can contain a
        SSLContext.

        """
        default_port = SMTP安全端口

        def __init__(self, host='', port=0, local_hostname=None, *, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, source_address=None, context=None):
            if context is None:
                context = ssl._create_stdlib_context()
            self.context = context
            SMTP客户端.__init__(self, host, port, local_hostname, timeout, source_address)

        def _get_socket(self, host, port, timeout):
            if self.debuglevel > 0:
                self._print_debug('connect:', (host, port))
            new_socket = super()._get_socket(host, port, timeout)
            new_socket = self.context.wrap_socket(new_socket, server_hostname=self._host)
            return new_socket
    __all__.append('SMTP_SSL')
LMTP端口 = 2003

class LMTP客户端(SMTP客户端):
    """LMTP - Local Mail Transfer Protocol

    The LMTP protocol, which is very similar to ESMTP, is heavily based
    on the standard SMTP client. It's common to use Unix sockets for
    LMTP, so our connect() method must support that as well as a regular
    host:port server.  local_hostname and source_address have the same
    meaning as they do in the SMTP class.  To specify a Unix socket,
    you must use an absolute path as the host, starting with a '/'.

    Authentication is supported, using the regular SMTP mechanism. When
    using a Unix socket, LMTP generally don't support or require any
    authentication, but your mileage might vary."""
    ehlo_msg = 'lhlo'

    def __init__(self, host='', port=LMTP端口, local_hostname=None, source_address=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):
        """Initialize a new instance."""
        super().__init__(host, port, local_hostname=local_hostname, source_address=source_address, timeout=timeout)

    def 连接(self, host='localhost', port=0, source_address=None):
        """Connect to the LMTP daemon, on either a Unix or a TCP socket."""
        if host[0] != '/':
            return super().connect(host, port, source_address=source_address)
        if self.timeout is not None and (not self.timeout):
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        try:
            self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            if self.timeout is not socket._GLOBAL_DEFAULT_TIMEOUT:
                self.sock.settimeout(self.timeout)
            self.file = None
            self.sock.connect(host)
        except OSError:
            if self.debuglevel > 0:
                self._print_debug('connect fail:', host)
            if self.sock:
                self.sock.close()
            self.sock = None
            raise
        code, msg = self.取响应()
        if self.debuglevel > 0:
            self._print_debug('connect:', msg)
        return (code, msg)
_装类转发(LMTP客户端, {'connect': '连接'}, {'connect': '连接', 'getreply': '取响应'})
if __name__ == '__main__':

    def prompt(prompt):
        sys.stdout.write(prompt + ': ')
        sys.stdout.flush()
        return sys.stdin.readline().strip()
    fromaddr = prompt('From')
    toaddrs = prompt('To').split(',')
    print('Enter message, end with ^D:')
    msg = ''
    while (line := sys.stdin.readline()):
        msg = msg + line
    print('Message length is %d' % len(msg))
    server = SMTP客户端('localhost')
    server.set_debuglevel(1)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


# ============================================================================
# 英文原名转发层（照 D-024）——「同一对象两种名字」
#
# 这一段是**新加的**，不在「只改名字」的等价证明范围内。
#   * 模块级、类成员：静态别名，指向的是**同一个对象**；
#   * 实例属性：类上挂 __getattr__/__setattr__，把英文名翻成中文名。
# 有了这一层，官方自带的测试可以原样跑在本模块上（换掉 sys.modules 即可）。
# ============================================================================
_模块别名 = {
    'CRLF': '回车换行',
    'LMTP': 'LMTP客户端',
    'LMTP_PORT': 'LMTP端口',
    'OLDSTYLE_AUTH': '旧式认证',
    'SMTP': 'SMTP客户端',
    'SMTPAuthenticationError': 'SMTP认证错误',
    'SMTPConnectError': 'SMTP连接错误',
    'SMTPDataError': 'SMTP数据错误',
    'SMTPException': 'SMTP异常',
    'SMTPHeloError': 'SMTP问候错误',
    'SMTPNotSupportedError': 'SMTP不支持错误',
    'SMTPRecipientsRefused': 'SMTP收件人被拒',
    'SMTPResponseException': 'SMTP响应异常',
    'SMTPSenderRefused': 'SMTP发件人被拒',
    'SMTPServerDisconnected': 'SMTP服务器断开',
    'SMTP_PORT': 'SMTP端口',
    'SMTP_SSL': 'SMTP安全客户端',
    'SMTP_SSL_PORT': 'SMTP安全端口',
    'bCRLF': '字节回车换行',
    'quoteaddr': '引用地址',
    'quotedata': '引用数据',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'LMTP客户端': {
        'connect': '连接',
    },
    'SMTP客户端': {
        'auth': '认证',
        'auth_cram_md5': 'CRAMMD5认证',
        'auth_login': '登录认证',
        'auth_plain': '明文认证',
        'connect': '连接',
        'data': '数据',
        'docmd': '执行命令',
        'ehlo': '扩展问候',
        'ehlo_or_helo_if_needed': '需要时问候',
        'expn': '展开邮件组',
        'getreply': '取响应',
        'has_extn': '有扩展吗',
        'helo': '问候',
        'login': '登录',
        'mail': '发件人',
        'noop': '空操作',
        'putcmd': '发送命令',
        'rcpt': '收件人',
        'rset': '重置会话',
        'send_message': '发消息',
        'sendmail': '发邮件',
        'set_debuglevel': '设调试级别',
        'starttls': '启动TLS',
        'verify': '校验地址',
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
    'LMTP客户端': {
        'connect': '连接',
        'getreply': '取响应',
    },
    'SMTP客户端': {
        'auth': '认证',
        'auth_cram_md5': 'CRAMMD5认证',
        'auth_login': '登录认证',
        'auth_plain': '明文认证',
        'connect': '连接',
        'data': '数据',
        'docmd': '执行命令',
        'ehlo': '扩展问候',
        'ehlo_or_helo_if_needed': '需要时问候',
        'expn': '展开邮件组',
        'getreply': '取响应',
        'has_extn': '有扩展吗',
        'helo': '问候',
        'login': '登录',
        'mail': '发件人',
        'noop': '空操作',
        'putcmd': '发送命令',
        'rcpt': '收件人',
        'rset': '重置会话',
        'send_message': '发消息',
        'sendmail': '发邮件',
        'set_debuglevel': '设调试级别',
        'starttls': '启动TLS',
        'verify': '校验地址',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'SMTP不支持错误',
    'SMTP发件人被拒',
    'SMTP响应异常',
    'SMTP安全客户端',
    'SMTP客户端',
    'SMTP异常',
    'SMTP收件人被拒',
    'SMTP数据错误',
    'SMTP服务器断开',
    'SMTP认证错误',
    'SMTP连接错误',
    'SMTP问候错误',
    '引用地址',
    '引用数据',
])

# ---- 转发层结束 ----
