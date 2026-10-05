# -*- coding: utf-8 -*-
"""FTP传输 —— 汉语库（由 tools/汉化库.py 从 Lib/ftplib.py 机械生成，**不要手改**）。

英文库 Lib/ftplib.py 一个字节都没动。本文件分两段：
  第一段 深拷贝派生 —— 只改了名字，逻辑逐记号相同（生成时机器证明过）；
  第二段 英文原名转发层 —— 新加的，让英文原名和中文名指向**同一个对象**。

想改名字：改 tools/库词表.py，然后跑 tools/汉化库.py FTP传输
"""


"""An FTP client class and some helper functions.

Based on RFC 959: File Transfer Protocol (FTP), by J. Postel and J. Reynolds

Example:

>>> from ftplib import FTP
>>> ftp = FTP('ftp.python.org') # connect to host, default port
>>> ftp.login() # default, i.e.: user anonymous, passwd anonymous@
'230 Guest login ok, access restrictions apply.'
>>> ftp.retrlines('LIST') # list directory contents
total 9
drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 .
drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 ..
drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 bin
drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 etc
d-wxrwxr-x   2 ftp      wheel        1024 Sep  5 13:43 incoming
drwxr-xr-x   2 root     wheel        1024 Nov 17  1993 lib
drwxr-xr-x   6 1094     wheel        1024 Sep 13 19:07 pub
drwxr-xr-x   3 root     wheel        1024 Jan  3  1994 usr
-rw-r--r--   1 root     root          312 Aug  1  1994 welcome.msg
'226 Transfer complete.'
>>> ftp.quit()
'221 Goodbye.'
>>>

A nice test that reveals some of the network dialogue would be:
python ftplib.py -d localhost -l -p -l
"""
_英文原名表 = {'FTP': 'FTP客户端', 'FTP_TLS': 'FTP安全客户端', 'all_errors': '全部错误', 'error_perm': '永久错误', 'error_proto': '协议错误', 'error_reply': '应答错误', 'error_temp': '临时错误'}

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
import sys
import socket
from socket import _GLOBAL_DEFAULT_TIMEOUT
__all__ = ['FTP', 'error_reply', 'error_temp', 'error_perm', 'error_proto', 'all_errors']
MSG_OOB = 1
FTP_PORT = 21
MAXLINE = 8192

class Error(Exception):
    pass

class 应答错误(Error):
    pass

class 临时错误(Error):
    pass

class 永久错误(Error):
    pass

class 协议错误(Error):
    pass
全部错误 = (Error, OSError, EOFError)
CRLF = '\r\n'
B_CRLF = b'\r\n'

class FTP客户端:
    """An FTP client class.

    To create a connection, call the class using these arguments:
            host, user, passwd, acct, timeout, source_address, encoding

    The first four arguments are all strings, and have default value ''.
    The parameter ´timeout´ must be numeric and defaults to None if not
    passed, meaning that no timeout will be set on any ftp socket(s).
    If a timeout is passed, then this is now the default timeout for all ftp
    socket operations for this instance.
    The last parameter is the encoding of filenames, which defaults to utf-8.

    Then use self.connect() with optional host and port argument.

    To download a file, use ftp.retrlines('RETR ' + filename),
    or ftp.retrbinary() with slightly different arguments.
    To upload a file, use ftp.storlines() or ftp.storbinary(),
    which have an open file as argument (see their definitions
    below for details).
    The download/upload functions first issue appropriate TYPE
    and PORT or PASV commands.
    """
    debugging = 0
    host = ''
    port = FTP_PORT
    maxline = MAXLINE
    sock = None
    file = None
    welcome = None
    passiveserver = True
    trust_server_pasv_ipv4_address = False

    def __init__(self, host='', user='', passwd='', acct='', timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None, *, encoding='utf-8'):
        """Initialization method (called by class instantiation).
        Initialize host to localhost, port to standard ftp port.
        Optional arguments are host (for connect()),
        and user, passwd, acct (for login()).
        """
        self.encoding = encoding
        self.source_address = source_address
        self.timeout = timeout
        if host:
            self.连接(host)
            if user:
                self.登录(user, passwd, acct)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self.sock is not None:
            try:
                self.quit()
            except (OSError, EOFError):
                pass
            finally:
                if self.sock is not None:
                    self.close()

    def 连接(self, host='', port=0, timeout=-999, source_address=None):
        """Connect to host.  Arguments are:
         - host: hostname to connect to (string, default previous host)
         - port: port to connect to (integer, default previous port)
         - timeout: the timeout to set against the ftp socket(s)
         - source_address: a 2-tuple (host, port) for the socket to bind
           to as its source address before connecting.
        """
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        if self.timeout is not None and (not self.timeout):
            raise ValueError('Non-blocking socket (timeout=0) is not supported')
        if source_address is not None:
            self.source_address = source_address
        sys.audit('ftplib.connect', self, self.host, self.port)
        self.sock = socket.create_connection((self.host, self.port), self.timeout, source_address=self.source_address)
        self.af = self.sock.family
        self.file = self.sock.makefile('r', encoding=self.encoding)
        self.welcome = self.取响应()
        return self.welcome

    def 取欢迎语(self):
        """Get the welcome message from the server.
        (this is read and squirreled away by connect())"""
        if self.debugging:
            print('*welcome*', self.清洗参数(self.welcome))
        return self.welcome

    def 设调试级别(self, level):
        """Set the debugging level.
        The required argument level means:
        0: no debugging output (default)
        1: print commands and responses but not body text etc.
        2: also print raw lines read and sent before stripping CR/LF"""
        self.debugging = level
    debug = 设调试级别

    def 设被动模式(self, val):
        """Use passive or active mode for data transfers.
        With a false argument, use the normal PORT mode,
        With a true argument, use the PASV command."""
        self.passiveserver = val

    def 清洗参数(self, s):
        if s[:5] in {'pass ', 'PASS '}:
            i = len(s.rstrip('\r\n'))
            s = s[:5] + '*' * (i - 5) + s[i:]
        return repr(s)

    def 发送行(self, line):
        if '\r' in line or '\n' in line:
            raise ValueError('an illegal newline character should not be contained')
        sys.audit('ftplib.sendcmd', self, line)
        line = line + CRLF
        if self.debugging > 1:
            print('*put*', self.清洗参数(line))
        self.sock.sendall(line.encode(self.encoding))

    def 发送命令(self, line):
        if self.debugging:
            print('*cmd*', self.清洗参数(line))
        self.发送行(line)

    def 取行(self):
        line = self.file.readline(self.maxline + 1)
        if len(line) > self.maxline:
            raise Error('got more than %d bytes' % self.maxline)
        if self.debugging > 1:
            print('*get*', self.清洗参数(line))
        if not line:
            raise EOFError
        if line[-2:] == CRLF:
            line = line[:-2]
        elif line[-1:] in CRLF:
            line = line[:-1]
        return line

    def 取多行(self):
        line = self.取行()
        if line[3:4] == '-':
            code = line[:3]
            while 1:
                nextline = self.取行()
                line = line + ('\n' + nextline)
                if nextline[:3] == code and nextline[3:4] != '-':
                    break
        return line

    def 取响应(self):
        resp = self.取多行()
        if self.debugging:
            print('*resp*', self.清洗参数(resp))
        self.lastresp = resp[:3]
        c = resp[:1]
        if c in {'1', '2', '3'}:
            return resp
        if c == '4':
            raise 临时错误(resp)
        if c == '5':
            raise 永久错误(resp)
        raise 协议错误(resp)

    def 取空响应(self):
        """Expect a response beginning with '2'."""
        resp = self.取响应()
        if resp[:1] != '2':
            raise 应答错误(resp)
        return resp

    def 中止(self):
        """Abort a file transfer.  Uses out-of-band data.
        This does not follow the procedure from the RFC to send Telnet
        IP and Synch; that doesn't seem to work with the servers I've
        tried.  Instead, just send the ABOR command as OOB data."""
        line = b'ABOR' + B_CRLF
        if self.debugging > 1:
            print('*put urgent*', self.清洗参数(line))
        self.sock.sendall(line, MSG_OOB)
        resp = self.取多行()
        if resp[:3] not in {'426', '225', '226'}:
            raise 协议错误(resp)
        return resp

    def 执行命令(self, cmd):
        """Send a command and return the response."""
        self.发送命令(cmd)
        return self.取响应()

    def 发送并校验(self, cmd):
        """Send a command and expect a response beginning with '2'."""
        self.发送命令(cmd)
        return self.取空响应()

    def 发送PORT(self, host, port):
        """Send a PORT command with the current host and the given
        port number.
        """
        hbytes = host.split('.')
        pbytes = [repr(port // 256), repr(port % 256)]
        bytes = hbytes + pbytes
        cmd = 'PORT ' + ','.join(bytes)
        return self.发送并校验(cmd)

    def 发送EPRT(self, host, port):
        """Send an EPRT command with the current host and the given port number."""
        af = 0
        if self.af == socket.AF_INET:
            af = 1
        if self.af == socket.AF_INET6:
            af = 2
        if af == 0:
            raise 协议错误('unsupported address family')
        fields = ['', repr(af), host, repr(port), '']
        cmd = 'EPRT ' + '|'.join(fields)
        return self.发送并校验(cmd)

    def 建数据端口(self):
        """Create a new socket and send a PORT command for it."""
        sock = socket.create_server(('', 0), family=self.af, backlog=1)
        port = sock.getsockname()[1]
        host = self.sock.getsockname()[0]
        if self.af == socket.AF_INET:
            resp = self.发送PORT(host, port)
        else:
            resp = self.发送EPRT(host, port)
        if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
            sock.settimeout(self.timeout)
        return sock

    def 建被动端口(self):
        """Internal: Does the PASV or EPSV handshake -> (address, port)"""
        if self.af == socket.AF_INET:
            untrusted_host, port = parse227(self.执行命令('PASV'))
            if self.trust_server_pasv_ipv4_address:
                host = untrusted_host
            else:
                host = self.sock.getpeername()[0]
        else:
            host, port = parse229(self.执行命令('EPSV'), self.sock.getpeername())
        return (host, port)

    def 建传输(self, cmd, rest=None):
        """Initiate a transfer over the data connection.

        If the transfer is active, send a port command and the
        transfer command, and accept the connection.  If the server is
        passive, send a pasv command, connect to it, and start the
        transfer command.  Either way, return the socket for the
        connection and the expected size of the transfer.  The
        expected size may be None if it could not be determined.

        Optional 'rest' argument can be a string that is sent as the
        argument to a REST command.  This is essentially a server
        marker used to tell the server to skip over any data up to the
        given marker.
        """
        取大小 = None
        if self.passiveserver:
            host, port = self.建被动端口()
            conn = socket.create_connection((host, port), self.timeout, source_address=self.source_address)
            try:
                if rest is not None:
                    self.执行命令('REST %s' % rest)
                resp = self.执行命令(cmd)
                if resp[0] == '2':
                    resp = self.取响应()
                if resp[0] != '1':
                    raise 应答错误(resp)
            except:
                conn.close()
                raise
        else:
            with self.建数据端口() as sock:
                if rest is not None:
                    self.执行命令('REST %s' % rest)
                resp = self.执行命令(cmd)
                if resp[0] == '2':
                    resp = self.取响应()
                if resp[0] != '1':
                    raise 应答错误(resp)
                conn, sockaddr = sock.accept()
                if self.timeout is not _GLOBAL_DEFAULT_TIMEOUT:
                    conn.settimeout(self.timeout)
        if resp[:3] == '150':
            取大小 = parse150(resp)
        return (conn, 取大小)

    def 建传输并连接(self, cmd, rest=None):
        """Like ntransfercmd() but returns only the socket."""
        return self.建传输(cmd, rest)[0]

    def 登录(self, user='', passwd='', acct=''):
        """Login, default anonymous."""
        if not user:
            user = 'anonymous'
        if not passwd:
            passwd = ''
        if not acct:
            acct = ''
        if user == 'anonymous' and passwd in {'', '-'}:
            passwd = passwd + 'anonymous@'
        resp = self.执行命令('USER ' + user)
        if resp[0] == '3':
            resp = self.执行命令('PASS ' + passwd)
        if resp[0] == '3':
            resp = self.执行命令('ACCT ' + acct)
        if resp[0] != '2':
            raise 应答错误(resp)
        return resp

    def 取二进制(self, cmd, callback, blocksize=8192, rest=None):
        """Retrieve data in binary mode.  A new port is created for you.

        Args:
          cmd: A RETR command.
          callback: A single parameter callable to be called on each
                    block of data read.
          blocksize: The maximum number of bytes to read from the
                     socket at one time.  [default: 8192]
          rest: Passed to transfercmd().  [default: None]

        Returns:
          The response code.
        """
        self.发送并校验('TYPE I')
        with self.建传输并连接(cmd, rest) as conn:
            while (data := conn.recv(blocksize)):
                callback(data)
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                conn.unwrap()
        return self.取空响应()

    def 取文本行(self, cmd, callback=None):
        """Retrieve data in line mode.  A new port is created for you.

        Args:
          cmd: A RETR, LIST, or NLST command.
          callback: An optional single parameter callable that is called
                    for each line with the trailing CRLF stripped.
                    [default: print_line()]

        Returns:
          The response code.
        """
        if callback is None:
            callback = print_line
        resp = self.执行命令('TYPE A')
        with self.建传输并连接(cmd) as conn, conn.makefile('r', encoding=self.encoding) as fp:
            while 1:
                line = fp.readline(self.maxline + 1)
                if len(line) > self.maxline:
                    raise Error('got more than %d bytes' % self.maxline)
                if self.debugging > 2:
                    print('*retr*', repr(line))
                if not line:
                    break
                if line[-2:] == CRLF:
                    line = line[:-2]
                elif line[-1:] == '\n':
                    line = line[:-1]
                callback(line)
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                conn.unwrap()
        return self.取空响应()

    def 存二进制(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        """Store a file in binary mode.  A new port is created for you.

        Args:
          cmd: A STOR command.
          fp: A file-like object with a read(num_bytes) method.
          blocksize: The maximum data size to read from fp and send over
                     the connection at once.  [default: 8192]
          callback: An optional single parameter callable that is called on
                    each block of data after it is sent.  [default: None]
          rest: Passed to transfercmd().  [default: None]

        Returns:
          The response code.
        """
        self.发送并校验('TYPE I')
        with self.建传输并连接(cmd, rest) as conn:
            while (buf := fp.read(blocksize)):
                conn.sendall(buf)
                if callback:
                    callback(buf)
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                conn.unwrap()
        return self.取空响应()

    def 存文本行(self, cmd, fp, callback=None):
        """Store a file in line mode.  A new port is created for you.

        Args:
          cmd: A STOR command.
          fp: A file-like object with a readline() method.
          callback: An optional single parameter callable that is called on
                    each line after it is sent.  [default: None]

        Returns:
          The response code.
        """
        self.发送并校验('TYPE A')
        with self.建传输并连接(cmd) as conn:
            while 1:
                buf = fp.readline(self.maxline + 1)
                if len(buf) > self.maxline:
                    raise Error('got more than %d bytes' % self.maxline)
                if not buf:
                    break
                if buf[-2:] != B_CRLF:
                    if buf[-1] in B_CRLF:
                        buf = buf[:-1]
                    buf = buf + B_CRLF
                conn.sendall(buf)
                if callback:
                    callback(buf)
            if _SSLSocket is not None and isinstance(conn, _SSLSocket):
                conn.unwrap()
        return self.取空响应()

    def 账号(self, password):
        """Send new account name."""
        cmd = 'ACCT ' + password
        return self.发送并校验(cmd)

    def 列名字(self, *args):
        """Return a list of files in a given directory (default the current)."""
        cmd = 'NLST'
        for arg in args:
            cmd = cmd + (' ' + arg)
        files = []
        self.取文本行(cmd, files.append)
        return files

    def dir(self, *args):
        """List a directory in long form.
        By default list current directory to stdout.
        Optional last argument is callback function; all
        non-empty arguments before it are concatenated to the
        LIST command.  (This *should* only be used for a pathname.)"""
        cmd = 'LIST'
        func = None
        if args[-1:] and (not isinstance(args[-1], str)):
            args, func = (args[:-1], args[-1])
        for arg in args:
            if arg:
                cmd = cmd + (' ' + arg)
        self.取文本行(cmd, func)

    def 列机器目录(self, path='', facts=[]):
        """List a directory in a standardized format by using MLSD
        command (RFC-3659). If path is omitted the current directory
        is assumed. "facts" is a list of strings representing the type
        of information desired (e.g. ["type", "size", "perm"]).

        Return a generator object yielding a tuple of two elements
        for every file found in path.
        First element is the file name, the second one is a dictionary
        including a variable number of "facts" depending on the server
        and whether "facts" argument has been provided.
        """
        if facts:
            self.执行命令('OPTS MLST ' + ';'.join(facts) + ';')
        if path:
            cmd = 'MLSD %s' % path
        else:
            cmd = 'MLSD'
        lines = []
        self.取文本行(cmd, lines.append)
        for line in lines:
            facts_found, _, name = line.rstrip(CRLF).partition(' ')
            entry = {}
            for fact in facts_found[:-1].split(';'):
                key, _, value = fact.partition('=')
                entry[key.lower()] = value
            yield (name, entry)

    def 重命名(self, fromname, toname):
        """Rename a file."""
        resp = self.执行命令('RNFR ' + fromname)
        if resp[0] != '3':
            raise 应答错误(resp)
        return self.发送并校验('RNTO ' + toname)

    def 删除文件(self, filename):
        """Delete a file."""
        resp = self.执行命令('DELE ' + filename)
        if resp[:3] in {'250', '200'}:
            return resp
        else:
            raise 应答错误(resp)

    def 切换目录(self, dirname):
        """Change to a directory."""
        if dirname == '..':
            try:
                return self.发送并校验('CDUP')
            except 永久错误 as msg:
                if msg.args[0][:3] != '500':
                    raise
        elif dirname == '':
            dirname = '.'
        cmd = 'CWD ' + dirname
        return self.发送并校验(cmd)

    def 取大小(self, filename):
        """Retrieve the size of a file."""
        resp = self.执行命令('SIZE ' + filename)
        if resp[:3] == '213':
            s = resp[3:].strip()
            return int(s)

    def 建目录(self, dirname):
        """Make a directory, return its full pathname."""
        resp = self.发送并校验('MKD ' + dirname)
        if not resp.startswith('257'):
            return ''
        return parse257(resp)

    def 删目录(self, dirname):
        """Remove a directory."""
        return self.发送并校验('RMD ' + dirname)

    def 取当前目录(self):
        """Return current working directory."""
        resp = self.发送并校验('PWD')
        if not resp.startswith('257'):
            return ''
        return parse257(resp)

    def quit(self):
        """Quit, and close the connection."""
        resp = self.发送并校验('QUIT')
        self.close()
        return resp

    def close(self):
        """Close the connection without assuming anything about it."""
        try:
            file = self.file
            self.file = None
            if file is not None:
                file.close()
        finally:
            sock = self.sock
            self.sock = None
            if sock is not None:
                sock.close()
_装类转发(FTP客户端, {'abort': '中止', 'acct': '账号', 'connect': '连接', 'cwd': '切换目录', 'delete': '删除文件', 'getline': '取行', 'getmultiline': '取多行', 'getresp': '取响应', 'getwelcome': '取欢迎语', 'login': '登录', 'makepasv': '建被动端口', 'makeport': '建数据端口', 'mkd': '建目录', 'mlsd': '列机器目录', 'nlst': '列名字', 'ntransfercmd': '建传输', 'putcmd': '发送命令', 'putline': '发送行', 'pwd': '取当前目录', 'rename': '重命名', 'retrbinary': '取二进制', 'retrlines': '取文本行', 'rmd': '删目录', 'sanitize': '清洗参数', 'sendcmd': '执行命令', 'sendeprt': '发送EPRT', 'sendport': '发送PORT', 'set_debuglevel': '设调试级别', 'set_pasv': '设被动模式', 'size': '取大小', 'storbinary': '存二进制', 'storlines': '存文本行', 'transfercmd': '建传输并连接', 'voidcmd': '发送并校验', 'voidresp': '取空响应'}, {'abort': '中止', 'acct': '账号', 'connect': '连接', 'cwd': '切换目录', 'delete': '删除文件', 'getline': '取行', 'getmultiline': '取多行', 'getresp': '取响应', 'getwelcome': '取欢迎语', 'login': '登录', 'makepasv': '建被动端口', 'makeport': '建数据端口', 'mkd': '建目录', 'mlsd': '列机器目录', 'nlst': '列名字', 'ntransfercmd': '建传输', 'putcmd': '发送命令', 'putline': '发送行', 'pwd': '取当前目录', 'rename': '重命名', 'retrbinary': '取二进制', 'retrlines': '取文本行', 'rmd': '删目录', 'sanitize': '清洗参数', 'sendcmd': '执行命令', 'sendeprt': '发送EPRT', 'sendport': '发送PORT', 'set_debuglevel': '设调试级别', 'set_pasv': '设被动模式', 'size': '取大小', 'storbinary': '存二进制', 'storlines': '存文本行', 'transfercmd': '建传输并连接', 'voidcmd': '发送并校验', 'voidresp': '取空响应'})
try:
    import ssl
except ImportError:
    _SSLSocket = None
else:
    _SSLSocket = ssl.SSLSocket

    class FTP安全客户端(FTP客户端):
        """A FTP subclass which adds TLS support to FTP as described
        in RFC-4217.

        Connect as usual to port 21 implicitly securing the FTP control
        connection before authenticating.

        Securing the data connection requires user to explicitly ask
        for it by calling prot_p() method.

        Usage example:
        >>> from ftplib import FTP_TLS
        >>> ftps = FTP_TLS('ftp.python.org')
        >>> ftps.login()  # login anonymously previously securing control channel
        '230 Guest login ok, access restrictions apply.'
        >>> ftps.prot_p()  # switch to secure data connection
        '200 Protection level set to P'
        >>> ftps.retrlines('LIST')  # list directory content securely
        total 9
        drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 .
        drwxr-xr-x   8 root     wheel        1024 Jan  3  1994 ..
        drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 bin
        drwxr-xr-x   2 root     wheel        1024 Jan  3  1994 etc
        d-wxrwxr-x   2 ftp      wheel        1024 Sep  5 13:43 incoming
        drwxr-xr-x   2 root     wheel        1024 Nov 17  1993 lib
        drwxr-xr-x   6 1094     wheel        1024 Sep 13 19:07 pub
        drwxr-xr-x   3 root     wheel        1024 Jan  3  1994 usr
        -rw-r--r--   1 root     root          312 Aug  1  1994 welcome.msg
        '226 Transfer complete.'
        >>> ftps.quit()
        '221 Goodbye.'
        >>>
        """

        def __init__(self, host='', user='', passwd='', acct='', *, context=None, timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None, encoding='utf-8'):
            if context is None:
                context = ssl._create_stdlib_context()
            self.context = context
            self._prot_p = False
            super().__init__(host, user, passwd, acct, timeout, source_address, encoding=encoding)

        def 登录(self, user='', passwd='', acct='', secure=True):
            if secure and (not isinstance(self.sock, ssl.SSLSocket)):
                self.认证()
            return super().login(user, passwd, acct)

        def 认证(self):
            """Set up secure control connection by using TLS/SSL."""
            if isinstance(self.sock, ssl.SSLSocket):
                raise ValueError('Already using TLS')
            if self.context.protocol >= ssl.PROTOCOL_TLS:
                resp = self.发送并校验('AUTH TLS')
            else:
                resp = self.发送并校验('AUTH SSL')
            self.sock = self.context.wrap_socket(self.sock, server_hostname=self.host)
            self.file = self.sock.makefile(mode='r', encoding=self.encoding)
            return resp

        def 清空命令通道(self):
            """Switch back to a clear-text control connection."""
            if not isinstance(self.sock, ssl.SSLSocket):
                raise ValueError('not using TLS')
            resp = self.发送并校验('CCC')
            self.sock = self.sock.unwrap()
            return resp

        def 设数据保护(self):
            """Set up secure data connection."""
            self.发送并校验('PBSZ 0')
            resp = self.发送并校验('PROT P')
            self._prot_p = True
            return resp

        def 设数据明文(self):
            """Set up clear text data connection."""
            resp = self.发送并校验('PROT C')
            self._prot_p = False
            return resp

        def 建传输(self, cmd, rest=None):
            conn, 取大小 = super().ntransfercmd(cmd, rest)
            if self._prot_p:
                conn = self.context.wrap_socket(conn, server_hostname=self.host)
            return (conn, 取大小)

        def 中止(self):
            line = b'ABOR' + B_CRLF
            self.sock.sendall(line)
            resp = self.取多行()
            if resp[:3] not in {'426', '225', '226'}:
                raise 协议错误(resp)
            return resp
    _装类转发(FTP安全客户端, {'abort': '中止', 'auth': '认证', 'ccc': '清空命令通道', 'login': '登录', 'ntransfercmd': '建传输', 'prot_c': '设数据明文', 'prot_p': '设数据保护'}, {'abort': '中止', 'auth': '认证', 'ccc': '清空命令通道', 'getmultiline': '取多行', 'login': '登录', 'ntransfercmd': '建传输', 'prot_c': '设数据明文', 'prot_p': '设数据保护', 'voidcmd': '发送并校验'})
    __all__.append('FTP_TLS')
    全部错误 = (Error, OSError, EOFError, ssl.SSLError)
_150_re = None

def parse150(resp):
    """Parse the '150' response for a RETR request.
    Returns the expected transfer size or None; size is not guaranteed to
    be present in the 150 message.
    """
    if resp[:3] != '150':
        raise 应答错误(resp)
    global _150_re
    if _150_re is None:
        import re
        _150_re = re.compile('150 .* \\((\\d+) bytes\\)', re.IGNORECASE | re.ASCII)
    m = _150_re.match(resp)
    if not m:
        return None
    return int(m.group(1))
_227_re = None

def parse227(resp):
    """Parse the '227' response for a PASV request.
    Raises error_proto if it does not contain '(h1,h2,h3,h4,p1,p2)'
    Return ('host.addr.as.numbers', port#) tuple."""
    if resp[:3] != '227':
        raise 应答错误(resp)
    global _227_re
    if _227_re is None:
        import re
        _227_re = re.compile('(\\d+),(\\d+),(\\d+),(\\d+),(\\d+),(\\d+)', re.ASCII)
    m = _227_re.search(resp)
    if not m:
        raise 协议错误(resp)
    numbers = m.groups()
    host = '.'.join(numbers[:4])
    port = (int(numbers[4]) << 8) + int(numbers[5])
    return (host, port)

def parse229(resp, peer):
    """Parse the '229' response for an EPSV request.
    Raises error_proto if it does not contain '(|||port|)'
    Return ('host.addr.as.numbers', port#) tuple."""
    if resp[:3] != '229':
        raise 应答错误(resp)
    left = resp.find('(')
    if left < 0:
        raise 协议错误(resp)
    right = resp.find(')', left + 1)
    if right < 0:
        raise 协议错误(resp)
    if resp[left + 1] != resp[right - 1]:
        raise 协议错误(resp)
    parts = resp[left + 1:right].split(resp[left + 1])
    if len(parts) != 5:
        raise 协议错误(resp)
    host = peer[0]
    port = int(parts[3])
    return (host, port)

def parse257(resp):
    """Parse the '257' response for a MKD or PWD request.
    This is a response to a MKD or PWD request: a directory name.
    Returns the directoryname in the 257 reply."""
    if resp[:3] != '257':
        raise 应答错误(resp)
    if resp[3:5] != ' "':
        return ''
    dirname = ''
    i = 5
    n = len(resp)
    while i < n:
        c = resp[i]
        i = i + 1
        if c == '"':
            if i >= n or resp[i] != '"':
                break
            i = i + 1
        dirname = dirname + c
    return dirname

def print_line(line):
    """Default retrlines callback to print a line."""
    print(line)

def ftpcp(source, sourcename, target, targetname='', type='I'):
    """Copy file from one FTP-instance to another."""
    if not targetname:
        targetname = sourcename
    type = 'TYPE ' + type
    source.voidcmd(type)
    target.voidcmd(type)
    untrusted_host, sourceport = parse227(source.sendcmd('PASV'))
    if source.trust_server_pasv_ipv4_address:
        sourcehost = untrusted_host
    else:
        sourcehost = source.sock.getpeername()[0]
    target.sendport(sourcehost, sourceport)
    treply = target.sendcmd('STOR ' + targetname)
    if treply[:3] not in {'125', '150'}:
        raise 协议错误
    sreply = source.sendcmd('RETR ' + sourcename)
    if sreply[:3] not in {'125', '150'}:
        raise 协议错误
    source.voidresp()
    target.voidresp()

def test():
    """Test program.
    Usage: ftplib [-d] [-r[file]] host [-l[dir]] [-d[dir]] [-p] [file] ...

    Options:
      -d        increase debugging level
      -r[file]  set alternate ~/.netrc file

    Commands:
      -l[dir]   list directory
      -d[dir]   change the current directory
      -p        toggle passive and active mode
      file      retrieve the file and write it to stdout
    """
    if len(sys.argv) < 2:
        print(test.__doc__)
        sys.exit(0)
    import netrc
    debugging = 0
    rcfile = None
    while sys.argv[1] == '-d':
        debugging = debugging + 1
        del sys.argv[1]
    if sys.argv[1][:2] == '-r':
        rcfile = sys.argv[1][2:]
        del sys.argv[1]
    host = sys.argv[1]
    ftp = FTP客户端(host)
    ftp.set_debuglevel(debugging)
    userid = passwd = 账号 = ''
    try:
        netrcobj = netrc.netrc(rcfile)
    except OSError:
        if rcfile is not None:
            print('Could not open account file -- using anonymous login.', file=sys.stderr)
    else:
        try:
            userid, 账号, passwd = netrcobj.authenticators(host)
        except (KeyError, TypeError):
            print('No account -- using anonymous login.', file=sys.stderr)
    ftp.login(userid, passwd, 账号)
    for file in sys.argv[2:]:
        if file[:2] == '-l':
            ftp.dir(file[2:])
        elif file[:2] == '-d':
            cmd = 'CWD'
            if file[2:]:
                cmd = cmd + ' ' + file[2:]
            resp = ftp.sendcmd(cmd)
        elif file == '-p':
            ftp.set_pasv(not ftp.passiveserver)
        else:
            ftp.retrbinary('RETR ' + file, sys.stdout.buffer.write, 1024)
            sys.stdout.buffer.flush()
        sys.stdout.flush()
    ftp.quit()
if __name__ == '__main__':
    test()


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
    'FTP复制': 'ftpcp',
    'FTP端口': 'FTP_PORT',
    '回车换行': 'CRLF',
    '字节回车换行': 'B_CRLF',
    '带外标志': 'MSG_OOB',
    '打印行': 'print_line',
    '最大行长': 'MAXLINE',
    '解析150': 'parse150',
    '解析227': 'parse227',
    '解析229': 'parse229',
    '解析257': 'parse257',
    '错误': 'Error',
}
globals().update({_中: globals()[_英]
                   for _中, _英 in _本模块别名.items()
                   if _英 in globals()})
_模块别名 = {
    'FTP': 'FTP客户端',
    'FTP_TLS': 'FTP安全客户端',
    'all_errors': '全部错误',
    'error_perm': '永久错误',
    'error_proto': '协议错误',
    'error_reply': '应答错误',
    'error_temp': '临时错误',
}
globals().update({_英: globals()[_中]
                   for _英, _中 in _模块别名.items()
                   if _中 in globals()})

_成员别名 = {
    'FTP安全客户端': {
        'abort': '中止',
        'auth': '认证',
        'ccc': '清空命令通道',
        'login': '登录',
        'ntransfercmd': '建传输',
        'prot_c': '设数据明文',
        'prot_p': '设数据保护',
    },
    'FTP客户端': {
        'abort': '中止',
        'acct': '账号',
        'connect': '连接',
        'cwd': '切换目录',
        'delete': '删除文件',
        'getline': '取行',
        'getmultiline': '取多行',
        'getresp': '取响应',
        'getwelcome': '取欢迎语',
        'login': '登录',
        'makepasv': '建被动端口',
        'makeport': '建数据端口',
        'mkd': '建目录',
        'mlsd': '列机器目录',
        'nlst': '列名字',
        'ntransfercmd': '建传输',
        'putcmd': '发送命令',
        'putline': '发送行',
        'pwd': '取当前目录',
        'rename': '重命名',
        'retrbinary': '取二进制',
        'retrlines': '取文本行',
        'rmd': '删目录',
        'sanitize': '清洗参数',
        'sendcmd': '执行命令',
        'sendeprt': '发送EPRT',
        'sendport': '发送PORT',
        'set_debuglevel': '设调试级别',
        'set_pasv': '设被动模式',
        'size': '取大小',
        'storbinary': '存二进制',
        'storlines': '存文本行',
        'transfercmd': '建传输并连接',
        'voidcmd': '发送并校验',
        'voidresp': '取空响应',
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
    'FTP安全客户端': {
        'abort': '中止',
        'auth': '认证',
        'ccc': '清空命令通道',
        'getmultiline': '取多行',
        'login': '登录',
        'ntransfercmd': '建传输',
        'prot_c': '设数据明文',
        'prot_p': '设数据保护',
        'voidcmd': '发送并校验',
    },
    'FTP客户端': {
        'abort': '中止',
        'acct': '账号',
        'connect': '连接',
        'cwd': '切换目录',
        'delete': '删除文件',
        'getline': '取行',
        'getmultiline': '取多行',
        'getresp': '取响应',
        'getwelcome': '取欢迎语',
        'login': '登录',
        'makepasv': '建被动端口',
        'makeport': '建数据端口',
        'mkd': '建目录',
        'mlsd': '列机器目录',
        'nlst': '列名字',
        'ntransfercmd': '建传输',
        'putcmd': '发送命令',
        'putline': '发送行',
        'pwd': '取当前目录',
        'rename': '重命名',
        'retrbinary': '取二进制',
        'retrlines': '取文本行',
        'rmd': '删目录',
        'sanitize': '清洗参数',
        'sendcmd': '执行命令',
        'sendeprt': '发送EPRT',
        'sendport': '发送PORT',
        'set_debuglevel': '设调试级别',
        'set_pasv': '设被动模式',
        'size': '取大小',
        'storbinary': '存二进制',
        'storlines': '存文本行',
        'transfercmd': '建传输并连接',
        'voidcmd': '发送并校验',
        'voidresp': '取空响应',
    },
}
for _类名, _对 in _实例属性.items():
    _类 = globals().get(_类名)
    if _类 is not None:
        _装类转发(_类, _成员别名.get(_类名, {}), _对)

# __all__：英文原名一个都不能少（硬约束），中文名并排加在后面。
__all__ = type(__all__)(list(__all__) + [
    'FTP复制',
    'FTP安全客户端',
    'FTP客户端',
    'FTP端口',
    '临时错误',
    '全部错误',
    '协议错误',
    '回车换行',
    '字节回车换行',
    '带外标志',
    '应答错误',
    '打印行',
    '最大行长',
    '永久错误',
    '解析150',
    '解析227',
    '解析229',
    '解析257',
    '错误',
])

# ---- 转发层结束 ----
